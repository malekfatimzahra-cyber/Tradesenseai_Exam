# ================================================
# DIAGNOSTIC COMPLET - PERSISTANCE UTILISATEUR
# ================================================

import sys
import os
sys.path.append(os.getcwd())

from flask import Flask
from config import get_config
from models import db, User, Account, UserChallenge, Transaction
from sqlalchemy import text

def diagnostic_complet():
    config_obj = get_config('development')
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    
    with app.app_context():
        print("\n" + "="*60)
        print("DIAGNOSTIC: PERSISTANCE DES DONNÉES UTILISATEUR")
        print("="*60)
        
        # 1. Vérifier la connexion
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ Connexion MySQL: OK")
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return
        
        # 2. Compter les utilisateurs
        total_users = User.query.count()
        print(f"\n📊 Total utilisateurs dans la base: {total_users}")
        
        # 3. Lister les 10 derniers utilisateurs
        recent_users = User.query.order_by(User.id.desc()).limit(10).all()
        print(f"\n👥 Derniers utilisateurs:")
        for u in recent_users:
            print(f"\n  ID: {u.id} | Email: {u.email} | Créé le: {u.created_at}")
            
            # Compter les challenges
            challenges_count = UserChallenge.query.filter_by(user_id=u.id).count()
            accounts_count = Account.query.filter_by(user_id=u.id).count()
            payments_count = Transaction.query.filter_by(user_id=u.id).count()
            
            print(f"    → Challenges (UserChallenge): {challenges_count}")
            print(f"    → Accounts (Trading): {accounts_count}")
            print(f"    → Paiements: {payments_count}")
            
            # Détails des challenges
            if challenges_count > 0:
                challenges = UserChallenge.query.filter_by(user_id=u.id).all()
                for c in challenges:
                    print(f"       - Challenge: {c.plan_name} | Status: {c.status} | {c.created_at}")
            
            # Détails des comptes
            if accounts_count > 0:
                accounts = Account.query.filter_by(user_id=u.id).all()
                for a in accounts:
                    print(f"       - Account: {a.plan_name} | Balance: {a.current_balance} | Status: {a.status.value}")
        
        # 4. Chercher l'utilisateur "karim@trade.ma" spécifiquement
        print("\n" + "="*60)
        print("RECHERCHE: karim@trade.ma")
        print("="*60)
        karim = User.query.filter_by(email='karim@trade.ma').first()
        if karim:
            print(f"✅ Trouvé: ID={karim.id} | Email={karim.email}")
            
            challenges = UserChallenge.query.filter_by(user_id=karim.id).all()
            accounts = Account.query.filter_by(user_id=karim.id).all()
            payments = Transaction.query.filter_by(user_id=karim.id).all()
            
            print(f"\n📊 Données associées:")
            print(f"  - Challenges actifs: {len([c for c in challenges if c.status == 'active'])}")
            print(f"  - Total challenges: {len(challenges)}")
            print(f"  - Comptes trading: {len(accounts)}")
            print(f"  - Paiements: {len(payments)}")
            
            print(f"\n📋 Détails des Challenges:")
            for c in challenges:
                print(f"  → Plan: {c.plan_name} | Status: {c.status} | Méthode: {c.payment_method} | {c.created_at}")
            
            print(f"\n💼 Détails des Accounts:")
            for a in accounts:
                print(f"  → Plan: {a.plan_name} | Balance: {a.current_balance}/{a.initial_balance} | Status: {a.status.value}")
            
            print(f"\n💳 Détails des Paiements:")
            for p in payments:
                print(f"  → Montant: {p.amount} {p.currency} | Méthode: {p.payment_method.value} | Status: {p.status.value}")
        else:
            print("❌ Utilisateur 'karim@trade.ma' NON TROUVÉ dans la base!")
        
        # 5. Vérifier la configuration de seed
        print("\n" + "="*60)
        print("VÉRIFICATION: Auto-seed au démarrage")
        print("="*60)
        print("⚠️  Attention: Le fichier __init__.py appelle seed_initial_data() au démarrage")
        print("    Cela ne devrait PAS supprimer les données existantes")
        print("    Vérifier que seed_initial_data() utilise 'filter_by().first()' avant INSERT")

if __name__ == "__main__":
    diagnostic_complet()
