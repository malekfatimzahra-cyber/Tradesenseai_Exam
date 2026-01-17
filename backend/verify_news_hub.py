
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, Post, Comment, PostLike

def verify_news_hub():
    print("Verifying News Hub Data in MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        
        print(f"\n📰 Total Posts in Database: {len(posts)}\n")
        print("=" * 80)
        
        for i, post in enumerate(posts[:10], 1):  # Show first 10
            print(f"\n📝 Post #{i}: {post.content[:60]}...")
            print(f"   Author: {post.author.full_name} (@{post.author.username})")
            print(f"   Tags: {post.tags or 'None'}")
            print(f"   Likes: {len(post.likes)} | Comments: {len(post.comments)}")
            print(f"   Created: {post.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            if post.image_url:
                print(f"   Image: {post.image_url}")
        
        print("\n" + "=" * 80)
        
        total_comments = Comment.query.count()
        total_likes = PostLike.query.count()
        
        print(f"\n📊 Statistics:")
        print(f"   Posts: {len(posts)}")
        print(f"   Comments: {total_comments}")
        print(f"   Likes: {total_likes}")
        
        if len(posts) == 0:
            print("\n⚠️  No posts found. Database needs seeding.")
        else:
            print("\n✓ News Hub data verified in MySQL")

if __name__ == '__main__':
    verify_news_hub()
