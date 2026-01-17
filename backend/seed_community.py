
import os
import sys
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, TradingFloor, FloorMessage, TradingFloorType, MessageType, User

def seed_community():
    print("Seeding Community Trading Floors...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check if floors already exist
        existing = TradingFloor.query.count()
        if existing > 0:
            print(f"Found {existing} existing floors. Skipping seed.")
            return
        
        # Create Trading Floors
        floors_data = [
            {
                "name": "Global Trading",
                "type": TradingFloorType.GLOBAL,
                "description": "Discussion générale sur le trading",
                "icon": "fa-globe",
                "level": "Bronze Trader"
            },
            {
                "name": "Forex Scalping",
                "type": TradingFloorType.SCALPING,
                "description": "Stratégies de scalping rapide",
                "icon": "fa-bolt",
                "level": "Silver Trader"
            },
            {
                "name": "Swing Trading",
                "type": TradingFloorType.SWING,
                "description": "Positions de moyen terme",
                "icon": "fa-chart-line",
                "level": "Bronze Trader"
            },
            {
                "name": "Crypto Trading",
                "type": TradingFloorType.CRYPTO,
                "description": "Bitcoin, Ethereum et altcoins",
                "icon": "fa-bitcoin",
                "level": "Bronze Trader"
            },
            {
                "name": "Indices & Actions",
                "type": TradingFloorType.INDICES,
                "description": "SP500, Nasdaq, stocks",
                "icon": "fa-chart-pie",
                "level": "Gold Trader"
            }
        ]
        
        created_floors = []
        
        print("\nCreating Trading Floors...")
        for floor_data in floors_data:
            floor = TradingFloor(
                name=floor_data["name"],
                floor_type=floor_data["type"],
                description=floor_data["description"],
                icon_name=floor_data["icon"],
                required_level=floor_data["level"]
            )
            db.session.add(floor)
            db.session.commit()
            created_floors.append(floor)
            print(f"  ✓ {floor.name}")
        
        # Get users for messages
        users = User.query.limit(10).all()
        if len(users) < 3:
            print("Not enough users for messages.")
            return
        
        # Add sample messages to floors
        print("\nAdding sample messages...")
        
        messages_data = [
            # Global Trading
            {
                "floor_idx": 0,
                "author_idx": 0,
                "type": MessageType.TEXT,
                "content": "Bonjour à tous ! Qui trade le Gold aujourd'hui ? 🚀",
                "asset": "XAUUSD",
                "days_ago": 0
            },
            {
                "floor_idx": 0,
                "author_idx": 1,
                "type": MessageType.TRADE_IDEA,
                "content": "Signal LONG EUR/USD @ 1.0850 | SL: 1.0820 | TP: 1.0920",
                "asset": "EURUSD",
                "metadata": '{"entry": 1.0850, "sl": 1.0820, "tp": 1.0920}',
                "days_ago": 0
            },
            # Forex Scalping
            {
                "floor_idx": 1,
                "author_idx": 2,
                "type": MessageType.TEXT,
                "content": "Session de scalping sur GBP/USD en cours. 5 trades, 4 gagnants ! 💪",
                "asset": "GBPUSD",
                "days_ago": 0
            },
            {
                "floor_idx": 1,
                "author_idx": 0,
                "type": MessageType.ALERT,
                "content": "⚠️ Forte volatilité sur le Yen - Attention aux spreads !",
                "asset": "USDJPY",
                "days_ago": 1
            },
            # Swing Trading
            {
                "floor_idx": 2,
                "author_idx": 3,
                "type": MessageType.TEXT,
                "content": "Position swing ouverte sur NASDAQ. Target +3% sur 2 semaines.",
                "asset": "NAS100",
                "days_ago": 1
            },
            # Crypto Trading
            {
                "floor_idx": 3,
                "author_idx": 1,
                "type": MessageType.TRADE_IDEA,
                "content": "BTC breakout imminent ! Zone d'achat 44500-45000",
                "asset": "BTCUSD",
                "metadata": '{"entry": 44750, "sl": 43500, "tp": 48000}',
                "days_ago": 0
            },
            {
                "floor_idx": 3,
                "author_idx": 2,
                "type": MessageType.TEXT,
                "content": "Ethereum teste les 2400$. Belle opportunité pour les bulls 📈",
                "asset": "ETHUSD",
                "days_ago": 1
            },
            # Indices
            {
                "floor_idx": 4,
                "author_idx": 0,
                "type": MessageType.TEXT,
                "content": "SP500 en mode consolidation. Attente du breakout pour entrer.",
                "asset": "SPX500",
                "days_ago": 2
            }
        ]
        
        for msg_data in messages_data:
            floor = created_floors[msg_data["floor_idx"]]
            author = users[msg_data["author_idx"] % len(users)]
            created_at = datetime.utcnow() - timedelta(days=msg_data["days_ago"])
            
            message = FloorMessage(
                floor_id=floor.id,
                user_id=author.id,
                message_type=msg_data["type"],
                content=msg_data["content"],
                asset=msg_data.get("asset"),
                metadata_json=msg_data.get("metadata"),
                likes_count=0,
                created_at=created_at
            )
            db.session.add(message)
        
        db.session.commit()
        
        print("\n✅ Community Successfully Seeded!")
        print("=" * 60)
        print(f"Total: {len(created_floors)} Trading Floors")
        print(f"Sample Messages: {len(messages_data)}")

if __name__ == '__main__':
    seed_community()
