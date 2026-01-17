
from app import app, db
from models import User, Account

def delete_screenshot_users():
    print("🗑️ Deleting the screenshot users...")

    emails_to_delete = [
        "lucas.martin@gmail.com",
        "sophia.nguyen@example.com",
        "mohammed.ela@example.com",
        "emily.zhang@example.com",
        "ali.bensaid@example.com",
        "oliver.garcia@example.com"
    ]

    count = 0
    for email in emails_to_delete:
        user = User.query.filter_by(email=email).first()
        if user:
            # Delete associated accounts first (although cascade should handle it ideally, but safer to be explicit if no cascade)
            # SQLAlchemy defaults might not cascade delete unless configured.
            # Let's try deleting user directly, SQLAlchemy relationship usually handles access or we do it manually.
            
            # Manual cleanup if needed (based on models.py definitions seen earlier)
            # models.py: trades = db.relationship('Trade', backref='user', lazy=True)
            # user.trades (might need manual deletion if cascade not set)
            # user.challenges (Account? No, models.py had `accounts = db.relationship('Account'...`)
            
            if user.accounts:
                for acc in user.accounts:
                    db.session.delete(acc)
            
            if user.trades:
                for trade in user.trades:
                    db.session.delete(trade)
            
            db.session.delete(user)
            count += 1
            print(f"   -> Deleted {user.full_name} ({email})")
        else:
            print(f"   -> User {email} not found (already deleted?)")

    db.session.commit()
    print(f"\n✅ Successfully deleted {count} users.")

if __name__ == "__main__":
    with app.app_context():
        delete_screenshot_users()
