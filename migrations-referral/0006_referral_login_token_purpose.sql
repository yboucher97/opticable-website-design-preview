ALTER TABLE referral_login_tokens
  ADD COLUMN purpose TEXT NOT NULL DEFAULT 'signin';
