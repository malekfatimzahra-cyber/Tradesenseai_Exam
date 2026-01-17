from app import app, db
import models

def reset_academy_tables():
    with app.app_context():
        print("Disabling foreign key checks...")
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        tables = [
            'user_quiz_attempts',
            'user_lesson_progress',
            'user_course_progress',
            'options',
            'questions',
            'quizzes',
            'lessons',
            'modules',
            'courses'
        ]
        
        for table in tables:
            print(f"Dropping table {table} if exists...")
            db.session.execute(db.text(f"DROP TABLE IF EXISTS {table};"))
        
        print("Re-enabling foreign key checks...")
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        print("Creating all tables (missing ones will be created)...")
        db.create_all()
        db.session.commit()
        print("Academy tables reset successfully!")

if __name__ == "__main__":
    reset_academy_tables()
