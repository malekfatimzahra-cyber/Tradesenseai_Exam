
import os
import sys
from sqlalchemy import text

# Ensure we can import from the backend package
sys.path.append(os.getcwd())

# Import from the package init (Application Factory)
# NOT from app.py which is legacy/sqlite
try:
    from backend import create_app, db
except ImportError:
    # If running from inside backend/ dir
    sys.path.append(os.path.join(os.getcwd(), '..'))
    from backend import create_app, db

def fix_schema():
    print("Starting MySQL schema fix for 'accounts' table...")
    
    # Initialize the app with development config (MySQL)
    app = create_app('development')
    
    with app.app_context():
        print(f"Connected to DB: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
        
        # 1. Check existing columns
        try:
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('accounts')]
            print(f"Current columns in 'accounts': {columns}")
            
            # 2. Add 'reason' if missing
            if 'reason' not in columns:
                print("Adding missing column: reason")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE accounts ADD COLUMN reason VARCHAR(255) NULL"))
                    conn.commit()
                print("Added 'reason'.")
            else:
                print("'reason' column already exists.")

            # 3. Add 'admin_note' if missing
            if 'admin_note' not in columns:
                print("Adding missing column: admin_note")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE accounts ADD COLUMN admin_note TEXT NULL"))
                    conn.commit()
                print("Added 'admin_note'.")
            else:
                print("'admin_note' column already exists.")

            # 4. Add 'last_daily_reset' if missing
            if 'last_daily_reset' not in columns:
                print("Adding missing column: last_daily_reset")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE accounts ADD COLUMN last_daily_reset DATE DEFAULT (CURRENT_DATE)"))
                    conn.commit()
                print("Added 'last_daily_reset'.")
            else:
                print("'last_daily_reset' column already exists.")

            print("Schema fix completed successfully.")
            
        except Exception as e:
            print(f"Error fixing schema: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_schema()
