import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, Quiz, Question, Option, LessonType, UserLessonProgress, UserQuizAttempt, UserQuizAnswer, UserCourseProgress

# Monkey patch Lesson.save_to_db for convenience
def save_to_db_lesson(self):
    db.session.add(self)
    return self

Lesson.save_to_db = save_to_db_lesson

def seed_course_content():
    with app.app_context():
        # 1. Target correct course
        target_title = "Trading Fundamentals & Market Mechanics"
        print(f"🚀 Seeding Course: {target_title}")
        
        course = Course.query.filter_by(title=target_title).first()
        if not course:
            print(f"❌ Course not found. Please run seed_beautiful_academy.py first.")
            return

        print(f"📚 Course ID: {course.id}")
        
        # 2. Clean existing content for this course
        print("♻️ Cleaning existing modules/lessons/quizzes for this course...")
        
        # Clean Final Exam
        final_exams = Quiz.query.filter_by(course_id=course.id, module_id=None).all()
        for fe in final_exams:
            for q in fe.questions:
                Option.query.filter_by(question_id=q.id).delete()
                UserQuizAnswer.query.filter_by(question_id=q.id).delete()
                db.session.delete(q)
            UserQuizAttempt.query.filter_by(quiz_id=fe.id).delete()
            db.session.delete(fe)
            
        # Clean Modules
        modules = Module.query.filter_by(course_id=course.id).all()
        for mod in modules:
            # Delete Lessons
            for lesson in mod.lessons:
                UserLessonProgress.query.filter_by(lesson_id=lesson.id).delete()
                db.session.delete(lesson)
            # Delete Quizzes
            quizzes = Quiz.query.filter_by(module_id=mod.id).all()
            for qz in quizzes:
                for q in qz.questions:
                    Option.query.filter_by(question_id=q.id).delete()
                    UserQuizAnswer.query.filter_by(question_id=q.id).delete()
                    db.session.delete(q)
                UserQuizAttempt.query.filter_by(quiz_id=qz.id).delete()
                db.session.delete(qz)
            db.session.delete(mod)
            
        db.session.commit()
        print("✅ Cleaned.")
        
        # 3. Create Content
        
        # MODULE 1
        mod1 = Module(course_id=course.id, title="Fundamentals of Trading", order_index=1)
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
                    </ul>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()

        Lesson(
            module_id=mod1.id,
            title="Trading Terminology",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Essential Terms</h2>
                <div class="bg-blue-900/30 p-6 rounded-xl border border-blue-500/40 mb-6">
                    <h3 class="text-2xl font-bold text-blue-300 mb-4">PIP (Percentage in Point)</h3>
                    <p class="text-gray-300 mb-3">The smallest price movement in most currency pairs. 1 Pip = 0.0001 (usually).</p>
                </div>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()

        # MODULE 2
        mod2 = Module(course_id=course.id, title="Market Structure & Instruments", order_index=2)
        db.session.add(mod2)
        db.session.flush()
        
        Lesson(
            module_id=mod2.id,
            title="How Markets Work",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Supply & Demand</h2>
                <p class="text-gray-300 text-lg">Markets move based on the imbalance between buyers (demand) and sellers (supply).</p>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()

        Lesson(
            module_id=mod2.id,
            title="Leverage & Margin",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Leverage</h2>
                <p class="text-gray-300 text-lg">Leverage allows you to multiply your buying power. Use it wisely.</p>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()

        # MODULE 3
        mod3 = Module(course_id=course.id, title="Risk & Psychology", order_index=3)
        db.session.add(mod3)
        db.session.flush()
        
        Lesson(
            module_id=mod3.id,
            title="The 1% Rule",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Risk Management</h2>
                <p class="text-gray-300 text-lg">Never risk more than 1% of your account on a single trade.</p>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=1
        ).save_to_db()

        Lesson(
            module_id=mod3.id,
            title="Trading Psychology",
            content="""<div class="space-y-6">
                <h2 class="text-3xl font-bold text-yellow-500">Psychology</h2>
                <p class="text-gray-300 text-lg">Master your emotions (FOMO, Greed, Fear) to succeed.</p>
            </div>""",
            content_type='html',
            lesson_type=LessonType.TEXT,
            order_index=2
        ).save_to_db()

        db.session.commit()
        print("✅ Modules created.")

        # FINAL EXAM
        print("📝 Creating Final Exam...")
        final_exam = Quiz(
            course_id=course.id,
            module_id=None,
            title="Final Exam: Trading Fundamentals",
            min_pass_score=70
        )
        db.session.add(final_exam)
        db.session.flush()

        questions_data = [
            {"text": "What is a PIP?", "explanation": "Percentage in Point, usually 4th decimal.", "options": [{"text": "Profit", "is_correct": False}, {"text": "Percentage in Point", "is_correct": True}]},
            {"text": "What is the 1% Rule?", "explanation": "Max risk per trade.", "options": [{"text": "Risk 1% max per trade", "is_correct": True}, {"text": "Make 1% profit daily", "is_correct": False}]},
            {"text": "Which market is most liquid?", "explanation": "Forex market.", "options": [{"text": "Stocks", "is_correct": False}, {"text": "Forex", "is_correct": True}]},
            {"text": "What moves price?", "explanation": "Supply and Demand.", "options": [{"text": "Magic", "is_correct": False}, {"text": "Supply and Demand", "is_correct": True}]},
            {"text": "What is FOMO?", "explanation": "Fear Of Missing Out.", "options": [{"text": "Fear Of Missing Out", "is_correct": True}, {"text": "Happy trading", "is_correct": False}]},
            {"text": "Why use stop loss?", "explanation": "To limit loss.", "options": [{"text": "To limit loss", "is_correct": True}, {"text": "To stop profit", "is_correct": False}]},
            {"text": "What is Leverage?", "explanation": "Borrowed capital.", "options": [{"text": "Borrowed buying power", "is_correct": True}, {"text": "Free money", "is_correct": False}]},
            {"text": "What is Spread?", "explanation": "Difference between Bid and Ask.", "options": [{"text": "Bid/Ask Diff", "is_correct": True}, {"text": "Profit", "is_correct": False}]},
            {"text": "Long position means?", "explanation": "Buying.", "options": [{"text": "Selling", "is_correct": False}, {"text": "Buying", "is_correct": True}]},
            {"text": "Short position means?", "explanation": "Selling.", "options": [{"text": "Buying", "is_correct": False}, {"text": "Selling", "is_correct": True}]}
        ]

        for idx, q_data in enumerate(questions_data):
            q = Question(quiz_id=final_exam.id, text=q_data['text'], explanation=q_data['explanation'], order_index=idx+1)
            db.session.add(q)
            db.session.flush()
            for opt in q_data['options']:
                db.session.add(Option(question_id=q.id, text=opt['text'], is_correct=opt['is_correct']))

        db.session.commit()
        print("✅ Final Exam created.")
        print("🎉 success")

if __name__ == "__main__":
    seed_course_content()
