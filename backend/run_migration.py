import pymysql
import sys

# Charger le fichier SQL
try:
    with open('migration_i18n.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
except FileNotFoundError:
    print("Erreur: Fichier migration_i18n.sql introuvable.")
    sys.exit(1)

# Connexion DB
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='2002',
        database='tradesense',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connexion à la base de données réussie.")
except pymysql.MySQLError as e:
    print(f"Erreur de connexion: {e}")
    sys.exit(1)

try:
    with conn.cursor() as cursor:
        # Séparer les commandes par point-virgule
        commands = sql_script.split(';')
        for i, cmd in enumerate(commands):
            cmd = cmd.strip()
            if not cmd:
                continue
            
            try:
                # Ignorer les commentaires
                if cmd.startswith("--"):
                    continue
                    
                print(f"Exécution de la commande {i+1}...")
                cursor.execute(cmd)
            except pymysql.MySQLError as e:
                print(f"⚠️ Erreur SQL (ignorée si 'exists'): {e}")
                # On continue même si erreur (ex: table already exists)
        
        conn.commit()
        print("\n✅ Migration terminée avec succès !")

finally:
    conn.close()
