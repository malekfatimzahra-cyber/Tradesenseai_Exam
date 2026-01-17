from app import app
from models import db, User

with app.app_context():
    # Check users
    users = User.query.all()
    print(f"Total users in database: {len(users)}\n")
    
    for user in users:
        print(f"Email: {user.email}")
        print(f"Username: {user.username}")
        print(f"Password Hash: {user.password_hash[:20]}...")
        
        # Test password
        test_pass = 'admin123' if 'admin' in user.email else 'test123'
        check = user.check_password(test_pass)
        print(f"Password '{test_pass}' check: {check}")
        print()
