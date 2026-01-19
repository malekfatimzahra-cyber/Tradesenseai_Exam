import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.app import app
from backend.models import db, ChallengePlan

def fix_plans():
    with app.app_context():
        print("Checking Plans...")
        plans = [
             { 'id': 'starter', 'name': 'Starter Challenge', 'capital': 5000, 'profit_target': 500, 'max_drawdown': 500, 'daily_loss_limit': 250, 'price': 200, 'currency': 'MAD' },
             { 'id': 'pro', 'name': 'Professional Pro', 'capital': 25000, 'profit_target': 2500, 'max_drawdown': 2500, 'daily_loss_limit': 1250, 'price': 500, 'currency': 'MAD' },
             { 'id': 'elite', 'name': 'Elite Institutional', 'capital': 100000, 'profit_target': 10000, 'max_drawdown': 10000, 'daily_loss_limit': 5000, 'price': 1000, 'currency': 'MAD' },
        ]
        
        for p in plans:
            existing = ChallengePlan.query.get(p['id'])
            if not existing:
                new_plan = ChallengePlan(**p, is_active=True)
                db.session.add(new_plan)
                print(f"Created Plan: {p['name']}")
            else:
                print(f"Plan exists: {p['name']}")
        
        db.session.commit()
        print("✅ Plans synchronization complete.")

if __name__ == "__main__":
    fix_plans()
