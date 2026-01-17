from flask import Blueprint, request, jsonify
from models import db, Account, Transaction, PaymentMethod, PaymentStatus, ChallengeStatus
from middleware import token_required
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/success', methods=['POST'])
@token_required
def payment_success(current_user):
    """
    Handle successful payment and create challenge account.
    Payload: { challenge_type, payment_method, transaction_id, amount }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        challenge_type = data.get('challenge_type', 'Starter')
        payment_method_str = data.get('payment_method', 'PAYPAL')
        transaction_id = data.get('transaction_id')
        amount = data.get('amount', 200)
        
        # Map challenge type to initial balance
        balance_map = {
            'Starter': 5000,
            'Pro': 25000,
            'Elite': 100000
        }
        initial_balance = balance_map.get(challenge_type, 5000)
        
        # Convert payment method string to enum
        try:
            payment_method_enum = PaymentMethod[payment_method_str.upper()]
        except KeyError:
            payment_method_enum = PaymentMethod.PAYPAL
        
        # 1. Create Transaction Record
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            currency='MAD',
            payment_method=payment_method_enum,
            status=PaymentStatus.COMPLETED,
            transaction_id=transaction_id or f"TXN_{datetime.utcnow().timestamp()}",
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.flush()  # Get transaction ID
        
        # 2. Create Challenge Account
        account = Account(
            user_id=current_user.id,
            plan_name=challenge_type,
            initial_balance=initial_balance,
            current_balance=initial_balance,
            equity=initial_balance,
            daily_starting_equity=initial_balance,
            status=ChallengeStatus.ACTIVE,
            reason="Challenge Active",
            admin_note=f"Activated via {payment_method_str}",
            created_at=datetime.utcnow()
        )
        db.session.add(account)
        db.session.flush()
        
        # Link transaction to account
        transaction.account_id = account.id

        # 3. Create UserChallenge record (Exam Requirement)
        from models import UserChallenge
        user_challenge = UserChallenge(
            user_id=current_user.id,
            plan_name=challenge_type,
            amount=amount,
            payment_method=payment_method_str,
            status='active',
            created_at=datetime.utcnow()
        )
        db.session.add(user_challenge)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Challenge activated successfully',
            'account_id': account.id,
            'redirect_url': '/terminal'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Payment activation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error activating challenge: {str(e)}'
        }), 500
