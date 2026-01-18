from flask import Blueprint, request, jsonify
from models import db, Course, Module, Lesson, Quiz, Question, Option, UserLessonProgress, UserCourseProgress, UserXP, UserBadge, Badge, UserQuizAttempt, UserQuizAnswer
from middleware import token_required
import datetime
from sqlalchemy import text

academy_bp = Blueprint('academy', __name__)

# --- HELPERS ---

def award_xp(user_id, amount):
    user_xp = UserXP.query.get(user_id)
    if not user_xp:
        user_xp = UserXP(user_id=user_id, total_xp=0, level_title="Novice")
        db.session.add(user_xp)
    
    user_xp.total_xp += amount
    
    # Simple leveling logic
    if user_xp.total_xp >= 5000:
        user_xp.level_title = "Elite Trader"
    elif user_xp.total_xp >= 2000:
        user_xp.level_title = "Gold Pro"
    elif user_xp.total_xp >= 500:
        user_xp.level_title = "Silver Student"
        
    db.session.commit()
    return user_xp

def calculate_course_progress(user_id, course_id):
    """Calculate course progress based on completed lessons and quizzes."""
    course = Course.query.get(course_id)
    if not course:
        return 0, False
    
    total_items = 0
    completed_items = 0
    
    for module in course.modules:
        # Each lesson is an item
        total_items += len(module.lessons)
        # Each module quiz is an item
        module_quizzes = Quiz.query.filter_by(module_id=module.id).all()
        total_items += len(module_quizzes)
        
        for lesson in module.lessons:
            lp = UserLessonProgress.query.filter_by(user_id=user_id, lesson_id=lesson.id, is_completed=True).first()
            if lp:
                completed_items += 1
        
        for quiz in module_quizzes:
            qa = UserQuizAttempt.query.filter_by(user_id=user_id, quiz_id=quiz.id, passed=True).first()
            if qa:
                completed_items += 1
                
    if total_items == 0:
        return 0, False
        
    progress_percent = int((completed_items / total_items) * 100)
    is_completed = progress_percent >= 100
    
    return progress_percent, is_completed

def update_course_progress(user_id, course_id):
    progress_percent, is_completed = calculate_course_progress(user_id, course_id)
    
    progress = UserCourseProgress.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not progress:
        progress = UserCourseProgress(user_id=user_id, course_id=course_id)
        db.session.add(progress)
    
    progress.progress_percent = progress_percent
    progress.is_completed = is_completed
    progress.last_accessed = datetime.datetime.utcnow()
    db.session.commit()
    return progress_percent, is_completed

# --- ROUTES ---

@academy_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    """List all courses with user progress + i18n support"""
    lang = request.args.get('lang', 'fr')
    category = request.args.get('category')
    level = request.args.get('level')
    search = request.args.get('search')
    
    # Base query with i18n join
    sql = """
        SELECT c.*, 
               COALESCE(ct.title, c.title) as translated_title,
               COALESCE(ct.description, c.description) as translated_description
        FROM courses c
        LEFT JOIN course_translations ct ON c.id = ct.course_id AND ct.lang = :lang
        WHERE 1=1
    """
    params = {'lang': lang}
    
    if category and category != 'ALL':
        sql += " AND c.category = :category"
        params['category'] = category
    
    if level and level != 'ALL':
        sql += " AND c.level = :level"
        params['level'] = level
        
    if search:
        sql += " AND (COALESCE(ct.title, c.title) LIKE :search OR COALESCE(ct.description, c.description) LIKE :search)"
        params['search'] = f"%{search}%"
        
    result_proxy = db.session.execute(text(sql), params)
    
    courses_list = []
    for row in result_proxy:
        # Reconstruct dict manually from row
        c_dict = {
            'id': row.id,
            'title': row.translated_title,
            'description': row.translated_description,
            'category': row.category,
            'level': row.level,
            # 'price': row.price, # Removed: Not in User Model
            'is_premium': row.is_premium,
            # 'total_students': row.total_students, # Removed: Not in User Model
            # 'rating': row.rating, # Removed: Not in User Model
            'duration_minutes': row.duration_minutes,
            'thumbnail_url': row.thumbnail_url or row.cover,
            'duration': f"{row.duration_minutes} min",
            'premium': row.is_premium
        }
        
        progress_percent, is_completed = calculate_course_progress(current_user.id, row.id)
        c_dict['progress'] = progress_percent
        c_dict['is_completed'] = is_completed
        courses_list.append(c_dict)
        
    return jsonify(courses_list), 200

@academy_bp.route('/courses/<int:course_id>', methods=['GET'])
@token_required
def get_course_details(current_user, course_id):
    """Get full course structure with i18n"""
    lang = request.args.get('lang', 'fr')
    
    # 1. Fetch Course with Translation
    sql_course = """
        SELECT c.*, 
               COALESCE(ct.title, c.title) as translated_title,
               COALESCE(ct.description, c.description) as translated_description
        FROM courses c
        LEFT JOIN course_translations ct ON c.id = ct.course_id AND ct.lang = :lang
        WHERE c.id = :course_id
    """
    course_row = db.session.execute(text(sql_course), {'course_id': course_id, 'lang': lang}).fetchone()
    
    if not course_row:
        return jsonify({'message': 'Course not found'}), 404
        
    data = {
        'id': course_row.id,
        'title': course_row.translated_title,
        'description': course_row.translated_description,
        'category': course_row.category,
        'level': course_row.level,
        'is_premium': course_row.is_premium,
        'thumbnail_url': course_row.thumbnail_url or course_row.cover,
        'duration': f"{course_row.duration_minutes} min",
        'premium': course_row.is_premium
    }
    
    progress_percent, is_completed = calculate_course_progress(current_user.id, course_id)
    data['progress'] = progress_percent
    data['is_completed'] = is_completed

    # 2. Fetch Modules with Translation
    sql_modules = """
        SELECT m.*, COALESCE(mt.title, m.title) as translated_title
        FROM modules m
        LEFT JOIN module_translations mt ON m.id = mt.module_id AND mt.lang = :lang
        WHERE m.course_id = :course_id
        ORDER BY m.order_index
    """
    modules_rows = db.session.execute(text(sql_modules), {'course_id': course_id, 'lang': lang}).fetchall()
    
    modules_data = []
    
    for mod_row in modules_rows:
        m_dict = {
            'id': mod_row.id,
            'title': mod_row.translated_title,
            'lessons': []
        }
        
        # 3. Fetch Lessons with Translation
        sql_lessons = """
            SELECT l.*, COALESCE(lt.title, l.title) as translated_title
            FROM lessons l
            LEFT JOIN lesson_translations lt ON l.id = lt.lesson_id AND lt.lang = :lang
            WHERE l.module_id = :module_id
            ORDER BY l.order_index
        """
        lessons_rows = db.session.execute(text(sql_lessons), {'module_id': mod_row.id, 'lang': lang}).fetchall()
        
        for less_row in lessons_rows:
            lp = UserLessonProgress.query.filter_by(user_id=current_user.id, lesson_id=less_row.id).first()
            l_dict = {
                'id': less_row.id,
                'title': less_row.translated_title,
                'type': less_row.lesson_type, # ENUM might need conversion if accessing raw
                'duration': 10, # Default duration since column missing
                'is_completed': lp.is_completed if lp else False
            }
            m_dict['lessons'].append(l_dict)
        
        # 4. Fetch Module Quiz (Translations handled in get_module_quiz)
        quiz = Quiz.query.filter_by(module_id=mod_row.id).first()
        if quiz:
            # We just need ID and basic info here, translation is fetched when taking quiz
            qa = UserQuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz.id, passed=True).first()
            m_dict['is_quiz_completed'] = True if qa else False
            m_dict['quiz_id'] = quiz.id
            
        modules_data.append(m_dict)
        
    data['modules'] = modules_data
    return jsonify(data), 200

@academy_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
@token_required
def get_lesson(current_user, lesson_id):
    """Fetch lesson content with i18n"""
    lang = request.args.get('lang', 'fr')
    
    sql = """
        SELECT l.*, 
               COALESCE(lt.title, l.title) as translated_title,
               COALESCE(lt.content, l.content) as translated_content
        FROM lessons l
        LEFT JOIN lesson_translations lt ON l.id = lt.lesson_id AND lt.lang = :lang
        WHERE l.id = :lesson_id
    """
    row = db.session.execute(text(sql), {'lesson_id': lesson_id, 'lang': lang}).fetchone()
    
    if not row:
        return jsonify({'message': 'Lesson not found'}), 404
        
    # Handle access tracking
    lp = UserLessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if not lp:
        lp = UserLessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.session.add(lp)
    
    lp.last_accessed = datetime.datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': row.id,
        'title': row.translated_title,
        'content': row.translated_content,
        'type': row.lesson_type, # Might need enum handling
        'video_url': row.video_url,
        'duration_minutes': 10 # Default
    }), 200

@academy_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@token_required
def complete_lesson(current_user, lesson_id):
    """Mark lesson as completed"""
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
    
    course_id = lesson.module.course_id
    progress_percent, is_completed = update_course_progress(current_user.id, course_id)
    
    return jsonify({
        'success': True,
        'message': 'Lesson completed',
        'course_progress': progress_percent
    }), 200

@academy_bp.route('/modules/<int:module_id>/quiz', methods=['GET'])
@token_required
def get_module_quiz(current_user, module_id):
    """Fetch quiz for a module with i18n"""
    lang = request.args.get('lang', 'fr')
    
    # Fetch translated quiz title
    sql_quiz = """
        SELECT q.*, COALESCE(qt.title, q.title) as translated_title
        FROM quizzes q
        LEFT JOIN quiz_translations qt ON q.id = qt.quiz_id AND qt.lang = :lang
        WHERE q.module_id = :module_id
    """
    quiz_row = db.session.execute(text(sql_quiz), {'module_id': module_id, 'lang': lang}).fetchone()
    
    if not quiz_row:
        return jsonify({'error': 'Quiz not found'}), 404
        
    # Fetch questions
    sql_questions = """
        SELECT q.*, COALESCE(qt.text, q.text) as translated_text
        FROM questions q
        LEFT JOIN question_translations qt ON q.id = qt.question_id AND qt.lang = :lang
        WHERE q.quiz_id = :quiz_id
        ORDER BY q.order_index
    """
    questions_rows = db.session.execute(text(sql_questions), {'quiz_id': quiz_row.id, 'lang': lang}).fetchall()
    
    questions_data = []
    for q_row in questions_rows:
        # Fetch options
        sql_options = """
            SELECT o.*, COALESCE(ot.text, o.text) as translated_text
            FROM options o
            LEFT JOIN option_translations ot ON o.id = ot.option_id AND ot.lang = :lang
            WHERE o.question_id = :question_id
        """
        options_rows = db.session.execute(text(sql_options), {'question_id': q_row.id, 'lang': lang}).fetchall()
        
        options_data = [{'id': o.id, 'text': o.translated_text} for o in options_rows]
        
        questions_data.append({
            'id': q_row.id,
            'text': q_row.translated_text,
            'options': options_data
        })
        
    return jsonify({
        'id': quiz_row.id,
        'title': quiz_row.translated_title,
        'min_pass_score': quiz_row.min_pass_score,
        'questions': questions_data
    }), 200

@academy_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@token_required
def submit_quiz(current_user, quiz_id):
    """Submit quiz answers"""
    data = request.json
    user_answers = data.get('answers', {}) 
    
    quiz = Quiz.query.get_or_404(quiz_id)
    
    score = 0
    total_questions = len(quiz.questions)
    results = []
    
    # We still need standard logic for grading, translation doesn't affect correctness
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
            'explanation': question.explanation # Could be i18n'd but keep simple for now
        })
        
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    passed = percentage >= quiz.min_pass_score
    
    attempt_count = UserQuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).count()
    attempt = UserQuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=percentage,
        passed=passed,
        attempt_number=attempt_count + 1
    )
    db.session.add(attempt)
    db.session.flush() # Get attempt ID

    # Save detailed answers
    for res in results:
        # res has: question_id, is_correct, explanation
        # we need selected_option_id
        # user_answers key might be string or int
        q_id_str = str(res['question_id'])
        q_id_int = res['question_id']
        selected_opt_id = user_answers.get(q_id_str) or user_answers.get(q_id_int)
        
        answer_record = UserQuizAnswer(
            attempt_id=attempt.id,
            question_id=res['question_id'],
            selected_option_id=int(selected_opt_id) if selected_opt_id else None,
            is_correct=res['is_correct']
        )
        db.session.add(answer_record)
    
    if passed:
        award_xp(current_user.id, 100)
        
    db.session.commit()
    
    if quiz.module_id:
        course_id = Module.query.get(quiz.module_id).course_id
        update_course_progress(current_user.id, course_id)
    elif quiz.course_id:
        update_course_progress(current_user.id, quiz.course_id)

    return jsonify({
        'passed': passed,
        'score_percent': round(percentage, 1),
        'results': results,
        'message': 'Success!' if passed else 'You failed. Try again.'
    }), 200

@academy_bp.route('/quizzes/<int:quiz_id>/attempts', methods=['GET'])
@token_required
def get_quiz_attempts(current_user, quiz_id):
    """Get history of attempts for a quiz"""
    attempts = UserQuizAttempt.query.filter_by(
        user_id=current_user.id, 
        quiz_id=quiz_id
    ).order_by(UserQuizAttempt.created_at.desc()).all()
    
    return jsonify([{
        'id': a.id,
        'score': a.score,
        'passed': a.passed,
        'date': a.created_at.isoformat()
    } for a in attempts]), 200
