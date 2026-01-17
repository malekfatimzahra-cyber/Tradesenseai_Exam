-- Migration to add admin_note column to accounts table
-- Run this if you haven't already
ALTER TABLE accounts ADD COLUMN admin_note TEXT;

-- Verify user_challenges (mapped to 'accounts' table in models.py) structure (already done via SQLAlchemy)
-- users table should have 'role' column (already exists)
