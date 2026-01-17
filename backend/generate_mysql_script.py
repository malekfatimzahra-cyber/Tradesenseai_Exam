
import sqlite3
import os
from datetime import datetime

# Path to the SQLite DB
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'tradesense.db')
output_file = os.path.join(os.path.dirname(__file__), '..', 'INSERT_USERS.sql')

def escape_string(s):
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"

def generate_sql():
    print(f"Reading from: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- SQL Script to insert 10 Moroccan Users into MySQL\n")
        f.write("-- Run this in MySQL Workbench\n\n")
        f.write("USE tradesense;\n\n") # Assuming DB name is tradesense
        
        # 1. USERS
        f.write("-- 1. Insert Users\n")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        # Get columns
        columns = [description[0] for description in cursor.description]
        
        user_mapping = {} # Old ID -> New ID (if needed, but we try to keep same)
        
        for row in users:
            row_dict = dict(zip(columns, row))
            
            # Skip existing users in your screenshot (ids 1-5) if they conflict?
            # Better to use INSERT IGNORE or ON DUPLICATE KEY UPDATE
            # But simpler: just Insert.
            
            vals = []
            for col in columns:
                vals.append(escape_string(row_dict[col]))
            
            f.write(f"INSERT INTO users ({', '.join(columns)}) VALUES ({', '.join(vals)});\n")

        # 2. ACCOUNTS (Check table name, usually 'accounts')
        f.write("\n-- 2. Insert Accounts\n")
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
        acc_cols = [description[0] for description in cursor.description]
        
        for row in accounts:
            row_dict = dict(zip(acc_cols, row))
            vals = []
            for col in acc_cols:
                val = row_dict[col]
                # Fix boolean/None for MySQL
                if val is None:
                    vals.append("NULL")
                else:
                    vals.append(escape_string(val))
            
            f.write(f"INSERT INTO accounts ({', '.join(acc_cols)}) VALUES ({', '.join(vals)});\n")

        # 3. TRADES
        f.write("\n-- 3. Insert Trades\n")
        cursor.execute("SELECT * FROM trades")
        trades = cursor.fetchall()
        trade_cols = [description[0] for description in cursor.description]
        
        for row in trades:
            row_dict = dict(zip(trade_cols, row))
            vals = []
            for col in trade_cols:
                val = row_dict[col]
                if val is None:
                    vals.append("NULL")
                else:
                    vals.append(escape_string(val))
            
            f.write(f"INSERT INTO trades ({', '.join(trade_cols)}) VALUES ({', '.join(vals)});\n")

    conn.close()
    print(f"✅ SQL Script generated at: {output_file}")

if __name__ == "__main__":
    generate_sql()
