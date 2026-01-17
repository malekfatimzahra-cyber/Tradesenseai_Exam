
import os
import sys
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import db, User, Account, Trade, ChallengeStatus, TradeStatus, TradeType, UserRole

def seed_moroccan_v2():
    print("Seeding 10 Moroccan Traders (v2)...")
    
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
            try:
                # 1. Create User
                user = User.query.filter_by(username=t['user']).first()
                if not user:
                    user = User(
                        full_name=t['name'],
                        username=t['user'],
                        email=f"{t['user']}@trade.ma",
                        role=UserRole.USER,
                        password_hash=generate_password_hash("maroc123")
                    )
                    db.session.add(user)
                    db.session.commit()
                    print(f"Created User: {user.username} (ID: {user.id})")
                
                # 2. Create Account
                # Check for existing account
                account = Account.query.filter_by(user_id=user.id).first()
                if not account:
                    account = Account(
                        user_id=user.id,
                        plan_name="Elite" if t['balance'] >= 100000 else "Pro",
                        initial_balance=t['balance'],
                        current_balance=t['balance'] + t['profit'],
                        equity=t['balance'] + t['profit'],
                        daily_starting_equity=t['balance'] + t['profit'],
                        status=ChallengeStatus.ACTIVE,
                        reason="Trading Active",
                        admin_note="Moroccan Trader"
                    )
                    db.session.add(account)
                    db.session.commit()
                    print(f"Created Account ID: {account.id}")

                # 3. Create Trade (if not exists)
                # We check if this user has any trades
                if not Trade.query.filter_by(user_id=user.id).first():
                    trade = Trade(
                        account_id=account.id,
                        user_id=user.id,
                        symbol="EURUSD",
                        side=TradeType.SELL, # Use Enum
                        quantity=2.0,
                        price=1.1000,
                        entry_price=1.1000,
                        exit_price=1.0900,
                        status=TradeStatus.CLOSED, # Use Enum
                        pnl=t['profit'], 
                        closed_at=datetime.utcnow()
                    )
                    db.session.add(trade)
                    db.session.commit()
                    print(f"Created Profit Trade for {t['name']}")
                else:
                    print(f"Trades exist for {t['name']}")

            except Exception as e:
                db.session.rollback()
                print(f"Error processing {t['name']}: {e}")
                import traceback
                traceback.print_exc()

        print("Seeding Complete.")

if __name__ == '__main__':
    seed_moroccan_v2()
