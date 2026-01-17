-- ============================================
-- TRADESENSE AI - DATA CONSISTENCY MIGRATION
-- Version: 1.0 - Full Data Integrity Fix
-- Execute in MySQL Workbench on 'tradesense' database
-- ============================================

-- 1. ENSURE FOREIGN KEY CONSTRAINTS ARE PROPERLY SET
-- Add indexes for performance

-- Index on accounts.user_id
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);

-- Index on trades.account_id  
CREATE INDEX IF NOT EXISTS idx_trades_account_id ON trades(account_id);

-- Index on trades.user_id
CREATE INDEX IF NOT EXISTS idx_trades_user_id ON trades(user_id);

-- Index on leaderboard
CREATE INDEX IF NOT EXISTS idx_leaderboard_user_id ON leaderboard(user_id);
CREATE INDEX IF NOT EXISTS idx_leaderboard_account_id ON leaderboard(account_id);

-- Index on admin_actions_log
CREATE INDEX IF NOT EXISTS idx_admin_log_admin_id ON admin_actions_log(admin_id);
CREATE INDEX IF NOT EXISTS idx_admin_log_target ON admin_actions_log(target_account_id);

-- 2. ENSURE trades table has required columns
ALTER TABLE trades ADD COLUMN IF NOT EXISTS user_id INT NULL;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS quantity FLOAT NULL;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS price FLOAT NULL;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS side VARCHAR(10) NULL;
ALTER TABLE trades ADD COLUMN IF NOT EXISTS timestamp DATETIME DEFAULT CURRENT_TIMESTAMP;

-- 3. Add FK constraint to trades.user_id if not exists
-- Note: Running this might fail if orphan records exist - we'll clean them in step 4
-- ALTER TABLE trades ADD CONSTRAINT fk_trades_user FOREIGN KEY (user_id) REFERENCES users(id);

-- 4. CLEANUP: Remove orphan records (trades without valid account)
-- First, let's backup potential orphans
CREATE TABLE IF NOT EXISTS _orphan_trades_backup AS
SELECT * FROM trades WHERE account_id NOT IN (SELECT id FROM accounts);

-- Delete orphans
DELETE FROM trades WHERE account_id NOT IN (SELECT id FROM accounts);

-- 5. Update trades.user_id from their parent account
UPDATE trades t
JOIN accounts a ON t.account_id = a.id
SET t.user_id = a.user_id
WHERE t.user_id IS NULL OR t.user_id = 0;

-- ============================================
-- VERIFICATION QUERIES
-- Run these to check data consistency
-- ============================================

-- Query 1: Users without accounts
-- SELECT u.id, u.email FROM users u 
-- LEFT JOIN accounts a ON a.user_id = u.id 
-- WHERE a.id IS NULL;

-- Query 2: Accounts without trades
-- SELECT a.id, a.plan_name FROM accounts a 
-- LEFT JOIN trades t ON t.account_id = a.id 
-- WHERE t.id IS NULL;

-- Query 3: Leaderboard entries with invalid FK
-- SELECT l.id FROM leaderboard l
-- LEFT JOIN users u ON u.id = l.user_id
-- LEFT JOIN accounts a ON a.id = l.account_id
-- WHERE (l.user_id IS NOT NULL AND u.id IS NULL) 
--    OR (l.account_id IS NOT NULL AND a.id IS NULL);

-- Query 4: Accounts without admin logs (for PASSED/FAILED status)
-- SELECT a.id, a.status FROM accounts a
-- LEFT JOIN admin_actions_log log ON log.target_account_id = a.id
-- WHERE a.status IN ('PASSED', 'FAILED', 'FUNDED') AND log.id IS NULL;
