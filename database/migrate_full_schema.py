"""
Migration Script - Full SQL Integration
Applique le schéma complet à la base de données existante
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'tradesense.db')

def run_migration():
    print("🔄 Début de la migration SQL...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Lire le fichier schema
        schema_path = os.path.join(os.path.dirname(__file__), 'full_schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Exécuter toutes les commandes SQL
        cursor.executescript(schema_sql)
        
        conn.commit()
        print("✅ Migration SQL réussie!")
        
        # Afficher les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("\n📋 Tables dans la base de données:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} enregistrements")
        
        # Vérifier les vues
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = cursor.fetchall()
        print("\n👁️ Vues créées:")
        for view in views:
            print(f"   - {view[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("\n🎉 Base de données prête pour l'intégration SQL complète!")
    else:
        print("\n⚠️ La migration a échoué. Vérifiez les erreurs ci-dessus.")
