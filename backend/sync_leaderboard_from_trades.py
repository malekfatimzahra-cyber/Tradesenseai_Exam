"""
TRADESENSE AI - LEADERBOARD SYNC FROM TRADES
=============================================
This script recalculates the leaderboard from real trade data.
Run this periodically (e.g., via cron) or after major data changes.

Usage: python sync_leaderboard_from_trades.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Account, Trade, Leaderboard, ChallengeStatus, TradeStatus
from datetime import datetime
import json
import random


# Countries for leaderboard diversity
COUNTRIES = ["MA", "FR", "US", "UK", "DE", "ES", "AE", "SA", "EG", "TN"]


def calculate_account_stats(account_id):
    """Calculate win rate, profit, and other stats from trades."""
    trades = Trade.query.filter_by(
        account_id=account_id, 
        status=TradeStatus.CLOSED
    ).all()
    
    if not trades:
        return {
            'total_profit': 0,
            'win_rate': 0,
            'trades_count': 0,
            'wins': 0,
            'losses': 0
        }
    
    wins = sum(1 for t in trades if t.pnl and t.pnl > 0)
    losses = sum(1 for t in trades if t.pnl and t.pnl <= 0)
    total_profit = sum(t.pnl or 0 for t in trades)
    
    return {
        'total_profit': total_profit,
        'win_rate': (wins / len(trades) * 100) if trades else 0,
        'trades_count': len(trades),
        'wins': wins,
        'losses': losses
    }


def generate_equity_curve(initial_balance, final_equity, num_points=20):
    """Generate a realistic equity curve for sparkline visualization."""
    curve = [initial_balance]
    total_change = final_equity - initial_balance
    
    for i in range(1, num_points):
        progress = i / num_points
        expected = initial_balance + (total_change * progress)
        noise = random.uniform(-abs(total_change) * 0.1, abs(total_change) * 0.1)
        value = max(initial_balance * 0.85, expected + noise)
        curve.append(round(value, 2))
    
    curve.append(round(final_equity, 2))
    return curve


def sync_leaderboard(period='ALL_TIME'):
    """Sync leaderboard from real trade data."""
    
    with app.app_context():
        print("\n" + "="*60)
        print(f"📊 LEADERBOARD SYNC FROM TRADES ({period})")
        print("="*60)
        
        # Clear existing leaderboard for this period
        deleted = Leaderboard.query.filter_by(period=period).delete()
        db.session.commit()
        print(f"\n🗑️  Cleared {deleted} existing entries for period: {period}")
        
        # Get all eligible accounts
        accounts = Account.query.filter(
            Account.status.in_([
                ChallengeStatus.ACTIVE, 
                ChallengeStatus.PASSED, 
                ChallengeStatus.FUNDED
            ])
        ).all()
        
        print(f"📋 Found {len(accounts)} eligible accounts")
        
        candidates = []
        
        for account in accounts:
            stats = calculate_account_stats(account.id)
            user = User.query.get(account.user_id)
            
            if not user:
                continue
            
            profit = stats['total_profit']
            
            # Skip if lost more than 50% (exclude from leaderboard)
            if profit <= -account.initial_balance * 0.5:
                continue
            
            roi = (profit / account.initial_balance * 100) if account.initial_balance > 0 else 0
            
            # Generate equity curve
            equity_curve = generate_equity_curve(account.initial_balance, account.equity)
            
            # Generate badges based on performance
            badges = []
            if profit > 1000:
                badges.append("profit_hunter")
            if stats['win_rate'] > 60:
                badges.append("consistent")
            if stats['trades_count'] > 50:
                badges.append("active_trader")
            if account.status == ChallengeStatus.FUNDED:
                badges.append("funded")
            if roi > 10:
                badges.append("high_roi")
            if stats['wins'] > 30:
                badges.append("streak_master")
            
            candidates.append({
                'user_id': user.id,
                'account_id': account.id,
                'username': user.username,
                'profit': profit,
                'roi': roi,
                'win_rate': stats['win_rate'],
                'funded': account.initial_balance,
                'avatar': f"https://ui-avatars.com/api/?name={user.full_name}&background=random",
                'country': random.choice(COUNTRIES),
                'badges': badges,
                'equity_curve': equity_curve,
                'consistency_score': min(100, stats['win_rate'] + (stats['trades_count'] / 2)),
                'risk_score': max(0, 100 - abs(roi / 2)),
                'trades_count': stats['trades_count']
            })
        
        # Sort by profit
        candidates.sort(key=lambda x: x['profit'], reverse=True)
        
        # Create leaderboard entries (Top 50)
        print(f"\n🏆 Creating leaderboard entries:")
        print("-" * 60)
        
        for i, c in enumerate(candidates[:50]):
            entry = Leaderboard(
                user_id=c['user_id'],
                account_id=c['account_id'],
                username=c['username'],
                country=c['country'],
                avatar_url=c['avatar'],
                profit=round(c['profit'], 2),
                roi=round(c['roi'], 2),
                win_rate=round(c['win_rate'], 2),
                funded_amount=c['funded'],
                consistency_score=round(c['consistency_score'], 2),
                risk_score=round(c['risk_score'], 2),
                ranking=i + 1,
                period=period,
                badges=json.dumps(c['badges']),
                equity_curve=json.dumps(c['equity_curve']),
                is_visible=True
            )
            db.session.add(entry)
            
            if i < 10:  # Show top 10
                print(f"  #{i+1}: {c['username']} - ${c['profit']:+,.2f} ({c['roi']:+.2f}% ROI) | {c['trades_count']} trades")
        
        db.session.commit()
        
        print(f"\n📊 Summary:")
        print(f"  - Processed: {len(accounts)} accounts")
        print(f"  - Qualified: {len(candidates)} candidates")
        print(f"  - Created: {len(candidates[:50])} leaderboard entries")
        print(f"  - Period: {period}")
        
        print("\n" + "="*60)
        print("✅ LEADERBOARD SYNC COMPLETE")
        print("="*60 + "\n")
        
        return len(candidates[:50])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Sync leaderboard from trades')
    parser.add_argument('--period', default='ALL_TIME', 
                       help='Period: ALL_TIME, MONTHLY, WEEKLY')
    args = parser.parse_args()
    
    sync_leaderboard(args.period)
