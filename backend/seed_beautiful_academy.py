
import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, LessonType

def seed_beautiful_academy():
    with app.app_context():
        print("🚀 Seeding Beautiful Academy with Professional Courses...")
        
        # Delete all existing courses to start fresh (with proper cascade)
        print("🗑️ Clearing existing courses...")
        # Delete in correct order to respect foreign keys
        from models import UserQuizAttempt, UserQuizAnswer, UserLessonProgress, UserCourseProgress
        
        UserQuizAnswer.query.delete()
        UserQuizAttempt.query.delete()
        UserLessonProgress.query.delete()
        UserCourseProgress.query.delete()
        
        Option.query.delete()
        Question.query.delete()
        Quiz.query.delete()
        Lesson.query.delete()
        Module.query.delete()
        Course.query.delete()
        
        db.session.commit()
        print("✅ Database cleaned!")
        
        courses_data = [
            {
                "title": "Introduction au Trading (FR)",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.BEGINNER,
                "description": "Le guide ultime pour débuter sur les marchés financiers. Apprenez tout de A à Z : vocabulaire, analyse, psychologie et gestion du risque.",
                "thumbnail_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
                "duration_minutes": 300,
                "xp_reward": 2500
            },
            {
                "title": "Trading Fundamentals & Market Mechanics",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.BEGINNER,
                "description": "Master the absolute basics: Pips, Spreads, Lots, and Order Types. Build your foundation here.",
                "thumbnail_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&q=80",
                "duration_minutes": 180,
                "xp_reward": 1500
            },
            {
                "title": "Introduction to Price Action",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Read the market without complex indicators. Pure Price Action.",
                "thumbnail_url": "https://images.unsplash.com/photo-1642790551116-18e150f248e5?w=800&q=80",
                "duration_minutes": 240,
                "xp_reward": 2000
            },
            {
                "title": "Smart Money Concepts (SMC / ICT)",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.EXPERT,
                "description": "Learn about Liquidity, Order Blocks, Fair Value Gaps, and Market Structure.",
                "thumbnail_url": "https://images.unsplash.com/photo-1612178991541-b48cc8e92a4d?w=800&q=80",
                "duration_minutes": 360,
                "xp_reward": 3500
            },
            {
                "title": "Trading Psychology Under Pressure",
                "category": CourseCategory.PSYCHOLOGY,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Conquer your mind. Master FOMO, Revenge trading, and Discipline without a Routine.",
                "thumbnail_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",
                "duration_minutes": 200,
                "xp_reward": 1800
            },
            {
                "title": "Basic Risk Management for Traders",
                "category": CourseCategory.RISK,
                "level": CourseLevel.BEGINNER,
                "description": "Survival comes first. Learn position sizing, R:R Multiples, and how to keep your account.",
                "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80",
                "duration_minutes": 150,
                "xp_reward": 1200
            },
            {
                "title": "Market Structure & Trend Logic",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Map the market properly. Identify BOS, Higher Highs, and major imbalance reversals.",
                "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
                "duration_minutes": 220,
                "xp_reward": 2200
            },
            {
                "title": "Supply & Demand Trading",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Find key levels where institutions buy and sell. Master the imbalance strategy.",
                "thumbnail_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80",
                "duration_minutes": 210,
                "xp_reward": 1900
            }
        ]
        
        for course_data in courses_data:
            print(f"📚 Creating: {course_data['title']}")
            course = Course(
                lang='en' if 'FR' not in course_data['title'] else 'fr',
                **course_data,
                is_premium=False
            )
            db.session.add(course)
            db.session.flush()
            
            # Add basic module structure for each
            module = Module(
                course_id=course.id,
                title="MODULE 1: LES FONDAMENTAUX" if course.lang == 'fr' else "MODULE 1: THE FUNDAMENTALS",
                order_index=1
            )
            db.session.add(module)
            db.session.flush()
            
            # Add sample lesson
            lesson = Lesson(
                module_id=module.id,
                title="Qu'est-ce que le Trading ?" if course.lang == 'fr' else "What is Trading?",
                content=f"<h2>Welcome to {course.title}</h2><p>This comprehensive course will teach you everything you need to know.</p>",
                content_type='html',
                lesson_type=LessonType.TEXT,
                order_index=1
            )
            db.session.add(lesson)
            
        db.session.commit()
        print("\n✅ SUCCESS: Beautiful Academy Ready!")

if __name__ == "__main__":
    seed_beautiful_academy()
