from app import app
from models import db, User, Post, Comment, PostLike
from datetime import datetime, timedelta
import random

def seed_community_data():
    with app.app_context():
        # Ensure tables exist (specifically new Post/Comment tables)
        db.create_all()
        print("Seeding community posts...")
        
        # Get existing users
        users = User.query.all()
        if not users:
            print("No users found! Please run seed_demo_data.py first.")
            return

        # Map generic mock authors to specific real users for consistency
        # Try to find specific users, otherwise fallback to random
        def get_user(name_part):
            u = next((u for u in users if name_part.lower() in u.full_name.lower()), None)
            return u if u else random.choice(users)

        yassine = get_user("Yassine")
        salma = get_user("Salma")
        mehdi = get_user("Mehdi")
        target_users = [yassine, salma, mehdi]

        # Mock Posts Data
        mock_posts_data = [
            {
                "author": yassine,
                "content": "Position LONG BTC opened at 44,250$. Target: 46,500$. Stop Loss: 43,800$. Breakout confirmed with massive volume. #Bitcoin #CryptoTrading",
                "tags": "BTC",
                "created_ago": 2, # hours
                "likes": 12, # realistic number for small userbase
                "comments": [
                    "Great entry point!", "Following this one.", "What leverage are you using?"
                ]
            },
            {
                "author": salma,
                "content": "Question for experts: How do you properly calculate Stop Loss placement on volatile pairs like EUR/USD? Thanks for the tips! 🙏",
                "tags": "Forex",
                "created_ago": 4,
                "likes": 8,
                "comments": [
                    "Use ATR indicator.", "Always look at previous pivotal lows.", "Depends on your risk appetite."
                ]
            },
            {
                "author": mehdi,
                "content": "Market Analysis: Casablanca Stock Exchange showing bullish signals on IAM and Attijariwafa Bank. Institutional volume increasing significantly. #CasablancaStockExchange #IAM",
                "tags": "IAM",
                "created_ago": 6,
                "likes": 20,
                "comments": [
                    "IAM is definitely looking strong.", "Good catch!", "Agreed, volume profile confirms it."
                ]
            }
        ]

        for post_data in mock_posts_data:
            # Check if post content already exists to avoid dupes
            exists = Post.query.filter_by(content=post_data["content"]).first()
            if exists:
                print(f"Skipping existing post by {post_data['author'].full_name}")
                continue

            # Create Post
            p = Post(
                user_id=post_data["author"].id,
                content=post_data["content"],
                tags=post_data["tags"],
                created_at=datetime.utcnow() - timedelta(hours=post_data["created_ago"])
            )
            db.session.add(p)
            db.session.flush() # get ID

            # Create Likes (Scatter them among users)
            # Ensure post has 'likes' count representation if we want, 
            # though model computes len(post.likes). 
            # So we create PostLike entries.
            potential_likers = [u for u in users if u.id != p.user_id]
            # Pick random subset
            likers = random.sample(potential_likers, k=min(len(potential_likers), post_data["likes"]))
            
            for liker in likers:
                l = PostLike(user_id=liker.id, post_id=p.id)
                db.session.add(l)

            # Create Comments
            for i, comment_text in enumerate(post_data["comments"]):
                commenter = random.choice(users)
                c = Comment(
                    post_id=p.id,
                    user_id=commenter.id,
                    content=comment_text,
                    created_at=p.created_at + timedelta(minutes=random.randint(5, 60))
                )
                db.session.add(c)

        db.session.commit()
        print("Community data seeded successfully!")

if __name__ == "__main__":
    seed_community_data()
