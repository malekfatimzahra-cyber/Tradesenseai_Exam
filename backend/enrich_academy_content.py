
import random
from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseLevel, LessonType
from sqlalchemy import text

# ==========================================
# RICH CONTENT GENERATOR
# ==========================================

def generate_rich_content(title, level, topic_type="Technical"):
    """
    Generates a realistic, long-form educational article for a trading lesson.
    """
    return f"""
<div class="lesson-content">
    <h2>Introduction to {title}</h2>
    <p>In this comprehensive lesson, we will explore <strong>{title}</strong>, a critical concept for any trader operating at the {level} level. Understanding this topic is essential for developing a robust trading edge and maintaining consistency in the markets.</p>
    
    <h3>Why is This Important?</h3>
    <p>Many traders overlook {title} because they are focused solely on entry signals. However, professional traders know that mastery of {title} provides the context necessary to interpret price action correctly. Without this foundation, your trading strategy lacks a solid base.</p>
    
    <hr />

    <h3>Core Concepts</h3>
    <p>{title} typically involves analyzing market behavior through specific lenses. Here are the key components you need to master:</p>
    <ul>
        <li><strong>Component A:</strong> The structural basis of the concept.</li>
        <li><strong>Component B:</strong> How it interacts with dynamic market forces.</li>
        <li><strong>Component C:</strong> The signal for execution or invalidation.</li>
    </ul>
    <p>When these three components align, the probability of a successful trade outcome increases significantly.</p>

    <h3>Deep Dive: Applying the Strategy</h3>
    <p>Let's break down how to apply {title} in a real-world scenario. Imagine the market is trending upwards. You see a setup forming that aligns with your higher timeframe analysis.</p>
    <ol>
        <li><strong>Identify the Zone:</strong> Mark your key levels on the chart.</li>
        <li><strong>Wait for Reaction:</strong> Do not just set a limit order; observe how price reacts when it reaches the level.</li>
        <li><strong>Confirm with Volume/Price Action:</strong> Look for a displacement or a candlestick pattern that confirms your bias.</li>
        <li><strong>Execute and Manage:</strong> Enter the trade with a predefined risk and management plan.</li>
    </ol>

    <div class="highlight-box" style="background: rgba(255, 215, 0, 0.1); border-left: 4px solid #ffd700; padding: 15px; margin: 20px 0;">
        <strong>Pro Tip:</strong> Never trade {title} in isolation. Always look for confluence with at least one other factor, such as a key support level, a moving average, or a Fibonacci retracement.
    </div>

    <h3>Real-World Scenario</h3>
    <p>Consider the EUR/USD pair on a 4-hour chart. The market has just broken structure to the upside (BOS). Following the rules of {title}, we would identify the origin of the move as our point of interest (POI). As price retraces into this POI, we drop to a 15-minute chart to look for a 'change of character' (ChoCH). This fractal entry reduces risk while maximizing reward potential.</p>

    <h3>Common Mistakes to Avoid</h3>
    <p>Even experienced traders fall into traps when dealing with {title}:</p>
    <ul>
        <li><strong>Over-trading:</strong> Seeing patterns where none exist.</li>
        <li><strong>Ignoring Context:</strong> Trading against the higher timeframe trend.</li>
        <li><strong>Tight Stops:</strong> Placing stop-losses too close to entry without accounting for volatility.</li>
    </ul>

    <hr />

    <h3>Summary & Key Takeaways</h3>
    <p>To wrap up, {title} is a powerful tool in your trading arsenal. Remember these key points:</p>
    <ul>
        <li>Always identify the higher timeframe narrative first.</li>
        <li>Wait for price to come to you; do not chase the market.</li>
        <li>Manage risk religiously—never risk more than 1-2% per trade.</li>
    </ul>
    <p>Proceed to the quiz to test your understanding of these concepts.</p>
</div>
"""

# ==========================================
# DATA DEFINITIONS
# ==========================================

# We will define the target structure for each course.
# If the course exists, we ensure these modules/lessons exist.
# If existing modules/lessons are essentially empty, we update them.

COURSES_STRUCTURE = {
    "Introduction au Trading (FR)": {
        "modules": [
            {"title": "Les Bases du Marché", "lessons": ["Comprendre le Forex", "Paires de Devises", "Sessions de Trading", "Mots-clés Essentiels"]},
            {"title": "Analyse Fondamentale", "lessons": ["PIB et Taux d'Intérêt", "Inflation et Chômage", "Le Calendrier Économique", "Impact des News"]},
            {"title": "Premiers Pas Techniques", "lessons": ["Bougies Japonaises", "Supports et Résistances", "Lignes de Tendance", "Utilisation de MT4/MT5"]}
        ]
    },
    "Trading Fundamentals & Market Mechanics": {
        "modules": [
            {"title": "Market Mechanics 101", "lessons": ["Bid, Ask, and Spread", "Leverage and Margin", "Lot Sizes and Pips", "Order Types Execution"]},
            {"title": "Brokerage & Platforms", "lessons": ["Choosing a Broker", "ECN vs Market Makers", "Platform Setup", "Charting Basics"]},
            {"title": "The flow of Money", "lessons": ["Who moves the market?", "Central Banks", "Hedge Funds", "Retail Traders"]}
        ]
    },
    "Introduction to Price Action": {
        "modules": [
            {"title": "Candlestick Mastery", "lessons": ["The Anatomy of a Candle", "Doji and Spinning Tops", "Engulfing Patterns", "Pin Bars and Hammers"]},
            {"title": "Chart Patterns", "lessons": ["Head and Shoulders", "Double Tops and Bottoms", "Triangles and Wedges", "Flags and Pennants"]},
            {"title": "Trend Identification", "lessons": ["Higher Highs & Lower Lows", "Trend Exhaustion", "Reversal Signals", "Multi-Timeframe Analysis"]}
        ]
    },
    "Smart Money Concepts (SMC / ICT)": {
        "modules": [
            {"title": "Liquidity Concepts", "lessons": ["Buy Side & Sell Side Liquidity", "Inducement", "Liquidity Sweeps", "Stop Hunts"]},
            {"title": "Structure Mapping", "lessons": ["Swing vs Internal Structure", "Strong Highs vs Weak Highs", "Break of Structure (BOS)", "Change of Character (CHoCH)"]},
            {"title": "Instituional References", "lessons": ["Order Blocks (OB)", "Fair Value Gaps (FVG)", "Breaker Blocks", "Mitigation Blocks"]},
            {"title": "Entry Models", "lessons": ["The Silver Bullet", "OTE (Optimal Trade Entry)", "London Killzone", "New York Killzone"]},
            {"title": "Advanced Narrative", "lessons": ["Daily Bias", "Weekly Profiles", "Quarterly Shifts", "Intermarket Analysis"]}
        ]
    },
    "Trading Psychology Under Pressure": {
        "modules": [
            {"title": "The Trader's Mind", "lessons": ["Thinking in Probabilities", "The Fear of Loss", "The Trap of Greed", "Accepting Risk"]},
            {"title": "Emotional Control", "lessons": ["Handling Drawdowns", "Avoiding Revenge Trading", "Euphoria Management", "Patience as an Edge"]},
            {"title": "Performance Routines", "lessons": ["Pre-Market Rituals", "Journaling Your Trades", "Reviewing Performance", "Meditation for Traders"]},
            {"title": "Professional Mindset", "lessons": ["Trading as a Business", "Long Term Thinking", "Detachment from Money", "Consistency > Home Runs"]},
            {"title": "Crisis Management", "lessons": ["Recovering from a Blowup", "Stopping the Tilt", "Knowing When to Step Away", "Rebuilding Confidence"]}
        ]
    },
    "Basic Risk Management for Traders": {
        "modules": [
            {"title": "The Math of Survival", "lessons": ["Risk of Ruin", "The 1% Rule", "Risk to Reward Ratio (RR)", "Win Rate vs RR"]},
            {"title": "Position Sizing", "lessons": ["Calculating Lots Correctly", "Pip Value Calculation", "Account Growth Math", "Compounding"]},
            {"title": "Trade Management", "lessons": ["Setting Stop Losses", "Trailing Stops", "Scaling Out", "Breakeven Strategies"]}
        ]
    },
    "Market Structure & Trend Logic": {
        "modules": [
            {"title": "Structure Basics", "lessons": ["Impulse vs Correction", "Valid Pullbacks", "Determining Ranges", "Premium vs Discount"]},
            {"title": "Complex Structure", "lessons": ["Fractal Nature of Markets", "Sub-structure Analysis", "Momentum Analysis", "Trend Alignment"]},
            {"title": "Trading the Trend", "lessons": ["Pullback Entries", "Breakout Entries", "Trend Continuation", "Counter-Trend Dangers"]},
            {"title": "Reversals", "lessons": ["Identifying Climax Moves", "The Wyman Cycle", "Accumulation & Distribution", "V-Shape Recoveries"]}
        ]
    },
    "Supply & Demand Trading": {
        "modules": [
            {"title": "Zones Identified", "lessons": ["Rally-Base-Drop", "Drop-Base-Rally", "Fresh vs Used Zones", "Zone Strength Scoring"]},
            {"title": "Refining Zones", "lessons": ["Wick vs Body", "Timeframe Refinement", "Validation Criteria", "Engulfing Confirmation"]},
            {"title": "Execution", "lessons": ["Limit Orders vs Market", "Set and Forget", "Confirmation Entries", "Flip Zones"]},
            {"title": "Contextual Nuance", "lessons": ["Compression", "Liquidity Approach", "Zone Failures", "News Events Interaction"]}
        ]
    }
}

# ==========================================
# MAIN LOGIC
# ==========================================

def enrich_academy():
    with app.app_context():
        print("🚀 Starting Academy Enrichment (Rich Content Injection)...")
        
        # 1. Iterate over our target schema
        for course_title, structure in COURSES_STRUCTURE.items():
            print(f"\nProcessing Course: {course_title}")
            
            # Find the course (fuzzy match or exact)
            course = Course.query.filter(Course.title == course_title).first()
            if not course:
                # Try simple match
                courses = Course.query.all()
                for c in courses:
                    if course_title in c.title or c.title in course_title:
                        course = c
                        break
            
            if not course:
                print(f"⚠️ Course '{course_title}' not found in DB. Skipping.")
                continue

            print(f"✅ Found Course ID {course.id}: {course.title} ({course.level.name})")

            # 2. Ensure Modules Exist
            existing_modules = Module.query.filter_by(course_id=course.id).all()
            existing_mod_titles = [m.title for m in existing_modules]
            
            modules_list = [] # Store module objects to add lessons to later

            for idx, mod_data in enumerate(structure['modules']):
                mod_title = mod_data['title']
                
                # Check if module exists by title
                module = next((m for m in existing_modules if m.title == mod_title), None)
                
                if not module:
                    # Create Module
                    print(f"   ➕ Creating Module: {mod_title}")
                    module = Module(course_id=course.id, title=mod_title, order_index=idx+1)
                    db.session.add(module)
                    db.session.flush() # Get ID
                else:
                    print(f"   🔹 Module exists: {mod_title}")
                
                modules_list.append((module, mod_data['lessons']))

            db.session.commit()

            # 3. Ensure Lessons Exist & Check Content
            for module, lesson_titles in modules_list:
                existing_lessons = Lesson.query.filter_by(module_id=module.id).all()
                
                for l_idx, l_title in enumerate(lesson_titles):
                    lesson = next((l for l in existing_lessons if l.title == l_title), None) # Match exact title usually
                    
                    # Generate RICH Content
                    rich_content = generate_rich_content(l_title, course.level.name)
                    
                    if not lesson:
                        print(f"      ➕ Creating Lesson: {l_title}")
                        lesson = Lesson(
                            module_id=module.id,
                            title=l_title,
                            lesson_type=LessonType.TEXT,
                            content=rich_content,
                            order_index=l_idx+1
                        )
                        db.session.add(lesson)
                    else:
                        # Check if content needs update (len check)
                        if not lesson.content or len(lesson.content) < 500:
                            print(f"      ✏️ Updating Lesson Content (was too short): {l_title}")
                            lesson.content = rich_content
                        else:
                            # print(f"      ✅ Lesson OK: {l_title}")
                            pass
                
                db.session.commit()

                # 4. Ensure Quiz Exists for Module
                quiz = Quiz.query.filter_by(module_id=module.id).first()
                if not quiz:
                    print(f"      🧩 Creating Quiz for Module: {module.title}")
                    quiz = Quiz(module_id=module.id, title=f"Quiz: {module.title}", min_pass_score=70)
                    db.session.add(quiz)
                    db.session.flush()
                
                # Ensure Questions Exist (simple check: if 0 questions, add 5)
                q_count = Question.query.filter_by(quiz_id=quiz.id).count()
                if q_count < 5:
                    print(f"      ❓ Adding Questions to Quiz...")
                    for q_i in range(5):
                        q = Question(
                            quiz_id=quiz.id,
                            text=f"Question {q_i+1} about {module.title} concepts?",
                            explanation="This is the correct answer because it aligns with the core principles discussed in the module.",
                            order_index=q_i+1
                        )
                        db.session.add(q)
                        db.session.flush()
                        
                        # Options
                        db.session.add(Option(question_id=q.id, text="Correct Answer", is_correct=True))
                        db.session.add(Option(question_id=q.id, text="Wrong Answer A", is_correct=False))
                        db.session.add(Option(question_id=q.id, text="Wrong Answer B", is_correct=False))
                        db.session.add(Option(question_id=q.id, text="Wrong Answer C", is_correct=False))
                
                db.session.commit()

    print("\n✅ Academy Enrichment Complete! All courses populated.")

if __name__ == "__main__":
    enrich_academy()
