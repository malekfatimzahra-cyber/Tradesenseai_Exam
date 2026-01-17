from flask import Blueprint, request, jsonify
from models import db, User, UserRole, SystemConfig
from middleware import token_required
import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get full user profile including preferences."""
    # Assuming User model has relation to preferences if implemented, or we use defaults
    # Current schema has user_preferences table but Model might be missing relationship.
    # Let's check if we can query the table directly if model missing.
    
    # Check if UserPreferences model exists, if not, use raw SQL or simple dict
    try:
        from models import UserPreferences
        prefs = UserPreferences.query.filter_by(user_id=current_user.id).first()
        prefs_dict = prefs.to_dict() if prefs else {}
    except ImportError:
        # Fallback if model not defined yet
        prefs_dict = {
            'language': 'en',
            'theme': 'dark', 
            'notifications_enabled': True
        }

    return jsonify({
        'user': current_user.to_dict(),
        'preferences': prefs_dict
    })

@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    
    # Update allowed fields
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    if 'username' in data:
        # Check uniqueness if changed
        if data['username'] != current_user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'message': 'Username taken'}), 409
            current_user.username = data['username']
            
    # Password update
    if 'password' in data and data['password']:
        if len(data['password']) < 6:
             return jsonify({'message': 'Password too short'}), 400
        current_user.set_password(data['password'])
        
    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': current_user.to_dict()})

@user_bp.route('/preferences', methods=['POST'])
@token_required
def update_preferences(current_user):
    data = request.json
    
    # Logic to update user_preferences table
    # Requires UserPreferences model.
    # We will assume it exists or create it.
    
    try:
        from models import UserPreferences
        prefs = UserPreferences.query.filter_by(user_id=current_user.id).first()
        if not prefs:
            prefs = UserPreferences(user_id=current_user.id)
            db.session.add(prefs)
        
        if 'language' in data: prefs.language = data['language']
        if 'theme' in data: prefs.theme = data['theme']
        if 'notifications_enabled' in data: prefs.notifications_enabled = data['notifications_enabled']
        
        db.session.commit()
        return jsonify({'message': 'Preferences updated', 'preferences': prefs.to_dict()})
        
    except ImportError:
        return jsonify({'message': 'Preferences system not active yet'}), 501
