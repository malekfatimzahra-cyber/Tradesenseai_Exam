"""
Fix leaderboard - Remove invalid entries and rebuild from real users
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Account, Trade, Leaderboard, ChallengeStatus, TradeStatus
from datetime import datetime
import json
import random

COUNTRIES = ["MA", "FR", "US", "UK", "DE", "ES", "AE", "SA", "EG", "TN"]

def fix_leaderboard():
    with app.app_context():
        print("\n" + "="*60)
        print("🔧 FIXING LEADERBOARD - Removing invalid entries")
        print("="*60)
        
        # Step 1: Find and remove entries with invalid user_ids
        all_entries = Leaderboard.query.all()
        invalid_entries = []
        valid_user_ids = set([u.id for u in User.query.all()])
        
        print(f"\n📊 Current state:")
        print(f"   Total leaderboard entries: {len(all_entries)}")
        print(f"   Valid user IDs in database: {len(valid_user_ids)}")
        
        for entry in all_entries:
            if entry.user_id not in valid_user_ids:
                invalid_entries.append(entry)
                print(f"   ❌ Invalid: {entry.username} (user_id={entry.user_id})")
        
        # Delete invalid entries
        if invalid_entries:
            print(f"\n🗑️  Deleting {len(invalid_entries)} invalid entries...")
            for entry in invalid_entries:
                db.session.delete(entry)
            db.session.commit()
            print("   ✅ Invalid entries deleted")
        else:
            print("\n✅ No invalid entries found")
        
        # Step 2: Clear and rebuild leaderboard from scratch
        print("\n🔄 Rebuilding leaderboard from real users...")
        
        # Clear all
        Leaderboard.query.delete()
        db.session.commit()
        
        # Get all accounts with their trade stats
        accounts = Account.query.filter(
            Account.status.in_([
                ChallengeStatus.ACTIVE, 
                ChallengeStatus.PASSED, 
                ChallengeStatus.FUNDED
            ])
        ).all()
        
        print(f"   Found {len(accounts)} eligible accounts")
        
        candidates = []
        
        for account in accounts:
            user = User.query.get(account.user_id)
            if not user:
                print(f"   ⚠️ Skipping account {account.id} - no user found")
                continue
            
            # Calculate from trades
            trades = Trade.query.filter_by(
                account_id=account.id, 
                status=TradeStatus.CLOSED
            ).all()
            
            if not trades:
                continue
            
            total_pnl = sum(t.pnl or 0 for t in trades)
            wins = sum(1 for t in trades if t.pnl and t.pnl > 0)
            win_rate = (wins / len(trades) * 100) if trades else 0
            roi = (total_pnl / account.initial_balance * 100) if account.initial_balance > 0 else 0
            
            # Generate badges
            badges = []
            if total_pnl > 1000:
                badges.append("profit_hunter")
            if win_rate > 60:
                badges.append("consistent")
            if len(trades) > 50:
                badges.append("active_trader")
            if account.status == ChallengeStatus.FUNDED:
                badges.append("funded")
            if roi > 10:
                badges.append("high_roi")
            
            # Generate sparkline
            equity_curve = [account.initial_balance]
            for i in range(1, 21):
                progress = i / 20
                expected = account.initial_balance + (total_pnl * progress)
                noise = random.uniform(-abs(total_pnl) * 0.05, abs(total_pnl) * 0.05)
                value = max(account.initial_balance * 0.9, expected + noise)
                equity_curve.append(round(value, 2))
            equity_curve[-1] = account.equity
            
            candidates.append({
                'user_id': user.id,
                'account_id': account.id,
                'username': user.username or user.full_name,
                'full_name': user.full_name,
                'profit': round(total_pnl, 2),
                'roi': round(roi, 2),
                'win_rate': round(win_rate, 2),
                'funded': account.initial_balance,
                'country': random.choice(COUNTRIES),
                'badges': badges,
                'equity_curve': equity_curve,
                'trades_count': len(trades)
            })
        
        # Sort by profit and assign ranks
        candidates.sort(key=lambda x: x['profit'], reverse=True)
        
        print(f"   Qualified candidates: {len(candidates)}")
        print("\n🏆 TOP 10 TRADERS (from real data):")
        print("-" * 60)
        
        for i, c in enumerate(candidates[:25]):  # Store top 25
            entry = Leaderboard(
                user_id=c['user_id'],
                account_id=c['account_id'],
                username=c['username'],
                country=c['country'],
                avatar_url=f"https://ui-avatars.com/api/?name={c['full_name']}&background=random",
                profit=c['profit'],
                roi=c['roi'],
                win_rate=c['win_rate'],
                funded_amount=c['funded'],
                consistency_score=min(100, c['win_rate'] + (c['trades_count'] / 2)),
                risk_score=max(0, 100 - abs(c['roi'] / 2)),
                ranking=i + 1,
                period='ALL_TIME',
                badges=json.dumps(c['badges']),
                equity_curve=json.dumps(c['equity_curve']),
                is_visible=True
            )
            db.session.add(entry)
            
            if i < 10:
                print(f"   #{i+1}: {c['username']} - ${c['profit']:+,.2f} ({c['roi']:+.1f}% ROI)")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ LEADERBOARD FIXED!")
        print(f"   Created {min(len(candidates), 25)} entries from real users")
        print("="*60 + "\n")


if __name__ == '__main__':
    fix_leaderboard()
