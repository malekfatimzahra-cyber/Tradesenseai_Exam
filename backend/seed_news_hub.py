
import os
import sys
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Post, Comment, PostLike, User

def seed_news_hub():
    print("Seeding News Hub with Trading News & Community Posts...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check if posts already exist
        existing = Post.query.count()
        if existing > 0:
            print(f"Found {existing} existing posts. Skipping seed.")
            return
        
        # Get some users for authorship (use existing traders + admin)
        users = User.query.limit(10).all()
        if len(users) < 3:
            print("Not enough users. Please seed users first.")
            return
        
        # News/Posts Data
        news_posts = [
            {
                "author_idx": 0,
                "content": "🚀 Le Gold (XAUUSD) franchit les 2100$ ! Les traders profitent de la volatilité actuelle pour capturer des profits massifs. Qui a réussi à profiter de ce mouvement ?",
                "tags": "GOLD,MARKET_UPDATE,BULLISH",
                "image_url": None,
                "days_ago": 0
            },
            {
                "author_idx": 1,
                "content": "📊 Analyse Technique : EUR/USD forme un pattern de double bottom sur le H4. Zone d'achat idéale autour de 1.0850 avec objectif 1.0950. Qui est déjà en position ?",
                "tags": "EURUSD,ANALYSIS,FOREX",
                "image_url": None,
                "days_ago": 1
            },
            {
                "author_idx": 2,
                "content": "💡 Astuce du jour : Toujours placer votre Stop Loss AVANT d'entrer en position. La gestion du risque est la clé de la longévité en trading !",
                "tags": "EDUCATION,RISK_MANAGEMENT,TIP",
                "image_url": None,
                "days_ago": 1
            },
            {
                "author_idx": 0,
                "content": "🔥 Résultats de la semaine : +18% sur mon compte Elite grâce à la stratégie Smart Money. Le scalping sur indices fonctionne à merveille en ce moment !",
                "tags": "RESULTS,STRATEGY,MOTIVATION",
                "image_url": None,
                "days_ago": 2
            },
            {
                "author_idx": 3,
                "content": "⚠️ Attention aux news économiques de demain : NFP US à 14h30. Forte volatilité attendue sur l'USD. Protégez vos positions !",
                "tags": "NEWS,ALERT,FUNDAMENTAL",
                "image_url": None,
                "days_ago": 2
            },
            {
                "author_idx": 1,
                "content": "🎯 Challenge du mois : Qui arrive à maintenir un win rate supérieur à 65% ? Partagez vos stats et stratégies !",
                "tags": "CHALLENGE,COMMUNITY,STATS",
                "image_url": None,
                "days_ago": 3
            },
            {
                "author_idx": 2,
                "content": "📈 Bitcoin teste la résistance des 45000$. Breakout imminent ou rejection ? Les traders crypto sont en alerte maximale !",
                "tags": "CRYPTO,BITCOIN,MARKET_WATCH",
                "image_url": None,
                "days_ago": 3
            },
            {
                "author_idx": 4,
                "content": "💪 Mentalité de champion : J'ai transformé un compte de 5000$ en 12000$ en 3 mois grâce à la discipline et au respect strict de mon plan de trading. Restez focus !",
                "tags": "MOTIVATION,SUCCESS_STORY,MINDSET",
                "image_url": None,
                "days_ago": 4
            },
            {
                "author_idx": 0,
                "content": "🌟 Nouveau record personnel : 15 trades gagnants consécutifs ! La clé ? Attendre les meilleurs setups et ne JAMAIS forcer le marché.",
                "tags": "ACHIEVEMENT,STRATEGY,PATIENCE",
                "image_url": None,
                "days_ago": 5
            },
            {
                "author_idx": 3,
                "content": "📚 Leçon apprise cette semaine : Les faux breakouts coûtent cher. Toujours attendre la confirmation avant d'entrer. Qui a vécu la même expérience ?",
                "tags": "LESSON,EDUCATION,EXPERIENCE",
                "image_url": None,
                "days_ago": 6
            }
        ]
        
        created_posts = []
        
        print("\nCreating posts...")
        for i, post_data in enumerate(news_posts, 1):
            author = users[post_data["author_idx"] % len(users)]
            created_at = datetime.utcnow() - timedelta(days=post_data["days_ago"])
            
            post = Post(
                user_id=author.id,
                content=post_data["content"],
                tags=post_data["tags"],
                image_url=post_data["image_url"],
                created_at=created_at,
                updated_at=created_at
            )
            db.session.add(post)
            db.session.commit()
            
            created_posts.append(post)
            print(f"  ✓ Post #{i} by {author.username}")
        
        # Add some comments and likes
        print("\nAdding engagement (comments & likes)...")
        
        import random
        
        for post in created_posts[:5]:  # Add engagement to first 5 posts
            # Add 1-3 random likes
            num_likes = random.randint(1, 3)
            liked_users = random.sample(users, min(num_likes, len(users)))
            
            for user in liked_users:
                like = PostLike(post_id=post.id, user_id=user.id)
                db.session.add(like)
            
            # Add 0-2 comments
            num_comments = random.randint(0, 2)
            for _ in range(num_comments):
                commenter = random.choice(users)
                comment_texts = [
                    "Excellente analyse ! 👍",
                    "Merci pour le partage !",
                    "Je suis d'accord avec cette approche",
                    "Très utile, merci !",
                    "Belle performance ! 🔥"
                ]
                comment = Comment(
                    post_id=post.id,
                    user_id=commenter.id,
                    content=random.choice(comment_texts)
                )
                db.session.add(comment)
        
        db.session.commit()
        
        print("\n✅ News Hub Successfully Seeded!")
        print("=" * 60)
        print(f"Total: {len(created_posts)} Posts")
        print(f"Engagement: Comments & Likes added to top posts")

if __name__ == '__main__':
    seed_news_hub()
