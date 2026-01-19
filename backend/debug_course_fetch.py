
import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db, Course, Module, Lesson, UserLessonProgress, Quiz, UserQuizAttempt
from flask import jsonify

def simulate_get_course_details(course_id):
    with app.app_context():
        print(f"\n🔍 Simulating GET /api/academy/course/{course_id}")
        
        course = Course.query.get(course_id)
        if not course:
            print("❌ Result: 404 Not Found (Course query returned None)")
            return
        
        print(f"✅ Course Found: {course.title} (ID: {course.id})")
        
        # Simulate the logic in academy.py
        try:
            modules_data = []
            print(f"   Processing {len(course.modules)} modules...")
            
            for module in sorted(course.modules, key=lambda m: m.order_index):
                lessons_data = []
                for lesson in sorted(module.lessons, key=lambda l: l.order_index):
                    # Mocking user progress (assuming no progress for simplicity)
                    lessons_data.append({
                        'id': lesson.id,
                        'title': lesson.title,
                        'type': lesson.lesson_type.value if lesson.lesson_type else 'TEXT',
                        'duration': 10,
                        'is_completed': False
                    })
                
                module_quiz = Quiz.query.filter_by(module_id=module.id).first()
                modules_data.append({
                    'id': module.id,
                    'title': module.title,
                    'lessons': lessons_data,
                    'quiz_id': module_quiz.id if module_quiz else None,
                    'is_quiz_completed': False
                })
            
            final_exam = Quiz.query.filter_by(course_id=course_id, module_id=None).first()
            has_final_exam = bool(final_exam)
            final_exam_id = final_exam.id if final_exam else None
            
            print(f"✅ Success! Generated JSON payload structure.")
            print(f"   - Modules: {len(modules_data)}")
            print(f"   - Final Exam: {'Yes' if has_final_exam else 'No'} (ID: {final_exam_id})")
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Test known IDs
    simulate_get_course_details(12)
    
    # List all available IDs just in case
    with app.app_context():
        print("\n📋 Available Courses in DB:")
        all_courses = Course.query.all()
        for c in all_courses:
            print(f"   - ID: {c.id} | {c.title}")
