
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, TradingFloor, FloorMessage

def verify_community():
    print("Verifying Community Data in MySQL...")
    
    app = create_app('development')
    
    with app.app_context():
        floors = TradingFloor.query.all()
        
        print(f"\n🏢 Total Trading Floors in Database: {len(floors)}\n")
        print("=" * 80)
        
        for floor in floors:
            messages = FloorMessage.query.filter_by(floor_id=floor.id).count()
            print(f"\n🔷 Floor: {floor.name}")
            print(f"   Type: {floor.floor_type.value}")
            print(f"   Description: {floor.description or 'N/A'}")
            print(f"   Required Level: {floor.required_level}")
            print(f"   Messages: {messages}")
        
        print("\n" + "=" * 80)
        
        total_messages = FloorMessage.query.count()
        
        print(f"\n📊 Statistics:")
        print(f"   Trading Floors: {len(floors)}")
        print(f"   Total Messages: {total_messages}")
        
        if len(floors) == 0:
            print("\n⚠️  No trading floors found. Database needs seeding.")
        else:
            print("\n✓ Community data verified in MySQL")

if __name__ == '__main__':
    verify_community()
