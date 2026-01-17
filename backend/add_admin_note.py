"""
Database migration to add admin_note column to accounts table
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'tradesense.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add admin_note column
    cursor.execute('ALTER TABLE accounts ADD COLUMN admin_note TEXT')
    conn.commit()
    print("✅ Column 'admin_note' added successfully to 'accounts' table")
    
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("ℹ️  Column 'admin_note' already exists")
    else:
        print(f"❌ Error: {e}")
finally:
    if conn:
        conn.close()

