
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Course, Module, Lesson

def verify_academy():
    print("Verifying Academy Data in MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        courses = Course.query.all()
        
        print(f"\n📚 Total Courses in Database: {len(courses)}\n")
        print("=" * 80)
        
        for course in courses:
            print(f"\n🎓 Course: {course.title}")
            print(f"   Category: {course.category.value} | Level: {course.level.value}")
            print(f"   Duration: {course.duration_minutes} min | XP: {course.xp_reward}")
            print(f"   Premium: {course.is_premium}")
            
            modules = Module.query.filter_by(course_id=course.id).all()
            print(f"   📖 Modules: {len(modules)}")
            
            for module in modules:
                lessons = Lesson.query.filter_by(module_id=module.id).all()
                print(f"      - {module.title} ({len(lessons)} lessons)")
                
        print("\n" + "=" * 80)
        print(f"\n✓ Academy data verified in MySQL")

if __name__ == '__main__':
    verify_academy()
