-- ============================================
-- TRADESENSE AI - SAFE USER DELETION SQL
-- Version: 1.0
-- Execute in MySQL Workbench on 'tradesense' database
-- ============================================
-- 
-- IMPORTANT: This script MUST be run in a TRANSACTION
-- Review carefully before executing!
--
-- Users to delete (from screenshots):
-- IDs: 28-37, 50-53, 55-60
-- (ID 54 = superadmin is EXCLUDED)
--
-- ============================================

-- ============================================
-- STEP 0: ENABLE TRANSACTION
-- ============================================
SET autocommit = 0;
START TRANSACTION;

-- ============================================
-- STEP 1: CREATE TEMPORARY TABLE WITH USER IDS TO DELETE
-- ============================================

DROP TEMPORARY TABLE IF EXISTS users_to_delete;
CREATE TEMPORARY TABLE users_to_delete (user_id INT PRIMARY KEY);

-- Insert user IDs from screenshot 1 (IDs 50-60, excluding 54 superadmin)
INSERT INTO users_to_delete (user_id)
SELECT id FROM users 
WHERE email IN (
    'sarahfx@tradesense.ai',
    'tokyodrift@tradesense.ai',
    'euroking@tradesense.ai',
    'dubaiwhale@tradesense.ai',
    -- 'superadmin@tradesense.ma',  -- EXCLUDED: SUPERADMIN
    'lucas.martin@gmail.com',
    'sophia.nguyen@example.com',
    'mohammed.ela@example.com',
    'emily.zhang@example.com',
    'alibensaid@example.com',
    'oliver.garcia@example.com'
)
OR username IN (
    'SarahFX', 'TokyoDrift', 'EuroKing', 'DubaiWhale',
    'lucasm', 'sophian', 'mohamedel', 'emilyz', 'alibs', 'oliverg'
);

-- Insert user IDs from screenshot 2 (IDs 28-37)
INSERT IGNORE INTO users_to_delete (user_id)
SELECT id FROM users 
WHERE email IN (
    'alex_pro@trade.com',
    'sarah_x@trade.com',
    'mike_m@trade.com',
    'emma_e@trade.com',
    'david_d@trade.com',
    'lucas_l@trade.com',
    'julia_j@trade.com',
    'tom_t@trade.com',
    'ryan_r@trade.com',
    'nina_n@trade.com'
)
OR username IN (
    'alex_pro', 'sarah_x', 'mike_m', 'emma_e', 'david_d',
    'lucas_l', 'julia_j', 'tom_t', 'ryan_r', 'nina_n'
);

-- Verify users found
SELECT 'Users to delete:' AS info, COUNT(*) AS count FROM users_to_delete;
SELECT u.id, u.full_name, u.email, u.role 
FROM users u 
JOIN users_to_delete utd ON u.id = utd.user_id
ORDER BY u.id;

-- ============================================
-- STEP 2: GET ACCOUNT IDS FOR THESE USERS
-- ============================================

DROP TEMPORARY TABLE IF EXISTS accounts_to_delete;
CREATE TEMPORARY TABLE accounts_to_delete (account_id INT PRIMARY KEY);

INSERT INTO accounts_to_delete (account_id)
SELECT id FROM accounts WHERE user_id IN (SELECT user_id FROM users_to_delete);

SELECT 'Accounts to delete:' AS info, COUNT(*) AS count FROM accounts_to_delete;

-- ============================================
-- STEP 3: BACKUP TABLES (Optional - Create backup tables)
-- ============================================

-- Backup users
CREATE TABLE IF NOT EXISTS _backup_deleted_users AS
SELECT * FROM users WHERE id IN (SELECT user_id FROM users_to_delete);

-- Backup accounts
CREATE TABLE IF NOT EXISTS _backup_deleted_accounts AS
SELECT * FROM accounts WHERE id IN (SELECT account_id FROM accounts_to_delete);

-- Backup trades
CREATE TABLE IF NOT EXISTS _backup_deleted_trades AS
SELECT * FROM trades WHERE account_id IN (SELECT account_id FROM accounts_to_delete);

SELECT 'Backup tables created' AS info;

-- ============================================
-- STEP 4: DELETE IN CORRECT ORDER (Children first)
-- ============================================

-- 4.1: Delete trades
DELETE FROM trades 
WHERE account_id IN (SELECT account_id FROM accounts_to_delete);
SELECT ROW_COUNT() AS trades_deleted;

-- 4.2: Delete performance_snapshots
DELETE FROM performance_snapshots 
WHERE account_id IN (SELECT account_id FROM accounts_to_delete);
SELECT ROW_COUNT() AS performance_snapshots_deleted;

-- 4.3: Delete admin_actions_log (admin_id OR target_account_id)
DELETE FROM admin_actions_log 
WHERE admin_id IN (SELECT user_id FROM users_to_delete)
   OR target_account_id IN (SELECT account_id FROM accounts_to_delete);
SELECT ROW_COUNT() AS admin_logs_deleted;

-- 4.4: Delete transactions
DELETE FROM transactions 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS transactions_deleted;

-- 4.5: Delete leaderboard
DELETE FROM leaderboard 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS leaderboard_deleted;

-- 4.6: Delete post_likes
DELETE FROM post_likes 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS post_likes_deleted;

-- 4.7: Delete comments
DELETE FROM comments 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS comments_deleted;

-- 4.8: Delete posts
DELETE FROM posts 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS posts_deleted;

-- 4.9: Delete floor_messages
DELETE FROM floor_messages 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS floor_messages_deleted;

-- 4.10: Delete user_course_progress
DELETE FROM user_course_progress 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_course_progress_deleted;

-- 4.11: Delete user_lesson_progress
DELETE FROM user_lesson_progress 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_lesson_progress_deleted;

-- 4.12: Delete user_quiz_attempts
DELETE FROM user_quiz_attempts 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_quiz_attempts_deleted;

-- 4.13: Delete user_badges
DELETE FROM user_badges 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_badges_deleted;

-- 4.14: Delete user_xp
DELETE FROM user_xp 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_xp_deleted;

-- 4.15: Delete risk_alerts
DELETE FROM risk_alerts 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS risk_alerts_deleted;

-- 4.16: Delete challenges
DELETE FROM challenges 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS challenges_deleted;

-- 4.17: Delete user_challenges
DELETE FROM user_challenges 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_challenges_deleted;

-- 4.18: Delete user_preferences
DELETE FROM user_preferences 
WHERE user_id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS user_preferences_deleted;

-- 4.19: Delete accounts (PARENT of trades, etc.)
DELETE FROM accounts 
WHERE id IN (SELECT account_id FROM accounts_to_delete);
SELECT ROW_COUNT() AS accounts_deleted;

-- 4.20: DELETE USERS (MAIN PARENT - LAST!)
DELETE FROM users 
WHERE id IN (SELECT user_id FROM users_to_delete);
SELECT ROW_COUNT() AS users_deleted;

-- ============================================
-- STEP 5: VERIFICATION QUERIES
-- ============================================

SELECT '=== VERIFICATION ===' AS status;

-- Should return 0
SELECT 'Remaining users to delete:' AS check_name, 
       COUNT(*) AS should_be_zero 
FROM users 
WHERE email IN (
    'sarahfx@tradesense.ai', 'tokyodrift@tradesense.ai', 'euroking@tradesense.ai',
    'dubaiwhale@tradesense.ai', 'lucas.martin@gmail.com', 'sophia.nguyen@example.com',
    'mohammed.ela@example.com', 'emily.zhang@example.com', 'alibensaid@example.com',
    'oliver.garcia@example.com', 'alex_pro@trade.com', 'sarah_x@trade.com',
    'mike_m@trade.com', 'emma_e@trade.com', 'david_d@trade.com', 'lucas_l@trade.com',
    'julia_j@trade.com', 'tom_t@trade.com', 'ryan_r@trade.com', 'nina_n@trade.com'
);

-- Check for orphan trades (should be 0)
SELECT 'Orphan trades:' AS check_name,
       COUNT(*) AS should_be_zero
FROM trades t 
LEFT JOIN accounts a ON t.account_id = a.id 
WHERE a.id IS NULL;

-- Check for orphan leaderboard entries
SELECT 'Orphan leaderboard:' AS check_name,
       COUNT(*) AS should_be_zero
FROM leaderboard l 
LEFT JOIN users u ON l.user_id = u.id 
WHERE l.user_id IS NOT NULL AND u.id IS NULL;

-- ============================================
-- STEP 6: COMMIT OR ROLLBACK
-- ============================================

-- If everything looks good, COMMIT:
-- COMMIT;

-- If something went wrong, ROLLBACK:
-- ROLLBACK;

-- ============================================
-- FINAL SUMMARY
-- ============================================
SELECT 'Deletion Summary' AS status;
SELECT 
    (SELECT COUNT(*) FROM users) AS remaining_users,
    (SELECT COUNT(*) FROM accounts) AS remaining_accounts,
    (SELECT COUNT(*) FROM trades) AS remaining_trades,
    (SELECT COUNT(*) FROM leaderboard) AS remaining_leaderboard,
    (SELECT COUNT(*) FROM admin_actions_log) AS remaining_admin_logs;

-- Don't forget to execute one of these:
-- COMMIT;   -- To save changes
-- ROLLBACK; -- To cancel changes
