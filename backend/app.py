from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, UserRole, ChallengeStatus, Account, Trade, TradeType, TradeStatus, Course, Module, Lesson, Quiz, Question, Option, CourseCategory, CourseLevel, Badge, UserBadge, UserXP, UserLessonProgress, UserCourseProgress, Leaderboard, PerformanceSnapshot, AdminActionLog
from engine import evaluate_challenge_rules
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

# Load env vars from root .env.local or .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
load_dotenv() # Fallback to .env

app = Flask(__name__)
# Enable CORS for all domains (Production ready for Vercel/Anywhere)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Hello from Backend!", 200

@app.get("/health")
def health():
    return {"status": "ok"}

# --- MODIFICATION DE LA BASE DE DONNÉES ---
db_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:2002@localhost/tradesense')
# SQLAlchemy requires mysql+pymysql:// instead of just mysql://
if db_url and db_url.startswith('mysql://'):
    db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    if os.getenv("RUN_DB_INIT") == "true":
        try:
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            masked_uri = db_uri.split('@')[-1] if '@' in db_uri else 'local'
            print(f"✅ Database tables initialized. Connected to: ...@{masked_uri}")
            
            # 1. Seed Users if empty
            if User.query.count() == 0:
                print("🌱 Seeding initial users...")
                admin = User(full_name="Admin TradeSense", email="malekfatimzahra@gmail.com", username="admin", role=UserRole.ADMIN)
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("✅ Initial users complete.")
                
            # 2. Seed Plans if empty
            from models import ChallengePlan
            if ChallengePlan.query.count() == 0:
                print("🌱 Seeding plans...")
                plans = [
                    { 'id': 'starter', 'name': 'Starter Challenge', 'capital': 5000, 'profit_target': 500, 'max_drawdown': 500, 'daily_loss_limit': 250, 'price': 200, 'currency': 'MAD' },
                    { 'id': 'pro', 'name': 'Professional Pro', 'capital': 25000, 'profit_target': 2500, 'max_drawdown': 2500, 'daily_loss_limit': 1250, 'price': 500, 'currency': 'MAD' },
                    { 'id': 'elite', 'name': 'Elite Institutional', 'capital': 100000, 'profit_target': 10000, 'max_drawdown': 10000, 'daily_loss_limit': 5000, 'price': 1000, 'currency': 'MAD' },
                ]
                for p in plans:
                    db.session.add(ChallengePlan(**p, is_active=True))
                db.session.commit()
                print("✅ Plans seeded.")
                
            # 3. Seed Courses if empty
            from models import Course, CourseCategory, CourseLevel
            if Course.query.count() == 0:
                print("🌱 Seeding academy...")
                courses = [
                    {
                        "title": "Introduction au Trading",
                        "category": CourseCategory.TECHNICAL,
                        "level": CourseLevel.BEGINNER,
                        "description": "Apprenez les bases du trading Forex et CFD. Maîtrisez les concepts de base du marché.",
                        "thumbnail_url": "https://img.freepik.com/free-vector/gradient-stock-market-concept_23-2149166910.jpg"
                    },
                    {
                        "title": "Analyse Technique Avancée",
                        "category": CourseCategory.TECHNICAL,
                        "level": CourseLevel.INTERMEDIATE,
                        "description": "Maîtrisez les indicateurs techniques et patterns graphiques pour prédire les mouvements.",
                        "thumbnail_url": "https://img.freepik.com/free-vector/trading-concept-with-tablet_23-2148564070.jpg"
                    }
                ]
                for c_data in courses:
                    course = Course(**c_data, lang="fr", duration_minutes=120, xp_reward=1000)
                    db.session.add(course)
                db.session.commit()
                print("✅ Academy seeded.")
                
            # 4. Seed Leaderboard (Accounts) if only 1 user or few accounts
            from models import Account, ChallengeStatus
            import random
            if Account.query.count() <= 1:
                print("🌱 Seeding leaderboard...")
                names = [("Othman Chakir", "ochakir"), ("Imane Benjelloun", "ibenjelloun"), ("Mehdi Lazrak", "mlazrak"), ("Khadija Tazi", "ktazi")]
                for full_name, username in names:
                    temp_user = User(full_name=full_name, email=f"{username}@demo.com", username=username, role=UserRole.USER)
                    temp_user.set_password("demo123")
                    db.session.add(temp_user)
                    db.session.flush()
                    st_balance = random.choice([5000, 25000, 100000])
                    equity = st_balance * (1 + random.uniform(-0.05, 0.15))
                    acc = Account(user_id=temp_user.id, plan_name=random.choice(['Starter', 'Pro', 'Elite']), initial_balance=st_balance, current_balance=equity, equity=equity, daily_starting_equity=st_balance, status=ChallengeStatus.ACTIVE)
                    db.session.add(acc)
                db.session.commit()
                print("✅ Leaderboard seeded.")

            print("✅ Full Seeding logic complete.")

        except Exception as e:
            print(f"❌ Error initializing tables: {e}")
    else:
        print("ℹ️ Automated DB migration/seeding skipped (RUN_DB_INIT not set).")

from payments import payments_bp
from challenges import challenges_bp
from market_data import market_bp
from academy import academy_bp
from community import community_bp
from ai_agency import ai_agency_bp
from trading import trading_bp
from admin_routes import admin_bp
from ai_analysis import ai_analysis_bp
from gemini_chat import gemini_chat_bp
from auth_routes import auth_bp
from mock_payment import mock_payment_bp
from paypal_config import paypal_config_bp
from payment import payment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(challenges_bp, url_prefix='/api/challenges')
app.register_blueprint(market_bp, url_prefix='/api/market')
app.register_blueprint(trading_bp, url_prefix='/api/trading')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(academy_bp, url_prefix='/api/academy')
app.register_blueprint(community_bp, url_prefix='/api/community')
app.register_blueprint(ai_agency_bp, url_prefix='/api/ai-agency')
app.register_blueprint(ai_analysis_bp, url_prefix='/api')
app.register_blueprint(gemini_chat_bp, url_prefix='/api')
app.register_blueprint(mock_payment_bp, url_prefix='/api')
app.register_blueprint(paypal_config_bp, url_prefix='/api/paypal')
from unified_payment import unified_payment_bp
app.register_blueprint(payment_bp, url_prefix='/api/payment')
app.register_blueprint(unified_payment_bp, url_prefix='/api/unified-payment')

from user_routes import user_bp
app.register_blueprint(user_bp, url_prefix='/api/users')

# --- Middleware ---
from middleware import token_required

# --- Auth Routes (Moved to auth_routes.py blueprint) ---
# Duplicate routes commented out - using auth_bp instead
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.json
#     if not data or not data.get('email') or not data.get('password'): 
#         return jsonify({'message': 'Missing data'}), 400
#     if User.query.filter_by(email=data.get('email')).first():
#         return jsonify({'message': 'Email exists'}), 409
#     
#     # Generate username from email if not provided
#     username = data.get('username') or data.get('email').split('@')[0]
#     
#     new_user = User(
#         full_name=data.get('full_name', 'User'), 
#         email=data.get('email'), 
#         username=username,
#         role=UserRole.USER
#     )
#     new_user.set_password(data.get('password'))
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'Registered', 'token': 'mock-token', 'user': new_user.to_dict()}), 201

# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.json
#     user = User.query.filter_by(email=data.get('email')).first()
#     if not user or not user.check_password(data.get('password')):
#         return jsonify({'message': 'Invalid credentials'}), 401
#     token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
#     return jsonify({'token': token, 'user': user.to_dict()})

# --- Health Check ---
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

# --- Module A: Challenge & Trade Routes ---

@app.route('/api/accounts', methods=['POST'])
@token_required
def create_account(current_user):
    """Start a new Challenge (Create Account)"""
    # In real app: verify payment here or pass payment_id
    new_account = Account(
        user_id=current_user.id,
        initial_balance=5000.0, # Default or from Plan
        current_balance=5000.0,
        equity=5000.0,
        daily_starting_equity=5000.0,
        status=ChallengeStatus.ACTIVE
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.to_dict()), 201

@app.route('/api/trades', methods=['POST'])
@token_required
def place_trade(current_user):
    """Execute Trade and Trigger Engine"""
    data = request.json
    account_id = data.get('account_id')
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'message': 'Account not found or access denied'}), 404
        
    if account.status != ChallengeStatus.ACTIVE:
        return jsonify({'message': 'Account is not ACTIVE'}), 400

    # Create Trade with Risk Controls
    trade = Trade(
        account_id=account.id,
        symbol=data.get('symbol'),
        trade_type=TradeType[data.get('type')], # BUY/SELL
        amount=float(data.get('amount')),
        entry_price=float(data.get('price')),
        stop_loss=data.get('sl'),
        take_profit=data.get('tp'),
        commission=3.50, # Standard institutional fee
        status=TradeStatus.OPEN,
        user_id=current_user.id, # Ensure user_id is set
        quantity=float(data.get('amount'))/float(data.get('price')), # Approx quantity
        price=float(data.get('price')),
        side=TradeType[data.get('type')]
    )
    
    # Deduct commission immediately from equity
    account.equity -= 3.50
    
    db.session.add(trade)
    db.session.commit()
    
    # Trigger Engine - THE CRITICAL MOMENT
    status = evaluate_challenge_rules(account.id)
    
    # Reload account to get updated reason field
    db.session.refresh(account)
    
    return jsonify({
        'message': 'Trade executed', 
        'trade': trade.to_dict(), 
        'account': {
            'status': status.value,
            'equity': account.equity,
            'daily_pnl': account.equity - account.daily_starting_equity,
            'total_pnl': account.equity - account.initial_balance,
            'reason': account.reason
        }
    }), 201

@app.route('/api/trades/close', methods=['POST'])
@token_required
def close_trade(current_user):
    data = request.json
    trade_id = data.get('trade_id')
    exit_price = float(data.get('exit_price'))
    
    trade = Trade.query.get(trade_id)
    if not trade or trade.account.user_id != current_user.id:
        return jsonify({'message': 'Trade not found'}), 404
        
    if trade.status == TradeStatus.CLOSED:
        return jsonify({'message': 'Trade already closed'}), 400

    # Calculate PnA
    pnl = (exit_price - trade.entry_price) * (trade.amount / trade.entry_price) if trade.trade_type == TradeType.BUY else (trade.entry_price - exit_price) * (trade.amount / trade.entry_price)
    
    trade.exit_price = exit_price
    trade.status = TradeStatus.CLOSED
    trade.pnl = pnl
    trade.closed_at = datetime.datetime.utcnow()
    
    # Update Account Balance & Equity
    account = trade.account
    account.current_balance += pnl
    account.equity += pnl # Realized PnL updates equity
    
    db.session.commit()
    
    # Trigger Engine (The moment of truth)
    new_status = evaluate_challenge_rules(account.id)
    
    # Reload to get updated reason
    db.session.refresh(account)
    
    return jsonify({
        'message': 'Trade closed',
        'pnl': pnl,
        'new_balance': account.current_balance,
        'account': {
            'status': new_status.value,
            'equity': account.equity,
            'daily_pnl': account.equity - account.daily_starting_equity,
            'total_pnl': account.equity - account.initial_balance,
            'reason': account.reason
        }
    })

# --- Module D: Leaderboard ---
from sqlalchemy import func

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Public Leaderboard: Top 10 Traders sorted by Profit.
    Primary: Uses cached 'leaderboard' table (synced from real trades)
    Fallback: Aggregates performance from the 'trades' table directly
    """
    try:
        from models import Leaderboard
        
        period = request.args.get('period', 'ALL_TIME')
        
        # PRIMARY: Use cached leaderboard table (populated by sync script)
        cached_entries = Leaderboard.query.filter_by(
            period=period, 
            is_visible=True
        ).order_by(Leaderboard.ranking.asc()).limit(10).all()
        
        if cached_entries:
            return jsonify([entry.to_dict() for entry in cached_entries])
        
        # FALLBACK: Calculate live from trades (if leaderboard table is empty)
        results = db.session.query(
            User.id,
            User.full_name,
            User.username,
            Account.id.label('account_id'),
            Account.initial_balance,
            Account.equity,
            func.sum(Trade.pnl).label('total_profit'),
            func.count(Trade.id).label('trades_count'),
            func.sum(db.case((Trade.pnl > 0, 1), else_=0)).label('wins')
        ).join(Account, Account.user_id == User.id)\
         .outerjoin(Trade, db.and_(Trade.account_id == Account.id, Trade.status == TradeStatus.CLOSED))\
         .filter(Account.status.in_([ChallengeStatus.ACTIVE, ChallengeStatus.PASSED, ChallengeStatus.FUNDED]))\
         .group_by(User.id, Account.id)\
         .order_by(db.desc('total_profit'))\
         .limit(10).all()

        leaderboard = []
        for rank, row in enumerate(results, 1):
            profit = row.total_profit if row.total_profit is not None else (row.equity - row.initial_balance)
            roi = (profit / row.initial_balance * 100) if row.initial_balance and row.initial_balance > 0 else 0
            win_rate = (row.wins / row.trades_count * 100) if row.trades_count and row.trades_count > 0 else 0
            
            leaderboard.append({
                'id': row.id,
                'rank': rank,
                'user_id': row.id,
                'account_id': row.account_id,
                'username': row.username or row.full_name,
                'profit': round(profit if profit else 0, 2),
                'roi': round(roi, 2),
                'winRate': round(win_rate, 2),
                'fundedCapital': row.initial_balance,
                'avatar': f"https://ui-avatars.com/api/?name={row.full_name}&background=random",
                'country': 'MA',
                'badges': [],
                'sparkline': []
            })
            
        return jsonify(leaderboard)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Error fetching leaderboard', 'error': str(e)}), 500
        traceback.print_exc()
        return jsonify({'message': 'Error fetching leaderboard', 'error': str(e)}), 500

# --- Module X: Settings & i18n ---
from sqlalchemy import text

@app.route('/api/settings/language', methods=['POST'])
@token_required
def update_language(current_user):
    """Update user language preference"""
    data = request.json
    lang = data.get('lang', 'fr')
    if lang not in ['fr', 'en', 'ar']:
        return jsonify({'message': 'Invalid language'}), 400
    
    try:
        # Update or insert setting using raw SQL for speed (since model not in ORM yet)
        sql = text("""
            INSERT INTO user_settings (user_id, lang) 
            VALUES (:uid, :lang) 
            ON DUPLICATE KEY UPDATE lang = :lang
        """)
        db.session.execute(sql, {'uid': current_user.id, 'lang': lang})
        db.session.commit()
        return jsonify({'success': True, 'lang': lang})
    except Exception as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

@app.route('/api/settings/language', methods=['GET'])
@token_required
def get_language(current_user):
    """Get user language preference"""
    try:
        sql = text("SELECT lang FROM user_settings WHERE user_id = :uid")
        result = db.session.execute(sql, {'uid': current_user.id}).fetchone()
        lang = result[0] if result else 'fr'
        return jsonify({'lang': lang})
    except Exception as e:
        return jsonify({'lang': 'fr', 'error': str(e)}), 200

@app.route('/api/debug/new-day', methods=['POST'])
@token_required
def reset_new_day(current_user):
    """
    DEMO ENDPOINT: Simulates a new trading day by resetting daily_starting_equity.
    In production, this would run automatically at 00:00 UTC via a scheduler.
    """
    data = request.json
    account_id = data.get('account_id')
    
    if not account_id:
        return jsonify({'message': 'account_id is required'}), 400
    
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'message': 'Account not found or access denied'}), 404
    
    # Reset daily starting equity to current equity
    old_daily_start = account.daily_starting_equity
    account.daily_starting_equity = account.equity
    db.session.commit()
    
    return jsonify({
        'message': 'New trading day started',
        'account_id': account.id,
        'old_daily_starting_equity': old_daily_start,
        'new_daily_starting_equity': account.daily_starting_equity,
        'current_equity': account.equity
    })

# --- Module E: Real-Time News ---
import requests
import random

@app.route('/api/news/live', methods=['GET'])
def get_live_news():
    """
    Fetches real-time financial news from NewsData.io (or similar free API).
    """
    # CRUCIAL: You must sign up at https://newsdata.io/ to get your own FREE API KEY.
    # Replace 'YOUR_NEWSDATA_API_KEY' below with your actual key.
    API_KEY = "pub_dac50fccb9114e728bf7aaadb2cc373f" 
    
    # URL for NewsData.io API - searching for business/crypto/finance news in English or French
    # using 'q' parameter for financial keywords if needed, or category 'business'
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&category=business&language=en,fr"

    try:
        # 1. Fetch data from external API
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            # Fallback if API fails (or key is invalid)
            return jsonify({'error': 'Failed to fetch news from external provider', 'details': data}), 500

        articles = data.get('results', [])
        formatted_news = []

        # 2. Transform into frontend format
        for idx, article in enumerate(articles[:10]): # Limit to 10 items
            # Format time: Extract HH:MM from pubDate (usually "YYYY-MM-DD HH:MM:SS")
            pub_date = article.get('pubDate', '')
            time_str = "N/A"
            if len(pub_date) >= 16:
                 # Extracting "HH:MM" assuming format "YYYY-MM-DD HH:MM..."
                 time_str = pub_date[11:16]
            
            # Helper for sentiment (Randomized as requested since free APIs usually lack this)
            sentiment_options = ['bullish', 'bearish', 'neutral']
            # Simple heuristic: if 'crypto' or 'bitcoin' in title, maybe more volatile? 
            # But prompt asked for random helper.
            sentiment = random.choice(sentiment_options)

            formatted_news.append({
                'id': str(idx), # or article.get('article_id')
                'source': article.get('source_id', 'Unknown'), # or article.get('source_id')
                'time': time_str,
                'title': article.get('title', 'No Title'),
                'sentiment': sentiment
            })

        return jsonify(formatted_news)

    except Exception as e:
        print(f"Error fetching news: {e}")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

@app.route('/api/debug/seed-leaderboard', methods=['POST'])
def debug_seed_leaderboard():
    """Seeds fake leaderboard data for demo/production"""
    try:
        import json
        
        # Elite Traders Data
        elite_traders = [
            {"username": "AtlasTrader_MA", "fullname": "Karim Benali", "country": "MA", "plan": "Elite $100k", "initial": 100000, "equity": 124500, "status": ChallengeStatus.FUNDED, "badges": ["Elite", "Sniper", "Risk Manager"], "win_rate": 78.5, "roi": 24.5, "consistency": 92, "risk_score": 9.5},
            {"username": "SarahFX", "fullname": "Sarah Connor", "country": "US", "plan": "Pro $200k", "initial": 200000, "equity": 238000, "status": ChallengeStatus.FUNDED, "badges": ["Consistent", "Shark"], "win_rate": 65.2, "roi": 19.0, "consistency": 88, "risk_score": 8.0},
            {"username": "TokyoDrift", "fullname": "Kenji Sato", "country": "JP", "plan": "Starter $50k", "initial": 50000, "equity": 58200, "status": ChallengeStatus.FUNDED, "badges": ["Algo", "disciplined"], "win_rate": 81.0, "roi": 16.4, "consistency": 95, "risk_score": 9.8},
            {"username": "EuroKing", "fullname": "Hans Zimmer", "country": "DE", "plan": "Elite $100k", "initial": 100000, "equity": 112000, "status": ChallengeStatus.PASSED, "badges": ["Funded"], "win_rate": 55.5, "roi": 12.0, "consistency": 70, "risk_score": 6.5},
            {"username": "DubaiWhale", "fullname": "Ahmed Al-Maktoum", "country": "AE", "plan": "VIP $500k", "initial": 500000, "equity": 545000, "status": ChallengeStatus.ACTIVE, "badges": ["VIP", "Whale"], "win_rate": 60.0, "roi": 9.0, "consistency": 85, "risk_score": 7.5}
        ]

        # Loop to create users and leaderboard entries
        for i, trader_data in enumerate(elite_traders):
            user = User.query.filter_by(username=trader_data['username']).first()
            if not user:
                user = User(username=trader_data['username'], full_name=trader_data['fullname'], email=f"{trader_data['username'].lower()}@tradesense.ai", role=UserRole.USER)
                user.set_password("password123")
                db.session.add(user)
                db.session.commit()
            
            # Create Account if not exists
            account = Account(user_id=user.id, plan_name=trader_data['plan'], initial_balance=trader_data['initial'], current_balance=trader_data['equity'], equity=trader_data['equity'], status=trader_data['status'], created_at=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(30, 90)))
            db.session.add(account)
            db.session.commit()

            # Create Leaderboard Entry (ALL_TIME)
            snapshots_json = [] # Simplified for inline
            steps = 20
            current_eq = trader_data['initial']
            step_val = (trader_data['equity'] - current_eq) / steps
            for d in range(steps):
                current_eq += step_val + (random.uniform(-step_val * 0.5, step_val * 1.5) * 0.2)
                snapshots_json.append(current_eq)
            snapshots_json.append(trader_data['equity'])

            lb_entry = Leaderboard(
                user_id=user.id, account_id=account.id, username=user.username, country=trader_data['country'],
                profit=trader_data['equity'] - trader_data['initial'], roi=trader_data['roi'], win_rate=trader_data['win_rate'],
                funded_amount=trader_data['initial'], consistency_score=trader_data['consistency'], risk_score=trader_data['risk_score'],
                ranking=i + 1, period='ALL_TIME', badges=json.dumps(trader_data['badges']), equity_curve=json.dumps(snapshots_json)
            )
            db.session.add(lb_entry)
            db.session.commit()

        return jsonify({'message': 'Leaderboard Seeded Successfully'}), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        error_details = traceback.format_exc()
        print("LEADERBOARD SEED ERROR:", error_details)
        return jsonify({'error': str(e), 'traceback': error_details}), 500

@app.route('/api/debug/seed-academy', methods=['POST'])
def debug_seed_academy():
    """
    Public Endpoint to trigger seeding of Academy content on Production.
    (Protected by simple check or kept open for exam demo speed)
    """
    try:
        import traceback
        seed_academy()
        return jsonify({'message': 'Academy Seeded Successfully'}), 200
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("SEEDING ERROR:", error_details)
        return jsonify({'error': str(e), 'traceback': error_details}), 500

def seed_academy():
    print("Seeding FULL Academy Content...")
    
    # Badges
    badges_data = [
        {"name": "Technical Titan", "desc": "Mastered technical analysis", "icon": "fa-chart-line", "cat": "TECHNICAL"},
        {"name": "Risk Guardian", "desc": "Completed risk management", "icon": "fa-shield-halved", "cat": "RISK"},
        {"name": "Psychology Master", "desc": "Mental discipline achieved", "icon": "fa-brain", "cat": "PSYCHOLOGY"}
    ]
    for bd in badges_data:
        if not Badge.query.filter_by(name=bd["name"]).first():
            db.session.add(Badge(name=bd["name"], description=bd["desc"], icon_name=bd["icon"], category=bd["cat"], xp_bonus=500))
    db.session.commit()
    
    # =========== COURSE 1: INSTITUTIONAL TRADING ===========
    if not Course.query.filter_by(title="Institutional Trading Mastery").first():
        c1 = Course(title="Institutional Trading Mastery", description="Master Order Blocks, Liquidity, Market Structure like the pros.", category=CourseCategory.TECHNICAL, level=CourseLevel.INTERMEDIATE, thumbnail_url="https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800", duration_minutes=180, xp_reward=1500, is_premium=False)
        db.session.add(c1)
        db.session.commit()
        
        # Module 1: Market Structure
        m1 = Module(course_id=c1.id, title="Market Structure Fundamentals", order=1)
        db.session.add(m1)
        db.session.commit()
        
        lessons_m1 = [
            {"title": "Introduction to Market Structure", "content": "## What is Market Structure?\nMarket structure is the backbone of price action. It defines trend direction using swing highs and lows.\n\n### Why It Matters\nInstitutions trade based on structure breaks. Retail traders who ignore this lose.\n\n### Core Concepts\n- **Uptrend**: Higher Highs (HH) + Higher Lows (HL)\n- **Downtrend**: Lower Lows (LL) + Lower Highs (LH)\n- **Range**: Equal highs and lows\n\n**Key Insight**: Structure determines bias. Always trade WITH the structure, never against it.", "order": 1},
            {"title": "Break of Structure (BOS)", "content": "## BOS Explained\nA Break of Structure confirms trend continuation.\n\n### In an Uptrend\nPrice breaks the previous swing high → Bullish BOS.\n\n### In a Downtrend\nPrice breaks the previous swing low → Bearish BOS.\n\n### Trading the BOS\n1. Wait for the break\n2. Look for pullback to order block\n3. Enter on confirmation\n\n**Example**: BTC breaks $45k high. Pullback to $44k order block = long entry.", "order": 2},
            {"title": "Change of Character (ChoCH)", "content": "## ChoCH: The Reversal Signal\nChange of Character signals a potential trend reversal.\n\n### How to Spot It\n- In uptrend: Price breaks the last HL (higher low)\n- In downtrend: Price breaks the last LH (lower high)\n\n### What to Do\nChoCH is NOT an entry—it's a WARNING. Wait for confirmation:\n- New structure formation\n- Order block in new direction\n- Volume spike\n\n**Pro Tip**: Most retail traders enter too early on ChoCH and get stopped out. Be patient.", "order": 3}
        ]
        
        for les_data in lessons_m1:
            les = Lesson(module_id=m1.id, title=les_data["title"], content=les_data["content"], order=les_data["order"])
            db.session.add(les)
            db.session.commit()
            
            quiz = Quiz(lesson_id=les.id, title=f"{les_data['title']} Quiz", min_pass_score=70)
            db.session.add(quiz)
            db.session.commit()
            
            if "Introduction" in les_data["title"]:
                q1 = Question(quiz_id=quiz.id, text="What defines an uptrend?", explanation="Higher Highs and Higher Lows.")
                db.session.add(q1)
                db.session.commit()
                db.session.add(Option(question_id=q1.id, text="HH + HL", is_correct=True))
                db.session.add(Option(question_id=q1.id, text="LL + LH", is_correct=False))
                db.session.add(Option(question_id=q1.id, text="Equal highs/lows", is_correct=False))
            elif "BOS" in les_data["title"]:
                q2 = Question(quiz_id=quiz.id, text="What does BOS confirm?", explanation="Trend continuation.")
                db.session.add(q2)
                db.session.commit()
                db.session.add(Option(question_id=q2.id, text="Trend continuation", is_correct=True))
                db.session.add(Option(question_id=q2.id, text="Trend reversal", is_correct=False))
            else:
                q3 = Question(quiz_id=quiz.id, text="ChoCH signals what?", explanation="Potential reversal warning.")
                db.session.add(q3)
                db.session.commit()
                db.session.add(Option(question_id=q3.id, text="Reversal warning", is_correct=True))
                db.session.add(Option(question_id=q3.id, text="Buy signal", is_correct=False))
            db.session.commit()
        
        # Module 2: Order Blocks
        m2 = Module(course_id=c1.id, title="Order Blocks & Fair Value Gaps", order=2)
        db.session.add(m2)
        db.session.commit()
        
        lessons_m2 = [
            {"title": "What Are Order Blocks?", "content": "## Order Blocks Defined\nAn Order Block (OB) is the last opposing candle before a strong move.\n\n### Why They Work\nInstitutions place massive orders in these zones. When price returns, they defend it.\n\n### Bullish OB\nLast **down** candle before a bullish rally.\n\n### Bearish OB\nLast **up** candle before a bearish drop.\n\n**Visual**: Think of OB as institutional support/resistance on steroids.", "order": 1},
            {"title": "Identifying Valid Order Blocks", "content": "## Valid vs Invalid OBs\nNot all order blocks are equal. Here's how to filter:\n\n### Valid OB Criteria\n1. **Engulfment**: OB candle must be engulfed by the breakout candle\n2. **Unmitigated**: Price hasn't returned to it yet\n3. **Close to current price**: Ideally within 5-10% range\n4. **Volume spike**: Confirmation of institutional activity\n\n### Invalid OBs\n- Already tested (mitigated)\n- Tiny candle with no volume\n- Too far from current price\n\n**Pro Tip**: Draw a box from OB open to close. Entry is when price re-enters that box.", "order": 2},
            {"title": "Fair Value Gaps (FVG)", "content": "## FVG: The Imbalance\nA Fair Value Gap is an imbalance between buyers and sellers, leaving a 'gap' on the chart.\n\n### How to Spot FVG\nThree consecutive candles where:\n- Candle 1 high < Candle 3 low (Bullish FVG)\n- Candle 1 low > Candle 3 high (Bearish FVG)\n\n### Trading FVGs\nPrice tends to 'fill' FVGs before continuing the trend.\n\n**Setup**:\n1. Identify FVG\n2. Wait for price to return to the gap\n3. Enter when price reacts (rejection candle)\n\n**Example**: EUR/USD rallies leaving FVG at 1.0850-1.0870. Price pulls back, fills at 1.0860, then resumes rally.", "order": 3}
        ]
        
        for les_data in lessons_m2:
            les = Lesson(module_id=m2.id, title=les_data["title"], content=les_data["content"], order=les_data["order"])
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"{les_data['title']} Quiz", min_pass_score=75)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text=f"What is the main concept of {les_data['title']}?", explanation="Review the lesson for details.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="Covered in lesson", is_correct=True))
            db.session.add(Option(question_id=q.id, text="Not mentioned", is_correct=False))
            db.session.commit()
    
    # =========== COURSE 2: PSYCHOLOGY ===========
    if not Course.query.filter_by(title="Iron Mindset: Trading Psychology").first():
        c2 = Course(title="Iron Mindset: Trading Psychology", description="Conquer fear, greed, and emotional trading.", category=CourseCategory.PSYCHOLOGY, level=CourseLevel.ADVANCED, thumbnail_url="https://images.unsplash.com/photo-1549633033-9a446772f533?w=800", duration_minutes=120, xp_reward=1000, is_premium=True)
        db.session.add(c2)
        db.session.commit()
        
        m1 = Module(course_id=c2.id, title="Emotional Mastery", order=1)
        db.session.add(m1)
        db.session.commit()
        
        psych_lessons = [
            {"title": "The Emotional Cycle", "content": "## Trading is 80% Psychology\n\n### The Cycle\n1. **Optimism**: New trade, full of hope\n2. **Excitement**: Position moves in your favor\n3. **Thrill**: Profit peaks, you feel invincible\n4. **Euphoria**: Top of the market, maximum risk\n5. **Anxiety**: Price reverses\n6. **Denial**: 'It will come back'\n7. **Fear**: Losses mount\n8. **Desperation**: Holding losing positions\n9. **Panic**: Capitulation, exit at worst price\n10. **Despondency**: Swear off trading\n\n**Solution**: Recognize this cycle. Exit at Thrill, never hold to Panic."},
            {"title": "Handling FOMO", "content": "## FOMO Kills Accounts\nFear Of Missing Out makes you chase price and enter at the worst time.\n\n### Why It Happens\n- Social media brags\n- Seeing others profit\n- Lack of patience\n\n### The Fix\n1. **Have a plan**: Only trade YOUR setups\n2. **Journal misses**: Track trades you skipped. You'll see most weren't worth it\n3. **Abundance mindset**: The market always provides another opportunity\n\n**Mantra**: 'If I missed it, it wasn't my trade.'"},
            {"title": "Overcoming Revenge Trading", "content": "## Revenge Trading: The Account Killer\nAfter a loss, the urge to 'win it back' is overwhelming. This is how you blow up.\n\n### The Trap\n- Take a loss → Feel angry → Enter random trade → Bigger loss → Repeat\n\n### Prevention\n1. **Hard stop**: After 2 losses, STOP for the day\n2. **Walk away**: Physical distance from charts\n3. **Review**: Journal what happened, learn\n4. **Reset**: Come back tomorrow with clear head\n\n**Truth**: One good trade can't fix bad trading. Fix the process, not the result."}
        ]
        
        for les_data in psych_lessons:
            les = Lesson(module_id=m1.id, title=les_data["title"], content=les_data["content"], order=len([l for l in psych_lessons if psych_lessons.index(l) <= psych_lessons.index(les_data)]))
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"Psychology: {les_data['title']}", min_pass_score=80)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text="What's the best response to a losing trade?", explanation="Stop, review, and reset.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="Stop and review", is_correct=True))
            db.session.add(Option(question_id=q.id, text="Revenge trade immediately", is_correct=False))
            db.session.commit()
    
    # == COURSE 3: RISK ==
    if not Course.query.filter_by(title="Risk Management Mastery").first():
        c3 = Course(title="Risk Management Mastery", description="Survival first, profits second.", category=CourseCategory.RISK, level=CourseLevel.BEGINNER, thumbnail_url="https://images.unsplash.com/photo-1639322537228-ad71c4295843?w=800", duration_minutes=90, xp_reward=800, is_premium=False)
        db.session.add(c3)
        db.session.commit()
        m = Module(course_id=c3.id, title="Risk Fundamentals", order=1)
        db.session.add(m)
        db.session.commit()
        
        risk_lessons = [
            {"title": "The 1% Rule", "content": "## Never Risk More Than 1-2%\n\n### The Math\n$10,000 account, 1% risk = $100 max loss per trade.\n\n### Why?\n- 10 losses in a row = only 10% drawdown\n- At 10% risk per trade, 3 losses = -27% (nearly impossible to recover)\n\n**Truth**: Risk management is more important than entry strategy."},
            {"title": "Position Sizing Formula", "content": "## Calculate Lot Size\n\n**Formula**:\nLot Size = (Account Size × Risk %) / (Stop Loss in pips × Pip Value)\n\n**Example**:\n- Account: $5,000\n- Risk: 1% ($50)\n- Stop Loss: 50 pips\n- Pip Value: $10/lot\n\nLot Size = $50 / (50 × $10) = 0.1 lots\n\n**Never** guess your position size."},
            {"title": "Risk-Reward Ratios", "content": "## Minimum 1:2 RR\n\nIf you risk $100, aim for $200+ profit.\n\n### Why 1:2?\nWith 40% win rate and 1:2 RR, you're profitable.\n\n**Calculation**:\n10 trades, 4 wins, 6 losses:\n- Wins: 4 × $200 = $800\n- Losses: 6 × $100 = -$600\n- Net: +$200\n\n**Rule**: Never take trades below 1:1.5 RR."}
        ]
        
        for i, ld in enumerate(risk_lessons):
            les = Lesson(module_id=m.id, title=ld["title"], content=ld["content"], order=i+1)
            db.session.add(les)
            db.session.commit()
            quiz = Quiz(lesson_id=les.id, title=f"Risk: {ld['title']}", min_pass_score=100)
            db.session.add(quiz)
            db.session.commit()
            q = Question(quiz_id=quiz.id, text="What's the max recommended risk per trade?", explanation="1-2% to survive drawdowns.")
            db.session.add(q)
            db.session.commit()
            db.session.add(Option(question_id=q.id, text="1-2%", is_correct=True))
            db.session.add(Option(question_id=q.id, text="10%", is_correct=False))
            db.session.commit()
    
    print("✅ Full Academy Content Seeded Successfully!")

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        # Seed mock users if not exist
        if not User.query.filter_by(email='karim@trade.ma').first():
            user = User(full_name='Karim Trader', email='karim@trade.ma', role=UserRole.USER, username='karimtrader')
            user.set_password('123456')
            db.session.add(user)
        if not User.query.filter_by(email='sara@admin.ma').first():
            admin = User(full_name='Sara Admin', email='sara@admin.ma', role=UserRole.ADMIN, username='saraadmin')
            admin.set_password('admin123')
            db.session.add(admin)
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Seed Mock PayPal Config (For Exam/Demo Purposes)
        from models import SystemConfig
        if not SystemConfig.query.filter_by(key='PAYPAL_CLIENT_ID').first():
            db.session.add(SystemConfig(key='PAYPAL_CLIENT_ID', value='mock_client_id_for_demo'))
        if not SystemConfig.query.filter_by(key='PAYPAL_CLIENT_SECRET').first():
            db.session.add(SystemConfig(key='PAYPAL_CLIENT_SECRET', value='mock_secret_for_demo'))
        if not SystemConfig.query.filter_by(key='PAYPAL_EMAIL').first():
            db.session.add(SystemConfig(key='PAYPAL_EMAIL', value='business@tradesense.ma'))
        
        db.session.commit()
        print("Seeding complete.")
        print("Starting Flask server on port 5000...")
    app.run(debug=True, port=5000, host='0.0.0.0')
