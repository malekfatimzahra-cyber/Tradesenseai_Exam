
import os
import sys
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db

def fix_floor_messages_schema():
    print("Fixing 'floor_messages' table schema...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('floor_messages')]
            print(f"Current columns: {columns}")
            
            missing_cols = []
            
            if 'parent_id' not in columns:
                missing_cols.append(('parent_id', 'INTEGER NULL'))
            
            if 'message_type' not in columns:
                missing_cols.append(('message_type', "ENUM('TEXT', 'TRADE_IDEA', 'ALERT', 'REVIEW') DEFAULT 'TEXT'"))
                
            if 'metadata_json' not in columns:
                missing_cols.append(('metadata_json', 'TEXT NULL'))
            
            if 'image_url' not in columns:
                missing_cols.append(('image_url', 'VARCHAR(255) NULL'))
                
            if 'asset' not in columns:
                missing_cols.append(('asset', 'VARCHAR(20) NULL'))
            
            if 'likes_count' not in columns:
                missing_cols.append(('likes_count', 'INTEGER DEFAULT 0'))
            
            with db.engine.connect() as conn:
                for col_name, sql_def in missing_cols:
                    print(f"Adding column: {col_name}...")
                    try:
                        conn.execute(text(f"ALTER TABLE floor_messages ADD COLUMN {col_name} {sql_def}"))
                        conn.commit()
                        print(f"  ✓ Added: {col_name}")
                    except Exception as e:
                        print(f"  Error adding {col_name}: {e}")
            
            # Add Foreign Key for parent_id if needed
            if 'parent_id' in missing_cols:
                print("Adding foreign key constraint for parent_id...")
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text(
                            "ALTER TABLE floor_messages ADD CONSTRAINT fk_parent_message "
                            "FOREIGN KEY (parent_id) REFERENCES floor_messages(id)"
                        ))
                        conn.commit()
                        print("  ✓ Added FK constraint")
                except Exception as e:
                    print(f"  Note: {e}")
            
            print("Schema fix completed.")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    fix_floor_messages_schema()
