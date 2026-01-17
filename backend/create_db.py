import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_db():
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    db_name = os.getenv('DB_NAME', 'tradesense')

    print(f"🔄 Attempting to create database '{db_name}' as {user}...")

    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port)
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.close()
        print(f"✅ Database '{db_name}' ensured.")
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

if __name__ == "__main__":
    create_db()
