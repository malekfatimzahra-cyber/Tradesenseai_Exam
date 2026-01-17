
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Leaderboard

def verify_leaderboard():
    print("Verifying Leaderboard Table Data...")
    
    app = create_app('development')
    
    with app.app_context():
        entries = Leaderboard.query.order_by(Leaderboard.ranking.asc()).all()
        
        print(f"\nTotal Entries in Leaderboard Table: {len(entries)}\n")
        print("=" * 80)
        
        for entry in entries:
            print(f"Rank #{entry.ranking}: {entry.username}")
            print(f"  Country: {entry.country} | Profit: ${entry.profit:,.2f} | ROI: {entry.roi:.1f}%")
            print(f"  Win Rate: {entry.win_rate:.1f}% | Funded: ${entry.funded_amount:,.2f}")
            print(f"  Visible: {entry.is_visible} | Period: {entry.period}")
            print("-" * 80)
        
        print(f"\n✓ Leaderboard contains {len(entries)} traders saved in MySQL")

if __name__ == '__main__':
    verify_leaderboard()
