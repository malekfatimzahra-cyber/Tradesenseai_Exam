
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserRole(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'
    SUPERADMIN = 'SUPERADMIN'

class ChallengeStatus(enum.Enum):
    ACTIVE = 'ACTIVE'
    PASSED = 'PASSED'
    FAILED = 'FAILED'
    PENDING = 'PENDING'
    FUNDED = 'FUNDED'

class TradeStatus(enum.Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

class TradeType(enum.Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class PaymentMethod(enum.Enum):
    PAYPAL = 'PAYPAL'
    CMI = 'CMI' # Credit Card
    CRYPTO = 'CRYPTO'

class TradingFloorType(enum.Enum):
    GLOBAL = 'GLOBAL'
    SCALPING = 'SCALPING'
    SWING = 'SWING'
    CRYPTO = 'CRYPTO'
    INDICES = 'INDICES'
    FOREX = 'FOREX'

class MessageType(enum.Enum):
    TEXT = 'TEXT'
    TRADE_IDEA = 'TRADE_IDEA' # Structured: BUY/SELL symbol @ price
    ALERT = 'ALERT'
    REVIEW = 'REVIEW' # Review of user or course

class PaymentStatus(enum.Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('Account', backref='user', lazy=True)
    trades = db.relationship('Trade', backref='user', lazy=True)
    challenges = db.relationship('Challenge', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat()
        }

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Challenge Details
    plan_name = db.Column(db.String(50), default='Starter')
    initial_balance = db.Column(db.Float, default=5000.0)
    current_balance = db.Column(db.Float, default=5000.0)
    equity = db.Column(db.Float, default=5000.0)
    daily_starting_equity = db.Column(db.Float, default=5000.0)
    
    status = db.Column(db.Enum(ChallengeStatus), default=ChallengeStatus.ACTIVE)
    reason = db.Column(db.String(255), nullable=True)  # Tracks failure/pass reason
    admin_note = db.Column(db.Text, nullable=True) # Admin comments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_daily_reset = db.Column(db.Date, default=datetime.utcnow().date)
    
    trades = db.relationship('Trade', backref='account', lazy=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'equity': self.equity,
            'daily_starting_equity': self.daily_starting_equity,
            'status': self.status.value,
            'reason': self.reason,
            'daily_pnl': self.equity - self.daily_starting_equity,
            'total_pnl': self.equity - self.initial_balance
        }

class Trade(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True) # Optional link to account
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Root required: One User -> Many Trades
    
    symbol = db.Column(db.String(20), nullable=False)
    side = db.Column(db.Enum(TradeType), nullable=False) # BUY/SELL
    quantity = db.Column(db.Float, nullable=False) # User requested quantity
    price = db.Column(db.Float, nullable=False)    # User requested price
    
    # Support both old and new column names
    trade_type = db.Column(db.Enum(TradeType), nullable=True) # Alias for side
    amount = db.Column(db.Float, nullable=True) # Position size in USD
    entry_price = db.Column(db.Float, nullable=True) # Entry price
    exit_price = db.Column(db.Float, nullable=True)
    
    stop_loss = db.Column(db.Float, nullable=True)
    take_profit = db.Column(db.Float, nullable=True)
    commission = db.Column(db.Float, default=0.0)
    swap = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    
    status = db.Column(db.Enum(TradeStatus), default=TradeStatus.OPEN)
    pnl = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # User requested timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'type': (self.trade_type or self.side).value if (self.trade_type or self.side) else 'BUY',
            'side': (self.side or self.trade_type).value if (self.side or self.trade_type) else 'BUY',
            'quantity': self.quantity or (self.amount / self.entry_price if self.amount and self.entry_price else 0),
            'amount': self.amount or (self.quantity * self.price if self.quantity and self.price else 0),
            'price': self.entry_price or self.price,
            'entry_price': self.entry_price or self.price,
            'exit_price': self.exit_price,
            'sl': self.stop_loss,
            'tp': self.take_profit,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'status': self.status.value,
            'pnl': self.pnl,
            'timestamp': (self.created_at or self.timestamp).isoformat() if (self.created_at or self.timestamp) else datetime.utcnow().isoformat()
        }

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_equity = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum(ChallengeStatus), default=ChallengeStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_amount': self.target_amount,
            'current_equity': self.current_equity,
            'status': self.status.value,
            'created_at': self.created_at.isoformat()
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = db.Column(db.String(100), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'method': self.payment_method.value,
            'status': self.status.value,
            'date': self.created_at.isoformat()
        }

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(500), nullable=True)

# --- ACADEMY MODELS ---
class CourseLevel(enum.Enum):
    BEGINNER = 'BEGINNER'
    INTERMEDIATE = 'INTERMEDIATE'
    ADVANCED = 'ADVANCED'
    EXPERT = 'EXPERT'

class CourseCategory(enum.Enum):
    TECHNICAL = 'TECHNICAL'
    PSYCHOLOGY = 'PSYCHOLOGY'
    RISK = 'RISK'
    QUANT = 'QUANT'
    PLATFORM = 'PLATFORM'

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    lang = db.Column(db.String(10), default='fr') # Added
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum(CourseCategory), nullable=False)
    level = db.Column(db.Enum(CourseLevel), nullable=False)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    cover = db.Column(db.String(255), nullable=True) # Added alias for thumbnail_url if needed
    duration_minutes = db.Column(db.Integer, default=60)
    xp_reward = db.Column(db.Integer, default=100)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    modules = db.relationship('Module', backref='course', lazy=True, cascade="all, delete-orphan")
    # Quizzes can still be at course level (Final Exam) but user specifically asked for Module quizzes

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.value,
            'level': self.level.value,
            'thumbnail_url': self.thumbnail_url,
            'duration': f"{self.duration_minutes} min",
            'xp_reward': self.xp_reward,
            'premium': self.is_premium
        }

class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order_index = db.Column(db.Integer, default=1) # Renamed from order
    
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade="all, delete-orphan")
    quizzes = db.relationship('Quiz', backref='module', lazy=True, cascade="all, delete-orphan") # Link quiz to module

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'order_index': self.order_index,
            'lessons': [l.to_dict() for l in sorted(self.lessons, key=lambda x: x.order_index)]
        }

class LessonType(enum.Enum):
    TEXT = 'TEXT'

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=True) # Added
    lesson_type = db.Column(db.Enum(LessonType), default=LessonType.TEXT)
    content_type = db.Column(db.String(20), default='markdown') # Added (markdown or html)
    video_url = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    content_prompt = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, default=1) # Renamed from order
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'slug': self.slug,
            'type': self.lesson_type.value,
            'content_type': self.content_type,
            'content': self.content,
            'order_index': self.order_index
        }

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True) # Added link to module
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    title = db.Column(db.String(150), default="Quiz")
    min_pass_score = db.Column(db.Integer, default=70)

    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_answers=False):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'min_pass_score': self.min_pass_score,
            'questions': [q.to_dict(include_answers=include_answers) for q in sorted(self.questions, key=lambda x: x.order_index)]
        }

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, default=1) # Added

    options = db.relationship('Option', backref='question', lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_answers=False):
        return {
            'id': self.id,
            'text': self.text,
            'explanation': self.explanation,
            'options': [o.to_dict(include_answers=include_answers) for o in self.options]
        }

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def to_dict(self, include_answers=False):
        d = {
            'id': self.id,
            'text': self.text
        }
        if include_answers:
            d['is_correct'] = self.is_correct
        return d

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    icon_name = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), default='GENERAL')
    xp_bonus = db.Column(db.Integer, default=50)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon_name,
            'category': self.category
        }

# --- COMMUNITY / TRADING FLOORS ---
class TradingFloor(db.Model):
    __tablename__ = 'trading_floors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor_type = db.Column(db.Enum(TradingFloorType), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    icon_name = db.Column(db.String(50), default='fa-hashtag')
    required_level = db.Column(db.String(50), default='Bronze Trader') 

    messages = db.relationship('FloorMessage', backref='floor', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.floor_type.value,
            'description': self.description,
            'icon': self.icon_name,
            'required_level': self.required_level
        }

class FloorMessage(db.Model):
    __tablename__ = 'floor_messages'
    id = db.Column(db.Integer, primary_key=True)
    floor_id = db.Column(db.Integer, db.ForeignKey('trading_floors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('floor_messages.id'), nullable=True)
    
    message_type = db.Column(db.Enum(MessageType), default=MessageType.TEXT)
    content = db.Column(db.Text, nullable=False) 
    metadata_json = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    asset = db.Column(db.String(20), nullable=True)
    
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', backref='messages')
    replies = db.relationship('FloorMessage', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def to_dict(self):
        author_profit = None
        main_acc = self.sender.accounts[0] if self.sender.accounts else None
        if main_acc:
            p = ((main_acc.equity - main_acc.initial_balance) / main_acc.initial_balance) * 100
            author_profit = f"+{p:.1f}%" if p > 0 else f"{p:.1f}%"

        return {
            'id': self.id,
            'floor_id': self.floor_id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'user_name': self.sender.full_name,
            'username': '@' + self.sender.username,
            'user_avatar': f"https://ui-avatars.com/api/?name={self.sender.full_name}&background=random",
            'author_profit': author_profit,
            'type': self.message_type.value,
            'content': self.content,
            'asset': self.asset,
            'image_url': self.image_url,
            'metadata': self.metadata_json,
            'likes': self.likes_count,
            'comments_count': self.replies.count(),
            'timestamp': self.created_at.isoformat()
        }

# --- COMMUNITY FEED (POSTS & COMMENTS) ---
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = db.relationship('User', backref='posts')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'tags': self.tags,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': {
                'id': self.author.id,
                'name': self.author.full_name,
                'username': self.author.username,
                'avatar': f"https://ui-avatars.com/api/?name={self.author.full_name}&background=random"
            },
            'likes': len(self.likes),
            'comments_count': len(self.comments)
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    author = db.relationship('User', backref='post_comments')

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'author': {
                'id': self.author.id,
                'name': self.author.full_name,
                'username': self.author.username,
                'avatar': f"https://ui-avatars.com/api/?name={self.author.full_name}&background=random"
            }
        }

class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- USER PROGRESS ---
class UserCourseProgress(db.Model):
    __tablename__ = 'user_course_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    progress_percent = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

class UserLessonProgress(db.Model):
    __tablename__ = 'user_lesson_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True) # Added
    quiz_score = db.Column(db.Integer, nullable=True) 
    quiz_passed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

class UserQuizAttempt(db.Model): # New
    __tablename__ = 'user_quiz_attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    passed = db.Column(db.Boolean, default=False)
    attempt_number = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship('UserQuizAnswer', backref='attempt', lazy=True, cascade="all, delete-orphan")

class UserQuizAnswer(db.Model):
    __tablename__ = 'user_quiz_answers'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('user_quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=True)
    is_correct = db.Column(db.Boolean, default=False)

class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserXP(db.Model):
    __tablename__ = 'user_xp'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    total_xp = db.Column(db.Integer, default=0)
    level_title = db.Column(db.String(50), default="Bronze Trader")

    def to_dict(self):
        return {
            'xp': self.total_xp,
            'level': self.level_title
        }

# --- TRADESENSE AI AGENCY ---
class MarketSignal(db.Model):
    __tablename__ = 'market_signals'
    id = db.Column(db.Integer, primary_key=True)
    asset = db.Column(db.String(20), nullable=False)
    signal_type = db.Column(db.String(10), nullable=False) # BUY / SELL
    confidence = db.Column(db.Integer, default=50) # 0-100
    entry_price = db.Column(db.Float, nullable=False)
    stop_loss = db.Column(db.Float, nullable=False)
    take_profit = db.Column(db.Float, nullable=False)
    reasoning = db.Column(db.Text, nullable=True)
    quality = db.Column(db.String(20), default='MEDIUM') # HIGH, MEDIUM, LOW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'asset': self.asset,
            'type': self.signal_type,
            'confidence': self.confidence,
            'entry': self.entry_price,
            'sl': self.stop_loss,
            'tp': self.take_profit,
            'reasoning': self.reasoning,
            'quality': self.quality,
            'timestamp': self.created_at.isoformat()
        }

class RiskAlert(db.Model):
    __tablename__ = 'risk_alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Global if null
    alert_type = db.Column(db.String(50), nullable=False) # VOLATILITY, NEWS, DRAWDOWN, VIOLATION
    severity = db.Column(db.String(20), default='WARNING') # INFO, WARNING, DANGER
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.created_at.isoformat()
        }

# --- NEW: LEADERBOARD & PERFORMANCE ---
class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Link to user if real
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    
    # Snapshot Data
    username = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(5), default='MA')
    avatar_url = db.Column(db.String(255), nullable=True)
    
    # Stats
    profit = db.Column(db.Float, default=0.0)
    roi = db.Column(db.Float, default=0.0)
    win_rate = db.Column(db.Float, default=0.0)
    funded_amount = db.Column(db.Float, default=0.0)
    consistency_score = db.Column(db.Float, default=0.0) # New
    risk_score = db.Column(db.Float, default=0.0) # New
    
    ranking = db.Column(db.Integer, default=0)
    period = db.Column(db.String(20), default='ALL_TIME') # ALL_TIME, MONTHLY
    
    # JSON Data for UI efficiency
    badges = db.Column(db.Text, nullable=True) # JSON list of strings
    equity_curve = db.Column(db.Text, nullable=True) # JSON list of numbers (sparkline)
    
    is_visible = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        badges_list = []
        curve_list = []
        try:
            badges_list = json.loads(self.badges) if self.badges else []
            curve_list = json.loads(self.equity_curve) if self.equity_curve else []
        except:
            pass

        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'country': self.country,
            'avatar': self.avatar_url or f"https://ui-avatars.com/api/?name={self.username}&background=random",
            'profit': self.profit,
            'roi': self.roi,
            'winRate': self.win_rate,
            'fundedCapital': self.funded_amount,
            'consistencyScore': self.consistency_score,
            'riskScore': self.risk_score,
            'rank': self.ranking,
            'badges': badges_list,
            'sparkline': curve_list
        }

class PerformanceSnapshot(db.Model):
    __tablename__ = 'performance_snapshots'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    period = db.Column(db.String(20), default='ALL_TIME')
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    profit = db.Column(db.Float, default=0.0)
    roi = db.Column(db.Float, default=0.0)
    win_rate = db.Column(db.Float, default=0.0)
    trades_count = db.Column(db.Integer, default=0)
    equity = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminActionLog(db.Model):
    __tablename__ = 'admin_actions_log'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False) # set_passed, set_failed, lock, unlock
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('User', foreign_keys=[admin_id])
    target_account = db.relationship('Account', foreign_keys=[target_account_id])



class UserChallenge(db.Model):
    __tablename__ = 'user_challenges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan': self.plan_name,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }



class ChallengePlan(db.Model):
    __tablename__ = 'challenge_plans'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capital = db.Column(db.Integer, nullable=False)
    profit_target = db.Column(db.Integer, nullable=False)
    max_drawdown = db.Column(db.Integer, nullable=False)
    daily_loss_limit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default='MAD')
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capital': self.capital,
            'profitTarget': self.profit_target,
            'maxDrawdown': self.max_drawdown,
            'dailyLossLimit': self.daily_loss_limit,
            'price': self.price,
            'currency': self.currency,
            'description': self.description
        }

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    language = db.Column(db.String(10), default='en')
    theme = db.Column(db.String(20), default='dark')
    timezone = db.Column(db.String(50), default='UTC')
    currency = db.Column(db.String(10), default='USD')
    notifications_enabled = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'language': self.language,
            'theme': self.theme,
            'timezone': self.timezone,
            'currency': self.currency,
            'notifications_enabled': self.notifications_enabled
        }

class CourseTranslation(db.Model):
    __tablename__ = 'course_translations'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('course_id', 'lang', name='unique_course_lang'),)

class ModuleTranslation(db.Model):
    __tablename__ = 'module_translations'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    __table_args__ = (db.UniqueConstraint('module_id', 'lang', name='unique_module_lang'),)

class LessonTranslation(db.Model):
    __tablename__ = 'lesson_translations'
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('lesson_id', 'lang', name='unique_lesson_lang'),)

class QuizTranslation(db.Model):
    __tablename__ = 'quiz_translations'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(150), nullable=True)
    __table_args__ = (db.UniqueConstraint('quiz_id', 'lang', name='unique_quiz_lang'),)

class QuestionTranslation(db.Model):
    __tablename__ = 'question_translations'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('question_id', 'lang', name='unique_question_lang'),)

class OptionTranslation(db.Model):
    __tablename__ = 'option_translations'
    id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    __table_args__ = (db.UniqueConstraint('option_id', 'lang', name='unique_option_lang'),)
