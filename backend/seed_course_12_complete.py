import os
import sys
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, LessonType

def seed_course_12_complete():
    with app.app_context():
        print("🚀 Seeding Course 12: Trading Fundamentals & Market Mechanics")
        
        course = Course.query.get(12)
        if not course:
            print("❌ Course 12 not found")
            return
        
        # Check if already seeded - FORCE RE-SEED by deleting manually if needed
        existing_modules = Module.query.filter_by(course_id=12).count()
        if existing_modules > 0:
            print(f"⚠️ Course 12 already has {existing_modules} modules.")
            print("⚠️ To re-seed, manually delete modules from Railway SQL first.")
            print("⚠️ Skipping to avoid data corruption.")
            return
        
        print(f"📚 Course: {course.title}")
        
        # MODULE 1: Fundamentals of Trading
        mod1 = Module(course_id=12, title="Fundamentals of Trading", order_index=1)
        db.session.add(mod1)
        db.session.flush()
        
        Lesson(
            module_id=mod1.id,
            title="What is Trading?",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Understanding Trading</h2>
                <p class="text-gray-300 text-lg">Trading is the act of buying and selling financial instruments (stocks, currencies, commodities) with the goal of generating profit from price movements.</p>
                
                <div class="bg-gray-800 p-6 rounded-xl border-l-4 border-blue-500">
                    <h3 class="text-xl font-bold text-white mb-3">Key Differences: Trading vs Investing</h3>
                    <ul class="list-disc pl-6 space-y-2 text-gray-300">
                        <li><strong>Trading:</strong> Short to medium-term (minutes to weeks)</li>
                        <li><strong>Investing:</strong> Long-term (months to years)</li>
                        <li><strong>Trading:</strong> Profit from volatility</li>
                        <li><strong>Investing:</strong> Profit from growth</li>
                    </ul>
                </div>
                
                <h3 class="text-2xl font-bold text-white mt-8">Types of Markets</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div class="bg-gray-800 p-4 rounded-lg">
                        <h4 class="font-bold text-blue-400">Forex (FX)</h4>
                        <p class="text-sm text-gray-300 mt-2">Currency pairs like EUR/USD. Most liquid market globally.</p>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg">
                        <h4 class="font-bold text-green-400">Stocks</h4>
                        <p class="text-sm text-gray-300 mt-2">Shares of companies (Apple, Tesla, Google).</p>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg">
                        <h4 class="font-bold text-purple-400">Indices</h4>
                        <p class="text-sm text-gray-300 mt-2">Baskets of stocks (S&P 500, NASDAQ, DAX).</p>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg">
                        <h4 class="font-bold text-yellow-400">Commodities</h4>
                        <p class="text-sm text-gray-300 mt-2">Gold, Oil, Silver, Natural Gas.</p>
                    </div>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()
        
        Lesson(
            module_id=mod1.id,
            title="Trading Terminology (Pips, Lots, Spread)",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Essential Trading Terms</h2>
                
                <div class="bg-blue-900/30 p-6 rounded-xl border border-blue-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-blue-300 mb-4">PIP (Percentage in Point)</h3>
                    <p class="text-gray-300 mb-3">The smallest price movement in most currency pairs.</p>
                    <div class="bg-gray-900 p-4 rounded-lg">
                        <p class="text-white font-mono">EUR/USD: 1.0850 → 1.0851 = <span class="text-green-400">+1 pip</span></p>
                        <p class="text-gray-400 text-sm mt-2">For standard lot (100,000 units), 1 pip = $10</p>
                    </div>
                </div>
                
                <div class="bg-green-900/30 p-6 rounded-xl border border-green-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-green-300 mb-4">LOT SIZE</h3>
                    <table class="w-full text-left">
                        <thead>
                            <tr class="border-b border-gray-700">
                                <th class="pb-2 text-white">Type</th>
                                <th class="pb-2 text-white">Units</th>
                                <th class="pb-2 text-white">Pip Value (EUR/USD)</th>
                            </tr>
                        </thead>
                        <tbody class="text-gray-300">
                            <tr><td class="py-2">Standard</td><td>100,000</td><td class="text-green-400">$10</td></tr>
                            <tr><td class="py-2">Mini</td><td>10,000</td><td class="text-green-400">$1</td></tr>
                            <tr><td class="py-2">Micro</td><td>1,000</td><td class="text-green-400">$0.10</td></tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="bg-red-900/30 p-6 rounded-xl border border-red-500/40">
                    <h3 class="text-2xl font-bold text-red-300 mb-4">SPREAD</h3>
                    <p class="text-gray-300 mb-3">The difference between Bid (sell) and Ask (buy) price. This is the broker's commission.</p>
                    <div class="bg-gray-900 p-4 rounded-lg">
                        <p class="text-white font-mono">Bid: 1.0850 | Ask: 1.0852 = <span class="text-red-400">2 pip spread</span></p>
                    </div>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()
        
        # MODULE 2: Market Structure & Instruments
        mod2 = Module(course_id=12, title="Market Structure & Instruments", order_index=2)
        db.session.add(mod2)
        db.session.flush()
        
        Lesson(
            module_id=mod2.id,
            title="How Markets Work (Supply & Demand)",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">The Core Principle: Supply & Demand</h2>
                <p class="text-gray-300 text-lg">All price movement is driven by imbalances between buyers and sellers.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                    <div class="bg-green-900/20 p-6 rounded-xl border-l-4 border-green-500">
                        <h3 class="text-xl font-bold text-green-400 mb-3">🟢 Demand > Supply</h3>
                        <p class="text-gray-300">More buyers than sellers → Price rises</p>
                        <p class="text-sm text-gray-400 mt-2">This creates an uptrend (bullish market)</p>
                    </div>
                    <div class="bg-red-900/20 p-6 rounded-xl border-l-4 border-red-500">
                        <h3 class="text-xl font-bold text-red-400 mb-3">🔴 Supply > Demand</h3>
                        <p class="text-gray-300">More sellers than buyers → Price falls</p>
                        <p class="text-sm text-gray-400 mt-2">This creates a downtrend (bearish market)</p>
                    </div>
                </div>
                
                <div class="bg-gray-800 p-6 rounded-xl mt-8">
                    <h3 class="text-2xl font-bold text-white mb-4">Order Types</h3>
                    <ul class="space-y-3">
                        <li class="flex items-start gap-3">
                            <span class="text-blue-400 font-bold">Market Order:</span>
                            <span class="text-gray-300">Execute immediately at current price</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-purple-400 font-bold">Limit Order:</span>
                            <span class="text-gray-300">Execute only at specified price or better</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-yellow-400 font-bold">Stop Order:</span>
                            <span class="text-gray-300">Trigger entry when price hits specific level</span>
                        </li>
                    </ul>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()
        
        Lesson(
            module_id=mod2.id,
            title="Understanding Leverage & Margin",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Leverage: The Double-Edged Sword</h2>
                
                <div class="bg-orange-900/30 p-6 rounded-xl border border-orange-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-orange-300 mb-3">⚠️ What is Leverage?</h3>
                    <p class="text-gray-300 mb-4">Leverage allows you to control a large position with a small amount of capital.</p>
                    <div class="bg-gray-900 p-4 rounded-lg">
                        <p class="text-white font-mono mb-2">1:100 Leverage = Control $100,000 with $1,000</p>
                        <p class="text-gray-400 text-sm">Your buying power is multiplied by 100</p>
                    </div>
                </div>
                
                <div class="bg-red-900/30 p-6 rounded-xl border border-red-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-red-300 mb-3">🚨 The Risk</h3>
                    <p class="text-gray-300 mb-3">Leverage magnifies both <strong>profits AND losses</strong>.</p>
                    <div class="bg-gray-900 p-4 rounded-lg space-y-2">
                        <p class="text-green-400">✅ $1,000 capital, 1% profit = $10 → With 100x leverage = <strong>$1,000 profit</strong></p>
                        <p class="text-red-400">❌ $1,000 capital, 1% loss = $10 → With 100x leverage = <strong>$1,000 loss (account wiped)</strong></p>
                    </div>
                </div>
                
                <div class="bg-blue-900/30 p-6 rounded-xl border border-blue-500/40">
                    <h3 class="text-2xl font-bold text-blue-300 mb-3">Margin & Margin Call</h3>
                    <p class="text-gray-300 mb-3"><strong>Margin:</strong> The collateral required to open a leveraged position.</p>
                    <p class="text-gray-300 mb-3"><strong>Margin Call:</strong> When your losses approach your margin, broker forces you to close positions or add funds.</p>
                    <div class="bg-yellow-900/20 p-4 rounded-lg border-l-4 border-yellow-500 mt-4">
                        <p class="text-yellow-300 font-bold">💡 Pro Tip: Use low leverage (1:10 or 1:20) until you master risk management.</p>
                    </div>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()
        
        # MODULE 3: Risk & Psychology
        mod3 = Module(course_id=12, title="Risk & Psychology", order_index=3)
        db.session.add(mod3)
        db.session.flush()
        
        Lesson(
            module_id=mod3.id,
            title="The 1% Rule (Position Sizing)",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">The Golden Rule of Trading</h2>
                <div class="bg-green-900/30 p-8 rounded-xl border border-green-500/40 mb-6">
                    <h3 class="text-3xl font-bold text-green-300 text-center mb-4">Never Risk More Than 1% Per Trade</h3>
                    <p class="text-gray-300 text-center text-lg">This single rule will save your account from catastrophic losses.</p>
                </div>
                
                <div class="bg-gray-800 p-6 rounded-xl">
                    <h3 class="text-2xl font-bold text-white mb-4">Example Calculation</h3>
                    <div class="space-y-3 text-gray-300">
                        <p>📊 <strong>Account Balance:</strong> $10,000</p>
                        <p>⚠️ <strong>Maximum Risk (1%):</strong> $100</p>
                        <p>📍 <strong>Entry Price:</strong> 1.0850</p>
                        <p>🛑 <strong>Stop Loss:</strong> 1.0830 (20 pips away)</p>
                        <p class="text-green-400 font-bold mt-4">✅ Lot Size = $100 ÷ (20 pips × $10/pip) = 0.5 standard lots</p>
                    </div>
                </div>
                
                <div class="bg-blue-900/20 p-6 rounded-xl border-l-4 border-blue-500 mt-6">
                    <h3 class="text-xl font-bold text-blue-300 mb-3">Why This Works</h3>
                    <ul class="list-disc pl-6 space-y-2 text-gray-300">
                        <li>You can survive <strong>100 consecutive losses</strong> (almost impossible)</li>
                        <li>Removes emotional decision-making</li>
                        <li>Forces disciplined trading</li>
                        <li>Preserves capital for the long run</li>
                    </ul>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()
        
        Lesson(
            module_id=mod3.id,
            title="Trading Psychology (FOMO & Discipline)",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Your Mind is Your Biggest Enemy</h2>
                
                <div class="bg-red-900/30 p-6 rounded-xl border border-red-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-red-300 mb-3">😰 FOMO (Fear of Missing Out)</h3>
                    <p class="text-gray-300 mb-3">The urge to enter a trade because "everyone else is winning."</p>
                    <div class="bg-gray-900 p-4 rounded-lg">
                        <p class="text-yellow-300 font-bold mb-2">Classic Scenario:</p>
                        <p class="text-gray-400 text-sm">Bitcoin pumps 10% → You rush to buy → It dumps 15% the next hour.</p>
                    </div>
                    <div class="mt-4 bg-green-900/20 p-4 rounded-lg border-l-4 border-green-500">
                        <p class="text-green-300 font-bold">Solution: Wait for your setup. Miss 100 trades rather than lose on 1 revenge trade.</p>
                    </div>
                </div>
                
                <div class="bg-purple-900/30 p-6 rounded-xl border border-purple-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-purple-300 mb-3">😡 Revenge Trading</h3>
                    <p class="text-gray-300 mb-3">Trying to "win back" losses immediately after a losing trade.</p>
                    <div class="bg-gray-900 p-4 rounded-lg">
                        <p class="text-red-400 mb-2">❌ Lost $100 → Double position size → Lose $200 → Triple size → Lose $400...</p>
                        <p class="text-gray-400 text-sm">This is the fastest way to blow your account.</p>
                    </div>
                    <div class="mt-4 bg-blue-900/20 p-4 rounded-lg border-l-4 border-blue-500">
                        <p class="text-blue-300 font-bold">Solution: Step away. Close your charts. Come back tomorrow with a clear head.</p>
                    </div>
                </div>
                
                <div class="bg-gray-800 p-6 rounded-xl">
                    <h3 class="text-2xl font-bold text-white mb-4">The Trader's Mindset Checklist</h3>
                    <ul class="space-y-2">
                        <li class="flex items-start gap-3">
                            <span class="text-green-400">✅</span>
                            <span class="text-gray-300">I have a written trading plan</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-green-400">✅</span>
                            <span class="text-gray-300">I never risk more than 1% per trade</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-green-400">✅</span>
                            <span class="text-gray-300">I journal every trade (win or loss)</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <span class="text-green-400">✅</span>
                            <span class="text-gray-300">I accept losses as part of the game</span>
                        </li>
                    </ul>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()
        
        db.session.commit()
        print("✅ Modules and Lessons created!")
        
        # FINAL EXAM QUIZ
        print("📝 Creating Final Exam...")
        final_exam = Quiz(
            course_id=12,
            module_id=None,
            title="Final Exam: Trading Fundamentals & Market Mechanics",
            min_pass_score=70
        )
        db.session.add(final_exam)
        db.session.flush()
        
        questions_data = [
            {
                "text": "What is a PIP in Forex trading?",
                "explanation": "A PIP (Percentage in Point) is the smallest price movement in most currency pairs, typically the 4th decimal place.",
                "options": [
                    {"text": "The profit you make on a trade", "is_correct": False},
                    {"text": "The smallest price movement in a currency pair", "is_correct": True},
                    {"text": "A type of order execution", "is_correct": False},
                    {"text": "The broker's commission", "is_correct": False}
                ]
            },
            {
                "text": "What does 1:100 leverage mean?",
                "explanation": "Leverage of 1:100 means you can control $100 for every $1 of your capital.",
                "options": [
                    {"text": "You can trade 100 times per day", "is_correct": False},
                    {"text": "You control $100 for every $1 of capital", "is_correct": True},
                    {"text": "Your profit is multiplied by 100", "is_correct": False},
                    {"text": "You must deposit $100 minimum", "is_correct": False}
                ]
            },
            {
                "text": "According to the 1% rule, if your account balance is $5,000, what is your maximum risk per trade?",
                "explanation": "1% of $5,000 = $50. This is the maximum you should risk on any single trade.",
                "options": [
                    {"text": "$50", "is_correct": True},
                    {"text": "$500", "is_correct": False},
                    {"text": "$100", "is_correct": False},
                    {"text": "$1,000", "is_correct": False}
                ]
            },
            {
                "text": "What is the SPREAD in trading?",
                "explanation": "The spread is the difference between the bid (sell) price and ask (buy) price, representing the broker's commission.",
                "options": [
                    {"text": "The difference between entry and exit price", "is_correct": False},
                    {"text": "The difference between bid and ask price", "is_correct": True},
                    {"text": "The maximum drawdown allowed", "is_correct": False},
                    {"text": "The profit target", "is_correct": False}
                ]
            },
            {
                "text": "What happens when Supply > Demand in a market?",
                "explanation": "When there are more sellers than buyers, the price falls (bearish market).",
                "options": [
                    {"text": "Price rises", "is_correct": False},
                    {"text": "Price falls", "is_correct": True},
                    {"text": "Price stays flat", "is_correct": False},
                    {"text": "Market closes", "is_correct": False}
                ]
            },
            {
                "text": "What is FOMO in trading psychology?",
                "explanation": "FOMO (Fear of Missing Out) is the urge to enter trades impulsively because you feel you're missing opportunities.",
                "options": [
                    {"text": "A technical indicator", "is_correct": False},
                    {"text": "Fear of Missing Out on trades", "is_correct": True},
                    {"text": "A type of order", "is_correct": False},
                    {"text": "A chart pattern", "is_correct": False}
                ]
            },
            {
                "text": "What is Revenge Trading?",
                "explanation": "Revenge trading is trying to immediately win back losses by taking impulsive, larger trades, often leading to bigger losses.",
                "options": [
                    {"text": "Trading to win back immediate losses", "is_correct": True},
                    {"text": "A profitable trading strategy", "is_correct": False},
                    {"text": "Trading based on news", "is_correct": False},
                    {"text": "A type of market order", "is_correct": False}
                ]
            },
            {
                "text": "What is a Market Order?",
                "explanation": "A market order executes immediately at the current market price.",
                "options": [
                    {"text": "An order that waits for a specific price", "is_correct": False},
                    {"text": "An order that executes immediately at current price", "is_correct": True},
                    {"text": "An order that never expires", "is_correct": False},
                    {"text": "An order placed during market close", "is_correct": False}
                ]
            },
            {
                "text": "How many units are in a Standard Lot?",
                "explanation": "A standard lot contains 100,000 units of the base currency.",
                "options": [
                    {"text": "1,000", "is_correct": False},
                    {"text": "10,000", "is_correct": False},
                    {"text": "100,000", "is_correct": True},
                    {"text": "1,000,000", "is_correct": False}
                ]
            },
            {
                "text": "What does a Margin Call indicate?",
                "explanation": "A margin call occurs when your account losses approach your margin requirement, forcing you to close positions or add funds.",
                "options": [
                    {"text": "You've made a profit", "is_correct": False},
                    {"text": "Your losses are approaching margin requirement", "is_correct": True},
                    {"text": "It's time to increase leverage", "is_correct": False},
                    {"text": "The market is closed", "is_correct": False}
                ]
            },
            {
                "text": "Which market is the most liquid globally?",
                "explanation": "The Forex (FX) market is the most liquid financial market in the world, with over $6 trillion daily trading volume.",
                "options": [
                    {"text": "Stock Market", "is_correct": False},
                    {"text": "Forex (FX)", "is_correct": True},
                    {"text": "Cryptocurrency", "is_correct": False},
                    {"text": "Commodities", "is_correct": False}
                ]
            },
            {
                "text": "Why is discipline important in trading?",
                "explanation": "Discipline ensures you follow your trading plan, manage risk properly, and avoid emotional decisions that lead to losses.",
                "options": [
                    {"text": "It guarantees profits", "is_correct": False},
                    {"text": "It prevents emotional trading and ensures risk management", "is_correct": True},
                    {"text": "It allows you to trade more frequently", "is_correct": False},
                    {"text": "It's not important", "is_correct": False}
                ]
            }
        ]
        
        for idx, q_data in enumerate(questions_data):
            question = Question(
                quiz_id=final_exam.id,
                text=q_data["text"],
                explanation=q_data["explanation"],
                order_index=idx + 1
            )
            db.session.add(question)
            db.session.flush()
            
            for opt_data in q_data["options"]:
                option = Option(
                    question_id=question.id,
                    text=opt_data["text"],
                    is_correct=opt_data["is_correct"]
                )
                db.session.add(option)
        
        db.session.commit()
        print(f"✅ Final Exam created with {len(questions_data)} questions!")
        print("\n🎉 Course 12 is now COMPLETE and production-ready!")

# Helper method for Lesson model
def save_to_db(self):
    from models import db
    db.session.add(self)
    return self

Lesson.save_to_db = save_to_db

if __name__ == "__main__":
    seed_course_12_complete()
