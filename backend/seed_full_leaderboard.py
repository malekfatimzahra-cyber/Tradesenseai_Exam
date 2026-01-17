from app import app
from models import db, User, Account, ChallengeStatus, Trade, TradeType, TradeStatus, Leaderboard, PerformanceSnapshot, UserRole, AdminActionLog
from datetime import datetime, timedelta
import random
import json

def seed_leaderboard():
    with app.app_context():
        print("--- Seeding Leaderboard & Admin Data ---")
        
        # 1. DROP Tables to ensure schema update (Development only)
        Leaderboard.__table__.drop(db.engine, checkfirst=True)
        PerformanceSnapshot.__table__.drop(db.engine, checkfirst=True)
        # AdminActionLog.__table__.drop(db.engine, checkfirst=True) # Optional
        
        db.create_all() 
        
        # Clear existing data (implicit by drop, but good for safety)
        # Leaderboard.query.delete() 
        
        # Clear existing demo users if needed or just find them
        
        elite_traders = [
            {
                "username": "AtlasTrader_MA",
                "fullname": "Karim Benali",
                "country": "MA",
                "plan": "Elite $100k",
                "initial": 100000,
                "equity": 124500,
                "status": ChallengeStatus.FUNDED,
                "badges": ["Elite", "Sniper", "Risk Manager"],
                "win_rate": 78.5,
                "roi": 24.5,
                "consistency": 92,
                "risk_score": 9.5
            },
            {
                "username": "SarahFX",
                "fullname": "Sarah Connor",
                "country": "US",
                "plan": "Pro $200k",
                "initial": 200000,
                "equity": 238000,
                "status": ChallengeStatus.FUNDED,
                "badges": ["Consistent", "Shark"],
                "win_rate": 65.2,
                "roi": 19.0,
                "consistency": 88,
                "risk_score": 8.0
            },
            {
                "username": "TokyoDrift",
                "fullname": "Kenji Sato",
                "country": "JP",
                "plan": "Starter $50k",
                "initial": 50000,
                "equity": 58200,
                "status": ChallengeStatus.FUNDED,
                "badges": ["Algo", " disciplined"],
                "win_rate": 81.0,
                "roi": 16.4,
                "consistency": 95,
                "risk_score": 9.8
            },
            {
                "username": "EuroKing",
                "fullname": "Hans Zimmer",
                "country": "DE",
                "plan": "Elite $100k",
                "initial": 100000,
                "equity": 112000,
                "status": ChallengeStatus.PASSED,
                "badges": ["Funded"],
                "win_rate": 55.5,
                "roi": 12.0,
                "consistency": 70,
                "risk_score": 6.5
            },
            {
                "username": "DubaiWhale",
                "fullname": "Ahmed Al-Maktoum",
                "country": "AE",
                "plan": "VIP $500k",
                "initial": 500000,
                "equity": 545000,
                "status": ChallengeStatus.ACTIVE,
                "badges": ["VIP", "Whale"],
                "win_rate": 60.0,
                "roi": 9.0,
                "consistency": 85,
                "risk_score": 7.5
            }
        ]

        # Create/Get Users and Accounts
        for i, trader_data in enumerate(elite_traders):
            user = User.query.filter_by(username=trader_data['username']).first()
            if not user:
                user = User(
                    username=trader_data['username'],
                    full_name=trader_data['fullname'],
                    email=f"{trader_data['username'].lower()}@tradesense.ai",
                    role=UserRole.USER
                )
                user.set_password("password123")
                db.session.add(user)
                db.session.commit()
                print(f"Created User: {user.username}")
            
            # Create Account if not exists (simplify: just create a new one for leaderboard demo)
            account = Account(
                user_id=user.id,
                plan_name=trader_data['plan'],
                initial_balance=trader_data['initial'],
                current_balance=trader_data['equity'],
                equity=trader_data['equity'],
                status=trader_data['status'],
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 90))
            )
            db.session.add(account)
            db.session.commit()

            # Create Performance Snapshots (Mini Chart Data)
            # Generate 20 points of data leading up to current equity
            snapshots_json = []
            current_eq = trader_data['initial']
            target_eq = trader_data['equity']
            
            # Linear interp + noise
            steps = 20
            step_val = (target_eq - current_eq) / steps
            
            for d in range(steps):
                date_point = datetime.utcnow() - timedelta(days=steps - d)
                
                # Add some volatility
                noise = random.uniform(-step_val * 0.5, step_val * 1.5)
                current_eq += step_val + (noise * 0.2)
                
                snap = PerformanceSnapshot(
                    account_id=account.id,
                    period='ALL_TIME',
                    date=date_point.date(),
                    equity=current_eq,
                    profit=current_eq - trader_data['initial'],
                    roi=((current_eq - trader_data['initial']) / trader_data['initial']) * 100,
                    win_rate=trader_data['win_rate'] + random.uniform(-2, 2)
                )
                db.session.add(snap)
                snapshots_json.append(current_eq)
            
            # Final snapshot matching current
            db.session.add(PerformanceSnapshot(
                account_id=account.id,
                period='ALL_TIME',
                date=datetime.utcnow().date(),
                equity=trader_data['equity'],
                profit=trader_data['equity'] - trader_data['initial'],
                roi=trader_data['roi'],
                win_rate=trader_data['win_rate']
            ))
            snapshots_json.append(trader_data['equity'])
            
            db.session.commit()

            # Create Leaderboard Entry (ALL_TIME)
            lb_entry = Leaderboard(
                user_id=user.id,
                account_id=account.id,
                username=user.username,
                country=trader_data['country'],
                avatar_url=None, 
                profit=trader_data['equity'] - trader_data['initial'],
                roi=trader_data['roi'],
                win_rate=trader_data['win_rate'],
                funded_amount=trader_data['initial'],
                consistency_score=trader_data['consistency'],
                risk_score=trader_data['risk_score'],
                ranking=i + 1,
                period='ALL_TIME',
                badges=json.dumps(trader_data['badges']),
                equity_curve=json.dumps(snapshots_json) 
            )
            db.session.add(lb_entry)

            # Create Leaderboard Entry (THIS_MONTH) - For demo, same data
            lb_entry_month = Leaderboard(
                user_id=user.id,
                account_id=account.id,
                username=user.username,
                country=trader_data['country'],
                avatar_url=None, 
                profit=trader_data['equity'] - trader_data['initial'], # Assuming all profit this month for demo
                roi=trader_data['roi'],
                win_rate=trader_data['win_rate'],
                funded_amount=trader_data['initial'],
                consistency_score=trader_data['consistency'],
                risk_score=trader_data['risk_score'],
                ranking=i + 1,
                period='THIS_MONTH',
                badges=json.dumps(trader_data['badges']),
                equity_curve=json.dumps(snapshots_json) 
            )
            db.session.add(lb_entry_month)

            print(f"Leaderboard Entries added for {user.username} (Rank {i+1})")
        
        # --- SEED ADMIN ACTIONS LOG ---
        print("Seeding Admin Actions Log...")
        # Create an Admin User
        admin_user = User.query.filter_by(role=UserRole.ADMIN).first()
        if not admin_user:
            admin_user = User(
                username='SuperAdmin_Youssef', 
                full_name='Youssef Admin',
                email='admin@tradesense.ai',
                role=UserRole.ADMIN
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            
        # Add some logs targeting the elite traders
        actions = ['set_passed', 'status_change_funded', 'note_added', 'unlock']
        
        # Get some accounts we just created
        accounts = Account.query.limit(3).all()
        
        for acc in accounts:
            log = AdminActionLog(
                admin_id=admin_user.id,
                target_account_id=acc.id,
                action=random.choice(actions),
                note=f"Manual override by admin during migration. Previous status: {acc.status.value}",
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.session.add(log)
            
        db.session.commit()
        print(f"✅ Admin Logs Seeded!")

        db.session.commit()
        print("✅ Leaderboard Seeding Complete!")

if __name__ == '__main__':
    seed_leaderboard()
