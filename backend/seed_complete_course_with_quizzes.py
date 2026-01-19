
import os
import sys

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, LessonType

def seed_complete_course_with_quizzes():
    with app.app_context():
        print("🚀 Starting Complete Course Seeding...")

        # 1. Define the Course
        course_title = "Introduction au Trading"
        
        # Check if course exists
        existing_course = Course.query.filter_by(title=course_title).first()
        if existing_course:
            print(f"♻️ Course '{course_title}' found. DELETING to ensure clean fresh seed...")
            db.session.delete(existing_course)
            db.session.commit()
            print("🗑️ Old course deleted.")
        
        print(f"📚 Creating new course: {course_title}")
        course = Course(
            title=course_title,
             # ... rest of creation logic remains valid because we deleted 'existing_course' so we flow into creation
                lang='fr',
                description="Le guide ultime pour débuter sur les marchés financiers. Apprenez tout de A à Z : vocabulaire, analyse, psychologie et gestion du risque.",
                category=CourseCategory.TECHNICAL,
                level=CourseLevel.BEGINNER,
                thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000",
                duration_minutes=300,
                xp_reward=2500,
                is_premium=False
            )
        db.session.add(course)
        db.session.flush()

        # 2. Define Content Structure
        # Format: (Module Title, [List of Lessons], Quiz Data)
        # Lesson: (Title, Content HTML)
        # Quiz: (Title, Questions List)
        # Question: (Text, Explanation, Options List)
        # Option: (Text, IsCorrect)

        modules_data = [
            {
                "title": "Module 1: Les Fondamentaux du Trading",
                "lessons": [
                    {
                        "title": "Qu'est-ce que le Trading ?",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">Introduction</h3>
                                <p>Le trading consiste à acheter et vendre des actifs financiers (actions, devises, matières premières) dans le but de réaliser un profit. Contrairement à l'investissement long terme, le trading cherche à profiter des fluctuations de prix à court ou moyen terme.</p>
                                
                                <div class="bg-gray-800 p-4 rounded-xl border-l-4 border-yellow-500">
                                    <h4 class="font-bold text-white mb-2">Concept Clé : L'Offre et la Demande</h4>
                                    <p class="text-sm">Le prix d'un actif monte si la demande dépasse l'offre (plus d'acheteurs), et baisse si l'offre dépasse la demande (plus de vendeurs).</p>
                                </div>

                                <h3 class="text-xl font-bold text-white mt-8">Les Différents Types de Marchés</h3>
                                <ul class="list-disc pl-5 space-y-2">
                                    <li><strong class="text-blue-400">Forex :</strong> Le marché des devises (ex: EUR/USD). C'est le plus liquide au monde.</li>
                                    <li><strong class="text-purple-400">Actions :</strong> Parts d'entreprises (ex: Apple, Tesla).</li>
                                    <li><strong class="text-green-400">Indices :</strong> Paniers d'actions représentatifs d'une économie (ex: S&P 500, CAC 40).</li>
                                    <li><strong class="text-yellow-400">Crypto :</strong> Actifs numériques décentralisés (ex: Bitcoin, Ethereum).</li>
                                    <li><strong class="text-red-400">Matières Premières :</strong> Or, Pétrole, Blé, etc.</li>
                                </ul>
                            </div>
                        """
                    },
                    {
                        "title": "Terminologie Essentielle (Pip, Spread, Levier)",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">Le Vocabulaire du Trader</h3>
                                
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="bg-gray-800 p-4 rounded-lg">
                                        <h4 class="font-bold text-blue-400 text-lg">PIP (Percentage in Point)</h4>
                                        <p class="text-sm mt-2">L'unité de mesure standard pour le changement de valeur entre deux devises. Pour l'EUR/USD, c'est la 4ème décimale (0.0001).</p>
                                    </div>
                                    <div class="bg-gray-800 p-4 rounded-lg">
                                        <h4 class="font-bold text-red-400 text-lg">Spread</h4>
                                        <p class="text-sm mt-2">La différence entre le prix d'achat (Ask) et le prix de vente (Bid). C'est la commission du courtier.</p>
                                    </div>
                                    <div class="bg-gray-800 p-4 rounded-lg">
                                        <h4 class="font-bold text-green-400 text-lg">Effet de Levier</h4>
                                        <p class="text-sm mt-2">Un outil qui permet de multiplier votre exposition sur le marché. Un levier de 1:100 signifie que pour 1$ investi, vous contrôlez 100$. <span class="text-red-500 font-bold">Attention : cela multiplie aussi les risques !</span></p>
                                    </div>
                                    <div class="bg-gray-800 p-4 rounded-lg">
                                        <h4 class="font-bold text-purple-400 text-lg">Lot</h4>
                                        <p class="text-sm mt-2">L'unité de volume standard. 1 Lot Standard = 100,000 unités de la devise de base.</p>
                                    </div>
                                </div>
                            </div>
                        """
                    }
                ],
                "quiz": {
                    "title": "Quiz - Les Bases",
                    "questions": [
                        {
                            "text": "Qu'est-ce qu'un PIP ?",
                            "explanation": "Le PIP (Percentage in Point) est la plus petite variation de prix standard pour la plupart des paires de devises, généralement la 4ème décimale.",
                            "options": [
                                {"text": "Percentage in Point", "is_correct": True},
                                {"text": "Price Interest Point", "is_correct": False},
                                {"text": "Profit Is Priority", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Si l'offre est supérieure à la demande, le prix...",
                            "explanation": "C'est la loi de l'offre et la demande. Plus de vendeurs que d'acheteurs fait baisser les prix.",
                            "options": [
                                {"text": "Monte", "is_correct": False},
                                {"text": "Baisse", "is_correct": True},
                                {"text": "Reste stable", "is_correct": False}
                            ]
                        }
                    ]
                }
            },
            {
                "title": "Module 2: Analyse Technique",
                "lessons": [
                    {
                        "title": "Les Chandeliers Japonais",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">Lire le Marché</h3>
                                <p>Les chandeliers japonais racontent l'histoire du prix sur une période donnée (1h, 4h, 1j...). Chaque bougie a 4 informations clés :</p>
                                
                                <ul class="list-none space-y-3">
                                    <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span><strong>Open (O) :</strong> Prix d'ouverture</li>
                                    <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span><strong>High (H) :</strong> Plus haut atteint</li>
                                    <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span><strong>Low (L) :</strong> Plus bas atteint</li>
                                    <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span><strong>Close (C) :</strong> Prix de clôture</li>
                                </ul>

                                <div class="mt-6 border border-gray-700 p-6 rounded-xl flex justify-center bg-gray-900">
                                    <!-- Simple SVG illustration of a candle -->
                                    <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <rect x="85" y="60" width="30" height="80" fill="#22c55e" />
                                        <line x1="100" y1="30" x2="100" y2="60" stroke="#22c55e" stroke-width="2"/>
                                        <line x1="100" y1="140" x2="100" y2="170" stroke="#22c55e" stroke-width="2"/>
                                        <text x="130" y="40" fill="white" font-size="12">High</text>
                                        <text x="130" y="70" fill="white" font-size="12">Open</text>
                                        <text x="130" y="140" fill="white" font-size="12">Close</text>
                                        <text x="130" y="170" fill="white" font-size="12">Low</text>
                                    </svg>
                                </div>
                            </div>
                        """
                    },
                    {
                        "title": "Support et Résistance",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">Zones Clés</h3>
                                <p>Le marché a de la mémoire. Il réagit souvent aux mêmes niveaux de prix.</p>

                                <div class="grid grid-cols-1 gap-6 mt-4">
                                    <div class="bg-gray-800 p-6 rounded-xl border-l-4 border-green-500">
                                        <h4 class="text-xl font-bold text-white">Support (Le Sol)</h4>
                                        <p class="mt-2">Un niveau de prix où la demande est assez forte pour empêcher le prix de descendre plus bas. Les acheteurs interviennent ici.</p>
                                    </div>
                                    <div class="bg-gray-800 p-6 rounded-xl border-l-4 border-red-500">
                                        <h4 class="text-xl font-bold text-white">Résistance (Le Plafond)</h4>
                                        <p class="mt-2">Un niveau de prix où l'offre est assez forte pour empêcher le prix de monter plus haut. Les vendeurs interviennent ici.</p>
                                    </div>
                                </div>

                                <p class="text-sm italic text-gray-500 mt-4">Astuce : Un support cassé devient souvent une résistance future, et inversement.</p>
                            </div>
                        """
                    }
                ],
                "quiz": {
                    "title": "Quiz - Analyse Technique",
                    "questions": [
                        {
                            "text": "Quelles sont les 4 informations d'une bougie ?",
                            "explanation": "Open, High, Low, Close (OHLC) définissent la structure complète d'une bougie.",
                            "options": [
                                {"text": "Open, Close, Volume, Temps", "is_correct": False},
                                {"text": "Open, High, Low, Close", "is_correct": True},
                                {"text": "Achat, Vente, Stop, Limite", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Que se passe-t-il souvent quand un support est cassé ?",
                            "explanation": "C'est le principe de 'changement de polarité'. Le sol devient plafond.",
                            "options": [
                                {"text": "Il disparaît", "is_correct": False},
                                {"text": "Il devient résistance", "is_correct": True},
                                {"text": "Le prix remonte immédiatement", "is_correct": False}
                            ]
                        }
                    ]
                }
            },
            {
                "title": "Module 3: Psychologie et Gestion du Risque",
                "lessons": [
                    {
                        "title": "La Règle des 1%",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">Protéger son Capital</h3>
                                <p>La règle d'or des traders professionnels : <strong>Ne jamais risquer plus de 1% de son capital total sur une seule transaction.</strong></p>

                                <div class="bg-blue-900/30 p-6 rounded-xl border border-blue-500/30 mt-4">
                                    <h4 class="font-bold text-blue-400 mb-2">Exemple Concret</h4>
                                    <p>Capital : 10,000 €</p>
                                    <p>Risque Max par trade : 1% = 100 €</p>
                                    <p class="mt-2 text-sm opacity-80">Si votre Stop Loss est à 20 pips, la valeur de votre lot doit être calculée pour que 20 pips = 100 €. Vous ne perdrez ainsi jamais votre compte sur un coup de malchance.</p>
                                </div>
                            </div>
                        """
                    },
                    {
                        "title": "FOMO et Discipline",
                        "content": """
                            <div class="space-y-6 text-gray-300">
                                <h3 class="text-2xl font-bold text-yellow-500">L'Ennemi Intérieur</h3>
                                <h4 class="font-bold text-white mt-4">FOMO (Fear Of Missing Out)</h4>
                                <p>La peur de rater une opportunité. Elle pousse à entrer en position trop tard, quand le prix a déjà explosé. Résultat : on achète souvent au plus haut avant la chute.</p>

                                <h4 class="font-bold text-white mt-4">Le Trading de Revanche</h4>
                                <p>Vouloir "refaire" ses pertes immédiatement après un trade perdant. C'est le meilleur moyen de perdre encore plus.</p>

                                <div class="bg-green-900/20 p-4 rounded-lg mt-6 text-center border border-green-500/30">
                                    <p class="text-green-400 font-bold">"Planifiez votre trade, et tradez votre plan."</p>
                                </div>
                            </div>
                        """
                    }
                ],
                "quiz": {
                    "title": "Quiz Final - Psychologie",
                    "questions": [
                        {
                            "text": "Quelle est la règle d'or du risque par trade ?",
                            "explanation": "1% (ou 2% max pour les agressifs) permet de survivre à une série de pertes.",
                            "options": [
                                {"text": "5%", "is_correct": False},
                                {"text": "10%", "is_correct": False},
                                {"text": "1%", "is_correct": True}
                            ]
                        },
                        {
                            "text": "Qu'est-ce que le FOMO ?",
                            "explanation": "Fear Of Missing Out : La peur de rater une occasion, menant à des décisions impulsives.",
                            "options": [
                                {"text": "Une stratégie de couverture", "is_correct": False},
                                {"text": "La peur de rater une opportunité", "is_correct": True},
                                {"text": "Un indicateur technique", "is_correct": False}
                            ]
                        }
                    ]
                }
            }
        ]

        # 3. Create Content in DB
        for mod_idx, m_data in enumerate(modules_data):
            # Create Module
            module = Module(
                course_id=course.id,
                title=m_data['title'],
                order_index=mod_idx + 1
            )
            db.session.add(module)
            db.session.flush() # Get module.id
            print(f"  📂 Created Module: {module.title}")

            # Create Lessons
            for less_idx, l_data in enumerate(m_data['lessons']):
                lesson = Lesson(
                    module_id=module.id,
                    title=l_data['title'],
                    content=l_data['content'],
                    content_type='html',
                    lesson_type=LessonType.TEXT,
                    order_index=less_idx + 1
                )
                db.session.add(lesson)
                # Flush not strictly needed here unless we link quiz to lesson specifically
            
            print(f"    📝 Added {len(m_data['lessons'])} lessons.")

            # Create Quiz for Module
            if 'quiz' in m_data:
                q_data = m_data['quiz']
                quiz = Quiz(
                    module_id=module.id,
                    course_id=course.id, # Optional link
                    title=q_data['title'],
                    min_pass_score=70
                )
                db.session.add(quiz)
                db.session.flush()
                print(f"    ❓ Created Quiz: {quiz.title}")

                # Create Questions
                for qst_idx, question_data in enumerate(q_data['questions']):
                    question = Question(
                        quiz_id=quiz.id,
                        text=question_data['text'],
                        explanation=question_data.get('explanation', ''),
                        order_index=qst_idx + 1
                    )
                    db.session.add(question)
                    db.session.flush()

                    # Create Options
                    for opt_data in question_data['options']:
                        option = Option(
                            question_id=question.id,
                            text=opt_data['text'],
                            is_correct=opt_data['is_correct']
                        )
                        db.session.add(option)

        db.session.commit()
        print("\n✅ SUCCESS: Complete Course Content & Quizzes seeded successfully!")

if __name__ == "__main__":
    seed_complete_course_with_quizzes()
