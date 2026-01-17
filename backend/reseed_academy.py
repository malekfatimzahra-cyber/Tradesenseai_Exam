"""
Script to reseed the Academy with courses, modules, and lessons.
This restores the initial state of the Academy database.
"""
from app import app, db
from models import Course, Module, Lesson, Quiz, Question, Option, Badge, CourseCategory, CourseLevel

def clean_academy():
    """Remove all academy data"""
    print("🧹 Cleaning existing academy data...")
    Module.query.delete()
    Course.query.delete()
    Badge.query.delete()
    db.session.commit()
    print("✅ Cleaned!")

def seed_full_academy():
    print("🌱 Seeding FULL Academy Content...")
    
    # Badges
    badges_data = [
        {"name": "Technical Titan", "desc": "Mastered technical analysis", "icon": "fa-chart-line", "cat": "TECHNICAL"},
        {"name": "Risk Guardian", "desc": "Completed risk management", "icon": "fa-shield-halved", "cat": "RISK"},
        {"name": "Psychology Master", "desc": "Mental discipline achieved", "icon": "fa-brain", "cat": "PSYCHOLOGY"}
    ]
    for bd in badges_data:
        if not Badge.query.filter_by(name=bd["name"]).first():
            db.session.add(Badge(name=bd["name"], description=bd["desc"], icon_name=bd["icon"], category=bd["cat"], xp_bonus=500))
    db.session.commit()
    
    # =========== COURSE 1: INSTITUTIONAL TRADING ===========
    if not Course.query.filter_by(title="Institutional Trading Mastery").first():
        c1 = Course(
            title="Institutional Trading Mastery", 
            description="Master Order Blocks, Liquidity, Market Structure like the pros.", 
            category=CourseCategory.TECHNICAL, 
            level=CourseLevel.INTERMEDIATE, 
            thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", 
            duration_minutes=180, 
            xp_reward=1500, 
            is_premium=False
        )
        db.session.add(c1)
        db.session.commit()
        
        # Module 1: Market Structure
        m1 = Module(course_id=c1.id, title="Market Structure Fundamentals", order=1)
        db.session.add(m1)
        db.session.commit()
        
        lessons_m1 = [
            {"title": "Introduction to Market Structure", "content": "## What is Market Structure?\nMarket structure is the backbone of price action. It defines trend direction using swing highs and lows.\n\n### Why It Matters\nInstitutions trade based on structure breaks. Retail traders who ignore this lose.\n\n### Core Concepts\n- **Uptrend**: Higher Highs (HH) + Higher Lows (HL)\n- **Downtrend**: Lower Lows (LL) + Lower Highs (LH)\n- **Range**: Equal highs and lows\n\n**Key Insight**: Structure determines bias. Always trade WITH the structure, never against it.", "order": 1},
            {"title": "Break of Structure (BOS)", "content": "## BOS Explained\nA Break of Structure confirms trend continuation.\n\n### In an Uptrend\nPrice breaks the previous swing high → Bullish BOS.\n\n### In a Downtrend\nPrice breaks the previous swing low → Bearish BOS.\n\n### Trading the BOS\n1. Wait for the break\n2. Look for pullback to order block\n3. Enter on confirmation\n\n**Example**: BTC breaks $45k high. Pullback to $44k order block = long entry.", "order": 2},
            {"title": "Change of Character (ChoCH)", "content": "## ChoCH: The Reversal Signal\nChange of Character signals a potential trend reversal.\n\n### How to Spot It\n- In uptrend: Price breaks the last HL (higher low)\n- In downtrend: Price breaks the last LH (lower high)\n\n### What to Do\nChoCH is NOT an entry—it's a WARNING. Wait for confirmation:\n- New structure formation\n- Order block in new direction\n- Volume spike\n\n**Pro Tip**: Most retail traders enter too early on ChoCH and get stopped out. Be patient.", "order": 3}
        ]
        
        for les_data in lessons_m1:
            les = Lesson(module_id=m1.id, title=les_data["title"], content=les_data["content"], order=les_data["order"])
            db.session.add(les)
            db.session.commit()
            
            quiz = Quiz(lesson_id=les.id, title=f"{les_data['title']} Quiz", min_pass_score=70)
            db.session.add(quiz)
            db.session.commit()
            
            if "Introduction" in les_data["title"]:
                q1 = Question(quiz_id=quiz.id, text="What defines an uptrend?", explanation="Higher Highs and Higher Lows.")
                db.session.add(q1)
                db.session.commit()
                db.session.add(Option(question_id=q1.id, text="HH + HL", is_correct=True))
                db.session.add(Option(question_id=q1.id, text="LL + LH", is_correct=False))
                db.session.add(Option(question_id=q1.id, text="Equal highs/lows", is_correct=False))
            elif "BOS" in les_data["title"]:
                q2 = Question(quiz_id=quiz.id, text="What does BOS confirm?", explanation="Trend continuation.")
                db.session.add(q2)
                db.session.commit()
                db.session.add(Option(question_id=q2.id, text="Trend continuation", is_correct=True))
                db.session.add(Option(question_id=q2.id, text="Trend reversal", is_correct=False))
            else:
                q3 = Question(quiz_id=quiz.id, text="ChoCH signals what?", explanation="Potential reversal warning.")
                db.session.add(q3)
                db.session.commit()
                db.session.add(Option(question_id=q3.id, text="Reversal warning", is_correct=True))
                db.session.add(Option(question_id=q3.id, text="Buy signal", is_correct=False))
            db.session.commit()
        
        # Module 2: Order Blocks
        m2 = Module(course_id=c1.id, title="Order Blocks & Fair Value Gaps", order=2)
        db.session.add(m2)
        db.session.commit()
        
        lessons_m2 = [
            {"title": "What Are Order Blocks?", "content": "## Order Blocks Defined\nAn Order Block (OB) is the last opposing candle before a strong move.\n\n### Why They Work\nInstitutions place massive orders in these zones. When price returns, they defend it.\n\n### Bullish OB\nLast **down** candle before a bullish rally.\n\n### Bearish OB\nLast **up** candle before a bearish drop.\n\n**Visual**: Think of OB as institutional support/resistance on steroids.", "order": 1},
            {"title": "Identifying Valid Order Blocks", "content": "## Valid vs Invalid OBs\nNot all order blocks are equal. Here's how to filter:\n\n### Valid OB Criteria\n1. **Engulfment**: OB candle must be engulfed by the breakout candle\n2. **Unmitigated**: Price hasn't returned to it yet\n3. **Close to current price**: Ideally within 5-10% range\n4. **Volume spike**: Confirmation of institutional activity\n\n### Invalid OBs\n- Already tested (mitigated)\n- Tiny candle with no volume\n- Too far from current price\n\n**Pro Tip**: Draw a box from OB open to close. Entry is when price re-enters that box.", "order": 2},
            {"title": "Fair Value Gaps (FVG)", "content": "## FVG: The Imbalance\nA Fair Value Gap is an imbalance between buyers and sellers, leaving a 'gap' on the chart.\n\n### How to Spot FVG\nThree consecutive candles where:\n- Candle 1 high < Candle 3 low (Bullish FVG)\n- Candle 1 low > Candle 3 high (Bearish FVG)\n\n### Trading FVGs\nPrice tends to 'fill' FVGs before continuing the trend.\n\n**Setup**:\n1. Identify FVG\n2. Wait for price to return to the gap\n3. Enter when price reacts (rejection candle)\n\n**Example**: EUR/USD rallies leaving FVG at 1.0850-1.0870. Price pulls back, fills at 1.0860, then resumes rally.", "order": 3}
        ]
        
        for les_data in lessons_m2:
            les = Lesson(module_id=m2.id, title=les_data["title"], content=les_data["content"], order=les_data["order"])
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"{les_data['title']} Quiz", min_pass_score=75)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text=f"What is the main concept of {les_data['title']}?", explanation="Review the lesson for details.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="Covered in lesson", is_correct=True))
            db.session.add(Option(question_id=q.id, text="Not mentioned", is_correct=False))
            db.session.commit()
    
    # =========== COURSE 2: PSYCHOLOGY ===========
    if not Course.query.filter_by(title="Iron Mindset: Trading Psychology").first():
        c2 = Course(
            title="Iron Mindset: Trading Psychology", 
            description="Conquer fear, greed, and emotional trading.", 
            category=CourseCategory.PSYCHOLOGY, 
            level=CourseLevel.ADVANCED, 
            thumbnail_url="https://images.unsplash.com/photo-1549633033-9a446772f533?w=800", 
            duration_minutes=120, 
            xp_reward=1000, 
            is_premium=True
        )
        db.session.add(c2)
        db.session.commit()
        
        m1 = Module(course_id=c2.id, title="Emotional Mastery", order=1)
        db.session.add(m1)
        db.session.commit()
        
        psych_lessons = [
            {"title": "The Emotional Cycle", "content": "## Trading is 80% Psychology\n\n### The Cycle\n1. **Optimism**: New trade, full of hope\n2. **Excitement**: Position moves in your favor\n3. **Thrill**: Profit peaks, you feel invincible\n4. **Euphoria**: Top of the market, maximum risk\n5. **Anxiety**: Price reverses\n6. **Denial**: 'It will come back'\n7. **Fear**: Losses mount\n8. **Desperation**: Holding losing positions\n9. **Panic**: Capitulation, exit at worst price\n10. **Despondency**: Swear off trading\n\n**Solution**: Recognize this cycle. Exit at Thrill, never hold to Panic."},
            {"title": "Handling FOMO", "content": "## FOMO Kills Accounts\nFear Of Missing Out makes you chase price and enter at the worst time.\n\n### Why It Happens\n- Social media brags\n- Seeing others profit\n- Lack of patience\n\n### The Fix\n1. **Have a plan**: Only trade YOUR setups\n2. **Journal misses**: Track trades you skipped. You'll see most weren't worth it\n3. **Abundance mindset**: The market always provides another opportunity\n\n**Mantra**: 'If I missed it, it wasn't my trade.'"},
            {"title": "Overcoming Revenge Trading", "content": "## Revenge Trading: The Account Killer\nAfter a loss, the urge to 'win it back' is overwhelming. This is how you blow up.\n\n### The Trap\n- Take a loss → Feel angry → Enter random trade → Bigger loss → Repeat\n\n### Prevention\n1. **Hard stop**: After 2 losses, STOP for the day\n2. **Walk away**: Physical distance from charts\n3. **Review**: Journal what happened, learn\n4. **Reset**: Come back tomorrow with clear head\n\n**Truth**: One good trade can't fix bad trading. Fix the process, not the result."}
        ]
        
        for les_data in psych_lessons:
            les = Lesson(module_id=m1.id, title=les_data["title"], content=les_data["content"], order=len([l for l in psych_lessons if psych_lessons.index(l) <= psych_lessons.index(les_data)]))
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"Psychology: {les_data['title']}", min_pass_score=80)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text="What's the best response to a losing trade?", explanation="Stop, review, and reset.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="Stop and review", is_correct=True))
            db.session.add(Option(question_id=q.id, text="Revenge trade immediately", is_correct=False))
            db.session.commit()
    
    # == COURSE 3: RISK ==
    if not Course.query.filter_by(title="Risk Management Mastery").first():
        c3 = Course(
            title="Risk Management Mastery", 
            description="Survival first, profits second.", 
            category=CourseCategory.RISK, 
            level=CourseLevel.BEGINNER, 
            thumbnail_url="https://images.unsplash.com/photo-1639322537228-ad71c4295843?w=800", 
            duration_minutes=90, 
            xp_reward=800, 
            is_premium=False
        )
        db.session.add(c3)
        db.session.commit()
        m = Module(course_id=c3.id, title="Risk Fundamentals", order=1)
        db.session.add(m)
        db.session.commit()
        
        risk_lessons = [
            {"title": "The 1% Rule", "content": "## Never Risk More Than 1-2%\n\n### The Math\n$10,000 account, 1% risk = $100 max loss per trade.\n\n### Why?\n- 10 losses in a row = only 10% drawdown\n- At 10% risk per trade, 3 losses = -27% (nearly impossible to recover)\n\n**Truth**: Risk management is more important than entry strategy."},
            {"title": "Position Sizing Formula", "content": "## Calculate Lot Size\n\n**Formula**:\nLot Size = (Account Size × Risk %) / (Stop Loss in pips × Pip Value)\n\n**Example**:\n- Account: $5,000\n- Risk: 1% ($50)\n- Stop Loss: 50 pips\n- Pip Value: $10/lot\n\nLot Size = $50 / (50 × $10) = 0.1 lots\n\n**Never** guess your position size."},
            {"title": "Risk-Reward Ratios", "content": "## Minimum 1:2 RR\n\nIf you risk $100, aim for $200+ profit.\n\n### Why 1:2?\nWith 40% win rate and 1:2 RR, you're profitable.\n\n**Calculation**:\n10 trades, 4 wins, 6 losses:\n- Wins: 4 × $200 = $800\n- Losses: 6 × $100 = -$600\n- Net: +$200\n\n**Rule**: Never take trades below 1:1.5 RR."}
        ]
        
        for i, ld in enumerate(risk_lessons):
            les = Lesson(module_id=m.id, title=ld["title"], content=ld["content"], order=i+1)
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"Risk: {ld['title']}", min_pass_score=100)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text="What's the max recommended risk per trade?", explanation="1-2% to survive drawdowns.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="1-2%", is_correct=True))
            db.session.add(Option(question_id=q.id, text="10%", is_correct=False))
            db.session.commit()
    
    print("✅ Full Academy Content Seeded Successfully!")
    print(f"📚 Total courses: {Course.query.count()}")
    print(f"📖 Total modules: {Module.query.count()}")
    print(f"📝 Total lessons: {Lesson.query.count()}")

if __name__ == '__main__':
    with app.app_context():
        clean_academy()
        seed_full_academy()
