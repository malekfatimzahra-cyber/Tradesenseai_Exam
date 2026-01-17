from app import app, db
import models

def reset_db():
    with app.app_context():
        print("Disabling foreign key checks...")
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        print("Dropping all tables...")
        db.drop_all()
        
        print("Re-enabling foreign key checks...")
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        print("Creating all tables...")
        db.create_all()
        print("Database reset successfully!")

if __name__ == "__main__":
    reset_db()
