
import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson

def check_db():
    with app.app_context():
        print("🔍 Checking Database Content...")
        courses = Course.query.all()
        if not courses:
            print("❌ No courses found in DB!")
            return

        print(f"✅ Found {len(courses)} courses:")
        for c in courses:
            mod_count = Module.query.filter_by(course_id=c.id).count()
            print(f"   [ID: {c.id}] {c.title} ({mod_count} modules)")
            
            if mod_count > 0:
                modules = Module.query.filter_by(course_id=c.id).all()
                for m in modules:
                    l_count = Lesson.query.filter_by(module_id=m.id).count()
                    print(f"      - Module {m.id}: {m.title} ({l_count} lessons)")

if __name__ == "__main__":
    check_db()
