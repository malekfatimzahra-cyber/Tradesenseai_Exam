
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
from models import db, User, Account, Trade, ChallengeStatus, TradeStatus, TradeType, UserRole

def seed_moroccan_traders():
    print("Seeding 10 Moroccan Traders into MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        moroccan_traders = [
            {"name": "Youssef Benali", "user": "youssef_fx", "profit": 18500, "balance": 100000},
            {"name": "Fatima Zahra",   "user": "fatima_z",   "profit": 16200, "balance": 100000},
            {"name": "Amine Tazi",     "user": "amine_tr",   "profit": 14800, "balance": 50000},
            {"name": "Hajar Idrissi",  "user": "hajar_id",   "profit": 11500, "balance": 50000},
            {"name": "Omar Berrada",   "user": "omar_b",     "profit": 9200,  "balance": 50000},
            {"name": "Salma Bennani",  "user": "salma_b",    "profit": 8700,  "balance": 25000},
            {"name": "Mehdi Alaoui",   "user": "mehdi_al",   "profit": 6500,  "balance": 25000},
            {"name": "Zineb El Fassi", "user": "zineb_el",   "profit": 5100,  "balance": 10000},
            {"name": "Tariq Mansouri", "user": "tariq_m",    "profit": 3400,  "balance": 10000},
            {"name": "Nadia Chraibi",  "user": "nadia_ch",   "profit": 1200,  "balance": 10000},
        ]

        for t in moroccan_traders:
            # Check if user exists to avoid duplicates
            if User.query.filter_by(username=t['user']).first():
                print(f"User {t['user']} already exists, skipping.")
                continue

            # 1. Create User
            user = User(
                full_name=t['name'],
                username=t['user'],
                email=f"{t['user']}@trade.ma", # Moroccan domain for flair
                role=UserRole.USER,
                password_hash=generate_password_hash("maroc123")
            )
            db.session.add(user)
            db.session.commit()
            
            # 2. Create Account (Challenge)
            account = Account(
                user_id=user.id,
                plan_name="Elite" if t['balance'] >= 100000 else ("Pro" if t['balance'] >= 50000 else "Starter"),
                initial_balance=t['balance'],
                current_balance=t['balance'] + t['profit'],
                equity=t['balance'] + t['profit'],
                daily_starting_equity=t['balance'] + t['profit'],
                status=ChallengeStatus.ACTIVE,
                reason="Trading Active",
                admin_note="Moroccan Trader - Verified"
            )
            db.session.add(account)
            db.session.commit()
            
            # 3. Create Trades (To show on Leaderboard)
            # Create a single winning trade to establish the PnL
            trade = Trade(
                account_id=account.id,
                user_id=user.id,
                symbol="EURUSD",
                side=TradeType.SELL,
                quantity=2.0,
                price=1.1000,
                entry_price=1.1000,
                exit_price=1.0900, # Profitable move
                status=TradeStatus.CLOSED,
                pnl=t['profit'], 
                closed_at=datetime.utcnow() - timedelta(days=random.randint(0, 5))
            )
            db.session.add(trade)
            db.session.commit()
            
            print(f"Added: {t['name']} (+{t['profit']} MAD)")

        print("Done! 10 Moroccan traders added to Leaderboard.")

if __name__ == '__main__':
    seed_moroccan_traders()
