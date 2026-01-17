from flask import Blueprint, request, jsonify, current_app
from models import db, User, UserRole, Account, ChallengeStatus
from werkzeug.security import generate_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # 1. Validation
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
        
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', username) # Default full_name to username if not provided

    # 2. Check existing user
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered. Please login.'}), 409
        
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already taken. Please choose another.'}), 409

    # 3. Create new user
    try:
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            role=UserRole.USER
        )
        new_user.set_password(password) # Hashes the password
        
        db.session.add(new_user)
        db.session.flush()  # Get the user ID before commit
        
        # 4. Create default Starter account for the new user
        # This ensures data consistency: every user has at least one account
        default_account = Account(
            user_id=new_user.id,
            plan_name='Starter',
            initial_balance=5000.0,
            current_balance=5000.0,
            equity=5000.0,
            daily_starting_equity=5000.0,
            status=ChallengeStatus.PENDING  # Pending until they pay for a challenge
        )
        db.session.add(default_account)
        
        db.session.commit()
        
        # 5. Generate Token (Auto-login after registration)
        token = jwt.encode({
            'user_id': new_user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': 'Registration successful!',
            'token': token,
            'user': new_user.to_dict(),
            'account': default_account.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user info from JWT token"""
    from middleware import token_required
    
    @token_required
    def _get_user(current_user):
        return jsonify({
            'ok': True,
            'user': current_user.to_dict()
        }), 200
    
    return _get_user()

