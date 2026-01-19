from flask import Blueprint, request, jsonify
from models import db, Course, Module, Lesson, Quiz, Question, Option, UserLessonProgress, UserCourseProgress, UserXP, UserBadge, Badge, UserQuizAttempt, UserQuizAnswer
from middleware import token_required
import datetime

academy_bp = Blueprint('academy', __name__)

# Helper to award XP
def award_xp(user_id, amount):
    user_xp = UserXP.query.get(user_id)
    if not user_xp:
        user_xp = UserXP(user_id=user_id, total_xp=0, level_title="Novice")
        db.session.add(user_xp)
    
    user_xp.total_xp += amount
    
    if user_xp.total_xp >= 5000:
        user_xp.level_title = "Elite Trader"
    elif user_xp.total_xp >= 2000:
        user_xp.level_title = "Gold Pro"
    elif user_xp.total_xp >= 500:
        user_xp.level_title = "Silver Student"
        
    db.session.commit()
    return user_xp

# GET /api/academy/courses - List all courses
@academy_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'category': c.category.value,
        'level': c.level.value,
        'thumbnail_url': c.thumbnail_url,
        'duration': f"{c.duration_minutes} min",
        'xp_reward': c.xp_reward,
        'is_premium': c.is_premium
    } for c in courses]), 200

# GET /api/academy/course/<id> - Get course details with modules
@academy_bp.route('/course/<int:course_id>', methods=['GET'])
@token_required
def get_course_details(current_user, course_id):
    print(f"📡 API Request: GET /course/{course_id}")
    course = Course.query.get(course_id)
    
    if not course:
        print(f"❌ Course {course_id} NOT FOUND in DB.")
        return jsonify({'message': 'Course not found'}), 404
    
    print(f"✅ Found Course: {course.title} (ID: {course.id})")
    
    modules_data = []
    for module in sorted(course.modules, key=lambda m: m.order_index):
        lessons_data = []
        for lesson in sorted(module.lessons, key=lambda l: l.order_index):
            lp = UserLessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
            lessons_data.append({
                'id': lesson.id,
                'title': lesson.title,
                'type': lesson.lesson_type.value if lesson.lesson_type else 'TEXT',
                'duration': 10,
                'is_completed': lp.is_completed if lp else False
            })
        
        # Check for module quiz
        module_quiz = Quiz.query.filter_by(module_id=module.id).first()
        quiz_completed = False
        if module_quiz:
            qa = UserQuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=module_quiz.id, passed=True).first()
            quiz_completed = bool(qa)
        
        modules_data.append({
            'id': module.id,
            'title': module.title,
            'lessons': lessons_data,
            'quiz_id': module_quiz.id if module_quiz else None,
            'is_quiz_completed': quiz_completed
        })
    
    # Check for final exam (quiz with module_id = NULL and course_id = X)
    final_exam = Quiz.query.filter_by(course_id=course_id, module_id=None).first()
    has_final_exam = bool(final_exam)
    final_exam_id = final_exam.id if final_exam else None
    
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'category': course.category.value,
        'level': course.level.value,
        'thumbnail_url': course.thumbnail_url,
        'duration': f"{course.duration_minutes} min",
        'modules': modules_data,
        'has_final_exam': has_final_exam,
        'final_exam_id': final_exam_id
    }), 200

# GET /api/academy/lesson/<id> - Get lesson content
@academy_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
@token_required
def get_lesson(current_user, lesson_id):
    lesson = Lesson.query.get(lesson_id)
    
    if not lesson:
        return jsonify({'message': 'Lesson not found'}), 404
    
    # Track access
    lp = UserLessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if not lp:
        lp = UserLessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.session.add(lp)
    
    lp.last_accessed = datetime.datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': lesson.id,
        'title': lesson.title,
        'content': lesson.content,
        'type': lesson.lesson_type.value if lesson.lesson_type else 'TEXT',
        'video_url': lesson.video_url,
        'duration_minutes': 10
    }), 200

# POST /api/academy/lessons/<id>/complete - Mark lesson complete
@academy_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@token_required
def complete_lesson(current_user, lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    lp = UserLessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
    
    if not lp:
        lp = UserLessonProgress(user_id=current_user.id, lesson_id=lesson.id)
        db.session.add(lp)
    
    if not lp.is_completed:
        lp.is_completed = True
        lp.completed_at = datetime.datetime.utcnow()
        award_xp(current_user.id, 25)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Lesson completed',
        'xp_earned': 25
    }), 200

# GET /api/academy/course/<id>/final-exam - Get final exam quiz
@academy_bp.route('/course/<int:course_id>/final-exam', methods=['GET'])
@token_required
def get_final_exam(current_user, course_id):
    quiz = Quiz.query.filter_by(course_id=course_id, module_id=None).first()
    
    if not quiz:
        return jsonify({'error': 'Final exam not found'}), 404
    
    questions_data = []
    for question in sorted(quiz.questions, key=lambda q: q.order_index):
        options_data = [{'id': o.id, 'text': o.text} for o in question.options]
        
        questions_data.append({
            'id': question.id,
            'text': question.text,
            'options': options_data
        })
    
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'min_pass_score': quiz.min_pass_score,
        'questions': questions_data
    }), 200

# GET /api/academy/modules/<id>/quiz - Get module quiz
@academy_bp.route('/modules/<int:module_id>/quiz', methods=['GET'])
@token_required
def get_module_quiz(current_user, module_id):
    quiz = Quiz.query.filter_by(module_id=module_id).first()
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    questions_data = []
    for question in sorted(quiz.questions, key=lambda q: q.order_index):
        options_data = [{'id': o.id, 'text': o.text} for o in question.options]
        
        questions_data.append({
            'id': question.id,
            'text': question.text,
            'options': options_data
        })
    
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'min_pass_score': quiz.min_pass_score,
        'questions': questions_data
    }), 200

# POST /api/academy/quiz/submit - Submit quiz answers
@academy_bp.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.json
    quiz_id = data.get('quiz_id')
    user_answers = data.get('answers', {})
    
    quiz = Quiz.query.get_or_404(quiz_id)
    
    score = 0
    total_questions = len(quiz.questions)
    results = []
    
    for question in quiz.questions:
        selected_option_id = user_answers.get(str(question.id)) or user_answers.get(question.id)
        correct_option = next((o for o in question.options if o.is_correct), None)
        
        is_correct = False
        if selected_option_id and correct_option and int(selected_option_id) == correct_option.id:
            score += 1
            is_correct = True
        
        results.append({
            'question_id': question.id,
            'is_correct': is_correct,
            'correct_option_id': correct_option.id if correct_option else None,
            'explanation': question.explanation
        })
    
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    passed = percentage >= quiz.min_pass_score
    
    # Save attempt
    attempt_count = UserQuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).count()
    attempt = UserQuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=percentage,
        passed=passed,
        attempt_number=attempt_count + 1
    )
    db.session.add(attempt)
    db.session.flush()
    
    # Save answers
    for res in results:
        q_id = res['question_id']
        selected_opt_id = user_answers.get(str(q_id)) or user_answers.get(q_id)
        
        answer_record = UserQuizAnswer(
            attempt_id=attempt.id,
            question_id=q_id,
            selected_option_id=int(selected_opt_id) if selected_opt_id else None,
            is_correct=res['is_correct']
        )
        db.session.add(answer_record)
    
    if passed:
        award_xp(current_user.id, 100)
    
    db.session.commit()
    
    return jsonify({
        'passed': passed,
        'score_percent': round(percentage, 1),
        'score': score,
        'total': total_questions,
        'results': results,
        'message': '🎉 Congratulations! You passed!' if passed else 'You need at least 70% to pass. Try again!'
    }), 200
