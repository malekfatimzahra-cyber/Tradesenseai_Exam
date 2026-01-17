
import os
import sys
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db

def fix_trades_schema():
    print("Starting schema fix for 'trades' table...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # 1. Check existing columns
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('trades')]
            print(f"Current columns in 'trades': {columns}")
            
            # 2. Add 'trade_type' if missing
            if 'trade_type' not in columns:
                print("Adding missing column: trade_type")
                with db.engine.connect() as conn:
                    # Enum needs to be handled carefully in raw SQL, usually VARCHAR or ENUM type.
                    # safe to use VARCHAR(10) or ENUM('BUY','SELL')
                    conn.execute(text("ALTER TABLE trades ADD COLUMN trade_type ENUM('BUY', 'SELL') NULL"))
                    conn.commit()
                print("Added 'trade_type'.")
            else:
                print("'trade_type' column already exists.")

            # 3. Add 'amount' if missing (User mentioned amount in models)
            if 'amount' not in columns:
                print("Adding missing column: amount")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE trades ADD COLUMN amount FLOAT NULL"))
                    conn.commit()
                print("Added 'amount'.")
            else:
                print("'amount' column already exists.")

            # 4. Add 'entry_price' if missing
            if 'entry_price' not in columns:
                print("Adding missing column: entry_price")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE trades ADD COLUMN entry_price FLOAT NULL"))
                    conn.commit()
                print("Added 'entry_price'.")
            else:
                print("'entry_price' column already exists.")

            print("Trades schema fix completed.")
            
        except Exception as e:
            print(f"Error fixing schema: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_trades_schema()
