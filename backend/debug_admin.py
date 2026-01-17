import requests

try:
    url = "http://localhost:5000/api/admin/dashboard"
    headers = {"X-ADMIN-KEY": "TRADESENSE_SUPER_SECRET_2026"}
    res = requests.get(url, headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")
