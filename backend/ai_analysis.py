"""
AI Trading Analysis Module
Provides simulated AI-powered trading signals and analysis
"""
from flask import Blueprint, jsonify
import random
import hashlib
import datetime

ai_analysis_bp = Blueprint('ai_analysis', __name__)

# Helper to generate deterministic "random" seed per symbol
def _seed_from_symbol(symbol: str) -> int:
    """Generate a stable hash from symbol for consistent random results"""
    return int(hashlib.sha256(symbol.encode('utf-8')).hexdigest(), 16) % (2**32)

@ai_analysis_bp.route('/ai-analysis/<symbol>', methods=['GET'])
def get_ai_analysis(symbol: str):
    """
    Simulated AI analysis endpoint.
    Returns comprehensive trading signals and risk assessment.
    
    Response includes:
      - signal: "BUY", "SELL", or "HOLD"
      - confidence: 0-100 percentage
      - entry_price: Current simulated price
      - stop_loss: Risk management level (2% away)
      - take_profit: Profit target (5% away)
      - risk_level: "Low", "Medium", or "High"
      - ai_comment: Explanatory sentence
    """
    
    # We want randomness for "Refresh Analysis" to work, but consistency in generation steps
    # We use random.seed to mix symbol and current time for refreshing
    # If we wanted strict consistency per symbol we would remove the time variance
    seed_value = _seed_from_symbol(symbol)
    random.seed(seed_value + int(random.random() * 10000))
    
    # ------------------------------------------------------------------
    # 1. Simulate current price (in production, fetch from market data)
    # ------------------------------------------------------------------
    entry_price = round(random.uniform(50, 500), 2)
    
    # ------------------------------------------------------------------
    # 2. Determine signal & confidence
    # ------------------------------------------------------------------
    signal_choices = ['BUY', 'SELL', 'HOLD']
    weights = [0.4, 0.35, 0.25]  # Slight bias toward action
    signal = random.choices(signal_choices, weights=weights)[0]
    
    # Higher confidence for clearer signals
    if signal == 'HOLD':
        confidence = random.randint(60, 80)
    else:
        confidence = random.randint(70, 95)
    
    # ------------------------------------------------------------------
    # 3. Calculate stop-loss and take-profit based on direction
    # ------------------------------------------------------------------
    if signal == 'BUY':
        stop_loss = round(entry_price * 0.98, 2)    # 2% below entry
        take_profit = round(entry_price * 1.05, 2)  # 5% above entry
    elif signal == 'SELL':
        stop_loss = round(entry_price * 1.02, 2)    # 2% above entry
        take_profit = round(entry_price * 0.95, 2)  # 5% below entry
    else:  # HOLD
        stop_loss = round(entry_price * 0.99, 2)
        take_profit = round(entry_price * 1.01, 2)
    
    # ------------------------------------------------------------------
    # 4. Determine risk level based on confidence and volatility
    # ------------------------------------------------------------------
    if confidence >= 85:
        risk_level = 'Low'
    elif confidence >= 75:
        risk_level = 'Medium'
    else:
        risk_level = 'High'
    
    # Add volatility factor
    if signal != 'HOLD' and random.random() > 0.7:
        risk_level = 'Medium' if risk_level == 'Low' else 'High'
    
    # ------------------------------------------------------------------
    # 5. Generate contextual AI comment
    # ------------------------------------------------------------------
    buy_comments = [
        "Bullish divergence detected on RSI indicator.",
        "Golden cross formation on moving averages.",
        "Strong support level holding with volume spike.",
        "Breakout above key resistance with momentum.",
        "Institutional buying detected in order flow.",
        "Positive correlation with sector leaders.",
    ]
    
    sell_comments = [
        "Bearish engulfing pattern on the 5-min chart.",
        "Death cross forming on moving averages.",
        "Resistance rejection with weakening volume.",
        "Overbought conditions on multiple timeframes.",
        "Distribution pattern detected in smart money flow.",
        "Negative divergence on momentum indicators.",
    ]
    
    hold_comments = [
        "Market sentiment is neutral; consider waiting.",
        "Sideways consolidation pattern detected.",
        "Mixed signals across technical indicators.",
        "Low volume suggests waiting for confirmation.",
        "Range-bound price action without clear direction.",
        "Awaiting catalyst for directional move.",
    ]
    
    if signal == 'BUY':
        ai_comment = random.choice(buy_comments)
    elif signal == 'SELL':
        ai_comment = random.choice(sell_comments)
    else:
        ai_comment = random.choice(hold_comments)
    
    # ------------------------------------------------------------------
    # 6. Build and return response
    # ------------------------------------------------------------------
    response = {
        "symbol": symbol.upper(),
        "signal": signal,
        "confidence": confidence,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_level": risk_level,
        "ai_comment": ai_comment,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return jsonify(response), 200
