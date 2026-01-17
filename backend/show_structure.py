"""
Check course structure with modules and lessons
"""

from app import app
from models import Course, Module, Lesson

def show_course_structure():
    with app.app_context():
        # Find Introduction au Trading course
        course = Course.query.filter_by(title="Introduction au Trading").first()
        
        if not course:
            print("❌ Course 'Introduction au Trading' not found!")
            return
        
        print(f"📚 Course: {course.title}\n")
        
        modules = Module.query.filter_by(course_id=course.id).order_by(Module.order).all()
        
        for module in modules:
            print(f"\n{'='*60}")
            print(f"📖 Module {module.order}: {module.title}")
            print(f"{'='*60}")
            
            lessons = Lesson.query.filter_by(module_id=module.id).order_by(Lesson.order).all()
            
            if not lessons:
                print("   (No lessons)")
            else:
                for lesson in lessons:
                    has_content = "✅" if lesson.content and len(lesson.content.strip()) > 0 else "❌"
                    print(f"   {has_content} {lesson.order}. {lesson.title}")

if __name__ == "__main__":
    show_course_structure()
