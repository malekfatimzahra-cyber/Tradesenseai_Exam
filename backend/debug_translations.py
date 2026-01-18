
from app import app
from models import db, Lesson, LessonTranslation
from sqlalchemy import text

def check_translations():
    with app.app_context():
        # Check Lesson 1 of Course 9
        # Assuming we know ID, or query it
        sql = text("""
            SELECT l.id, l.title, LENGTH(l.content) as base_len, 
                   lt.lang, LENGTH(lt.content) as trans_len
            FROM lessons l
            LEFT JOIN lesson_translations lt ON l.id = lt.lesson_id
            JOIN modules m ON l.module_id = m.id
            WHERE m.course_id = 9
            LIMIT 5
        """)
        
        rows = db.session.execute(sql).fetchall()
        print(f"{'ID':<5} | {'Title':<30} | {'Base Len':<10} | {'Lang':<5} | {'Trans Len':<10}")
        print("-" * 75)
        for r in rows:
            print(f"{r.id:<5} | {r.title[:28]:<30} | {r.base_len:<10} | {r.lang or 'N/A':<5} | {r.trans_len or 'N/A':<10}")

if __name__ == "__main__":
    check_translations()
