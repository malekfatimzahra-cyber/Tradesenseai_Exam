
from app import app
from models import db
from sqlalchemy import text
import os

def diagnose():
    with app.app_context():
        print("=== 1) DIAGNOSTIC SQL ===")
        
        # A) Check Course
        print("\n--- A) Check Course 9 ---")
        sql_course = text("SELECT id, title, level, category FROM courses WHERE id = 9")
        course = db.session.execute(sql_course).fetchone()
        if course:
            print(f"✅ Found: {course}")
        else:
            print("❌ Course 9 NOT FOUND")

        # B) Check Modules
        print("\n--- B) Check Modules for Course 9 ---")
        sql_modules = text("SELECT id, title, order_index FROM modules WHERE course_id = 9 ORDER BY order_index")
        modules = db.session.execute(sql_modules).fetchall()
        if modules:
            for m in modules:
                print(f"   Module {m.id}: {m.title}")
        else:
            print("❌ No modules found for Course 9")

        # C) Check Lessons
        print("\n--- C) Check Lessons for Course 9 ---")
        sql_lessons = text("""
            SELECT l.id, l.title, LENGTH(l.content) as base_len, l.module_id 
            FROM lessons l
            JOIN modules m ON m.id = l.module_id
            WHERE m.course_id = 9
            ORDER BY m.order_index, l.order_index
        """)
        lessons = db.session.execute(sql_lessons).fetchall()
        if lessons:
            for l in lessons:
                print(f"   Lesson {l.id} (Mod {l.module_id}): {l.title} - Content Len: {l.base_len}")
        else:
            print("❌ No lessons found for Course 9")

        # D) Check Quizzes
        print("\n--- D) Check Quizzes for Course 9 ---")
        sql_quizzes = text("""
            SELECT q.id, q.title, q.module_id 
            FROM quizzes q
            JOIN modules m ON m.id = q.module_id
            WHERE m.course_id = 9
        """)
        quizzes = db.session.execute(sql_quizzes).fetchall()
        if quizzes:
            for q in quizzes:
                print(f"   Quiz {q.id} (Mod {q.module_id}): {q.title}")
        else:
            print("❌ No quizzes found for Course 9")

        print("\n=== 2) DATABASE INFO ===")
        # Check current DB name
        db_name = db.session.execute(text("SELECT DATABASE()")).scalar()
        print(f"Current Database: {db_name}")
        
        # Check Env Vars
        print(f"DB_USER: {os.environ.get('DB_USER')}")
        print(f"DB_NAME: {os.environ.get('DB_NAME')}")
        # Mask password
        # print(f"DB_PASSWORD: {'*' * 8 if os.environ.get('DB_PASSWORD') else 'None'}") 

if __name__ == "__main__":
    diagnose()
