"""
Clean up Academy database and re-seed with consistent data.
This script will:
1. Delete all existing course data
2. Re-seed ONLY the complete courses from seed_courses.py
"""
from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, UserCourseProgress, UserLessonProgress
from seed_courses import seed_courses

def cleanup_and_reseed():
    with app.app_context():
        print("🧹 Cleaning up existing Academy data...")
        
        # Delete all academy-related data in correct order (to avoid foreign key issues)
        print("  - Deleting user progress...")
        UserLessonProgress.query.delete()
        UserCourseProgress.query.delete()
        
        print("  - Deleting quiz data...")
        Option.query.delete()
        Question.query.delete()
        Quiz.query.delete()
        
        print("  - Deleting lessons...")
        Lesson.query.delete()
        
        print("  - Deleting modules...")
        Module.query.delete()
        
        print("  - Deleting courses...")
        Course.query.delete()
        
        db.session.commit()
        print("✅ Cleanup complete!")
        
        print("\n🌱 Re-seeding courses...")
        seed_courses()
        
        # Verify the courses
        courses = Course.query.all()
        print(f"\n✅ Database now has {len(courses)} courses:")
        for course in courses:
            modules_count = len(course.modules)
            lessons_count = sum(len(m.lessons) for m in course.modules)
            print(f"  📚 {course.title}")
            print(f"     - Level: {course.level.value}")
            print(f"     - Category: {course.category.value}")
            print(f"     - Modules: {modules_count}")
            print(f"     - Lessons: {lessons_count}")
            print(f"     - Premium: {'Yes' if course.is_premium else 'No'}")
            print()
        
        print("🎉 Academy database is now clean and consistent!")

if __name__ == "__main__":
    cleanup_and_reseed()
