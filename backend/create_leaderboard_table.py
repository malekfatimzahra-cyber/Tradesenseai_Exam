
import os
import sys
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db

def create_leaderboard_table():
    print("Creating 'leaderboard' table in MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Check if exists
            inspector = db.inspect(db.engine)
            if 'leaderboard' in inspector.get_table_names():
                print("Table 'leaderboard' already exists.")
            else:
                # Create table from model
                # Doing it manually via raw SQL to ensure precise control over types if needed,
                # or just db.create_all() but that tries to create ALL tables.
                # Better to use raw SQL for a single migration to avoid side effects.
                sql = """
                CREATE TABLE leaderboard (
                    id INTEGER NOT NULL AUTO_INCREMENT, 
                    user_id INTEGER, 
                    username VARCHAR(50) NOT NULL, 
                    country VARCHAR(5), 
                    avatar_url VARCHAR(255), 
                    profit FLOAT, 
                    roi FLOAT, 
                    win_rate FLOAT, 
                    funded_amount FLOAT, 
                    ranking INTEGER, 
                    period VARCHAR(20), 
                    is_visible BOOLEAN, 
                    updated_at DATETIME, 
                    PRIMARY KEY (id), 
                    FOREIGN KEY(user_id) REFERENCES users (id)
                );
                """
                with db.engine.connect() as conn:
                    conn.execute(text(sql))
                    # Add default if missing in model definition handled by python
                print("Table 'leaderboard' created successfully.")
                
        except Exception as e:
            print(f"Error creating table: {e}")

if __name__ == '__main__':
    create_leaderboard_table()
