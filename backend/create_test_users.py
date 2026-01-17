from app import app
from models import db, User, UserRole

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(email='admin@tradesense.com').first()
    
    if not admin:
        print("Creating admin user...")
        admin = User(
            full_name='Admin User',
            email='admin@tradesense.com',
            username='admin',
            role=UserRole.ADMIN
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created!")
    else:
        print("Admin already exists, updating password...")
        admin.set_password('admin123')
        db.session.commit()
        print("✅ Password updated!")
    
    # Create test user
    test_user = User.query.filter_by(email='test@test.com').first()
    if not test_user:
        print("Creating test user...")
        test_user = User(
            full_name='Test User',
            email='test@test.com',
            username='test',
            role=UserRole.USER
        )
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        print("✅ Test user created!")
    else:
        print("Test user already exists, updating password...")
        test_user.set_password('test123')
        db.session.commit()
        print("✅ Test password updated!")
    
    print("\n📝 Login Credentials:")
    print("Admin: admin@tradesense.com / admin123")
    print("Test:  test@test.com / test123")
