
from app import app, db
from models import User, Account, UserRole, ChallengeStatus, TradeStatus
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_screenshot_users():
    print("🚀 Seeding users from the reference screenshot...")

    # Data from the screenshot
    users_data = [
        {
            "name": "Lucas Martin", 
            "email": "lucas.martin@gmail.com", 
            "plan": "Starter", 
            "initial": 5000, 
            "equity": 5200, 
            "status": ChallengeStatus.ACTIVE
        },
        {
            "name": "Sophia Nguyen", 
            "email": "sophia.nguyen@example.com", 
            "plan": "Elite", 
            "initial": 100000, 
            "equity": 110500, 
            "status": ChallengeStatus.PASSED
        },
        {
            "name": "Mohammed El A.", 
            "email": "mohammed.ela@example.com", 
            "plan": "Pro", 
            "initial": 25000, 
            "equity": 22500, 
            "status": ChallengeStatus.FAILED
        },
        {
            "name": "Emily Zhang", 
            "email": "emily.zhang@example.com", 
            "plan": "Starter", 
            "initial": 5000, 
            "equity": 4500, 
            "status": ChallengeStatus.ACTIVE
        },
        {
            "name": "Ali Ben Säid", 
            "email": "ali.bensaid@example.com", 
            "plan": "Pro", 
            "initial": 25000, 
            "equity": 25200, 
            "status": ChallengeStatus.ACTIVE
        },
        {
            "name": "Oliver Garcia", 
            "email": "oliver.garcia@example.com", 
            "plan": "Starter", 
            "initial": 5000, 
            "equity": 4250, 
            "status": ChallengeStatus.FAILED
        }
    ]

    default_pw = generate_password_hash("Test@1234")

    for u_data in users_data:
        # 1. Create User
        user = User.query.filter_by(email=u_data["email"]).first()
        if not user:
            # Create username from email prefix
            username = u_data["email"].split('@')[0]
            # Ensure unique username
            if User.query.filter_by(username=username).first():
                username = f"{username}_{int(datetime.now().timestamp())}"
                
            user = User(
                full_name=u_data["name"],
                email=u_data["email"],
                username=username,
                role=UserRole.USER,
                password_hash=default_pw,
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ Created User: {user.full_name}")
        else:
            print(f"ℹ️ User {user.full_name} already exists.")

        # 2. Create Challenge (Account)
        # Check if they already have this specific plan active
        existing_acc = Account.query.filter_by(user_id=user.id, plan_name=u_data["plan"]).first()
        if not existing_acc:
            acc = Account(
                user_id=user.id,
                plan_name=u_data["plan"],
                initial_balance=u_data["initial"],
                current_balance=u_data["equity"], # Assuming closed trades match equity
                equity=u_data["equity"],
                daily_starting_equity=u_data["equity"],
                status=u_data["status"],
                created_at=datetime.utcnow() - timedelta(days=5),
                last_daily_reset=datetime.utcnow().date()
            )
            db.session.add(acc)
            db.session.commit()
            print(f"   -> Added {u_data['plan']} Challenge. Equity: {u_data['equity']} ({u_data['status'].value})")
        else:
             print(f"   -> Challenge already exists.")

    print("\n✅ All screenshot users added successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_screenshot_users()
