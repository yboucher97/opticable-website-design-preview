ALTER TABLE referral_cases ADD COLUMN zoho_lead_id TEXT;
ALTER TABLE referral_cases ADD COLUMN zoho_deal_id TEXT;
ALTER TABLE referral_cases ADD COLUMN zoho_quote_id TEXT;
ALTER TABLE referral_cases ADD COLUMN zoho_invoice_id TEXT;

CREATE INDEX IF NOT EXISTS referral_cases_zoho_lead_idx
  ON referral_cases(zoho_lead_id);

CREATE INDEX IF NOT EXISTS referral_cases_zoho_deal_idx
  ON referral_cases(zoho_deal_id);

CREATE INDEX IF NOT EXISTS referral_cases_zoho_quote_idx
  ON referral_cases(zoho_quote_id);

CREATE INDEX IF NOT EXISTS referral_cases_zoho_invoice_idx
  ON referral_cases(zoho_invoice_id);
