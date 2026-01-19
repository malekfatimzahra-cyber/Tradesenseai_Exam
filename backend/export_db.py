
import os
import sys
import datetime

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import app
from models import db
from sqlalchemy import text, inspect

def export_database():
    print("🚀 Starting Database Export...")
    
    output_file = os.path.join(os.path.dirname(backend_dir), 'database.sql')
    
    with app.app_context():
        # Using the engine from the configured app (should be Railway if env is set)
        engine = db.engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- TradeSense AI Database Export\n")
            f.write(f"-- Generated: {datetime.datetime.now()}\n")
            f.write(f"-- ------------------------------------------------------\n\n")
            
            # Disable FK checks
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            for table_name in tables:
                print(f"Processing table: {table_name}")
                f.write(f"-- Table structure for table `{table_name}`\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                
                # Get Create Table
                try:
                    # Generic fallback or specific mysql
                    create_table_sql = db.session.execute(text(f"SHOW CREATE TABLE `{table_name}`")).fetchone()[1]
                    f.write(f"{create_table_sql};\n\n")
                except Exception as e:
                    print(f"Warning: Could not get CREATE TABLE for {table_name}: {e}")
                    # Fallback? SQLAlchemy doesn't easily give raw CREATE TABLE without specific dialect calls
                    
                # Get Data
                f.write(f"-- Dumping data for table `{table_name}`\n")
                # f.write(f"LOCK TABLES `{table_name}` WRITE;\n")
                
                rows = db.session.execute(text(f"SELECT * FROM `{table_name}`")).fetchall()
                if rows:
                    f.write(f"INSERT INTO `{table_name}` VALUES \n")
                    values_list = []
                    for i, row in enumerate(rows):
                        # Format value
                        vals = []
                        for val in row:
                            if val is None:
                                vals.append("NULL")
                            elif isinstance(val, (int, float)):
                                vals.append(str(val))
                            elif isinstance(val, datetime.datetime):
                                vals.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                            elif isinstance(val, bool):
                                vals.append("1" if val else "0")
                            else:
                                # Escape string
                                safe_val = str(val).replace("'", "''").replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r")
                                vals.append(f"'{safe_val}'")
                        values_list.append(f"({', '.join(vals)})")
                        
                        # Batching to avoid huge lines
                        if (i + 1) % 100 == 0:
                            f.write(",\n".join(values_list) + ";\n")
                            if i < len(rows) - 1:
                                f.write(f"INSERT INTO `{table_name}` VALUES \n")
                            values_list = []
                            
                    if values_list:
                        f.write(",\n".join(values_list) + ";\n")
                        
                # f.write(f"UNLOCK TABLES;\n\n")
            
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
            
    print(f"✅ Database exported to {output_file}")

if __name__ == "__main__":
    export_database()
