"""
Migration script to add last_daily_reset column to accounts table
"""
import sqlite3
import os
from datetime import datetime

# Path to database
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
db_path = os.path.join(instance_path, 'tradesense.db')

print(f"Checking database at: {db_path}")

if not os.path.exists(db_path):
    print("[ERROR] Database file not found!")
    exit(1)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info(accounts)")
    columns = [column[1] for column in cursor.fetchall()]
    
    print(f"Current columns in accounts table: {columns}")
    
    if 'last_daily_reset' in columns:
        print("[OK] Column 'last_daily_reset' already exists!")
    else:
        print("[+] Adding 'last_daily_reset' column...")
        
        # Add the column with a default value (using current date)
        cursor.execute("""
            ALTER TABLE accounts 
            ADD COLUMN last_daily_reset DATE
        """)
        
        # Update existing rows to use their created_at date as last_daily_reset
        cursor.execute("""
            UPDATE accounts 
            SET last_daily_reset = DATE(created_at)
            WHERE last_daily_reset IS NULL
        """)
        
        conn.commit()
        print("[OK] Column added successfully!")
        
    # Verify the change
    cursor.execute("PRAGMA table_info(accounts)")
    columns_after = [column[1] for column in cursor.fetchall()]
    print(f"Updated columns: {columns_after}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n[OK] Migration complete!")
