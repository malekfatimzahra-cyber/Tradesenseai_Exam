from app import app, db
from models import Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, LessonType

def seed_intro_trading():
    with app.app_context():
        print("🌱 Seeding 'Introduction au Trading (FR)'...")
        
        # 1. Create Course
        course = Course(
            title="Introduction au Trading (FR)",
            lang="fr",
            description="Apprenez les bases du trading Forex et CFD. Maîtrisez les concepts de base du marché.",
            category=CourseCategory.TECHNICAL,
            level=CourseLevel.BEGINNER,
            thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800",
            duration_minutes=120,
            xp_reward=1000,
            is_premium=False
        )
        db.session.add(course)
        db.session.commit()
        
        # 2. Create Module 1
        module1 = Module(
            course_id=course.id,
            title="Module 1: Les Fondamentaux",
            order_index=1
        )
        db.session.add(module1)
        db.session.commit()
        
        # 3. Create Lessons
        lessons_data = [
            {
                "title": "Qu’est-ce que le trading ?",
                "content": """
<h2>Qu'est-ce que le trading ?</h2>
<p>Le trading est l'art d'acheter et de vendre des actifs financiers sur les marchés mondiaux dans le but de réaliser un profit à partir des variations de prix.</p>

<h3>Les principes de base</h3>
<ul>
    <li><strong>Achat (Long) :</strong> Vous achetez un actif en espérant que son prix augmente pour le revendre plus cher.</li>
    <li><strong>Vente (Short) :</strong> Vous vendez un actif (que vous empruntez souvent via un courtier) en espérant que son prix baisse pour le racheter moins cher.</li>
</ul>

<div class="alert">
    <strong>Note :</strong> Contrairement à l'investissement à long terme, le trading se concentre souvent sur des horizons de temps plus courts (secondes, minutes, heures ou jours).
</div>

<h3>Pourquoi trader ?</h3>
<p>Le trading offre une liberté financière potentielle et la possibilité de travailler de n'importe où, mais il comporte des risques importants de perte en capital.</p>
""",
                "content_type": "html"
            },
            {
                "title": "Les actifs financiers",
                "content": """
<h2>Les actifs financiers</h2>
<p>Dans le monde du trading, vous pouvez échanger une multitude d'instruments. Voici les catégories principales :</p>

<h3>1. Le Forex (Marché des devises)</h3>
<p>C'est le marché le plus liquide au monde. On y échange des paires de monnaies comme l'<strong>EUR/USD</strong> ou le <strong>GBP/JPY</strong>.</p>

<h3>2. Les Actions</h3>
<p>Représentent des parts de propriété d'une entreprise (ex: Apple, Tesla, LVMH).</p>

<h3>3. Les Indices</h3>
<p>Mesurent la performance d'un groupe d'actions d'un pays ou secteur (ex: NASDAQ, DAX, CAC 40).</p>

<h3>4. Les Cryptomonnaies</h3>
<p>Actifs numériques décentralisés (ex: Bitcoin, Ethereum).</p>

<h3>5. Les Matières Premières</h3>
<p>Produits physiques comme l'Or (Gold), le Pétrole (Oil) ou le Gaz.</p>
""",
                "content_type": "html"
            },
            {
                "title": "Gestion du risque (bases)",
                "content": """
<h2>Gestion du risque : La Clé de la Survie</h2>
<p>La règle numéro 1 en trading n'est pas de gagner de l'argent, mais de <strong>ne pas le perdre</strong>.</p>

<h3>Le Ratio Risque/Récompense (Risk/Reward)</h3>
<p>Ne prenez jamais un trade si le gain potentiel n'est pas au moins 2 fois supérieur au risque pris (Ratio 1:2).</p>

<h3>Le Risque par Trade</h3>
<ul>
    <li>Utilisez la règle des <strong>1% ou 2%</strong>.</li>
    <li>Si vous avez 10 000 MAD sur votre compte, ne risquez jamais plus de 100 ou 200 MAD sur une seule position.</li>
</ul>

<div class="alert" style="background: #fee; border-left: 4px solid #f55; padding: 10px;">
    <strong>Crucial :</strong> Sans gestion du risque, même la meilleure stratégie finira par vider votre compte.
</div>
""",
                "content_type": "html"
            },
            {
                "title": "Types d’ordres (Market/Limit/Stop)",
                "content": """
<h2>Maîtriser les Types d'Ordres</h2>
<p>Pour entrer ou sortir du marché, vous devez utiliser différents types d'ordres :</p>

<h3>1. Ordre au Marché (Market Order)</h3>
<p>Exécution immédiate au prix actuel. Utile pour entrer vite, mais vous ne contrôlez pas le prix exact.</p>

<h3>2. Ordre Limite (Limit Order)</h3>
<p>Vous fixez un prix spécifique. L'ordre ne sera exécuté que si le marché atteint ce prix (ou un meilleur prix). Idéal pour acheter à bas prix ou vendre à haut prix.</p>

<h3>3. Ordre Stop (Stop Order)</h3>
<p>Un ordre qui devient un ordre au marché une fois qu'un prix spécifié est atteint. Souvent utilisé pour le <strong>Stop Loss</strong> afin de limiter les pertes.</p>
""",
                "content_type": "html"
            },
            {
                "title": "Psychologie du trader (bases)",
                "content": """
<h2>La Psychologie : 80% du Succès</h2>
<p>Le trading est un combat contre vous-même, pas contre le marché.</p>

<h3>Les deux émotions fatales</h3>
<ul>
    <li><strong>La Peur :</strong> Vous empêche de prendre de bons trades ou vous fait sortir trop tôt par crainte d'une perte.</li>
    <li><strong>L'Avidité (Greed) :</strong> Vous pousse à risquer trop gros ou à ne pas prendre vos profits en espérant "gagner encore plus".</li>
</ul>

<h3>Le FOMO (Fear Of Missing Out)</h3>
<p>La peur de rater une opportunité. C'est ce qui vous pousse à entrer en retard dans un mouvement qui a déjà commencé.</p>

<p><strong>Conseil :</strong> Développez une routine et restez discipliné. Suivez votre plan, pas vos émotions.</p>
""",
                "content_type": "html"
            }
        ]
        
        for i, ld in enumerate(lessons_data):
            lesson = Lesson(
                module_id=module1.id,
                title=ld["title"],
                slug=ld["title"].lower().replace(" ", "-"),
                content=ld["content"],
                content_type=ld["content_type"],
                order_index=i + 1
            )
            db.session.add(lesson)
        db.session.commit()
        
        # 4. Create Quiz for Module 1
        quiz = Quiz(
            module_id=module1.id,
            title="Quiz du module : Les Fondamentaux",
            min_pass_score=70
        )
        db.session.add(quiz)
        db.session.commit()
        
        # 5. Create Quiz Questions
        questions = [
            {
                "question": "Quel est l'objectif principal du trading ?",
                "explanation": "Le trading vise à profiter des variations de prix des actifs financiers.",
                "options": [
                    {"text": "Collectionner des devises rares", "correct": False},
                    {"text": "Réaliser un profit sur les variations de prix", "correct": True},
                    {"text": "Éviter tout contact avec les banques", "correct": False},
                    {"text": "Devenir propriétaire de banques", "correct": False}
                ]
            },
            {
                "question": "Que signifie être 'Long' sur un actif ?",
                "explanation": "Être long signifie que vous achetez l'actif en espérant une hausse de son prix.",
                "options": [
                    {"text": "Parier sur la baisse", "correct": False},
                    {"text": "Garder la position pendant des années", "correct": False},
                    {"text": "Acheter en espérant une hausse", "correct": True},
                    {"text": "Vendre sans posséder l'actif", "correct": False}
                ]
            },
            {
                "question": "Quelle est la règle recommandée pour le risque par trade ?",
                "explanation": "Il est conseillé de ne pas risquer plus de 1% à 2% de son capital par trade.",
                "options": [
                    {"text": "Risquez tout sur un bon trade", "correct": False},
                    {"text": "10% à 20% par trade", "correct": False},
                    {"text": "1% à 2% par trade", "correct": True},
                    {"text": "Ne jamais mettre de Stop Loss", "correct": False}
                ]
            },
            {
                "question": "Un ordre 'Limit' est utilisé pour :",
                "explanation": "Un ordre limite permet de spécifier le prix exact (ou mieux) auquel vous souhaitez être exécuté.",
                "options": [
                    {"text": "Entrer immédiatement au prix actuel", "correct": False},
                    {"text": "Spécifier un prix d'exécution souhaité", "correct": True},
                    {"text": "Fermer le compte de trading", "correct": False},
                    {"text": "Payer moins de commissions", "correct": False}
                ]
            }
        ]
        
        for i, qd in enumerate(questions):
            q = Question(
                quiz_id=quiz.id,
                text=qd["question"],
                explanation=qd["explanation"],
                order_index=i + 1
            )
            db.session.add(q)
            db.session.commit()
            
            for od in qd["options"]:
                opt = Option(
                    question_id=q.id,
                    text=od["text"],
                    is_correct=od["correct"]
                )
                db.session.add(opt)
        
        db.session.commit()
        print("✅ Course 'Introduction au Trading (FR)' seeded successfully!")

if __name__ == "__main__":
    seed_intro_trading()
