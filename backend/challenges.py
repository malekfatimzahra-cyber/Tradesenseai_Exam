from flask import Blueprint, request, jsonify
from models import db, Account, ChallengeStatus, Trade, TradeStatus
from middleware import token_required
from sqlalchemy import desc


challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/plans', methods=['GET'])
def get_challenge_plans():
    """
    Get all active challenge plans.
    Public endpoint.
    """
    try:
        from models import ChallengePlan
        plans = ChallengePlan.query.filter_by(is_active=True).all()
        return jsonify({
            'ok': True,
            'data': [p.to_dict() for p in plans]
        }), 200
    except Exception as e:
         return jsonify({'ok': False, 'message': str(e)}), 500


@challenges_bp.route('/active', methods=['GET'])
@token_required
def get_active_challenge(current_user):
    """
    Get the active challenge for the current user.
    Returns the challenge with status='ACTIVE', or null if none exists.
    """
    try:
        # Find the most recent ACTIVE account for this user
        active_account = Account.query.filter_by(
            user_id=current_user.id,
            status=ChallengeStatus.ACTIVE
        ).order_by(desc(Account.created_at)).first()
        
        if not active_account:
            return jsonify({
                'ok': True,
                'data': None,
                'message': 'No active challenge found'
            }), 200
        
        # Get active trades count
        active_trades = Trade.query.filter_by(
            account_id=active_account.id,
            status=TradeStatus.OPEN
        ).count()
        
        # Return challenge data
        return jsonify({
            'ok': True,
            'data': {
                'id': active_account.id,
                'plan_name': active_account.plan_name,
                'initial_balance': active_account.initial_balance,
                'current_balance': active_account.current_balance,
                'equity': active_account.equity,
                'daily_starting_equity': active_account.daily_starting_equity,
                'status': active_account.status.value,
                'daily_pnl': active_account.equity - active_account.daily_starting_equity,
                'total_pnl': active_account.equity - active_account.initial_balance,
                'active_trades_count': active_trades,
                'created_at': active_account.created_at.isoformat(),
                'reason': active_account.reason
            }
        }), 200
        
    except Exception as e:
        print(f"Error fetching active challenge: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'ok': False,
            'message': f'Error fetching active challenge: {str(e)}'
        }), 500


@challenges_bp.route('', methods=['GET'])
@challenges_bp.route('/', methods=['GET'])
@token_required
def get_all_challenges(current_user):
    """
    Get ALL challenges for the current user (active, passed, failed, pending).
    """
    try:
        accounts = Account.query.filter_by(
            user_id=current_user.id
        ).order_by(desc(Account.created_at)).all()
        
        challenges = []
        for account in accounts:
            challenges.append({
                'id': account.id,
                'plan_name': account.plan_name,
                'initial_balance': account.initial_balance,
                'current_balance': account.current_balance,
                'equity': account.equity,
                'status': account.status.value,
                'daily_pnl': account.equity - account.daily_starting_equity,
                'total_pnl': account.equity - account.initial_balance,
                'created_at': account.created_at.isoformat(),
                'reason': account.reason
            })
        
        return jsonify({
            'ok': True,
            'data': challenges
        }), 200
        
    except Exception as e:
        print(f"Error fetching challenges: {str(e)}")
        return jsonify({
            'ok': False,
            'message': f'Error: {str(e)}'
        }), 500


@challenges_bp.route('/<int:challenge_id>', methods=['GET'])
@token_required
def get_challenge_by_id(current_user, challenge_id):
    """
    Get a specific challenge by ID.
    Only returns if it belongs to the current user.
    """
    try:
        account = Account.query.filter_by(
            id=challenge_id,
            user_id=current_user.id
        ).first()
        
        if not account:
            return jsonify({
                'ok': False,
                'message': 'Challenge not found or access denied'
            }), 404
        
        # Get trades for this challenge
        trades = Trade.query.filter_by(account_id=account.id).all()
        
        return jsonify({
            'ok': True,
            'data': {
                'id': account.id,
                'plan_name': account.plan_name,
                'initial_balance': account.initial_balance,
                'current_balance': account.current_balance,
                'equity': account.equity,
                'daily_starting_equity': account.daily_starting_equity,
                'status': account.status.value,
                'daily_pnl': account.equity - account.daily_starting_equity,
                'total_pnl': account.equity - account.initial_balance,
                'created_at': account.created_at.isoformat(),
                'reason': account.reason,
                'trades': [t.to_dict() for t in trades]
            }
        }), 200
        
    except Exception as e:
        print(f"Error fetching challenge: {str(e)}")
        return jsonify({
            'ok': False,
            'message': f'Error: {str(e)}'
        }), 500
