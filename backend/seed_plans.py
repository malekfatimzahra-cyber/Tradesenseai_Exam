import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.models import db, ChallengePlan

def seed_plans():
    with app.app_context():
        print("SEEDING Challenge Plans...")
        
        plans = [
             { 'id': 'starter', 'name': 'Starter Challenge', 'capital': 5000, 'profit_target': 500, 'max_drawdown': 500, 'daily_loss_limit': 250, 'price': 200, 'currency': 'MAD' },
             { 'id': 'pro', 'name': 'Professional Pro', 'capital': 25000, 'profit_target': 2500, 'max_drawdown': 2500, 'daily_loss_limit': 1250, 'price': 500, 'currency': 'MAD' },
             { 'id': 'elite', 'name': 'Elite Institutional', 'capital': 100000, 'profit_target': 10000, 'max_drawdown': 10000, 'daily_loss_limit': 5000, 'price': 1000, 'currency': 'MAD' },
        ]
        
        for p in plans:
            existing = ChallengePlan.query.get(p['id'])
            if not existing:
                new_plan = ChallengePlan(
                    id=p['id'],
                    name=p['name'],
                    capital=p['capital'],
                    profit_target=p['profit_target'],
                    max_drawdown=p['max_drawdown'],
                    daily_loss_limit=p['daily_loss_limit'],
                    price=p['price'],
                    currency=p['currency'],
                    is_active=True
                )
                db.session.add(new_plan)
                print(f"Created Plan: {p['name']}")
            else:
                # Update existing just in case
                existing.capital = p['capital']
                existing.profit_target = p['profit_target']
                existing.max_drawdown = p['max_drawdown']
                existing.daily_loss_limit = p['daily_loss_limit']
                existing.price = p['price']
                print(f"Updated Plan: {p['name']}")
        
        db.session.commit()
        print("✅ Plans Seeded Successfully!")

if __name__ == "__main__":
    seed_plans()
