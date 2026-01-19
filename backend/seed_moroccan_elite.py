
import os
import sys
import random
import json
from datetime import datetime, timedelta

# Ensure backend dir is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, User, UserRole, Account, ChallengeStatus, Leaderboard

MOROCCAN_NAMES = [
    "Amine Benali", "Fatima Zahra El Idrissi", "Youssef Alami", 
    "Siham Mansouri", "Omar Bennani", "Laila Tazi", 
    "Mehdi Chraibi", "Salma El Fassi", "Anas Belkhayat", "Zineb Berrada"
]

def seed_moroccan_elite():
    with app.app_context():
        print("🚀 Seeding 10 Elite Moroccan Traders to Railway...")
        
        default_password = "EliteTrader123!"
        
        for i, full_name in enumerate(MOROCCAN_NAMES):
            username = full_name.lower().replace(" ", "_") + str(random.randint(10, 99))
            email = f"{username}@tradesense-elite.ma"
            
            # 1. Create User
            existing_user = User.query.filter_by(email=email).first()
            if not existing_user:
                print(f"👤 Creating user: {full_name}")
                user = User(
                    full_name=full_name,
                    username=username,
                    email=email,
                    role=UserRole.USER
                )
                user.set_password(default_password)
                db.session.add(user)
                db.session.flush() # Get user.id
            else:
                user = existing_user
                print(f"⚠️ User {email} already exists.")

            # 2. Create Elite Account (Passed)
            # Plan details for Elite
            initial_balance = 100000.0
            equity = random.uniform(120000.0, 185000.0)
            
            # Check if an elite account already exists for this user
            existing_acc = Account.query.filter_by(user_id=user.id, plan_name='Elite Institutional').first()
            if not existing_acc:
                print(f"💰 Creating Elite Account for {full_name}")
                account = Account(
                    user_id=user.id,
                    plan_name='Elite Institutional',
                    initial_balance=initial_balance,
                    current_balance=equity,
                    equity=equity,
                    daily_starting_equity=initial_balance,
                    status=ChallengeStatus.PASSED,
                    reason="Passed via manual evaluation (Exam Demo)"
                )
                db.session.add(account)
                db.session.flush() # Get account.id
            else:
                account = existing_acc
                account.equity = equity
                account.current_balance = equity
                account.status = ChallengeStatus.PASSED
                print(f"♻️ Updated existing account for {full_name}")

            # 3. Create Leaderboard Entry
            # Check if leaderboard entry exists
            existing_lb = Leaderboard.query.filter_by(user_id=user.id).first()
            
            profit = equity - initial_balance
            roi = (profit / initial_balance) * 100
            win_rate = random.uniform(65.0, 88.0)
            
            # Generate dummy equity curve (sparkline)
            curve = [initial_balance]
            curr = initial_balance
            for _ in range(10):
                curr += random.uniform(-2000, 10000)
                curve.append(curr)
            curve.append(equity)

            badges = ["Elite Performer", "Moroccan Pro", "Top 10"]
            
            if not existing_lb:
                print(f"🏆 Adding {full_name} to Leaderboard")
                lb_entry = Leaderboard(
                    user_id=user.id,
                    account_id=account.id,
                    username=user.full_name,
                    country='MA',
                    profit=profit,
                    roi=roi,
                    win_rate=win_rate,
                    funded_amount=initial_balance,
                    consistency_score=random.uniform(85.0, 98.0),
                    risk_score=random.uniform(90.0, 99.0),
                    badges=json.dumps(badges),
                    equity_curve=json.dumps(curve),
                    ranking=0, # Will be updated by system or displayed by ROI
                    period='ALL_TIME'
                )
                db.session.add(lb_entry)
            else:
                existing_lb.profit = profit
                existing_lb.roi = roi
                existing_lb.win_rate = win_rate
                existing_lb.equity_curve = json.dumps(curve)
                print(f"♻️ Updated Leaderboard entry for {full_name}")

        try:
            db.session.commit()
            print("\n✅ SUCCESS: Added 10 Elite Moroccan Traders and populated Leaderboard!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ FAILED to seed data: {e}")

if __name__ == "__main__":
    seed_moroccan_elite()
