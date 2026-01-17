import requests
import sys

print("🔍 Checking backend server status...\n")

# Check health endpoint
try:
    health_response = requests.get('https://faty2002.pythonanywhere.com/api/health', timeout=2)
    print(f"✅ Health endpoint: {health_response.status_code}")
    print(f"   Response: {health_response.json()}\n")
except Exception as e:
    print(f"❌ Health endpoint failed: {e}\n")
    sys.exit(1)

# Check if auth endpoints exist
endpoints_to_test = [
    ('POST', 'https://faty2002.pythonanywhere.com/api/auth/login'),
    ('POST', 'https://faty2002.pythonanywhere.com/api/auth/register'),
]

for method, url in endpoints_to_test:
    try:
        if method == 'POST':
            r = requests.post(url, json={}, timeout=2)
        else:
            r = requests.get(url, timeout=2)
        
        print(f"✅ {method} {url}")
        print(f"   Status: {r.status_code}")
        print(f"   Response: {r.json()}\n")
    except Exception as e:
        print(f"❌ {method} {url}")
        print(f"   Error: {e}\n")

# Try actual login
print("🔐 Testing login with test user...")
try:
    login_response = requests.post(
        'https://faty2002.pythonanywhere.com/api/auth/login',
        json={'email': 'admin@tradesense.com', 'password': 'admin123'},
        timeout=2
    )
    print(f"Status: {login_response.status_code}")
    print(f"Response: {login_response.json()}")
    
    if login_response.status_code == 200:
        print("\n✅ LOGIN WORKS! Backend is ready.")
    else:
        print(f"\n⚠️  Login failed: {login_response.json()}")
except Exception as e:
    print(f"❌ Login test failed: {e}")
