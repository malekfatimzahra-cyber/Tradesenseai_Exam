"""
Unified Payment Handler - PRODUCTION READY
Routes handling all payment methods with full SQL persistence
"""
from flask import Blueprint, request, jsonify
from models import db, Account, Transaction, UserChallenge, PaymentMethod, PaymentStatus, ChallengeStatus
from middleware import token_required
from datetime import datetime
import traceback

unified_payment_bp = Blueprint('unified_payment', __name__)

@unified_payment_bp.route('/process', methods=['POST'])
@token_required
def process_payment(current_user):
    """
    Universal payment processor for ALL methods: PayPal, CMI, Crypto
    
    Payload:
    {
        "plan": "Starter" | "Pro" | "Elite",
        "amount": 200,
        "payment_method": "PAYPAL" | "CMI" | "CRYPTO",
        "transaction_id": "optional-external-id"
    }
    
    GARANTIT:
    1. Transaction record (payments table)
    2. Account record (accounts table)
    3. UserChallenge record (user_challenges table)
    4. ATOMIC: All or nothing
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        plan = data.get('plan')
        amount = data.get('amount')
        payment_method_str = data.get('payment_method', 'PAYPAL').upper()
        transaction_id_external = data.get('transaction_id')
        
        if not plan or not amount:
            return jsonify({'success': False, 'message': 'Missing plan or amount'}), 400
        
        # Map plan to balance
        balance_map = {
            'Starter': 5000,
            'Starter Challenge': 5000,
            'Pro': 25000,
            'Professional Pro': 25000,
            'Elite': 100000,
            'Elite Institutional': 100000
        }
        initial_balance = balance_map.get(plan, 5000)
        
        # Convert payment method to enum
        try:
            payment_method_enum = PaymentMethod[payment_method_str]
        except KeyError:
            payment_method_enum = PaymentMethod.PAYPAL
        
        # ========================================
        # TRANSACTION SQL ATOMIQUE
        # ========================================
        db.session.begin_nested()  # START SAVEPOINT
        
        try:
            # 1. CREATE TRANSACTION RECORD
            transaction = Transaction(
                user_id=current_user.id,
                amount=amount,
                currency='MAD',
                payment_method=payment_method_enum,
                status=PaymentStatus.COMPLETED,
                transaction_id=transaction_id_external or f"TXN_{datetime.utcnow().timestamp()}_{current_user.id}",
                created_at=datetime.utcnow()
            )
            db.session.add(transaction)
            db.session.flush()  # Get ID
            
            # 2. CREATE ACCOUNT (Trading Account)
            account = Account(
                user_id=current_user.id,
                plan_name=plan,
                initial_balance=initial_balance,
                current_balance=initial_balance,
                equity=initial_balance,
                daily_starting_equity=initial_balance,
                status=ChallengeStatus.ACTIVE,
                reason="Challenge Activated",
                admin_note=f"Payment via {payment_method_str}",
                created_at=datetime.utcnow()
            )
            db.session.add(account)
            db.session.flush()  # Get ID
            
            # Link transaction to account
            transaction.account_id = account.id
            
            # 3. CREATE USER_CHALLENGE RECORD
            user_challenge = UserChallenge(
                user_id=current_user.id,
                plan_name=plan,
                amount=amount,
                payment_method=payment_method_str,
                status='active',
                created_at=datetime.utcnow()
            )
            db.session.add(user_challenge)
            
            # COMMIT ALL
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Challenge {plan} activated successfully',
                'data': {
                    'account_id': account.id,
                    'challenge_id': user_challenge.id,
                    'transaction_id': transaction.id,
                    'balance': initial_balance,
                    'status': 'ACTIVE'
                },
                'redirect_url': '/terminal'
            }), 200
            
        except Exception as inner_e:
            db.session.rollback()
            raise inner_e
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Payment processing error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error processing payment: {str(e)}'
        }), 500


@unified_payment_bp.route('/history', methods=['GET'])
@token_required
def get_payment_history(current_user):
    """Get user's payment history"""
    try:
        payments = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in payments]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@unified_payment_bp.route('/active-challenge', methods=['GET'])
@token_required
def get_active_challenge(current_user):
    """
    Get user's currently active challenge
    This is what the frontend calls after login to restore state
    """
    try:
        # Find most recent ACTIVE account
        account = Account.query.filter_by(
            user_id=current_user.id,
            status=ChallengeStatus.ACTIVE
        ).order_by(Account.created_at.desc()).first()
        
        if not account:
            return jsonify({
                'success': True,
                'data': None,
                'message': 'No active challenge found'
            }), 200
        
        # Also get associated challenge record if exists
        challenge = UserChallenge.query.filter_by(
            user_id=current_user.id,
            status='active'
        ).order_by(UserChallenge.created_at.desc()).first()
        
        return jsonify({
            'success': True,
            'data': {
                'id': account.id,
                'plan_name': account.plan_name,
                'initial_balance': account.initial_balance,
                'current_balance': account.current_balance,
                'equity': account.equity,
                'daily_starting_equity': account.daily_starting_equity,
                'status': account.status.value,
                'created_at': account.created_at.isoformat(),
                'challenge_id': challenge.id if challenge else None
            }
        }), 200
    except Exception as e:
        print(f"Error fetching active challenge: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
