
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Course, Module, Lesson, CourseCategory, CourseLevel, LessonType

def seed_academy_courses():
    print("Seeding Academy Courses into MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check if courses already exist
        existing = Course.query.count()
        if existing > 0:
            print(f"Found {existing} existing courses. Skipping seed.")
            return
        
        # Course 1: Introduction au Trading
        print("Creating Course 1: Introduction au Trading...")
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
        
        # Lessons for Module 1.1
        lessons1_1 = [
            Lesson(module_id=mod1_1.id, title="Qu'est-ce que le Trading?", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Introduction au Trading</h2><p>Le trading est l'achat et la vente d'instruments financiers...</p>"),
            Lesson(module_id=mod1_1.id, title="Les Marchés Financiers", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Les Différents Marchés</h2><p>Il existe plusieurs types de marchés : Forex, Actions, Crypto...</p>"),
            Lesson(module_id=mod1_1.id, title="Terminologie Essentielle", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Vocabulaire du Trader</h2><p>Pip, Lot, Spread, Levier... découvrez les termes clés.</p>")
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
                   content="<h2>Les Chandeliers</h2><p>Apprenez à lire les patterns de chandeliers japonais...</p>"),
            Lesson(module_id=mod1_2.id, title="Support et Résistance", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Niveaux Clés</h2><p>Identifiez les zones de support et résistance sur les graphiques.</p>")
        ]
        for lesson in lessons1_2:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ Created: {course1.title} (2 modules, 5 lessons)")
        
        # Course 2: Psychologie du Trading
        print("Creating Course 2: Psychologie du Trading...")
        course2 = Course(
            title="Psychologie du Trading",
            description="Maîtrisez vos émotions et développez un mental de gagnant",
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
                   content="<h2>Émotions du Trader</h2><p>La peur et l'avidité sont vos pires ennemis...</p>"),
            Lesson(module_id=mod2_1.id, title="Discipline et Patience", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Les Piliers du Succès</h2><p>La discipline est la clé de la réussite à long terme.</p>")
        ]
        for lesson in lessons2_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ Created: {course2.title} (1 module, 2 lessons)")
        
        # Course 3: Gestion des Risques
        print("Creating Course 3: Gestion des Risques...")
        course3 = Course(
            title="Gestion des Risques",
            description="Protégez votre capital avec des stratégies de risk management",
            category=CourseCategory.RISK,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/risk-management.jpg",
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
                   content="<h2>Ne Risquez Jamais Plus de 2%</h2><p>La règle d'or de la gestion du risque...</p>"),
            Lesson(module_id=mod3_1.id, title="Position Sizing", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Calculer la Taille de Position</h2><p>Apprenez à dimensionner correctement vos trades.</p>"),
            Lesson(module_id=mod3_1.id, title="Stop Loss & Take Profit", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Protégez Vos Gains</h2><p>Placez intelligemment vos ordres de protection.</p>")
        ]
        for lesson in lessons3_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ Created: {course3.title} (1 module, 3 lessons)")
        
        # Course 4: Stratégies Avancées (Premium)
        print("Creating Course 4: Stratégies Avancées...")
        course4 = Course(
            title="Stratégies Avancées",
            description="Techniques de trading professionnelles et stratégies gagnantes",
            category=CourseCategory.QUANT,
            level=CourseLevel.ADVANCED,
            thumbnail_url="/course-thumbnails/advanced-strategies.jpg",
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
                   content="<h2>Scalping Professionnel</h2><p>Techniques de scalping à haute fréquence...</p>"),
            Lesson(module_id=mod4_1.id, title="Day Trading avec Smart Money", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Suivez les Institutionnels</h2><p>Identifiez les mouvements du smart money.</p>")
        ]
        for lesson in lessons4_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ Created: {course4.title} (1 module, 2 lessons) [PREMIUM]")
        
        print("\n✅ Academy seeded successfully!")
        print(f"Total: 4 courses, 5 modules, 12 lessons")

if __name__ == '__main__':
    seed_academy_courses()
