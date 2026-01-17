"""
Simple test: Try to login with credentials
"""
import requests

print("="*60)
print("TESTING LOGIN")
print("="*60)

credentials = [
    ('admin@tradesense.com', 'admin123'),
    ('test@test.com', 'test123'),
    ('karim@trade.ma', '123456'),
    ('sara@admin.ma', 'admin123'),
]

for email, password in credentials:
    print(f"\nTrying: {email} / {password}")
    try:
        r = requests.post(
            'http://localhost:5000/api/auth/login',
            json={'email': email, 'password': password},
            timeout=5
        )
        print(f"Status: {r.status_code}")
        data = r.json()
        if r.status_code == 200:
            print(f"✅ SUCCESS! Token: {data.get('token', 'N/A')[:20]}...")
            print(f"   User: {data.get('user', {}).get('username')}")
            break
        else:
            print(f"❌ Failed: {data.get('message')}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("\n❌ All login attempts failed!")
