from app import app
from models import Course, Module, Lesson, Quiz
import json

with app.app_context():
    courses = Course.query.all()
    print(f"Total Courses: {len(courses)}\n")
    
    for course in courses:
        print(f"ID: {course.id} | {course.title}")
        print(f"  Level: {course.level} | Duration: {course.duration_minutes}m")
        
        modules = Module.query.filter_by(course_id=course.id).all()
        print(f"  Modules: {len(modules)}")
        
        for m in modules:
            lessons = Lesson.query.filter_by(module_id=m.id).all()
            print(f"    - {m.title}: {len(lessons)} lessons")
            for l in lessons:
                has_content = len(l.content) > 100 if l.content else False
                print(f"      * {l.title} [Content: {'✓' if has_content else '✗'}]")
        
        quiz = Quiz.query.filter_by(course_id=course.id).first()
        print(f"  Quiz: {'✓' if quiz else '✗'}")
        print()
