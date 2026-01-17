
import os
import sys
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db

def fix_full_trades_schema():
    print("Starting COMPREHENSIVE schema fix for 'trades' table...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('trades')]
            print(f"Current columns: {columns}")
            
            # List of columns to check and adding logic
            # (Column Name, SQL Definition)
            missing_cols = [
                ('trade_type', "ENUM('BUY', 'SELL') NULL"),
                ('amount', "FLOAT NULL"),
                ('entry_price', "FLOAT NULL"),
                ('exit_price', "FLOAT NULL"),
                ('created_at', "DATETIME DEFAULT CURRENT_TIMESTAMP"),
                ('closed_at', "DATETIME NULL"),
                ('timestamp', "DATETIME DEFAULT CURRENT_TIMESTAMP"),
                ('commission', "FLOAT DEFAULT 0.0"),
                ('swap', "FLOAT DEFAULT 0.0"),
                ('notes', "TEXT NULL"),
                ('pnl', "FLOAT DEFAULT 0.0"),
                ('stop_loss', "FLOAT NULL"),
                ('take_profit', "FLOAT NULL"),
                ('status', "ENUM('OPEN', 'CLOSED') DEFAULT 'OPEN'")
            ]

            with db.engine.connect() as conn:
                for col_name, sql_def in missing_cols:
                    if col_name not in columns:
                        print(f"Adding missing column: {col_name}...")
                        try:
                            # Using implicit transaction from context manager if possible, but explicit valid too
                            conn.execute(text(f"ALTER TABLE trades ADD COLUMN {col_name} {sql_def}"))
                            conn.commit()
                            print(f"   Success: {col_name}")
                        except Exception as inner_e:
                            print(f"   Failed to add {col_name}: {inner_e}")
                    else:
                        print(f"   Exists: {col_name}")

            print("Comprehensive schema fix completed.")
            
        except Exception as e:
            print(f"Error fixing schema: {e}")

if __name__ == '__main__':
    fix_full_trades_schema()
