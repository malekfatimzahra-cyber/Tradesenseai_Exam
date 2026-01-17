import sqlite3
import os

# Path from backend/config.py
db_path = os.path.join('backend', 'instance', 'tradesense.db')

print(f"Connecting to database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(accounts)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'last_daily_reset' in columns:
        print("Column 'last_daily_reset' already exists.")
    else:
        print("Adding missing column 'last_daily_reset'...")
        cursor.execute("ALTER TABLE accounts ADD COLUMN last_daily_reset DATE")
        conn.commit()
        print("Successfully added column.")
        
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
