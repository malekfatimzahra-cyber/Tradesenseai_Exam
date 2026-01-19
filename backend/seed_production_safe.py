
import os
import sys

# Ensure backend directory is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, LessonType

def seed_safe_production():
    with app.app_context():
        print("🚀 Starting SAFE Production Seeding...")
        
        # 1. Ensure DB Connection
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"🔗 Connected to: {db_url.split('@')[-1] if '@' in db_url else 'local'}")

        # ==========================================
        # COURSE 11: INTRO TO TRADING (Check & Seed)
        # ==========================================
        c11 = Course.query.get(11)
        if not c11:
            print("⚠️ Course 11 missing. Creating 'Introduction au Trading'...")
            c11 = Course(
                id=11,
                title="Introduction au Trading",
                description="Les bases essentielles pour débuter sur les marchés financiers.",
                category=CourseCategory.TECHNICAL,
                level=CourseLevel.BEGINNER,
                thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800",
                duration_minutes=90,
                xp_reward=500,
                is_premium=False
            )
            db.session.add(c11)
            db.session.commit()
            print("✅ Course 11 Created.")
            
            # Add Module 1
            m1 = Module(course_id=11, title="Les Bases", order_index=1)
            db.session.add(m1)
            db.session.commit()
            
            # Add Lessons
            l1 = Lesson(
                module_id=m1.id,
                title="Qu'est-ce que le Trading ?",
                content="""
                <div class="space-y-4">
                    <h2 class="text-2xl font-bold text-white">Définition</h2>
                    <p class="text-gray-300">Le trading est l'activité d'achat et de vente d'actifs financiers...</p>
                    <div class="bg-blue-900/20 p-4 rounded-lg border-l-4 border-blue-500">
                        <p class="text-white font-bold">Concept Clé :</p>
                        <p class="text-gray-400">Acheter bas, vendre haut (Long) ou vendre haut, acheter bas (Short).</p>
                    </div>
                </div>
                """,
                content_type='html',
                lesson_type=LessonType.TEXT,
                order_index=1
            )
            db.session.add(l1)
            db.session.commit()
        else:
            print("✅ Course 11 already exists. Skipping.")

        # ==========================================
        # COURSE 12: FUNDAMENTALS (Check & Seed)
        # ==========================================
        c12 = Course.query.get(12)
        if not c12:
            print("⚠️ Course 11 missing. Creating 'Trading Fundamentals'...")
            c12 = Course(
                id=12,
                title="Trading Fundamentals & Market Mechanics",
                description="Master the core mechanics of price movement and market structure.",
                category=CourseCategory.TECHNICAL,
                level=CourseLevel.INTERMEDIATE,
                thumbnail_url="https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=800",
                duration_minutes=120,
                xp_reward=1000,
                is_premium=True
            )
            db.session.add(c12)
            db.session.commit()
            print("✅ Course 12 Created.")
            
            # (We could add full content here, but sticking to basics for safe seed)
        else:
            print("✅ Course 12 already exists. Skipping.")
            
            # Check if Course 12 has a final exam, if not, add one
            exam = Quiz.query.filter_by(course_id=12, module_id=None).first()
            if not exam:
                print("⚠️ Course 12 has no Final Exam. Creating one...")
                exam = Quiz(
                    course_id=12,
                    module_id=None,
                    title="Examen Final: Fundamentals",
                    min_pass_score=70
                )
                db.session.add(exam)
                db.session.commit()
                
                # Add a sample question
                q1 = Question(quiz_id=exam.id, text="What drives market price?", explanation="Supply and Demand")
                db.session.add(q1)
                db.session.commit()
                db.session.add(Option(question_id=q1.id, text="Supply & Demand", is_correct=True))
                db.session.add(Option(question_id=q1.id, text="Magic", is_correct=False))
                db.session.commit()
                print("✅ Final Exam added to Course 12.")
            else:
                print("✅ Course 12 Final Exam exists.")

        print("\n🎉 Seeding Verification Complete.")

if __name__ == "__main__":
    seed_safe_production()
