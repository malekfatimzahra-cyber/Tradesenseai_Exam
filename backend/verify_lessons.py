"""
Quick verification script to check all lessons in the database
"""

from app import app
from models import Lesson

def verify_lessons():
    with app.app_context():
        print("📚 All lessons in database:\n")
        lessons = Lesson.query.all()
        
        if not lessons:
            print("❌ No lessons found in database!")
            return
        
        for i, lesson in enumerate(lessons, 1):
            has_content = "✅" if lesson.content and len(lesson.content.strip()) > 0 else "❌"
            content_length = len(lesson.content) if lesson.content else 0
            print(f"{i}. {has_content} {lesson.title} ({content_length} chars)")
        
        print(f"\n📊 Total: {len(lessons)} lessons")
        
        # Check for missing lessons
        expected_titles = [
            "Qu'est-ce que le Trading ?",
            "Lire un Graphique",
            "La terminologie essentielle",
            "Support et Résistance",
            "La Tendance (Trend)",
            "Indicateurs Classiques",
            "Le Ratio Risque/Récompense",
            "La Psychologie"
        ]
        
        found_titles = [lesson.title for lesson in lessons]
        missing = [title for title in expected_titles if title not in found_titles]
        
        if missing:
            print(f"\n⚠️ Missing lessons:")
            for title in missing:
                print(f"   - {title}")

if __name__ == "__main__":
    verify_lessons()
