from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, UserCourseProgress, UserLessonProgress
from sqlalchemy import text

def clear_academy():
    with app.app_context():
        print("🗑️ Clearing Academy Data...")
        
        # Attempt to disable FK checks to ensure smooth deletion
        try:
            if 'sqlite' in str(db.engine.url):
                db.session.execute(text("PRAGMA foreign_keys=OFF"))
            else:
                db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        except Exception as e:
            print(f"⚠️ Note: Could not disable FK checks: {e}")

        try:
            # Delete in reverse dependency order (just to be safe)
            num_deleted = 0
            
            num_deleted += db.session.query(UserLessonProgress).delete()
            num_deleted += db.session.query(UserCourseProgress).delete()
            num_deleted += db.session.query(Option).delete()
            num_deleted += db.session.query(Question).delete()
            num_deleted += db.session.query(Quiz).delete()
            num_deleted += db.session.query(Lesson).delete()
            num_deleted += db.session.query(Module).delete()
            num_deleted += db.session.query(Course).delete()
            
            db.session.commit()
            print(f"✅ Deleted {num_deleted} records across all tables.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during delete: {e}")
        finally:
            # Re-enable FK checks
            try:
                if 'sqlite' in str(db.engine.url):
                    db.session.execute(text("PRAGMA foreign_keys=ON"))
                else:
                    db.session.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            except:
                pass

        print("✅ Academy tables cleared successfully!")

if __name__ == "__main__":
    clear_academy()
