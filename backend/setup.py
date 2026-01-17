"""
Quick setup script for TradeSense Backend.
This script helps configure the database connection and verify the setup.
"""
import os
import sys
import getpass
from pathlib import Path


def create_env_file():
    """Create .env file with user input."""
    print("\n" + "="*60)
    print("🔧 TradeSense Backend Setup")
    print("="*60 + "\n")
    
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("✓ Keeping existing .env file")
            return
    
    print("Please provide your MySQL database credentials:\n")
    
    # Get database credentials
    db_user = input("MySQL Username [root]: ").strip() or "root"
    db_password = getpass.getpass("MySQL Password: ").strip()
    db_host = input("MySQL Host [localhost]: ").strip() or "localhost"
    db_port = input("MySQL Port [3306]: ").strip() or "3306"
    db_name = input("Database Name [tradesense]: ").strip() or "tradesense"
    
    # Get Flask configuration
    print("\nFlask Configuration (press Enter for defaults):\n")
    flask_env = input("Environment (development/production) [development]: ").strip() or "development"
    flask_port = input("Server Port [5000]: ").strip() or "5000"
    
    # Generate secret key
    import secrets
    secret_key = secrets.token_hex(32)
    jwt_secret = secrets.token_hex(32)
    
    # Create .env content
    env_content = f"""# Flask Configuration
FLASK_ENV={flask_env}
FLASK_HOST=0.0.0.0
FLASK_PORT={flask_port}

# Security (Auto-generated)
SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret}

# MySQL Database Configuration
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}

# PayPal Configuration (Optional - Update if needed)
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox

# Gemini AI (Optional - Update if needed)
VITE_GEMINI_API_KEY=your_gemini_api_key
"""
    
    # Write to file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("\n✓ .env file created successfully!")
    print(f"✓ Location: {env_path}")


def test_database_connection():
    """Test MySQL database connection."""
    print("\n" + "="*60)
    print("🔍 Testing Database Connection")
    print("="*60 + "\n")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import pymysql
        
        # Get credentials from environment
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'tradesense'),
            'charset': 'utf8mb4'
        }
        
        print(f"Connecting to: {db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
        
        # Try to connect
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"\n✓ Connection successful!")
            print(f"✓ MySQL Version: {version[0]}")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"✓ Found {len(tables)} existing tables")
            else:
                print("ℹ️  No tables found (will be created on first run)")
        
        connection.close()
        return True
        
    except ImportError as e:
        print(f"\n✗ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False
        
    except pymysql.err.OperationalError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nPossible solutions:")
        print("  1. Check if MySQL server is running")
        print("  2. Verify your credentials in .env file")
        print("  3. Ensure database 'tradesense' exists:")
        print("     CREATE DATABASE tradesense CHARACTER SET utf8mb4;")
        return False
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    print("\n" + "="*60)
    print("🗄️  Database Setup")
    print("="*60 + "\n")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import pymysql
        
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
        db_name = os.getenv('DB_NAME', 'tradesense')
        
        # Connect without specifying database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Check if database exists
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            exists = cursor.fetchone()
            
            if exists:
                print(f"✓ Database '{db_name}' already exists")
            else:
                # Create database
                cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✓ Database '{db_name}' created successfully!")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def initialize_tables():
    """Initialize database tables using SQLAlchemy."""
    print("\n" + "="*60)
    print("📊 Initializing Database Tables")
    print("="*60 + "\n")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import app factory
        sys.path.insert(0, str(Path(__file__).parent))
        from __init__ import create_app
        from models import db
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✓ All database tables created successfully!")
            
            # Show created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error initializing tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main setup workflow."""
    print("\n" + "="*70)
    print(" "*20 + "🚀 TradeSense Backend Setup")
    print("="*70)
    
    # Step 1: Create .env file
    create_env_file()
    
    # Step 2: Create database if needed
    if create_database_if_not_exists():
        # Step 3: Test connection
        if test_database_connection():
            # Step 4: Initialize tables
            initialize_tables()
            
            print("\n" + "="*60)
            print("✅ Setup Complete!")
            print("="*60)
            print("\nNext steps:")
            print("  1. Review your .env file")
            print("  2. Start the server: python run.py")
            print("  3. Test the API: http://localhost:5000/api/test-db")
            print("\n" + "="*60 + "\n")
        else:
            print("\n⚠️  Setup incomplete. Please fix the connection issues above.")
    else:
        print("\n⚠️  Setup incomplete. Please fix the database issues above.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
