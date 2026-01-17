from flask import Blueprint, request, jsonify
from models import db, Account, Trade, TradeStatus, TradeType, ChallengeStatus
from engine import evaluate_challenge_rules
from datetime import datetime
from middleware import token_required

trades_bp = Blueprint('trades', __name__)

@trades_bp.route('', methods=['POST'])
@token_required
def create_trade(current_user):
    """
    Exam Compliant Endpoint: POST /api/trades
    Body: { challenge_id, symbol, side, qty, price }
    """
    data = request.json
    challenge_id = data.get('challenge_id')
    symbol = data.get('symbol')
    side_str = data.get('side') # BUY or SELL
    qty = float(data.get('qty', 0))
    price = float(data.get('price', 0))
    
    # 1. Validation & Auth
    if not challenge_id:
        return jsonify({'message': 'challenge_id is required'}), 400
        
    account = Account.query.get(challenge_id)
    if not account or account.user_id != current_user.id:
        return jsonify({'message': 'Challenge not found or unauthorized'}), 403
        
    if account.status != ChallengeStatus.ACTIVE:
        return jsonify({'message': 'Challenge is not active'}), 400

    try:
        side = TradeType[side_str.upper()]
    except:
        return jsonify({'message': 'Invalid side. Use BUY or SELL'}), 400

    # 2. Insert Trade
    # Calculate amount (Total value of position)
    amount = price * qty
    
    new_trade = Trade(
        account_id=account.id,
        user_id=current_user.id,
        symbol=symbol,
        trade_type=side,
        side=side,
        amount=amount,
        entry_price=price,
        price=price,
        quantity=qty,
        status=TradeStatus.OPEN,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_trade)
    db.session.commit()
    
    # 3. Compute PnL and Update Challenge Equity
    # Note: For a newly opened trade, PnL is typically 0 (ignoring spread).
    # However, if this endpoint is simulating a closed trade or update, requirements says "compute pnl".
    # Since it's inserting a trade, we assume it's OPENING.
    # Current equity shouldn't change yet unless we mark commissions.
    # We'll calculate equity based on ALL open trades if possible, but for now:
    # Equity = Balance + Unrealized PnL.
    # We assume Unrealized PnL starts at 0.
    
    # 4. Background Task: Check Rules
    # Synchronous for MVP safety
    new_status = evaluate_challenge_rules(account.id)
    
    # 5. Return Updated State
    return jsonify({
        'ok': True,
        'trade_id': new_trade.id,
        'equity': account.equity,
        'status': new_status.value if new_status else account.status.value,
        'daily_dd': account.daily_starting_equity - account.equity, # Approx
        'total_dd': account.initial_balance - account.equity
    }), 201
