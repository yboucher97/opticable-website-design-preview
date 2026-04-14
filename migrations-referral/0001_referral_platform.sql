PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS referral_accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_type TEXT NOT NULL CHECK (account_type IN ('client', 'partner')),
  status TEXT NOT NULL CHECK (status IN ('pending', 'active', 'paused', 'rejected')),
  locale TEXT NOT NULL CHECK (locale IN ('en', 'fr')),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  email_normalized TEXT NOT NULL UNIQUE,
  phone TEXT,
  company TEXT,
  company_normalized TEXT,
  website TEXT,
  notes TEXT,
  current_code_id INTEGER,
  wallet_balance_cents INTEGER NOT NULL DEFAULT 0,
  total_earned_cents INTEGER NOT NULL DEFAULT 0,
  approved_at TEXT,
  activated_at TEXT,
  rejected_at TEXT,
  paused_at TEXT,
  last_login_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (current_code_id) REFERENCES referral_codes(id)
);

CREATE TABLE IF NOT EXISTS referral_codes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  code TEXT NOT NULL UNIQUE,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  deactivated_at TEXT,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS referral_codes_account_idx
  ON referral_codes(account_id, is_active);

CREATE TABLE IF NOT EXISTS referral_login_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  token_hash TEXT NOT NULL UNIQUE,
  locale TEXT NOT NULL CHECK (locale IN ('en', 'fr')),
  redirect_path TEXT,
  expires_at TEXT NOT NULL,
  used_at TEXT,
  created_at TEXT NOT NULL,
  created_ip_hash TEXT,
  created_user_agent_hash TEXT,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS referral_login_tokens_account_idx
  ON referral_login_tokens(account_id, expires_at);

CREATE TABLE IF NOT EXISTS referral_cases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  referral_code_id INTEGER,
  referral_code TEXT NOT NULL,
  account_type TEXT NOT NULL CHECK (account_type IN ('client', 'partner')),
  status TEXT NOT NULL CHECK (status IN ('new', 'quoted', 'won', 'completed_paid', 'void')),
  locale TEXT NOT NULL CHECK (locale IN ('en', 'fr')),
  referred_name TEXT NOT NULL,
  referred_email TEXT NOT NULL,
  referred_email_normalized TEXT NOT NULL,
  referred_phone TEXT,
  referred_company TEXT NOT NULL,
  referred_company_normalized TEXT,
  referred_project_notes TEXT,
  quote_reference TEXT,
  landing_path TEXT,
  landing_url TEXT,
  referrer_url TEXT,
  referrer_host TEXT,
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  utm_content TEXT,
  utm_term TEXT,
  referred_discount_percent INTEGER NOT NULL DEFAULT 0,
  referred_discount_cap_cents INTEGER NOT NULL DEFAULT 0,
  quoted_subtotal_cents INTEGER,
  reward_policy_type TEXT NOT NULL CHECK (reward_policy_type IN ('client_credit', 'partner_fixed')),
  reward_amount_cents INTEGER,
  reward_generated_at TEXT,
  completed_paid_at TEXT,
  void_reason TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE,
  FOREIGN KEY (referral_code_id) REFERENCES referral_codes(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS referral_cases_account_idx
  ON referral_cases(account_id, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_cases_status_idx
  ON referral_cases(status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_cases_email_idx
  ON referral_cases(referred_email_normalized, created_at DESC);

CREATE TABLE IF NOT EXISTS referral_rewards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  referral_case_id INTEGER NOT NULL UNIQUE,
  reward_type TEXT NOT NULL CHECK (reward_type IN ('credit', 'payout')),
  status TEXT NOT NULL CHECK (status IN ('pending', 'earned', 'settled', 'void')),
  amount_cents INTEGER NOT NULL,
  note TEXT,
  created_at TEXT NOT NULL,
  earned_at TEXT,
  settled_at TEXT,
  voided_at TEXT,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE,
  FOREIGN KEY (referral_case_id) REFERENCES referral_cases(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS referral_rewards_account_idx
  ON referral_rewards(account_id, status, created_at DESC);

CREATE TABLE IF NOT EXISTS referral_audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER,
  referral_case_id INTEGER,
  reward_id INTEGER,
  actor_type TEXT NOT NULL CHECK (actor_type IN ('system', 'public', 'admin', 'account')),
  actor_label TEXT,
  event_type TEXT NOT NULL,
  metadata_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE SET NULL,
  FOREIGN KEY (referral_case_id) REFERENCES referral_cases(id) ON DELETE SET NULL,
  FOREIGN KEY (reward_id) REFERENCES referral_rewards(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS referral_audit_events_account_idx
  ON referral_audit_events(account_id, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_audit_events_case_idx
  ON referral_audit_events(referral_case_id, created_at DESC);
