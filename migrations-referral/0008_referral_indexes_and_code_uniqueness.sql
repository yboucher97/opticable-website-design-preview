UPDATE referral_codes
SET
  is_active = 0,
  deactivated_at = COALESCE(deactivated_at, CURRENT_TIMESTAMP)
WHERE is_active = 1
  AND id NOT IN (
    SELECT MAX(id)
    FROM referral_codes
    WHERE is_active = 1
    GROUP BY account_id
  );

CREATE UNIQUE INDEX IF NOT EXISTS referral_codes_single_active_idx
  ON referral_codes(account_id)
  WHERE is_active = 1;

UPDATE referral_credit_codes
SET
  is_active = 0,
  deactivated_at = COALESCE(deactivated_at, CURRENT_TIMESTAMP)
WHERE is_active = 1
  AND id NOT IN (
    SELECT MAX(id)
    FROM referral_credit_codes
    WHERE is_active = 1
    GROUP BY account_id
  );

CREATE UNIQUE INDEX IF NOT EXISTS referral_credit_codes_single_active_idx
  ON referral_credit_codes(account_id)
  WHERE is_active = 1;

CREATE INDEX IF NOT EXISTS referral_accounts_type_status_created_idx
  ON referral_accounts(account_type, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_cases_account_status_created_idx
  ON referral_cases(account_id, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_cases_type_status_created_idx
  ON referral_cases(account_type, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_rewards_account_type_status_created_idx
  ON referral_rewards(account_id, reward_type, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_rewards_type_status_created_idx
  ON referral_rewards(reward_type, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_login_tokens_account_purpose_expires_idx
  ON referral_login_tokens(account_id, purpose, expires_at DESC);
