
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, SystemConfig

def init_paypal_config():
    print("Initializing PayPal Configuration in Database...")
    
    app = create_app('development')
    
    with app.app_context():
        # Default PayPal configurations
        default_configs = {
            'PAYPAL_CLIENT_ID': '',
            'PAYPAL_CLIENT_SECRET': '',
            'PAYPAL_EMAIL': '',
            'PAYPAL_SANDBOX_MODE': 'true'
        }
        
        for key, default_value in default_configs.items():
            existing = SystemConfig.query.filter_by(key=key).first()
            
            if not existing:
                config = SystemConfig(key=key, value=default_value)
                db.session.add(config)
                print(f"  ✓ Created: {key}")
            else:
                print(f"  ℹ Already exists: {key} = {existing.value}")
        
        db.session.commit()
        
        print("\n✅ PayPal configuration initialized!")
        print("\n📝 Next Steps:")
        print("1. Login as SuperAdmin")
        print("2. Go to Admin Dashboard → PayPal Settings")
        print("3. Enter your PayPal Developer credentials")
        print("4. Save and test the connection")

if __name__ == '__main__':
    init_paypal_config()
