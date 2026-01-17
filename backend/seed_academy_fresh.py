
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Course, Module, Lesson

def clear_and_seed_academy():
    print("Clearing and Re-seeding Academy...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. Clear existing (Cascade deletes will handle modules/lessons)
        print("Clearing existing courses...")
        Course.query.delete()
        db.session.commit()
        
        from models import CourseCategory, CourseLevel, LessonType
        
        # Course 1: Introduction au Trading
        print("\n📚 Creating Course 1: Introduction au Trading...")
        course1 = Course(
            title="Introduction au Trading",
            description="Apprenez les bases du trading Forex et CFD",
            category=CourseCategory.TECHNICAL,
            level=CourseLevel.BEGINNER,
            thumbnail_url="/course-thumbnails/intro-trading.jpg",
            duration_minutes=120,
            xp_reward=100,
            is_premium=False
        )
        db.session.add(course1)
        db.session.commit()
        
        # Module 1.1
        mod1_1 = Module(course_id=course1.id, title="Les Bases du Marché", order=1)
        db.session.add(mod1_1)
        db.session.commit()
        
        lessons1_1 = [
            Lesson(module_id=mod1_1.id, title="Qu'est-ce que le Trading?", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Introduction au Trading</h2><p>Le trading est l'achat et la vente d'instruments financiers dans le but de réaliser un profit.</p>"),
            Lesson(module_id=mod1_1.id, title="Les Marchés Financiers", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Les Différents Marchés</h2><p>Forex, Actions, Crypto, Indices - découvrez les opportunités.</p>"),
            Lesson(module_id=mod1_1.id, title="Terminologie Essentielle", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Vocabulaire du Trader</h2><p>Pip, Lot, Spread, Levier... les termes indispensables.</p>")
        ]
        for lesson in lessons1_1:
            db.session.add(lesson)
        db.session.commit()
        
        # Module 1.2
        mod1_2 = Module(course_id=course1.id, title="Analyse Technique", order=2)
        db.session.add(mod1_2)
        db.session.commit()
        
        lessons1_2 = [
            Lesson(module_id=mod1_2.id, title="Chandelles Japonaises", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Les Chandeliers</h2><p>Patterns haussiers, baissiers et de retournement.</p>"),
            Lesson(module_id=mod1_2.id, title="Support et Résistance", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Niveaux Clés</h2><p>Identifiez les zones critiques du marché.</p>")
        ]
        for lesson in lessons1_2:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course1.title} - 2 modules, 5 lessons")
        
        # Course 2: Psychologie du Trading
        print("\n🧠 Creating Course 2: Psychologie du Trading...")
        course2 = Course(
            title="Psychologie du Trading",
            description="Maîtrisez vos émotions pour trader avec discipline",
            category=CourseCategory.PSYCHOLOGY,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/psychology.jpg",
            duration_minutes=90,
            xp_reward=150,
            is_premium=False
        )
        db.session.add(course2)
        db.session.commit()
        
        mod2_1 = Module(course_id=course2.id, title="Gestion Émotionnelle", order=1)
        db.session.add(mod2_1)
        db.session.commit()
        
        lessons2_1 = [
            Lesson(module_id=mod2_1.id, title="Comprendre la Peur et l'Avidité", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Émotions du Trader</h2><p>Les deux forces qui détruisent les comptes.</p>"),
            Lesson(module_id=mod2_1.id, title="Discipline et Patience", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Les Piliers du Succès</h2><p>Suivez votre plan, respectez vos règles.</p>")
        ]
        for lesson in lessons2_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course2.title} - 1 module, 2 lessons")
        
        # Course 3: Gestion des Risques
        print("\n🛡️ Creating Course 3: Gestion des Risques...")
        course3 = Course(
            title="Gestion des Risques",
            description="Protégez votre capital avec le risk management",
            category=CourseCategory.RISK,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/risk.jpg",
            duration_minutes=75,
            xp_reward=120,
            is_premium=False
        )
        db.session.add(course3)
        db.session.commit()
        
        mod3_1 = Module(course_id=course3.id, title="Principes Fondamentaux", order=1)
        db.session.add(mod3_1)
        db.session.commit()
        
        lessons3_1 = [
            Lesson(module_id=mod3_1.id, title="Règle des 1-2%", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Ne Risquez Jamais Plus de 2%</h2><p>Préservez votre capital sur le long terme.</p>"),
            Lesson(module_id=mod3_1.id, title="Position Sizing", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Calculer la Taille de Position</h2><p>Formule et exemples concrets.</p>"),
            Lesson(module_id=mod3_1.id, title="Stop Loss & Take Profit", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Protégez Vos Gains</h2><p>Stratégies de placement optimales.</p>")
        ]
        for lesson in lessons3_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course3.title} - 1 module, 3 lessons")
        
        # Course 4: Stratégies Avancées (Premium)
        print("\n⭐ Creating Course 4: Stratégies Avancées [PREMIUM]...")
        course4 = Course(
            title="Stratégies Avancées",
            description="Techniques professionnelles réservées aux traders Elite",
            category=CourseCategory.QUANT,
            level=CourseLevel.ADVANCED,
            thumbnail_url="/course-thumbnails/advanced.jpg",
            duration_minutes=180,
            xp_reward=250,
            is_premium=True
        )
        db.session.add(course4)
        db.session.commit()
        
        mod4_1 = Module(course_id=course4.id, title="Stratégies Intraday", order=1)
        db.session.add(mod4_1)
        db.session.commit()
        
        lessons4_1 = [
            Lesson(module_id=mod4_1.id, title="Scalping Avancé", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Scalping Professionnel</h2><p>Techniques haute fréquence pour profits rapides.</p>"),
            Lesson(module_id=mod4_1.id, title="Smart Money Concepts", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Suivez les Institutionnels</h2><p>Order blocks, liquidity sweeps, FVG.</p>")
        ]
        for lesson in lessons4_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course4.title} - 1 module, 2 lessons")
        
        print("\n✅ Academy Successfully Seeded!")
        print("=" * 60)
        print("Total: 4 Courses | 5 Modules | 12 Lessons")

if __name__ == '__main__':
    clear_and_seed_academy()
