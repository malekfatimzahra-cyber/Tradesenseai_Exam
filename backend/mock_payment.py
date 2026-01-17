from models import db, UserChallenge
from flask import Blueprint, request, jsonify
from middleware import token_required
from datetime import datetime

mock_payment_bp = Blueprint('mock_payment', __name__)

@mock_payment_bp.route('/mock-payment', methods=['POST'])
@token_required
def mock_payment(current_user):
    try:
        data = request.get_json()
        
        # Validate input
        plan = data.get('plan') # Starter, Pro, Elite
        amount = data.get('amount')
        payment_method = data.get('payment_method') # CMI or Crypto
        
        if not all([plan, amount, payment_method]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
            
        # Create UserChallenge record
        new_challenge = UserChallenge(
            user_id=current_user.id,
            plan_name=plan,
            amount=amount,
            payment_method=payment_method,
            status='active',
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_challenge)
        
        # Also create the Account for trading access (System requirement)
        # This keeps the system functional while fulfilling the specific exam requirement for UserChallenge table
        from models import Account, ChallengeStatus
        
        initial_balances = {
            'Starter': 5000.0,
            'Starter Challenge': 5000.0,
            'Pro': 25000.0,
            'Professional Pro': 25000.0,
            'Elite': 100000.0,
            'Elite Institutional': 100000.0
        }
        
        initial_equity = initial_balances.get(plan, 5000.0)
        
        account = Account(
            user_id=current_user.id,
            plan_name=plan,
            initial_balance=initial_equity,
            current_balance=initial_equity,
            equity=initial_equity,
            daily_starting_equity=initial_equity,
            status=ChallengeStatus.ACTIVE
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Payment simulated', 
            'challengeId': new_challenge.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
