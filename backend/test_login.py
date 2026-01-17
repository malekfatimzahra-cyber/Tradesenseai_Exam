import requests
import json

# Test login
print("Testing login endpoint...")
try:
    response = requests.post(
        'https://faty2002.pythonanywhere.com/api/auth/login',
        json={'email': 'admin@tradesense.com', 'password': 'admin123'},
        timeout=5
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
