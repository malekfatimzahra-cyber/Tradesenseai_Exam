-- ============================================
-- TRADESENSE AI - DATA VERIFICATION QUERIES
-- Run these queries to verify data consistency
-- ============================================

-- ============================================
-- 1. USERS WITHOUT ACCOUNTS
-- Expected: 0 rows (except admins)
-- ============================================
SELECT 
    u.id AS user_id,
    u.full_name,
    u.email,
    u.role,
    'NO ACCOUNT' AS issue
FROM users u 
LEFT JOIN accounts a ON a.user_id = u.id 
WHERE a.id IS NULL 
  AND u.role = 'USER';

-- ============================================
-- 2. ACCOUNTS WITHOUT TRADES
-- Expected: 0 rows (all accounts should have trades)
-- ============================================
SELECT 
    a.id AS account_id,
    u.full_name AS user_name,
    a.plan_name,
    a.status,
    a.equity,
    'NO TRADES' AS issue
FROM accounts a 
LEFT JOIN trades t ON t.account_id = a.id 
JOIN users u ON u.id = a.user_id
WHERE t.id IS NULL;

-- ============================================
-- 3. LEADERBOARD WITH INVALID FOREIGN KEYS
-- Expected: 0 rows
-- ============================================
SELECT 
    l.id AS leaderboard_id,
    l.username,
    l.user_id,
    l.account_id,
    CASE 
        WHEN u.id IS NULL THEN 'INVALID USER_ID'
        WHEN a.id IS NULL THEN 'INVALID ACCOUNT_ID'
    END AS issue
FROM leaderboard l
LEFT JOIN users u ON u.id = l.user_id
LEFT JOIN accounts a ON a.id = l.account_id
WHERE (l.user_id IS NOT NULL AND u.id IS NULL)
   OR (l.account_id IS NOT NULL AND a.id IS NULL);

-- ============================================
-- 4. ACCOUNTS WITH STATUS CHANGES BUT NO ADMIN LOG
-- Expected: 0 rows (all PASSED/FAILED/FUNDED should have logs)
-- ============================================
SELECT 
    a.id AS account_id,
    u.full_name AS user_name,
    a.status,
    a.plan_name,
    'NO ADMIN LOG' AS issue
FROM accounts a
JOIN users u ON u.id = a.user_id
LEFT JOIN admin_actions_log log ON log.target_account_id = a.id
WHERE a.status IN ('PASSED', 'FAILED', 'FUNDED') 
  AND log.id IS NULL;

-- ============================================
-- 5. ORPHAN TRADES (without valid account)
-- Expected: 0 rows
-- ============================================
SELECT 
    t.id AS trade_id,
    t.account_id,
    t.symbol,
    t.pnl,
    'ORPHAN TRADE' AS issue
FROM trades t
LEFT JOIN accounts a ON a.id = t.account_id
WHERE a.id IS NULL;

-- ============================================
-- 6. ADMIN ACTIONS LOG SUMMARY
-- Shows all logged actions
-- ============================================
SELECT 
    log.id,
    u.full_name AS admin_name,
    CONCAT('Account #', log.target_account_id, ' (', target_u.full_name, ')') AS target,
    log.action,
    LEFT(log.note, 50) AS note_preview,
    log.created_at
FROM admin_actions_log log
JOIN users u ON u.id = log.admin_id
LEFT JOIN accounts a ON a.id = log.target_account_id
LEFT JOIN users target_u ON target_u.id = a.user_id
ORDER BY log.created_at DESC
LIMIT 20;

-- ============================================
-- 7. DATABASE STATISTICS SUMMARY
-- ============================================
SELECT 'Users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'Accounts', COUNT(*) FROM accounts
UNION ALL
SELECT 'Trades', COUNT(*) FROM trades
UNION ALL
SELECT 'Leaderboard', COUNT(*) FROM leaderboard
UNION ALL
SELECT 'Admin Action Logs', COUNT(*) FROM admin_actions_log
UNION ALL
SELECT 'Performance Snapshots', COUNT(*) FROM performance_snapshots;

-- ============================================
-- 8. LEADERBOARD TOP 10 (Derived from Trades)
-- ============================================
SELECT 
    ROW_NUMBER() OVER (ORDER BY SUM(t.pnl) DESC) AS rank_calculated,
    u.full_name,
    u.username,
    a.plan_name,
    a.initial_balance,
    a.equity,
    ROUND(SUM(t.pnl), 2) AS total_pnl_from_trades,
    ROUND((SUM(t.pnl) / a.initial_balance) * 100, 2) AS roi_percent,
    COUNT(t.id) AS trade_count,
    ROUND(SUM(CASE WHEN t.pnl > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(t.id), 2) AS win_rate
FROM users u
JOIN accounts a ON a.user_id = u.id
JOIN trades t ON t.account_id = a.id AND t.status = 'CLOSED'
WHERE a.status IN ('ACTIVE', 'PASSED', 'FUNDED')
GROUP BY u.id, a.id
HAVING SUM(t.pnl) > 0
ORDER BY total_pnl_from_trades DESC
LIMIT 10;

-- ============================================
-- 9. ACCOUNT STATUS DISTRIBUTION
-- ============================================
SELECT 
    status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM accounts), 2) AS percentage
FROM accounts
GROUP BY status
ORDER BY count DESC;

-- ============================================
-- 10. TRADES PER ACCOUNT DISTRIBUTION
-- ============================================
SELECT 
    a.id AS account_id,
    u.full_name,
    a.plan_name,
    COUNT(t.id) AS trades_count,
    ROUND(SUM(t.pnl), 2) AS total_pnl,
    a.equity - a.initial_balance AS account_pnl_diff
FROM accounts a
JOIN users u ON u.id = a.user_id
LEFT JOIN trades t ON t.account_id = a.id
GROUP BY a.id
ORDER BY trades_count DESC;
