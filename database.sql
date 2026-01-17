-- TradeSense AI Prop Firm Database Schema (SQLite/PostgreSQL)

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'USER',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Accounts Table (Module A: Challenge Engine)
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_name VARCHAR(50) DEFAULT 'Starter',
    initial_balance FLOAT DEFAULT 5000.0,
    current_balance FLOAT DEFAULT 5000.0,
    equity FLOAT DEFAULT 5000.0,
    daily_starting_equity FLOAT DEFAULT 5000.0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Trades Table (Module C: Trading Execution)
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    trade_type VARCHAR(10) NOT NULL, -- BUY/SELL
    amount FLOAT NOT NULL,
    entry_price FLOAT NOT NULL,
    exit_price FLOAT,
    stop_loss FLOAT,
    take_profit FLOAT,
    commission FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'OPEN', -- OPEN/CLOSED
    pnl FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Transactions Table (Module B: Payments)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(20) NOT NULL, -- PAYPAL/CMI/CRYPTO
    status VARCHAR(20) DEFAULT 'PENDING',
    transaction_id VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- System Config (Bonus: Admin Config)
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(50) PRIMARY KEY,
    value TEXT
);

-- Academy Models
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    level VARCHAR(50) NOT NULL,
    thumbnail_url VARCHAR(255),
    duration_minutes INTEGER DEFAULT 60,
    xp_reward INTEGER DEFAULT 100,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    "order" INTEGER DEFAULT 1,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    lesson_type VARCHAR(20) DEFAULT 'TEXT',
    content TEXT,
    "order" INTEGER DEFAULT 1,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);

-- Community Models
CREATE TABLE IF NOT EXISTS trading_floors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    floor_type VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    icon_name VARCHAR(50) DEFAULT 'fa-hashtag',
    required_level VARCHAR(50) DEFAULT 'Bronze Trader'
);

CREATE TABLE IF NOT EXISTS floor_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floor_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    message_type VARCHAR(20) DEFAULT 'TEXT',
    content TEXT NOT NULL,
    metadata_json TEXT,
    likes_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (floor_id) REFERENCES trading_floors(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
