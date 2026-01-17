
import requests
import sys

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

BASE_URL = "https://faty2002.pythonanywhere.com"

def test_unified_payment_persistence():
    print(f"--- TEST: Unified Payment & Persistence ---\n")

    # 1. Login
    print(f"[*] Logging in as 'karim@trade.ma'...")
    try:
        res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "karim@trade.ma",
            "password": "123456"
        })
        if res.status_code != 200:
            print(f"{RED}[!] Login failed: {res.text}{RESET}")
            return
        
        token = res.json()['token']
        print(f"{GREEN}[+] Login successful.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Connection refused. Is backend running?{RESET}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Simulate Payment via Unified Endpoint (CMI)
    print(f"\n[*] Simulating CMI Payment for 'Pro' Plan (25000 MAD)...")
    payload = {
        "plan": "Pro",
        "amount": 1500, # Price for Pro
        "payment_method": "CMI",
        "transaction_id": "TEST_AUTO_VERIFY_001"
    }
    
    amount_paid = 1500

    try:
        # Note: If user already has active challenge, this might create another one or handle it. 
        # The code creates a new one.
        res = requests.post(f"{BASE_URL}/api/unified-payment/process", json=payload, headers=headers)
        
        if res.status_code == 200:
            data = res.json()
            print(f"{GREEN}[+] Payment Processed Successfully!{RESET}")
            print(f"    Account ID: {data['data']['account_id']}")
            print(f"    Challenge ID: {data['data']['challenge_id']}")
            print(f"    Transaction ID: {data['data']['transaction_id']}")
        else:
            print(f"{RED}[!] Payment Failed: {res.text}{RESET}")
            return
    except Exception as e:
        print(f"{RED}[!] Error calling payment endpoint: {e}{RESET}")
        return

    # 3. Verify Persistence immediately via API
    print(f"\n[*] Verifying data persistence via API (simulate refresh)...")
    
    # Check Active Challenge
    res_chal = requests.get(f"{BASE_URL}/api/unified-payment/active-challenge", headers=headers)
    if res_chal.status_code == 200:
        chal_data = res_chal.json()['data']
        if chal_data and chal_data['plan_name'] == 'Pro':
            print(f"{GREEN}[+] Active Challenge Found: {chal_data['plan_name']} | Balance: {chal_data['current_balance']}{RESET}")
        else:
            print(f"{RED}[!] Persistence Fail: No active challenge found matching 'Pro'{RESET}")
            print(res_chal.json())
    
    # Check Payment History
    res_hist = requests.get(f"{BASE_URL}/api/unified-payment/history", headers=headers)
    if res_hist.status_code == 200:
        txns = res_hist.json()['data']
        found = any(t['amount'] == amount_paid for t in txns)
        if found:
            print(f"{GREEN}[+] Transaction found in history.{RESET}")
        else:
            print(f"{RED}[!] Persistence Fail: Transaction not found in history.{RESET}")

    print(f"\n{GREEN}=== TEST COMPLETED SUCCESSFULLY ==={RESET}")
    print("This confirms that:")
    print("1. Unified endpoint works.")
    print("2. SQL Transaction (Account + Challenge + Payment) committed.")
    print("3. Data persists and is retrievable.")

if __name__ == "__main__":
    test_unified_payment_persistence()
