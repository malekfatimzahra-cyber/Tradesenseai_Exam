from flask import Blueprint, request, jsonify
from models import db, SystemConfig
from middleware import token_required
from models import UserRole

paypal_config_bp = Blueprint('paypal_config', __name__)

@paypal_config_bp.route('/status', methods=['GET'])
def get_paypal_status():
    """Get PayPal configuration status (public)"""
    try:
        client_id = SystemConfig.query.filter_by(key='PAYPAL_CLIENT_ID').first()
        client_secret = SystemConfig.query.filter_by(key='PAYPAL_CLIENT_SECRET').first()
        paypal_email = SystemConfig.query.filter_by(key='PAYPAL_EMAIL').first()
        sandbox_mode = SystemConfig.query.filter_by(key='PAYPAL_SANDBOX_MODE').first()
        
        is_sandbox = sandbox_mode.value == 'true' if sandbox_mode else True
        has_credentials = bool(client_id and client_id.value and client_secret and client_secret.value)
        
        return jsonify({
            'enabled': has_credentials,
            'email_configured': bool(paypal_email and paypal_email.value),
            'email': paypal_email.value if paypal_email else None,
            'sandbox_mode': is_sandbox,
            'client_id': client_id.value if client_id else None
        }), 200
    except Exception as e:
        return jsonify({'enabled': False, 'error': str(e)}), 200

@paypal_config_bp.route('/config', methods=['GET'])
@token_required
def get_paypal_config(current_user):
    """Get PayPal configuration (SuperAdmin only)"""
    if current_user.role != UserRole.SUPERADMIN:
        return jsonify({'message': 'SuperAdmin access required'}), 403
    
    try:
        client_id = SystemConfig.query.filter_by(key='PAYPAL_CLIENT_ID').first()
        client_secret = SystemConfig.query.filter_by(key='PAYPAL_CLIENT_SECRET').first()
        paypal_email = SystemConfig.query.filter_by(key='PAYPAL_EMAIL').first()
        sandbox_mode = SystemConfig.query.filter_by(key='PAYPAL_SANDBOX_MODE').first()
        
        return jsonify({
            'client_id': client_id.value if client_id else '',
            'client_secret': client_secret.value if client_secret else '',
            'email': paypal_email.value if paypal_email else '',
            'sandbox_mode': sandbox_mode.value == 'true' if sandbox_mode else True
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@paypal_config_bp.route('/config', methods=['POST'])
@token_required
def update_paypal_config(current_user):
    """Update PayPal configuration (SuperAdmin only)"""
    if current_user.role != UserRole.SUPERADMIN:
        return jsonify({'message': 'SuperAdmin access required'}), 403
    
    try:
        data = request.get_json()
        
        # Update or create config entries
        configs = {
            'PAYPAL_CLIENT_ID': data.get('client_id', ''),
            'PAYPAL_CLIENT_SECRET': data.get('client_secret', ''),
            'PAYPAL_EMAIL': data.get('email', ''),
            'PAYPAL_SANDBOX_MODE': 'true' if data.get('sandbox_mode', True) else 'false'
        }
        
        for key, value in configs.items():
            config = SystemConfig.query.filter_by(key=key).first()
            if config:
                config.value = value
            else:
                config = SystemConfig(key=key, value=value)
                db.session.add(config)
        
        db.session.commit()
        
        return jsonify({
            'message': 'PayPal configuration updated successfully',
            'success': True
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
