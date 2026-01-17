
import sys
import os

# Add directory to path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend import create_app

app = create_app('development')
print("--- URL MAP ---")
for rule in app.url_map.iter_rules():
    if 'mock-payment' in str(rule):
        print(rule)
print("--- END URL MAP ---")
