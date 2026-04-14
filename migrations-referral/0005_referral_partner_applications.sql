CREATE TABLE IF NOT EXISTS referral_partner_applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  status TEXT NOT NULL CHECK (status IN ('pending', 'reviewed', 'approved', 'rejected', 'void')) DEFAULT 'pending',
  locale TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  email_normalized TEXT NOT NULL UNIQUE,
  phone TEXT,
  company TEXT NOT NULL,
  company_normalized TEXT,
  website TEXT,
  notes TEXT,
  review_note TEXT,
  reviewed_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  created_ip_hash TEXT,
  created_user_agent_hash TEXT
);

CREATE INDEX IF NOT EXISTS referral_partner_applications_status_idx
  ON referral_partner_applications(status, created_at DESC);
