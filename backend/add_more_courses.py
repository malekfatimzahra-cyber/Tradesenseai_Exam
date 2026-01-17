
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Course, Module, Lesson, CourseCategory, CourseLevel, LessonType

def add_more_courses():
    print("Adding More Academy Courses...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check existing courses
        existing_count = Course.query.count()
        print(f"Current courses in database: {existing_count}")
        
        courses_to_add = []
        
        # ======== TECHNICAL COURSES ========
        
        # Course 2: Analyse Technique Avancée
        print("\n📊 Creating TECHNICAL Course: Analyse Technique Avancée...")
        course2 = Course(
            title="Analyse Technique Avancée",
            description="Maîtrisez les indicateurs techniques et patterns chartistes",
            category=CourseCategory.TECHNICAL,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/technical-advanced.jpg",
            duration_minutes=150,
            xp_reward=180,
            is_premium=False
        )
        db.session.add(course2)
        db.session.commit()
        
        mod2_1 = Module(course_id=course2.id, title="Indicateurs Techniques", order=1)
        db.session.add(mod2_1)
        db.session.commit()
        
        lessons2_1 = [
            Lesson(module_id=mod2_1.id, title="RSI et Divergences", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Relative Strength Index</h2><p>Le RSI identifie les zones de surachat et survente...</p>"),
            Lesson(module_id=mod2_1.id, title="MACD et Croisements", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Moving Average Convergence Divergence</h2><p>Signal de momentum puissant...</p>"),
            Lesson(module_id=mod2_1.id, title="Bandes de Bollinger", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Volatilité et Écarts</h2><p>Mesurez la volatilité du marché...</p>")
        ]
        for lesson in lessons2_1:
            db.session.add(lesson)
        db.session.commit()
        
        mod2_2 = Module(course_id=course2.id, title="Patterns Chartistes", order=2)
        db.session.add(mod2_2)
        db.session.commit()
        
        lessons2_2 = [
            Lesson(module_id=mod2_2.id, title="Triangles et Fanions", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Patterns de Continuation</h2><p>Identifiez les consolidations haussières...</p>"),
            Lesson(module_id=mod2_2.id, title="Épaule-Tête-Épaule", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Pattern de Retournement</h2><p>Le pattern le plus fiable...</p>")
        ]
        for lesson in lessons2_2:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course2.title} - 2 modules, 5 lessons")
        
        # Course 3: Smart Money Concepts
        print("\n💎 Creating TECHNICAL Course: Smart Money Concepts...")
        course3 = Course(
            title="Smart Money Concepts",
            description="Tradez comme les institutionnels - Order Blocks, FVG, Liquidity",
            category=CourseCategory.TECHNICAL,
            level=CourseLevel.ADVANCED,
            thumbnail_url="/course-thumbnails/smart-money.jpg",
            duration_minutes=200,
            xp_reward=300,
            is_premium=True
        )
        db.session.add(course3)
        db.session.commit()
        
        mod3_1 = Module(course_id=course3.id, title="Concepts Fondamentaux SMC", order=1)
        db.session.add(mod3_1)
        db.session.commit()
        
        lessons3_1 = [
            Lesson(module_id=mod3_1.id, title="Order Blocks", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Zones Institutionnelles</h2><p>Où les banques placent leurs ordres...</p>"),
            Lesson(module_id=mod3_1.id, title="Fair Value Gaps (FVG)", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Inefficiences de Prix</h2><p>Les gaps que le marché revisite...</p>"),
            Lesson(module_id=mod3_1.id, title="Liquidity Sweeps", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Chasse aux Stops</h2><p>Comment les institutions piègent les traders retail...</p>")
        ]
        for lesson in lessons3_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course3.title} - 1 module, 3 lessons [PREMIUM]")
        
        # ======== PSYCHOLOGY COURSES ========
        
        # Course 4: Trading Psychology Masterclass
        print("\n🧠 Creating PSYCHOLOGY Course: Trading Psychology Masterclass...")
        course4 = Course(
            title="Trading Psychology Masterclass",
            description="Développez un mental d'acier et dominez vos émotions",
            category=CourseCategory.PSYCHOLOGY,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/psychology-master.jpg",
            duration_minutes=120,
            xp_reward=200,
            is_premium=False
        )
        db.session.add(course4)
        db.session.commit()
        
        mod4_1 = Module(course_id=course4.id, title="Maîtrise Émotionnelle", order=1)
        db.session.add(mod4_1)
        db.session.commit()
        
        lessons4_1 = [
            Lesson(module_id=mod4_1.id, title="Gérer la Peur de Perdre", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>FOMO et Revenge Trading</h2><p>Évitez les pièges psychologiques...</p>"),
            Lesson(module_id=mod4_1.id, title="Discipline de Fer", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Respecter son Plan</h2><p>La discipline bat le talent...</p>"),
            Lesson(module_id=mod4_1.id, title="Gestion des Losing Streaks", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Rebondir Après une Série de Pertes</h2><p>Techniques pour rester fort...</p>")
        ]
        for lesson in lessons4_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course4.title} - 1 module, 3 lessons")
        
        # ======== RISK MANAGEMENT COURSES ========
        
        # Course 5: Money Management Pro
        print("\n🛡️ Creating RISK Course: Money Management Pro...")
        course5 = Course(
            title="Money Management Pro",
            description="Stratégies avancées de gestion du capital",
            category=CourseCategory.RISK,
            level=CourseLevel.ADVANCED,
            thumbnail_url="/course-thumbnails/money-management.jpg",
            duration_minutes=100,
            xp_reward=220,
            is_premium=False
        )
        db.session.add(course5)
        db.session.commit()
        
        mod5_1 = Module(course_id=course5.id, title="Stratégies Avancées", order=1)
        db.session.add(mod5_1)
        db.session.commit()
        
        lessons5_1 = [
            Lesson(module_id=mod5_1.id, title="Kelly Criterion", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Optimiser la Taille de Position</h2><p>Formule mathématique pour maximiser les gains...</p>"),
            Lesson(module_id=mod5_1.id, title="Risk/Reward Ratio", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Minimum 1:2 pour Rentabilité</h2><p>Pourquoi le R:R est crucial...</p>"),
            Lesson(module_id=mod5_1.id, title="Drawdown Management", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Protéger son Capital</h2><p>Comment limiter les pertes maximales...</p>")
        ]
        for lesson in lessons5_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course5.title} - 1 module, 3 lessons")
        
        # ======== QUANT/ALGORITHMIC COURSES ========
        
        # Course 6: Algorithmic Trading Basics
        print("\n🤖 Creating QUANT Course: Algorithmic Trading Basics...")
        course6 = Course(
            title="Algorithmic Trading Basics",
            description="Introduction au trading algorithmique et aux bots",
            category=CourseCategory.QUANT,
            level=CourseLevel.ADVANCED,
            thumbnail_url="/course-thumbnails/algo-trading.jpg",
            duration_minutes=180,
            xp_reward=280,
            is_premium=True
        )
        db.session.add(course6)
        db.session.commit()
        
        mod6_1 = Module(course_id=course6.id, title="Introduction aux Algos", order=1)
        db.session.add(mod6_1)
        db.session.commit()
        
        lessons6_1 = [
            Lesson(module_id=mod6_1.id, title="Qu'est-ce qu'un Bot de Trading?", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Automatisation</h2><p>Laissez le code trader pour vous...</p>"),
            Lesson(module_id=mod6_1.id, title="Backtesting de Stratégies", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Tester sur Historique</h2><p>Validez vos stratégies avant de risquer...</p>"),
            Lesson(module_id=mod6_1.id, title="API Trading et Automation", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Connecter à votre Broker</h2><p>Python, REST APIs...</p>")
        ]
        for lesson in lessons6_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course6.title} - 1 module, 3 lessons [PREMIUM]")
        
        # ======== PLATFORM COURSES ========
        
        # Course 7: MetaTrader 5 Masterclass
        print("\n📱 Creating PLATFORM Course: MetaTrader 5 Masterclass...")
        course7 = Course(
            title="MetaTrader 5 Masterclass",
            description="Maîtrisez la plateforme MT5 de A à Z",
            category=CourseCategory.PLATFORM,
            level=CourseLevel.BEGINNER,
            thumbnail_url="/course-thumbnails/mt5.jpg",
            duration_minutes=90,
            xp_reward=120,
            is_premium=False
        )
        db.session.add(course7)
        db.session.commit()
        
        mod7_1 = Module(course_id=course7.id, title="Interface MT5", order=1)
        db.session.add(mod7_1)
        db.session.commit()
        
        lessons7_1 = [
            Lesson(module_id=mod7_1.id, title="Navigation et Graphiques", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Interface MT5</h2><p>Personnalisez votre espace de travail...</p>"),
            Lesson(module_id=mod7_1.id, title="Passer des Ordres", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Market et Pending Orders</h2><p>Types d'ordres disponibles...</p>"),
            Lesson(module_id=mod7_1.id, title="Indicateurs et EAs", order=3, lesson_type=LessonType.TEXT,
                   content="<h2>Personnalisation Avancée</h2><p>Ajoutez des indicateurs custom...</p>")
        ]
        for lesson in lessons7_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course7.title} - 1 module, 3 lessons")
        
        # Course 8: TradingView Pro
        print("\n📊 Creating PLATFORM Course: TradingView Pro...")
        course8 = Course(
            title="TradingView Pro",
            description="Utilisez TradingView comme un professionnel",
            category=CourseCategory.PLATFORM,
            level=CourseLevel.INTERMEDIATE,
            thumbnail_url="/course-thumbnails/tradingview.jpg",
            duration_minutes=100,
            xp_reward=150,
            is_premium=False
        )
        db.session.add(course8)
        db.session.commit()
        
        mod8_1 = Module(course_id=course8.id, title="Outils TradingView", order=1)
        db.session.add(mod8_1)
        db.session.commit()
        
        lessons8_1 = [
            Lesson(module_id=mod8_1.id, title="Pine Script Basics", order=1, lesson_type=LessonType.TEXT,
                   content="<h2>Créer vos Indicateurs</h2><p>Codez vos propres outils...</p>"),
            Lesson(module_id=mod8_1.id, title="Alertes et Notifications", order=2, lesson_type=LessonType.TEXT,
                   content="<h2>Ne Ratez Plus Rien</h2><p>Configurez des alertes intelligentes...</p>")
        ]
        for lesson in lessons8_1:
            db.session.add(lesson)
        db.session.commit()
        
        print(f"  ✓ {course8.title} - 1 module, 2 lessons")
        
        db.session.commit()
        
        # Summary
        final_count = Course.query.count()
        print("\n" + "=" * 60)
        print("✅ Academy Successfully Expanded!")
        print(f"Total Courses: {final_count}")
        print(f"New Courses Added: {final_count - existing_count}")
        print("\nBy Category:")
        for cat in CourseCategory:
            count = Course.query.filter_by(category=cat).count()
            print(f"  {cat.value}: {count} courses")

if __name__ == '__main__':
    add_more_courses()
