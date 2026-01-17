
import sqlite3
import pymysql
import os
import sys

# SQLite Source
sqlite_db_path = os.path.join(os.path.dirname(__file__), 'instance', 'tradesense.db')

# MySQL Target Defaults
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '2002' # UPDATED WITH USER PASSWORD
MYSQL_DB = 'tradesense'

def migrate():
    print(f"🔄 Starting Migration from SQLite -> MySQL...")
    print(f"📂 Source: {sqlite_db_path}")

    # 1. Connect to SQLite
    if not os.path.exists(sqlite_db_path):
        print("❌ SQLite DB not found!")
        return

    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    # 2. Connect to MySQL
    try:
        mysql_conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Connected to MySQL!")
    except Exception as e:
        print(f"❌ Failed to connect to MySQL: {e}")
        print("💡 TIP: If you have a password, please tell me so I can update the script.")
        return

    try:
        with mysql_conn.cursor() as cursor:
            # Create Database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
            cursor.execute(f"USE {MYSQL_DB}")
            
            # --- USERS ---
            print("➡️ Migrating Users...")
            sqlite_cur.execute("SELECT * FROM users")
            users = sqlite_cur.fetchall()
            for user in users:
                # Check duplication
                cursor.execute("SELECT id FROM users WHERE email = %s", (user['email'],))
                if not cursor.fetchone():
                    sql = """
                        INSERT INTO users (full_name, username, email, password_hash, role, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        user['full_name'], user['username'], user['email'], 
                        user['password_hash'], user['role'], user['created_at']
                    ))
            
            # Commit users first to get IDs if needed (assuming emails match)
            mysql_conn.commit()

            # --- ACCOUNTS ---
            print("➡️ Migrating Accounts...")
            sqlite_cur.execute("SELECT * FROM accounts")
            accounts = sqlite_cur.fetchall()
            
            # Get MySQL Account Columns dynamically to avoid errors
            cursor.execute("DESCRIBE accounts")
            mysql_acc_cols = [row['Field'] for row in cursor.fetchall()]

            for acc in accounts:
                sqlite_cur.execute("SELECT email FROM users WHERE id = ?", (acc['user_id'],))
                user_row = sqlite_cur.fetchone()
                if user_row:
                    email = user_row['email']
                    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                    mysql_user = cursor.fetchone()
                    
                    if mysql_user:
                        mysql_user_id = mysql_user['id']
                        
                        # Build Insert Dict dynamically
                        insert_data = {}
                        insert_data['user_id'] = mysql_user_id
                        
                        # Map common fields
                        common_fields = ['plan_name', 'initial_balance', 'current_balance', 'equity', 'daily_starting_equity', 'status', 'created_at']
                        for field in common_fields:
                            if field in mysql_acc_cols:
                                insert_data[field] = acc[field]
                        
                        # Map optional fields
                        if 'reason' in mysql_acc_cols: insert_data['reason'] = acc.get('reason')
                        if 'admin_note' in mysql_acc_cols: insert_data['admin_note'] = acc.get('admin_note')
                        if 'last_daily_reset' in mysql_acc_cols: insert_data['last_daily_reset'] = acc.get('last_daily_reset')

                        # Construct SQL
                        cols = ', '.join(insert_data.keys())
                        placeholders = ', '.join(['%s'] * len(insert_data))
                        sql = f"INSERT INTO accounts ({cols}) VALUES ({placeholders})"
                        
                        cursor.execute(sql, list(insert_data.values()))
                        
                        # Capture the new Account ID for Trades
                        new_account_id = cursor.lastrowid

                        # --- TRADES (Nested to link to correct Account) ---
                        if new_account_id:
                            sqlite_cur.execute("SELECT * FROM trades WHERE account_id = ?", (acc['id'],))
                            trades = sqlite_cur.fetchall()
                            if trades:
                                # Get MySQL Trade Columns
                                cursor.execute("DESCRIBE trades")
                                mysql_trade_cols = [row['Field'] for row in cursor.fetchall()]
                                
                                for trade in trades:
                                    t_data = {}
                                    t_data['account_id'] = new_account_id
                                    t_data['user_id'] = mysql_user_id
                                    
                                    # Copy fields that exist in both
                                    full_trade_fields = ['symbol', 'side', 'quantity', 'price', 'trade_type', 'amount', 'entry_price', 'exit_price', 'stop_loss', 'take_profit', 'commission', 'swap', 'notes', 'status', 'pnl', 'timestamp', 'created_at', 'closed_at']
                                    
                                    for f in full_trade_fields:
                                        if f in mysql_trade_cols and f in trade.keys():
                                            t_data[f] = trade[f]
                                    
                                    t_cols = ', '.join(t_data.keys())
                                    t_holders = ', '.join(['%s'] * len(t_data))
                                    t_sql = f"INSERT INTO trades ({t_cols}) VALUES ({t_holders})"
                                    cursor.execute(t_sql, list(t_data.values()))

            mysql_conn.commit()
            print("✅ Migration Complete! Users, Accounts (matched columns), and Trades added to MySQL.")

    except Exception as e:
        print(f"❌ Migration Error: {e}")
    finally:
        mysql_conn.close()
        sqlite_conn.close()

if __name__ == "__main__":
    migrate()
