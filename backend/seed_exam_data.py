"""
Seed realistic Moroccan demo data for TradeSense AI Exam
- 10 Moroccan users (8 normal, 1 admin, 1 superadmin)
- Each normal user has 1 challenge + 5-15 trades
- Data is mathematically consistent (equity = start_balance + sum(pnl))
"""

from app import app
from models import db, User, UserRole, Account, ChallengeStatus, Trade, TradeStatus, TradeType
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Moroccan Users Data
USERS_DATA = [
    # Normal users
    {"full_name": "Yassine Alaoui", "email": "yassine.alaoui@gmail.com", "username": "yalaoui", "role": UserRole.USER},
    {"full_name": "Imane Benjelloun", "email": "imane.benjelloun@gmail.com", "username": "ibenjelloun", "role": UserRole.USER},
    {"full_name": "Soufiane El Idrissi", "email": "soufiane.elidrissi@gmail.com", "username": "selidrissi", "role": UserRole.USER},
    {"full_name": "Khadija Tazi", "email": "khadija.tazi@gmail.com", "username": "ktazi", "role": UserRole.USER},
    {"full_name": "Othman Chakir", "email": "othman.chakir@gmail.com", "username": "ochakir", "role": UserRole.USER},
    {"full_name": "Salma Benkirane", "email": "salma.benkirane@gmail.com", "username": "sbenkirane", "role": UserRole.USER},
    {"full_name": "Mehdi Lazrak", "email": "mehdi.lazrak@gmail.com", "username": "mlazrak", "role": UserRole.USER},
    {"full_name": "Asmaa Naciri", "email": "asmaa.naciri@gmail.com", "username": "anaciri", "role": UserRole.USER},
    # Admin users
    {"full_name": "Admin TradeSense", "email": "admin@tradesense.ma", "username": "admin_ts", "role": UserRole.ADMIN},
    {"full_name": "SuperAdmin TradeSense", "email": "superadmin@tradesense.ma", "username": "superadmin_ts", "role": UserRole.SUPERADMIN},
]

# Challenge Templates (for normal users)
CHALLENGE_TEMPLATES = [
    {"plan": "Starter", "start_balance": 5000, "status": ChallengeStatus.PASSED, "equity_target": 5750},  # +15% win
    {"plan": "Pro", "start_balance": 25000, "status": ChallengeStatus.ACTIVE, "equity_target": 26500},   # +6% in progress
    {"plan": "Elite", "start_balance": 100000, "status": ChallengeStatus.PASSED, "equity_target": 112000}, # +12% big win
    {"plan": "Starter", "start_balance": 5000, "status": ChallengeStatus.FAILED, "equity_target": 4200},  # -16% loss
    {"plan": "Pro", "start_balance": 25000, "status": ChallengeStatus.ACTIVE, "equity_target": 25800},   # +3.2%
    {"plan": "Starter", "start_balance": 5000, "status": ChallengeStatus.ACTIVE, "equity_target": 5300},  # +6%
    {"plan": "Elite", "start_balance": 100000, "status": ChallengeStatus.FAILED, "equity_target": 93000}, # -7% loss
    {"plan": "Pro", "start_balance": 25000, "status": ChallengeStatus.ACTIVE, "equity_target": 24500},   # -2% drawdown
]

# Moroccan + Global Symbols
SYMBOLS = ["BTC-USD", "ETH-USD", "AAPL", "TSLA", "EUR-USD", "GBP-USD", "GOLD", "IAM", "ATW", "CIH"]

def seed_exam_data():
    with app.app_context():
        print("=" * 80)
        print("SEEDING TRADESENSE AI EXAM DATA - MOROCCAN USERS + CHALLENGES + TRADES")
        print("=" * 80)
        
        # DEFAULT PASSWORD (same for all users for easy testing)
        default_password = "Test@1234"
        
        # =============================
        # 1. INSERT USERS
        # =============================
        users = []
        for user_data in USERS_DATA:
            # Check if user already exists (idempotent)
            existing = User.query.filter_by(email=user_data["email"]).first()
            if existing:
                print(f"⚠️  User {user_data['email']} already exists, skipping.")
                users.append(existing)
                continue
                
            # Create new user
            user = User(
                full_name=user_data["full_name"],
                email=user_data["email"],
                username=user_data["username"],
                role=user_data["role"]
            )
            user.set_password(default_password)
            db.session.add(user)
            db.session.flush()  # Get ID
            users.append(user)
            print(f"✅ Created user: {user.full_name} ({user.role.value})")
        
        db.session.commit()
        
        # =============================
        # 2. INSERT CHALLENGES + TRADES (for normal users only)
        # =============================
        normal_users = [u for u in users if u.role == UserRole.USER]
        
        for i, user in enumerate(normal_users):
            template = CHALLENGE_TEMPLATES[i]
            
            # Check if user already has a challenge (idempotent)
            existing_challenge = Account.query.filter_by(user_id=user.id).first()
            if existing_challenge:
                print(f"⚠️  User {user.full_name} already has a challenge, skipping.")
                continue
            
            # Create Challenge
            start_balance = template["start_balance"]
            equity = template["equity_target"]
            total_pnl = equity - start_balance
            
            challenge = Account(
                user_id=user.id,
                plan_name=template["plan"],
                initial_balance=start_balance,
                current_balance=equity,
                equity=equity,
                daily_starting_equity=start_balance,  # Simplified
                status=template["status"],
                created_at=datetime.utcnow() - timedelta(days=random.randint(5, 30))
            )
            db.session.add(challenge)
            db.session.flush()
            
            print(f"\n💰 Challenge for {user.full_name}:")
            print(f"   Plan: {template['plan']} | Start: {start_balance} MAD | Equity: {equity} MAD | PnL: {total_pnl:+.2f} MAD")
            
            # =============================
            # 3. INSERT TRADES (to match the PnL)
            # =============================
            num_trades = random.randint(8, 15)
            
            # Generate trades that sum to total_pnl
            trades_pnl = []
            for t in range(num_trades):
                if t == num_trades - 1:
                    # Last trade absorbs remaining PnL
                    pnl = total_pnl - sum(trades_pnl)
                else:
                    # Random PnL between -500 and +800
                    pnl = random.uniform(-500, 800)
                trades_pnl.append(pnl)
            
            # Create Trade records
            for t, pnl in enumerate(trades_pnl):
                symbol = random.choice(SYMBOLS)
                side = TradeType.BUY if random.random() > 0.5 else TradeType.SELL
                entry_price = random.uniform(50, 500)
                qty = abs(pnl) / 10 if abs(pnl) > 0 else 1  # Simplified quantity
                
                trade = Trade(
                    account_id=challenge.id,
                    user_id=user.id,
                    symbol=symbol,
                    side=side,
                    trade_type=side,
                    quantity=qty,
                    price=entry_price,
                    entry_price=entry_price,
                    exit_price=entry_price + (pnl / qty) if qty > 0 else entry_price,
                    amount=entry_price * qty,
                    status=TradeStatus.CLOSED,
                    pnl=pnl,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7), hours=random.randint(0, 23)),
                    closed_at=datetime.utcnow() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23))
                )
                db.session.add(trade)
            
            print(f"   📊 Inserted {num_trades} trades | Total PnL: {sum(trades_pnl):+.2f} MAD")
        
        db.session.commit()
        
        # =============================
        # SUMMARY
        # =============================
        print("\n" + "=" * 80)
        print("✅ SEEDING COMPLETE!")
        print("=" * 80)
        print(f"Total Users: {User.query.count()}")
        print(f"Total Challenges: {Account.query.count()}")
        print(f"Total Trades: {Trade.query.count()}")
        print("\nBreakdown:")
        print(f"  - Active Challenges: {Account.query.filter_by(status=ChallengeStatus.ACTIVE).count()}")
        print(f"  - Passed Challenges: {Account.query.filter_by(status=ChallengeStatus.PASSED).count()}")
        print(f"  - Failed Challenges: {Account.query.filter_by(status=ChallengeStatus.FAILED).count()}")
        
        print("\n🔑 DEFAULT PASSWORD FOR ALL USERS: Test@1234")
        print("\n📋 TEST ACCOUNTS:")
        print("   - Normal User: yassine.alaoui@gmail.com / Test@1234")
        print("   - Admin: admin@tradesense.ma / Test@1234")
        print("   - SuperAdmin: superadmin@tradesense.ma / Test@1234")
        print("=" * 80)

if __name__ == '__main__':
    seed_exam_data()
