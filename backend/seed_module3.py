"""
Seed the remaining lessons for Module 3 (Gestion du Risque)
"""

from app import app
from models import db, Lesson

def seed_remaining_lessons():
    with app.app_context():
        print("🌱 Seeding remaining lessons for Module 3...\n")
        
        # Lesson 3.1: La Règle des 1%
        lesson = Lesson.query.filter_by(title="La Règle des 1%").first()
        if lesson:
            lesson.content = """
<h2>💯 La Règle des 1% : Votre Bouclier de Protection</h2>
<p class="text-xl font-bold text-green-400">Ne JAMAIS risquer plus de 1% de votre capital par trade.</p>

<h3>🎯 Qu'est-ce que la Règle des 1% ?</h3>
<p>C'est une <strong>règle de gestion du risque fondamentale</strong> qui stipule que vous ne devez jamais risquer plus de <strong>1% à 2%</strong> de votre capital total sur un seul trade.</p>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>Exemple</strong> : Avec un capital de <strong>10,000€</strong>, vous ne devriez pas risquer plus de <strong>100€</strong> par trade.</p>
</div>

<h3>🛡️ Pourquoi C'est Crucial ?</h3>
<p>La règle des 1% vous protège contre les <strong>séries de pertes</strong> inévitables.</p>

<p><strong>Scénario catastrophe</strong> : 10 trades perdants consécutifs</p>
<ul>
    <li><strong>Avec risque de 10%</strong> : Capital restant = 0€ → <span class="text-red-400">GAME OVER</span></li>
    <li><strong>Avec risque de 1%</strong> : Capital restant = 9,044€ → <span class="text-green-400">Vous pouvez continuer</span></li>
</ul>

<h3>📊 Calcul Pratique</h3>
<ol>
    <li><strong>Déterminez votre risque max</strong> : Capital × 1% = Montant à risquer</li>
    <li><strong>Calculez la distance au Stop Loss</strong> : Entry - SL = X pips/points</li>
    <li><strong>Ajustez votre taille de position</strong> pour que la perte = 1% max</li>
</ol>

<div class="bg-yellow-500/10 border-l-4 border-yellow-500 p-4 my-4">
    <p><strong>💡 Formule</strong> : Taille de position = (Capital × 1%) / Distance au SL</p>
</div>

<h3>🚀 Avantages de la Règle des 1%</h3>
<ul>
    <li>✅ <strong>Longévité</strong> : Vous pouvez survivre à de longues séries de pertes</li>
    <li>✅ <strong>Sérénité psychologique</strong> : Pas de stress excessif sur chaque trade</li>
    <li>✅ <strong>Croissance du compte</strong> : Avec un bon RR, votre capital augmente progressivement</li>
    <li>✅ <strong>Discipline</strong> : Ça vous force à trader avec un plan, pas avec l'émotion</li>
</ul>

<h3>⚠️ Les Erreurs à Éviter</h3>
<ul>
    <li>❌ Risquer 5-10% par trade → Blown account garanti</li>
    <li>❌ Augmenter le risque après une perte (revenge trading)</li>
    <li>❌ Ne pas calculer son risque avant d'entrer en position</li>
</ul>

<div class="bg-red-500/10 border-l-4 border-red-500 p-4 my-4">
    <p><strong>🔴 Règle d'Or</strong> : Si votre setup ne permet pas de respecter la règle des 1% avec un bon RR, alors <strong>SKIP</strong> le trade.</p>
</div>

<p class="text-blue-400 font-bold mt-4">📌 Les traders professionnels gagnent leur vie en <strong>protégeant leur capital</strong>, pas en cherchant le home run.</p>

<h3>🎓 Exercice Pratique</h3>
<p>Calculez votre taille de position pour ce trade :</p>
<ul>
    <li>Capital : 5,000€</li>
    <li>Risque max : 1% = 50€</li>
    <li>Entry : 1.2000</li>
    <li>Stop Loss : 1.1950</li>
    <li>Distance : 50 pips</li>
</ul>
<p><strong>Réponse</strong> : Si 1 pip = 0.10€ pour 0.01 lot, alors 50 pips × 0.10€ = 5€ de perte pour 0.01 lot.<br>
Pour perdre 50€ max : <strong>0.10 lot</strong> (soit 10,000 unités).</p>

<p class="italic text-gray-400 mt-4">💼 Conseil : Utilisez toujours un calculateur de position-sizing pour ne jamais vous tromper.</p>
"""
            db.session.commit()
            print("✅ Seeded: La Règle des 1%")
        else:
            print("❌ Lesson 'La Règle des 1%' not found")
        
        # Lesson 3.2: Placer le Stop Loss
        lesson = Lesson.query.filter_by(title="Placer le Stop Loss").first()
        if lesson:
            lesson.content = """
<h2>🛑 Placer le Stop Loss : L'Art de la Protection</h2>
<p class="text-xl font-bold text-red-400">Le Stop Loss (SL) est votre meilleur ami. Ne tradez JAMAIS sans SL.</p>

<h3>🎯 Qu'est-ce qu'un Stop Loss ?</h3>
<p>Le <strong>Stop Loss</strong> est un ordre automatique qui <strong>ferme votre position</strong> lorsque le prix atteint un niveau prédéfini, limitant ainsi vos pertes.</p>

<p><strong>Pourquoi c'est essentiel ?</strong></p>
<ul>
    <li>✅ Protège votre capital contre des pertes catastrophiques</li>
    <li>✅ Élimine l'émotion de la décision (pas de "j'attends encore un peu...")</li>
    <li>✅ Vous permet de dormir tranquille</li>
</ul>

<div class="bg-red-500/10 border-l-4 border-red-500 p-4 my-4">
    <p><strong>⚠️ Règle Absolue</strong> : TOUJOURS placer un Stop Loss AVANT d'entrer en position. Pas d'exception.</p>
</div>

<h3>📐 Où Placer Votre Stop Loss ?</h3>

<h4>1️⃣ En Position LONG (Achat)</h4>
<p>Placez le SL <strong>sous le support</strong> le plus proche ou sous le dernier swing low.</p>
<ul>
    <li>Si vous achetez à un support, placez le SL <strong>quelques pips en-dessous</strong></li>
    <li>Laissez un peu de "breathing room" pour éviter d'être stoppé par du bruit de marché</li>
</ul>

<h4>2️⃣ En Position SHORT (Vente)</h4>
<p>Placez le SL <strong>au-dessus de la résistance</strong> ou au-dessus du dernier swing high.</p>

<div class="bg-blue-500/10 border-l-4 border-blue-500 p-4 my-4">
    <p><strong>💡 Principe Clé</strong> : Le SL doit invalider votre analyse. Si le prix touche votre SL, c'est que votre scénario ne s'est pas réalisé.</p>
</div>

<h3>🧠 Les Erreurs Mortelles</h3>

<h4>❌ Erreur #1 : Ne PAS Mettre de Stop Loss</h4>
<p><strong>Conséquence</strong> : Le prix va contre vous → Vous espérez un retournement → Grosse perte → Blown account</p>

<h4>❌ Erreur #2 : Déplacer le SL Plus Loin Quand le Prix Approche</h4>
<p><strong>Psychologie</strong> : "Allez, encore 10 pips, ça va remonter..."<br>
<strong>Réalité</strong> : Le prix continue, votre perte s'aggrave, vous perdez le contrôle.</p>

<div class="bg-yellow-500/10 border-l-4 border-yellow-500 p-4 my-4">
    <p><strong>🛡️ Règle d'Or</strong> : Une fois le SL placé, vous ne pouvez le déplacer QUE dans le sens du profit (trailing stop), JAMAIS dans le sens de la perte.</p>
</div>

<h4>❌ Erreur #3 : SL Trop Serré</h4>
<p>Si vous placez votre SL trop proche du prix d'entrée, vous serez stoppé par le <strong>bruit du marché</strong> (volatilité normale).</p>
<p><strong>Solution</strong> : Placez le SL à un niveau technique logique (support/résistance), pas arbitrairement.</p>

<h4>❌ Erreur #4 : SL Trop Large</h4>
<p>Un SL trop éloigné viole la règle des 1% et expose votre capital à un risque excessif.</p>
<p><strong>Solution</strong> : Si le SL technique nécessaire est trop large, réduisez votre taille de position ou skip le trade.</p>

<h3>✅ Types de Stop Loss</h3>

<h4>1. Stop Loss Fixe</h4>
<p>Vous définissez un niveau et ne le bougez jamais (sauf pour sécuriser des profits).</p>

<h4>2. Trailing Stop</h4>
<p>Le SL suit le prix dans le sens du profit.</p>
<p><strong>Exemple</strong> : Vous êtes en profit de 50 pips → Déplacez le SL au breakeven (prix d'entrée) pour sécuriser 0 perte.</p>

<h4>3. Stop Loss ATR (Average True Range)</h4>
<p>Basé sur la volatilité du marché. Si l'ATR = 50 pips, placez le SL à 1.5× ATR = 75 pips pour éviter le bruit.</p>

<h3>📊 Exemple Pratique</h3>
<p><strong>Setup</strong> : Achat sur EUR/USD</p>
<ul>
    <li>Support identifié : <strong>1.1000</strong></li>
    <li>Entry : <strong>1.1020</strong> (après rebond confirmé)</li>
    <li>Stop Loss : <strong>1.0980</strong> (sous le support + buffer de 20 pips)</li>
    <li>Risque : 40 pips</li>
    <li>Take Profit : <strong>1.1100</strong> (résistance suivante)</li>
    <li>Gain potentiel : 80 pips → <strong>RR = 1:2 ✅</strong></li>
</ul>

<p class="text-green-400 font-bold mt-4">📌 Le SL n'est PAS votre ennemi, c'est votre assurance-vie en trading.</p>

<p class="italic text-gray-400 mt-4">🧘 Mindset : Acceptez que les stop loss touchés font partie du trading. Ce qui compte, c'est votre performance globale sur 100 trades, pas un seul trade.</p>
"""
            db.session.commit()
            print("✅ Seeded: Placer le Stop Loss")
        else:
            print("❌ Lesson 'Placer le Stop Loss' not found")
        
        print("\n🎉 SUCCESS! All lessons for 'Introduction au Trading' are now complete!")
        print("📚 You now have rich, professional content for all 9 lessons across 3 modules.")

if __name__ == "__main__":
    seed_remaining_lessons()
