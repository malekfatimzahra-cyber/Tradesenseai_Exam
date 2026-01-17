
from app import app, db
from models import User, Account, Trade, UserRole, ChallengeStatus, TradeType, TradeStatus, PaymentMethod, Transaction, PaymentStatus
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta

def seed_demo_data():
    print("🚀 Starting realistic demo data seeding for Morocco Exam...")

    # Static list of 10 Moroccan users
    users_data = [
        {"first": "Yassine", "last": "Benali", "email": "yassine@tradesense.ma", "role": UserRole.SUPERADMIN, "plan": "Elite"},
        {"first": "Imane", "last": "Tazi", "email": "imane@tradesense.ma", "role": UserRole.ADMIN, "plan": "Pro"},
        {"first": "Soufiane", "last": "Amrani", "email": "soufiane@gmail.com", "role": UserRole.USER, "plan": "Starter"},
        {"first": "Khadija", "last": "Idrissi", "email": "khadija.trading@gmail.com", "role": UserRole.USER, "plan": "Pro"},
        {"first": "Othman", "last": "El Fassi", "email": "othman.crypto@yahoo.com", "role": UserRole.USER, "plan": "Elite"},
        {"first": "Salma", "last": "Bennani", "email": "salma.b@hotmail.com", "role": UserRole.USER, "plan": "Starter"},
        {"first": "Mehdi", "last": "Jettou", "email": "mehdi.fx@gmail.com", "role": UserRole.USER, "plan": "Pro"},
        {"first": "Asmaa", "last": "Chaoui", "email": "asmaa.c@gmail.com", "role": UserRole.USER, "plan": "Starter"},
        {"first": "Hamza", "last": "Alami", "email": "hamza.alami@live.com", "role": UserRole.USER, "plan": "Elite"},
        {"first": "Meryem", "last": "Ouazzani", "email": "meryem.o@gmail.com", "role": UserRole.USER, "plan": "Pro"},
    ]

    plans = {
        "Starter": 5000.0,
        "Pro": 25000.0,
        "Elite": 100000.0
    }

    symbols = ["BTC-USD", "ETH-USD", "XAU-USD", "EUR-USD", "GBP-JPY", "AAPL", "TSLA", "IAM.MA", "ATW.MA", "NDX100"]
    
    # Common password for everyone
    default_password_hash = generate_password_hash("Test@1234")

    # Clear existing data? Maybe not, just check idempotency as requested.
    # But usually for a clean seeded logic, we might want to ensure these specific users are fresh.
    # The requirement says "if users already exist, don't duplicate".
    
    for i, u_data in enumerate(users_data):
        email = u_data["email"]
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            print(f"⚠️ User {email} already exists. Skipping creation but checking challenge...")
            user = existing_user
        else:
            username = f"{u_data['first'].lower()}{u_data['last'].lower()}"
            # Ensure username uniqueness
            if User.query.filter_by(username=username).first():
                username = f"{username}{random.randint(1,999)}"

            user = User(
                full_name=f"{u_data['first']} {u_data['last']}",
                username=username,
                email=email,
                role=u_data["role"],
                password_hash=default_password_hash
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ Created User: {user.full_name} ({user.role.value})")

        # Now handle Challenge (Account)
        # Check if user already has an account
        if user.accounts:
            print(f"   -> User already has {len(user.accounts)} accounts. Skipping challenge creation.")
            continue # Skip if already has accounts to avoid duplicates on re-run

        # Plan details
        plan_name = u_data["plan"]
        start_balance = plans[plan_name]
        
        # Decide if winner or loser (deterministic based on index to ensure mix)
        # i=0 (Admin) -> Winner
        # i=2,3 (Soufiane, Khadija) -> Failed
        # i=4,5 -> Passed
        # Others -> Active/Mixed
        
        is_winner = True
        status = ChallengeStatus.ACTIVE
        
        if i in [2, 7]: # Soufiane, Asmaa -> FAILED
            is_winner = False
            status = ChallengeStatus.FAILED
        elif i in [4, 8]: # Othman, Hamza -> PASSED
            is_winner = True
            status = ChallengeStatus.PASSED
        elif i in [0, 1]: # Admins -> Active/Good
             is_winner = True
             status = ChallengeStatus.ACTIVE
             
        # Generate Trades
        num_trades = random.randint(5, 15)
        current_equity = start_balance
        trades_list = []
        
        print(f"   -> Creating {plan_name} Challenge with {num_trades} trades...")

        # Create the Account first
        account = Account(
            user_id=user.id,
            plan_name=plan_name,
            initial_balance=start_balance,
            current_balance=start_balance, # Will update after trades
            equity=start_balance,          # Will update after trades
            daily_starting_equity=start_balance, # Simplified
            status=status,
            created_at=datetime.utcnow() - timedelta(days=7)
        )
        db.session.add(account)
        db.session.commit()

        total_pnl = 0.0

        for t_idx in range(num_trades):
            symbol = random.choice(symbols)
            trade_type = random.choice([TradeType.BUY, TradeType.SELL])
            
            # PnL Logic
            if is_winner:
                # 60% chance of win
                if random.random() > 0.4:
                    pnl = random.uniform(50, 500) * (start_balance / 5000) # Scale by plan
                else:
                    pnl = random.uniform(-50, -300) * (start_balance / 5000)
            else:
                # Loser: 70% chance of loss
                if random.random() > 0.3:
                    pnl = random.uniform(-100, -600) * (start_balance / 5000)
                else:
                    pnl = random.uniform(20, 200) * (start_balance / 5000)
            
            total_pnl += pnl
            
            # Create Trade
            trade = Trade(
                account_id=account.id,
                user_id=user.id,
                symbol=symbol,
                side=trade_type,
                trade_type=trade_type,
                quantity=random.uniform(0.1, 2.0),
                amount=0, # Calculated or simplified
                price=random.uniform(100, 50000),
                entry_price=random.uniform(100, 50000),
                exit_price=random.uniform(100, 50000), # Mock
                status=TradeStatus.CLOSED,
                pnl=pnl,
                timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23)),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23)),
                closed_at=datetime.utcnow()
            )
            db.session.add(trade)
        
        # Update Account consistency
        account.equity = start_balance + total_pnl
        account.current_balance = account.equity # Assuming all closed
        
        # Adjust status logic for reality if needed
        # If FAILED but equity is high, force equity low
        if status == ChallengeStatus.FAILED and account.equity >= start_balance:
             account.equity = start_balance * 0.85 # Force loss
             
        # If PASSED but equity is low, force equity high
        if status == ChallengeStatus.PASSED and account.equity <= start_balance:
             account.equity = start_balance * 1.15 # Force profit

        account.daily_starting_equity = account.equity # Reset for "today"
        
        db.session.commit()
        print(f"   -> Finished. Equity: {account.equity:.2f} (Start: {start_balance})")

    print("\n✅ Seed Script Completed Successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_demo_data()
