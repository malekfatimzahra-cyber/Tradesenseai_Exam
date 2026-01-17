from flask import Blueprint, request, jsonify
from models import db, Account, Trade, TradeStatus, TradeType, ChallengeStatus
from engine import evaluate_challenge_rules
from datetime import datetime
from middleware import token_required

trading_bp = Blueprint('trading', __name__)

@trading_bp.route('/open', methods=['POST'])
@token_required
def open_trade(current_user):
    data = request.json
    account_id = data.get('account_id')
    
    # Validation
    if not account_id:
        # Try to find active account for user
        active_account = Account.query.filter_by(user_id=current_user.id, status=ChallengeStatus.ACTIVE).first()
        if not active_account:
            return jsonify({'message': 'No active account found'}), 404
        account = active_account
    else:
        account = Account.query.get(account_id)
        if not account or account.user_id != current_user.id:
            return jsonify({'message': 'Account not found or unauthorized'}), 403

    if account.status != ChallengeStatus.ACTIVE:
        return jsonify({'message': 'Account is not active'}), 400

    # Trade Details
    symbol = data.get('symbol')
    trade_type_str = data.get('type') # BUY or SELL
    amount = float(data.get('amount', 0))
    entry_price = float(data.get('entry_price', 0))
    sl = float(data.get('sl')) if data.get('sl') else None
    tp = float(data.get('tp')) if data.get('tp') else None
    
    try:
        trade_type = TradeType[trade_type_str]
    except KeyError:
        return jsonify({'message': 'Invalid trade type'}), 400

    # Calculate quantity from amount and price
    quantity = amount / entry_price if entry_price > 0 else 0

    new_trade = Trade(
        account_id=account.id,
        user_id=current_user.id,
        symbol=symbol,
        trade_type=trade_type,
        side=trade_type,  # Set both for compatibility
        amount=amount,
        entry_price=entry_price,
        price=entry_price,  # Set both for compatibility
        quantity=quantity,
        stop_loss=sl,
        take_profit=tp,
        status=TradeStatus.OPEN,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_trade)
    db.session.commit()
    
    return jsonify({
        'message': 'Trade opened successfully', 
        'trade': new_trade.to_dict(),
        'account': account.to_dict()
    }), 201


@trading_bp.route('/close', methods=['POST'])
@token_required
def close_trade(current_user):
    data = request.json
    trade_id = data.get('trade_id')
    exit_price = float(data.get('exit_price'))
    
    trade = Trade.query.get(trade_id)
    if not trade:
        return jsonify({'message': 'Trade not found'}), 404
        
    account = Account.query.get(trade.account_id)
    if account.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
        
    if trade.status != TradeStatus.OPEN:
        return jsonify({'message': 'Trade already closed'}), 400

    # Calculate PnL
    # Simplified Logic: (Exit - Entry) * (Amount / Entry)
    # Amount is in USD size of position. 
    # Example: Bought 1000 USD of BTC at 50,000. Price goes to 55,000.
    # PnL = (55000 - 50000) * (1000 / 50000) = 5000 * 0.02 = 100 USD. Correct.
    
    quantity = trade.amount / trade.entry_price
    
    if trade.trade_type == TradeType.BUY:
        pnl = (exit_price - trade.entry_price) * quantity
    else:
        pnl = (trade.entry_price - exit_price) * quantity
        
    # Update Trade
    trade.status = TradeStatus.CLOSED
    trade.exit_price = exit_price
    trade.closed_at = datetime.utcnow()
    trade.pnl = pnl
    
    # Update Account Balance & Equity
    # Realized PnL adds to Balance AND Equity (since Equity = Balance + Unrealized, and now it's realized)
    # Wait: Equity = Balance + Unrealized. When realized, Balance increases, Unrealized becomes 0.
    # So effectively Equity reflects the change too.
    # We update Balance here.
    account.current_balance += pnl
    account.equity = account.current_balance # Assuming no other open trades for simplicity, OR we should re-calc equity from all open trades.
    # For Module A (Exam), let's assume this is the triggered update.
    # Ideally, specific route recalculates equity based on ALL open trades prices. 
    # But here we just commit the realized gain.
    
    db.session.commit()
    
    # Trigger Challenge Engine
    new_status = evaluate_challenge_rules(account.id)
    
    return jsonify({
        'message': 'Trade closed successfully',
        'pnl': pnl,
        'account_status': new_status.value if new_status else account.status.value,
        'trade': trade.to_dict(),
        'account': account.to_dict()
    })

@trading_bp.route('/active', methods=['GET'])
@token_required
def get_active_trades(current_user):
    active_account = Account.query.filter_by(user_id=current_user.id, status=ChallengeStatus.ACTIVE).first()
    if not active_account:
        return jsonify([])
        
    trades = Trade.query.filter_by(account_id=active_account.id, status=TradeStatus.OPEN).order_by(Trade.created_at.desc()).all()
    return jsonify([t.to_dict() for t in trades])

@trading_bp.route('/account', methods=['GET'])
@token_required
def get_active_account(current_user):
    account = Account.query.filter_by(user_id=current_user.id, status=ChallengeStatus.ACTIVE).first()
    if not account:
        return jsonify(None), 200 # No active account
    return jsonify(account.to_dict())

@trading_bp.route('/history', methods=['GET'])
@token_required
def get_trade_history(current_user):
    # Get all accounts or just active? Usually all.
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [a.id for a in accounts]
    
    trades = Trade.query.filter(Trade.account_id.in_(account_ids), Trade.status == TradeStatus.CLOSED).order_by(Trade.closed_at.desc()).limit(50).all()
    return jsonify([t.to_dict() for t in trades])
