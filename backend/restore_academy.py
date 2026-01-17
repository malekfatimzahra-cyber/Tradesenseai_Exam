
import os
import sys

# Ensure parent directory of backend is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

from __init__ import create_app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseLevel, CourseCategory, LessonType, UserCourseProgress, UserLessonProgress, Badge
from sqlalchemy import text

def restore_academy():
    app = create_app('development')
    with app.app_context():
        print("🧹 Cleaning up Academy data...")
        try:
            # Detect DB type
            is_sqlite = 'sqlite' in str(db.engine.url)
            
            if is_sqlite:
                db.session.execute(text("PRAGMA foreign_keys=OFF"))
            else:
                db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            # Clean tables
            UserLessonProgress.query.delete()
            UserCourseProgress.query.delete()
            Option.query.delete()
            Question.query.delete()
            Quiz.query.delete()
            Lesson.query.delete()
            Module.query.delete()
            Course.query.delete()
            db.session.commit()
            print("✅ Database cleared.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during cleanup: {e}")
        finally:
            if is_sqlite:
                db.session.execute(text("PRAGMA foreign_keys=ON"))
            else:
                db.session.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        print("🌱 Seeding Full TradeSense Academy Experience...")
        
        courses_data = [
            {
                "title": "Introduction au Trading",
                "desc": "Apprenez les bases du trading Forex et CFD. Maîtrisez les concepts de base du marché.",
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "xp": 500, "premium": False,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800",
                "lessons": [
                    {"title": "Qu'est-ce que le Trading ?", "content": "<h2>📈 Introduction au Trading</h2><p>Le trading est l'art d'acheter et de vendre des actifs financiers...</p>"},
                    {"title": "Lire un Graphique", "content": "<h2>📊 Décrypter un Graphique</h2><p>Le graphique est l'outil principal du trader...</p>"}
                ]
            },
            {
                "title": "Institutional Trading Mastery", 
                "desc": "Master Order Blocks, Liquidity, Market Structure like the pros.", 
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.TECHNICAL, "xp": 1500, "premium": False,
                "img": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=800",
                "lessons": [{"title": "Order Blocks (OB)", "content": "<h2>Understanding Order Blocks</h2><p>Institutional footprints...</p>"}]
            },
            {
                "title": "Smart Money Concepts (SMC / ICT)",
                "desc": "Learn about Liquidity, Fair Value Gaps, and Institutional Market Structure.",
                "level": CourseLevel.ADVANCED, "cat": CourseCategory.TECHNICAL, "xp": 2000, "premium": True,
                "img": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=800"
            },
            {
                "title": "Trading Psychology Under Pressure", 
                "desc": "Conquer your mind. Master FOMO, Revenge Trading, and Building a Winner's Routine.", 
                "level": CourseLevel.ADVANCED, "cat": CourseCategory.PSYCHOLOGY, "xp": 1200, "premium": True,
                "img": "https://images.unsplash.com/photo-1549633033-9a446772f533?w=800"
            },
            {
                "title": "Basic Risk Management for Traders", 
                "desc": "Survival comes first. Learn position sizing, R-Multiples, and how not to blow your account.", 
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.RISK, "xp": 600, "premium": False,
                "img": "https://images.unsplash.com/photo-1639322537228-ad71c4295843?w=800"
            },
            {
                "title": "Market Structure & Trend Logic", 
                "desc": "Map the market properly. Identify BOS, Higher Highs, and Trend Reversals.", 
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.TECHNICAL, "xp": 900, "premium": False,
                "img": "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=800"
            },
            {
                "title": "Supply & Demand Trading",
                "desc": "Find key levels where institutions buy and sell. Master the imbalance strategy.",
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.TECHNICAL, "xp": 1100, "premium": True,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800"
            },
            {
                "title": "Psychologie du Trading (FR)",
                "desc": "Maîtrisez vos émotions et développez un mental de gagnant.",
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.PSYCHOLOGY, "xp": 150, "premium": False,
                "img": "https://images.unsplash.com/photo-1549633033-9a446772f533?w=800"
            }
        ]
        
        for c in courses_data:
            course = Course(
                title=c['title'], description=c['desc'], level=c['level'], category=c['cat'],
                thumbnail_url=c['img'], xp_reward=c['xp'], is_premium=c['premium'], duration_minutes=120
            )
            db.session.add(course)
            db.session.commit()
            
            # Add a default module
            mod = Module(course_id=course.id, title="Basics", order=1)
            db.session.add(mod)
            db.session.commit()
            
            # Add lessons if available
            lessons = c.get('lessons', [{"title": "Introduction", "content": "<h2>Intro</h2><p>Content coming soon...</p>"}])
            for i, l in enumerate(lessons):
                lesson = Lesson(
                    module_id=mod.id, title=l['title'], order=i+1, 
                    lesson_type=LessonType.TEXT, content=l['content']
                )
                db.session.add(lesson)
            db.session.commit()
        
        print(f"✅ Seeding complete. Added {Course.query.count()} courses with modules and lessons.")

if __name__ == "__main__":
    restore_academy()
