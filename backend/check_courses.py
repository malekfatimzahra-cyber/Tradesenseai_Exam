from app import app
from models import Course, Module, Lesson

def check():
    with app.app_context():
        courses = Course.query.all()
        print(f"Found {len(courses)} courses:")
        for c in courses:
            print(f"ID: {c.id} | Title: {c.title}")
            modules = Module.query.filter_by(course_id=c.id).all()
            print(f" - Modules: {len(modules)}")
            for m in modules:
                lessons = Lesson.query.filter_by(module_id=m.id).all()
                print(f"   - Mod '{m.title}': {len(lessons)} lessons")

if __name__ == "__main__":
    check()
