
import os
import sys
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from sqlalchemy import text

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import db, User, Account, Trade, ChallengeStatus, TradeStatus, TradeType, UserRole

def nuclear_reset_and_seed():
    print("Starting NUCLEAR Leaderboard RESET & SEED...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. NUCLEAR CLEANUP
        print("1. Disabling Foreign Keys and Truncating Tables...")
        try:
            db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            print("   - Truncating tables...")
            db.session.execute(text("TRUNCATE TABLE transactions"))
            db.session.execute(text("TRUNCATE TABLE trades"))
            db.session.execute(text("TRUNCATE TABLE challenges"))
            db.session.execute(text("TRUNCATE TABLE post_likes"))
            db.session.execute(text("TRUNCATE TABLE comments"))
            db.session.execute(text("TRUNCATE TABLE posts"))
            db.session.execute(text("TRUNCATE TABLE floor_messages"))
            # Truncate Accounts (Reset IDs)
            db.session.execute(text("TRUNCATE TABLE accounts"))
            
            # Delete Users (Can't truncate usually due to preserved IDs, but let's try strict delete)
            preserved_emails = ['sara@admin.ma', 'superadmin@tradesense.ma', 'karim@trade.ma']
            # Format list for SQL IN clause
            # 'sara@admin.ma', ...
            # Actually easier to just delete via ORM for users since we want to preserve some
            print("   - Deleting non-admin Users...")
            db.session.execute(text(
                "DELETE FROM users WHERE email NOT IN ('sara@admin.ma', 'superadmin@tradesense.ma', 'karim@trade.ma')"
            ))
            
            db.session.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            db.session.commit()
            print("   Cleanup successful.")
            
        except Exception as e:
            print(f"   Error during nuclear cleanup: {e}")
            db.session.rollback()
            return

        # 2. SEED TOP 10 TRADERS
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
            # Check exist (safety)
            existing = User.query.filter_by(username=t['user']).first()
            if existing: # Should not happen after delete
                continue

            # Create User
            user = User(
                full_name=t['name'],
                username=t['user'],
                email=f"{t['user']}@trade.com",
                role=UserRole.USER,
                password_hash=generate_password_hash("password123")
            )
            db.session.add(user)
            db.session.commit()
            
            # Create Account
            account = Account(
                user_id=user.id,
                plan_name="Elite" if t['balance'] >= 100000 else "Pro",
                initial_balance=t['balance'],
                current_balance=t['balance'] + t['profit'],
                equity=t['balance'] + t['profit'],
                daily_starting_equity=t['balance'] + t['profit'],
                status=ChallengeStatus.ACTIVE,
                reason="Trading Session Active",
                admin_note=f"Rank #{t['rank']} - Verified"
            )
            db.session.add(account)
            db.session.commit()
            
            # Create Trade (Closed)
            trade = Trade(
                account_id=account.id,
                user_id=user.id,
                symbol="XAUUSD",
                side=TradeType.BUY,
                quantity=1.0,
                price=2000.0,
                entry_price=2000.0,
                exit_price=2000.0 + (t['profit'] / 10 if t['profit'] > 0 else 0),
                status=TradeStatus.CLOSED,
                pnl=t['profit'], 
                closed_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.session.add(trade)
            db.session.commit()
            
            print(f"   Seeded Rank #{t['rank']}: {t['name']} (+${t['profit']})")

        print("Done! Nuclear reset complete.")

if __name__ == '__main__':
    nuclear_reset_and_seed()
