from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import yfinance as yf
from models import db, MarketSignal, RiskAlert, Account, Trade, TradeStatus, User
from middleware import token_required
from datetime import datetime

ai_agency_bp = Blueprint('ai_agency', __name__)

def get_gemini_model():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

@ai_agency_bp.route('/signals', methods=['GET'])
@token_required
def get_ai_signals(current_user):
    asset = request.args.get('asset', 'BTC-USD')
    # Fetch last 3 signals for this asset
    signals = MarketSignal.query.filter_by(asset=asset).order_by(MarketSignal.created_at.desc()).limit(3).all()
    
    # If no signals or old signals (older than 1 hour), generate a new one
    if not signals or (datetime.utcnow() - signals[0].created_at).total_seconds() > 3600:
        model = get_gemini_model()
        if model:
            try:
                ticker = yf.Ticker(asset)
                hist = ticker.history(period="5d", interval="1h")
                price = ticker.info.get('regularMarketPrice', hist['Close'].iloc[-1])
                
                context = f"Asset: {asset}. Current Price: {price}. Last 48h data: {hist['Close'].tail(48).tolist()}"
                
                prompt = f"""
                Act as TradeSense AI, an elite Prop Firm Trading Bot.
                Market Data: {context}
                
                Generate a high-probability trade signal.
                Return ONLY a JSON object with:
                type: "BUY" or "SELL"
                entry: current price or slightly better
                sl: logical stop loss
                tp: target with at least 1:2 RR
                confidence: 0-100
                quality: "HIGH", "MEDIUM", or "LOW"
                reasoning: 1 sentence on why
                """
                
                response = model.generate_content(prompt)
                import json
                import re
                
                # Extract JSON from response
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if match:
                    res_json = json.loads(match.group())
                    new_sig = MarketSignal(
                        asset=asset,
                        signal_type=res_json['type'],
                        confidence=res_json['confidence'],
                        entry_price=res_json['entry'],
                        stop_loss=res_json['sl'],
                        take_profit=res_json['tp'],
                        reasoning=res_json['reasoning'],
                        quality=res_json['quality']
                    )
                    db.session.add(new_sig)
                    db.session.commit()
                    signals = [new_sig]
            except Exception as e:
                print(f"AI Signal Error: {e}")
                
    return jsonify([s.to_dict() for s in signals])

@ai_agency_bp.route('/trade-plan', methods=['GET'])
@token_required
def get_trade_plan(current_user):
    asset = request.args.get('asset', 'BTC-USD')
    model = get_gemini_model()
    if not model:
        return jsonify({'message': 'AI service unavailable'}), 503
        
    try:
        ticker = yf.Ticker(asset)
        info = ticker.info
        
        prompt = f"""
        Asset: {asset}. Generate a Professional Trade Plan for the current session.
        Include:
        1. Market Bias (Bullish/Bearish/Neutral)
        2. Key Structural Levels (Support/Resistance)
        3. Risk Note for Prop Firm Traders (Max drawdown focus)
        4. Session Strategy (NY/London focus)
        
        Format as clear sections.
        """
        response = model.generate_content(prompt)
        return jsonify({'plan': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_agency_bp.route('/risk-check', methods=['GET'])
@token_required
def run_risk_check(current_user):
    # Analyze user's active trades and account to generate alerts
    account = Account.query.filter_by(user_id=current_user.id).first()
    if not account:
        return jsonify({'alerts': [], 'risk_level': 'SAFE'})
        
    alerts = []
    risk_level = 'SAFE'
    
    # 1. Check for high open risk
    active_trades = Trade.query.filter_by(account_id=account.id, status=TradeStatus.OPEN).all()
    open_pnl = sum([t.pnl or 0 for t in active_trades]) # This is mocked usually, would need live prices
    
    # 2. Check for daily loss proximity
    daily_drawdown = account.daily_starting_equity - account.equity
    if daily_drawdown > account.initial_balance * 0.03:
        risk_level = 'WARNING'
        alerts.append({
            'type': 'DRAWDOWN',
            'severity': 'WARNING',
            'message': "Approaching 4% Daily Loss Limit. Exercise extreme caution."
        })
    elif daily_drawdown > account.initial_balance * 0.045:
        risk_level = 'DANGER'
        alerts.append({
            'type': 'DRAWDOWN',
            'severity': 'DANGER',
            'message': "CRITICAL: 0.5% away from Daily Hard-Stop. Closing all positions recommended."
        })
        
    # 3. Check for news (mocked for now)
    # In a real app, query a news API
    
    return jsonify({
        'alerts': alerts,
        'risk_level': risk_level,
        'equity_shield': max(0, (1 - (daily_drawdown / (account.initial_balance * 0.05))) * 100)
    })

@ai_agency_bp.route('/validate-trade', methods=['POST'])
@token_required
def validate_trade(current_user):
    data = request.json
    asset = data.get('asset')
    side = data.get('type')
    amount = float(data.get('amount', 0))
    entry = float(data.get('entry', 0))
    
    account = Account.query.filter_by(user_id=current_user.id).first()
    if not account:
        return jsonify({'status': 'APPROVED', 'message': 'Simulation Mode'})

    model = get_gemini_model()
    if not model:
        # Fallback logic if AI offline
        daily_loss = account.daily_starting_equity - account.equity
        if daily_loss > account.initial_balance * 0.04:
             return jsonify({'status': 'BLOCKED', 'message': 'Daily Loss Limit Approaching (Hard Rule)'})
        return jsonify({'status': 'APPROVED', 'message': 'AI Offline - Standard Risk Rules Apply'})
        
    # Context for AI
    risk_pct = (amount / account.equity) * 100
    daily_drawdown_pct = ((account.daily_starting_equity - account.equity) / account.initial_balance) * 100
    
    prompt = f"""
    Role: Chief Risk Officer for an Elite Prop Firm.
    Task: Validate this trade proposal. Strict rules apply.
    
    Trader Context:
    - Equity: ${account.equity:.2f}
    - Proposed Trade Risk: ${amount:.2f} ({risk_pct:.2f}% of equity)
    - Current Daily Drawdown: {daily_drawdown_pct:.2f}% (Max allowed: 5%)
    - Asset: {asset} ({side} @ {entry})
    
    Validation Rules:
    1. BLOCK if Daily Drawdown > 4.5%.
    2. WARN if Trade Risk > 2% of equity.
    3. WARN if trying to catch a falling knife (e.g. buying after huge drop) - assume standard volatility.
    4. APPROVE if standard parameters.
    
    Response JSON ONLY:
    {{
        "status": "APPROVED" | "WARNING" | "BLOCKED",
        "message": "Concise, professional explanation (max 10 words)."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        import json
        text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        return jsonify(result)
    except Exception as e:
        print(f"Validation Error: {e}")
        return jsonify({'status': 'APPROVED', 'message': 'System Bypass'})

@ai_agency_bp.route('/explain-price-action', methods=['POST'])
@token_required
def explain_price_action(current_user):
    data = request.json
    asset = data.get('asset', 'BTC-USD')
    change = data.get('change', 0)
    price = data.get('price', 0)
    
    model = get_gemini_model()
    if not model:
        return jsonify({'explanation': 'AI currently offline. Market volatility detected.'})
        
    prompt = f"""
    Role: Institutional Market Analyst.
    Task: Explain the current immediate price action for {asset}.
    Context: Price: ${price}, Daily Change: {change}%.
    
    Output: A single, dense, professional paragraph (max 40 words). No fluff. Focus on order flow, volatility, and key reaction levels. 
    Use terms like "liquidity grab", "consolidation", "impulsive move", "rejection".
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({'explanation': response.text})
    except Exception as e:
        return jsonify({'explanation': 'Analysis unavailable.'})
