CREATE TABLE IF NOT EXISTS promo_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  campaign_id TEXT NOT NULL,
  locale TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  email_normalized TEXT NOT NULL,
  phone TEXT,
  company TEXT,
  business_attestation INTEGER NOT NULL DEFAULT 0,
  quebec_attestation INTEGER NOT NULL DEFAULT 0,
  rules_version TEXT NOT NULL,
  privacy_version TEXT NOT NULL,
  marketing_opt_in INTEGER NOT NULL DEFAULT 0,
  marketing_opt_in_at TEXT,
  marketing_opt_out_at TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  discount_percent INTEGER NOT NULL,
  discount_cap_cad INTEGER NOT NULL,
  promo_code TEXT NOT NULL,
  promo_expires_at TEXT NOT NULL,
  skill_question TEXT NOT NULL,
  result_created_at TEXT NOT NULL,
  landing_path TEXT,
  landing_url TEXT,
  referrer_url TEXT,
  referrer_host TEXT,
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  utm_content TEXT,
  utm_term TEXT,
  turnstile_hostname TEXT,
  client_ip_hash TEXT,
  user_agent_hash TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS promo_entries_campaign_email_idx
  ON promo_entries (campaign_id, email_normalized);

CREATE UNIQUE INDEX IF NOT EXISTS promo_entries_campaign_code_idx
  ON promo_entries (campaign_id, promo_code);

CREATE INDEX IF NOT EXISTS promo_entries_created_at_idx
  ON promo_entries (created_at DESC);

CREATE INDEX IF NOT EXISTS promo_entries_marketing_idx
  ON promo_entries (marketing_opt_in, marketing_opt_out_at, created_at DESC);

CREATE TABLE IF NOT EXISTS promo_marketing_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  campaign_id TEXT,
  email_normalized TEXT NOT NULL,
  locale TEXT,
  event_type TEXT NOT NULL,
  source TEXT NOT NULL,
  created_at TEXT NOT NULL,
  client_ip_hash TEXT,
  user_agent_hash TEXT
);

CREATE INDEX IF NOT EXISTS promo_marketing_events_email_idx
  ON promo_marketing_events (email_normalized, created_at DESC);
