"""
Seed Course Content Script
This script populates the 'Introduction au Trading' course with rich, static HTML content.
Run: python backend/seed_course_content.py
"""

from app import app
from models import db, Lesson

def seed_content():
    with app.app_context():
        print("🌱 Starting content seeding for 'Introduction au Trading'...")
        
        # =====================================================
        # MODULE 1: LES BASES
        # =====================================================
        
        # Lesson 1.1: Qu'est-ce que le Trading ?
        lesson = Lesson.query.filter_by(title="Qu'est-ce que le Trading ?").first()
        if lesson:
            lesson.content = """
<h2>📈 Introduction au Trading</h2>
<p>Le <strong>trading</strong> est l'art d'acheter et de vendre des actifs financiers (actions, devises, cryptomonnaies) dans le but de réaliser un <strong>profit à court terme</strong>.</p>

<h3>🔹 Trading vs Investissement</h3>
<ul>
    <li><strong>Trading</strong> : Opérations fréquentes sur des périodes courtes (minutes, heures, jours). L'objectif est de profiter de la <strong>volatilité</strong> des prix.</li>
    <li><strong>Investissement</strong> : Achats à long terme (mois, années) en pariant sur la croissance future d'une entreprise ou d'un actif.</li>
</ul>

<h3>🎯 L'Objectif du Trader</h3>
<p>Le trader cherche à <strong>acheter bas</strong> et <strong>vendre haut</strong> (ou vendre haut puis racheter bas en position Short).</p>
<p>Contrairement à l'investisseur, le trader ne s'intéresse pas à la valeur intrinsèque d'une entreprise, mais uniquement au <strong>mouvement du prix</strong>.</p>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>💡 Point Clé :</strong> Le trading nécessite discipline, gestion du risque et psychologie solide. Ce n'est PAS un casino.</p>
</div>

<h3>📊 Types de Trading</h3>
<ul>
    <li><strong>Scalping</strong> : Trades ultra-rapides (secondes/minutes)</li>
    <li><strong>Day Trading</strong> : Positions ouvertes et fermées dans la même journée</li>
    <li><strong>Swing Trading</strong> : Positions tenues plusieurs jours à semaines</li>
    <li><strong>Position Trading</strong> : Approche long-terme (moins fréquent)</li>
</ul>

<p class="text-gray-400 italic mt-4">Dans ce cours, nous nous concentrons sur le <strong>Day Trading</strong> et le <strong>Swing Trading</strong>.</p>
"""
            db.session.commit()
            print("✅ Seeded: Qu'est-ce que le Trading ?")
        
        # Lesson 1.2: Lire un Graphique
        lesson = Lesson.query.filter_by(title="Lire un Graphique").first()
        if lesson:
            lesson.content = """
<h2>📊 Décrypter un Graphique de Trading</h2>
<p>Le graphique est l'outil principal du trader. Il affiche l'évolution du <strong>prix</strong> d'un actif dans le temps.</p>

<h3>🕯️ Les Bougies Japonaises (Candlesticks)</h3>
<p>Chaque bougie représente une période de temps (1 minute, 1 heure, 1 jour...) et contient <strong>4 informations essentielles</strong> :</p>

<ul>
    <li><strong>Open (O)</strong> : Prix d'ouverture de la période</li>
    <li><strong>High (H)</strong> : Prix le plus haut atteint</li>
    <li><strong>Low (L)</strong> : Prix le plus bas atteint</li>
    <li><strong>Close (C)</strong> : Prix de clôture de la période</li>
</ul>

<div class="bg-green-500/10 border-l-4 border-green-500 p-4 my-4">
    <p><strong>🟢 Bougie Verte (Haussière)</strong> : Close > Open → Les acheteurs dominent</p>
</div>

<div class="bg-red-500/10 border-l-4 border-red-500 p-4 my-4">
    <p><strong>🔴 Bougie Rouge (Baissière)</strong> : Close < Open → Les vendeurs dominent</p>
</div>

<h3>⏱️ Les Timeframes (Unités de Temps)</h3>
<p>Un timeframe détermine ce que représente chaque bougie :</p>
<ul>
    <li><strong>M1</strong> : 1 minute (scalping)</li>
    <li><strong>M15</strong> : 15 minutes (day trading)</li>
    <li><strong>H1</strong> : 1 heure (swing trading)</li>
    <li><strong>D1</strong> : 1 jour (analyse long-terme)</li>
</ul>

<h3>📦 Le Volume</h3>
<p>Le <strong>volume</strong> indique le nombre de transactions effectuées. Un mouvement de prix avec un <strong>volume élevé</strong> est plus fiable qu'un mouvement avec un volume faible (peu de conviction).</p>

<p class="text-yellow-400 font-bold mt-4">📌 Règle d'Or : Plus le timeframe est élevé, plus le signal est fiable.</p>
"""
            db.session.commit()
            print("✅ Seeded: Lire un Graphique")
        
        # Lesson 1.3: La terminologie essentielle
        lesson = Lesson.query.filter_by(title="La terminologie essentielle").first()
        if lesson:
            lesson.content = """
<h2>📚 Vocabulaire du Trader Professionnel</h2>
<p>Maîtriser le jargon est essentiel pour comprendre les analyses et communiquer avec d'autres traders.</p>

<h3>💰 Pip (Point in Percentage)</h3>
<p>Le <strong>Pip</strong> est la plus petite variation de prix sur le marché Forex.</p>
<p><strong>Exemple</strong> : EUR/USD passe de 1.1000 à 1.1001 → +1 pip</p>
<p>Sur la plupart des paires de devises, 1 pip = 0.0001</p>

<h3>📏 Spread</h3>
<p>Le <strong>Spread</strong> est la différence entre le prix d'achat (Ask) et le prix de vente (Bid).</p>
<p>C'est la commission invisible du broker. Plus le spread est faible, mieux c'est.</p>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>Exemple</strong> : EUR/USD - Bid: 1.1000 / Ask: 1.1002 → Spread = 2 pips</p>
</div>

<h3>📦 Lot</h3>
<p>Un <strong>Lot</strong> est l'unité de mesure de la taille d'une position en trading :</p>
<ul>
    <li><strong>1 Lot Standard</strong> = 100,000 unités de devise</li>
    <li><strong>1 Mini Lot</strong> = 10,000 unités</li>
    <li><strong>1 Micro Lot</strong> = 1,000 unités</li>
</ul>

<h3>⚡ Leverage (Effet de Levier)</h3>
<p>Le <strong>levier</strong> permet de contrôler une position importante avec un capital réduit.</p>
<p><strong>Levier 1:100</strong> → Avec 100€, vous contrôlez 10,000€</p>
<p class="text-red-400 font-bold">⚠️ ATTENTION : Le levier amplifie les gains MAIS AUSSI les pertes !</p>

<h3>🔼 Long vs 🔽 Short</h3>
<ul>
    <li><strong>Position LONG (Achat)</strong> : Vous pariez sur la <span class="text-green-400">HAUSSE</span> du prix</li>
    <li><strong>Position SHORT (Vente)</strong> : Vous pariez sur la <span class="text-red-400">BAISSE</span> du prix</li>
</ul>

<p class="italic text-gray-400 mt-4">📖 Astuce : Notez ces termes dans un glossaire personnel pour les mémoriser.</p>
"""
            db.session.commit()
            print("✅ Seeded: La terminologie essentielle")
        
        # =====================================================
        # MODULE 2: ANALYSE TECHNIQUE
        # =====================================================
        
        # Lesson 2.1: Support et Résistance
        lesson = Lesson.query.filter_by(title="Support et Résistance").first()
        if lesson:
            lesson.content = """
<h2>🧱 Support et Résistance : Les Fondations de l'Analyse</h2>
<p>Ce sont les concepts les PLUS importants en trading. Maîtrisez-les et vous aurez un avantage énorme.</p>

<h3>🟢 Support (Zone d'Achat)</h3>
<p>Un <strong>support</strong> est un niveau de prix où la <strong>demande est forte</strong>. Le prix a tendance à rebondir à la hausse en touchant cette zone.</p>
<p><em>Métaphore</em> : C'est comme un trampoline — le prix tombe, puis rebondit.</p>

<h3>🔴 Résistance (Zone de Vente)</h3>
<p>Une <strong>résistance</strong> est un niveau où l'<strong>offre est forte</strong>. Le prix a du mal à la franchir et redescend souvent.</p>
<p><em>Métaphore</em> : Un plafond solide que le prix ne peut pas traverser facilement.</p>

<h3>📐 Comment Tracer S/R ?</h3>
<ol>
    <li>Identifiez au moins <strong>2 touchés</strong> du prix sur une zone horizontale</li>
    <li>Plus il y a de touchés, plus le niveau est fort</li>
    <li>Tracez une ligne horizontale claire</li>
</ol>

<div class="bg-yellow-500/10 border-l-4 border-yellow-500 p-4 my-4">
    <p><strong>💡 Psychologie derrière S/R</strong> :</p>
    <p>Les traders se souviennent des niveaux historiques. Si EUR/USD a rebondi 3 fois à 1.1000, beaucoup placeront des ordres d'achat à ce niveau → auto-réalisation de la prédiction.</p>
</div>

<h3>💥 Rebond vs Cassure</h3>
<ul>
    <li><strong>Rebond</strong> : Le prix touche le support/résistance et repart dans l'autre sens (trade classique)</li>
    <li><strong>Cassure (Break)</strong> : Le prix franchit le niveau avec force → changement de tendance potentiel</li>
</ul>

<p class="text-green-400 font-bold mt-4">✅ Stratégie Pro : Attendez une CONFIRMATION (bougie de retournement) avant d'entrer en position au support/résistance.</p>
"""
            db.session.commit()
            print("✅ Seeded: Support et Résistance")
        
        # Lesson 2.2: La Tendance (Trend)
        lesson = Lesson.query.filter_by(title="La Tendance (Trend)").first()
        if lesson:
            lesson.content = """
<h2>📈 La Tendance est Votre Amie</h2>
<p class="text-xl font-bold text-blue-400">"The Trend is Your Friend" — Maxime #1 du Trading</p>
<p>Tradez TOUJOURS dans le sens de la tendance. Les traders qui vont contre la tendance perdent de l'argent.</p>

<h3>🟢 Tendance Haussière (Uptrend)</h3>
<p>Caractéristiques :</p>
<ul>
    <li><strong>Higher Highs (HH)</strong> : Chaque sommet est plus haut que le précédent</li>
    <li><strong>Higher Lows (HL)</strong> : Chaque creux est plus haut que le précédent</li>
</ul>
<p><strong>Action</strong> : Cherchez des opportunités d'ACHAT (Long) sur les pullbacks</p>

<h3>🔴 Tendance Baissière (Downtrend)</h3>
<p>Caractéristiques :</p>
<ul>
    <li><strong>Lower Lows (LL)</strong> : Chaque creux est plus bas</li>
    <li><strong>Lower Highs (LH)</strong> : Chaque sommet est plus bas</li>
</ul>
<p><strong>Action</strong> : Cherchez des opportunités de VENTE (Short) sur les rallyes</p>

<h3>➡️ Range (Consolidation)</h3>
<p>Le prix oscille entre un support et une résistance sans direction claire.</p>
<p><strong>Stratégie</strong> : Achetez au support, vendez à la résistance. OU attendez la cassure pour suivre le nouveau trend.</p>

<div class="bg-red-500/10 border-l-4 border-red-500 p-4 my-4">
    <p><strong>⚠️ Erreur Fatale</strong> : ACHETER en tendance baissière ou VENDRE en tendance haussière = suicide financier.</p>
</div>

<h3>🔄 Identifier un Renversement de Tendance</h3>
<p>Signes précurseurs :</p>
<ol>
    <li><strong>Cassure de structure</strong> : Un HL devient un LL en uptrend (ou inversement)</li>
    <li><strong>Divergence</strong> : Le prix monte mais l'indicateur (RSI) baisse</li>
    <li><strong>Volume décroissant</strong> : La tendance s'essouffle</li>
</ol>

<p class="text-yellow-400 font-bold mt-4">📌 Ne "call" JAMAIS un top ou un bottom. Attendez la CONFIRMATION du changement de structure.</p>
"""
            db.session.commit()
            print("✅ Seeded: La Tendance (Trend)")
        
        # Lesson 2.3: Indicateurs Classiques
        lesson = Lesson.query.filter_by(title="Indicateurs Classiques").first()
        if lesson:
            lesson.content = """
<h2>🛠️ Les Indicateurs Techniques Essentiels</h2>
<p>Les indicateurs sont des outils mathématiques qui vous aident à <strong>confirmer</strong> vos décisions. Ils ne sont JAMAIS utilisés seuls.</p>

<h3>📊 RSI (Relative Strength Index)</h3>
<p>Le RSI mesure la <strong>force</strong> d'une tendance sur une échelle de 0 à 100.</p>
<ul>
    <li><strong>RSI > 70</strong> : Zone de <span class="text-red-400">SURACHAT</span> → Possible retournement baissier</li>
    <li><strong>RSI < 30</strong> : Zone de <span class="text-green-400">SURVENTE</span> → Possible retournement haussier</li>
    <li><strong>RSI entre 40-60</strong> : Zone neutre</li>
</ul>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>💡 Stratégie Pro</strong> : En tendance haussière forte, le RSI peut rester > 70 longtemps. Ne vendez pas juste parce que "c'est surachat".</p>
</div>

<h3>📈 MACD (Moving Average Convergence Divergence)</h3>
<p>Le MACD montre la relation entre deux moyennes mobiles (12 et 26 périodes).</p>
<p><strong>Signaux</strong> :</p>
<ul>
    <li><strong>Croisement haussier</strong> : La ligne MACD croise au-dessus de la ligne de signal → Signal d'ACHAT</li>
    <li><strong>Croisement baissier</strong> : La ligne MACD croise en-dessous → Signal de VENTE</li>
    <li><strong>Divergence</strong> : Le prix monte mais le MACD baisse → Faiblesse de la tendance</li>
</ul>

<h3>📉 Moyennes Mobiles (MA)</h3>
<p>Une moyenne mobile lisse les fluctuations du prix pour révéler la tendance générale.</p>
<p><strong>Types</strong> :</p>
<ul>
    <li><strong>SMA (Simple)</strong> : Moyenne arithmétique simple</li>
    <li><strong>EMA (Exponentielle)</strong> : Donne plus de poids aux prix récents (plus réactive)</li>
</ul>

<p><strong>Utilisation</strong> :</p>
<ul>
    <li><strong>Prix au-dessus de la MA</strong> → Tendance haussière</li>
    <li><strong>Prix en-dessous de la MA</strong> → Tendance baissière</li>
    <li><strong>Croisement de 2 MA</strong> (ex: MA 50 croise MA 200) → Signal fort de changement de tendance</li>
</ul>

<div class="bg-yellow-500/10 border-l-4 border-yellow-500 p-4 my-4">
    <p><strong>⚠️ Avertissement</strong> : Les indicateurs sont des outils de <strong>confirmation</strong>, pas de prédiction. Ne basez JAMAIS une décision uniquement sur un indicateur.</p>
</div>

<p class="italic text-gray-400 mt-4">🎯 L'approche gagnante : Structure du marché (S/R, Tendance) PUIS Confirmation par indicateurs.</p>
"""
            db.session.commit()
            print("✅ Seeded: Indicateurs Classiques")
        
        # =====================================================
        # MODULE 3: GESTION DU RISQUE
        # =====================================================
        
        # Lesson 3.1: Le Ratio Risque/Récompense
        lesson = Lesson.query.filter_by(title="Le Ratio Risque/Récompense").first()
        if lesson:
            lesson.content = """
<h2>⚖️ Le Ratio Risque/Récompense (RR)</h2>
<p class="text-xl font-bold text-green-400">Si vous ne devez retenir QU'UNE chose de ce cours, c'est CECI.</p>

<h3>🎯 Qu'est-ce que le RR ?</h3>
<p>Le ratio RR compare le <strong>gain potentiel</strong> au <strong>risque pris</strong> sur un trade.</p>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>Formule</strong> : RR = (Take Profit - Entry) / (Entry - Stop Loss)</p>
</div>

<h3>📊 Exemple Concret</h3>
<p>Vous entrez à <strong>100€</strong> :</p>
<ul>
    <li>Stop Loss (SL) : <strong>95€</strong> → Risque = 5€</li>
    <li>Take Profit (TP) : <strong>110€</strong> → Gain = 10€</li>
    <li><strong>RR = 10/5 = 2</strong> → Ratio 1:2 ✅</li>
</ul>

<h3>✅ Pourquoi 1:2 est le MINIMUM ?</h3>
<p>Avec un RR de 1:2, vous êtes <strong>rentable à 40% de winrate</strong> :</p>
<p><strong>Simulation (10 trades)</strong> :</p>
<ul>
    <li>4 wins × 10€ = +40€</li>
    <li>6 losses × 5€ = -30€</li>
    <li><strong>Résultat net = +10€</strong> 🎉</li>
</ul>

<p>À l'inverse, avec un RR de 1:1, vous devez gagner 50%+ des trades juste pour break-even. Avec un RR de 1:0.5, vous êtes condamné à perdre.</p>

<div class="bg-red-500/10 border-l-4 border-red-500 p-4 my-4">
    <p><strong>⚠️ Règle d'Or</strong> : Ne prenez JAMAIS un trade avec un RR inférieur à 1:1.5. Idéalement, visez 1:2 ou 1:3.</p>
</div>

<h3>🛠️ Comment Calculer Votre RR ?</h3>
<ol>
    <li>Identifiez votre point d'entrée (support, résistance, etc.)</li>
    <li>Placez votre Stop Loss sous la structure (invalide votre analyse si touché)</li>
    <li>Identifiez votre Take Profit (prochain niveau de S/R)</li>
    <li>Calculez le ratio</li>
    <li><strong>Si RR < 1:2 → SKIP le trade</strong></li>
</ol>

<p class="text-yellow-400 font-bold mt-4">📌 La patience est une vertu. Attendez les setups avec un bon RR plutôt que de forcer des trades médiocres.</p>
"""
            db.session.commit()
            print("✅ Seeded: Le Ratio Risque/Récompense")
        
        # Lesson 3.2: La Psychologie
        lesson = Lesson.query.filter_by(title="La Psychologie").first()
        if lesson:
            lesson.content = """
<h2>🧠 La Psychologie : 80% du Trading</h2>
<p class="text-xl font-bold text-red-400">L'analyse technique ne représente que 20% du succès. Le reste, c'est VOUS.</p>

<h3>😱 FOMO (Fear Of Missing Out)</h3>
<p>Le FOMO est cette pulsion irrationnelle de <strong>rentrer dans un trade trop tard</strong> par peur de manquer une opportunité.</p>

<p><strong>Symptômes</strong> :</p>
<ul>
    <li>Vous voyez Bitcoin monter de 5% → "Je DOIS acheter maintenant !"</li>
    <li>Entrée précipitée sans analyse → Achat au TOP</li>
    <li>Le prix corrige immédiatement → Stop Loss touché</li>
</ul>

<div class="bg-yellow-500/10 border-l-4 border-yellow-500 p-4 my-4">
    <p><strong>🛡️ Solution</strong> : Ayez un PLAN de trading écrit. Si votre setup n'est pas respecté, ne tradez PAS. Le marché offre des opportunités TOUS LES JOURS.</p>
</div>

<h3>😡 Revenge Trading (Trading de Vengeance)</h3>
<p>Vous venez de perdre un trade → Vous êtes en colère → Vous ouvrez un nouveau trade immédiatement pour "récupérer" l'argent perdu.</p>

<p><strong>Résultat</strong> : Perte encore plus grosse → Spirale destructrice → Compte explosé 💥</p>

<p><strong>🛡️ Solution</strong> :</p>
<ol>
    <li>Acceptez que les pertes font partie du jeu</li>
    <li>Après 2 pertes consécutives, ARRÊTEZ de trader pour la journée</li>
    <li>Analysez vos erreurs à froid (journaling)</li>
    <li>Revenez demain avec un esprit clair</li>
</ol>

<h3>💪 La Discipline : La Compétence #1</h3>
<p>La discipline, c'est :</p>
<ul>
    <li>Respecter votre Stop Loss (TOUJOURS)</li>
    <li>Ne pas déplacer votre SL quand le trade va contre vous (= espérer)</li>
    <li>Prendre vos profits comme prévu (ne pas être gourmand)</li>
    <li>Ne trader QUE vos setups validés</li>
    <li>Respecter votre risque max par trade (1-2% du capital)</li>
</ul>

<div class="bg-green-500/10 border-l-4 border-green-500 p-4 my-4">
    <p><strong>✅ Citation du Day</strong> : "Les traders amateurs cherchent à avoir raison. Les pros cherchent à être profitables."</p>
</div>

<h3>📓 Le Journal de Trading</h3>
<p>Documentez CHAQUE trade :</p>
<ul>
    <li>Setup utilisé</li>
    <li>Raison de l'entrée</li>
    <li>Emotions ressenties</li>
    <li>Résultat (Win/Loss)</li>
    <li>Leçons apprises</li>
</ul>

<p class="text-blue-400 font-bold mt-4">🎯 Après 100 trades journalisés, vous verrez vos patterns d'erreurs et pourrez les corriger. C'est VOTRE avantage concurrentiel.</p>

<p class="italic text-gray-400 mt-6">🧘 Dernier conseil : Méditez 10 minutes avant de trader. Un esprit clair = Décisions rationnelles.</p>
"""
            db.session.commit()
            print("✅ Seeded: La Psychologie")
        
        db.session.commit()
        print("\n🎉 SUCCESS! All lessons for 'Introduction au Trading' have been seeded with rich content.")
        print("You can now safely navigate to the course and see professional, static content.")

if __name__ == "__main__":
    seed_content()
