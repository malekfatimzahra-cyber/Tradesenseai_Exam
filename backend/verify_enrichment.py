
from app import app
from models import db, Course, Module, Lesson, Quiz

def verify():
    with app.app_context():
        courses = Course.query.all()
        print(f"Total Courses: {len(courses)}")
        
        for c in courses:
            print(f"\nCourse: {c.title} (ID: {c.id})")
            modules = Module.query.filter_by(course_id=c.id).all()
            print(f"  Modules: {len(modules)}")
            
            for m in modules:
                lessons = Lesson.query.filter_by(module_id=m.id).all()
                quiz = Quiz.query.filter_by(module_id=m.id).first()
                print(f"    Module '{m.title}': {len(lessons)} lessons, Quiz: {'YES' if quiz else 'NO'}")
                
                # Check one lesson content length
                if lessons:
                    l = lessons[0]
                    content_len = len(l.content) if l.content else 0
                    print(f"      sample lesson '{l.title}' len: {content_len} chars")

if __name__ == "__main__":
    verify()
