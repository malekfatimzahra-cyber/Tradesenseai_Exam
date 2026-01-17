
import os
import sys

# Ensure backend dir is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

from __init__ import create_app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseLevel, CourseCategory, LessonType, UserCourseProgress, UserLessonProgress
from sqlalchemy import text

def seed_8_courses_mysql():
    app = create_app('development')
    with app.app_context():
        print("🧹 Cleaning up existing Academy data...")
        try:
            # Detect DB type
            is_sqlite = 'sqlite' in str(db.engine.url)
            if is_sqlite:
                db.session.execute(text("PRAGMA foreign_keys=OFF"))
            else:
                db.session.execute(text("SET FOREIGN_KEY_CHECKS=0"))

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

        # 8 Courses Data
        courses_data = [
            {
                "title": "Introduction au Trading (FR)",
                "desc": "Apprenez les bases du trading Forex et CFD. Maîtrisez les concepts de base du marché.",
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "duration": "3h 00m", "xp": 1000,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", "premium": False,
                "modules": [
                    {
                        "title": "Les Fondamentaux",
                        "lessons": [
                            {"title": "Qu'est-ce que le Trading ?", "content": "<h2>📉 Introduction au Trading</h2><p>Le trading est l'art d'acheter et de vendre des actifs financiers pour profiter des variations de prix.</p>"},
                            {"title": "Les Actifs Financiers", "content": "<h2>💰 Types d'Actifs</h2><p>Le Forex, les Actions, les Cryptomonnaies et les Matières Premières sont les plus populaires.</p>"}
                        ]
                    }
                ],
                "quiz": [
                    ("Qu'est-ce qu'un Pip ?", ["Une unité de mouvement de prix", "Une sorte de fruit", "Un broker"], 0)
                ]
            },
            {
                "title": "Trading Fundamentals & Market Mechanics",
                "desc": "Master the absolute basics: Pips, Spreads, Lots, and Order Types.",
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "duration": "1h 30m", "xp": 500,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", "premium": False,
                "modules": [
                    {
                        "title": "The Language of the Market",
                        "lessons": [
                            {"title": "Pips, Spreads, and Lots", "content": "<h2>The Building Blocks of Price</h2><p>Pips measure price movement. Spreads are the cost. Lots are the volume.</p>"}
                        ]
                    }
                ]
            },
            {
                "title": "Introduction to Price Action",
                "desc": "Learn to read the market without complex indicators. Pure Price Action.",
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "duration": "2h 00m", "xp": 800,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", "premium": False,
                "modules": [
                    {"title": "Candlestick Anatomy", "lessons": [{"title": "Basics", "content": "<h2>Candlesticks</h2><p>Open, High, Low, Close.</p>"}]}
                ]
            },
            {
                "title": "Smart Money Concepts (SMC / ICT)",
                "desc": "Learn about Liquidity, Fair Value Gaps, and Institutional Market Structure.",
                "level": CourseLevel.ADVANCED, "cat": CourseCategory.TECHNICAL, "duration": "4h 45m", "xp": 2000,
                "img": "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=800", "premium": True,
                "modules": [
                    {"title": "Institutional Order Flow", "lessons": [{"title": "Order Blocks", "content": "<h2>OB</h2><p>Institutional footprint.</p>"}]}
                ]
            },
            {
                "title": "Trading Psychology Under Pressure",
                "desc": "Conquer your mind. Master FOMO, Revenge Trading, and Building a Winner's Routine.",
                "level": CourseLevel.ADVANCED, "cat": CourseCategory.PSYCHOLOGY, "duration": "2h 15m", "xp": 1200,
                "img": "https://images.unsplash.com/photo-1549633033-9a446772f533?w=800", "premium": True,
                "modules": [
                    {"title": "Emotional Discipline", "lessons": [{"title": "Handling FOMO", "content": "<h2>FOMO</h2><p>Fear of missing out.</p>"}]}
                ]
            },
            {
                "title": "Basic Risk Management for Traders",
                "desc": "Survival comes first. Learn position sizing, R-Multiples, and how not to blow your account.",
                "level": CourseLevel.BEGINNER, "cat": CourseCategory.RISK, "duration": "1h 00m", "xp": 600,
                "img": "https://images.unsplash.com/photo-1639322537228-ad71c4295843?w=800", "premium": False,
                "modules": [
                    {"title": "Risk Foundation", "lessons": [{"title": "The 1% Rule", "content": "<h2>1% Rule</h2><p>Limit risk per trade.</p>"}]}
                ]
            },
            {
                "title": "Market Structure & Trend Logic",
                "desc": "Map the market properly. Identify BOS, Higher Highs, and Trend Reversals.",
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.TECHNICAL, "duration": "2h 10m", "xp": 900,
                "img": "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=800", "premium": False,
                "modules": [
                    {"title": "Mapping Structure", "lessons": [{"title": "BOS & CHOCh", "content": "<h2>BOS</h2><p>Break of structure.</p>"}]}
                ]
            },
            {
                "title": "Supply & Demand Trading",
                "desc": "Find key levels where institutions buy and sell. Master the imbalance strategy.",
                "level": CourseLevel.INTERMEDIATE, "cat": CourseCategory.TECHNICAL, "duration": "2h 30m", "xp": 1100,
                "img": "https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", "premium": True,
                "modules": [
                    {"title": "Zones of Value", "lessons": [{"title": "Drawing Zones", "content": "<h2>S/D Zones</h2><p>Supply and demand.</p>"}]}
                ]
            }
        ]

        # Seeding logic
        for c_data in courses_data:
            print(f"🌱 Seeding: {c_data['title']}...")
            
            # Duration parse
            hrs = int(c_data['duration'].split('h')[0])
            mins = int(c_data['duration'].split(' ')[1].replace('m', ''))
            duration = hrs * 60 + mins

            course = Course(
                title=c_data['title'], description=c_data['desc'], level=c_data['level'], category=c_data['cat'],
                duration_minutes=duration, thumbnail_url=c_data['img'], xp_reward=c_data['xp'], is_premium=c_data['premium']
            )
            db.session.add(course)
            db.session.commit()

            for m_data in c_data['modules']:
                module = Module(course_id=course.id, title=m_data['title'])
                db.session.add(module)
                db.session.commit()

                for l_data in m_data['lessons']:
                    lesson = Lesson(
                        module_id=module.id, title=l_data['title'], 
                        lesson_type=LessonType.TEXT, content=l_data['content']
                    )
                    db.session.add(lesson)
            db.session.commit()

            if 'quiz' in c_data:
                quiz = Quiz(course_id=course.id, title=f"Examen: {c_data['title']}", min_pass_score=80)
                db.session.add(quiz)
                db.session.commit()
                for q_text, opts, c_idx in c_data['quiz']:
                    q = Question(quiz_id=quiz.id, text=q_text, explanation="Review content.")
                    db.session.add(q)
                    db.session.commit()
                    for o_idx, o_text in enumerate(opts):
                        db.session.add(Option(question_id=q.id, text=o_text, is_correct=(o_idx==c_idx)))
                db.session.commit()

        print(f"✅ SUCCESSFULLY SEEDED 8 COURSES INTO { 'SQLITE' if is_sqlite else 'MYSQL' }!")

if __name__ == "__main__":
    seed_8_courses_mysql()
