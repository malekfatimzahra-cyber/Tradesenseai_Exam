
import os
import sys
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from __init__ import create_app
from models import db, TradingFloor, FloorMessage, MessageType, User

def seed_floor_messages():
    print("Seeding Trading Floor Messages...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check if messages already exist
        existing = FloorMessage.query.count()
        if existing > 0:
            print(f"Found {existing} existing messages.")
            response = input("Clear and re-seed? (y/n): ")
            if response.lower() != 'y':
                return
            FloorMessage.query.delete()
            db.session.commit()
        
        # Get floors and users
        floors = TradingFloor.query.all()
        users = User.query.limit(10).all()
        
        if len(floors) == 0:
            print("No trading floors found. Run seed_community.py first.")
            return
            
        if len(users) < 3:
            print("Not enough users for messages.")
            return
        
        # Messages data
        messages_data = [
            # Global Trading (floor 0)
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
            {
                "floor_idx": 0,
                "author_idx": 2,
                "type": MessageType.TEXT,
                "content": "Excellente journée ! +800$ de profit sur mes positions scalping 💰",
                "asset": None,
                "days_ago": 1
            },
            # Scalping (floor 1)
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
                "days_ago": 0
            },
            {
                "floor_idx": 1,
                "author_idx": 3,
                "type": MessageType.TEXT,
                "content": "Le M5 offre de belles opportunités aujourd'hui sur les paires EUR 📊",
                "asset": "EURUSD",
                "days_ago": 1
            },
            # Swing Trading (floor 2)
            {
                "floor_idx": 2,
                "author_idx": 3,
                "type": MessageType.TEXT,
                "content": "Position swing ouverte sur NASDAQ. Target +3% sur 2 semaines.",
                "asset": "NAS100",
                "days_ago": 1
            },
            {
                "floor_idx": 2,
                "author_idx": 1,
                "type": MessageType.TEXT,
                "content": "Patience et discipline, c'est le secret du swing trading réussi 🎯",
                "asset": None,
                "days_ago": 2
            },
            # Crypto (floor 3)
            {
                "floor_idx": 3,
                "author_idx": 1,
                "type": MessageType.TRADE_IDEA,
                "content": "BTC breakout imminent ! Zone d'achat 44500-45000 🚀",
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
                "days_ago": 0
            },
            {
                "floor_idx": 3,
                "author_idx": 0,
                "type": MessageType.TEXT,
                "content": "Altcoin season arrive ? Les volumes explosent ! 🔥",
                "asset": None,
                "days_ago": 1
            },
            # Indices (floor 4)
            {
                "floor_idx": 4,
                "author_idx": 0,
                "type": MessageType.TEXT,
                "content": "SP500 en mode consolidation. Attente du breakout pour entrer.",
                "asset": "SPX500",
                "days_ago": 0
            },
            {
                "floor_idx": 4,
                "author_idx": 4,
                "type": MessageType.TRADE_IDEA,
                "content": "DAX30 signal LONG @ 16850 | SL: 16750 | TP: 17050",
                "asset": "DAX30",
                "metadata": '{"entry": 16850, "sl": 16750, "tp": 17050}',
                "days_ago": 1
            }
        ]
        
        print(f"\nCreating {len(messages_data)} messages...")
        
        for msg_data in messages_data:
            floor = floors[msg_data["floor_idx"]] if msg_data["floor_idx"] < len(floors) else floors[0]
            author = users[msg_data["author_idx"] % len(users)]
            created_at = datetime.utcnow() - timedelta(days=msg_data["days_ago"], hours=msg_data.get("hours_ago", 0))
            
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
            print(f"  ✓ {floor.name}: {msg_data['content'][:50]}...")
        
        db.session.commit()
        
        print("\n✅ Messages Successfully Seeded!")
        print(f"Total: {len(messages_data)} messages across {len(floors)} floors")

if __name__ == '__main__':
    seed_floor_messages()
