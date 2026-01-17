
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    language VARCHAR(10) DEFAULT 'en',
    theme VARCHAR(20) DEFAULT 'dark',
    timezone VARCHAR(50) DEFAULT 'UTC',
    currency VARCHAR(10) DEFAULT 'USD',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    trading_alerts BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notification_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    price_alerts BOOLEAN DEFAULT TRUE,
    risk_alerts BOOLEAN DEFAULT TRUE,
    trade_confirmations BOOLEAN DEFAULT TRUE,
    daily_summary BOOLEAN DEFAULT FALSE,
    weekly_report BOOLEAN DEFAULT FALSE,
    marketing_emails BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    image_url TEXT,
    category VARCHAR(50) DEFAULT 'general',
    is_pinned BOOLEAN DEFAULT FALSE,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_posts_user ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_likes_post ON likes(post_id);

CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    category VARCHAR(50) DEFAULT 'market',
    impact VARCHAR(20) DEFAULT 'medium',
    source VARCHAR(100),
    author_id INTEGER,
    image_url TEXT,
    volatility_score FLOAT,
    assets_affected TEXT,
    is_published BOOLEAN DEFAULT TRUE,
    views_count INTEGER DEFAULT 0,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_news_published ON news_articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_category ON news_articles(category);

CREATE TABLE IF NOT EXISTS challenge_plans (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    capital INTEGER NOT NULL,
    profit_target INTEGER NOT NULL,
    max_drawdown INTEGER NOT NULL,
    daily_loss_limit INTEGER NOT NULL,
    price INTEGER NOT NULL,
    currency VARCHAR(10) DEFAULT 'MAD',
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT,
    features TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO challenge_plans (id, name, capital, profit_target, max_drawdown, daily_loss_limit, price)
VALUES 
('starter', 'Starter Challenge', 5000, 500, 500, 250, 200),
('pro', 'Professional Pro', 25000, 2500, 2500, 1250, 500),
('elite', 'Elite Institutional', 100000, 10000, 10000, 5000, 1000);

CREATE TABLE IF NOT EXISTS trading_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    starting_equity FLOAT NOT NULL,
    ending_equity FLOAT,
    trades_count INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    total_pnl FLOAT DEFAULT 0,
    max_drawdown FLOAT DEFAULT 0,
    largest_win FLOAT DEFAULT 0,
    largest_loss FLOAT DEFAULT 0,
    duration_minutes INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    total_trades INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    win_rate FLOAT DEFAULT 0,
    total_profit FLOAT DEFAULT 0,
    total_loss FLOAT DEFAULT 0,
    profit_factor FLOAT DEFAULT 0,
    sharpe_ratio FLOAT DEFAULT 0,
    max_consecutive_wins INTEGER DEFAULT 0,
    max_consecutive_losses INTEGER DEFAULT 0,
    average_win FLOAT DEFAULT 0,
    average_loss FLOAT DEFAULT 0,
    best_day FLOAT DEFAULT 0,
    worst_day FLOAT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admin_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    target_user_id INTEGER,
    target_entity VARCHAR(50),
    target_id INTEGER,
    details TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (target_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_admin_actions_admin ON admin_actions(admin_id);
CREATE INDEX IF NOT EXISTS idx_admin_actions_created ON admin_actions(created_at DESC);

CREATE VIEW IF NOT EXISTS leaderboard_view AS
SELECT 
    u.id AS user_id,
    u.full_name,
    u.username,
    u.avatar,
    u.role,
    a.id AS account_id,
    a.plan_name,
    a.initial_balance,
    a.equity,
    a.status,
    (a.equity - a.initial_balance) AS profit,
    ROUND((a.equity - a.initial_balance) * 100.0 / a.initial_balance, 2) AS roi_percentage,
    (SELECT COUNT(*) FROM trades t WHERE t.account_id = a.id AND t.status = 'CLOSED' AND t.pnl > 0) AS winning_trades,
    (SELECT COUNT(*) FROM trades t WHERE t.account_id = a.id AND t.status = 'CLOSED') AS total_trades,
    a.created_at AS challenge_started
FROM users u
INNER JOIN accounts a ON u.id = a.user_id
WHERE a.status IN ('ACTIVE', 'PASSED')
ORDER BY profit DESC;

CREATE TRIGGER IF NOT EXISTS increment_post_likes
AFTER INSERT ON likes
BEGIN
    UPDATE posts 
    SET likes_count = likes_count + 1 
    WHERE id = NEW.post_id;
END;

CREATE TRIGGER IF NOT EXISTS decrement_post_likes
AFTER DELETE ON likes
BEGIN
    UPDATE posts 
    SET likes_count = likes_count - 1 
    WHERE id = OLD.post_id;
END;

CREATE TRIGGER IF NOT EXISTS increment_post_comments
AFTER INSERT ON comments
BEGIN
    UPDATE posts 
    SET comments_count = comments_count + 1 
    WHERE id = NEW.post_id;
END;

CREATE TRIGGER IF NOT EXISTS decrement_post_comments
AFTER DELETE ON comments
BEGIN
    UPDATE posts 
    SET comments_count = comments_count - 1 
    WHERE id = OLD.post_id;
END;

INSERT OR IGNORE INTO user_preferences (user_id)
SELECT id FROM users WHERE id NOT IN (SELECT user_id FROM user_preferences);

INSERT OR IGNORE INTO notification_settings (user_id)
SELECT id FROM users WHERE id NOT IN (SELECT user_id FROM notification_settings);
