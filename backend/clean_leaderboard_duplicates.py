"""
Clean leaderboard - Keep only best account per user (no duplicates)
"""
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root', 
    password='2002',
    database='tradesense'
)

try:
    with conn.cursor() as cursor:
        print("=" * 60)
        print("🔧 CLEANING LEADERBOARD - Removing duplicate users")
        print("=" * 60)
        
        # Step 1: Find duplicate users
        cursor.execute("""
            SELECT user_id, COUNT(*) as count, MAX(profit) as best_profit
            FROM leaderboard
            WHERE period = 'ALL_TIME'
            GROUP BY user_id
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        
        print(f"\n📊 Found {len(duplicates)} users with multiple entries:")
        for dup in duplicates:
            print(f"   user_id={dup[0]}: {dup[1]} entries, best profit: ${dup[2]:,.2f}")
        
        # Step 2: For each user, keep only the entry with highest profit
        for dup in duplicates:
            user_id = dup[0]
            
            # Find the best entry
            cursor.execute("""
                SELECT id FROM leaderboard 
                WHERE user_id = %s AND period = 'ALL_TIME'
                ORDER BY profit DESC
                LIMIT 1
            """, (user_id,))
            best_entry = cursor.fetchone()
            
            if best_entry:
                # Delete all other entries for this user
                cursor.execute("""
                    DELETE FROM leaderboard 
                    WHERE user_id = %s AND period = 'ALL_TIME' AND id != %s
                """, (user_id, best_entry[0]))
                deleted = cursor.rowcount
                print(f"   ✓ Kept best entry #{best_entry[0]}, deleted {deleted} duplicates")
        
        conn.commit()
        
        # Step 3: Re-rank all entries
        print("\n🔄 Re-ranking entries...")
        cursor.execute("SET @rank = 0")
        cursor.execute("""
            UPDATE leaderboard
            SET ranking = (@rank := @rank + 1)
            WHERE period = 'ALL_TIME'
            ORDER BY profit DESC
        """)
        conn.commit()
        
        # Step 4: Show final top 10
        cursor.execute("""
            SELECT ranking, username, profit, user_id
            FROM leaderboard
            WHERE period = 'ALL_TIME'
            ORDER BY ranking
            LIMIT 10
        """)
        
        print("\n" + "=" * 60)
        print("🏆 FINAL TOP 10 ELITE HALL OF FAME:")
        print("=" * 60)
        for row in cursor.fetchall():
            print(f"   #{row[0]}: {row[1]} - ${row[2]:,.2f}")
        
        print("\n✅ Leaderboard cleaned successfully!")
        
finally:
    conn.close()
