import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from flask import Flask
from config import get_config
from models import db, User, Account, UserChallenge, Transaction
from sqlalchemy import text

def check_persistence():
    # 1. Inspect Configuration
    config_obj = get_config('development')
    uri = config_obj.SQLALCHEMY_DATABASE_URI
    
    print(f"\n[DIAGNOSTIC] Checking Persistence Configuration...")
    print(f"[-] Database URI: {uri.split('@')[-1] if '@' in uri else uri}") # Hide password
    print(f"[-] Debug Mode: {config_obj.DEBUG}")
    
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    
    with app.app_context():
        try:
            # 2. Check Connection
            db.session.execute(text('SELECT 1'))
            print("[-] Database Connection: SUCCESS")
            
            # 3. List Users (last 5)
            users = User.query.order_by(User.id.desc()).limit(5).all()
            print(f"\n[DATA] Found {len(users)} recent users:")
            for u in users:
                print(f"  - User ID: {u.id} | Email: {u.email} | Created: {u.created_at}")
                
                # Check challenges
                challenges = UserChallenge.query.filter_by(user_id=u.id).all()
                mock_challenges = Account.query.filter_by(user_id=u.id).all()
                payments = Transaction.query.filter_by(user_id=u.id).all()
                
                print(f"    - Active Challenges (UserChallenge): {len(challenges)}")
                for c in challenges:
                    print(f"      > Plan: {c.plan_name} | Status: {c.status}")
                
                print(f"    - Accounts (Trading): {len(mock_challenges)}")
                print(f"    - Payments: {len(payments)}")

        except Exception as e:
            print(f"[!] ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_persistence()
