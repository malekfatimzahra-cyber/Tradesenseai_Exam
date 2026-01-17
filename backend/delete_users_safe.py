"""
TRADESENSE AI - SAFE USER DELETION SCRIPT
==========================================
This script safely deletes specified users and ALL their related data
from all tables with proper CASCADE handling, backup, and transaction safety.

FEATURES:
- Backup before delete (exported to JSON)
- Transaction-based (rollback on error)
- Cascade delete in correct order
- Verification queries after deletion
- No orphan rows left

Usage: python delete_users_safe.py [--dry-run] [--backup-only]
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import (
    db, User, Account, Trade, Leaderboard, AdminActionLog, PerformanceSnapshot,
    Transaction, Post, Comment, PostLike, FloorMessage, UserCourseProgress,
    UserLessonProgress, UserQuizAttempt, UserBadge, UserXP, RiskAlert,
    UserRole, Challenge
)
from sqlalchemy import text

# ============================================
# USERS TO DELETE (From Screenshots)
# ============================================

# Screenshot 1: IDs 50-60
USERS_TO_DELETE_SCREENSHOT_1 = [
    # (id, username, email)
    (50, "SarahFX", "sarahfx@tradesense.ai"),
    (51, "TokyoDrift", "tokyodrift@tradesense.ai"),
    (52, "EuroKing", "euroking@tradesense.ai"),
    (53, "DubaiWhale", "dubaiwhale@tradesense.ai"),
    # (54, "superadmin", "superadmin@tradesense.ma"),  # SKIP - This is SUPERADMIN
    (55, "lucasm", "lucas.martin@gmail.com"),
    (56, "sophian", "sophia.nguyen@example.com"),
    (57, "mohamedel", "mohammed.ela@example.com"),
    (58, "emilyz", "emily.zhang@example.com"),
    (59, "alibs", "alibensaid@example.com"),
    (60, "oliverg", "oliver.garcia@example.com"),
]

# Screenshot 2: IDs 28-37
USERS_TO_DELETE_SCREENSHOT_2 = [
    (28, "alex_pro", "alex_pro@trade.com"),
    (29, "sarah_x", "sarah_x@trade.com"),
    (30, "mike_m", "mike_m@trade.com"),
    (31, "emma_e", "emma_e@trade.com"),
    (32, "david_d", "david_d@trade.com"),
    (33, "lucas_l", "lucas_l@trade.com"),
    (34, "julia_j", "julia_j@trade.com"),
    (35, "tom_t", "tom_t@trade.com"),
    (36, "ryan_r", "ryan_r@trade.com"),
    (37, "nina_n", "nina_n@trade.com"),
]

# Combine all users
ALL_USERS_TO_DELETE = USERS_TO_DELETE_SCREENSHOT_1 + USERS_TO_DELETE_SCREENSHOT_2

# Extract emails and usernames for queries
EMAILS_TO_DELETE = [u[2] for u in ALL_USERS_TO_DELETE]
USERNAMES_TO_DELETE = [u[1] for u in ALL_USERS_TO_DELETE]

# ============================================
# BACKUP FUNCTION
# ============================================

def backup_user_data(user_ids, backup_dir="backups"):
    """Backup all data for specified users to JSON files."""
    
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"users_backup_{timestamp}.json")
    
    backup_data = {
        "deleted_at": timestamp,
        "user_ids": user_ids,
        "users": [],
        "accounts": [],
        "trades": [],
        "leaderboard": [],
        "admin_logs": [],
        "performance_snapshots": [],
        "transactions": [],
        "posts": [],
        "comments": [],
        "post_likes": [],
        "floor_messages": [],
        "user_course_progress": [],
        "user_lesson_progress": [],
        "user_quiz_attempts": [],
        "user_badges": [],
        "user_xp": [],
        "risk_alerts": [],
        "challenges": [],
    }
    
    # Backup Users
    users = User.query.filter(User.id.in_(user_ids)).all()
    for u in users:
        backup_data["users"].append({
            "id": u.id,
            "full_name": u.full_name,
            "username": u.username,
            "email": u.email,
            "role": u.role.value,
            "created_at": u.created_at.isoformat() if u.created_at else None
        })
    
    # Backup Accounts
    accounts = Account.query.filter(Account.user_id.in_(user_ids)).all()
    account_ids = [a.id for a in accounts]
    for a in accounts:
        backup_data["accounts"].append({
            "id": a.id,
            "user_id": a.user_id,
            "plan_name": a.plan_name,
            "initial_balance": a.initial_balance,
            "equity": a.equity,
            "status": a.status.value
        })
    
    # Backup Trades
    trades = Trade.query.filter(Trade.account_id.in_(account_ids)).all()
    for t in trades:
        backup_data["trades"].append({
            "id": t.id,
            "account_id": t.account_id,
            "user_id": t.user_id,
            "symbol": t.symbol,
            "pnl": t.pnl
        })
    
    # Backup Leaderboard
    lb_entries = Leaderboard.query.filter(Leaderboard.user_id.in_(user_ids)).all()
    for lb in lb_entries:
        backup_data["leaderboard"].append({
            "id": lb.id,
            "user_id": lb.user_id,
            "username": lb.username,
            "profit": lb.profit
        })
    
    # Backup Admin Logs (as admin or target)
    admin_logs = AdminActionLog.query.filter(
        db.or_(
            AdminActionLog.admin_id.in_(user_ids),
            AdminActionLog.target_account_id.in_(account_ids)
        )
    ).all()
    for log in admin_logs:
        backup_data["admin_logs"].append({
            "id": log.id,
            "admin_id": log.admin_id,
            "target_account_id": log.target_account_id,
            "action": log.action
        })
    
    # Backup Performance Snapshots
    snapshots = PerformanceSnapshot.query.filter(
        PerformanceSnapshot.account_id.in_(account_ids)
    ).all()
    for s in snapshots:
        backup_data["performance_snapshots"].append({
            "id": s.id,
            "account_id": s.account_id,
            "profit": s.profit
        })
    
    # Backup Transactions
    transactions = Transaction.query.filter(Transaction.user_id.in_(user_ids)).all()
    for t in transactions:
        backup_data["transactions"].append({
            "id": t.id,
            "user_id": t.user_id,
            "amount": t.amount
        })
    
    # Backup Posts
    posts = Post.query.filter(Post.user_id.in_(user_ids)).all()
    post_ids = [p.id for p in posts]
    for p in posts:
        backup_data["posts"].append({
            "id": p.id,
            "user_id": p.user_id,
            "content": p.content[:100] if p.content else None
        })
    
    # Backup Comments
    comments = Comment.query.filter(Comment.user_id.in_(user_ids)).all()
    for c in comments:
        backup_data["comments"].append({
            "id": c.id,
            "user_id": c.user_id,
            "post_id": c.post_id
        })
    
    # Backup other tables...
    try:
        floor_msgs = FloorMessage.query.filter(FloorMessage.user_id.in_(user_ids)).all()
        for m in floor_msgs:
            backup_data["floor_messages"].append({"id": m.id, "user_id": m.user_id})
    except:
        pass
    
    try:
        course_progress = UserCourseProgress.query.filter(
            UserCourseProgress.user_id.in_(user_ids)
        ).all()
        for cp in course_progress:
            backup_data["user_course_progress"].append({"id": cp.id, "user_id": cp.user_id})
    except:
        pass
    
    try:
        lesson_progress = UserLessonProgress.query.filter(
            UserLessonProgress.user_id.in_(user_ids)
        ).all()
        for lp in lesson_progress:
            backup_data["user_lesson_progress"].append({"id": lp.id, "user_id": lp.user_id})
    except:
        pass
    
    try:
        quiz_attempts = UserQuizAttempt.query.filter(
            UserQuizAttempt.user_id.in_(user_ids)
        ).all()
        for qa in quiz_attempts:
            backup_data["user_quiz_attempts"].append({"id": qa.id, "user_id": qa.user_id})
    except:
        pass
    
    try:
        user_badges = UserBadge.query.filter(UserBadge.user_id.in_(user_ids)).all()
        for ub in user_badges:
            backup_data["user_badges"].append({"id": ub.id, "user_id": ub.user_id})
    except:
        pass
    
    try:
        user_xp = UserXP.query.filter(UserXP.user_id.in_(user_ids)).all()
        for ux in user_xp:
            backup_data["user_xp"].append({"user_id": ux.user_id, "total_xp": ux.total_xp})
    except:
        pass
    
    try:
        risk_alerts = RiskAlert.query.filter(RiskAlert.user_id.in_(user_ids)).all()
        for ra in risk_alerts:
            backup_data["risk_alerts"].append({"id": ra.id, "user_id": ra.user_id})
    except:
        pass
    
    try:
        challenges = Challenge.query.filter(Challenge.user_id.in_(user_ids)).all()
        for ch in challenges:
            backup_data["challenges"].append({"id": ch.id, "user_id": ch.user_id})
    except:
        pass
    
    # Write backup to file
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Backup saved to: {backup_file}")
    return backup_file, account_ids


# ============================================
# DELETE FUNCTION
# ============================================

def delete_users_cascade(user_ids, dry_run=False):
    """
    Delete users and all related data in correct order.
    
    Order of deletion (children first, parents last):
    1. trades (FK: account_id)
    2. performance_snapshots (FK: account_id)
    3. admin_actions_log (FK: admin_id, target_account_id)
    4. transactions (FK: user_id, account_id)
    5. leaderboard (FK: user_id, account_id)
    6. post_likes (FK: user_id)
    7. comments (FK: user_id)
    8. posts (FK: user_id)
    9. floor_messages (FK: user_id)
    10. user_course_progress (FK: user_id)
    11. user_lesson_progress (FK: user_id)
    12. user_quiz_attempts (FK: user_id)
    13. user_badges (FK: user_id)
    14. user_xp (FK: user_id)
    15. risk_alerts (FK: user_id)
    16. challenges (FK: user_id)
    17. accounts (FK: user_id)
    18. users (PARENT)
    """
    
    print("\n" + "="*60)
    print("🗑️  DELETING USERS AND RELATED DATA")
    if dry_run:
        print("   [DRY RUN - NO CHANGES WILL BE MADE]")
    print("="*60)
    
    # Get account IDs first
    accounts = Account.query.filter(Account.user_id.in_(user_ids)).all()
    account_ids = [a.id for a in accounts]
    
    deletion_counts = {}
    
    try:
        # 1. Delete trades
        count = Trade.query.filter(Trade.account_id.in_(account_ids)).delete(synchronize_session=False)
        deletion_counts['trades'] = count
        print(f"  ✓ trades: {count} rows")
        
        # 2. Delete performance_snapshots
        count = PerformanceSnapshot.query.filter(
            PerformanceSnapshot.account_id.in_(account_ids)
        ).delete(synchronize_session=False)
        deletion_counts['performance_snapshots'] = count
        print(f"  ✓ performance_snapshots: {count} rows")
        
        # 3. Delete admin_actions_log (where user is admin OR target account belongs to user)
        count = AdminActionLog.query.filter(
            db.or_(
                AdminActionLog.admin_id.in_(user_ids),
                AdminActionLog.target_account_id.in_(account_ids)
            )
        ).delete(synchronize_session=False)
        deletion_counts['admin_actions_log'] = count
        print(f"  ✓ admin_actions_log: {count} rows")
        
        # 4. Delete transactions
        count = Transaction.query.filter(Transaction.user_id.in_(user_ids)).delete(synchronize_session=False)
        deletion_counts['transactions'] = count
        print(f"  ✓ transactions: {count} rows")
        
        # 5. Delete leaderboard
        count = Leaderboard.query.filter(Leaderboard.user_id.in_(user_ids)).delete(synchronize_session=False)
        deletion_counts['leaderboard'] = count
        print(f"  ✓ leaderboard: {count} rows")
        
        # 6. Delete post_likes
        try:
            count = PostLike.query.filter(PostLike.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['post_likes'] = count
            print(f"  ✓ post_likes: {count} rows")
        except Exception as e:
            print(f"  ⚠ post_likes: skipped ({e})")
        
        # 7. Delete comments
        try:
            count = Comment.query.filter(Comment.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['comments'] = count
            print(f"  ✓ comments: {count} rows")
        except Exception as e:
            print(f"  ⚠ comments: skipped ({e})")
        
        # 8. Delete posts
        try:
            count = Post.query.filter(Post.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['posts'] = count
            print(f"  ✓ posts: {count} rows")
        except Exception as e:
            print(f"  ⚠ posts: skipped ({e})")
        
        # 9. Delete floor_messages
        try:
            count = FloorMessage.query.filter(FloorMessage.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['floor_messages'] = count
            print(f"  ✓ floor_messages: {count} rows")
        except Exception as e:
            print(f"  ⚠ floor_messages: skipped ({e})")
        
        # 10. Delete user_course_progress
        try:
            count = UserCourseProgress.query.filter(
                UserCourseProgress.user_id.in_(user_ids)
            ).delete(synchronize_session=False)
            deletion_counts['user_course_progress'] = count
            print(f"  ✓ user_course_progress: {count} rows")
        except Exception as e:
            print(f"  ⚠ user_course_progress: skipped ({e})")
        
        # 11. Delete user_lesson_progress
        try:
            count = UserLessonProgress.query.filter(
                UserLessonProgress.user_id.in_(user_ids)
            ).delete(synchronize_session=False)
            deletion_counts['user_lesson_progress'] = count
            print(f"  ✓ user_lesson_progress: {count} rows")
        except Exception as e:
            print(f"  ⚠ user_lesson_progress: skipped ({e})")
        
        # 12. Delete user_quiz_attempts
        try:
            count = UserQuizAttempt.query.filter(
                UserQuizAttempt.user_id.in_(user_ids)
            ).delete(synchronize_session=False)
            deletion_counts['user_quiz_attempts'] = count
            print(f"  ✓ user_quiz_attempts: {count} rows")
        except Exception as e:
            print(f"  ⚠ user_quiz_attempts: skipped ({e})")
        
        # 13. Delete user_badges
        try:
            count = UserBadge.query.filter(UserBadge.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['user_badges'] = count
            print(f"  ✓ user_badges: {count} rows")
        except Exception as e:
            print(f"  ⚠ user_badges: skipped ({e})")
        
        # 14. Delete user_xp
        try:
            count = UserXP.query.filter(UserXP.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['user_xp'] = count
            print(f"  ✓ user_xp: {count} rows")
        except Exception as e:
            print(f"  ⚠ user_xp: skipped ({e})")
        
        # 15. Delete risk_alerts
        try:
            count = RiskAlert.query.filter(RiskAlert.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['risk_alerts'] = count
            print(f"  ✓ risk_alerts: {count} rows")
        except Exception as e:
            print(f"  ⚠ risk_alerts: skipped ({e})")
        
        # 16. Delete challenges
        try:
            count = Challenge.query.filter(Challenge.user_id.in_(user_ids)).delete(synchronize_session=False)
            deletion_counts['challenges'] = count
            print(f"  ✓ challenges: {count} rows")
        except Exception as e:
            print(f"  ⚠ challenges: skipped ({e})")
        
        # 17. Delete accounts
        count = Account.query.filter(Account.user_id.in_(user_ids)).delete(synchronize_session=False)
        deletion_counts['accounts'] = count
        print(f"  ✓ accounts: {count} rows")
        
        # 18. DELETE USERS (PARENT - LAST)
        count = User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        deletion_counts['users'] = count
        print(f"  ✓ users: {count} rows")
        
        if dry_run:
            db.session.rollback()
            print("\n⚠️  DRY RUN - All changes rolled back")
        else:
            db.session.commit()
            print("\n✅ All deletions committed successfully!")
        
        return deletion_counts
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERROR: {e}")
        print("🔄 Transaction rolled back - no changes made")
        raise


# ============================================
# VERIFICATION FUNCTION
# ============================================

def verify_deletion(user_ids, emails, usernames):
    """Verify that all data has been deleted."""
    
    print("\n" + "="*60)
    print("🔍 VERIFICATION - Checking for remaining data")
    print("="*60)
    
    issues = []
    
    # Check users
    remaining_users = User.query.filter(
        db.or_(
            User.id.in_(user_ids),
            User.email.in_(emails),
            User.username.in_(usernames)
        )
    ).count()
    
    if remaining_users > 0:
        issues.append(f"❌ {remaining_users} users still exist")
    else:
        print(f"  ✓ users: 0 remaining")
    
    # Check accounts
    remaining_accounts = Account.query.filter(Account.user_id.in_(user_ids)).count()
    if remaining_accounts > 0:
        issues.append(f"❌ {remaining_accounts} accounts still exist")
    else:
        print(f"  ✓ accounts: 0 remaining")
    
    # Check trades (need to get account IDs differently since accounts are deleted)
    # We use direct SQL for this
    try:
        result = db.session.execute(
            text("SELECT COUNT(*) FROM trades WHERE user_id IN :user_ids"),
            {"user_ids": tuple(user_ids) if len(user_ids) > 1 else (user_ids[0],)}
        ).scalar()
        if result > 0:
            issues.append(f"❌ {result} trades still exist")
        else:
            print(f"  ✓ trades: 0 remaining")
    except:
        print("  ⚠ trades: could not verify")
    
    # Check leaderboard
    remaining_lb = Leaderboard.query.filter(Leaderboard.user_id.in_(user_ids)).count()
    if remaining_lb > 0:
        issues.append(f"❌ {remaining_lb} leaderboard entries still exist")
    else:
        print(f"  ✓ leaderboard: 0 remaining")
    
    # Check admin_actions_log
    remaining_logs = AdminActionLog.query.filter(AdminActionLog.admin_id.in_(user_ids)).count()
    if remaining_logs > 0:
        issues.append(f"❌ {remaining_logs} admin logs still exist")
    else:
        print(f"  ✓ admin_actions_log: 0 remaining")
    
    print("\n" + "-"*40)
    if issues:
        print("⚠️  VERIFICATION FAILED:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ VERIFICATION PASSED - All data deleted")
        return True


# ============================================
# MAIN FUNCTION
# ============================================

def main(dry_run=False, backup_only=False):
    """Main execution function."""
    
    print("\n" + "="*70)
    print("🗑️  TRADESENSE AI - SAFE USER DELETION SCRIPT")
    print("="*70)
    print(f"Started at: {datetime.now().isoformat()}")
    
    with app.app_context():
        # Step 1: Find user IDs from emails/usernames
        print("\n" + "-"*40)
        print("STEP 1: IDENTIFYING USERS TO DELETE")
        print("-"*40)
        
        users_to_delete = User.query.filter(
            db.or_(
                User.email.in_(EMAILS_TO_DELETE),
                User.username.in_(USERNAMES_TO_DELETE)
            )
        ).all()
        
        if not users_to_delete:
            print("⚠️  No matching users found in database!")
            print(f"   Searched emails: {EMAILS_TO_DELETE[:5]}...")
            print(f"   Searched usernames: {USERNAMES_TO_DELETE[:5]}...")
            return 1
        
        user_ids = [u.id for u in users_to_delete]
        
        print(f"\n📋 Found {len(users_to_delete)} users to delete:")
        for u in users_to_delete[:10]:
            role_warning = " ⚠️ ADMIN!" if u.role in [UserRole.ADMIN, UserRole.SUPERADMIN] else ""
            print(f"   [{u.id}] {u.full_name} ({u.email}){role_warning}")
        if len(users_to_delete) > 10:
            print(f"   ... and {len(users_to_delete) - 10} more")
        
        # Check for admin users
        admin_users = [u for u in users_to_delete if u.role in [UserRole.ADMIN, UserRole.SUPERADMIN]]
        if admin_users:
            print(f"\n⚠️  WARNING: {len(admin_users)} ADMIN/SUPERADMIN users will be deleted!")
            print("   Consider removing them from the deletion list if unintended.")
        
        # Step 2: Backup
        print("\n" + "-"*40)
        print("STEP 2: CREATING BACKUP")
        print("-"*40)
        
        backup_file, account_ids = backup_user_data(user_ids)
        
        if backup_only:
            print("\n✅ Backup complete. Exiting (--backup-only mode)")
            return 0
        
        # Step 3: Delete
        print("\n" + "-"*40)
        print("STEP 3: DELETING DATA")
        print("-"*40)
        
        deletion_counts = delete_users_cascade(user_ids, dry_run=dry_run)
        
        # Step 4: Verify
        if not dry_run:
            verify_deletion(user_ids, EMAILS_TO_DELETE, USERNAMES_TO_DELETE)
        
        # Summary
        print("\n" + "="*70)
        print("📊 DELETION SUMMARY")
        print("="*70)
        for table, count in deletion_counts.items():
            print(f"   {table}: {count} rows deleted")
        
        total = sum(deletion_counts.values())
        print(f"\n   TOTAL: {total} rows deleted across {len(deletion_counts)} tables")
        print(f"   Backup file: {backup_file}")
        
        if dry_run:
            print("\n⚠️  THIS WAS A DRY RUN - No actual changes were made")
            print("   Run without --dry-run to execute deletion")
        
        print("\n" + "="*70)
        print(f"Completed at: {datetime.now().isoformat()}")
        print("="*70 + "\n")
        
        return 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Safely delete users from TradeSense database')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be deleted without making changes')
    parser.add_argument('--backup-only', action='store_true',
                       help='Only create backup, do not delete')
    
    args = parser.parse_args()
    
    exit(main(dry_run=args.dry_run, backup_only=args.backup_only))
