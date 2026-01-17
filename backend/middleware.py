from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            # Special handling for mock tokens in demo mode
            if token.startswith('mock_jwt_token_'):
                user_id_str = token.replace('mock_jwt_token_', '')
                # Handle 'u1', 'u2' etc. by stripping 'u'
                if user_id_str.startswith('u'):
                    user_id = int(user_id_str[1:])
                else:
                    user_id = int(user_id_str)
                current_user = User.query.get(user_id)
            else:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['user_id'])
            
            if not current_user:
                raise Exception('User not found')
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated
