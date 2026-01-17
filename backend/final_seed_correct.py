
import os
import sys
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add 'backend' to path
backend_dir = os.path.join(os.getcwd(), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from __init__ import create_app
from models import (
    db, User, Account, Trade, Transaction, Challenge, 
    Post, Comment, PostLike, FloorMessage, 
    UserBadge, UserXP, UserCourseProgress, UserLessonProgress, RiskAlert, 
    UserRole, ChallengeStatus, TradeStatus, TradeType
)

def safe_cleanup_and_seed():
    print("Starting SAFE Leaderboard RESET & SEED (Corrected)...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. FIND ALL 'USER' ROLE USERS (Target to delete)
        users_to_delete = User.query.filter(
            User.role == UserRole.USER,
            User.email.notin_(['karim@trade.ma', 'sara@admin.ma', 'superadmin@tradesense.ma'])
        ).all()
        
        print(f"Found {len(users_to_delete)} users to delete.")
        
        for u in users_to_delete:
            try:
                print(f"   Deleting user {u.username} (ID: {u.id})...")
                # Delete related data
                RiskAlert.query.filter_by(user_id=u.id).delete()
                UserLessonProgress.query.filter_by(user_id=u.id).delete()
                UserCourseProgress.query.filter_by(user_id=u.id).delete()
                UserXP.query.filter_by(user_id=u.id).delete()
                UserBadge.query.filter_by(user_id=u.id).delete()
                FloorMessage.query.filter_by(user_id=u.id).delete()
                PostLike.query.filter_by(user_id=u.id).delete()
                Comment.query.filter_by(user_id=u.id).delete()
                Post.query.filter_by(user_id=u.id).delete()
                
                # Financials
                accounts = Account.query.filter_by(user_id=u.id).all()
                for acc in accounts:
                    Transaction.query.filter_by(account_id=acc.id).delete()
                    Trade.query.filter_by(account_id=acc.id).delete()
                    db.session.delete(acc)
                
                Transaction.query.filter_by(user_id=u.id).delete()
                Trade.query.filter_by(user_id=u.id).delete()
                Challenge.query.filter_by(user_id=u.id).delete()
                
                db.session.delete(u)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                print(f"   ERROR deleting {u.username}: {e}")

        # 2. SEED TOP 10 ELITE TRADERS
        print("Seeding Top 10 Elite Traders...")
        
        top_traders = [
            {"rank": 1, "name": "Alex Momentum", "user": "alex_pro", "balance": 100000, "profit": 25450},
            {"rank": 2, "name": "Sarah Sniper", "user": "sarah_x", "balance": 100000, "profit": 21200},
            {"rank": 3, "name": "Mike Macro", "user": "mike_m", "balance": 100000, "profit": 18900},
            {"rank": 4, "name": "Emma Elliott", "user": "emma_e", "balance": 50000, "profit": 15600},
            {"rank": 5, "name": "David Day", "user": "david_d", "balance": 50000, "profit": 12400},
            {"rank": 6, "name": "Lucas Long", "user": "lucas_l", "balance": 50000, "profit": 9800},
            {"rank": 7, "name": "Julia Just", "user": "julia_j", "balance": 25000, "profit": 7500},
            {"rank": 8, "name": "Tom Trend", "user": "tom_t", "balance": 25000, "profit": 6200},
            {"rank": 9, "name": "Ryan Risk", "user": "ryan_r", "balance": 10000, "profit": 4100},
            {"rank": 10, "name": "Nina News", "user": "nina_n", "balance": 10000, "profit": 2300}
        ]

        for t in top_traders:
            try:
                if User.query.filter_by(username=t['user']).first():
                    print(f"   Skipping {t['name']} (Exists)")
                    continue

                user = User(
                    full_name=t['name'],
                    username=t['user'],
                    email=f"{t['user']}@trade.com",
                    role=UserRole.USER
                )
                user.set_password("password123")
                db.session.add(user)
                db.session.commit()
                
                account = Account(
                    user_id=user.id,
                    plan_name="Elite" if t['balance'] >= 100000 else "Pro",
                    initial_balance=t['balance'],
                    current_balance=t['balance'] + t['profit'],
                    equity=t['balance'] + t['profit'],
                    daily_starting_equity=t['balance'] + t['profit'],
                    status=ChallengeStatus.ACTIVE,
                    reason="Active Session",
                    admin_note=f"Rank #{t['rank']} - Manual Seed"
                )
                db.session.add(account)
                db.session.commit()
                
                trade = Trade(
                    account_id=account.id,
                    user_id=user.id,
                    symbol="XAUUSD",
                    side=TradeType.BUY,
                    quantity=1.0,
                    price=2000.0,
                    entry_price=2000.0,
                    exit_price=2000.0 + (t['profit'] / 20 * 20),
                    pnl=float(t['profit']),
                    status=TradeStatus.CLOSED,
                    closed_at=datetime.utcnow()
                )
                db.session.add(trade)
                db.session.commit()
                print(f"   + Created Rank {t['rank']}: {t['name']}")
                
            except Exception as e:
                db.session.rollback()
                print(f"   Error creating {t['name']}: {e}")
                import traceback
                traceback.print_exc()

        print("Final Seed Correct complete.")

if __name__ == '__main__':
    safe_cleanup_and_seed()
