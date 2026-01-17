from flask import Blueprint, request, jsonify, current_app
from models import db, TradingFloor, FloorMessage, MessageType, TradingFloorType, User, UserRole, Account, ChallengeStatus, TradeStatus, Post, Comment, PostLike
from middleware import token_required
from datetime import datetime, timedelta
import google.generativeai as genai
import os

community_bp = Blueprint('community', __name__)

def get_ai_response(prompt, context_messages=[]):
    """Helper to call Gemini API"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return "Error: AI Service not configured (Missing API Key)"
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Construct context
        context_str = "\n".join([f"{m['user_name']}: {m['content']}" for m in context_messages])
        full_prompt = f"""
        Act as a professional Prop Firm Trading Assistant.
        Context (recent floor messages):
        {context_str}
        
        User Query: {prompt}
        
        Provide a concise, professional, and actionable response. Focus on market sentiment, risk, and key levels if mentioned.
        """
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble connecting to the market feeds right now. Please try again later."


def seed_floors():
    """Seed default trading floors if none exist"""
    defaults = [
        {'name': 'Global Trading Floor', 'type': TradingFloorType.GLOBAL, 'icon': 'fa-globe', 'desc': 'The heart of our prop firm. General market discussion.', 'level': 'Bronze Trader'},
        {'name': 'Scalping Pit (1m/5m)', 'type': TradingFloorType.SCALPING, 'icon': 'fa-bolt', 'desc': 'High frequency setups. Fast execution only.', 'level': 'Silver Trader'},
        {'name': 'Swing Trading Room', 'type': TradingFloorType.SWING, 'icon': 'fa-chart-line', 'desc': 'HTF Analysis, macroscopic trends.', 'level': 'Bronze Trader'},
        {'name': 'Crypto Derivatives', 'type': TradingFloorType.CRYPTO, 'icon': 'fa-bitcoin', 'desc': 'Perpetual futures, BTC & ETH analysis.', 'level': 'Bronze Trader'},
        {'name': 'Forex Majors', 'type': TradingFloorType.FOREX, 'icon': 'fa-dollar-sign', 'desc': 'EURUSD, GBPUSD, USDJPY technicals.', 'level': 'Silver Trader'},
    ]
    
    for d in defaults:
        # Check if exists
        exists = TradingFloor.query.filter_by(name=d['name']).first()
        if not exists:
            f = TradingFloor(
                name=d['name'],
                floor_type=d['type'],
                icon_name=d['icon'],
                description=d['desc'],
                required_level=d['level']
            )
            db.session.add(f)
    db.session.commit()

@community_bp.route('/posts', methods=['GET'])
def get_community_posts():
    # Public endpoint? Or authenticated? User said "visibles par tous".
    # But usually frontend sends token. Let's make it flexible or token required if needed for 'isLiked'.
    # For now, public read is fine, but to know "isLiked" we need user.
    # We'll assume simplest first: just list. Frontend can handle "isLiked" via separate call or we check token if present.
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in posts])

@community_bp.route('/posts', methods=['POST'])
@token_required
def create_community_post(current_user):
    # Using multipart/form-data now
    content = request.form.get('content')
    tags = request.form.get('tags') # String format "BTC,GOLD"
    image = request.files.get('image')
    
    if not content or len(content) < 3:
        return jsonify({'message': 'Content too short'}), 400
        
    image_url = None
    if image and image.filename:
        # Save image
        import uuid, os
        from werkzeug.utils import secure_filename
        
        ext = image.filename.rsplit('.', 1)[1].lower()
        if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            filename = f"{uuid.uuid4().hex}.{ext}"
            upload_folder = os.path.join(current_app.root_path, 'uploads', 'posts')
            os.makedirs(upload_folder, exist_ok=True)
            image.save(os.path.join(upload_folder, filename))
            # image_url = f"/api/community/uploads/posts/{filename}" # If routed via API
            # Or simplified:
            image_url = f"/uploads/posts/{filename}"

    new_post = Post(
        user_id=current_user.id,
        content=content,
        tags=tags,
        image_url=image_url
    )
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify(new_post.to_dict()), 201

# Serve uploads
from flask import send_from_directory
@community_bp.route('/uploads/posts/<filename>')
def serve_post_image(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'uploads', 'posts'), filename)

@community_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify([c.to_dict() for c in comments])

@community_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def create_post_comment(current_user, post_id):
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'message': 'Content required'}), 400
        
    # Check post exists
    post = Post.query.get_or_404(post_id)
    
    new_comment = Comment(
        post_id=post.id,
        user_id=current_user.id,
        content=content
    )
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify(new_comment.to_dict()), 201

@community_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    existing = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing:
        db.session.delete(existing) # Unlike
        db.session.commit()
        return jsonify({'liked': False, 'count': len(post.likes)})
    else:
        new_like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'liked': True, 'count': len(post.likes)})

# Keep AI endpoint for other features if needed
@community_bp.route('/ai/ask', methods=['POST'])
@token_required
def ask_ai(current_user):
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'message': 'Prompt required'}), 400
        
    response_text = get_ai_response(prompt)
    
    return jsonify({'response': response_text})

@community_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    # Frontend sends 'THIS_MONTH' or 'ALL_TIME'
    period = request.args.get('period', 'ALL_TIME')
    
    # 1. Try fetching from Persistent Leaderboard Table first
    try:
        from models import Leaderboard
        entries = Leaderboard.query.filter_by(is_visible=True, period=period)\
                                   .order_by(Leaderboard.ranking.asc())\
                                   .limit(10).all()  # ELITE HALL OF FAME: TOP 10 ONLY
        
        if entries and len(entries) > 0:
            # Use saved data
            return jsonify([entry.to_dict() for entry in entries])
            
    except Exception as e:
        print(f"Leaderboard Table Error: {e}")
        # Fallthrough to dynamic
    
    # --- DYNAMIC CALCULATION (Fallback) ---
    accounts = Account.query.filter(Account.status.in_([ChallengeStatus.ACTIVE, ChallengeStatus.PASSED, ChallengeStatus.FUNDED])).all()
    
    leaderboard_data = []
    import random
    
    now = datetime.utcnow()
    
    for acc in accounts:
        # Determine Profit
        profit = 0
        roi = 0
        win_rate = 0
        
        relevant_trades = []
        
        if period == 'ALL_TIME':
            profit = acc.equity - acc.initial_balance
            relevant_trades = acc.trades
        elif period == 'THIS_MONTH':
            start_date = now - timedelta(days=30)
            monthly_trades = [t for t in acc.trades if t.status.value == 'CLOSED' and t.closed_at and t.closed_at >= start_date]
            profit = sum(t.pnl for t in monthly_trades)
            relevant_trades = monthly_trades
            if not monthly_trades and profit == 0:
                continue

        if acc.initial_balance > 0:
            roi = (profit / acc.initial_balance) * 100
            
        closed_trades = [t for t in relevant_trades if t.status.value == 'CLOSED']
        if closed_trades:
            wins = sum(1 for t in closed_trades if t.pnl > 0)
            win_rate = (wins / len(closed_trades)) * 100
            
        country = 'MA' 
        # Deterministic country fallback
        countries = ['MA', 'US', 'FR', 'UK', 'AE', 'SG', 'DE']
        country = countries[acc.user.id % len(countries)]

        if profit > 0: # Only positive traders typically
            leaderboard_data.append({
                'rank': 0,
                'username': acc.user.username,
                'country': country,
                'profit': round(profit, 2),
                'roi': round(roi, 1),
                'winRate': round(win_rate, 1),
                'status': acc.status.value,
                'fundedCapital': acc.initial_balance,
                'avatar': f"https://ui-avatars.com/api/?name={acc.user.full_name}&background=random"
            })
        
    leaderboard_data.sort(key=lambda x: x['profit'], reverse=True)
    top_10 = leaderboard_data[:10]
    for i, entry in enumerate(top_10):
        entry['rank'] = i + 1
        
    return jsonify(top_10)
