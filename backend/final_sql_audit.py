
from app import app
from models import db
from sqlalchemy import text

def audit():
    with app.app_context():
        print("📊 FINAL SQL CONTENT AUDIT 📊")
        print("==============================")
        
        # 1. COURSES
        c_count = db.session.execute(text("SELECT COUNT(*) FROM courses")).scalar()
        print(f"✅ Courses: {c_count}")
        
        # 2. MODULES
        m_count = db.session.execute(text("SELECT COUNT(*) FROM modules")).scalar()
        print(f"✅ Modules: {m_count}")
        
        # 3. LESSONS
        l_count = db.session.execute(text("SELECT COUNT(*) FROM lessons")).scalar()
        l_with_content = db.session.execute(text("SELECT COUNT(*) FROM lessons WHERE LENGTH(content) > 500")).scalar()
        print(f"✅ Lessons: {l_count}")
        print(f"   - With Rich Content: {l_with_content} ({(l_with_content/l_count)*100:.1f}%)")
        
        # 4. QUIZZES
        q_count = db.session.execute(text("SELECT COUNT(*) FROM quizzes")).scalar()
        print(f"✅ Quizzes: {q_count}")
        
        # 5. QUESTIONS & OPTIONS
        ques_count = db.session.execute(text("SELECT COUNT(*) FROM questions")).scalar()
        opt_count = db.session.execute(text("SELECT COUNT(*) FROM options")).scalar()
        print(f"✅ Questions: {ques_count}")
        print(f"✅ Options: {opt_count}")
        
        # 6. INTEGRITY CHECK
        # Check if any module is missing a quiz
        orphans = db.session.execute(text("""
            SELECT m.title FROM modules m 
            LEFT JOIN quizzes q ON q.module_id = m.id 
            WHERE q.id IS NULL
        """)).fetchall()
        
        if not orphans:
            print("✨ INTEGRITY: All modules have quizzes.")
        else:
            print(f"⚠️ WAITING: {len(orphans)} modules without quizzes ({[o[0] for o in orphans]})")

        print("==============================")
        print("💾 ALL DATA IS PERSISTED IN MySQL.")

if __name__ == "__main__":
    audit()
