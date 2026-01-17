-- Quick fix: Delete leaderboard entries for users that don't exist
-- Run this in MySQL Workbench

-- Check invalid entries
SELECT l.id, l.username, l.user_id, 
       (SELECT COUNT(*) FROM users u WHERE u.id = l.user_id) AS user_exists
FROM leaderboard l
WHERE l.username LIKE '%Atlas%';

-- Delete entries where user doesn't exist
DELETE l FROM leaderboard l
LEFT JOIN users u ON u.id = l.user_id
WHERE u.id IS NULL;

-- After delete, update rankings
SET @rank = 0;
UPDATE leaderboard
SET ranking = (@rank := @rank + 1)
WHERE period = 'ALL_TIME'
ORDER BY profit DESC;

-- Verify
SELECT ranking, username, profit, user_id FROM leaderboard 
WHERE period = 'ALL_TIME' 
ORDER BY ranking LIMIT 10;
