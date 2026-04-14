ALTER TABLE referral_accounts ADD COLUMN password_hash TEXT;
ALTER TABLE referral_accounts ADD COLUMN password_salt TEXT;
ALTER TABLE referral_accounts ADD COLUMN password_set_at TEXT;
