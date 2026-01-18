
from app import app
from models import db, Module, Quiz, Question
from sqlalchemy import text

def verify_data():
    with app.app_context():
        print("=== 1. VERIFY MODULE QUIZZES ===")
        sql = text("""
            SELECT m.id AS module_id, m.title, COUNT(q.id) AS quiz_count
            FROM modules m
            LEFT JOIN quizzes q ON q.module_id = m.id
            GROUP BY m.id;
        """)
        rows = db.session.execute(sql).fetchall()
        for r in rows:
            status = "✅" if r.quiz_count == 1 else "❌"
            print(f"{status} Module {r.module_id}: {r.title} --> {r.quiz_count} quiz(zes)")

        print("\n=== 2. VERIFY QUESTIONS PER QUIZ ===")
        sql2 = text("""
            SELECT q.id AS quiz_id, q.title, COUNT(qq.id) AS question_count
            FROM quizzes q
            LEFT JOIN questions qq ON qq.quiz_id = q.id
            GROUP BY q.id;
        """)
        rows2 = db.session.execute(sql2).fetchall()
        for r in rows2:
            status = "✅" if r.question_count >= 8 else "⚠️"
            print(f"{status} Quiz {r.quiz_id}: {r.title} --> {r.question_count} questions")

if __name__ == "__main__":
    verify_data()
