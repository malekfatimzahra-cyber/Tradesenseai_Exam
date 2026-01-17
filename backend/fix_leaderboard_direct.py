"""
Quick fix for leaderboard - Remove orphan entries
"""
import pymysql

# Direct database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='2002',
    database='tradesense',
    charset='utf8mb4'
)

try:
    with conn.cursor() as cursor:
        # Check current state
        cursor.execute("""
            SELECT l.id, l.username, l.user_id, 
                   (SELECT COUNT(*) FROM users u WHERE u.id = l.user_id) AS user_exists
            FROM leaderboard l
            ORDER BY l.ranking
            LIMIT 15
        """)
        
        print("Current leaderboard state:")
        for row in cursor.fetchall():
            status = "✓" if row[3] > 0 else "❌ INVALID"
            print(f"  #{row[0]} {row[1]} (user_id={row[2]}) - {status}")
        
        # Delete invalid entries
        cursor.execute("""
            DELETE l FROM leaderboard l
            LEFT JOIN users u ON u.id = l.user_id
            WHERE u.id IS NULL
        """)
        deleted = cursor.rowcount
        print(f"\n🗑️ Deleted {deleted} invalid entries")
        
        conn.commit()
        
        # Re-rank remaining entries
        cursor.execute("""
            SET @rank = 0;
        """)
        cursor.execute("""
            UPDATE leaderboard
            SET ranking = (@rank := @rank + 1)
            WHERE period = 'ALL_TIME'
            ORDER BY profit DESC
        """)
        conn.commit()
        
        # Show final result
        cursor.execute("""
            SELECT ranking, username, profit, user_id 
            FROM leaderboard 
            WHERE period = 'ALL_TIME' 
            ORDER BY ranking 
            LIMIT 10
        """)
        
        print("\n🏆 NEW TOP 10 LEADERBOARD:")
        print("-" * 50)
        for row in cursor.fetchall():
            print(f"  #{row[0]}: {row[1]} - ${row[2]:,.2f}")
        
        print("\n✅ Leaderboard fixed!")
        
finally:
    conn.close()
