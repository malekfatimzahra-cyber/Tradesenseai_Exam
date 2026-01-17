
import os
import sys
from datetime import datetime

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import db, User, Account, Leaderboard, ChallengeStatus

def sync_leaderboard():
    print("Syncing Leaderboard Table from Active Accounts...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. Clear existing leaderboard
        db.session.query(Leaderboard).delete()
        
        # 2. Get all accounts with positive profit
        # Logic: Profit = Equity - Initial Balance
        accounts = Account.query.filter(
            Account.status.in_([ChallengeStatus.ACTIVE, ChallengeStatus.PASSED, ChallengeStatus.FUNDED])
        ).all()
        
        candidates = []
        for acc in accounts:
            profit = acc.equity - acc.initial_balance
            if profit <= 0:
                continue
            
            roi = (profit / acc.initial_balance) * 100
            
            # Win Rate Calculation
            wins = 0
            total_trades = len(acc.trades)
            if total_trades > 0:
                wins = sum(1 for t in acc.trades if t.pnl > 0)
                win_rate = (wins / total_trades) * 100
            else:
                win_rate = 0.0
            
            # Country (Mock random or fixed for now since User model doesn't have it yet)
            # Use 'MA' for the Moroccan traders we seeded
            country = 'MA' 
            
            candidates.append({
                'user_id': acc.user_id,
                'username': acc.user.username,
                'profit': profit,
                'roi': roi,
                'win_rate': win_rate,
                'funded': acc.initial_balance,
                'country': country,
                'avatar': f"https://ui-avatars.com/api/?name={acc.user.full_name}&background=random"
            })
            
        # 3. Sort by Profit Desc
        candidates.sort(key=lambda x: x['profit'], reverse=True)
        
        # 4. Insert Top 10-20 into Leaderboard Table
        for i, c in enumerate(candidates[:20]): # Keep top 20
            entry = Leaderboard(
                user_id=c['user_id'],
                username=c['username'],
                country=c['country'],
                avatar_url=c['avatar'],
                profit=c['profit'],
                roi=c['roi'],
                win_rate=c['win_rate'],
                funded_amount=c['funded'],
                ranking=i + 1,
                period='ALL_TIME',
                is_visible=True
            )
            db.session.add(entry)
            print(f"Added Rank #{i+1}: {c['username']} (+{c['profit']})")
            
        db.session.commit()
        print("Leaderboard synced successfully.")

if __name__ == '__main__':
    sync_leaderboard()
