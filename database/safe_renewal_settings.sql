-- Safe SQL for Supabase: Add system settings table for renewal control
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS system_settings (
    setting_id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO system_settings (setting_key, setting_value)
VALUES ('renewal_open', 'false')
ON CONFLICT (setting_key) DO NOTHING;
