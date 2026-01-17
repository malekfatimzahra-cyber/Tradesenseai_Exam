import sqlite3
import json
import os

def export_raw_sqlite():
    db_path = "instance/tradesense.db"
    if not os.path.exists(db_path):
        print(f"❌ DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    data = {
        'users': [],
        'accounts': [],
        'trades': []
    }

    print("🔄 Exporting raw data from SQLite via sqlite3...")

    try:
        # Users
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            d = dict(row)
            # Add missing fields that the new models expect
            if 'username' not in d:
                d['username'] = d['email'].split('@')[0]
            data['users'].append(d)

        # Accounts
        cursor.execute("SELECT * FROM accounts")
        for row in cursor.fetchall():
            data['accounts'].append(dict(row))

        # Trades
        cursor.execute("SELECT * FROM trades")
        for row in cursor.fetchall():
            data['trades'].append(dict(row))

        with open('backup_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Exported {len(data['users'])} users, {len(data['accounts'])} accounts, {len(data['trades'])} trades")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_raw_sqlite()
