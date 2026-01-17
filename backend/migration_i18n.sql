-- ========================================================
-- TRADESENSE AI - MIGRATION MULTI-LANGUE (i18n)
---- ========================================================

-- 1. USER SETTINGS
CREATE TABLE IF NOT EXISTS user_settings (
    user_id INT PRIMARY KEY,
    lang ENUM('fr', 'en', 'ar') DEFAULT 'fr',
    theme ENUM('light', 'dark', 'system') DEFAULT 'dark',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed user_settings for existing users (default to FR)
INSERT IGNORE INTO user_settings (user_id, lang)
SELECT id, 'fr' FROM users;

-- 2. ACADEMY TRANSLATIONS

-- Courses Translations
CREATE TABLE IF NOT EXISTS course_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    lang CHAR(2) NOT NULL, -- 'fr', 'en', 'ar'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_course_lang (course_id, lang)
);

-- Modules Translations
CREATE TABLE IF NOT EXISTS module_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT NOT NULL,
    lang CHAR(2) NOT NULL,
    title VARCHAR(255) NOT NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    UNIQUE KEY unique_module_lang (module_id, lang)
);

-- Lessons Translations
CREATE TABLE IF NOT EXISTS lesson_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    lang CHAR(2) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT, -- HTML content
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    UNIQUE KEY unique_lesson_lang (lesson_id, lang)
);

-- Quizzes Translations
CREATE TABLE IF NOT EXISTS quiz_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    lang CHAR(2) NOT NULL,
    title VARCHAR(150),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_quiz_lang (quiz_id, lang)
);

-- Questions Translations
CREATE TABLE IF NOT EXISTS question_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    lang CHAR(2) NOT NULL,
    text TEXT NOT NULL,
    explanation TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_question_lang (question_id, lang)
);

-- Options Translations
CREATE TABLE IF NOT EXISTS option_translations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    option_id INT NOT NULL,
    lang CHAR(2) NOT NULL,
    text VARCHAR(200) NOT NULL,
    FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE,
    UNIQUE KEY unique_option_lang (option_id, lang)
);

-- 3. MIGRATE EXISTING DATA TO 'FR' (Default)

-- Courses
INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'fr', title, description FROM courses;

-- Modules
INSERT IGNORE INTO module_translations (module_id, lang, title)
SELECT id, 'fr', title FROM modules;

-- Lessons
INSERT IGNORE INTO lesson_translations (lesson_id, lang, title, content)
SELECT id, 'fr', title, content FROM lessons;

-- Quizzes
INSERT IGNORE INTO quiz_translations (quiz_id, lang, title)
SELECT id, 'fr', title FROM quizzes;

-- Questions
INSERT IGNORE INTO question_translations (question_id, lang, text, explanation)
SELECT id, 'fr', text, explanation FROM questions;

-- Options
INSERT IGNORE INTO option_translations (option_id, lang, text)
SELECT id, 'fr', text FROM options;

-- 4. SEED ENGLISH & ARABIC (Basic Examples)

-- Update 'Introduction au Trading' (assuming ID=1)
INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'en', 'Introduction to Trading', 'Master the basics of financial markets and trading psychology.'
FROM courses WHERE title LIKE '%Introduction%';

INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'ar', 'مقدمة في التداول', 'أتقن أساسيات الأسواق المالية وعلم النفس التجاري.'
FROM courses WHERE title LIKE '%Introduction%';

-- Update 'Analyste Technique' (assuming ID=2)
INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'en', 'Technical Analysis Mastery', 'Learn to read charts, patterns, and indicators like a pro.'
FROM courses WHERE title LIKE '%Technique%';

INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'ar', 'إتقان التحليل الفني', 'تعلم قراءة الرسوم البيانية والأنماط والمؤشرات كالمحترفين.'
FROM courses WHERE title LIKE '%Technique%';

-- Update 'Stratégies Avancées' (assuming ID=3)
INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'en', 'Advanced Strategies', 'Professional trading strategies for consistent profits.'
FROM courses WHERE title LIKE '%Avancées%';

INSERT IGNORE INTO course_translations (course_id, lang, title, description)
SELECT id, 'ar', 'استراتيجيات متقدمة', 'استراتيجيات تداول احترافية لتحقيق أرباح مستمرة.'
FROM courses WHERE title LIKE '%Avancées%';
