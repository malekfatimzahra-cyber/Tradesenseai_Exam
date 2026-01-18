
from app import app
from models import db
from sqlalchemy import text

def run_checks():
    with app.app_context():
        print("🔍 CHECK 1: Lesson Content Length (Course 9)")
        sql1 = text("""
            SELECT id, title, LENGTH(content) AS len
            FROM lessons
            WHERE module_id IN (SELECT id FROM modules WHERE course_id = 9)
            ORDER BY len ASC;
        """)
        rows1 = db.session.execute(sql1).fetchall()
        for r in rows1:
            print(f"   Lesson {r.id}: {r.title[:30]}... Len: {r.len}")

        print("\n🔍 CHECK 2: Quiz Questions Count")
        sql2 = text("""
            SELECT q.id, q.title, COUNT(qq.id) as q_count
            FROM quizzes q 
            JOIN questions qq ON qq.quiz_id=q.id
            WHERE q.module_id IN (SELECT id FROM modules WHERE course_id=9)
            GROUP BY q.id;
        """)
        rows2 = db.session.execute(sql2).fetchall()
        for r in rows2:
            print(f"   Quiz {r.id}: {r.title} -> {r.q_count} questions")

if __name__ == "__main__":
    run_checks()
