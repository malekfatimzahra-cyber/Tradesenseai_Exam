
from app import app
from models import db, Lesson, LessonType
import random

def generate_simple_rich_content(title):
    return f"""
<div class="lesson-content">
    <h2>Mastering {title}</h2>
    <p>Welcome to this lesson on <strong>{title}</strong>. This is a crucial concept that bridges the gap between novice understanding and professional application.</p>
    
    <h3>In-Depth Analysis</h3>
    <p>{title} serves as a fundamental building block in our trading strategy. By understanding the mechanics behind it, you can better anticipate market moves and react with confidence rather than hesitation.</p>
    
    <div class="highlight-box" style="background: rgba(0, 255, 127, 0.1); border-left: 4px solid #00ff7f; padding: 15px; margin: 20px 0;">
        <strong>Key Insight:</strong> The market often tests traders on this exact concept. Ensure you identify it correctly on the higher timeframes first.
    </div>

    <h3>Practical Application</h3>
    <ul>
        <li><strong>Step 1:</strong> Identify the setup on the H4 or H1 chart.</li>
        <li><strong>Step 2:</strong> Wait for a clear confirmation signal regarding {title}.</li>
        <li><strong>Step 3:</strong> Execute with defined risk parameters.</li>
    </ul>

    <h3>Conclusion</h3>
    <p>Mastery of {title} takes time, but it is well worth the effort. Review this lesson and apply the concepts in your practice sessions.</p>
</div>
"""

def cleanup_short_content():
    with app.app_context():
        print("🧹 Scanning for 'short' content (stubs)...")
        short_lessons = Lesson.query.filter(db.func.length(Lesson.content) < 500).all()
        
        print(f"Found {len(short_lessons)} lessons with short content.")
        
        for lesson in short_lessons:
            print(f"   ✏️ Enriching stub lesson: {lesson.title} (ID: {lesson.id})")
            lesson.content = generate_simple_rich_content(lesson.title)
            lesson.lesson_type = LessonType.TEXT
            
        db.session.commit()
        print("✅ All stub lessons enriched.")

if __name__ == "__main__":
    cleanup_short_content()
