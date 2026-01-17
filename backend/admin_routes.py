from flask import Blueprint, jsonify, request
from models import db, User, Account, ChallengeStatus, UserRole, AdminActionLog
from middleware import token_required
from sqlalchemy import or_
import traceback

admin_bp = Blueprint('admin', __name__)

def check_admin_role(user):
    return user.role in [UserRole.ADMIN, UserRole.SUPERADMIN]

@admin_bp.route('/overview', methods=['GET'])
@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    try:
        # 1. Check Admin Key
        if request.headers.get('X-ADMIN-KEY') == 'TRADESENSE_SUPER_SECRET_2026':
            # Success - proceed
            pass
        else:
            # 2. Check Token (Simplified manual check)
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]
            
            if not token:
                 return jsonify({'message': 'Unauthorized'}), 403
            
            # If token is present but Key is missing, treat as Unauthorized for this critical endpoint
            return jsonify({'message': 'Unauthorized (Key Required)'}), 403

        total_users = User.query.count()
        active_challenges = Account.query.filter_by(status=ChallengeStatus.ACTIVE).count()
        passed_challenges = Account.query.filter_by(status=ChallengeStatus.PASSED).count()
        failed_challenges = Account.query.filter_by(status=ChallengeStatus.FAILED).count()
        
        # Get recent admin logs
        from models import AdminActionLog
        recent_logs = []
        logs = AdminActionLog.query.order_by(AdminActionLog.created_at.desc()).limit(10).all()
        for log in logs:
            recent_logs.append({
                'id': log.id,
                'admin': log.admin.full_name if log.admin else 'Unknown',
                'target': log.target_account.user.username if log.target_account and log.target_account.user else 'Deleted',
                'action': log.action,
                'time': log.created_at.isoformat()
            })

        return jsonify({
            'total_users': total_users,
            'active_challenges': active_challenges,
            'passed_challenges': passed_challenges,
            'failed_challenges': failed_challenges,
            'recent_logs': recent_logs
        })

    except Exception as e:
        print(f"CRITICAL ERROR in /admin/dashboard: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500

@admin_bp.route('/challenges', methods=['GET'])
def get_challenges():
    try:
        # 1. Check Admin Key
        if request.headers.get('X-ADMIN-KEY') == 'TRADESENSE_SUPER_SECRET_2026':
            pass
        else:
            return jsonify({'message': 'Unauthorized'}), 403
            
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        status_filter = request.args.get('status', 'All')

        query = db.session.query(Account, User).join(User, Account.user_id == User.id)

        # Search filter
        if search:
            search = f"%{search}%"
            query = query.filter(or_(
                User.full_name.ilike(search), 
                User.email.ilike(search)
            ))

        # Status filter
        if status_filter != 'All' and status_filter != 'ALL':
            try:
                status_enum = ChallengeStatus[status_filter.upper()]
                query = query.filter(Account.status == status_enum)
            except KeyError:
                pass # Ignore invalid status
                
        # Ordering
        query = query.order_by(Account.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        results = []
        for acc, user in pagination.items:
            profit = acc.equity - acc.initial_balance
            results.append({
                'challenge_id': acc.id,
                'user_name': user.full_name,
                'user_email': user.email,
                'user_avatar': None, 
                'plan': acc.plan_name,
                'equity': acc.equity,
                'profit_loss': profit,
                'status': acc.status.value,
                'created_at': acc.created_at.isoformat()
            })
            
        return jsonify({
            'challenges': results,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })

    except Exception as e:
        print(f"CRITICAL ERROR in /admin/challenges: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500

@admin_bp.route('/challenges/<int:id>/status', methods=['PATCH'])
def update_challenge_status(id):
    try:
        # 1. Check Admin Key
        if request.headers.get('X-ADMIN-KEY') != 'TRADESENSE_SUPER_SECRET_2026':
             return jsonify({'message': 'Unauthorized'}), 403
            
        data = request.json
        if not data:
             return jsonify({'message': 'No JSON payload provided'}), 400

        new_status_str = data.get('status')
        if not new_status_str:
            return jsonify({'message': 'No status provided'}), 400

        account = Account.query.get(id)
        if not account:
            return jsonify({'message': 'Challenge not found'}), 404
            
        try:
            new_status = ChallengeStatus[new_status_str.upper()]
        except KeyError:
            return jsonify({'message': f'Invalid status: {new_status_str}'}), 400

        # Update Logic
        old_status = account.status.value
        print(f"Updating Challenge #{id} status from {old_status} to {new_status.value}")
        account.status = new_status
        
        # Log Admin Action
        from models import AdminActionLog
        admin_user = User.query.filter_by(role=UserRole.ADMIN).first()
        admin_id = admin_user.id if admin_user else 1 # Fallback
        
        log = AdminActionLog(
            admin_id=admin_id,
            target_account_id=account.id,
            action=f"status_change_{new_status.value.lower()}",
            note=f"Changed status from {old_status} to {new_status.value}"
        )
        db.session.add(log)
        
        db.session.add(account)
        
        # --- Recalculate Leaderboard Cache ---
        # If user failed, remove from leaderboard
        # If user passed/funded, they might need to be added or updated? 
        # For simplicity: If FAILED, remove. If Active/Passed, we assume the scheduled sync or next trade handles it.
        # But to be "instant", we can try to update visibility.
        from models import Leaderboard
        if new_status == ChallengeStatus.FAILED:
            Leaderboard.query.filter_by(account_id=account.id).delete()
            print(f"Removed Account {account.id} from Leaderboard")
            
        elif new_status in [ChallengeStatus.PASSED, ChallengeStatus.FUNDED]:
            # Optional: We could trigger a sync here, but for now we settle on removing failures.
            pass
            
        db.session.commit()
        
        print(f"SUCCESS: Challenge #{id} updated.")
        
        return jsonify({
            'message': f'Challenge updated to {new_status.value}',
            'status': new_status.value
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL ERROR in update_challenge_status: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Database Error: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'])
def get_users_admin():
    try:
        # Admin Key Check matching Frontend
        admin_key = request.headers.get('X-ADMIN-KEY')
        if admin_key != 'TRADESENSE_SUPER_SECRET_2026': 
             return jsonify({'message': 'Unauthorized'}), 403

        users = User.query.all()
        user_data = []
        
        for user in users:
            challenges = []
            for acc in user.accounts:
                profit = acc.equity - acc.initial_balance
                profit_percent = (profit / acc.initial_balance * 100) if acc.initial_balance > 0 else 0
                challenges.append({
                    'id': acc.id,
                    'plan': acc.plan_name,
                    'start_balance': acc.initial_balance,
                    'equity': acc.equity,
                    'profit_percent': round(profit_percent, 2),
                    'status': acc.status.value,
                    'created_at': acc.created_at.isoformat(),
                    'admin_note': acc.admin_note,
                    'reason': acc.reason
                })
                
            user_data.append({
                'user_id': user.id,
                'name': user.full_name,
                'email': user.email,
                'role': user.role.value,
                'joined_at': user.created_at.isoformat(),
                'challenges': challenges
            })
            
        return jsonify(user_data)

    except Exception as e:
        print(f"CRITICAL ERROR in /admin/users: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500

# --- LEADERBOARD MANAGEMENT ---

@admin_bp.route('/leaderboard', methods=['GET'])
def get_admin_leaderboard():
    try:
        if request.headers.get('X-ADMIN-KEY') != 'TRADESENSE_SUPER_SECRET_2026':
             return jsonify({'message': 'Unauthorized'}), 403
             
        from models import Leaderboard
        entries = Leaderboard.query.order_by(Leaderboard.ranking.asc()).all()
        return jsonify([entry.to_dict() for entry in entries])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@admin_bp.route('/leaderboard/sync', methods=['POST'])
def sync_leaderboard_endpoint():
    try:
        if request.headers.get('X-ADMIN-KEY') != 'TRADESENSE_SUPER_SECRET_2026':
             return jsonify({'message': 'Unauthorized'}), 403
             
        from models import Leaderboard
        from datetime import datetime, timedelta
        
        # 1. Clear current Leaderboard for clean sync
        db.session.query(Leaderboard).delete()
        
        # 2. Re-calculate from Active Accounts
        accounts = Account.query.filter(Account.status.in_([ChallengeStatus.ACTIVE, ChallengeStatus.PASSED, ChallengeStatus.FUNDED])).all()
        
        candidates = []
        for acc in accounts:
            profit = acc.equity - acc.initial_balance
            if profit <= 0: continue
            
            roi = (profit / acc.initial_balance) * 100 if acc.initial_balance > 0 else 0
            
            wins = sum(1 for t in acc.trades if t.pnl > 0 and t.status.value == 'CLOSED')
            total = sum(1 for t in acc.trades if t.status.value == 'CLOSED')
            win_rate = (wins / total * 100) if total > 0 else 0
            
            country = 'MA'
            # Fallback random country logic if needed, or stick to MA
            
            candidates.append({
                'user_id': acc.user_id,
                'username': acc.user.username,
                'profit': profit,
                'roi': roi,
                'win_rate': win_rate,
                'funded': acc.initial_balance,
                'avatar': f"https://ui-avatars.com/api/?name={acc.user.full_name}&background=random",
                'country': country
            })
            
        candidates.sort(key=lambda x: x['profit'], reverse=True)
        
        for i, c in enumerate(candidates[:50]): # Keep Top 50
            entry = Leaderboard(
                user_id=c['user_id'],
                username=c['username'],
                country=c['country'], # Default MA
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
            
        db.session.commit()
        return jsonify({'message': 'Leaderboard Synced Successfully', 'count': len(candidates[:50])})
        
    except Exception as e:
        db.session.rollback()
        print(f"Sync Error: {e}")
        return jsonify({'message': str(e)}), 500
