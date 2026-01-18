
from app import app
from models import db, Module, Quiz, Question, Option, QuestionTranslation, OptionTranslation, QuizTranslation
import random

# ==========================================
# QUIZ CONTENT GENERATOR (REALISTIC)
# ==========================================

QUIZ_DATA = {
    # KEYWORDS to match Module Title -> Questions list
    "market": [
        ("What defines a Bull Market?", ["Higher Highs & Higher Lows", "Lower Highs & Lower Lows", "Flat price action", "High Volatility"], 0),
        ("Which session has the most volume?", ["London & New York Overlap", "Asian Session", "Sydney Session", "Sunday Open"], 0),
        ("What is the 'Spread'?", ["Difference between Bid and Ask", "The commission fee", "The swap rate", "The profit margin"], 0),
        ("What is a 'Lot' size?", ["Standardized quantity of currency", "The leverage ratio", "The profit target", "The number of trades"], 0),
        ("Who is a market maker?", ["Institution providing liquidity", "A retail trader", "A signal provider", "A news agency"], 0),
        ("What moves the market the most?", ["Central Bank Interest Rates", "Twitter sentiment", "Chart patterns", "Fibonacci levels"], 0),
        ("When is the market most volatile?", ["During High Impact News", "During lunch time", "On weekends", "During Asian session"], 0),
        ("What is 'Slippage'?", ["Execution at a different price than ordered", "Falling asleep while trading", "Losing money", "A technical indicator"], 0)
    ],
    "fundamental": [
        ("What does GDP measure?", ["Total economic output of a country", "Total debt of a country", "Total tax revenue", "Total trade balance"], 0),
        ("If Inflation rises, what do Central Banks usually do?", ["Raise Interest Rates", "Lower Interest Rates", "Print more money", "Ignore it"], 0),
        ("What is NFP (Non-Farm Payrolls)?", ["US Employment Report", "Agricultural output", "European Interest Rate", "Asian GDP"], 0),
        ("High Interest Rates usually make a currency...", ["Stronger", "Weaker", "Neutral", "Volatile"], 0),
        ("What is a 'Safe Haven' asset?", ["Gold", "Bitcoin", "Tesla Stock", "Emerging Market Currencies"], 0),
        ("What represents a 'Hawkish' stance?", ["Favoring higher interest rates", "Favoring lower interest rates", "Neutral stance", "Printing money"], 0),
        ("Which pair is most affected by Oil prices?", ["USD/CAD", "EUR/USD", "GBP/JPY", "AUD/NZD"], 0),
        ("The Economic Calendar is used to...", ["Anticipate volatility events", "Draw support levels", "Calculate lot size", "Open account"], 0)
    ],
    "candlestick": [
        ("What does a Doji signify?", ["Indecision/Potential Reversal", "Strong Trend", "High Volatility", "Market Closure"], 0),
        ("What makes an Engulfing Pattern valid?", ["Body fully covers previous candle body", "Wick covers previous wick", "It is green", "It is red"], 0),
        ("A Pinbar at resistance suggests...", ["Rejection/Reversal down", "Breakout up", "Continuation", "Nothing"], 0),
        ("Which timeframe is most reliable for patterns?", ["Daily/H4", "1 Minute", "5 Seconds", "Tick chart"], 0),
        ("Three White Soldiers is a...", ["Bullish Reversal Pattern", "Bearish Pattern", "Neutral Pattern", "Crypto term"], 0),
        ("A 'Hammer' candle is found...", ["At the bottom of a downtrend", "At the top of an uptrend", "In a sideways market", "Anywhere"], 0),
        ("What does a long upper wick indicate?", ["Selling pressure", "Buying pressure", "No pressure", "Low volume"], 0),
        ("Inside Bar represents...", ["Consolidation/Pause", "Reversal", "Crash", "Rally"], 0)
    ],
    "structure": [
        ("What is a BOS?", ["Break of Structure", "Break of Support", "Buy or Sell", "Base of Supply"], 0),
        ("What defines an Uptrend?", ["HH + HL", "LH + LL", "Flat Highs", "Flat Lows"], 0),
        ("What is a CHoCH?", ["Change of Character (Reversal)", "Change of Chart", "Channel of Change", "Choice of Challenge"], 0),
        ("Swing High is...", ["A high surrounded by lower highs", "The highest point of the year", "A moving average", "A gap"], 0),
        ("Internal Structure is...", ["Price action between swing points", "The daily timeframe", "The weekly timeframe", "Volume profile"], 0),
        ("Strong Low is expected to...", ["Hold price", "Break", "Be swept", "Be ignored"], 0),
        ("Premium vs Discount refers to...", ["Fibonacci zones >50% and <50%", "Commissions", "Swap rates", "Broker spreads"], 0),
        ("Trend is your friend until...", ["It bends (Reversal)", "You lose money", "Friday close", "News event"], 0)
    ],
    "risk": [
        ("Max risk per trade recommendation?", ["1-2%", "10%", "50%", "All in"], 0),
        ("What is Risk to Reward (RR)?", ["Potential Profit vs Potential Loss", "Win rate", "Leverage", "Lot size"], 0),
        ("If I lose 50%, I need to make ___ to recover?", ["100%", "50%", "25%", "10%"], 0),
        ("Where should Stop Loss be placed?", ["Invalidation level", "Random 10 pips", "Where I feel pain", "No Stop Loss"], 0),
        ("What is 'Over-leveraging'?", ["Using too much borrowed money", "Trading too often", "Trading at night", "Using indicators"], 0),
        ("The '1% Rule' means...", ["Risking 1% of equity per trade", "Making 1% per day", "Using 1:1 leverage", "Winning 1% of trades"], 0),
        ("Drawdown is...", ["Peak to Trough decline", "Profit withdrawal", "Drawing on chart", "Down trend"], 0),
        ("Psychology accounts for ___ of success?", ["80%", "10%", "0%", "100%"], 0)
    ],
    "liquidity": [
        ("Buy Side Liquidity (BSL) rests...", ["Above old highs", "Below old lows", "In the middle", "Nowhere"], 0),
        ("Equal Highs (EQH) usually act as...", ["Magnets for price", "Strong resistance", "Reversal points", "Safe zones"], 0),
        ("A 'Stop Hunt' is...", ["Sweeping liquidity before reversing", "Broker cheating", "Market crashing", "A game"], 0),
        ("Inducement is used to...", ["Trap early traders", "Help traders", "Signal entry", "Close market"], 0),
        ("Asian Range usually provides...", ["Liquidity to be swept", "Direction for the day", "High volume", "Nothing"], 0),
        ("Which session often sweeps Asian High/Low?", ["London", "New York", "Sydney", "Late Asian"], 0),
        ("Fair Value Gap (FVG) is...", ["Imbalance", "Support", "Resistance", "Trendline"], 0),
        ("Banks trade against...", ["Retail Stop Losses", "Other banks only", "Governments", "Nobody"], 0)
    ]
}

def get_questions_for_module(title):
    t = title.lower()
    if "market" in t or "base" in t or "introduction" in t: return QUIZ_DATA["market"]
    if "fundamental" in t or "news" in t or "calendar" in t: return QUIZ_DATA["fundamental"]
    if "candle" in t or "pattern" in t or "price" in t or "first" in t: return QUIZ_DATA["candlestick"]
    if "structure" in t or "trend" in t or "technical" in t: return QUIZ_DATA["structure"]
    if "risk" in t or "management" in t or "psycholog" in t: return QUIZ_DATA["risk"]
    if "liquid" in t or "smc" in t or "smart" in t or "institutional" in t: return QUIZ_DATA["liquidity"]
    return QUIZ_DATA["market"] # Fallback

def seed_quizzes():
    with app.app_context():
        print("🧩 STARTING REALISTIC QUIZ SEEDING...")
        
        modules = Module.query.all()
        for mod in modules:
            print(f"   Processing Module: {mod.title}")
            
            # Ensure Quiz Exists
            quiz = Quiz.query.filter_by(module_id=mod.id).first()
            if not quiz:
                quiz = Quiz(module_id=mod.id, title=f"Exam: {mod.title}", min_pass_score=70)
                db.session.add(quiz)
                db.session.commit()
            
            # Ensure Questions Count (Target 8)
            current_q_count = Question.query.filter_by(quiz_id=quiz.id).count()
            
            if current_q_count < 8:
                print(f"      ---> Adding questions to reach 8 (Current: {current_q_count})")
                
                target_q_data = get_questions_for_module(mod.title)
                
                # Add 8 questions (or fewer if list small)
                for idx, (txt, opts, correct_idx) in enumerate(target_q_data):
                    # Check duplication
                    exists = Question.query.filter_by(quiz_id=quiz.id, order_index=idx+1).first()
                    if exists:
                        # Update text to be realistic if it was a stub
                        if "Question" in exists.text and "concept" in exists.text:
                            exists.text = txt
                            exists.explanation = f"Correct answer is: {opts[correct_idx]}"
                            # Update options too... complex but let's just delete options and recreate?
                            # Safer: Delete old stub question and create new
                            db.session.delete(exists)
                            db.session.commit()
                            exists = None
                    
                    if not exists:
                        q = Question(
                            quiz_id=quiz.id,
                            text=txt,
                            explanation=f"Explanation: {opts[correct_idx]} is the correct answer because it aligns with market theory.",
                            order_index=idx+1
                        )
                        db.session.add(q)
                        db.session.flush()
                        
                        # Options
                        for opt_i, opt_val in enumerate(opts):
                            db.session.add(Option(
                                question_id=q.id,
                                text=opt_val,
                                is_correct=(opt_i == correct_idx)
                            ))
                
                db.session.commit()
                
            # Sync Translation Table (Stub)
            qt = QuizTranslation.query.filter_by(quiz_id=quiz.id, lang='fr').first()
            if not qt:
                qt = QuizTranslation(quiz_id=quiz.id, lang='fr', title=quiz.title)
                db.session.add(qt)
            
            # Question Translation Sync
            qs = Question.query.filter_by(quiz_id=quiz.id).all()
            for q in qs:
                qtr = QuestionTranslation.query.filter_by(question_id=q.id, lang='fr').first()
                if not qtr:
                    qtr = QuestionTranslation(question_id=q.id, lang='fr', text=q.text, explanation=q.explanation)
                    db.session.add(qtr)
                else:
                    qtr.text = q.text # Update stub
                    
                # Options Translation logic omitted for brevity but standard similar pattern
            
            db.session.commit()

        print("✅ QUIZ SEEDING COMPLETE.")

if __name__ == "__main__":
    seed_quizzes()
