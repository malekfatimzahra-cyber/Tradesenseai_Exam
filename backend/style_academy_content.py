
import os
from app import app
from models import db, Lesson, LessonTranslation
from sqlalchemy import text

# ==========================================
# 🎨 STYLING CONSTANTS & TEMPLATES
# ==========================================

STYLE_YELLOW = "color: #fbbf24;" # amber-400
STYLE_BLUE   = "color: #60a5fa;" # blue-400
STYLE_RED    = "color: #f87171;" # red-400
STYLE_GREEN  = "color: #4ade80;" # green-400

BOX_BLUE = "background-color: rgba(30, 58, 138, 0.4); border-left: 4px solid #3b82f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;"
BOX_RED  = "background-color: rgba(127, 29, 29, 0.4); border-left: 4px solid #ef4444; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;"
BOX_GREEN = "background-color: rgba(20, 83, 45, 0.4); border-left: 4px solid #22c55e; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;"
BOX_YELLOW = "background-color: rgba(120, 53, 15, 0.4); border-left: 4px solid #f59e0b; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem;"

def get_base_content(title):
    """
    Returns specific text snippets based on keyword matching in the title.
    This ensures the content 'feels' real and relevant.
    """
    title_lower = title.lower()
    
    # Defaults
    definition = f"Le concept de <strong>{title}</strong> est un pilier fondamental pour tout trader sérieux. Il permet de structurer votre approche et d'éviter les décisions émotionnelles."
    why_important = "Sans cette compréhension, vous naviguez à l'aveugle. Les professionnels l'utilisent quotidiennement pour filtrer les faux signaux et augmenter leur taux de réussite."
    
    context_keys = ["Analysons la structure du marché", "Observons la réaction du prix", "Identifiez la tendance de fond"]
    concept_list = ["La relation prix-temps", "La psychologie des intervenants", "Les zones de liquidité"]
    
    steps = ["Identifier la zone sur H4", "Attendre une réaction sur M15", "Entrer avec un stop défini"]
    example = "Le marché arrive sur une résistance majeure. Au lieu de vendre immédiatement, nous attendons une bougie de rejet (Pinbar). Une fois clôturée, nous entrons en position."
    
    mistakes = ["Entrer trop tôt sans confirmation", "Ignorer la tendance de fond", "Risquer plus de 2% du capital"]
    checklist = ["Tendance identifiée ?", "Zone tracée ?", "Ratio Risque/Recompense > 2 ?"]

    # ---------------- Specific Logic ----------------
    
    if "paires" in title_lower or "currency" in title_lower:
        definition = "Une Paire de Devises est la cotation de la valeur relative d'une devise par rapport à une autre (ex: EUR/USD)."
        concept_list = ["Devise de base vs Cotation", "Corrélation entre paires", "Volatilité spécifique"]
        steps = ["Choisir une paire majeure (EURUSD)", "Vérifier le spread", "Analyser la session active"]
        mistakes = ["Trader des paires exotiques (spread élevé)", "Ignorer les heures d'ouverture"]
        
    elif "forex" in title_lower:
        definition = "Le FOREX (Foreign Exchange) est le marché des changes, le plus liquide au monde avec plus de 6000 milliards de dollars échangés par jour."
        
    elif "bougies" in title_lower or "candlestick" in title_lower:
        definition = "Les Bougies Japonaises (Candlesticks) racontent l'histoire du combat entre acheteurs et vendeurs sur une période donnée."
        steps = ["Identifier le corps (body)", "Analyser les mèches (wicks)", "Comparer la clôture par rapport à l'ouverture"]
        mistakes = ["Trader une bougie hors zone", "Ignorer la taille relative des bougies"]
        checklist = ["Bougie clôturée ?", "Rejet visible ?", "Volume cohérent ?"]
        
    elif "support" in title_lower or "zones" in title_lower:
        definition = "Les Supports et Résistances sont des zones de prix où le marché a historiquement réagi, inversant ou freinant une tendance."
        concept_list = ["Ancienne résistance devient support", "Chiffres ronds (psychologiques)", "Zones d'offre et de demande"]
        steps = ["Tracer les sommets/creux majeurs", "Étendre les lignes vers le futur", "Observer la réaction du prix au contact"]
        
    elif "trend" in title_lower or "tendance" in title_lower:
        definition = "La Ligne de Tendance est un outil visuel connectant des points bas de plus en plus hauts (tendance haussière) ou des sommets de plus en plus bas."
        steps = ["Relier au moins 2 points", "Le 3ème point confirme la tendance", "Trader le rebond ou la cassure"]

    elif "pib" in title_lower or "inflation" in title_lower or "news" in title_lower:
        definition = "L'Analyse Fondamentale étudie les forces économiques (PIB, Inflation, Emploi) qui font bouger les devises sur le long terme."
        concept_list = ["Taux d'intérêt", "Politique des Banques Centrales", "Sentiment de risque"]
        example = "Si le PIB US est meilleur que prévu, le Dollar (USD) a tendance à s'apprécier car l'économie est forte, attirant les capitaux."

    elif "risk" in title_lower or "gestion" in title_lower:
        definition = "Le Money Management est l'art de préserver son capital pour survivre aux séries de pertes inévitables."
        concept_list = ["Règle du 1%", "Risk of Ruin (Risque de ruine)", "Ratio Risque/Récompense"]
        mistakes = ["Martingale (doubler après perte)", "Déplacer son Stop Loss", "Over-leveraging"]
        checklist = ["Stop Loss est-il placé ?", "Taille de lot calculée ?", "Perte max < 1% ?"]

    elif "psycholog" in title_lower:
        definition = "La Psychologie du Trading représente 80% de la réussite. C'est la capacité à gérer ses émotions (peur, avidité) face à l'incertitude."
        concept_list = ["FOMO (Fear of Missing Out)", "Biais de confirmation", "Discipline et Routine"]
        
    elif "smc" in title_lower or "smart money" in title_lower or "order" in title_lower:
        definition = "Les Smart Money Concepts (SMC) cherchent à identifier les traces des institutions (Banques, Fonds) sur le graphique pour trader dans leur sens."
        concept_list = ["Liquidity Grabs", "Imbalances (FVG)", "Order Blocks"]
    
    return {
        "definition": definition,
        "why": why_important,
        "concepts": concept_list,
        "steps": steps,
        "example": example,
        "mistakes": mistakes,
        "checklist": checklist
    }

def format_lesson_html(title, level):
    """
    Assembles the fully distinct HTML structure.
    """
    data = get_base_content(title)
    
    # Generate List Items HTML
    li_concepts = "".join([f"<li class='mb-2'>🔹 <strong style='color:white'>{c}</strong></li>" for c in data['concepts']])
    li_steps = "".join([f"<li class='mb-2'><span style='{STYLE_GREEN}'>Step {i+1}:</span> {s}</li>" for i,s in enumerate(data['steps'])])
    li_mistakes = "".join([f"<li class='mb-2'>❌ {m}</li>" for m in data['mistakes']])
    li_checklist = "".join([f"<li class='mb-2'>✅ {c}</li>" for c in data['checklist']])

    html = f"""
    <div class="lesson-container text-gray-200">
        
        <!-- SECTION 1: DEFINITION -->
        <div style="{BOX_BLUE}">
            <h3 style="{STYLE_BLUE}; margin-top:0; margin-bottom:1rem; font-size: 1.25rem;">🔵 1. Définition & Objectif</h3>
            <p style="margin-bottom: 1rem;">
                <strong style="{STYLE_BLUE}">Définition :</strong> {data['definition']}
            </p>
            <p style="font-style:italic; opacity: 0.9;">
                "{data['why']}"
            </p>
        </div>

        <!-- SECTION 2: CONCEPTS -->
        <div class="mb-10">
            <h3 style="{STYLE_YELLOW}; font-size: 1.5rem; margin-bottom: 1rem;">🟡 2. Concepts Clés à Comprendre</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {li_concepts}
            </ul>
        </div>

        <hr style="border-color: #333; margin: 2rem 0;">

        <!-- SECTION 3: METHODOLOGY -->
        <div class="mb-10">
            <h3 style="{STYLE_GREEN}; font-size: 1.5rem; margin-bottom: 1rem;">🟢 3. Méthodologie Étape par Étape</h3>
            <p class="mb-4">Pour appliquer {title}, suivez ce processus rigoureux :</p>
            <ul style="list-style-type: none; padding-left: 0;">
                {li_steps}
            </ul>
        </div>

        <!-- SECTION 4: EXAMPLE -->
        <div class="mb-10 p-6 bg-gray-800 rounded-lg">
            <h4 style="color: white; margin-top:0;">🔎 4. Exemple Concret (Scénario)</h4>
            <p style="margin-top: 0.5rem; line-height: 1.6;">
                {data['example']}
            </p>
        </div>

        <!-- SECTION 5: MISTAKES -->
        <div style="{BOX_RED}">
            <h3 style="{STYLE_RED}; margin-top:0; margin-bottom:1rem;">🔴 5. Erreurs Fréquentes</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {li_mistakes}
            </ul>
        </div>

        <!-- SECTION 6: CHECKLIST -->
        <div style="{BOX_GREEN}">
            <h3 style="{STYLE_GREEN}; margin-top:0; margin-bottom:1rem;">🟢 6. Checklist de Validation</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {li_checklist}
            </ul>
        </div>

        <!-- SECTION 7: SUMMARY -->
        <div style="{BOX_YELLOW}">
            <h3 style="color: #f59e0b; margin-top:0; margin-bottom:0.5rem; font-weight: bold;">🟡 7. À Retenir Absolument</h3>
            <p>
                Maîtriser <strong>{title}</strong> prend du temps. Ne brûlez pas les étapes. 
                Revenez sur cette leçon chaque fois que vous avez un doute en temps réel.
            </p>
        </div>

    </div>
    """
    return html

def apply_styles():
    with app.app_context():
        print("🎨 Starting Visual Upgrade for ALL Academy Lessons...")
        
        lessons = Lesson.query.all()
        count = 0
        
        for lesson in lessons:
            # We assume Course Level helps, but title is main driver
            new_content = format_lesson_html(lesson.title, "Pro")
            
            # Update BASE Lesson
            lesson.content = new_content
            
            # Update Translations (Safety)
            translations = LessonTranslation.query.filter_by(lesson_id=lesson.id).all()
            for t in translations:
                t.content = new_content
            
            count += 1
            if count % 5 == 0:
                print(f"   ✨ Styled {count} lessons... ({lesson.title})")

        db.session.commit()
        print(f"✅ Success! {count} lessons have been visually re-mastered.")

if __name__ == "__main__":
    apply_styles()
