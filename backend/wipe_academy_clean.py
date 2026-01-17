from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, UserCourseProgress, UserLessonProgress

def wipe_academy():
    with app.app_context():
        print("Starting full academy wipe...")
        try:
            # Delete in order to satisfy FK constraints
            UserLessonProgress.query.delete()
            UserCourseProgress.query.delete()
            Option.query.delete()
            Question.query.delete()
            Quiz.query.delete()
            Lesson.query.delete()
            Module.query.delete()
            Course.query.delete()
            
            db.session.commit()
            print("✅ All academy courses and progress data have been DELETED.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during wipe: {e}")

if __name__ == "__main__":
    wipe_academy()
