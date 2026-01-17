from app import app
from models import db, User, Account, ChallengeStatus, UserRole
from werkzeug.security import generate_password_hash
import datetime

def seed_admin_data():
    with app.app_context():
        print("Seeding Admin Demo User Data...")
        
        # 1. Create specific users from the Exam Image
        # Lucas Martin (Active, Starter, +Profit)
        u1 = User.query.filter_by(email='lucas.martin@gmail.com').first()
        if not u1:
            u1 = User(full_name='Lucas Martin', email='lucas.martin@gmail.com', username='lucasm', role=UserRole.USER)
            u1.set_password('123456')
            db.session.add(u1)
            db.session.commit()
            print("Created Lucas Martin")
            
        # Sophia Nguyen (Passed, Elite, Huge Profit)
        u2 = User.query.filter_by(email='sophia.nguyen@example.com').first()
        if not u2:
            u2 = User(full_name='Sophia Nguyen', email='sophia.nguyen@example.com', username='sophian', role=UserRole.USER)
            u2.set_password('123456')
            db.session.add(u2)
            db.session.commit()
            print("Created Sophia Nguyen")

        # Mohammed El A. (Failed, Pro, Loss)
        u3 = User.query.filter_by(email='mohanmed.ela@example.com').first()
        if not u3:
            u3 = User(full_name='Mohammed El A.', email='mohanmed.ela@example.com', username='mohamedel', role=UserRole.USER)
            u3.set_password('123456')
            db.session.add(u3)
            db.session.commit()
            print("Created Mohammed El A.")
            
        # Emily Zhang (Active, Starter, Loss)
        u4 = User.query.filter_by(email='emily.zhang@example.com').first()
        if not u4:
            u4 = User(full_name='Emily Zhang', email='emily.zhang@example.com', username='emilyz', role=UserRole.USER)
            u4.set_password('123456')
            db.session.add(u4)
            db.session.commit()

        # Ali Ben Said (Active, Pro, Profit)
        u5 = User.query.filter_by(email='alibensaid@example.com').first()
        if not u5:
            u5 = User(full_name='Ali Ben Säid', email='alibensaid@example.com', username='alibs', role=UserRole.USER)
            u5.set_password('123456')
            db.session.add(u5)
            db.session.commit()
            
        # Oliver Garcia (Failed, Starter, Loss)
        u6 = User.query.filter_by(email='oliver.garcia@example.com').first()
        if not u6:
            u6 = User(full_name='Oliver Garcia', email='oliver.garcia@example.com', username='oliverg', role=UserRole.USER)
            u6.set_password('123456')
            db.session.add(u6)
            db.session.commit()

        # Create Challenges matching the image
        
        # Lucas: Starter, 5000, Equity 5200 (+200), ACTIVE
        if not Account.query.filter_by(user_id=u1.id).first():
            c1 = Account(user_id=u1.id, plan_name='Starter', initial_balance=5000, equity=5200, current_balance=5200, status=ChallengeStatus.ACTIVE, created_at=datetime.datetime.utcnow())
            db.session.add(c1)
            
        # Sophia: Elite, 100000, Equity 110500 (+10500), PASSED
        if not Account.query.filter_by(user_id=u2.id).first():
            c2 = Account(user_id=u2.id, plan_name='Elite', initial_balance=100000, equity=110500, current_balance=110500, status=ChallengeStatus.PASSED, created_at=datetime.datetime.utcnow())
            db.session.add(c2)
            
        # Mohammed: Pro, 25000, Equity 22500 (-2500), FAILED
        if not Account.query.filter_by(user_id=u3.id).first():
            c3 = Account(user_id=u3.id, plan_name='Pro', initial_balance=25000, equity=22500, current_balance=22500, status=ChallengeStatus.FAILED, created_at=datetime.datetime.utcnow())
            db.session.add(c3)
            
        # Emily: Starter, 5000, Equity 4500 (-500), ACTIVE
        if not Account.query.filter_by(user_id=u4.id).first():
            c4 = Account(user_id=u4.id, plan_name='Starter', initial_balance=5000, equity=4500, current_balance=4500, status=ChallengeStatus.ACTIVE, created_at=datetime.datetime.utcnow())
            db.session.add(c4)
            
        # Ali: Pro, 25000, Equity 25200 (+200), ACTIVE
        if not Account.query.filter_by(user_id=u5.id).first():
            c5 = Account(user_id=u5.id, plan_name='Pro', initial_balance=25000, equity=25200, current_balance=25200, status=ChallengeStatus.ACTIVE, created_at=datetime.datetime.utcnow())
            db.session.add(c5)
            
        # Oliver: Starter, 5000, Equity 4250 (-750), FAILED
        if not Account.query.filter_by(user_id=u6.id).first():
            c6 = Account(user_id=u6.id, plan_name='Starter', initial_balance=5000, equity=4250, current_balance=4250, status=ChallengeStatus.FAILED, created_at=datetime.datetime.utcnow())
            db.session.add(c6)
            
        db.session.commit()
        print("✅ Seeded Virtual Admin Data Successfully!")

if __name__ == '__main__':
    seed_admin_data()
