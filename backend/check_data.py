
import os
import sys

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import User, Account

def check_data():
    app = create_app('development')
    with app.app_context():
        user_count = User.query.count()
        account_count = Account.query.count()
        print(f"Total Users: {user_count}")
        print(f"Total Accounts: {account_count}")
        
        print("\n--- Recent Accounts ---")
        accounts = Account.query.order_by(Account.created_at.desc()).limit(10).all()
        for acc in accounts:
            print(f"User: {acc.user.username} | Equity: ${acc.equity:,.2f} | Status: {acc.status.value}")

if __name__ == '__main__':
    check_data()
