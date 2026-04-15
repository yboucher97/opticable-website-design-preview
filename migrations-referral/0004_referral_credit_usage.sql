CREATE TABLE IF NOT EXISTS referral_credit_codes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  code TEXT NOT NULL UNIQUE,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  deactivated_at TEXT,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS referral_credit_codes_account_idx
  ON referral_credit_codes(account_id, is_active);

CREATE TABLE IF NOT EXISTS referral_credit_uses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  credit_code_id INTEGER,
  credit_code TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('reserved', 'applied', 'released', 'void')),
  amount_cents INTEGER NOT NULL,
  contact_name TEXT NOT NULL,
  contact_email TEXT NOT NULL,
  contact_email_normalized TEXT NOT NULL,
  contact_company TEXT,
  contact_company_normalized TEXT,
  quote_reference TEXT,
  note TEXT,
  reserved_at TEXT NOT NULL,
  applied_at TEXT,
  released_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES referral_accounts(id) ON DELETE CASCADE,
  FOREIGN KEY (credit_code_id) REFERENCES referral_credit_codes(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS referral_credit_uses_account_idx
  ON referral_credit_uses(account_id, status, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_credit_uses_email_idx
  ON referral_credit_uses(contact_email_normalized, created_at DESC);

CREATE INDEX IF NOT EXISTS referral_credit_uses_quote_ref_idx
  ON referral_credit_uses(quote_reference);
