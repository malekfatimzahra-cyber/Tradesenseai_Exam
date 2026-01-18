
# 🚀 Deployment Guide: Vercel + PythonAnywhere

This guide explains how to deploy **TradeSense AI** with a **Frontend on Vercel** and **Backend on PythonAnywhere**, ensuring they communicate correctly.

---

## 🏗️ Phase 1: Backend Deployment (PythonAnywhere)

The "Network error" happens because Vercel cannot reach your localhost. You MUST deploy the backend to the public internet.

### 1. Create Account & Web App
1. Sign up/Log in to [PythonAnywhere](https://www.pythonanywhere.com/).
2. Go to **Web** tab -> **Add a new web app**.
3. Select **Flask** -> **Python 3.10** (or latest).
4. Path to source code: `/home/yourusername/tradesense/backend`.

### 2. Upload Code
1. Go to **Files** tab.
2. Create a folder `tradesense`.
3. Inside, upload your `backend` folder contents (zip it locally, upload, then unzip in Bash console).
   ```bash
   unzip backend.zip
   ```

### 3. Install Dependencies
Open a **Bash Console** on PythonAnywhere:
```bash
cd tradesense/backend
mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt
pip install mysql-connector-python
```

### 4. Setup Database (MySQL)
1. Go to **Databases** tab on PythonAnywhere.
2. Initialize MySQL (create a password).
3. Create a database named `tradesense`.
4. **IMPORTANT**: Note your database connection string:
   `mysql+pymysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$tradesense`

### 5. Configure Environment Variables
You cannot use `.env` easily in WSGI, so edit your WSGI configuration file (link on Web tab):
```python
import os
import sys

# Add your project directory
path = '/home/yourusername/tradesense/backend'
if path not in sys.path:
    sys.path.append(path)

# Set Environment Variables
os.environ['DATABASE_URL'] = 'mysql+pymysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$tradesense'
os.environ['SECRET_KEY'] = 'production_secret_key_here'
os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

### 6. Run Migrations / Seed Data
In Bash Console:
```bash
export DATABASE_URL='mysql+pymysql://yourusername:... (same as above)'
python seed_all_8_mysql.py
```
*Note: Ensure `seed_all_8_mysql.py` uses `os.getenv('DATABASE_URL')`.*

### 7. Reload Web App
Go to **Web** tab and click **Reload**.
Your API is now live at: `https://yourusername.pythonanywhere.com/api`.

---

## 🌐 Phase 2: Frontend Deployment (Vercel)

### 1. Push to GitHub
Ensure your latest code (especially `store.ts` changes) is on GitHub.

### 2. Configure Vercel Project
1. Go to [Vercel Dashboard](https://vercel.com/dashboard).
2. Import your TradeSense repository.
3. **Environment Variables**:
   Add a new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://yourusername.pythonanywhere.com/api` (Replace `yourusername` with actual ID).

4. **Deploy**.

### 3. Verify
1. Open your Vercel URL.
2. The "Network error" should be gone.
3. Login should work using the database you seeded on PythonAnywhere.

---

## 🔧 Troubleshooting

- **Error: Network Error / Failed to fetch**:
  - Check Vercel Console (F12).
  - Ensure `VITE_API_URL` is set correctly in Vercel (no trailing slash issues, usually `/api` is needed if your backend routes start with `/api`).
  - Ensure PythonAnywhere Web App is **Reloaded** and running (check Error Log on PythonAnywhere Dashboard).

- **Error: CORS**:
  - `backend/app.py` has `CORS(app, resources={r"/*": {"origins": "*"}})`. This should work.
  - If fails, verify you are hitting `https` (secure) and not `http`.

