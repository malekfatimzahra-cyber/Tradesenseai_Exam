"""
Script de Migration Complète - TradeSense AI
Crée toutes les tables si elles n'existent pas
"""

import sqlite3
import os
from datetime import datetime
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'tradesense.db')

def create_complete_schema():
    print("🔄 Création du schéma SQL complet...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # ========== 1. USERS TABLE ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                username VARCHAR(50),
                role VARCHAR(20) DEFAULT 'USER',
                balance FLOAT DEFAULT 0,
                status VARCHAR(20) DEFAULT 'PENDING',
                avatar VARCHAR(255),
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        # ========== 2. ACCOUNTS (CHALLENGES) ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_name VARCHAR(50) NOT NULL,
                initial_balance FLOAT NOT NULL,
                current_balance FLOAT NOT NULL,
                equity FLOAT NOT NULL,
                daily_starting_equity FLOAT NOT NULL,
                status VARCHAR(20) DEFAULT 'ACTIVE',
                reason TEXT,
                admin_note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_daily_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # ========== 3. TRADES ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                symbol VARCHAR(20) NOT NULL,
                type VARCHAR(10) NOT NULL,
                amount FLOAT NOT NULL,
                entry_price FLOAT NOT NULL,
                exit_price FLOAT,
                sl FLOAT,
                tp FLOAT,
                status VARCHAR(20) DEFAULT 'OPEN',
                pnl FLOAT DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # ========== 4. TRANSACTIONS ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_id INTEGER,
                amount FLOAT NOT NULL,
                currency VARCHAR(10) DEFAULT 'MAD',
                payment_method VARCHAR(20) NOT NULL,
                status VARCHAR(20) DEFAULT 'PENDING',
                transaction_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL
            )
        """)
        
        # ========== 5. USER_CHALLENGES (EXAM REQUIREMENT) ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_name VARCHAR(50) NOT NULL,
                amount FLOAT NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # ========== 6. SYSTEM_CONFIG ==========
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                key VARCHAR(100) PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("✅ Schéma de base créé!")
        
        # Maintenant appliquer les tables additionnelles
        schema_path = os.path.join(os.path.dirname(__file__), 'full_schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)
            conn.commit()
            print("✅ Tables additionnelles créées!")
        
        # Créer utilisateurs de démo si table vide
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            print("📝 Création des utilisateurs de démo...")
            
            # Hash passwords
            users_data = [
                ('Karim Trader', 'karim@trade.ma', '123456', 'karimtrader', 'USER'),
                ('Sara Admin', 'sara@admin.ma', 'admin123', 'saraadmin', 'ADMIN'),
                ('Boss Super', 'ceo@tradesense.ma', 'super123', 'ceo', 'SUPERADMIN'),
            ]
            
            for name, email, password, username, role in users_data:
                # Simple hash for demo (in production use proper bcrypt)
                password_hash = password  # Simplifié pour démo
                cursor.execute("""
                    INSERT INTO users (full_name, email, password_hash, username, role, balance, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE')
                """, (name, email, password_hash, username, role, 0 if role != 'SUPERADMIN' else 100000))
            
            conn.commit()
            print("✅ Utilisateurs de démo créés!")
        
        # Afficher statistiques
        print("\n📊 STATISTIQUES DE LA BASE:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   {table[0]}: {count} enregistrements")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = create_complete_schema()
    if success:
        print("\n🎉 Base de données complètement configurée!")
    else:
        print("\n⚠️ Échec de la migration.")
