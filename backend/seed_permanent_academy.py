
import random
from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, CourseLevel, LessonType, CourseCategory, LessonTranslation, QuizTranslation, QuestionTranslation, OptionTranslation
from sqlalchemy import text

# ==========================================
# RICH CONTENT GENERATOR & STRUCTURE
# ==========================================

def generate_rich_html(title, level, topic="Trading"):
    return f"""
<div class="lesson-content premium-content">
    <div class="lesson-header">
        <h2>Mastering {title}</h2>
        <span class="badge badge-{level.lower()}">{level}</span>
    </div>
    
    <p class="lead">In this comprehensive lesson, we will explore <strong>{title}</strong>, a cornerstone concept for {level} traders. Understanding this is key to building a sustainable edge.</p>
    
    <hr class="divider"/>

    <h3>1. Core Principles</h3>
    <p>{title} isn't just a theory; it's a practical framework used by institutional traders. Here's what you need to know:</p>
    <ul>
        <li><strong>Foundation:</strong> The underlying mechanics that drive price.</li>
        <li><strong>Context:</strong> How to identify the right market conditions.</li>
        <li><strong>Execution:</strong> Precise timing for entries and exits.</li>
    </ul>

    <div class="alert alert-info">
        <i class="fas fa-lightbulb"></i>
        <strong>Key Insight:</strong> Professional traders focus on risk first. {title} allows you to define your risk clearly before entering a trade.
    </div>

    <h3>2. Technical Breakdown</h3>
    <p>Let's look at the chart. When analyzing {title}, pay attention to:</p>
    <ol>
        <li><strong>The Setup:</strong> Wait for price to approach the key zone.</li>
        <li><strong>The Trigger:</strong> Look for a confirmation candle (e.g., Engulfing, Pinbar).</li>
        <li><strong>The Validation:</strong> Ensure volume supports the move.</li>
    </ol>

    <h3>3. Real-World Examples</h3>
    <p>Imagine the EUR/USD is in an uptrend. You identify a setup based on {title}. Instead of jumping in, you wait for a pullback to the value area. This patience is what separates winners from losers.</p>

    <h3>4. Common Pitfalls</h3>
    <ul>
        <li>Assuming {title} works 100% of the time. (Nothing does!)</li>
        <li>Ignoring higher timeframe market structure.</li>
        <li>Trading during high-impact news events without protection.</li>
    </ul>

    <hr class="divider"/>

    <h3>Summary</h3>
    <p>To master {title}, practice identifying it on historical charts first. Once confident, move to a demo account. Remember, consistency is the goal.</p>
</div>
"""

TARGET_COURSES = [
    {
        "id": 9, "title": "Introduction au Trading (FR)", "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "lang": "fr",
        "modules": [
            {"title": "Les Bases du Marché", "lessons": ["Comprendre le Forex", "Paires de Devises", "Sessions de Trading", "Mots-clés Essentiels"]},
            {"title": "Analyse Fondamentale", "lessons": ["PIB et Taux d'Intérêt", "Inflation et Chômage", "Le Calendrier Économique", "Impact des News"]},
            {"title": "Premiers Pas Techniques", "lessons": ["Bougies Japonaises", "Supports et Résistances", "Lignes de Tendance", "Utilisation de MT4/MT5"]}
        ]
    },
    {
        "id": 10, "title": "Trading Fundamentals", "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "lang": "en",
        "modules": [
            {"title": "Market Mechanics", "lessons": ["Bid, Ask, and Spread", "Leverage and Margin", "Lot Sizes and Pips", "Order Types Execution"]},
            {"title": "Brokerage & Platforms", "lessons": ["Choosing a Broker", "ECN vs Market Makers", "Platform Setup", "Charting Basics"]},
            {"title": "The Flow of Money", "lessons": ["Who moves the market?", "Central Banks", "Hedge Funds", "Retail Traders"]}
        ]
    },
    {
        "id": 11, "title": "Price Action Mastery", "level": CourseLevel.BEGINNER, "cat": CourseCategory.TECHNICAL, "lang": "en",
        "modules": [
            {"title": "Candlestick Patterns", "lessons": ["Anatomy of a Candle", "Doji & Reversals", "Engulfing Patterns", "Pin Bars Setup"]},
            {"title": "Chart Patterns", "lessons": ["Head & Shoulders", "Double Tops/Bottoms", "Triangles", "Flags & Pennants"]},
            {"title": "Trend Identification", "lessons": ["Highs & Lows", "Trend Exhaustion", "Reversal Signals", "Multi-Timeframe Analysis"]}
        ]
    },
    {
        "id": 12, "title": "Smart Money Concepts", "level": CourseLevel.ADVANCED, "cat": CourseCategory.TECHNICAL, "lang": "en",
        "modules": [
            {"title": "Liquidity", "lessons": ["Buy/Sell Side Liquidity", "Inducement Traps", "Liquidity Sweeps", "Stop Hunts"]},
            {"title": "Structure Mapping", "lessons": ["Swing vs Internal", "Strong/Weak Highs", "BOS Mechanics", "CHoCH Entry"]},
            {"title": "Institutional Footprint", "lessons": ["Order Blocks (OB)", "Fair Value Gaps (FVG)", "Breaker Blocks", "Mitigation Strategy"]}
        ]
    }
]

def seed_permanent():
    with app.app_context():
        print("🛡️ STARTING PERMANENT ACADEMY SEED 🛡️")
        
        # 1. Ensure Courses Exist (Upsert)
        for c_data in TARGET_COURSES:
            course = Course.query.get(c_data['id'])
            if not course:
                print(f"➕ Creating Course: {c_data['title']} (ID: {c_data['id']})")
                course = Course(
                    id=c_data['id'], # Force ID
                    title=c_data['title'],
                    description=f"Complete mastery of {c_data['title']}.",
                    level=c_data['level'],
                    category=c_data['cat'],
                    lang=c_data['lang'],
                    duration_minutes=180,
                    xp_reward=500,
                    is_premium=True if c_data['level'] == CourseLevel.ADVANCED else False,
                    thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800"
                )
                db.session.add(course)
            else:
                print(f"🔄 Updating Course: {c_data['title']}")
                course.title = c_data['title']
                course.level = c_data['level']
                course.category = c_data['cat']
            
            db.session.commit()

            # 2. Ensure Modules
            for idx, mod_data in enumerate(c_data['modules']):
                # Find by title AND course_id to avoid mixups
                module = Module.query.filter_by(course_id=course.id, title=mod_data['title']).first()
                if not module:
                    print(f"   ➕ Module: {mod_data['title']}")
                    module = Module(course_id=course.id, title=mod_data['title'], order_index=idx+1)
                    db.session.add(module)
                    db.session.flush() # get ID
                
                # 3. Ensure Lessons & Content
                for l_idx, l_title in enumerate(mod_data['lessons']):
                    lesson = Lesson.query.filter_by(module_id=module.id, title=l_title).first()
                    
                    real_content = generate_rich_html(l_title, course.level.name)
                    
                    if not lesson:
                        print(f"      ➕ Lesson: {l_title}")
                        lesson = Lesson(
                            module_id=module.id,
                            title=l_title,
                            order_index=l_idx+1,
                            lesson_type=LessonType.TEXT,
                            content=real_content
                        )
                        db.session.add(lesson)
                    else:
                        # ENFORCE CONTENT PERSISTENCE
                        if not lesson.content or len(lesson.content) < 500:
                            print(f"      ✏️ Fixing Content for: {l_title}")
                            lesson.content = real_content
                    
                    db.session.flush()

                    # 4. Sync Translation (Crucial for i18n fallback issues)
                    # We inject the same content into the translation table for the course's language
                    trans = LessonTranslation.query.filter_by(lesson_id=lesson.id, lang=c_data['lang']).first()
                    if not trans:
                        trans = LessonTranslation(lesson_id=lesson.id, lang=c_data['lang'], title=l_title, content=real_content)
                        db.session.add(trans)
                    else:
                        trans.title = l_title
                        trans.content = real_content # Ensure trans also has the rich content

                # 5. Ensure Quiz
                quiz = Quiz.query.filter_by(module_id=module.id).first()
                if not quiz:
                    print(f"      🧩 Quiz: {mod_data['title']}")
                    quiz = Quiz(module_id=module.id, title=f"Examen: {mod_data['title']}", min_pass_score=70)
                    db.session.add(quiz)
                    db.session.flush()
                
                # Ensure Questions
                if Question.query.filter_by(quiz_id=quiz.id).count() == 0:
                    for i in range(5):
                        q = Question(
                            quiz_id=quiz.id,
                            text=f"Question {i+1} regarding {mod_data['title']}?",
                            explanation="This is important because..."
                        )
                        db.session.add(q)
                        db.session.flush()
                        db.session.add(Option(question_id=q.id, text="Correct", is_correct=True))
                        db.session.add(Option(question_id=q.id, text="Wrong", is_correct=False))

            db.session.commit()
            
        print("✅ PERMANENT SEED COMPLETE. Data is secured.")

if __name__ == "__main__":
    seed_permanent()
