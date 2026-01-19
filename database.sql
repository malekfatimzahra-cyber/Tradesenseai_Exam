-- TradeSense AI Database Export
-- Generated: 2026-01-19 20:27:20.532320
-- ------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

-- Table structure for table `accounts`
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `plan_name` varchar(50) DEFAULT NULL,
  `initial_balance` float DEFAULT NULL,
  `current_balance` float DEFAULT NULL,
  `equity` float DEFAULT NULL,
  `daily_starting_equity` float DEFAULT NULL,
  `status` enum('ACTIVE','PASSED','FAILED','PENDING','FUNDED') DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `admin_note` text,
  `created_at` datetime DEFAULT NULL,
  `last_daily_reset` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `accounts`
INSERT INTO `accounts` VALUES 
(1, 3, 'Starter', 5000.0, 5000.0, 5000.0, 5000.0, 'PENDING', NULL, NULL, '2026-01-19 00:04:08', '2026-01-18'),
(2, 7, 'Pro', 5000.0, 5632.88, 5632.88, 5000.0, 'ACTIVE', NULL, NULL, '2026-01-19 09:55:01', '2026-01-19'),
(3, 8, 'Starter', 100000.0, 114452.0, 114452.0, 100000.0, 'ACTIVE', NULL, NULL, '2026-01-19 09:55:02', '2026-01-19'),
(4, 9, 'Starter', 100000.0, 101400.0, 101400.0, 100000.0, 'ACTIVE', NULL, NULL, '2026-01-19 09:55:02', '2026-01-19'),
(5, 10, 'Elite', 5000.0, 4870.85, 4870.85, 5000.0, 'ACTIVE', NULL, NULL, '2026-01-19 09:55:03', '2026-01-19'),
(6, 11, 'Elite Institutional', 100000.0, 130555.0, 130555.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:13', '2026-01-19'),
(7, 12, 'Elite Institutional', 100000.0, 142625.0, 142625.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:16', '2026-01-19'),
(8, 13, 'Elite Institutional', 100000.0, 136424.0, 136424.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:18', '2026-01-19'),
(9, 14, 'Elite Institutional', 100000.0, 168359.0, 168359.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:20', '2026-01-19'),
(10, 15, 'Elite Institutional', 100000.0, 120322.0, 120322.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:22', '2026-01-19'),
(11, 16, 'Elite Institutional', 100000.0, 150924.0, 150924.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:23', '2026-01-19'),
(12, 17, 'Elite Institutional', 100000.0, 120693.0, 120693.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:25', '2026-01-19'),
(13, 18, 'Elite Institutional', 100000.0, 155360.0, 155360.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:26', '2026-01-19'),
(14, 19, 'Elite Institutional', 100000.0, 171836.0, 171836.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:28', '2026-01-19'),
(15, 20, 'Elite Institutional', 100000.0, 176883.0, 176883.0, 100000.0, 'PASSED', 'Passed via manual evaluation (Exam Demo)', NULL, '2026-01-19 09:55:30', '2026-01-19'),
(16, 21, 'Starter', 5000.0, 5000.0, 5000.0, 5000.0, 'PENDING', NULL, NULL, '2026-01-19 11:14:47', '2026-01-19'),
(17, 21, 'Elite Institutional', 100000.0, 100000.0, 100000.0, 100000.0, 'ACTIVE', 'Challenge Activated', 'Payment via CRYPTO', '2026-01-19 11:16:01', '2026-01-19'),
(18, 1, 'Elite Institutional', 100000.0, 100000.0, 100000.0, 100000.0, 'ACTIVE', 'Challenge Activated', 'Payment via CMI', '2026-01-19 11:24:56', '2026-01-19'),
(19, 22, 'Starter', 5000.0, 5000.0, 5000.0, 5000.0, 'PENDING', NULL, NULL, '2026-01-19 12:08:39', '2026-01-19'),
(20, 23, 'Starter', 5000.0, 5000.0, 5000.0, 5000.0, 'PENDING', NULL, NULL, '2026-01-19 12:09:43', '2026-01-19'),
(21, 23, 'Starter Challenge', 5000.0, 5000.0, 5000.0, 5000.0, 'ACTIVE', 'Challenge Activated', 'Payment via CMI', '2026-01-19 12:10:00', '2026-01-19');
-- Table structure for table `admin_actions_log`
DROP TABLE IF EXISTS `admin_actions_log`;
CREATE TABLE `admin_actions_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `target_account_id` int DEFAULT NULL,
  `action` varchar(50) NOT NULL,
  `note` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `target_account_id` (`target_account_id`),
  CONSTRAINT `admin_actions_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`),
  CONSTRAINT `admin_actions_log_ibfk_2` FOREIGN KEY (`target_account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `admin_actions_log`
-- Table structure for table `badges`
DROP TABLE IF EXISTS `badges`;
CREATE TABLE `badges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `icon_name` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `xp_bonus` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `badges`
-- Table structure for table `challenge_plans`
DROP TABLE IF EXISTS `challenge_plans`;
CREATE TABLE `challenge_plans` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `capital` int NOT NULL,
  `profit_target` int NOT NULL,
  `max_drawdown` int NOT NULL,
  `daily_loss_limit` int NOT NULL,
  `price` int NOT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `description` text,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `challenge_plans`
INSERT INTO `challenge_plans` VALUES 
('elite', 'Elite Institutional', 100000, 10000, 10000, 5000, 1000, 'MAD', NULL, 1),
('pro', 'Professional Pro', 25000, 2500, 2500, 1250, 500, 'MAD', NULL, 1),
('starter', 'Starter Challenge', 5000, 500, 500, 250, 200, 'MAD', NULL, 1);
-- Table structure for table `challenges`
DROP TABLE IF EXISTS `challenges`;
CREATE TABLE `challenges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `target_amount` float NOT NULL,
  `current_equity` float DEFAULT NULL,
  `status` enum('ACTIVE','PASSED','FAILED','PENDING','FUNDED') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `challenges_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `challenges`
-- Table structure for table `comments`
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `comments`
-- Table structure for table `course_translations`
DROP TABLE IF EXISTS `course_translations`;
CREATE TABLE `course_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_course_lang` (`course_id`,`lang`),
  CONSTRAINT `course_translations_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `course_translations`
-- Table structure for table `courses`
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `lang` varchar(10) DEFAULT NULL,
  `description` text,
  `category` enum('TECHNICAL','PSYCHOLOGY','RISK','QUANT','PLATFORM') NOT NULL,
  `level` enum('BEGINNER','INTERMEDIATE','ADVANCED','EXPERT') NOT NULL,
  `thumbnail_url` varchar(255) DEFAULT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `duration_minutes` int DEFAULT NULL,
  `xp_reward` int DEFAULT NULL,
  `is_premium` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `courses`
INSERT INTO `courses` VALUES 
(11, 'Introduction au Trading (FR)', 'fr', 'Le guide ultime pour débuter sur les marchés financiers. Apprenez tout de A à Z : vocabulaire, analyse, psychologie et gestion du risque.', 'TECHNICAL', 'BEGINNER', 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80', NULL, 300, 2500, 0, '2026-01-19 18:05:23'),
(12, 'Trading Fundamentals & Market Mechanics', 'en', 'Master the absolute basics: Pips, Spreads, Lots, and Order Types. Build your foundation here.', 'TECHNICAL', 'BEGINNER', 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&q=80', NULL, 180, 1500, 0, '2026-01-19 18:05:24'),
(13, 'Introduction to Price Action', 'en', 'Read the market without complex indicators. Pure Price Action.', 'TECHNICAL', 'INTERMEDIATE', 'https://images.unsplash.com/photo-1642790551116-18e150f248e5?w=800&q=80', NULL, 240, 2000, 0, '2026-01-19 18:05:24'),
(14, 'Smart Money Concepts (SMC / ICT)', 'en', 'Learn about Liquidity, Order Blocks, Fair Value Gaps, and Market Structure.', 'TECHNICAL', 'EXPERT', 'https://images.unsplash.com/photo-1612178991541-b48cc8e92a4d?w=800&q=80', NULL, 360, 3500, 0, '2026-01-19 18:05:25'),
(15, 'Trading Psychology Under Pressure', 'en', 'Conquer your mind. Master FOMO, Revenge trading, and Discipline without a Routine.', 'PSYCHOLOGY', 'INTERMEDIATE', 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80', NULL, 200, 1800, 0, '2026-01-19 18:05:26'),
(16, 'Basic Risk Management for Traders', 'en', 'Survival comes first. Learn position sizing, R:R Multiples, and how to keep your account.', 'RISK', 'BEGINNER', 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80', NULL, 150, 1200, 0, '2026-01-19 18:05:26'),
(17, 'Market Structure & Trend Logic', 'en', 'Map the market properly. Identify BOS, Higher Highs, and major imbalance reversals.', 'TECHNICAL', 'INTERMEDIATE', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80', NULL, 220, 2200, 0, '2026-01-19 18:05:27'),
(18, 'Supply & Demand Trading', 'en', 'Find key levels where institutions buy and sell. Master the imbalance strategy.', 'TECHNICAL', 'INTERMEDIATE', 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80', NULL, 210, 1900, 0, '2026-01-19 18:05:27');
-- Table structure for table `floor_messages`
DROP TABLE IF EXISTS `floor_messages`;
CREATE TABLE `floor_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `floor_id` int NOT NULL,
  `user_id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `message_type` enum('TEXT','TRADE_IDEA','ALERT','REVIEW') DEFAULT NULL,
  `content` text NOT NULL,
  `metadata_json` text,
  `image_url` varchar(255) DEFAULT NULL,
  `asset` varchar(20) DEFAULT NULL,
  `likes_count` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `floor_id` (`floor_id`),
  KEY `user_id` (`user_id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `floor_messages_ibfk_1` FOREIGN KEY (`floor_id`) REFERENCES `trading_floors` (`id`),
  CONSTRAINT `floor_messages_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `floor_messages_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `floor_messages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `floor_messages`
-- Table structure for table `leaderboard`
DROP TABLE IF EXISTS `leaderboard`;
CREATE TABLE `leaderboard` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `account_id` int DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `profit` float DEFAULT NULL,
  `roi` float DEFAULT NULL,
  `win_rate` float DEFAULT NULL,
  `funded_amount` float DEFAULT NULL,
  `consistency_score` float DEFAULT NULL,
  `risk_score` float DEFAULT NULL,
  `ranking` int DEFAULT NULL,
  `period` varchar(20) DEFAULT NULL,
  `badges` text,
  `equity_curve` text,
  `is_visible` tinyint(1) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `leaderboard_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `leaderboard_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `leaderboard`
INSERT INTO `leaderboard` VALUES 
(1, 11, 6, 'Amine Benali', 'MA', NULL, 30555.2, 30.5552, 85.8573, 100000.0, 96.6097, 91.5344, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 106152.30800516673, 115716.25801739133, 124988.78565964605, 131090.94860711688, 132026.83002691556, 139336.58161311704, 147307.62184934056, 155727.95553516079, 158375.3014047103, 164528.59113928987, 130555.20874887999]', 1, '2026-01-19 09:55:14'),
(2, 12, 7, 'Fatima Zahra El Idrissi', 'MA', NULL, 42625.2, 42.6252, 76.5273, 100000.0, 86.1233, 96.8166, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 109739.51581147454, 116129.6734343191, 119554.59261549685, 124122.9615173526, 126045.24046002117, 129999.27803332682, 136717.05621484725, 143322.22578283705, 145217.91431184448, 143940.12939860846, 142625.19655061344]', 1, '2026-01-19 09:55:16'),
(3, 13, 8, 'Youssef Alami', 'MA', NULL, 36424.2, 36.4242, 67.7673, 100000.0, 93.6496, 94.8428, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 103507.41230900341, 103673.06753935012, 113119.56132101051, 117138.60226407704, 117495.88762254312, 122639.72515477682, 126087.34907160164, 130614.33041163917, 131301.59343946548, 131899.03201194567, 136424.19055759406]', 1, '2026-01-19 09:55:19'),
(4, 14, 9, 'Siham Mansouri', 'MA', NULL, 68358.8, 68.3588, 81.2712, 100000.0, 97.3014, 97.098, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 100267.22834060254, 105266.60115411358, 106520.87909988932, 109707.14423097091, 118600.445163141, 125354.92863549796, 127291.41726214293, 125580.90958396185, 131158.02068615903, 135129.23392674545, 168358.81125283544]', 1, '2026-01-19 09:55:20'),
(5, 15, 10, 'Omar Bennani', 'MA', NULL, 20322.3, 20.3223, 84.6277, 100000.0, 85.9906, 96.1624, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 101517.03252229618, 100094.58754579912, 102504.947617913, 102406.85628030176, 102817.61676108137, 110938.83255134616, 115295.85143071898, 123047.32747458789, 126448.59530254448, 130582.32381889483, 120322.34993700305]', 1, '2026-01-19 09:55:22'),
(6, 16, 11, 'Laila Tazi', 'MA', NULL, 50923.9, 50.9239, 72.5543, 100000.0, 94.6016, 91.2836, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 109329.92070728923, 118301.67254232749, 121475.2857842476, 127465.21403721427, 130242.17829190388, 132389.11128670516, 131145.829962902, 131284.84207332935, 139194.76842163966, 148499.04482366244, 150923.9163264755]', 1, '2026-01-19 09:55:24'),
(7, 17, 12, 'Mehdi Chraibi', 'MA', NULL, 20693.3, 20.6933, 69.5919, 100000.0, 92.5683, 94.4136, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 99722.25232975754, 102906.1929638651, 107768.51128421891, 107754.02729587434, 109729.45238792282, 110870.35631025932, 110065.61380068287, 114703.67023320997, 122621.81785450733, 130904.61612680482, 120693.32883078682]', 1, '2026-01-19 09:55:25'),
(8, 18, 13, 'Salma El Fassi', 'MA', NULL, 55360.4, 55.3604, 66.6795, 100000.0, 85.9909, 91.6579, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 105126.58564860391, 113713.78934399513, 119282.6489793523, 128612.8424353487, 133162.059894026, 140929.92585195083, 141462.60623479207, 141066.4973222508, 148538.750563349, 147371.86567436327, 155360.4108524217]', 1, '2026-01-19 09:55:27'),
(9, 19, 14, 'Anas Belkhayat', 'MA', NULL, 71835.6, 71.8356, 87.3296, 100000.0, 91.4836, 95.8172, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 98047.64051526436, 97800.53824834788, 102269.57256612445, 102561.35717231157, 107516.55849021902, 108412.52252551312, 116577.70257038675, 118739.37873153324, 120365.74780397095, 123513.00559898565, 171835.63302635262]', 1, '2026-01-19 09:55:28'),
(10, 20, 15, 'Zineb Berrada', 'MA', NULL, 76882.6, 76.8826, 74.1808, 100000.0, 96.2121, 93.4439, 0, 'ALL_TIME', '["Elite Performer", "Moroccan Pro", "Top 10"]', '[100000.0, 107969.45051260103, 116234.55009182716, 119379.20055681879, 117754.45268108098, 121812.60255293017, 120592.42978388848, 122779.13799200812, 130648.05283153286, 129648.6922193376, 128035.4294268124, 176882.64261721855]', 1, '2026-01-19 09:55:30');
-- Table structure for table `lesson_translations`
DROP TABLE IF EXISTS `lesson_translations`;
CREATE TABLE `lesson_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lesson_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_lesson_lang` (`lesson_id`,`lang`),
  CONSTRAINT `lesson_translations_ibfk_1` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `lesson_translations`
-- Table structure for table `lessons`
DROP TABLE IF EXISTS `lessons`;
CREATE TABLE `lessons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `title` varchar(150) NOT NULL,
  `slug` varchar(150) DEFAULT NULL,
  `lesson_type` enum('TEXT') DEFAULT NULL,
  `content_type` varchar(20) DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL,
  `content` text,
  `content_prompt` text,
  `order_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `lessons`
INSERT INTO `lessons` VALUES 
(22, 15, 'Qu''est-ce que le Trading ?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Introduction au Trading (FR)</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(24, 17, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Introduction to Price Action</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(25, 18, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Smart Money Concepts (SMC / ICT)</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(26, 19, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Trading Psychology Under Pressure</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(27, 20, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Basic Risk Management for Traders</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(28, 21, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Market Structure & Trend Logic</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(29, 22, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<h2>Welcome to Supply & Demand Trading</h2><p>This comprehensive course will teach you everything you need to know.</p>', NULL, 1),
(30, 23, 'What is Trading?', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Understanding Trading</h2>\n                <p class="text-gray-300 text-lg">Trading is the act of buying and selling financial instruments (stocks, currencies, commodities) with the goal of generating profit from price movements.</p>\n                <div class="bg-gray-800 p-6 rounded-xl border-l-4 border-blue-500">\n                    <h3 class="text-xl font-bold text-white mb-3">Key Differences: Trading vs Investing</h3>\n                    <ul class="list-disc pl-6 space-y-2 text-gray-300">\n                        <li><strong>Trading:</strong> Short to medium-term (minutes to weeks)</li>\n                        <li><strong>Investing:</strong> Long-term (months to years)</li>\n                    </ul>\n                </div>\n            </div>', NULL, 1),
(31, 23, 'Trading Terminology', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Essential Terms</h2>\n                <div class="bg-blue-900/30 p-6 rounded-xl border border-blue-500/40 mb-6">\n                    <h3 class="text-2xl font-bold text-blue-300 mb-4">PIP (Percentage in Point)</h3>\n                    <p class="text-gray-300 mb-3">The smallest price movement in most currency pairs. 1 Pip = 0.0001 (usually).</p>\n                </div>\n            </div>', NULL, 2),
(32, 24, 'How Markets Work', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Supply & Demand</h2>\n                <p class="text-gray-300 text-lg">Markets move based on the imbalance between buyers (demand) and sellers (supply).</p>\n            </div>', NULL, 1),
(33, 24, 'Leverage & Margin', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Leverage</h2>\n                <p class="text-gray-300 text-lg">Leverage allows you to multiply your buying power. Use it wisely.</p>\n            </div>', NULL, 2),
(34, 25, 'The 1% Rule', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Risk Management</h2>\n                <p class="text-gray-300 text-lg">Never risk more than 1% of your account on a single trade.</p>\n            </div>', NULL, 1),
(35, 25, 'Trading Psychology', NULL, 'TEXT', 'html', NULL, '<div class="space-y-6">\n                <h2 class="text-3xl font-bold text-yellow-500">Psychology</h2>\n                <p class="text-gray-300 text-lg">Master your emotions (FOMO, Greed, Fear) to succeed.</p>\n            </div>', NULL, 2);
-- Table structure for table `market_signals`
DROP TABLE IF EXISTS `market_signals`;
CREATE TABLE `market_signals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asset` varchar(20) NOT NULL,
  `signal_type` varchar(10) NOT NULL,
  `confidence` int DEFAULT NULL,
  `entry_price` float NOT NULL,
  `stop_loss` float NOT NULL,
  `take_profit` float NOT NULL,
  `reasoning` text,
  `quality` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `market_signals`
-- Table structure for table `module_translations`
DROP TABLE IF EXISTS `module_translations`;
CREATE TABLE `module_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_module_lang` (`module_id`,`lang`),
  CONSTRAINT `module_translations_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `module_translations`
-- Table structure for table `modules`
DROP TABLE IF EXISTS `modules`;
CREATE TABLE `modules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `title` varchar(150) NOT NULL,
  `order_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `modules_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `modules`
INSERT INTO `modules` VALUES 
(15, 11, 'MODULE 1: LES FONDAMENTAUX', 1),
(17, 13, 'MODULE 1: THE FUNDAMENTALS', 1),
(18, 14, 'MODULE 1: THE FUNDAMENTALS', 1),
(19, 15, 'MODULE 1: THE FUNDAMENTALS', 1),
(20, 16, 'MODULE 1: THE FUNDAMENTALS', 1),
(21, 17, 'MODULE 1: THE FUNDAMENTALS', 1),
(22, 18, 'MODULE 1: THE FUNDAMENTALS', 1),
(23, 12, 'Fundamentals of Trading', 1),
(24, 12, 'Market Structure & Instruments', 2),
(25, 12, 'Risk & Psychology', 3);
-- Table structure for table `option_translations`
DROP TABLE IF EXISTS `option_translations`;
CREATE TABLE `option_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `option_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `text` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_option_lang` (`option_id`,`lang`),
  CONSTRAINT `option_translations_ibfk_1` FOREIGN KEY (`option_id`) REFERENCES `options` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `option_translations`
-- Table structure for table `options`
DROP TABLE IF EXISTS `options`;
CREATE TABLE `options` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `text` varchar(200) NOT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `options_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `options`
INSERT INTO `options` VALUES 
(40, 14, 'Profit', 0),
(41, 14, 'Percentage in Point', 1),
(42, 15, 'Risk 1% max per trade', 1),
(43, 15, 'Make 1% profit daily', 0),
(44, 16, 'Stocks', 0),
(45, 16, 'Forex', 1),
(46, 17, 'Magic', 0),
(47, 17, 'Supply and Demand', 1),
(48, 18, 'Fear Of Missing Out', 1),
(49, 18, 'Happy trading', 0),
(50, 19, 'To limit loss', 1),
(51, 19, 'To stop profit', 0),
(52, 20, 'Borrowed buying power', 1),
(53, 20, 'Free money', 0),
(54, 21, 'Bid/Ask Diff', 1),
(55, 21, 'Profit', 0),
(56, 22, 'Selling', 0),
(57, 22, 'Buying', 1),
(58, 23, 'Buying', 0),
(59, 23, 'Selling', 1);
-- Table structure for table `performance_snapshots`
DROP TABLE IF EXISTS `performance_snapshots`;
CREATE TABLE `performance_snapshots` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `period` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `profit` float DEFAULT NULL,
  `roi` float DEFAULT NULL,
  `win_rate` float DEFAULT NULL,
  `trades_count` int DEFAULT NULL,
  `equity` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `performance_snapshots_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `performance_snapshots`
-- Table structure for table `post_likes`
DROP TABLE IF EXISTS `post_likes`;
CREATE TABLE `post_likes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_likes_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `post_likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `post_likes`
-- Table structure for table `posts`
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `posts`
-- Table structure for table `question_translations`
DROP TABLE IF EXISTS `question_translations`;
CREATE TABLE `question_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `text` text NOT NULL,
  `explanation` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_question_lang` (`question_id`,`lang`),
  CONSTRAINT `question_translations_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `question_translations`
-- Table structure for table `questions`
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int NOT NULL,
  `text` text NOT NULL,
  `explanation` text,
  `order_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `questions`
INSERT INTO `questions` VALUES 
(14, 8, 'What is a PIP?', 'Percentage in Point, usually 4th decimal.', 1),
(15, 8, 'What is the 1% Rule?', 'Max risk per trade.', 2),
(16, 8, 'Which market is most liquid?', 'Forex market.', 3),
(17, 8, 'What moves price?', 'Supply and Demand.', 4),
(18, 8, 'What is FOMO?', 'Fear Of Missing Out.', 5),
(19, 8, 'Why use stop loss?', 'To limit loss.', 6),
(20, 8, 'What is Leverage?', 'Borrowed capital.', 7),
(21, 8, 'What is Spread?', 'Difference between Bid and Ask.', 8),
(22, 8, 'Long position means?', 'Buying.', 9),
(23, 8, 'Short position means?', 'Selling.', 10);
-- Table structure for table `quiz_translations`
DROP TABLE IF EXISTS `quiz_translations`;
CREATE TABLE `quiz_translations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_quiz_lang` (`quiz_id`,`lang`),
  CONSTRAINT `quiz_translations_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `quiz_translations`
-- Table structure for table `quizzes`
DROP TABLE IF EXISTS `quizzes`;
CREATE TABLE `quizzes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `lesson_id` int DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  `min_pass_score` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `module_id` (`module_id`),
  KEY `course_id` (`course_id`),
  KEY `lesson_id` (`lesson_id`),
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`),
  CONSTRAINT `quizzes_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `quizzes_ibfk_3` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `quizzes`
INSERT INTO `quizzes` VALUES 
(8, NULL, 12, NULL, 'Final Exam: Trading Fundamentals', 70);
-- Table structure for table `risk_alerts`
DROP TABLE IF EXISTS `risk_alerts`;
CREATE TABLE `risk_alerts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `alert_type` varchar(50) NOT NULL,
  `severity` varchar(20) DEFAULT NULL,
  `message` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `risk_alerts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `risk_alerts`
-- Table structure for table `system_config`
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `key` varchar(50) NOT NULL,
  `value` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `system_config`
-- Table structure for table `trades`
DROP TABLE IF EXISTS `trades`;
CREATE TABLE `trades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `side` enum('BUY','SELL') NOT NULL,
  `quantity` float NOT NULL,
  `price` float NOT NULL,
  `trade_type` enum('BUY','SELL') DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `entry_price` float DEFAULT NULL,
  `exit_price` float DEFAULT NULL,
  `stop_loss` float DEFAULT NULL,
  `take_profit` float DEFAULT NULL,
  `commission` float DEFAULT NULL,
  `swap` float DEFAULT NULL,
  `notes` text,
  `status` enum('OPEN','CLOSED') DEFAULT NULL,
  `pnl` float DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `closed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `trades_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`),
  CONSTRAINT `trades_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `trades`
INSERT INTO `trades` VALUES 
(1, 18, 1, 'BTC/USD', 'BUY', 0.0, 0.0, 'BUY', 1000.0, 0.0, NULL, NULL, NULL, 0.0, 0.0, NULL, 'OPEN', 0.0, '2026-01-19 11:32:10', '2026-01-19 11:32:10', NULL),
(2, 17, 21, 'BTC/USD', 'BUY', 0.0, 0.0, 'BUY', 1000.0, 0.0, NULL, NULL, NULL, 0.0, 0.0, NULL, 'OPEN', 0.0, '2026-01-19 11:33:44', '2026-01-19 11:33:44', NULL),
(3, 17, 21, 'BTC/USD', 'SELL', 0.0, 0.0, 'SELL', 1000.0, 0.0, NULL, NULL, NULL, 0.0, 0.0, NULL, 'OPEN', 0.0, '2026-01-19 11:33:52', '2026-01-19 11:33:52', NULL);
-- Table structure for table `trading_floors`
DROP TABLE IF EXISTS `trading_floors`;
CREATE TABLE `trading_floors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `floor_type` enum('GLOBAL','SCALPING','SWING','CRYPTO','INDICES','FOREX') NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `icon_name` varchar(50) DEFAULT NULL,
  `required_level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `trading_floors`
-- Table structure for table `transactions`
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `amount` float NOT NULL,
  `currency` varchar(3) DEFAULT NULL,
  `payment_method` enum('PAYPAL','CMI','CRYPTO') NOT NULL,
  `status` enum('PENDING','COMPLETED','FAILED') DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `transactions`
INSERT INTO `transactions` VALUES 
(1, 17, 21, 1000.0, 'MAD', 'CRYPTO', 'COMPLETED', 'CRYPTO_1768821360266_p2cckf2yu', '2026-01-19 11:16:00'),
(2, 18, 1, 1000.0, 'MAD', 'CMI', 'COMPLETED', 'CMI_1768821880351_up547m6hw', '2026-01-19 11:24:56'),
(3, 21, 23, 200.0, 'MAD', 'CMI', 'COMPLETED', 'CMI_1768824597512_qt9wdk3m9', '2026-01-19 12:09:59');
-- Table structure for table `user_badges`
DROP TABLE IF EXISTS `user_badges`;
CREATE TABLE `user_badges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `badge_id` int NOT NULL,
  `earned_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `badge_id` (`badge_id`),
  CONSTRAINT `user_badges_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_badges_ibfk_2` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_badges`
-- Table structure for table `user_challenges`
DROP TABLE IF EXISTS `user_challenges`;
CREATE TABLE `user_challenges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `plan_name` varchar(50) NOT NULL,
  `amount` float NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_challenges_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_challenges`
INSERT INTO `user_challenges` VALUES 
(1, 21, 'Elite Institutional', 1000.0, 'CRYPTO', 'active', '2026-01-19 11:16:01'),
(2, 1, 'Elite Institutional', 1000.0, 'CMI', 'active', '2026-01-19 11:24:57'),
(3, 23, 'Starter Challenge', 200.0, 'CMI', 'active', '2026-01-19 12:10:00');
-- Table structure for table `user_course_progress`
DROP TABLE IF EXISTS `user_course_progress`;
CREATE TABLE `user_course_progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `is_completed` tinyint(1) DEFAULT NULL,
  `progress_percent` int DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `user_course_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_course_progress_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_course_progress`
-- Table structure for table `user_lesson_progress`
DROP TABLE IF EXISTS `user_lesson_progress`;
CREATE TABLE `user_lesson_progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `lesson_id` int NOT NULL,
  `is_completed` tinyint(1) DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `quiz_score` int DEFAULT NULL,
  `quiz_passed` tinyint(1) DEFAULT NULL,
  `last_accessed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `lesson_id` (`lesson_id`),
  CONSTRAINT `user_lesson_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_lesson_progress_ibfk_2` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_lesson_progress`
INSERT INTO `user_lesson_progress` VALUES 
(15, 1, 22, 0, NULL, NULL, 0, '2026-01-19 18:30:14'),
(16, 1, 27, 0, NULL, NULL, 0, '2026-01-19 18:13:36');
-- Table structure for table `user_preferences`
DROP TABLE IF EXISTS `user_preferences`;
CREATE TABLE `user_preferences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `language` varchar(10) DEFAULT NULL,
  `theme` varchar(20) DEFAULT NULL,
  `timezone` varchar(50) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `notifications_enabled` tinyint(1) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_preferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_preferences`
-- Table structure for table `user_quiz_answers`
DROP TABLE IF EXISTS `user_quiz_answers`;
CREATE TABLE `user_quiz_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `attempt_id` int NOT NULL,
  `question_id` int NOT NULL,
  `selected_option_id` int DEFAULT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `attempt_id` (`attempt_id`),
  KEY `question_id` (`question_id`),
  KEY `selected_option_id` (`selected_option_id`),
  CONSTRAINT `user_quiz_answers_ibfk_1` FOREIGN KEY (`attempt_id`) REFERENCES `user_quiz_attempts` (`id`),
  CONSTRAINT `user_quiz_answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  CONSTRAINT `user_quiz_answers_ibfk_3` FOREIGN KEY (`selected_option_id`) REFERENCES `options` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_quiz_answers`
-- Table structure for table `user_quiz_attempts`
DROP TABLE IF EXISTS `user_quiz_attempts`;
CREATE TABLE `user_quiz_attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `quiz_id` int NOT NULL,
  `score` float DEFAULT NULL,
  `passed` tinyint(1) DEFAULT NULL,
  `attempt_number` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `user_quiz_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_quiz_attempts_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_quiz_attempts`
-- Table structure for table `user_xp`
DROP TABLE IF EXISTS `user_xp`;
CREATE TABLE `user_xp` (
  `user_id` int NOT NULL,
  `total_xp` int DEFAULT NULL,
  `level_title` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_xp_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `user_xp`
INSERT INTO `user_xp` VALUES 
(22, 50, 'Novice');
-- Table structure for table `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `role` enum('USER','ADMIN','SUPERADMIN') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `users`
INSERT INTO `users` VALUES 
(1, 'Admin TradeSense', 'admin', 'malekfatimzahra@gmail.com', 'scrypt:32768:8:1$L2qo0zTkadOhLjxY$994a00e13e0eac56a5adb7b12f6a1061e62bd2a03d4f9c7ebaa5ba39b0f70fae70fe3ed649453085903f40155608521cae8a9703a35fb11a29415143e077dee0', 'ADMIN', '2026-01-18 23:30:19'),
(2, 'Test User', 'testuser', 'test@tradesense.com', 'scrypt:32768:8:1$Mil9ims7cJbhI2nI$c179761c0a890d8b7f45d98c32e083be779cb57b070be9f49d85f347c371c93309b31052ceb3f975e39398667ab20c2718027fcb7642ba4785b5dd42e98f0481', 'USER', '2026-01-18 23:30:19'),
(3, 'faty', 'ml', 'fatyy@gmail.com', 'scrypt:32768:8:1$fAuqJbF5DOCEjzi4$3045aec5ff6a4ea5c793e598c7d3fc40486ac3eb51d94784d1332d3dfb4075c4870cd2c05914a94e69b0a4fdca6d90afd26b29ca84b660457d2920fbc775d136', 'USER', '2026-01-19 00:04:08'),
(4, 'Karim Trader', 'karim_trader', 'karim@trade.ma', 'scrypt:32768:8:1$3zDDU2VycCogFXeU$51e39825a2dcdbef076c814ac0d8d19df58c39a58f51d2cfd73e19b2d9a8220b1a3887ec7949957fcbf4303719814a99252dac754c4a5da225105cacc637f8ed', 'USER', '2026-01-19 00:39:45'),
(5, 'Sara Admin', 'sara_admin', 'sara@admin.ma', 'scrypt:32768:8:1$Dw3MnpS7j0rHaL4a$994002a8e2a2fcd566cfae274247507005301c4624f688f1c453b9255e142e1433c05102a428e0c49225c45da8daa7e291e03b172d86e91155f996c9c6760b50', 'ADMIN', '2026-01-19 00:39:46'),
(6, 'Super Admin', 'super_admin', 'superadmin@tradesense.ma', 'scrypt:32768:8:1$fAxkulfpdQg2Ioe8$735594ca07aad42b9b62d15d87e29e0dda244b95b691d75b4e11388d18c72346db5ee77c49189bc349704f4f2b2e648f8b2fe62973e5d12d65a599006d25a646', 'SUPERADMIN', '2026-01-19 00:39:47'),
(7, 'Othman Chakir', 'ochakir', 'ochakir@demo.com', 'scrypt:32768:8:1$LNvf49XkYv0RQKKk$8e01b377cc7192137facd4aa74fe1d041599d3590a1978b105554a664fc94f98797f13651d4c598ea66479f56b317cb15695bfbca9ae176bbbe23db2b7a165d3', 'USER', '2026-01-19 09:55:00'),
(8, 'Imane Benjelloun', 'ibenjelloun', 'ibenjelloun@demo.com', 'scrypt:32768:8:1$QzvaM3EdR8cHbOZs$11491e5996d995c3b8c981d36588ace17af2022d2b865b26077760dc7a73cc5a8a76589a14ab3100a476c99ce106bb9c4d0dd689cf06f4e74635ed576e4187b6', 'USER', '2026-01-19 09:55:00'),
(9, 'Mehdi Lazrak', 'mlazrak', 'mlazrak@demo.com', 'scrypt:32768:8:1$pwxHSWcfPrq7r69O$5cb6385ac08049c6b21b21033cc4d8b030e7c30ad293433075f156df2ad522d46148cd42e34b09eb89d9e643c890066d5633a346f351a91a181c464cf4464dd8', 'USER', '2026-01-19 09:55:01'),
(10, 'Khadija Tazi', 'ktazi', 'ktazi@demo.com', 'scrypt:32768:8:1$6wP8km3ydFVfaFyr$bb3a263c02bb3e450fe8fef5a27c3a16a5ae3eca5efee2fb768a1d8603ab4b1b0421b66abea9cd74bae8d894a32902d2e320b37b259b1c8aec33ee54c44e6213', 'USER', '2026-01-19 09:55:02'),
(11, 'Amine Benali', 'amine_benali54', 'amine_benali54@tradesense-elite.ma', 'scrypt:32768:8:1$TPWYXnYgjPfKo5cK$318a01027a9feb3a928199974cbffacd9bb6f0680da97232e84ca823bddeb13ff8b19ae8d1abb3261cda1f62dfdf50d34dbbc77f8a500d1b044644090c3f2f0c', 'USER', '2026-01-19 09:55:13'),
(12, 'Fatima Zahra El Idrissi', 'fatima_zahra_el_idrissi33', 'fatima_zahra_el_idrissi33@tradesense-elite.ma', 'scrypt:32768:8:1$o6sPNcFw0gbWg37b$7f44ab81f04bd7306161f39d98f9d1767958b37c339d53a01a6a22050e6763824341bab0d95f30aa0897b16f64f618fda69f3fca3cf85f869ed9805fe1480261', 'USER', '2026-01-19 09:55:15'),
(13, 'Youssef Alami', 'youssef_alami32', 'youssef_alami32@tradesense-elite.ma', 'scrypt:32768:8:1$pqpf6OJEc2Gz6ZwU$d8c52f281501c82e707d8f3978f01df91b12122e53a909165c721834e3a11756d8b85251be6b959821da86c315484e5dc3749a8fb8d75c1ebd1438315d7085ea', 'USER', '2026-01-19 09:55:17'),
(14, 'Siham Mansouri', 'siham_mansouri96', 'siham_mansouri96@tradesense-elite.ma', 'scrypt:32768:8:1$iaDpyxcyVUaXui2N$e244517ebc5d8f05e8916cdea4931df7ee6e28cf8c90551bafdf492bdcce0c3c58f4ad8afe060a6e49d79a8bfe6fa9256fee7e10b8a5a0759234c12d549a0488', 'USER', '2026-01-19 09:55:20'),
(15, 'Omar Bennani', 'omar_bennani44', 'omar_bennani44@tradesense-elite.ma', 'scrypt:32768:8:1$esGKmve49giKQy08$5eca8408637215b0b60a685079ba6101a229bf6c0ef3647ceea4e40782cf757891a9e7b8d4204a7d974e6052e20f09da040cb05f78b9174fe0a769dd2b20b28e', 'USER', '2026-01-19 09:55:21'),
(16, 'Laila Tazi', 'laila_tazi48', 'laila_tazi48@tradesense-elite.ma', 'scrypt:32768:8:1$4TuxMrnxrWduogHR$ef46f9f874d9ac52bd6291def514848e5e11d3e5a1091f919912f015786bf4f10055d95bf73ec405a83c8b678b47a0838bc601c4bf17a5cd139e590d7afe57c7', 'USER', '2026-01-19 09:55:23'),
(17, 'Mehdi Chraibi', 'mehdi_chraibi48', 'mehdi_chraibi48@tradesense-elite.ma', 'scrypt:32768:8:1$4w8Py1oZueDnu44o$ff998d8930797965eb0e3e5cb72f491dabd72cb9ff2d839174c213708de17ddbc4a297ac54f147cce79d9be8eb2388ace7fb372b6f063175f0defa7ce8ce4804', 'USER', '2026-01-19 09:55:24'),
(18, 'Salma El Fassi', 'salma_el_fassi37', 'salma_el_fassi37@tradesense-elite.ma', 'scrypt:32768:8:1$RcrrPLCSqVWws7kw$b3d2e28e55ad9fd85e6c44120bfc4a517eaf45c1c0db361b70141d5bf9b8e0de1e108aeae1fd55357356595d737fa8cecd714cdc15d7a156ac1fe7245ce45516', 'USER', '2026-01-19 09:55:26'),
(19, 'Anas Belkhayat', 'anas_belkhayat87', 'anas_belkhayat87@tradesense-elite.ma', 'scrypt:32768:8:1$v3SSjGqpUu7FaD0g$9965697f7c2e567376f8435078128ee90c9a98131e5fbccbab3c428fab69e0d53c1d3f4f564dec9be8724f8939d5a2cdac841ed1e3cd0f2e0109edc837ba5e4a', 'USER', '2026-01-19 09:55:28'),
(20, 'Zineb Berrada', 'zineb_berrada32', 'zineb_berrada32@tradesense-elite.ma', 'scrypt:32768:8:1$H4tNJMFuppNUK4HR$ec5fa64721ec26a5479203a9be1b7ccb63d60c351487e432dadef59d30a932f7a4ac4fb334313284da7716089c37be75ae22d83baf8ca0287eaf2e13c9a026b3', 'USER', '2026-01-19 09:55:29'),
(21, 'MOUHCINE MALEK', 'malek', 'mhcnmalek@gmail.com', 'scrypt:32768:8:1$21thpHYUiHS3Uwd3$be4b4bffa94a159b37a584b2edf79615c9108a103013118accb62c661b5b31d2a7a9d869e0476f519cb08b299dd05e0c100bb4aedba93871a094d8f584f68286', 'USER', '2026-01-19 11:14:46'),
(22, 'wiame', 'pro', 'fahmiwiame2@gmail.com', 'scrypt:32768:8:1$M3Ax6Tt4uTteNeru$6ad7f73b364eb55f79c2e6b0febad52645f7b6678e76f0a003164b6ec04048ca75c42d41e08c0eeec2a2a1d556dd90ea1bd581fa6374942f23919b383dda954b', 'USER', '2026-01-19 12:08:38'),
(23, 'faty', 'de', 'faty@gmail.com', 'scrypt:32768:8:1$wb0TnL0GKpxlRR5M$652a176cfd11fdb8c618f0e191e856caafb108ba9b7df547d285eca284934c24512fb363a035cbdcbb4d9592d95bef2cc1467c6a2a03977a1ae4adc90e61765a', 'USER', '2026-01-19 12:09:42');
SET FOREIGN_KEY_CHECKS = 1;
