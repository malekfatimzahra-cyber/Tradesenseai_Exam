import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.getcwd())

load_dotenv()

from __init__ import create_app
from models import db, User, Account, Trade, UserRole, ChallengeStatus, TradeType, TradeStatus, Challenge

def import_data():
    print("🔄 Importing data into MySQL...")
    
    if not os.path.exists('backup_data.json'):
        print("❌ Backup file backup_data.json not found!")
        return

    with open('backup_data.json', 'r') as f:
        data = json.load(f)

    app = create_app()
    
    with app.app_context():
        try:
            # Create tables first
            db.create_all()
            print("✅ Database tables ensured.")

            # Clear existing data if any (optional, be careful)
            # db.drop_all()
            # db.create_all()

            # Map old IDs to new objects if necessary
            user_map = {}
            
            # Import Users
            print(f"👤 Importing {len(data['users'])} users...")
            for u_data in data['users']:
                # Check if user already exists
                existing_user = User.query.filter_by(email=u_data['email']).first()
                if existing_user:
                    print(f"   - User {u_data['email']} already exists, skipping.")
                    user_map[u_data['id']] = existing_user
                    continue

                user = User(
                    full_name=u_data['full_name'],
                    username=u_data['username'],
                    email=u_data['email'],
                    password_hash=u_data['password_hash'],
                    role=UserRole[u_data['role']] if u_data['role'] in UserRole.__members__ else UserRole.USER,
                    created_at=datetime.fromisoformat(u_data['created_at']) if u_data.get('created_at') else datetime.utcnow()
                )
                db.session.add(user)
                db.session.commit()
                user_map[u_data['id']] = user

            # Import Accounts
            print(f"💳 Importing {len(data['accounts'])} accounts...")
            account_map = {}
            for a_data in data['accounts']:
                user = user_map.get(a_data['user_id'])
                if not user:
                    print(f"   - Skipping account {a_data['id']} (no user found).")
                    continue

                account = Account(
                    user_id=user.id,
                    plan_name=a_data.get('plan_name', 'Starter'),
                    initial_balance=a_data['initial_balance'],
                    current_balance=a_data['current_balance'],
                    equity=a_data['equity'],
                    status=ChallengeStatus[a_data['status']] if a_data['status'] in ChallengeStatus.__members__ else ChallengeStatus.ACTIVE,
                    created_at=datetime.fromisoformat(a_data['created_at']) if a_data.get('created_at') else datetime.utcnow()
                )
                db.session.add(account)
                db.session.commit()
                account_map[a_data['id']] = account

            # Import Trades
            print(f"📈 Importing {len(data['trades'])} trades...")
            for t_data in data['trades']:
                # Handle missing user_id in legacy data
                user_id_val = t_data.get('user_id')
                user = user_map.get(user_id_val) if user_id_val else None
                
                account = account_map.get(t_data['account_id'])
                
                if not user:
                    # Try to get user from account if trade user_id is missing
                    if account:
                        user = account.user
                
                if not user:
                    print(f"   - Skipping trade {t_data['id']} (no user found).")
                    continue

                # Map legacy fields to new schema
                side_val = t_data.get('side', t_data.get('trade_type', 'BUY'))
                qty_val = t_data.get('quantity', t_data.get('amount', 0.0))
                price_val = t_data.get('price', t_data.get('entry_price', 0.0))
                
                # Check enum validity
                side_enum = TradeType.BUY
                if side_val in TradeType.__members__:
                    side_enum = TradeType[side_val]
                elif side_val == 'SELL':
                    side_enum = TradeType.SELL
                
                status_val = t_data.get('status', 'OPEN')
                status_enum = TradeStatus.OPEN
                if status_val in TradeStatus.__members__:
                    status_enum = TradeStatus[status_val]

                timestamp_val = None
                if t_data.get('timestamp'):
                    timestamp_val = datetime.fromisoformat(t_data.get('timestamp'))
                elif t_data.get('created_at'):
                    timestamp_val = datetime.fromisoformat(t_data.get('created_at'))
                else:
                    timestamp_val = datetime.utcnow()

                trade = Trade(
                    account_id=account.id if account else None,
                    user_id=user.id,
                    symbol=t_data['symbol'],
                    side=side_enum,
                    quantity=qty_val,
                    price=price_val,
                    status=status_enum,
                    pnl=t_data.get('pnl', 0.0),
                    timestamp=timestamp_val
                )
                db.session.add(trade)
            
            db.session.commit()
            print("✅ Data migration complete!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Import failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import_data()
