
from app import app
import json

def test_api():
    print("=== TESTING API ENDPOINTS LOCALLY ===")
    
    with app.test_client() as client:
        # Mock auth token? 
        # The endpoints require @token_required. We need to mock that or bypass it?
        # Alternatively, we can just call the view function directly if we could, but routing is easier.
        # Let's try to login first if possible, or just hack the middleware?
        # Simpler: The user said "backend running". I will assume standard requests work if I have a token.
        
        # Actually... let's mock the token in the headers. 
        # But I don't have a valid token handy without logging in.
        # I'll create a fake user or just query a known user.
        
        # Let's try to login as a test user
        # login_res = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
        # This is flaky if user doesn't exist.
        
        # Plan B: Use a script that imports 'get_course_details' and runs it with a mock user.
        pass

from models import User
from flask import Flask, request

def debug_direct_function():
    print("\n--- Direct Function Call Debug ---")
    with app.app_context():
        # Get a user (any user)
        user = User.query.first()
        if not user:
            print("❌ No users found in DB. Cannot test authenticated route.")
            return

        print(f"👤 Using User: {user.id} ({user.email})")
        
        # We need to manually invoke the logic from academy.py 
        # But since it's inside a route with request.args, we need a request context.
        
        with app.test_request_context('/api/academy/courses/9?lang=fr'):
            from academy import get_course_details
            
            # The 'get_course_details' expects (current_user, course_id) because of the @token_required decorator wrapper?
            # Wait, @token_required passes current_user as first arg.
            # But we can't easily call the decorated function directly without the wrapper logic sometimes.
            # However, usually decorated_function(current_user, *args) is how it works if it passes it down.
            
            # Let's checking academy.py decorator usage:
            # @academy_bp.route(...)
            # @token_required
            # def get_course_details(current_user, course_id):
            
            # If I call get_course_details(user, 9), it might work if the wrapper is stripped or if I call the underlying?
            # No, in Flask, the function is replaced by the wrapper.
            # BUT, the original function is often available? Maybe not.
            
            # Let's just reproduce the SQL logic here. That's safer and verifies the data retrieval logic.
            
            # COPY OF LOGIC FROM academy.py (get_course_details)
            lang = 'fr' 
            course_id = 9
            
            from models import db
            from sqlalchemy import text
            
            print(f"🔎 Fetching Course {course_id} for Lang '{lang}'...")
            
            # 1. Course
            sql_course = text("""
                SELECT c.*, 
                       COALESCE(ct.title, c.title) as translated_title,
                       COALESCE(ct.description, c.description) as translated_description
                FROM courses c
                LEFT JOIN course_translations ct ON c.id = ct.course_id AND ct.lang = :lang
                WHERE c.id = :course_id
            """)
            course_row = db.session.execute(sql_course, {'course_id': course_id, 'lang': lang}).fetchone()
            
            if not course_row:
                print("❌ Course Query returned None")
            else:
                print(f"✅ Course Query Result: ID={course_row.id}, Title='{course_row.translated_title}'")
                
            # 2. Modules
            sql_modules = text("""
                SELECT m.*, COALESCE(mt.title, m.title) as translated_title
                FROM modules m
                LEFT JOIN module_translations mt ON m.id = mt.module_id AND mt.lang = :lang
                WHERE m.course_id = :course_id
                ORDER BY m.order_index
            """)
            modules_rows = db.session.execute(sql_modules, {'course_id': course_id, 'lang': lang}).fetchall()
            print(f"📦 Modules Found: {len(modules_rows)}")
            
            for m in modules_rows:
                print(f"   Module {m.id}: {m.translated_title}")
                
                # 3. Lessons
                sql_lessons = text("""
                    SELECT l.*, COALESCE(lt.title, l.title) as translated_title,
                           COALESCE(lt.content, l.content) as translated_content
                    FROM lessons l
                    LEFT JOIN lesson_translations lt ON l.id = lt.lesson_id AND lt.lang = :lang
                    WHERE l.module_id = :module_id
                    ORDER BY l.order_index
                """)
                l_rows = db.session.execute(sql_lessons, {'module_id': m.id, 'lang': lang}).fetchall()
                print(f"      -> {len(l_rows)} Lessons")
                for l in l_rows:
                    content_len = len(l.translated_content) if l.translated_content else 0
                    print(f"         - Lesson {l.id}: '{l.translated_title}' (Len: {content_len})")
                    if content_len == 0:
                        print("           ⚠️ WARNING: Content is empty!")

if __name__ == "__main__":
    debug_direct_function()
