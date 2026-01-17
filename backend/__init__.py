"""
Application Factory Pattern for Flask.
Creates and configures the Flask application instance.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import get_config
import os


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration environment ('development', 'testing', 'production')
                          If None, uses FLASK_ENV environment variable
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables and seed initial data
    with app.app_context():
        initialize_database(app)
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'environment': config_name,
            'database': 'connected'
        }), 200
    
    # Database test route
    @app.route('/api/test-db', methods=['GET'])
    def test_db():
        """Test database connection."""
        try:
            # Try to execute a simple query
            db.session.execute(db.text('SELECT 1'))
            return jsonify({
                'status': 'success',
                'message': 'Database Connected!',
                'database': app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]  # Hide credentials
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Database connection failed',
                'error': str(e)
            }), 500
    
    return app


def register_blueprints(app):
    """Register all application blueprints."""
    
    # Import and register auth routes (will be created separately)
    try:
        from auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
    except ImportError:
        # If auth_routes doesn't exist yet, register inline
        from flask import Blueprint
        auth_bp = Blueprint('auth', __name__)
        
        @auth_bp.route('/register', methods=['POST'])
        def register():
            from flask import request
            from models import User, UserRole
            data = request.json
            if not data or not data.get('email') or not data.get('password'):
                return jsonify({'message': 'Missing data'}), 400
            if User.query.filter_by(email=data.get('email')).first():
                return jsonify({'message': 'Email exists'}), 409
            
            new_user = User(
                full_name=data.get('full_name', 'User'),
                email=data.get('email'),
                role=UserRole.USER
            )
            new_user.set_password(data.get('password'))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Registered'}), 201
        
        @auth_bp.route('/login', methods=['POST'])
        def login():
            from flask import request
            from models import User
            import jwt
            import datetime
            
            data = request.json
            user = User.query.filter_by(email=data.get('email')).first()
            if not user or not user.check_password(data.get('password')):
                return jsonify({'message': 'Invalid credentials'}), 401
            
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'])
            
            return jsonify({'token': token, 'user': user.to_dict()})
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Import other blueprints
    # Import other blueprints
    from payments import payments_bp
    from market_data import market_bp
    from academy import academy_bp
    from community import community_bp
    from ai_agency import ai_agency_bp
    from trading import trading_bp
    from admin_routes import admin_bp
    from ai_analysis import ai_analysis_bp
    from gemini_chat import gemini_chat_bp
    from news_routes import news_bp
    from challenges import challenges_bp
    from trades_routes import trades_bp
    from payment import payment_bp
    from paypal_config import paypal_config_bp
    from unified_payment import unified_payment_bp  # NEW
    
    # Register all blueprints
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(trading_bp, url_prefix='/api/trading')
    app.register_blueprint(trades_bp, url_prefix='/api/trades')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(academy_bp, url_prefix='/api/academy')
    app.register_blueprint(community_bp, url_prefix='/api/community')
    app.register_blueprint(ai_agency_bp, url_prefix='/api/ai-agency')
    app.register_blueprint(ai_analysis_bp, url_prefix='/api')
    app.register_blueprint(gemini_chat_bp, url_prefix='/api')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    app.register_blueprint(challenges_bp, url_prefix='/api/challenges')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(paypal_config_bp, url_prefix='/api/paypal')
    app.register_blueprint(unified_payment_bp, url_prefix='/api/unified-payment')  # NEW

    from mock_payment import mock_payment_bp
    app.register_blueprint(mock_payment_bp, url_prefix='/api')



def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback any failed transactions
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


def initialize_database(app):
    """
    Initialize database tables and seed initial data.
    Only runs in development mode.
    """
    from models import User, UserRole
    
    try:
        # Create all tables
        db.create_all()
        app.logger.info("Database tables created successfully")
        
        # Seed initial data only in development
        if app.config.get('DEBUG'):
            seed_initial_data()
            seed_plans_data()
            app.logger.info("Initial data seeded successfully")
            
    except Exception as e:
        app.logger.error(f"Database initialization failed: {str(e)}")
        raise


def seed_initial_data():
    """Seed initial users and data for development."""
    from models import User, UserRole
    
    # Create default users if they don't exist
    if not User.query.filter_by(email='karim@trade.ma').first():
        user = User(
            full_name='Karim Trader',
            username='karim_trader',
            email='karim@trade.ma',
            role=UserRole.USER
        )
        user.set_password('123456')
        db.session.add(user)
        print("✓ Created demo user: karim@trade.ma / 123456")
    
    if not User.query.filter_by(email='sara@admin.ma').first():
        admin = User(
            full_name='Sara Admin',
            username='sara_admin',
            email='sara@admin.ma',
            role=UserRole.ADMIN
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Created admin user: sara@admin.ma / admin123")
    
    if not User.query.filter_by(email='superadmin@tradesense.ma').first():
        superadmin = User(
            full_name='Super Admin',
            username='super_admin',
            email='superadmin@tradesense.ma',
            role=UserRole.SUPERADMIN
        )
        superadmin.set_password('superadmin123')
        db.session.add(superadmin)
        print("✓ Created superadmin: superadmin@tradesense.ma / superadmin123")
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding data: {str(e)}")

def seed_plans_data():
    """Seed challenge plans."""
    from models import ChallengePlan
    
    plans = [
             { 'id': 'starter', 'name': 'Starter Challenge', 'capital': 5000, 'profit_target': 500, 'max_drawdown': 500, 'daily_loss_limit': 250, 'price': 200, 'currency': 'MAD' },
             { 'id': 'pro', 'name': 'Professional Pro', 'capital': 25000, 'profit_target': 2500, 'max_drawdown': 2500, 'daily_loss_limit': 1250, 'price': 500, 'currency': 'MAD' },
             { 'id': 'elite', 'name': 'Elite Institutional', 'capital': 100000, 'profit_target': 10000, 'max_drawdown': 10000, 'daily_loss_limit': 5000, 'price': 1000, 'currency': 'MAD' },
    ]
    
    for p in plans:
        # Check if plan exists
        existing = ChallengePlan.query.get(p['id'])
        if not existing:
            new_plan = ChallengePlan(
                id=p['id'],
                name=p['name'],
                capital=p['capital'],
                profit_target=p['profit_target'],
                max_drawdown=p['max_drawdown'],
                daily_loss_limit=p['daily_loss_limit'],
                price=p['price'],
                currency=p['currency'],
                is_active=True
            )
            db.session.add(new_plan)
            print(f"Created Plan: {p['name']}")
    
    try:
        db.session.commit()
        print("✓ Plans Seeded Successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding plans: {str(e)}")

