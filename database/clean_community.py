"""
Script de Nettoyage - Community
Supprime tous les posts, comments, et likes existants
"""

import sqlite3
import os

# Correct path to the Flask instance database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'instance', 'tradesense.db')

def clean_community_data():
    print("🧹 Nettoyage de la section Community...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Supprimer tous les likes
        cursor.execute("DELETE FROM post_likes")
        likes_deleted = cursor.rowcount
        print(f"   ❌ {likes_deleted} likes supprimés")
        
        # Supprimer tous les commentaires
        cursor.execute("DELETE FROM comments")
        comments_deleted = cursor.rowcount
        print(f"   ❌ {comments_deleted} commentaires supprimés")
        
        # Supprimer tous les posts
        cursor.execute("DELETE FROM posts")
        posts_deleted = cursor.rowcount
        print(f"   ❌ {posts_deleted} posts supprimés")
        
        # Reset les compteurs auto-increment (Optionnel, ignoré si erreur)
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='posts'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='comments'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='post_likes'")
        except:
            pass
        
        conn.commit()
        
        # Vérification
        cursor.execute("SELECT COUNT(*) FROM posts")
        remaining_posts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM comments")
        remaining_comments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM post_likes")
        remaining_likes = cursor.fetchone()[0]
        
        print("\n✅ Nettoyage terminé!")
        print(f"   Posts restants: {remaining_posts}")
        print(f"   Comments restants: {remaining_comments}")
        print(f"   Likes restants: {remaining_likes}")
        
        if remaining_posts == 0 and remaining_comments == 0 and remaining_likes == 0:
            print("\n🎉 La section Community est maintenant complètement vide et prête!")
            return True
        else:
            print("\n⚠️ Certaines données persistent encore.")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    clean_community_data()
