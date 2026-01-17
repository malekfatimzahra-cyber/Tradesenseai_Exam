
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Course, Module, Lesson, CourseCategory

def show_all_courses():
    print("📚 TRADESENSE ACADEMY - ALL COURSES\n")
    print("=" * 80)
    
    app = create_app('development')
    
    with app.app_context():
        # Group by category
        for category in CourseCategory:
            courses = Course.query.filter_by(category=category).all()
            
            if courses:
                print(f"\n{'🔷' if category == CourseCategory.TECHNICAL else '🧠' if category == CourseCategory.PSYCHOLOGY else '🛡️' if category == CourseCategory.RISK else '🤖' if category == CourseCategory.QUANT else '📱'} {category.value.upper()} ({len(courses)} courses)")
                print("-" * 80)
                
                for course in courses:
                    premium = "⭐ PREMIUM" if course.is_premium else ""
                    print(f"\n  📖 {course.title} {premium}")
                    print(f"     Level: {course.level.value} | Duration: {course.duration_minutes} min | XP: {course.xp_reward}")
                    print(f"     {course.description}")
                    
                    modules = Module.query.filter_by(course_id=course.id).all()
                    print(f"     📚 {len(modules)} Module(s):")
                    
                    for module in modules:
                        lessons = Lesson.query.filter_by(module_id=module.id).all()
                        print(f"        • {module.title} ({len(lessons)} lessons)")
        
        # Summary
        total = Course.query.count()
        premium_count = Course.query.filter_by(is_premium=True).count()
        
        print("\n" + "=" * 80)
        print(f"\n📊 SUMMARY:")
        print(f"   Total Courses: {total}")
        print(f"   Premium Courses: {premium_count}")
        print(f"   Free Courses: {total - premium_count}")
        
        print("\n✅ All courses are saved in MySQL database!")

if __name__ == '__main__':
    show_all_courses()
