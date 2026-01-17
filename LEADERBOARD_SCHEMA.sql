-- LEADERBOARD SCHEMA FOR MySQL WORKBENCH

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('USER', 'ADMIN', 'SUPERADMIN') DEFAULT 'USER',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_name VARCHAR(50) DEFAULT 'Starter',
    initial_balance FLOAT DEFAULT 5000.0,
    current_balance FLOAT DEFAULT 5000.0,
    equity FLOAT DEFAULT 5000.0,
    daily_starting_equity FLOAT DEFAULT 5000.0,
    status ENUM('ACTIVE', 'PASSED', 'FAILED', 'PENDING', 'FUNDED') DEFAULT 'ACTIVE',
    reason VARCHAR(255),
    admin_note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_daily_reset DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE performance_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    period VARCHAR(20) DEFAULT 'ALL_TIME',
    date DATE,
    profit FLOAT DEFAULT 0.0,
    roi FLOAT DEFAULT 0.0,
    win_rate FLOAT DEFAULT 0.0,
    trades_count INT DEFAULT 0,
    equity FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_id INT,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(5) DEFAULT 'MA',
    avatar_url VARCHAR(255),
    profit FLOAT DEFAULT 0.0,
    roi FLOAT DEFAULT 0.0,
    win_rate FLOAT DEFAULT 0.0,
    funded_amount FLOAT DEFAULT 0.0,
    consistency_score FLOAT DEFAULT 0.0,
    risk_score FLOAT DEFAULT 0.0,
    ranking INT DEFAULT 0,
    period VARCHAR(20) DEFAULT 'ALL_TIME',
    badges TEXT, -- JSON List
    equity_curve TEXT, -- JSON List
    is_visible BOOLEAN DEFAULT TRUE,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE admin_actions_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    target_account_id INT,
    action VARCHAR(50) NOT NULL,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id),
    FOREIGN KEY (target_account_id) REFERENCES accounts(id)
);

-- INDEXES
CREATE INDEX idx_leaderboard_rank ON leaderboard(ranking);
CREATE INDEX idx_leaderboard_period ON leaderboard(period);
CREATE INDEX idx_snapshots_account ON performance_snapshots(account_id);
