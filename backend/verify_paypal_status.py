import requests
try:
    response = requests.get('https://faty2002.pythonanywhere.com/api/paypal/status')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
