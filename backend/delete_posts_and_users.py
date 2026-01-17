from app import app, db
from models import Post, User, Comment, PostLike

def delete_data():
    print("Cleaning up Community Data...")
    
    try:
        # 1. Delete all posts
        try:
             PostLike.query.delete()
             Comment.query.delete()
        except:
             pass 
        
        num_posts = Post.query.delete()
        print(f"   -> Deleted {num_posts} posts.")
        
        # 2. Delete specific users from the screenshot
        target_users = ["Yassine Benali", "Salma Bennani", "Mehdi Jettou", "Youssef Bennani", "Sara El Amrani", "Mehdi Alaoui"]
        for name in target_users:
            u = User.query.filter_by(full_name=name).first()
            if u:
                db.session.delete(u)
                print(f"   -> Deleted user: {name}")
                
        db.session.commit()
        print("Cleanup complete!")
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()

if __name__ == "__main__":
    with app.app_context():
        delete_data()
