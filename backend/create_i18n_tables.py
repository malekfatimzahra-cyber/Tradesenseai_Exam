
from app import app
from models import db

def create_tables():
    with app.app_context():
        print("🛠️ Creating i18n tables...")
        db.create_all()
        print("✅ Tables created successfully.")

if __name__ == '__main__':
    create_tables()
