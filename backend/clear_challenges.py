from app import app
from models import db, Account

def clear_all_challenges():
    with app.app_context():
        print("Clearing all challenges/accounts...")
        # Delete all accounts (challenges)
        Account.query.delete()
        db.session.commit()
        print("✅ All challenges cleared! Users now have 0 balance and can purchase new challenges.")

if __name__ == '__main__':
    clear_all_challenges()
