"""
TRADESENSE AI - FULL DATA CONSISTENCY SEED SCRIPT
=================================================
This script ensures complete data consistency across all tables:
- users ↔ accounts ↔ trades ↔ leaderboard ↔ admin_actions_log

Run this script to:
1. Create missing users (with accounts)
2. Create realistic trades for all accounts
3. Backfill admin_actions_log for all status changes
4. Recalculate and sync leaderboard from real trade data
5. Verify data consistency

Usage: python seed_full_data_consistency.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import (
    db, User, Account, Trade, Leaderboard, AdminActionLog, PerformanceSnapshot,
    ChallengeStatus, UserRole, TradeType, TradeStatus
)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random
import json

# ============================================
# CONFIGURATION
# ============================================

# Traders to seed (ensuring diverse data)
TRADERS_DATA = [
    # Format: (full_name, username, email, role, plan, initial_balance, target_equity, status)
    ("Karim Trader", "karimtrader", "karim@trade.ma", "USER", "Starter", 5000, 5850, "ACTIVE"),
    ("Sara Admin", "saraadmin", "sara@admin.ma", "ADMIN", None, None, None, None),
    ("Super Admin", "superadmin", "admin@tradesense.ma", "SUPERADMIN", None, None, None, None),
    ("Lucas Martin", "lucasm", "lucas.martin@gmail.com", "USER", "Starter", 5000, 5200, "ACTIVE"),
    ("Sophia Nguyen", "sophian", "sophia.nguyen@example.com", "USER", "Elite", 100000, 110500, "PASSED"),
    ("Mohammed El Amrani", "mohamedel", "mohammed.ela@example.com", "USER", "Pro", 25000, 22500, "FAILED"),
    ("Emily Zhang", "emilyz", "emily.zhang@example.com", "USER", "Starter", 5000, 4500, "ACTIVE"),
    ("Ali Ben Said", "alibs", "alibensaid@example.com", "USER", "Pro", 25000, 27800, "ACTIVE"),
    ("Oliver Garcia", "oliverg", "oliver.garcia@example.com", "USER", "Starter", 5000, 4250, "FAILED"),
    ("Fatima Zahra", "fatimazahra", "fatima.z@trade.ma", "USER", "Elite", 100000, 112000, "PASSED"),
    ("Youssef Bennani", "youssef_b", "youssef.b@trade.ma", "USER", "Pro", 25000, 28500, "FUNDED"),
    ("Amina Hassani", "aminah", "amina.h@trade.ma", "USER", "Starter", 5000, 5650, "ACTIVE"),
    ("Hassan Idrissi", "hassani", "hassan.i@trade.ma", "USER", "Pro", 25000, 26200, "ACTIVE"),
    ("Leila Chakir", "leilac", "leila.c@trade.ma", "USER", "Elite", 100000, 98500, "ACTIVE"),
    ("Omar Tazi", "omart", "omar.t@trade.ma", "USER", "Starter", 5000, 5120, "ACTIVE"),
    ("Nadia Alami", "nadiaa", "nadia.a@trade.ma", "USER", "Pro", 25000, 27100, "PASSED"),
    ("Rachid Moussaoui", "rachidm", "rachid.m@trade.ma", "USER", "Starter", 5000, 4680, "ACTIVE"),
    ("Salma Benkirane", "salmab", "salma.b@trade.ma", "USER", "Elite", 100000, 105800, "ACTIVE"),
    ("Khalid Fassi", "khalidf", "khalid.f@trade.ma", "USER", "Pro", 25000, 23800, "ACTIVE"),
    ("Zineb Ouazzani", "zinebo", "zineb.o@trade.ma", "USER", "Starter", 5000, 5480, "ACTIVE"),
]

# Trading symbols
SYMBOLS = ["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "BTC/USD", "ETH/USD", "US30", "NAS100"]

# Countries for leaderboard
COUNTRIES = ["MA", "FR", "US", "UK", "DE", "ES", "AE", "SA", "EG", "TN"]

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_realistic_trades(account, target_equity):
    """
    Generate 30-100 realistic trades that result in the target equity.
    Trades will have realistic PnL distribution (some wins, some losses).
    """
    trades = []
    num_trades = random.randint(30, 80)
    
    # Calculate total PnL needed
    total_pnl_needed = target_equity - account.initial_balance
    
    # Generate trades with realistic distribution
    # 55-65% win rate is realistic for profitable traders
    win_rate = random.uniform(0.48, 0.68)
    num_wins = int(num_trades * win_rate)
    num_losses = num_trades - num_wins
    
    # Distribute PnL across trades
    # Winners typically have higher absolute values due to better RR ratio
    if total_pnl_needed > 0:
        # Profitable account: bigger wins
        avg_win = abs(total_pnl_needed) / num_wins * random.uniform(1.2, 1.8) if num_wins > 0 else 100
        avg_loss = abs(total_pnl_needed) / num_wins * random.uniform(0.5, 0.8) if num_wins > 0 else 50
    else:
        # Losing account: bigger losses
        avg_loss = abs(total_pnl_needed) / num_losses * random.uniform(1.2, 1.5) if num_losses > 0 else 100
        avg_win = abs(total_pnl_needed) / num_losses * random.uniform(0.3, 0.6) if num_losses > 0 else 30
    
    current_pnl = 0
    base_date = datetime.utcnow() - timedelta(days=random.randint(10, 60))
    
    for i in range(num_trades):
        is_last_trade = (i == num_trades - 1)
        is_winner = i < num_wins
        
        # Adjust last trade to hit exact target
        if is_last_trade:
            pnl = total_pnl_needed - current_pnl
        else:
            if is_winner:
                pnl = abs(avg_win) * random.uniform(0.5, 2.0)
            else:
                pnl = -abs(avg_loss) * random.uniform(0.5, 2.0)
        
        current_pnl += pnl
        
        symbol = random.choice(SYMBOLS)
        side = random.choice([TradeType.BUY, TradeType.SELL])
        
        # Generate realistic prices based on symbol
        if "XAU" in symbol:
            entry_price = random.uniform(1900, 2100)
        elif "BTC" in symbol:
            entry_price = random.uniform(40000, 70000)
        elif "ETH" in symbol:
            entry_price = random.uniform(2000, 4000)
        elif "US30" in symbol:
            entry_price = random.uniform(38000, 42000)
        elif "NAS100" in symbol:
            entry_price = random.uniform(17000, 20000)
        else:
            entry_price = random.uniform(1.05, 1.35)
        
        # Calculate exit price from PnL
        quantity = random.uniform(0.1, 2.0) if "USD" in symbol and "BTC" not in symbol else random.uniform(0.01, 0.5)
        
        if side == TradeType.BUY:
            exit_price = entry_price + (pnl / quantity) if quantity > 0 else entry_price + pnl
        else:
            exit_price = entry_price - (pnl / quantity) if quantity > 0 else entry_price - pnl
        
        trade_date = base_date + timedelta(hours=random.randint(1, 24) * (i + 1))
        
        trade = Trade(
            account_id=account.id,
            user_id=account.user_id,
            symbol=symbol,
            side=side,
            trade_type=side,
            quantity=round(quantity, 2),
            price=round(entry_price, 5),
            entry_price=round(entry_price, 5),
            exit_price=round(exit_price, 5) if pnl != 0 else None,
            amount=round(entry_price * quantity, 2),
            stop_loss=round(entry_price * (0.99 if side == TradeType.BUY else 1.01), 5),
            take_profit=round(entry_price * (1.02 if side == TradeType.BUY else 0.98), 5),
            status=TradeStatus.CLOSED,
            pnl=round(pnl, 2),
            commission=round(random.uniform(1.5, 5.0), 2),
            created_at=trade_date,
            closed_at=trade_date + timedelta(minutes=random.randint(5, 480)),
            timestamp=trade_date
        )
        trades.append(trade)
    
    return trades


def calculate_account_stats(account_id):
    """Calculate win rate, profit, and other stats from trades."""
    trades = Trade.query.filter_by(account_id=account_id, status=TradeStatus.CLOSED).all()
    
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
        # Add some noise but trend towards final equity
        progress = i / num_points
        expected = initial_balance + (total_change * progress)
        noise = random.uniform(-abs(total_change) * 0.1, abs(total_change) * 0.1)
        value = max(initial_balance * 0.85, expected + noise)  # Never go below 85% of initial
        curve.append(round(value, 2))
    
    # Ensure last point matches final equity
    curve.append(round(final_equity, 2))
    return curve


# ============================================
# MAIN SEED FUNCTIONS
# ============================================

def seed_users_and_accounts():
    """Step 1: Create all users and their accounts."""
    print("\n" + "="*60)
    print("STEP 1: SEEDING USERS AND ACCOUNTS")
    print("="*60)
    
    created_users = 0
    created_accounts = 0
    
    for data in TRADERS_DATA:
        full_name, username, email, role, plan, initial, target, status = data
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                full_name=full_name,
                username=username,
                email=email,
                role=UserRole[role]
            )
            user.set_password('123456')  # Default password
            db.session.add(user)
            db.session.commit()
            created_users += 1
            print(f"  ✅ Created user: {full_name} ({role})")
        else:
            print(f"  ⏭️  User exists: {full_name}")
        
        # Create account if this user should have one (not admin/superadmin without plan)
        if plan and initial:
            account = Account.query.filter_by(user_id=user.id).first()
            if not account:
                account = Account(
                    user_id=user.id,
                    plan_name=plan,
                    initial_balance=initial,
                    current_balance=target,
                    equity=target,
                    daily_starting_equity=target,
                    status=ChallengeStatus[status]
                )
                db.session.add(account)
                db.session.commit()
                created_accounts += 1
                print(f"      ✅ Created account: {plan} (${initial:,} → ${target:,}) [{status}]")
            else:
                # Update existing account to target values
                account.equity = target
                account.current_balance = target
                account.status = ChallengeStatus[status]
                db.session.commit()
                print(f"      ⏭️  Account exists, updated: {plan} [{status}]")
    
    print(f"\n📊 Summary: Created {created_users} users, {created_accounts} accounts")
    return created_users, created_accounts


def seed_trades_for_accounts():
    """Step 2: Generate realistic trades for all accounts."""
    print("\n" + "="*60)
    print("STEP 2: SEEDING TRADES FOR ALL ACCOUNTS")
    print("="*60)
    
    accounts = Account.query.all()
    total_trades = 0
    
    for account in accounts:
        existing_trades = Trade.query.filter_by(account_id=account.id).count()
        
        if existing_trades >= 10:
            print(f"  ⏭️  Account #{account.id} ({account.plan_name}) already has {existing_trades} trades")
            continue
        
        # Delete any existing trades for clean seed
        Trade.query.filter_by(account_id=account.id).delete()
        db.session.commit()
        
        # Generate new trades
        trades = generate_realistic_trades(account, account.equity)
        
        for trade in trades:
            db.session.add(trade)
        
        db.session.commit()
        total_trades += len(trades)
        
        stats = calculate_account_stats(account.id)
        print(f"  ✅ Account #{account.id} ({account.plan_name}): {len(trades)} trades, "
              f"Win Rate: {stats['win_rate']:.1f}%, Total PnL: ${stats['total_profit']:+,.2f}")
    
    print(f"\n📊 Summary: Created {total_trades} total trades")
    return total_trades


def backfill_admin_actions_log():
    """Step 3: Create admin_actions_log entries for all status changes."""
    print("\n" + "="*60)
    print("STEP 3: BACKFILLING ADMIN ACTIONS LOG")
    print("="*60)
    
    # Get admin user for backfill attribution
    admin_user = User.query.filter(User.role.in_([UserRole.ADMIN, UserRole.SUPERADMIN])).first()
    if not admin_user:
        print("  ⚠️  No admin user found! Creating default admin...")
        admin_user = User(
            full_name="System Admin",
            username="sysadmin",
            email="sysadmin@tradesense.ma",
            role=UserRole.ADMIN
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
    
    created_logs = 0
    
    # Get all accounts with non-ACTIVE status that don't have a log entry
    accounts_needing_log = db.session.query(Account).filter(
        Account.status.in_([ChallengeStatus.PASSED, ChallengeStatus.FAILED, ChallengeStatus.FUNDED])
    ).all()
    
    for account in accounts_needing_log:
        # Check if log already exists for this account
        existing_log = AdminActionLog.query.filter_by(target_account_id=account.id).first()
        
        if not existing_log:
            action = f"backfill_status_{account.status.value.lower()}"
            note = f"[Migration Backfill] Account status was {account.status.value} - log created for data consistency"
            
            log = AdminActionLog(
                admin_id=admin_user.id,
                target_account_id=account.id,
                action=action,
                note=note,
                created_at=account.created_at or datetime.utcnow()
            )
            db.session.add(log)
            created_logs += 1
            
            user = User.query.get(account.user_id)
            print(f"  ✅ Created log: {action} for {user.full_name if user else 'Unknown'} (Account #{account.id})")
    
    db.session.commit()
    
    # Also create logs for any account that has admin_note but no log
    accounts_with_notes = Account.query.filter(
        Account.admin_note.isnot(None),
        Account.admin_note != ''
    ).all()
    
    for account in accounts_with_notes:
        existing_log = AdminActionLog.query.filter_by(target_account_id=account.id).first()
        if not existing_log:
            log = AdminActionLog(
                admin_id=admin_user.id,
                target_account_id=account.id,
                action="admin_note_added",
                note=f"[Backfill] Admin note: {account.admin_note}",
                created_at=datetime.utcnow()
            )
            db.session.add(log)
            created_logs += 1
    
    db.session.commit()
    print(f"\n📊 Summary: Created {created_logs} admin action logs")
    return created_logs


def sync_leaderboard_from_trades():
    """Step 4: Recalculate leaderboard from actual trade data."""
    print("\n" + "="*60)
    print("STEP 4: SYNCING LEADERBOARD FROM TRADES")
    print("="*60)
    
    # Clear existing leaderboard
    Leaderboard.query.delete()
    db.session.commit()
    print("  🗑️  Cleared existing leaderboard entries")
    
    # Get all profitable accounts (ACTIVE, PASSED, FUNDED only)
    accounts = Account.query.filter(
        Account.status.in_([ChallengeStatus.ACTIVE, ChallengeStatus.PASSED, ChallengeStatus.FUNDED])
    ).all()
    
    candidates = []
    
    for account in accounts:
        stats = calculate_account_stats(account.id)
        user = User.query.get(account.user_id)
        
        if not user:
            continue
        
        profit = stats['total_profit']
        
        # Only include profitable or notable traders
        if profit <= -account.initial_balance * 0.5:  # Skip if lost more than 50%
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
            'risk_score': max(0, 100 - abs(roi / 2))
        })
    
    # Sort by profit
    candidates.sort(key=lambda x: x['profit'], reverse=True)
    
    # Create leaderboard entries
    for i, c in enumerate(candidates[:50]):  # Top 50
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
            period='ALL_TIME',
            badges=json.dumps(c['badges']),
            equity_curve=json.dumps(c['equity_curve']),
            is_visible=True
        )
        db.session.add(entry)
        print(f"  🏆 Rank #{i+1}: {c['username']} - ${c['profit']:+,.2f} ({c['roi']:+.2f}% ROI)")
    
    db.session.commit()
    print(f"\n📊 Summary: Created {len(candidates[:50])} leaderboard entries")
    return len(candidates[:50])


def create_performance_snapshots():
    """Step 5: Create performance snapshots for all accounts."""
    print("\n" + "="*60)
    print("STEP 5: CREATING PERFORMANCE SNAPSHOTS")
    print("="*60)
    
    # Clear existing snapshots
    PerformanceSnapshot.query.delete()
    db.session.commit()
    
    accounts = Account.query.all()
    snapshots_created = 0
    
    for account in accounts:
        stats = calculate_account_stats(account.id)
        
        snapshot = PerformanceSnapshot(
            account_id=account.id,
            period='ALL_TIME',
            date=datetime.utcnow().date(),
            profit=stats['total_profit'],
            roi=(stats['total_profit'] / account.initial_balance * 100) if account.initial_balance > 0 else 0,
            win_rate=stats['win_rate'],
            trades_count=stats['trades_count'],
            equity=account.equity
        )
        db.session.add(snapshot)
        snapshots_created += 1
    
    db.session.commit()
    print(f"  ✅ Created {snapshots_created} performance snapshots")
    return snapshots_created


def verify_data_consistency():
    """Step 6: Run verification queries and report any issues."""
    print("\n" + "="*60)
    print("STEP 6: VERIFYING DATA CONSISTENCY")
    print("="*60)
    
    issues = []
    
    # 1. Users without accounts (excluding admins)
    users_no_accounts = db.session.query(User).outerjoin(Account).filter(
        Account.id == None,
        User.role == UserRole.USER
    ).all()
    
    if users_no_accounts:
        issues.append(f"⚠️  {len(users_no_accounts)} USER(s) without accounts")
        for u in users_no_accounts[:5]:
            print(f"     - {u.full_name} ({u.email})")
    else:
        print("  ✅ All regular users have accounts")
    
    # 2. Accounts without trades
    accounts_no_trades = db.session.query(Account).outerjoin(Trade).filter(
        Trade.id == None
    ).all()
    
    if accounts_no_trades:
        issues.append(f"⚠️  {len(accounts_no_trades)} account(s) without trades")
    else:
        print("  ✅ All accounts have trades")
    
    # 3. Leaderboard entries with invalid FK
    invalid_leaderboard = db.session.query(Leaderboard).outerjoin(
        User, Leaderboard.user_id == User.id
    ).outerjoin(
        Account, Leaderboard.account_id == Account.id
    ).filter(
        db.or_(
            db.and_(Leaderboard.user_id.isnot(None), User.id == None),
            db.and_(Leaderboard.account_id.isnot(None), Account.id == None)
        )
    ).all()
    
    if invalid_leaderboard:
        issues.append(f"⚠️  {len(invalid_leaderboard)} invalid leaderboard entries")
    else:
        print("  ✅ All leaderboard entries have valid FK references")
    
    # 4. Accounts with PASSED/FAILED/FUNDED without admin log
    status_no_log = db.session.query(Account).outerjoin(
        AdminActionLog, AdminActionLog.target_account_id == Account.id
    ).filter(
        Account.status.in_([ChallengeStatus.PASSED, ChallengeStatus.FAILED, ChallengeStatus.FUNDED]),
        AdminActionLog.id == None
    ).all()
    
    if status_no_log:
        issues.append(f"⚠️  {len(status_no_log)} status changes without admin log")
    else:
        print("  ✅ All status changes have admin logs")
    
    # 5. Print summary stats
    print("\n" + "-"*40)
    print("DATABASE STATISTICS:")
    print("-"*40)
    print(f"  👤 Total Users: {User.query.count()}")
    print(f"  💼 Total Accounts: {Account.query.count()}")
    print(f"  📈 Total Trades: {Trade.query.count()}")
    print(f"  🏆 Leaderboard Entries: {Leaderboard.query.count()}")
    print(f"  📝 Admin Action Logs: {AdminActionLog.query.count()}")
    print(f"  📊 Performance Snapshots: {PerformanceSnapshot.query.count()}")
    
    if issues:
        print("\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("\n✅ ALL DATA CONSISTENCY CHECKS PASSED!")
        return True


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("🚀 TRADESENSE AI - FULL DATA CONSISTENCY SEED")
    print("="*60)
    print(f"Started at: {datetime.now().isoformat()}")
    
    with app.app_context():
        try:
            # Step 1: Users & Accounts
            seed_users_and_accounts()
            
            # Step 2: Trades
            seed_trades_for_accounts()
            
            # Step 3: Admin Logs Backfill
            backfill_admin_actions_log()
            
            # Step 4: Leaderboard Sync
            sync_leaderboard_from_trades()
            
            # Step 5: Performance Snapshots
            create_performance_snapshots()
            
            # Step 6: Verification
            success = verify_data_consistency()
            
            print("\n" + "="*60)
            if success:
                print("✅ DATA CONSISTENCY SEED COMPLETED SUCCESSFULLY!")
            else:
                print("⚠️  SEED COMPLETED WITH WARNINGS - Review Issues Above")
            print("="*60)
            print(f"Completed at: {datetime.now().isoformat()}\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
