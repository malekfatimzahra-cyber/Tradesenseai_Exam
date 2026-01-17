from app import app, db
from models import Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, LessonType
import datetime

def seed_full_academy():
    with app.app_context():
        print("🚀 Starting Full Academy Seeding...")

        courses_data = [
            {
                "id": 1,
                "title": "Introduction au Trading",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.BEGINNER,
                "description": "Apprenez les bases du trading Forex et CFD. Maîtrisez les concepts de base du marché.",
                "thumbnail_url": "/course-1.jpg",
                "modules": [
                    {
                        "title": "Les Bases du Marché",
                        "lessons": [
                            {"title": "Qu'est-ce que le Trading ?", "content": "<h2>Introduction au Trading</h2><p>Le trading est l'échange d'actifs financiers...</p>"},
                            {"title": "Les Acteurs du Marché", "content": "<h2>Les Acteurs</h2><p>Banques, Institutions, Traders particuliers...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Fondamentaux",
                            "questions": [
                                {
                                    "text": "Qui sont les plus gros acteurs du Forex ?",
                                    "explanation": "Les banques centrales et commerciales dominent les volumes.",
                                    "options": [
                                        {"text": "Les traders particuliers", "correct": False},
                                        {"text": "Les Banques Centrales", "correct": True},
                                        {"text": "Les influenceurs YouTube", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 2,
                "title": "Analyse Technique Avancée",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Maîtrisez les indicateurs techniques et patterns graphiques pour prédire les mouvements.",
                "thumbnail_url": "/course-2.jpg",
                "modules": [
                    {
                        "title": "Indicateurs de Tendance",
                        "lessons": [
                            {"title": "Moyennes Mobiles (EMA/SMA)", "content": "<h2>Les Moyennes Mobiles</h2><p>L'EMA donne plus de poids aux prix récents...</p>"},
                            {"title": "Le RSI et les Divergences", "content": "<h2>RSI</h2><p>Le Relative Strength Index mesure la force du mouvement...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Indicateurs",
                            "questions": [
                                {
                                    "text": "Que signifie une divergence RSI ?",
                                    "explanation": "Une divergence indique un essoufflement de la tendance actuelle.",
                                    "options": [
                                        {"text": "Le prix et l'indicateur vont dans le même sens", "correct": False},
                                        {"text": "Le prix fait un nouveau plus haut mais pas l'indicateur", "correct": True},
                                        {"text": "Le prix s'arrête de bouger", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 3,
                "title": "Smart Money Concepts",
                "category": CourseCategory.TECHNICAL,
                "level": CourseLevel.ADVANCED,
                "description": "Tradez comme les institutionnels - Order Blocks, Liquidity et Market Structure.",
                "thumbnail_url": "/course-3.jpg",
                "modules": [
                    {
                        "title": "Market Structure (BOS & CHoCH)",
                        "lessons": [
                            {"title": "Break of Structure (BOS)", "content": "<h2>BOS</h2><p>Un BOS confirme la continuation d'une tendance...</p>"},
                            {"title": "Change of Character (CHoCH)", "content": "<h2>CHoCH</h2><p>Un CHoCH indique un potentiel retournement de tendance...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Structure SMC",
                            "questions": [
                                {
                                    "text": "Quelle est la différence entre BOS et CHoCH ?",
                                    "explanation": "BOS = Continuation, CHoCH = Retournement.",
                                    "options": [
                                        {"text": "C'est la même chose", "correct": False},
                                        {"text": "Le CHoCH est le premier signe de changement de direction", "correct": True},
                                        {"text": "Le BOS est utilisé uniquement en Range", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 4,
                "title": "Trading Psychology Masterclass",
                "category": CourseCategory.PSYCHOLOGY,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Développez un mental d'acier et dominez vos émotions lors des trades.",
                "thumbnail_url": "/course-4.jpg",
                "modules": [
                    {
                        "title": "Biais Cognitifs en Trading",
                        "lessons": [
                            {"title": "L'aversion à la perte", "content": "<h2>Aversion à la perte</h2><p>Pourquoi nous gardons nos pertes trop longtemps...</p>"},
                            {"title": "L'excès de confiance", "content": "<h2>Overconfidence</h2><p>Le danger après une série de gains...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Psychologie",
                            "questions": [
                                {
                                    "text": "Quel est le biais qui pousse à trader par vengeance ?",
                                    "explanation": "Le Revenge Trading est souvent dû à l'incapacité d'accepter une perte.",
                                    "options": [
                                        {"text": "Le biais de confirmation", "correct": False},
                                        {"text": "L'aversion à la perte", "correct": True},
                                        {"text": "L'effet de halo", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 5,
                "title": "Money Management Pro",
                "category": CourseCategory.RISK,
                "level": CourseLevel.ADVANCED,
                "description": "Stratégies avancées de gestion du capital et contrôle drastique du risque.",
                "thumbnail_url": "/course-5.jpg",
                "modules": [
                    {
                        "title": "Dimensionnement de Position",
                        "lessons": [
                            {"title": "Calcul de Lot", "content": "<h2>Calculer sa taille</h2><p>Le risque doit être fixe en pourcentage du capital...</p>"},
                            {"title": "Le Kelly Criterion", "content": "<h2>Critère de Kelly</h2><p>Une formule mathématique pour optimiser la taille des paris...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Gestion du Risque",
                            "questions": [
                                {
                                    "text": "Si vous risquez 1% par trade, combien de pertes consécutives faut-il pour perdre 50% ?",
                                    "explanation": "Grâce aux intérêts composés inversés, c'est environ 69 trades.",
                                    "options": [
                                        {"text": "50 trades", "correct": False},
                                        {"text": "69 trades", "correct": True},
                                        {"text": "100 trades", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 6,
                "title": "Algorithmic Trading Basics",
                "category": CourseCategory.QUANT,
                "level": CourseLevel.ADVANCED,
                "description": "Introduction au trading algorithmique et création de bots de trading.",
                "thumbnail_url": "/course-6.jpg",
                "modules": [
                    {
                        "title": "Introduction aux EAs",
                        "lessons": [
                            {"title": "Qu'est-ce qu'un Expert Advisor ?", "content": "<h2>Les EAs</h2><p>Un programme qui exécute des trades automatiquement...</p>"},
                            {"title": "Backtesting 101", "content": "<h2>Backtesting</h2><p>Tester sa stratégie sur les données historiques...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : Algorithmique",
                            "questions": [
                                {
                                    "text": "Quel langage est utilisé par défaut sur MetaTrader 5 ?",
                                    "explanation": "MT5 utilise le MQL5.",
                                    "options": [
                                        {"text": "Python", "correct": False},
                                        {"text": "MQL5", "correct": True},
                                        {"text": "PineScript", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 7,
                "title": "MetaTrader 5 Masterclass",
                "category": CourseCategory.PLATFORM,
                "level": CourseLevel.BEGINNER,
                "description": "Maîtrisez la plateforme MT5 de A à Z : ordres, indicateurs, templates.",
                "thumbnail_url": "/course-7.jpg",
                "modules": [
                    {
                        "title": "Interface et Ordres",
                        "lessons": [
                            {"title": "Navigation dans MT5", "content": "<h2>Interface MT5</h2><p>Market Watch, Navigator, Toolbox...</p>"},
                            {"title": "Exécution d'ordres complexes", "content": "<h2>Ordres Différés</h2><p>Buy Limit, Sell Stop, Buy Stop Limit...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : MT5",
                            "questions": [
                                {
                                    "text": "Où se trouvent vos trades ouverts dans MT5 ?",
                                    "explanation": "L'onglet 'Trade' de la Toolbox affiche les positions en cours.",
                                    "options": [
                                        {"text": "Le Market Watch", "correct": False},
                                        {"text": "La Toolbox (Boîte à outils)", "correct": True},
                                        {"text": "Le Navigator", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "id": 8,
                "title": "TradingView Pro",
                "category": CourseCategory.PLATFORM,
                "level": CourseLevel.INTERMEDIATE,
                "description": "Utilisez TradingView comme un professionnel : alertes, scripts et layouts.",
                "thumbnail_url": "/course-8.jpg",
                "modules": [
                    {
                        "title": "Outils de Dessin et Alertes",
                        "lessons": [
                            {"title": "Maîtriser les Fibonaccis", "content": "<h2>Retracements de Fibonacci</h2><p>Utiliser les ratios d'or pour trouver des supports...</p>"},
                            {"title": "Système d'Alertes Avancé", "content": "<h2>Alertes</h2><p>Paramétrer des alertes sur indicateurs ou prix...</p>"}
                        ],
                        "quiz": {
                            "title": "Quiz : TradingView",
                            "questions": [
                                {
                                    "text": "Comment s'appelle le langage de script de TradingView ?",
                                    "explanation": "TradingView utilise le PineScript.",
                                    "options": [
                                        {"text": "JavaScript", "correct": False},
                                        {"text": "PineScript", "correct": True},
                                        {"text": "MQL4", "correct": False}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        ]

        for c_data in courses_data:
            course = Course.query.get(c_data["id"])
            if not course:
                print(f"Adding course: {c_data['title']}")
                course = Course(
                    id=c_data["id"],
                    title=c_data["title"],
                    category=c_data["category"],
                    level=c_data["level"],
                    description=c_data["description"],
                    thumbnail_url=c_data["thumbnail_url"],
                    lang="fr",
                    duration_minutes=120,
                    xp_reward=1000
                )
                db.session.add(course)
            else:
                print(f"Updating course: {c_data['title']}")
                course.title = c_data["title"]
                course.category = c_data["category"]
                course.level = c_data["level"]
                course.description = c_data["description"]
                course.thumbnail_url = c_data["thumbnail_url"]

            db.session.commit()

            # Modules
            for mod_idx, m_data in enumerate(c_data["modules"]):
                module = Module.query.filter_by(course_id=course.id, title=m_data["title"]).first()
                if not module:
                    module = Module(
                        course_id=course.id,
                        title=m_data["title"],
                        order_index=mod_idx + 1
                    )
                    db.session.add(module)
                    db.session.commit()

                # Lessons
                for less_idx, l_data in enumerate(m_data["lessons"]):
                    lesson = Lesson.query.filter_by(module_id=module.id, title=l_data["title"]).first()
                    if not lesson:
                        lesson = Lesson(
                            module_id=module.id,
                            title=l_data["title"],
                            content=l_data["content"],
                            content_type="html",
                            order_index=less_idx + 1,
                            slug=l_data["title"].lower().replace(" ", "-")
                        )
                        db.session.add(lesson)

                # Quiz
                if "quiz" in m_data:
                    quiz = Quiz.query.filter_by(module_id=module.id).first()
                    if not quiz:
                        quiz = Quiz(
                            module_id=module.id,
                            title=m_data["quiz"]["title"],
                            min_pass_score=70
                        )
                        db.session.add(quiz)
                        db.session.commit()

                        for q_idx, q_data in enumerate(m_data["quiz"]["questions"]):
                            question = Question(
                                quiz_id=quiz.id,
                                text=q_data["text"],
                                explanation=q_data["explanation"],
                                order_index=q_idx + 1
                            )
                            db.session.add(question)
                            db.session.commit()

                            for o_data in q_data["options"]:
                                option = Option(
                                    question_id=question.id,
                                    text=o_data["text"],
                                    is_correct=o_data["correct"]
                                )
                                db.session.add(option)

            db.session.commit()

        print("✅ Full Academy Seeding Completed!")

if __name__ == "__main__":
    seed_full_academy()
