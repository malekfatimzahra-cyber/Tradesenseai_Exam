"""
TRADESENSE AI - ADMIN ACTIONS LOG BACKFILL SCRIPT
=================================================
This script backfills missing admin action logs for all
accounts that have status changes (PASSED, FAILED, FUNDED)
but no corresponding log entry.

Usage: python backfill_admin_logs.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Account, AdminActionLog, ChallengeStatus, UserRole
from datetime import datetime


def backfill_admin_logs():
    """Backfill missing admin action logs."""
    
    with app.app_context():
        print("\n" + "="*60)
        print("🔧 ADMIN ACTIONS LOG BACKFILL")
        print("="*60)
        
        # Get admin user for backfill attribution
        admin_user = User.query.filter(
            User.role.in_([UserRole.ADMIN, UserRole.SUPERADMIN])
        ).first()
        
        if not admin_user:
            print("⚠️  No admin user found! Creating default admin...")
            admin_user = User(
                full_name="System Admin",
                username="sysadmin",
                email="sysadmin@tradesense.ma",
                role=UserRole.ADMIN
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print(f"  ✅ Created admin user: {admin_user.full_name} ({admin_user.email})")
        
        print(f"\n📋 Using admin: {admin_user.full_name} (ID: {admin_user.id})")
        
        # Get all accounts that need logs (PASSED, FAILED, FUNDED)
        status_needs_log = [ChallengeStatus.PASSED, ChallengeStatus.FAILED, ChallengeStatus.FUNDED]
        
        accounts_needing_log = db.session.query(Account).outerjoin(
            AdminActionLog, AdminActionLog.target_account_id == Account.id
        ).filter(
            Account.status.in_(status_needs_log),
            AdminActionLog.id == None
        ).all()
        
        print(f"\n📊 Found {len(accounts_needing_log)} accounts needing backfill")
        
        created_logs = 0
        
        for account in accounts_needing_log:
            user = User.query.get(account.user_id)
            
            # Determine action based on status
            if account.status == ChallengeStatus.PASSED:
                action = "backfill_set_passed"
                note = f"[Migration Backfill] Challenge passed - log created for audit trail"
            elif account.status == ChallengeStatus.FAILED:
                action = "backfill_set_failed"
                note = f"[Migration Backfill] Challenge failed - log created for audit trail"
            elif account.status == ChallengeStatus.FUNDED:
                action = "backfill_set_funded"
                note = f"[Migration Backfill] Account funded - log created for audit trail"
            else:
                action = "backfill_status_change"
                note = f"[Migration Backfill] Status: {account.status.value}"
            
            # Add reason if available
            if account.reason:
                note += f" | Reason: {account.reason}"
            
            # Add admin note if available
            if account.admin_note:
                note += f" | Admin Note: {account.admin_note}"
            
            log = AdminActionLog(
                admin_id=admin_user.id,
                target_account_id=account.id,
                action=action,
                note=note,
                created_at=account.created_at or datetime.utcnow()
            )
            db.session.add(log)
            created_logs += 1
            
            user_name = user.full_name if user else 'Unknown User'
            print(f"  ✅ {action}: Account #{account.id} ({user_name}) - {account.plan_name}")
        
        db.session.commit()
        
        print(f"\n📊 Summary:")
        print(f"  - Created: {created_logs} new log entries")
        print(f"  - Total logs now: {AdminActionLog.query.count()}")
        
        # Show recent logs
        print(f"\n📋 Recent Admin Logs:")
        print("-" * 60)
        recent_logs = AdminActionLog.query.order_by(
            AdminActionLog.created_at.desc()
        ).limit(10).all()
        
        for log in recent_logs:
            admin_name = log.admin.full_name if log.admin else 'Unknown'
            target_name = 'Unknown'
            if log.target_account and log.target_account.user:
                target_name = log.target_account.user.full_name
            
            print(f"  [{log.created_at.strftime('%Y-%m-%d')}] {admin_name} → {target_name}: {log.action}")
        
        print("\n" + "="*60)
        print("✅ BACKFILL COMPLETE")
        print("="*60 + "\n")
        
        return created_logs


if __name__ == '__main__':
    backfill_admin_logs()
