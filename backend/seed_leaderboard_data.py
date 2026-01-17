
import os
import sys
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add 'backend' to path so we can import modules as if we are inside it
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Now import directly from the modules
from __init__ import create_app
from models import db, User, Account, Trade, ChallengeStatus, TradeStatus, TradeType, UserRole

def seed_leaderboard():
    print("Starting Leaderboard & Admin Data Seeding...")
    print("Connecting to MySQL...")
    
    # Initialize the app with development config (MySQL)
    app = create_app('development')
    
    with app.app_context():
        # Check connection
        try:
            inspector = db.inspect(db.engine)
            print(f"Connected to DB: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
            users_tbl = inspector.get_table_names()
            if 'users' not in users_tbl:
                print("Error: 'users' table not found. Is the DB initialized?")
                db.create_all() # Try to create if missing
        except Exception as e:
            print(f"Connection Failed: {e}")
            return

        # 1. Create Top 10 Traders
        traders_data = [
            {"name": "Alex Momentum", "user": "alex_mo", "email": "alex@trade.com", "profit_target": 15000},
            {"name": "Sarah Sniper", "user": "sarah_sn", "email": "sarah@trade.com", "profit_target": 12000},
            {"name": "Mike Macro", "user": "mike_ma", "email": "mike@trade.com", "profit_target": 9500},
            {"name": "Emma Elliott", "user": "emma_el", "email": "emma@trade.com", "profit_target": 8000},
            {"name": "David Day", "user": "david_da", "email": "david@trade.com", "profit_target": 6500},
            {"name": "Lucas Long", "user": "lucas_lo", "email": "lucas@trade.com", "profit_target": 5000},
            {"name": "Julia Just", "user": "julia_ju", "email": "julia@trade.com", "profit_target": 4200},
            {"name": "Tom Trend", "user": "tom_tr", "email": "tom@trade.com", "profit_target": 3500},
            {"name": "Ryan Risk", "user": "ryan_ri", "email": "ryan@trade.com", "profit_target": 2000},
            {"name": "Nina News", "user": "nina_ne", "email": "nina@trade.com", "profit_target": 1500},
        ]

        print("Checking existing users...")
        
        for i, t_data in enumerate(traders_data):
            try:
                # Create User
                user = User.query.filter_by(email=t_data["email"]).first()
                if not user:
                    user = User(
                        full_name=t_data["name"],
                        username=t_data["user"],
                        email=t_data["email"],
                        role=UserRole.USER,
                        password_hash=generate_password_hash("password123")
                    )
                    db.session.add(user)
                    db.session.commit()
                    print(f"Created User: {user.username}")
                else:
                    print(f"User exists: {user.username}")

                # Create Account (Challenge)
                account = Account.query.filter_by(user_id=user.id, status=ChallengeStatus.ACTIVE).first()
                if not account:
                    # Funded amount depends on rank roughly
                    initial = 100000 if i < 3 else (50000 if i < 6 else 25000)
                    target_profit = t_data["profit_target"]
                    
                    account = Account(
                        user_id=user.id,
                        plan_name="Elite" if i < 3 else "Pro",
                        initial_balance=initial,
                        current_balance=initial + target_profit,
                        equity=initial + target_profit,
                        daily_starting_equity=initial + target_profit,
                        status=ChallengeStatus.ACTIVE,
                        reason="Trading Session Active",
                        admin_note="Top Performer - Verified"
                    )
                    db.session.add(account)
                    db.session.commit()
                    print(f"Created Account for {user.username} with ${target_profit} profit")
                    
                    # Create Trades to justify the profit (For Leaderboard ROI calc)
                    # Split profit into 3-5 trades
                    num_trades = random.randint(3, 6)
                    profit_per_trade = target_profit / num_trades
                    
                    for _ in range(num_trades):
                        symbol = random.choice(["XAUUSD", "EURUSD", "BTCUSD", "US30"])
                        entry = 2000.0 if "XAU" in symbol else (1.1000 if "EUR" in symbol else 45000.0)
                        
                        trade = Trade(
                            account_id=account.id,
                            user_id=user.id,
                            symbol=symbol,
                            side=TradeType.BUY,
                            quantity=1.0,
                            price=entry,
                            entry_price=entry,
                            exit_price=entry + (entry * 0.01), 
                            status=TradeStatus.CLOSED,
                            pnl=profit_per_trade,
                            closed_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
                        )
                        db.session.add(trade)
                    db.session.commit()
                else:
                    print(f"Account exists for {user.username}")
            except Exception as loop_e:
                print(f"Error seeding {t_data['name']}: {loop_e}")
                db.session.rollback()

        print("Success! Leaderboard data seeded.")

if __name__ == '__main__':
    seed_leaderboard()
