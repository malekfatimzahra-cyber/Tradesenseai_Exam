from flask import Blueprint, request, jsonify, redirect
from models import db, Transaction, User, Account, ChallengeStatus, PaymentMethod, PaymentStatus, SystemConfig, UserRole
from functools import wraps
import jwt
import paypalrestsdk
from datetime import datetime
import traceback

payments_bp = Blueprint('payments', __name__)

# --- Helper: Configure PayPal ---
def configure_paypal():
    try:
        client_id_config = SystemConfig.query.get('PAYPAL_CLIENT_ID')
        secret_config = SystemConfig.query.get('PAYPAL_SECRET')
        
        if client_id_config and secret_config:
            paypalrestsdk.configure({
                "mode": "sandbox", # sandbox or live
                "client_id": client_id_config.value,
                "client_secret": secret_config.value 
            })
            return True
        return False
    except Exception as e:
        print(f"Error configuring PayPal: {e}")
        return False

from middleware import token_required

def superadmin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != UserRole.SUPERADMIN:
            return jsonify({'message': 'SuperAdmin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# --- Routes ---

@payments_bp.route('/mock-checkout', methods=['POST'])
@token_required
def mock_checkout(current_user):
    """
    POST /api/payments/mock-checkout
    body: { plan, provider }
    behavior:
    - simulate loading
    - create row in user_challenges (Account table)
    - return challenge_id
    """
    try:
        # Check for existing active challenge
        existing_active = Account.query.filter_by(
            user_id=current_user.id, 
            status=ChallengeStatus.ACTIVE
        ).first()
        
        if existing_active:
            return jsonify({
                'ok': False,
                'message': 'You already have an active challenge. Complete or fail it before starting a new one.'
            }), 400

        data = request.json
        plan_id = data.get('plan', 'Starter').lower()
        provider = data.get('provider', 'Mock')

        # Plan configurations
        plan_config = {
            'starter': {'funding': 5000, 'price': 200},
            'pro': {'funding': 25000, 'price': 500},
            'elite': {'funding': 100000, 'price': 1000}
        }
        
        config = plan_config.get(plan_id, plan_config['starter'])
        capital = config['funding']
        price = config['price']

        # 1. Record Transaction
        tx = Transaction(
            user_id=current_user.id,
            amount=float(price),
            payment_method=PaymentMethod.CMI if provider != 'PayPal' else PaymentMethod.PAYPAL,
            status=PaymentStatus.COMPLETED,
            transaction_id=f"MOCK-{int(datetime.utcnow().timestamp())}"
        )
        db.session.add(tx)
        
        # 2. Create Challenge Account
        new_account = Account(
            user_id=current_user.id,
            plan_name=plan_id.capitalize(),
            initial_balance=capital,
            current_balance=capital,
            equity=capital,
            daily_starting_equity=capital,
            status=ChallengeStatus.ACTIVE
        )
        db.session.add(new_account)
        db.session.commit()
        
        # Link tx to account
        tx.account_id = new_account.id
        db.session.commit()

        return jsonify({
            'ok': True,
            'message': 'Challenge started successfully!',
            'challenge_id': new_account.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL ERROR in /mock-checkout: {str(e)}")
        traceback.print_exc()
        return jsonify({'ok': False, 'message': f'Server Error: {str(e)}'}), 500


# --- PayPal Routes ---

@payments_bp.route('/paypal/create', methods=['POST'])
@token_required
def create_paypal_payment(current_user):
    try:
        if not configure_paypal():
            return jsonify({'message': 'PayPal not configured by Admin'}), 503

        data = request.json
        amount = data.get('amount')
        plan_id = data.get('planId')
        
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"https://faty2002.pythonanywhere.com/api/payments/paypal/execute?user_id={current_user.id}&plan={plan_id}",
                "cancel_url": "https://faty2002.pythonanywhere.com/api/payments/paypal/cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"TradeSense {plan_id} Challenge",
                        "sku": plan_id,
                        "price": str(amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "description": f"Challenge Plan {plan_id}"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return jsonify({'approval_url': link.href})
            return jsonify({'message': 'Approval URL not found'}), 500
        else:
            return jsonify({'error': payment.error}), 400
    except Exception as e:
        print(f"Error creating PayPal payment: {e}")
        traceback.print_exc()
        return jsonify({'message': f'Server Error: {str(e)}'}), 500

@payments_bp.route('/paypal/execute', methods=['GET'])
def execute_paypal_payment():
    # Public endpoint called by PayPal redirect
    try:
        if not configure_paypal():
            return jsonify({'message': 'System Error'}), 503

        payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')
        user_id = request.args.get('user_id')
        plan_id = request.args.get('plan')
        
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Payment Success
            user = User.query.get(user_id)
            if not user:
                return "User not found", 404

            capital_map = {'starter': 5000, 'pro': 25000, 'elite': 100000}
            capital = capital_map.get(plan_id.lower(), 5000)

            new_account = Account(
                user_id=user.id,
                plan_name=plan_id.capitalize(),
                initial_balance=capital,
                current_balance=capital,
                equity=capital,
                daily_starting_equity=capital,
                status=ChallengeStatus.ACTIVE
            )
            db.session.add(new_account)
            db.session.commit()
            
            tx = Transaction(
                user_id=user.id,
                account_id=new_account.id,
                amount=float(payment.transactions[0].amount.total),
                payment_method=PaymentMethod.PAYPAL,
                status=PaymentStatus.COMPLETED,
                transaction_id=payment.id
            )
            db.session.add(tx)
            db.session.commit()

            # Redirect to Frontend Success Page
            return redirect("http://localhost:5173/challenges?payment=success")
        else:
            return redirect("http://localhost:5173/challenges?payment=failed")
            
    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL ERROR in execute_paypal_payment: {str(e)}")
        traceback.print_exc()
        # Redirect with error param so frontend can show something
        return redirect(f"http://localhost:5173/challenges?payment=error&message={str(e)}")

@payments_bp.route('/paypal/cancel', methods=['GET'])
def cancel_paypal_payment():
    return redirect("http://localhost:5173/challenges?payment=cancelled")

@payments_bp.route('/paypal-availability', methods=['GET'])
def get_paypal_availability():
    """Public endpoint for frontend to check if PayPal is enabled"""
    try:
        is_available = configure_paypal()
        # Check for PayPal email as well as per requirements
        paypal_email = SystemConfig.query.get('PAYPAL_EMAIL')
        
        return jsonify({
            'enabled': is_available,
            'email_configured': bool(paypal_email and paypal_email.value)
        }), 200
    except Exception as e:
        return jsonify({'enabled': False, 'error': str(e)}), 500

# --- SuperAdmin Config ---

@payments_bp.route('/config/paypal', methods=['POST'])
@token_required
@superadmin_required
def set_paypal_config(current_user):
    try:
        data = request.json
        client_id = data.get('client_id')
        secret = data.get('secret')
        email = data.get('email')
        
        # Save Client ID
        conf_id = SystemConfig.query.get('PAYPAL_CLIENT_ID')
        if not conf_id: 
            conf_id = SystemConfig(key='PAYPAL_CLIENT_ID')
            db.session.add(conf_id)
        conf_id.value = client_id
        
        # Save Secret
        conf_sec = SystemConfig.query.get('PAYPAL_SECRET')
        if not conf_sec: 
            conf_sec = SystemConfig(key='PAYPAL_SECRET')
            db.session.add(conf_sec)
        conf_sec.value = secret

        # Save Email
        conf_email = SystemConfig.query.get('PAYPAL_EMAIL')
        if not conf_email:
            conf_email = SystemConfig(key='PAYPAL_EMAIL')
            db.session.add(conf_email)
        conf_email.value = email
        
        db.session.commit()
        return jsonify({'message': 'PayPal Configuration Saved'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error saving PayPal config: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

@payments_bp.route('/config/paypal', methods=['GET'])
@token_required
@superadmin_required
def get_paypal_config(current_user):
    try:
        conf_id = SystemConfig.query.get('PAYPAL_CLIENT_ID')
        conf_email = SystemConfig.query.get('PAYPAL_EMAIL')
        return jsonify({
            'client_id': conf_id.value if conf_id else '',
            'email': conf_email.value if conf_email else '',
            'is_configured': bool(conf_id and conf_id.value)
        })
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
