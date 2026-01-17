
import os
import sys
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import db, User, Account, Trade, ChallengeStatus, TradeStatus, TradeType, UserRole, Transaction

def reset_and_seed():
    print("Starting Leaderboard RESET & SEED (v2)...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. DELETE EXISTING DATA (Clean Slate)
        print("1. Deleting existing Data (keeping SuperAdmins)...")
        try:
            # Delete Transactions first (Foreign Key to Accounts)
            print("   - Deleting Transactions...")
            db.session.query(Transaction).delete()
            
            # Delete Trades (Foreign Key to Accounts)
            print("   - Deleting Trades...")
            db.session.query(Trade).delete()
            
            # Delete Accounts
            print("   - Deleting Accounts...")
            db.session.query(Account).delete()
            
            # Delete Users (Except defaults)
            print("   - Deleting Users...")
            preserved_emails = ['sara@admin.ma', 'superadmin@tradesense.ma', 'karim@trade.ma']
            
            count = db.session.query(User).filter(User.email.notin_(preserved_emails)).delete(synchronize_session=False)
            db.session.commit()
            print(f"   Deleted {count} old users.")
            
        except Exception as e:
            db.session.rollback()
            print(f"   Error clearing data: {e}")
            return

        # 2. SEED TOP 10 TRADERS (Strict Ranking)
        print("2. Seeding Top 10 Elite Traders...")
        
        traders_config = [
            {"rank": 1, "name": "Alex Momentum", "user": "alex_pro", "profit": 25400, "balance": 100000},
            {"rank": 2, "name": "Sarah Sniper",   "user": "sarah_x", "profit": 21200, "balance": 100000},
            {"rank": 3, "name": "Mike Macro",     "user": "mike_m",  "profit": 18900, "balance": 100000},
            {"rank": 4, "name": "Emma Elliott",   "user": "emma_e",  "profit": 15600, "balance": 50000},
            {"rank": 5, "name": "David Day",      "user": "david_d", "profit": 12400, "balance": 50000},
            {"rank": 6, "name": "Lucas Long",     "user": "lucas_l", "profit": 9800,  "balance": 50000},
            {"rank": 7, "name": "Julia Just",     "user": "julia_j", "profit": 7500,  "balance": 25000},
            {"rank": 8, "name": "Tom Trend",      "user": "tom_t",   "profit": 6200,  "balance": 25000},
            {"rank": 9, "name": "Ryan Risk",      "user": "ryan_r",  "profit": 4100,  "balance": 10000},
            {"rank": 10,"name": "Nina News",      "user": "nina_n",  "profit": 2300,  "balance": 10000},
        ]

        for t in traders_config:
            # Create User
            email = f"{t['user']}@trade.com"
            user = User(
                full_name=t['name'],
                username=t['user'],
                email=email,
                role=UserRole.USER,
                password_hash=generate_password_hash("password123")
            )
            db.session.add(user)
            db.session.commit()
            
            # Create Account
            account = Account(
                user_id=user.id,
                plan_name="Elite" if t['balance'] >= 100000 else ("Pro" if t['balance'] >= 50000 else "Starter"),
                initial_balance=t['balance'],
                current_balance=t['balance'] + t['profit'],
                equity=t['balance'] + t['profit'],
                daily_starting_equity=t['balance'] + t['profit'],
                status=ChallengeStatus.ACTIVE,
                reason="Trading Session Active",
                admin_note=f"Rank #{t['rank']} - Verified Performance"
            )
            db.session.add(account)
            db.session.commit()
            
            # Create Trade
            trade = Trade(
                account_id=account.id,
                user_id=user.id,
                symbol="XAUUSD",
                side=TradeType.BUY,
                quantity=1.0,
                price=2000.0,
                entry_price=2000.0,
                exit_price=2000.0 + (t['profit'] / 10),
                status=TradeStatus.CLOSED,
                pnl=t['profit'], 
                closed_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            )
            db.session.add(trade)
            db.session.commit()
            
            print(f"   Seeded Rank #{t['rank']}: {t['name']} (+${t['profit']})")

        print("Done! Database updated with clean Top 10.")

if __name__ == '__main__':
    reset_and_seed()
