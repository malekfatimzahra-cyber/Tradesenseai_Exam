# Migration Guide: SQLite → MySQL

This guide helps you migrate your existing TradeSense backend from SQLite to MySQL.

## 📋 Overview

**Current Setup:** SQLite (`instance/tradesense.db`)  
**Target Setup:** MySQL (`localhost:3306/tradesense`)

---

## 🔄 Migration Steps

### Step 1: Backup Existing Data (SQLite)

```bash
# Backup your SQLite database
cd backend
cp instance/tradesense.db instance/tradesense.db.backup
```

### Step 2: Export Data (Optional - if you have existing data)

```python
# export_data.py
from app import app, db
from models import User, Account, Trade
import json

with app.app_context():
    users = User.query.all()
    accounts = Account.query.all()
    trades = Trade.query.all()
    
    data = {
        'users': [u.to_dict() for u in users],
        'accounts': [a.to_dict() for a in accounts],
        'trades': [t.to_dict() for t in trades]
    }
    
    with open('backup_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Exported {len(users)} users, {len(accounts)} accounts, {len(trades)} trades")
```

### Step 3: Install MySQL Dependencies

```bash
pip install pymysql cryptography
```

### Step 4: Create MySQL Database

```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE tradesense CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify
SHOW DATABASES;
USE tradesense;
```

### Step 5: Configure Environment

**Option A: Use setup script**
```bash
python setup.py
```

**Option B: Manual configuration**
```bash
# Create .env file
cp .env.example .env

# Edit .env and set:
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tradesense
```

### Step 6: Update Application Files

The new files are already created:
- ✅ `config.py` - MySQL configuration
- ✅ `__init__.py` - Application factory
- ✅ `run.py` - New entry point

### Step 7: Initialize MySQL Tables

```bash
python run.py
```

The application will automatically:
1. Connect to MySQL
2. Create all tables
3. Seed initial users (development mode)

### Step 8: Verify Connection

```bash
# Test database connection
curl http://localhost:5000/api/test-db

# Expected response:
# {
#   "status": "success",
#   "message": "Database Connected!",
#   "database": "localhost:3306/tradesense"
# }
```

### Step 9: Import Data (Optional)

If you exported data in Step 2:

```python
# import_data.py
from __init__ import create_app
from models import db, User, Account, Trade, UserRole, ChallengeStatus, TradeType, TradeStatus
import json

app = create_app()

with app.app_context():
    with open('backup_data.json', 'r') as f:
        data = json.load(f)
    
    # Import users
    for user_data in data['users']:
        user = User(
            id=user_data['id'],
            full_name=user_data['full_name'],
            email=user_data['email'],
            role=UserRole[user_data['role']]
        )
        # Note: password_hash needs to be set separately
        db.session.add(user)
    
    db.session.commit()
    print(f"Imported {len(data['users'])} users")
    
    # Import accounts and trades similarly...
```

---

## 🔍 Verification Checklist

- [ ] MySQL server is running
- [ ] Database 'tradesense' exists
- [ ] `.env` file is configured with correct password
- [ ] Dependencies installed (`pymysql`, `cryptography`)
- [ ] `/api/test-db` returns success
- [ ] Can register new user
- [ ] Can login and get JWT token
- [ ] Can create account
- [ ] Can place trade

---

## 📊 Key Differences: SQLite vs MySQL

| Feature | SQLite | MySQL |
|---------|--------|-------|
| **Connection** | File-based | Network-based |
| **URI Format** | `sqlite:///path/to/db` | `mysql+pymysql://user:pass@host/db` |
| **Concurrent Writes** | Limited | Excellent |
| **Production Ready** | No | Yes |
| **Setup Complexity** | Simple | Moderate |
| **Performance** | Good for small apps | Excellent for large apps |

---

## 🔧 Configuration Changes

### Old Configuration (SQLite)
```python
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
```

### New Configuration (MySQL)
```python
# config.py
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)
```

---

## 🚀 Running the New Setup

### Development
```bash
python run.py
# or
FLASK_ENV=development python run.py
```

### Production
```bash
FLASK_ENV=production python run.py
# or with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

---

## 🐛 Common Migration Issues

### Issue: "Access denied for user 'root'"
**Solution:** Check password in `.env` file
```bash
# Test MySQL connection manually
mysql -u root -p
```

### Issue: "Unknown database 'tradesense'"
**Solution:** Create the database
```sql
CREATE DATABASE tradesense CHARACTER SET utf8mb4;
```

### Issue: "No module named 'pymysql'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Table already exists"
**Solution:** Drop and recreate
```python
from __init__ import create_app
from models import db

app = create_app()
with app.app_context():
    db.drop_all()  # Warning: deletes all data!
    db.create_all()
```

### Issue: Old app.py still running
**Solution:** Use new entry point
```bash
# OLD (don't use)
python app.py

# NEW (use this)
python run.py
```

---

## 📁 File Changes Summary

### New Files Created
- `config.py` - Database configuration
- `__init__.py` - Application factory
- `run.py` - New entry point
- `setup.py` - Interactive setup
- `.env.example` - Environment template
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick reference

### Modified Files
- `requirements.txt` - Added `pymysql` and `cryptography`

### Deprecated Files
- `app.py` - Old entry point (keep for reference, but use `run.py`)

---

## 🔄 Rollback Plan

If you need to rollback to SQLite:

1. **Stop the server**
2. **Restore old configuration**
   ```bash
   # Use old app.py
   python app.py
   ```
3. **Restore database backup**
   ```bash
   cp instance/tradesense.db.backup instance/tradesense.db
   ```

---

## ✅ Post-Migration Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### Test Database
```bash
# Health check
curl http://localhost:5000/api/health

# Database test
curl http://localhost:5000/api/test-db
```

### Test Trading
```bash
# Create account (requires JWT token)
curl -X POST http://localhost:5000/api/accounts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🎯 Next Steps

1. ✅ Complete migration
2. ✅ Verify all endpoints work
3. ✅ Test with frontend
4. 📝 Update frontend API base URL if needed
5. 🚀 Deploy to production

---

## 📞 Support

If you encounter issues:
1. Check `README.md` for detailed documentation
2. Review troubleshooting section above
3. Verify MySQL is running: `mysql -u root -p`
4. Test connection: `http://localhost:5000/api/test-db`

---

**Migration Complete! 🎉**

Your TradeSense backend is now running on MySQL with a production-ready architecture.
