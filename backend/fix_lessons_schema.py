
import os
import sys
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db

def fix_lessons_schema():
    print("Fixing 'lessons' table schema...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('lessons')]
            print(f"Current columns: {columns}")
            
            missing_cols = []
            
            if 'content_prompt' not in columns:
                missing_cols.append(('content_prompt', 'TEXT NULL'))
            
            if 'content' not in columns:
                missing_cols.append(('content', 'TEXT NULL'))
                
            if 'order' not in columns:
                missing_cols.append(('order', 'INTEGER DEFAULT 1'))
            
            with db.engine.connect() as conn:
                for col_name, sql_def in missing_cols:
                    print(f"Adding column: {col_name}...")
                    try:
                        # Use backticks for 'order' as it's a reserved keyword
                        if col_name == 'order':
                            conn.execute(text(f"ALTER TABLE lessons ADD COLUMN `{col_name}` {sql_def}"))
                        else:
                            conn.execute(text(f"ALTER TABLE lessons ADD COLUMN {col_name} {sql_def}"))
                        conn.commit()
                        print(f"  ✓ Added: {col_name}")
                    except Exception as e:
                        print(f"  Error adding {col_name}: {e}")
            
            print("Schema fix completed.")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    fix_lessons_schema()
