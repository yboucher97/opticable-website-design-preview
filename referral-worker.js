import referralConfig from "./referral-config.json";

const REFERRAL_COOKIE_NAME = "opticable-referral-session";
const REFERRAL_CONTACT_PATHS = { en: "/en/contact/", fr: "/fr/contact/" };
const REFERRAL_PORTAL_PATHS = { en: "/en/referral-portal/", fr: "/fr/portail-references/" };
const REFERRAL_ACCESS_PATHS = { en: "/en/referral-portal/access/", fr: "/fr/portail-references/acces/" };
const PASSWORD_HASH_ITERATIONS = 100000;
const PASSWORD_HASH_LENGTH = 32;
const PASSWORD_MIN_LENGTH = 10;

const TEXT = {
  en: {
    configUnavailable: "The referral platform is not configured.",
    invalidRequest: "The request body is invalid.",
    invalidEmail: "Use a valid email address.",
    invalidCode: "Use a valid referral code.",
    requiredField: "Complete all required fields.",
    requiredConsent: "Accept the program terms before continuing.",
    selfReferral: "You cannot use your own referral code.",
    existingLead: "This referral code has already been used for this contact.",
    authRequired: "Sign in to access the portal.",
    invalidToken: "This password reset link is invalid or expired. Request a new reset email from the portal.",
    accountUnavailable: "The referral account is not available.",
    genericError: "The referral request could not be completed.",
    oneProgramOnly: "This email address is already linked to the other referral program. Use one program only per email address.",
    partnerApplicationPending: "A referral partner application already exists for this email. Opticable will review it and contact you.",
    partnerApplicationSubmitted: "Your referral partner application has been sent. Opticable will review it and contact you.",
    loginSent: "If an account exists for this address, a password reset email has just been sent. Check your junk folder if needed.",
    linkPreview: "A password reset link is ready.",
    invalidPassword: "Use a password with at least 10 characters.",
    invalidCredentials: "The email address or password is invalid.",
    currentPasswordRequired: "Enter the current password to change it.",
    currentPasswordInvalid: "The current password is invalid.",
    passwordSaved: "Your password has been saved.",
  },
  fr: {
    configUnavailable: "La plateforme de référence n'est pas configurée.",
    invalidRequest: "Le corps de la requête est invalide.",
    invalidEmail: "Utilisez une adresse courriel valide.",
    invalidCode: "Utilisez un code de référence ou de partenaire valide.",
    requiredField: "Remplissez tous les champs obligatoires.",
    requiredConsent: "Acceptez les conditions du programme avant de continuer.",
    selfReferral: "Vous ne pouvez pas utiliser votre propre code de référence.",
    existingLead: "Ce code a déjà été utilisé pour ce contact.",
    authRequired: "Connectez-vous pour accéder au portail.",
    invalidToken: "Le lien de réinitialisation est invalide ou expiré. Demandez un nouveau courriel de réinitialisation depuis le portail.",
    accountUnavailable: "Le compte de référence n'est pas disponible.",
    genericError: "La demande de référence n'a pas pu être traitée.",
    loginSent: "Si un compte existe pour cette adresse, un courriel de réinitialisation du mot de passe vient d’être envoyé. Vérifiez aussi vos courriels indésirables au besoin.",
    linkPreview: "Un lien de réinitialisation est prêt.",
  },
};

TEXT.fr.invalidPassword = "Utilisez un mot de passe d’au moins 10 caractères.";
TEXT.fr.invalidCredentials = "Le courriel ou le mot de passe est invalide.";
TEXT.fr.currentPasswordRequired = "Entrez le mot de passe actuel pour le modifier.";
TEXT.fr.currentPasswordInvalid = "Le mot de passe actuel est invalide.";
TEXT.fr.passwordSaved = "Votre mot de passe a été enregistré.";

TEXT.en.invalidToken = "This password reset link is invalid or expired. Request a new reset email from the portal.";
TEXT.en.loginSent = "If an account exists for this address, a password reset email has just been sent. Check your junk folder if needed.";
TEXT.en.linkPreview = "A password reset link is ready.";
TEXT.fr.invalidCode = "Utilisez un code de référence valide.";
TEXT.fr.invalidToken = "Le lien de réinitialisation est invalide ou expiré. Demandez un nouveau courriel de réinitialisation depuis le portail.";
TEXT.fr.loginSent = "Si un compte existe pour cette adresse, un courriel de réinitialisation du mot de passe vient d’être envoyé. Vérifiez aussi vos courriels indésirables au besoin.";
TEXT.fr.linkPreview = "Un lien de réinitialisation est prêt.";

function jsonResponse(payload, status = 200, headers = {}) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

function normalizeLocale(value) {
  return typeof value === "string" && value.toLowerCase().startsWith("fr") ? "fr" : "en";
}

function messageSet(locale) {
  return TEXT[normalizeLocale(locale)];
}

TEXT.fr.oneProgramOnly = "Cette adresse courriel est déjà liée à l'autre programme. Une même adresse ne peut être inscrite qu'à un seul programme.";
TEXT.fr.partnerApplicationPending = "Une demande partenaire existe déjà pour cette adresse. Opticable la révisera et communiquera avec vous.";
TEXT.fr.partnerApplicationSubmitted = "Votre demande partenaire a été transmise. Opticable la révisera et communiquera avec vous.";

TEXT.fr.configUnavailable = "La plateforme de référence n'est pas configurée.";
TEXT.fr.invalidRequest = "Le corps de la requête est invalide.";
TEXT.fr.invalidEmail = "Utilisez une adresse courriel valide.";
TEXT.fr.invalidCode = "Utilisez un code de référence valide.";
TEXT.fr.requiredField = "Remplissez tous les champs obligatoires.";
TEXT.fr.requiredConsent = "Acceptez les conditions du programme avant de continuer.";
TEXT.fr.selfReferral = "Vous ne pouvez pas utiliser votre propre code de référence.";
TEXT.fr.existingLead = "Ce code a déjà été utilisé pour ce contact.";
TEXT.fr.authRequired = "Connectez-vous pour accéder au portail.";
TEXT.fr.invalidToken = "Le lien de réinitialisation est invalide ou expiré. Demandez un nouveau courriel de réinitialisation depuis le portail.";
TEXT.fr.accountUnavailable = "Le compte de référence n'est pas disponible.";
TEXT.fr.genericError = "La demande de référence n'a pas pu être traitée.";
TEXT.fr.oneProgramOnly = "Cette adresse courriel est déjà liée à l'autre programme. Une même adresse ne peut être inscrite qu'à un seul programme.";
TEXT.fr.partnerApplicationPending = "Une demande partenaire existe déjà pour cette adresse. Opticable la révisera et communiquera avec vous.";
TEXT.fr.partnerApplicationSubmitted = "Votre demande partenaire a été transmise. Opticable la révisera et communiquera avec vous.";
TEXT.fr.loginSent = "Si un compte existe pour cette adresse, un courriel de réinitialisation du mot de passe vient d’être envoyé. Vérifiez aussi vos courriels indésirables au besoin.";
TEXT.fr.linkPreview = "Un lien de réinitialisation est prêt.";
TEXT.fr.invalidPassword = "Utilisez un mot de passe d’au moins 10 caractères.";
TEXT.fr.invalidCredentials = "Le courriel ou le mot de passe est invalide.";
TEXT.fr.currentPasswordRequired = "Entrez le mot de passe actuel pour le modifier.";
TEXT.fr.currentPasswordInvalid = "Le mot de passe actuel est invalide.";
TEXT.fr.passwordSaved = "Votre mot de passe a été enregistré.";

function formatMessage(template, replacements = {}) {
  return String(template || "").replace(/\{(\w+)\}/g, (_match, key) => (
    Object.prototype.hasOwnProperty.call(replacements, key) ? String(replacements[key]) : ""
  ));
}

function bodyValue(body, keys, max = 500) {
  for (const key of keys) {
    if (!Object.prototype.hasOwnProperty.call(body || {}, key)) continue;
    const value = body[key];
    if (value == null) continue;
    const trimmed = safeTrim(String(value), max);
    if (trimmed) return trimmed;
  }
  return "";
}

function safeTrim(value, max = 500) {
  if (typeof value !== "string") return "";
  return value.trim().slice(0, max);
}

function normalizeEmail(value) {
  return safeTrim(value, 320).toLowerCase();
}

function normalizeCompany(value) {
  return safeTrim(value, 200).toLowerCase();
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function isValidPassword(value) {
  return typeof value === "string" && value.length >= PASSWORD_MIN_LENGTH;
}

function toNumber(value) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : 0;
}

function toCents(value) {
  const numeric = Number.parseFloat(String(value ?? "").replace(",", "."));
  if (!Number.isFinite(numeric) || numeric < 0) return null;
  return Math.round(numeric * 100);
}

function fromCents(value) {
  return (toNumber(value) / 100).toFixed(2);
}

function parseLimit(value, fallback = 200, maximum = 500) {
  const parsed = Number.parseInt(String(value || ""), 10);
  if (!Number.isFinite(parsed) || parsed < 1) return fallback;
  return Math.min(parsed, maximum);
}

function normalizeCaseStatusInput(value) {
  const normalized = safeTrim(String(value || ""), 80).toLowerCase().replace(/[\s-]+/g, "_");
  const mapping = {
    new: "new",
    lead: "new",
    submitted: "new",
    created: "new",
    quoted: "quoted",
    quote: "quoted",
    quote_sent: "quoted",
    quotecreated: "quoted",
    proposal: "quoted",
    proposal_sent: "quoted",
    won: "accepted",
    accepted: "accepted",
    closed_won: "accepted",
    deal_won: "accepted",
    approved: "accepted",
    awarded: "accepted",
    completed_paid: "completed_paid",
    completedandpaid: "completed_paid",
    "completed_&_paid": "completed_paid",
    completed__paid: "completed_paid",
    invoice_paid: "completed_paid",
    paid: "completed_paid",
    settled: "completed_paid",
    member_paid: "member_paid",
    memberpaid: "member_paid",
    reward_paid: "member_paid",
    payout_paid: "member_paid",
    commission_paid: "member_paid",
    credit_paid: "member_paid",
    void: "void",
    voided: "void",
    cancelled: "void",
    canceled: "void",
    lost: "void",
    closed_lost: "void",
    disqualified: "void",
  };
  return mapping[normalized] || "";
}

function dbReady(env) {
  return Boolean(env.REFERRAL_DB);
}

function previewLinksEnabled(env) {
  return String(env.REFERRAL_DEV_MAGIC_LINKS || "1") !== "0";
}

function referralEmailFrom(env) {
  const configured = safeTrim(env.REFERRAL_EMAIL_FROM || "", 320);
  if (configured) return configured;
  if (env.REFERRAL_RESEND_API_KEY && previewLinksEnabled(env)) {
    return "Opticable <onboarding@resend.dev>";
  }
  return "";
}

function referralEmailReplyTo(env) {
  const configured = safeTrim(env.REFERRAL_EMAIL_REPLY_TO || "", 320);
  if (configured && isValidEmail(configured)) return configured;
  return "info@opticable.ca";
}

function emailDeliveryReady(env) {
  return Boolean(env.REFERRAL_RESEND_API_KEY && referralEmailFrom(env));
}

function referralApplicationReviewTo(env) {
  const configured = safeTrim(env.REFERRAL_APPLICATION_REVIEW_TO || "", 320);
  if (configured && isValidEmail(configured)) return configured;
  return "info@opticable.ca";
}

function magicLinkSubject(locale, purpose) {
  const lang = normalizeLocale(locale);
  if (lang === "fr") {
    if (purpose === "password_setup") return "Configurez votre accès Opticable";
    if (purpose === "password_reset") return "Réinitialisez votre mot de passe Opticable";
    return "Votre lien de connexion Opticable";
  }
  if (purpose === "password_setup") return "Set up your Opticable access";
  if (purpose === "password_reset") return "Reset your Opticable password";
  return "Your Opticable sign-in link";
}

function magicLinkIntroHtml(locale, purpose, name) {
  const safeName = safeTrim(name || "", 160);
  if (normalizeLocale(locale) === "fr") {
    if (purpose === "password_setup") {
      return `<p>Bonjour ${safeName},</p><p>Votre compte Opticable est prêt. Utilisez ce lien pour choisir votre mot de passe et ouvrir votre portail :</p>`;
    }
    if (purpose === "password_reset") {
      return `<p>Bonjour ${safeName},</p><p>Utilisez ce lien pour réinitialiser votre mot de passe Opticable et rouvrir votre portail :</p>`;
    }
    return `<p>Bonjour ${safeName},</p><p>Voici votre lien de connexion au portail de référence Opticable :</p>`;
  }
  if (purpose === "password_setup") {
    return `<p>Hello ${safeName},</p><p>Your Opticable account is ready. Use this link to choose your password and open your portal:</p>`;
  }
  if (purpose === "password_reset") {
    return `<p>Hello ${safeName},</p><p>Use this link to reset your Opticable password and reopen your portal:</p>`;
  }
  return `<p>Hello ${safeName},</p><p>Here is your Opticable referral portal sign-in link:</p>`;
}

function partnerApplicationEmailCopy(locale, application) {
  if (normalizeLocale(locale) === "fr") {
    return {
      subject: `Nouvelle demande partenaire Opticable: ${application.company}`,
      html: `<h1>Nouvelle demande partenaire</h1>
<p><strong>Nom:</strong> ${application.name}</p>
<p><strong>Courriel:</strong> ${application.email}</p>
<p><strong>Téléphone:</strong> ${application.phone || "—"}</p>
<p><strong>Entreprise:</strong> ${application.company}</p>
<p><strong>Site web:</strong> ${application.website || "—"}</p>
<p><strong>Notes:</strong><br>${(application.notes || "—").replace(/\n/g, "<br>")}</p>
<p><strong>ID de demande:</strong> ${application.id}</p>`,
    };
  }
  return {
    subject: `New Opticable referral partner application: ${application.company}`,
    html: `<h1>New referral partner application</h1>
<p><strong>Name:</strong> ${application.name}</p>
<p><strong>Email:</strong> ${application.email}</p>
<p><strong>Phone:</strong> ${application.phone || "—"}</p>
<p><strong>Company:</strong> ${application.company}</p>
<p><strong>Website:</strong> ${application.website || "—"}</p>
<p><strong>Notes:</strong><br>${(application.notes || "—").replace(/\n/g, "<br>")}</p>
<p><strong>Application ID:</strong> ${application.id}</p>`,
  };
}

function sessionSecret(env) {
  return env.REFERRAL_SESSION_SECRET || env.PROMO_SIGNING_SECRET || env.PROMO_TURNSTILE_SECRET || "";
}

async function hashPayload(value) {
  if (!value) return "";
  const buffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(buffer)).map((item) => item.toString(16).padStart(2, "0")).join("");
}

function base64UrlEncodeBytes(bytes) {
  let binary = "";
  for (const item of bytes) binary += String.fromCharCode(item);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function base64UrlDecodeBytes(value) {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "===".slice((normalized.length + 3) % 4);
  const binary = atob(padded);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

async function signHmac(secret, data) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  return base64UrlEncodeBytes(new Uint8Array(signature));
}

function randomToken(byteLength = 24) {
  const values = new Uint8Array(byteLength);
  crypto.getRandomValues(values);
  return base64UrlEncodeBytes(values);
}

async function derivePasswordHash(password, salt) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(String(password || "")),
    { name: "PBKDF2" },
    false,
    ["deriveBits"],
  );
  const bits = await crypto.subtle.deriveBits(
    {
      name: "PBKDF2",
      salt: new TextEncoder().encode(String(salt || "")),
      iterations: PASSWORD_HASH_ITERATIONS,
      hash: "SHA-256",
    },
    key,
    PASSWORD_HASH_LENGTH * 8,
  );
  return base64UrlEncodeBytes(new Uint8Array(bits));
}

async function createPasswordRecord(password) {
  const salt = randomToken(16);
  const hash = await derivePasswordHash(password, salt);
  return { salt, hash };
}

async function verifyPassword(password, salt, expectedHash) {
  if (!password || !salt || !expectedHash) return false;
  const computed = await derivePasswordHash(password, salt);
  return computed === expectedHash;
}

function nowIso() {
  return new Date().toISOString();
}

function contactPath(locale, code = "") {
  const lang = normalizeLocale(locale);
  if (!code) return REFERRAL_CONTACT_PATHS[lang];
  const url = new URL(REFERRAL_CONTACT_PATHS[lang], "https://opticable.ca");
  url.searchParams.set("ref", code);
  return `${url.pathname}${url.search}`;
}

function portalPath(locale) {
  return REFERRAL_PORTAL_PATHS[normalizeLocale(locale)];
}

function accessPath(locale) {
  return REFERRAL_ACCESS_PATHS[normalizeLocale(locale)];
}

function absoluteUrl(request, path) {
  return new URL(path, new URL(request.url).origin).toString();
}

function authNoticeUrl(request, locale, targetPath = "", authState = "") {
  const fallbackPath = safeTrim(targetPath, 240) || portalPath(locale);
  const url = new URL(fallbackPath, new URL(request.url).origin);
  if (authState) url.searchParams.set("auth", authState);
  return url.toString();
}

function sessionCookieHeader(value) {
  const maxAge = referralConfig.sessionDurationDays * 24 * 60 * 60;
  return `${REFERRAL_COOKIE_NAME}=${value}; Max-Age=${maxAge}; Path=/; HttpOnly; Secure; SameSite=Lax`;
}

function clearSessionCookieHeader() {
  return `${REFERRAL_COOKIE_NAME}=; Max-Age=0; Path=/; HttpOnly; Secure; SameSite=Lax`;
}

async function createSessionValue(env, account, extras = {}) {
  const secret = sessionSecret(env);
  const payload = {
    accountId: account.id,
    locale: normalizeLocale(account.locale),
    exp: Date.now() + (referralConfig.sessionDurationDays * 24 * 60 * 60 * 1000),
    ...(extras && typeof extras === "object" ? extras : {}),
  };
  const encoded = base64UrlEncodeBytes(new TextEncoder().encode(JSON.stringify(payload)));
  const signature = await signHmac(secret, encoded);
  return `${encoded}.${signature}`;
}

async function readPortalSession(request, env) {
  const secret = sessionSecret(env);
  if (!secret) return null;
  const cookieHeader = request.headers.get("Cookie") || "";
  const match = cookieHeader.match(new RegExp(`(?:^|; )${REFERRAL_COOKIE_NAME}=([^;]+)`));
  if (!match) return null;
  const [payloadEncoded, signature] = String(match[1]).split(".");
  if (!payloadEncoded || !signature) return null;
  const expected = await signHmac(secret, payloadEncoded);
  if (expected !== signature) return null;
  try {
    const payload = JSON.parse(new TextDecoder().decode(base64UrlDecodeBytes(payloadEncoded)));
    if (!payload || payload.exp < Date.now()) return null;
    return payload;
  } catch {
    return null;
  }
}

function isProtectedReferralAdminPath(pathname) {
  return pathname.startsWith("/en/admin/referrals/")
    || pathname.startsWith("/fr/admin/references/")
    || pathname.startsWith("/api/referrals/admin/");
}

async function recordAuditEvent(env, payload) {
  await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_audit_events (
      account_id, referral_case_id, reward_id, actor_type, actor_label, event_type, metadata_json, created_at
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)`
  ).bind(
    payload.accountId || null,
    payload.caseId || null,
    payload.rewardId || null,
    payload.actorType,
    payload.actorLabel || null,
    payload.eventType,
    payload.metadataJson ? JSON.stringify(payload.metadataJson) : null,
    payload.createdAt || nowIso(),
  ).run();
}

async function findAccountByEmail(env, emailNormalized) {
  return env.REFERRAL_DB.prepare(
    `SELECT
       account.id,
       account.account_type,
       account.status,
       account.locale,
       account.name,
       account.email,
       account.email_normalized,
       account.phone,
       account.company,
       account.company_normalized,
       account.website,
       account.notes,
       account.current_code_id,
       account.wallet_balance_cents,
       account.total_earned_cents,
       account.password_hash,
       account.password_salt,
       account.password_set_at,
       account.last_login_at,
       account.created_at,
       account.updated_at,
       codes.code AS current_code,
       (
         SELECT credit.code
         FROM referral_credit_codes AS credit
         WHERE credit.account_id = account.id AND credit.is_active = 1
         ORDER BY credit.id DESC
         LIMIT 1
       ) AS current_credit_code
     FROM referral_accounts AS account
     LEFT JOIN referral_codes AS codes
       ON codes.id = account.current_code_id
     WHERE account.email_normalized = ?1
     LIMIT 1`
  ).bind(emailNormalized).first();
}

async function findPartnerApplicationByEmail(env, emailNormalized) {
  return env.REFERRAL_DB.prepare(
    `SELECT *
     FROM referral_partner_applications
     WHERE email_normalized = ?1
     ORDER BY id DESC
     LIMIT 1`
  ).bind(emailNormalized).first();
}

async function loadAccountById(env, accountId) {
  return env.REFERRAL_DB.prepare(
    `SELECT
       account.id,
       account.account_type,
       account.status,
       account.locale,
       account.name,
       account.email,
       account.email_normalized,
       account.phone,
       account.company,
       account.company_normalized,
       account.website,
       account.notes,
       account.current_code_id,
       account.wallet_balance_cents,
       account.total_earned_cents,
       account.approved_at,
       account.activated_at,
       account.paused_at,
       account.rejected_at,
       account.password_hash,
       account.password_salt,
       account.password_set_at,
       account.last_login_at,
       account.created_at,
       account.updated_at,
       codes.code AS current_code,
       (
         SELECT credit.code
         FROM referral_credit_codes AS credit
         WHERE credit.account_id = account.id AND credit.is_active = 1
         ORDER BY credit.id DESC
         LIMIT 1
       ) AS current_credit_code
     FROM referral_accounts AS account
     LEFT JOIN referral_codes AS codes
       ON codes.id = account.current_code_id
     WHERE account.id = ?1
     LIMIT 1`
  ).bind(accountId).first();
}

async function ensureAccountCodesIfActive(env, account, now) {
  if (!account || account.status !== "active") return account;
  let changed = false;
  if (!account.current_code) {
    await ensureActiveCode(env, account.id, account.account_type, now);
    changed = true;
  }
  if (!account.current_credit_code) {
    await ensureActiveCreditCode(env, account.id, account.account_type, now);
    changed = true;
  }
  return changed ? loadAccountById(env, account.id) : account;
}

async function ensureActiveCode(env, accountId, accountType, now) {
  const existing = await env.REFERRAL_DB.prepare(
    `SELECT id, code
     FROM referral_codes
     WHERE account_id = ?1 AND is_active = 1
     ORDER BY id DESC
     LIMIT 1`
  ).bind(accountId).first();
  if (existing) {
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_accounts
       SET current_code_id = ?1, updated_at = ?2
       WHERE id = ?3`
    ).bind(existing.id, now, accountId).run();
    return existing;
  }
  const prefix = accountType === "partner" ? (referralConfig.codes.partnerPrefix || "PART") : (referralConfig.codes.clientPrefix || "REF");
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  for (let attempt = 0; attempt < 12; attempt += 1) {
    const bytes = new Uint8Array(referralConfig.codes.randomLength || 6);
    crypto.getRandomValues(bytes);
    const suffix = Array.from(bytes, (item) => alphabet[item % alphabet.length]).join("");
    const code = `${prefix}-${suffix}`;
    const collision = await env.REFERRAL_DB.prepare(
      `SELECT id FROM referral_codes WHERE code = ?1 LIMIT 1`
    ).bind(code).first();
    if (collision) continue;
    const insert = await env.REFERRAL_DB.prepare(
      `INSERT INTO referral_codes (account_id, code, is_active, created_at)
       VALUES (?1, ?2, 1, ?3)`
    ).bind(accountId, code, now).run();
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_accounts
       SET current_code_id = ?1, updated_at = ?2
       WHERE id = ?3`
    ).bind(insert.meta?.last_row_id, now, accountId).run();
    return { id: insert.meta?.last_row_id, code };
  }
  throw new Error("Could not allocate a unique referral code.");
}

async function ensureActiveCreditCode(env, accountId, accountType, now) {
  const normalizedAccountType = accountType === "partner" ? "partner" : "client";
  const existing = await env.REFERRAL_DB.prepare(
    `SELECT id, code
     FROM referral_credit_codes
     WHERE account_id = ?1 AND is_active = 1
     ORDER BY id DESC
     LIMIT 1`
  ).bind(accountId).first();
  if (existing) return existing;
  const prefix = normalizedAccountType === "partner"
    ? (referralConfig.codes.partnerCreditPrefix || "MEMB")
    : (referralConfig.codes.clientCreditPrefix || "CRED");
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  for (let attempt = 0; attempt < 12; attempt += 1) {
    const bytes = new Uint8Array(referralConfig.codes.randomLength || 6);
    crypto.getRandomValues(bytes);
    const suffix = Array.from(bytes, (item) => alphabet[item % alphabet.length]).join("");
    const code = `${prefix}-${suffix}`;
    const collision = await env.REFERRAL_DB.prepare(
      `SELECT id FROM referral_credit_codes WHERE code = ?1 LIMIT 1`
    ).bind(code).first();
    if (collision) continue;
    const insert = await env.REFERRAL_DB.prepare(
      `INSERT INTO referral_credit_codes (account_id, code, is_active, created_at)
       VALUES (?1, ?2, 1, ?3)`
     ).bind(accountId, code, now).run();
    return { id: insert.meta?.last_row_id, code };
  }
  throw new Error("Could not allocate a unique member code.");
}

async function createMagicLink(env, request, account, locale, redirectPath, purpose = "signin") {
  const createdAt = nowIso();
  const token = randomToken(24);
  const tokenHash = await hashPayload(token);
  const expiresAt = new Date(Date.now() + (referralConfig.loginLinkExpiryMinutes * 60 * 1000)).toISOString();
  const normalizedPurpose = purpose === "password_setup" || purpose === "password_reset" ? purpose : "signin";
  await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_login_tokens (
      account_id, token_hash, locale, redirect_path, purpose, expires_at, created_at, created_ip_hash, created_user_agent_hash
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)`
  ).bind(
    account.id,
    tokenHash,
    normalizeLocale(locale),
    redirectPath || portalPath(locale),
    normalizedPurpose,
    expiresAt,
    createdAt,
    await hashPayload(request.headers.get("CF-Connecting-IP") || ""),
    await hashPayload(request.headers.get("User-Agent") || ""),
  ).run();
  const verifyUrl = new URL("/api/referrals/auth/verify", new URL(request.url).origin);
  verifyUrl.searchParams.set("token", token);
  verifyUrl.searchParams.set("lang", normalizeLocale(locale));
  verifyUrl.searchParams.set("next", redirectPath || portalPath(locale));
  const previewLink = verifyUrl.toString();
  const subject = normalizeLocale(locale) === "fr"
    ? (normalizedPurpose === "password_setup"
      ? "Configurez votre accès Opticable"
      : normalizedPurpose === "password_reset"
        ? "Réinitialisez votre mot de passe Opticable"
        : "Votre lien de connexion Opticable")
    : (normalizedPurpose === "password_setup"
      ? "Set up your Opticable access"
      : normalizedPurpose === "password_reset"
        ? "Reset your Opticable password"
        : "Your Opticable sign-in link");
  const introHtml = normalizeLocale(locale) === "fr"
    ? (normalizedPurpose === "password_setup"
      ? `<p>Bonjour ${account.name || ""},</p><p>Votre compte Opticable est prêt. Utilisez ce lien pour choisir votre mot de passe et ouvrir votre portail :</p>`
      : normalizedPurpose === "password_reset"
        ? `<p>Bonjour ${account.name || ""},</p><p>Utilisez ce lien pour réinitialiser votre mot de passe Opticable et rouvrir votre portail :</p>`
        : `<p>Bonjour ${account.name || ""},</p><p>Voici votre lien de connexion au portail de référence Opticable :</p>`)
    : (normalizedPurpose === "password_setup"
      ? `<p>Hello ${account.name || ""},</p><p>Your Opticable account is ready. Use this link to choose your password and open your portal:</p>`
      : normalizedPurpose === "password_reset"
        ? `<p>Hello ${account.name || ""},</p><p>Use this link to reset your Opticable password and reopen your portal:</p>`
        : `<p>Hello ${account.name || ""},</p><p>Here is your Opticable referral portal sign-in link:</p>`);
  const outroHtml = normalizeLocale(locale) === "fr"
    ? `<p>Le lien expire dans ${referralConfig.loginLinkExpiryMinutes} minutes.</p>`
    : `<p>The link expires in ${referralConfig.loginLinkExpiryMinutes} minutes.</p>`;
  const localizedSubject = magicLinkSubject(locale, normalizedPurpose);
  const localizedIntroHtml = magicLinkIntroHtml(locale, normalizedPurpose, account.name);
  let delivery = "preview_link";
  let emailProvider = "";
  let emailProviderMessageId = "";
  let emailProviderError = "";
  if (emailDeliveryReady(env)) {
    const fromAddress = referralEmailFrom(env);
    const replyToAddress = referralEmailReplyTo(env);
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.REFERRAL_RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: fromAddress,
        to: [account.email],
        reply_to: replyToAddress,
        subject: localizedSubject,
        html: `${localizedIntroHtml}<p><a href="${previewLink}">${previewLink}</a></p>${outroHtml}`,
      }),
    });
    emailProvider = "resend";
    let responsePayload = null;
    try {
      responsePayload = await response.json();
    } catch {
      responsePayload = null;
    }
    if (response.ok) {
      delivery = "email";
      emailProviderMessageId = safeTrim(responsePayload?.id || "", 200);
    } else if (!previewLinksEnabled(env)) {
      emailProviderError = safeTrim(
        String(responsePayload?.message || responsePayload?.error || "Portal email delivery failed."),
        500,
      );
      throw new Error(emailProviderError || "Portal email delivery failed.");
    } else {
      emailProviderError = safeTrim(
        String(responsePayload?.message || responsePayload?.error || "Portal email delivery failed."),
        500,
      );
    }
  } else if (!previewLinksEnabled(env)) {
    throw new Error("Portal email delivery is not configured.");
  }
  await recordAuditEvent(env, {
    accountId: account.id,
    actorType: "system",
    actorLabel: "referral-auth",
    eventType: "magic_link_created",
    metadataJson: {
      delivery,
      purpose: normalizedPurpose,
      redirectPath: redirectPath || portalPath(locale),
      emailProvider: emailProvider || null,
      emailProviderMessageId: emailProviderMessageId || null,
      emailProviderError: emailProviderError || null,
      emailFrom: emailProvider ? referralEmailFrom(env) : null,
      emailReplyTo: emailProvider ? referralEmailReplyTo(env) : null,
    },
    createdAt,
  });
  return { delivery, previewLink: delivery === "preview_link" ? previewLink : "" };
}

async function sendPartnerApplicationEmail(env, application) {
  if (!emailDeliveryReady(env)) {
    throw new Error("Partner application email delivery is not configured.");
  }
  const locale = normalizeLocale(application.locale);
  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${env.REFERRAL_RESEND_API_KEY}`,
    },
    body: JSON.stringify({
      from: referralEmailFrom(env),
      to: [referralApplicationReviewTo(env)],
      reply_to: application.email,
      subject: locale === "fr"
        ? `Nouvelle demande partenaire Opticable: ${application.company}`
        : `New Opticable referral partner application: ${application.company}`,
      html: locale === "fr"
        ? `<h1>Nouvelle demande partenaire</h1>
<p><strong>Nom:</strong> ${application.name}</p>
<p><strong>Courriel:</strong> ${application.email}</p>
<p><strong>Téléphone:</strong> ${application.phone || "—"}</p>
<p><strong>Entreprise:</strong> ${application.company}</p>
<p><strong>Site web:</strong> ${application.website || "—"}</p>
<p><strong>Notes:</strong><br>${(application.notes || "—").replace(/\n/g, "<br>")}</p>
<p><strong>ID de demande:</strong> ${application.id}</p>`
        : `<h1>New referral partner application</h1>
<p><strong>Name:</strong> ${application.name}</p>
<p><strong>Email:</strong> ${application.email}</p>
<p><strong>Phone:</strong> ${application.phone || "—"}</p>
<p><strong>Company:</strong> ${application.company}</p>
<p><strong>Website:</strong> ${application.website || "—"}</p>
<p><strong>Notes:</strong><br>${(application.notes || "—").replace(/\n/g, "<br>")}</p>
<p><strong>Application ID:</strong> ${application.id}</p>`,
    }),
  });
  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }
  if (!response.ok) {
    throw new Error(
      safeTrim(String(payload?.message || payload?.error || "Partner application email delivery failed."), 500),
    );
  }
  return {
    provider: "resend",
    messageId: safeTrim(payload?.id || "", 200),
  };
}

function clientDiscountCapCents() {
  return Math.round(referralConfig.clientProgram.discountCapCad * 100);
}

function clientMinimumSubtotalCents() {
  return Math.round(Number(referralConfig.clientProgram.minimumSubtotalCad || 0) * 100);
}

function clientRewardCapCents() {
  return Math.round(referralConfig.clientProgram.creditCapCad * 100);
}

function clientRewardCents(subtotalCents) {
  if (subtotalCents < clientMinimumSubtotalCents()) return 0;
  return Math.min(
    Math.round(subtotalCents * (referralConfig.clientProgram.creditPercent / 100)),
    clientRewardCapCents(),
  );
}

function clientCreditUseCapCents() {
  return clientRewardCapCents();
}

function partnerRewardCents(subtotalCents) {
  const subtotalCad = subtotalCents / 100;
  const minimumEligible = Number(referralConfig.partnerProgram.minimumSubtotalCad || 0);
  if (subtotalCad < minimumEligible) return 0;
  for (const tier of referralConfig.partnerProgram.payoutTiersCad || []) {
    const minimum = Number(tier.minSubtotalCad || 0);
    const maximum = tier.maxSubtotalCad == null ? Number.POSITIVE_INFINITY : Number(tier.maxSubtotalCad);
    if (subtotalCad >= minimum && subtotalCad <= maximum) {
      return Math.round(Number(tier.payoutCad || 0) * 100);
    }
  }
  return 0;
}

function hasManualRewardOverride(caseRow) {
  return caseRow && caseRow.manual_reward_amount_cents != null && caseRow.manual_reward_amount_cents !== "";
}

function computedRewardAmountCents(caseRow) {
  const subtotalCents = toNumber(caseRow?.quoted_subtotal_cents);
  if (!subtotalCents || subtotalCents < 0) return 0;
  return caseRow.account_type === "client"
    ? clientRewardCents(subtotalCents)
    : partnerRewardCents(subtotalCents);
}

function effectiveRewardAmountCents(caseRow) {
  return hasManualRewardOverride(caseRow)
    ? Math.max(0, toNumber(caseRow.manual_reward_amount_cents))
    : computedRewardAmountCents(caseRow);
}

function effectiveRewardNote(caseRow, rewardType) {
  const manualNote = safeTrim(caseRow?.manual_reward_note || "", 500);
  if (manualNote) return manualNote;
  return rewardType === "credit" ? "Referral credit earned" : "Partner payout earned";
}

function rewardLifecycleStatus(caseStatus) {
  const normalized = normalizeCaseStatusInput(caseStatus) || caseStatus;
  if (normalized === "completed_paid") return "earned";
  if (normalized === "member_paid") return "settled";
  return "void";
}

function parseAuditMetadata(metadataJson) {
  if (!metadataJson) return {};
  try {
    return JSON.parse(metadataJson);
  } catch {
    return {};
  }
}

function buildAccountRollup(accountType, caseRows = [], auditRows = []) {
  let openCaseRewardCents = 0;
  let settledRewardCents = 0;
  let openCaseCount = 0;
  let settledCaseCount = 0;
  let availableRewardCents = 0;
  let availableCaseCount = 0;
  for (const row of caseRows || []) {
    if (!row || row.status === "void") continue;
    const normalizedStatus = normalizeCaseStatusInput(row.status) || row.status;
    const amountCents = effectiveRewardAmountCents({
      ...row,
      account_type: row.account_type || accountType,
    });
    if (normalizedStatus === "member_paid") {
      settledRewardCents += amountCents;
      settledCaseCount += 1;
    } else if (normalizedStatus === "completed_paid") {
      availableRewardCents += amountCents;
      availableCaseCount += 1;
    } else {
      openCaseRewardCents += amountCents;
      openCaseCount += 1;
    }
  }
  let manualAdjustmentCents = 0;
  if (accountType === "client") {
    for (const row of auditRows || []) {
      if (row?.event_type !== "client_wallet_adjusted") continue;
      const metadata = parseAuditMetadata(row.metadata_json);
      manualAdjustmentCents += toNumber(metadata.deltaCents);
    }
  }
  return {
    availableRewardCents,
    availableCaseCount,
    openCaseRewardCents,
    settledRewardCents,
    openCaseCount,
    settledCaseCount,
    completedCaseCount: availableCaseCount + settledCaseCount,
    manualAdjustmentCents,
    currentOutstandingCents: availableRewardCents + manualAdjustmentCents,
    totalEarnedCents: availableRewardCents + settledRewardCents + manualAdjustmentCents,
  };
}

async function syncStoredAccountBalance(env, accountId, now = nowIso()) {
  const account = await loadAccountById(env, accountId);
  if (!account) return null;
  const [cases, auditRows] = await Promise.all([
    (await env.REFERRAL_DB.prepare(
      `SELECT account_type, status, quoted_subtotal_cents, manual_reward_amount_cents, reward_amount_cents
       FROM referral_cases
       WHERE account_id = ?1`
    ).bind(accountId).all()).results || [],
    account.account_type === "client"
      ? ((await env.REFERRAL_DB.prepare(
        `SELECT event_type, metadata_json
         FROM referral_audit_events
         WHERE account_id = ?1
           AND event_type = 'client_wallet_adjusted'`
      ).bind(accountId).all()).results || [])
      : [],
  ]);
  const rollup = buildAccountRollup(account.account_type, cases, auditRows);
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts
     SET wallet_balance_cents = ?1,
         total_earned_cents = ?2,
         updated_at = ?3
     WHERE id = ?4`
  ).bind(
    account.account_type === "client" ? rollup.currentOutstandingCents : 0,
    rollup.totalEarnedCents,
    now,
    accountId,
  ).run();
  return rollup;
}

async function findRewardByCaseId(env, caseId) {
  return env.REFERRAL_DB.prepare(
    `SELECT * FROM referral_rewards WHERE referral_case_id = ?1 LIMIT 1`
  ).bind(caseId).first();
}

async function adjustCreditBalance(env, accountId, deltaCents, now) {
  if (!deltaCents) return;
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts
     SET wallet_balance_cents = wallet_balance_cents + ?1,
         total_earned_cents = total_earned_cents + ?1,
         updated_at = ?2
     WHERE id = ?3`
  ).bind(deltaCents, now, accountId).run();
}

async function adjustWalletBalance(env, accountId, deltaCents, now) {
  if (!deltaCents) return;
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts
     SET wallet_balance_cents = wallet_balance_cents + ?1,
         updated_at = ?2
     WHERE id = ?3`
  ).bind(deltaCents, now, accountId).run();
}

async function syncRewardForCaseLifecycle(env, caseRow, now, reason = "status_changed") {
  const rewardType = caseRow.account_type === "client" ? "credit" : "payout";
  const amountCents = effectiveRewardAmountCents(caseRow);
  const rewardNote = effectiveRewardNote(caseRow, rewardType);
  const targetStatus = rewardLifecycleStatus(caseRow.status);
  const existing = await findRewardByCaseId(env, caseRow.id);
  const currentAmountCents = existing ? toNumber(existing.amount_cents) : 0;
  let nextRewardStatus = targetStatus;
  let balanceDelta = 0;

  if (existing) {
    if (targetStatus === "void" && existing.status === "settled") {
      nextRewardStatus = "settled";
    }
    if (rewardType === "credit") {
      if (existing.status === "earned" && nextRewardStatus !== "earned") {
        balanceDelta -= currentAmountCents;
      } else if (existing.status !== "earned" && nextRewardStatus === "earned") {
        balanceDelta += amountCents;
      } else if (existing.status === "earned" && nextRewardStatus === "earned") {
        balanceDelta += amountCents - currentAmountCents;
      }
    }
  }

  if (!existing && targetStatus !== "void" && amountCents > 0) {
    const insert = await env.REFERRAL_DB.prepare(
      `INSERT INTO referral_rewards (
        account_id, referral_case_id, reward_type, status, amount_cents, note, created_at, earned_at, settled_at, updated_at
      ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?7)`
    ).bind(
      caseRow.account_id,
      caseRow.id,
      rewardType,
      targetStatus,
      amountCents,
      rewardNote,
      now,
      targetStatus === "void" ? null : now,
      targetStatus === "settled" ? now : null,
    ).run();
    if (rewardType === "credit" && targetStatus === "earned") {
      await adjustWalletBalance(env, caseRow.account_id, amountCents, now);
    }
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_cases
       SET reward_amount_cents = ?1,
           reward_generated_at = COALESCE(reward_generated_at, ?2),
           updated_at = ?2
       WHERE id = ?3`
    ).bind(amountCents, now, caseRow.id).run();
    await recordAuditEvent(env, {
      accountId: caseRow.account_id,
      caseId: caseRow.id,
      rewardId: insert.meta?.last_row_id || null,
      actorType: "system",
      actorLabel: "reward-engine",
      eventType: "reward_created",
      metadataJson: { rewardType, amountCents, nextStatus: targetStatus },
      createdAt: now,
    });
    await syncStoredAccountBalance(env, caseRow.account_id, now);
    return;
  }

  if (!existing && targetStatus !== "void" && amountCents <= 0) {
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_cases
       SET reward_amount_cents = ?1,
           updated_at = ?2
       WHERE id = ?3`
    ).bind(0, now, caseRow.id).run();
    await syncStoredAccountBalance(env, caseRow.account_id, now);
    return;
  }

  if (existing) {
    if (rewardType === "credit" && balanceDelta !== 0) {
      await adjustWalletBalance(env, caseRow.account_id, balanceDelta, now);
    }
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_rewards
       SET reward_type = ?1,
           status = ?2,
           amount_cents = ?3,
           note = CASE
             WHEN ?4 IS NULL OR ?4 = '' THEN note
             ELSE ?4
           END,
           earned_at = CASE
             WHEN ?2 IN ('earned', 'settled') THEN COALESCE(earned_at, ?5)
             ELSE earned_at
           END,
           settled_at = CASE
             WHEN ?2 = 'settled' THEN COALESCE(settled_at, ?5)
             WHEN ?2 = 'earned' THEN NULL
             ELSE settled_at
           END,
           voided_at = CASE
             WHEN ?2 = 'void' THEN COALESCE(voided_at, ?5)
             ELSE NULL
           END,
           updated_at = ?5
       WHERE id = ?6`
    ).bind(
      rewardType,
      nextRewardStatus,
      amountCents,
      nextRewardStatus === "void" ? `${rewardNote} | Voided: ${reason}` : rewardNote,
      now,
      existing.id,
    ).run();
  }

  await env.REFERRAL_DB.prepare(
    `UPDATE referral_cases
     SET reward_amount_cents = ?1,
         reward_generated_at = CASE
           WHEN ?2 IN ('earned', 'settled') THEN COALESCE(reward_generated_at, ?3)
           ELSE reward_generated_at
         END,
         updated_at = ?3
     WHERE id = ?4`
  ).bind(amountCents, nextRewardStatus, now, caseRow.id).run();
  await syncStoredAccountBalance(env, caseRow.account_id, now);
}

async function loadCaseById(env, caseId) {
  return env.REFERRAL_DB.prepare(
    `SELECT * FROM referral_cases WHERE id = ?1 LIMIT 1`
  ).bind(caseId).first();
}

async function findActiveReferralCode(env, referralCode, accountId = null) {
  if (!referralCode) return null;
  const normalized = String(referralCode || "").trim().toUpperCase();
  if (!normalized) return null;
  const sql = accountId
    ? `SELECT
         codes.id,
         codes.code,
         account.id AS account_id,
         account.account_type,
         account.status,
         account.locale,
         account.email_normalized,
         account.company_normalized
       FROM referral_codes AS codes
       INNER JOIN referral_accounts AS account
         ON account.id = codes.account_id
       WHERE codes.code = ?1
         AND codes.is_active = 1
         AND account.id = ?2
       LIMIT 1`
    : `SELECT
         codes.id,
         codes.code,
         account.id AS account_id,
         account.account_type,
         account.status,
         account.locale,
         account.email_normalized,
         account.company_normalized
       FROM referral_codes AS codes
       INNER JOIN referral_accounts AS account
         ON account.id = codes.account_id
       WHERE codes.code = ?1
         AND codes.is_active = 1
       LIMIT 1`;
  const statement = env.REFERRAL_DB.prepare(sql);
  return accountId
    ? statement.bind(normalized, accountId).first()
    : statement.bind(normalized).first();
}

async function findActiveCaseByAccountAndEmail(env, accountId, emailNormalized) {
  return env.REFERRAL_DB.prepare(
    `SELECT *
     FROM referral_cases
     WHERE account_id = ?1
       AND referred_email_normalized = ?2
       AND status != 'void'
     ORDER BY id DESC
     LIMIT 1`
  ).bind(accountId, emailNormalized).first();
}

async function findActiveCreditCode(env, creditCode) {
  return env.REFERRAL_DB.prepare(
    `SELECT
       codes.id AS credit_code_id,
       codes.code,
       account.id,
       account.account_type,
       account.status,
       account.locale,
       account.name,
       account.email,
       account.email_normalized,
       account.company,
       account.company_normalized,
       account.wallet_balance_cents
     FROM referral_credit_codes AS codes
     INNER JOIN referral_accounts AS account
       ON account.id = codes.account_id
     WHERE codes.code = ?1 AND codes.is_active = 1
     LIMIT 1`
  ).bind(creditCode).first();
}

async function upsertRewardForCompletedCase(env, caseRow, now) {
  const rewardType = caseRow.account_type === "client" ? "credit" : "payout";
  const amountCents = effectiveRewardAmountCents(caseRow);
  const rewardNote = effectiveRewardNote(caseRow, rewardType);
  const existing = await findRewardByCaseId(env, caseRow.id);
  if (!existing) {
    const insert = await env.REFERRAL_DB.prepare(
      `INSERT INTO referral_rewards (
        account_id, referral_case_id, reward_type, status, amount_cents, note, created_at, earned_at, updated_at
      ) VALUES (?1, ?2, ?3, 'earned', ?4, ?5, ?6, ?6, ?6)`
    ).bind(
      caseRow.account_id,
      caseRow.id,
      rewardType,
      amountCents,
      rewardNote,
      now,
    ).run();
    if (rewardType === "credit") {
      await adjustCreditBalance(env, caseRow.account_id, amountCents, now);
    }
    await env.REFERRAL_DB.prepare(
      `UPDATE referral_cases
       SET reward_amount_cents = ?1,
           reward_generated_at = ?2,
           updated_at = ?2
       WHERE id = ?3`
    ).bind(amountCents, now, caseRow.id).run();
    await recordAuditEvent(env, {
      accountId: caseRow.account_id,
      caseId: caseRow.id,
      rewardId: insert.meta?.last_row_id || null,
      actorType: "system",
      actorLabel: "reward-engine",
      eventType: "reward_created",
      metadataJson: { rewardType, amountCents },
      createdAt: now,
    });
    return;
  }
  const delta = amountCents - toNumber(existing.amount_cents);
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_rewards
     SET reward_type = ?1,
         status = CASE WHEN status = 'void' THEN 'earned' ELSE status END,
         amount_cents = ?2,
         voided_at = NULL,
         note = ?3,
         earned_at = COALESCE(earned_at, ?4),
         updated_at = ?4
     WHERE id = ?5`
  ).bind(
    rewardType,
    amountCents,
    rewardNote,
    now,
    existing.id,
  ).run();
  if (rewardType === "credit" && delta !== 0) {
    await adjustCreditBalance(env, caseRow.account_id, existing.status === "void" ? amountCents : delta, now);
  }
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_cases
     SET reward_amount_cents = ?1,
         reward_generated_at = COALESCE(reward_generated_at, ?2),
         updated_at = ?2
     WHERE id = ?3`
  ).bind(amountCents, now, caseRow.id).run();
}

async function voidRewardForCase(env, caseRow, now, reason) {
  const reward = await findRewardByCaseId(env, caseRow.id);
  if (!reward || reward.status === "void") return;
  if (reward.status === "settled") {
    throw new Error("A settled reward cannot be voided automatically.");
  }
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_rewards
     SET status = 'void',
         voided_at = ?1,
         updated_at = ?1,
         note = CASE
           WHEN note IS NULL OR note = '' THEN ?2
           ELSE note || ' | ' || ?2
         END
     WHERE id = ?3`
  ).bind(now, `Voided: ${reason}`, reward.id).run();
  if (reward.reward_type === "credit") {
    await adjustCreditBalance(env, caseRow.account_id, -toNumber(reward.amount_cents), now);
  }
}

async function createOrReuseAccount(request, env, body) {
  const locale = normalizeLocale(body.locale);
  const messages = messageSet(locale);
  const now = nowIso();
  const accountType = "client";
  const name = safeTrim(body.name, 160);
  const email = safeTrim(body.email, 320);
  const emailNormalized = normalizeEmail(email);
  const phone = safeTrim(body.phone, 64) || null;
  const company = safeTrim(body.company, 200) || null;
  const companyNormalized = company ? normalizeCompany(company) : null;
  const website = safeTrim(body.website, 300) || null;
  const notes = safeTrim(body.notes, 1200) || null;
  const password = typeof body.password === "string" ? body.password : "";
  if (!name || !emailNormalized || !isValidEmail(emailNormalized)) {
    return { error: messages.invalidEmail, status: 400 };
  }
  if (!isValidPassword(password)) {
    return { error: messages.invalidPassword, status: 400 };
  }
  if (body.rulesAttestation !== true) {
    return { error: messages.requiredConsent, status: 400 };
  }
  const existingApplication = await findPartnerApplicationByEmail(env, emailNormalized);
  if (existingApplication) {
    return { error: messages.oneProgramOnly, status: 409 };
  }
  const existing = await findAccountByEmail(env, emailNormalized);
  if (existing) {
    if (existing.account_type !== accountType) {
      return { error: messages.oneProgramOnly, status: 409 };
    }
    return { duplicate: true, account: existing };
  }
  const passwordRecord = await createPasswordRecord(password);
  const status = "active";
  const insert = await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_accounts (
      account_type, status, locale, name, email, email_normalized, phone, company, company_normalized,
      website, notes, approved_at, activated_at, password_hash, password_salt, password_set_at, created_at, updated_at
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18)`
  ).bind(
    accountType,
    status,
    locale,
    name,
    email,
    emailNormalized,
    phone,
    company,
    companyNormalized,
    website,
    notes,
    status === "active" ? now : null,
    status === "active" ? now : null,
    passwordRecord.hash,
    passwordRecord.salt,
    now,
    now,
    now,
  ).run();
  const accountId = insert.meta?.last_row_id;
  if (status === "active") {
    await ensureActiveCode(env, accountId, accountType, now);
    await ensureActiveCreditCode(env, accountId, accountType, now);
  }
  await recordAuditEvent(env, {
    accountId,
    actorType: "public",
    actorLabel: "apply-form",
    eventType: accountType === "partner" ? "partner_application_created" : "client_account_created",
    metadataJson: {
      locale,
      status,
      rulesAttestation: true,
      termsVersion: referralConfig.termsVersion,
      privacyVersion: referralConfig.privacyVersion,
    },
    createdAt: now,
  });
  return { duplicate: false, account: await loadAccountById(env, accountId) };
}

async function createPartnerApplication(request, env, body) {
  const locale = normalizeLocale(body.locale);
  const messages = messageSet(locale);
  const now = nowIso();
  const name = safeTrim(body.name, 160);
  const email = safeTrim(body.email, 320);
  const emailNormalized = normalizeEmail(email);
  const phone = safeTrim(body.phone, 64) || null;
  const company = safeTrim(body.company, 200) || null;
  const companyNormalized = company ? normalizeCompany(company) : null;
  const website = safeTrim(body.website, 300) || null;
  const notes = safeTrim(body.notes, 1200) || null;
  if (!name || !emailNormalized || !isValidEmail(emailNormalized)) {
    return { error: messages.invalidEmail, status: 400 };
  }
  if (!company) {
    return { error: messages.requiredField, status: 400 };
  }
  if (body.rulesAttestation !== true) {
    return { error: messages.requiredConsent, status: 400 };
  }
  const existingAccount = await findAccountByEmail(env, emailNormalized);
  if (existingAccount) {
    if (existingAccount.account_type !== "partner") {
      return { error: messages.oneProgramOnly, status: 409 };
    }
    return {
      duplicate: true,
      applicationLike: true,
      message: existingAccount.status === "active" ? messages.loginSent : messages.partnerApplicationPending,
    };
  }
  const existingApplication = await findPartnerApplicationByEmail(env, emailNormalized);
  if (existingApplication) {
    return { duplicate: true, applicationLike: true, message: messages.partnerApplicationPending };
  }
  const insert = await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_partner_applications (
      status, locale, name, email, email_normalized, phone, company, company_normalized,
      website, notes, created_at, updated_at, created_ip_hash, created_user_agent_hash
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?11, ?12, ?13)`
  ).bind(
    "pending",
    locale,
    name,
    email,
    emailNormalized,
    phone,
    company,
    companyNormalized,
    website,
    notes,
    now,
    await hashPayload(request.headers.get("CF-Connecting-IP") || ""),
    await hashPayload(request.headers.get("User-Agent") || ""),
  ).run();
  const applicationId = insert.meta?.last_row_id;
  const application = await findPartnerApplicationByEmail(env, emailNormalized);
  const emailResult = await sendPartnerApplicationEmail(env, application);
  await recordAuditEvent(env, {
    actorType: "public",
    actorLabel: "partner-application",
    eventType: "partner_application_submitted",
    metadataJson: {
      applicationId,
      email,
      company,
      rulesAttestation: true,
      termsVersion: referralConfig.termsVersion,
      privacyVersion: referralConfig.privacyVersion,
      emailProvider: emailResult.provider,
      emailProviderMessageId: emailResult.messageId || null,
    },
    createdAt: now,
  });
  return { duplicate: false, application, message: messages.partnerApplicationSubmitted };
}

async function handleReferralApply(request, env) {
  if (!dbReady(env)) {
    return jsonResponse({ ok: false, error: TEXT.en.configUnavailable }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: TEXT.en.invalidRequest }, 400);
  }
  const locale = normalizeLocale(body.locale);
  const messages = messageSet(locale);
  try {
    const accountType = body.accountType === "partner" ? "partner" : "client";
    if (accountType === "partner") {
      const applicationResult = await createPartnerApplication(request, env, body);
      if (applicationResult.error) {
        return jsonResponse({ ok: false, error: applicationResult.error }, applicationResult.status || 400);
      }
      return jsonResponse({
        ok: true,
        duplicate: Boolean(applicationResult.duplicate),
        message: applicationResult.message || messages.partnerApplicationSubmitted,
        application: applicationResult.application ? {
          id: applicationResult.application.id,
          status: applicationResult.application.status,
          locale: applicationResult.application.locale,
          name: applicationResult.application.name,
          email: applicationResult.application.email,
          company: applicationResult.application.company,
        } : null,
      });
    }
    const accountResult = await createOrReuseAccount(request, env, body);
    if (accountResult.error) {
      return jsonResponse({ ok: false, error: accountResult.error }, accountResult.status || 400);
    }
    if (!accountResult.duplicate) {
      const now = nowIso();
      await env.REFERRAL_DB.prepare(
        `UPDATE referral_accounts SET last_login_at = ?1, updated_at = ?1 WHERE id = ?2`
      ).bind(now, accountResult.account.id).run();
      const sessionValue = await createSessionValue(env, accountResult.account);
      return jsonResponse({
        ok: true,
        duplicate: false,
        portalUrl: portalPath(locale),
        account: {
          id: accountResult.account.id,
          accountType: accountResult.account.account_type,
          status: accountResult.account.status,
          locale: accountResult.account.locale,
          name: accountResult.account.name,
          email: accountResult.account.email,
          code: accountResult.account.current_code || "",
        },
      }, 200, { "Set-Cookie": sessionCookieHeader(sessionValue) });
    }
    const magicLink = await createMagicLink(env, request, accountResult.account, locale, accessPath(locale), "password_reset");
    return jsonResponse({
      ok: true,
      duplicate: true,
      account: {
        id: accountResult.account.id,
        accountType: accountResult.account.account_type,
        status: accountResult.account.status,
        locale: accountResult.account.locale,
        name: accountResult.account.name,
        email: accountResult.account.email,
        code: accountResult.account.current_code || "",
      },
      magicLink: {
        delivery: magicLink.delivery,
        previewLink: magicLink.previewLink || "",
        message: magicLink.delivery === "preview_link" ? messages.linkPreview : messages.loginSent,
      },
    });
  } catch (error) {
    return jsonResponse({ ok: false, error: messages.genericError, detail: String(error?.message || "") }, 500);
  }
}

async function handleReferralRequestLink(request, env) {
  if (!dbReady(env)) {
    return jsonResponse({ ok: false, error: TEXT.en.configUnavailable }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const locale = normalizeLocale(body.locale);
  const messages = messageSet(locale);
  const emailNormalized = normalizeEmail(body.email);
  if (!emailNormalized || !isValidEmail(emailNormalized)) {
    return jsonResponse({ ok: false, error: messages.invalidEmail }, 400);
  }
  const account = await findAccountByEmail(env, emailNormalized);
  if (!account || account.status !== "active") {
    return jsonResponse({ ok: true, message: messages.loginSent, magicLink: { delivery: "none", previewLink: "" } });
  }
  try {
    const resetPath = safeTrim(body.redirectPath, 240) || accessPath(locale);
    const magicLink = await createMagicLink(env, request, account, locale, resetPath, "password_reset");
    return jsonResponse({
      ok: true,
      message: magicLink.delivery === "preview_link" ? messages.linkPreview : messages.loginSent,
      magicLink,
    });
  } catch (error) {
    return jsonResponse({ ok: false, error: messages.genericError, detail: String(error?.message || "") }, 500);
  }
}

async function handleReferralPasswordLogin(request, env) {
  if (!dbReady(env)) {
    return jsonResponse({ ok: false, error: TEXT.en.configUnavailable }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const locale = normalizeLocale(body.locale);
  const messages = messageSet(locale);
  const emailNormalized = normalizeEmail(body.email);
  const password = typeof body.password === "string" ? body.password : "";
  if (!emailNormalized || !isValidEmail(emailNormalized)) {
    return jsonResponse({ ok: false, error: messages.invalidCredentials }, 401);
  }
  const account = await findAccountByEmail(env, emailNormalized);
  if (!account || account.status !== "active" || !account.password_hash || !account.password_salt) {
    return jsonResponse({ ok: false, error: messages.invalidCredentials }, 401);
  }
  const valid = await verifyPassword(password, account.password_salt, account.password_hash);
  if (!valid) {
    return jsonResponse({ ok: false, error: messages.invalidCredentials }, 401);
  }
  const now = nowIso();
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts SET last_login_at = ?1, updated_at = ?1 WHERE id = ?2`
  ).bind(now, account.id).run();
  await recordAuditEvent(env, {
    accountId: account.id,
    actorType: "account",
    actorLabel: account.email,
    eventType: "password_login",
    createdAt: now,
  });
  const sessionValue = await createSessionValue(env, account);
  return jsonResponse({
    ok: true,
    portalUrl: portalPath(locale),
    account: {
      id: account.id,
      accountType: account.account_type,
      status: account.status,
      locale: account.locale,
      name: account.name,
      email: account.email,
    },
  }, 200, { "Set-Cookie": sessionCookieHeader(sessionValue) });
}

async function handleReferralVerify(request, env) {
  if (!dbReady(env)) {
    return new Response("Referral platform is not configured.", { status: 503 });
  }
  const url = new URL(request.url);
  const locale = normalizeLocale(url.searchParams.get("lang"));
  const token = safeTrim(url.searchParams.get("token"), 500);
  const requestedPath = safeTrim(url.searchParams.get("next"), 240) || portalPath(locale);
  if (!token) {
    return new Response(null, { status: 302, headers: { Location: authNoticeUrl(request, locale, requestedPath, "invalid") } });
  }
  const tokenHash = await hashPayload(token);
  const tokenRow = await env.REFERRAL_DB.prepare(
    `SELECT * FROM referral_login_tokens WHERE token_hash = ?1 LIMIT 1`
  ).bind(tokenHash).first();
  if (!tokenRow) {
    return new Response(null, { status: 302, headers: { Location: authNoticeUrl(request, locale, requestedPath, "invalid") } });
  }
  if (tokenRow.used_at) {
    return new Response(null, { status: 302, headers: { Location: authNoticeUrl(request, locale, tokenRow.redirect_path || requestedPath, "used") } });
  }
  if (Date.parse(tokenRow.expires_at) < Date.now()) {
    return new Response(null, { status: 302, headers: { Location: authNoticeUrl(request, locale, tokenRow.redirect_path || requestedPath, "expired") } });
  }
  const account = await loadAccountById(env, tokenRow.account_id);
  if (!account || account.status !== "active") {
    return new Response(null, { status: 302, headers: { Location: authNoticeUrl(request, locale, tokenRow.redirect_path || requestedPath, "invalid") } });
  }
  const now = nowIso();
  await env.REFERRAL_DB.batch([
    env.REFERRAL_DB.prepare(`UPDATE referral_login_tokens SET used_at = ?1 WHERE id = ?2`).bind(now, tokenRow.id),
    env.REFERRAL_DB.prepare(`UPDATE referral_accounts SET last_login_at = ?1, updated_at = ?1 WHERE id = ?2`).bind(now, account.id),
  ]);
  const passwordResetReady = tokenRow.purpose === "password_setup" || tokenRow.purpose === "password_reset";
  const sessionValue = await createSessionValue(env, account, passwordResetReady ? { passwordResetReady: true } : {});
  const redirectPath = safeTrim(tokenRow.redirect_path, 240) || requestedPath || portalPath(locale);
  return new Response(null, {
    status: 302,
    headers: {
      Location: absoluteUrl(request, redirectPath),
      "Set-Cookie": sessionCookieHeader(sessionValue),
    },
  });
}

async function handleReferralLogout(request) {
  const locale = normalizeLocale(new URL(request.url).searchParams.get("lang"));
  return new Response(null, {
    status: 302,
    headers: {
      Location: absoluteUrl(request, portalPath(locale)),
      "Set-Cookie": clearSessionCookieHeader(),
    },
  });
}

async function handleReferralPasswordUpdate(request, env) {
  if (!dbReady(env)) {
    return jsonResponse({ ok: false, error: TEXT.en.configUnavailable }, 503);
  }
  const account = await loadPortalAccount(request, env);
  if (!account) {
    return jsonResponse({ ok: false, error: TEXT.en.authRequired }, 401, { "Set-Cookie": clearSessionCookieHeader() });
  }
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const locale = normalizeLocale(body.locale || account.locale);
  const messages = messageSet(locale);
  const session = await readPortalSession(request, env);
  const passwordResetReady = Boolean(session?.passwordResetReady);
  const currentPassword = typeof body.currentPassword === "string" ? body.currentPassword : "";
  const newPassword = typeof body.newPassword === "string" ? body.newPassword : "";
  if (!isValidPassword(newPassword)) {
    return jsonResponse({ ok: false, error: messages.invalidPassword }, 400);
  }
  if (account.password_hash && account.password_salt && !passwordResetReady) {
    if (!currentPassword) {
      return jsonResponse({ ok: false, error: messages.currentPasswordRequired }, 400);
    }
    const valid = await verifyPassword(currentPassword, account.password_salt, account.password_hash);
    if (!valid) {
      return jsonResponse({ ok: false, error: messages.currentPasswordInvalid }, 401);
    }
  }
  const record = await createPasswordRecord(newPassword);
  const now = nowIso();
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts
     SET password_hash = ?1,
         password_salt = ?2,
         password_set_at = ?3,
         updated_at = ?3
     WHERE id = ?4`
  ).bind(record.hash, record.salt, now, account.id).run();
  await recordAuditEvent(env, {
    accountId: account.id,
    actorType: "account",
    actorLabel: account.email,
    eventType: passwordResetReady ? "password_reset_completed" : (account.password_hash ? "password_changed" : "password_created"),
    createdAt: now,
  });
  const sessionValue = await createSessionValue(env, account);
  return jsonResponse({ ok: true, message: messages.passwordSaved }, 200, { "Set-Cookie": sessionCookieHeader(sessionValue) });
}

async function loadPortalAccount(request, env) {
  const session = await readPortalSession(request, env);
  if (!session?.accountId) return null;
  const account = await loadAccountById(env, session.accountId);
  if (!account || account.status !== "active") return null;
  return account;
}

async function handleReferralPortal(request, env) {
  if (!dbReady(env)) {
    return jsonResponse({ ok: false, error: TEXT.en.configUnavailable }, 503);
  }
  const session = await readPortalSession(request, env);
  let account = await loadPortalAccount(request, env);
  if (!account) {
    return jsonResponse({ ok: false, error: TEXT.en.authRequired }, 401, { "Set-Cookie": clearSessionCookieHeader() });
  }
  account = await ensureAccountCodesIfActive(env, account, nowIso());
  const stats = await env.REFERRAL_DB.prepare(
    `SELECT
       COUNT(*) AS total_referrals,
       SUM(CASE WHEN status IN ('new', 'quoted', 'accepted', 'won') THEN 1 ELSE 0 END) AS open_referrals,
       SUM(CASE WHEN status IN ('completed_paid', 'member_paid') THEN 1 ELSE 0 END) AS completed_referrals,
       SUM(CASE WHEN quoted_subtotal_cents IS NOT NULL THEN quoted_subtotal_cents ELSE 0 END) AS tracked_subtotal_cents
     FROM referral_cases
     WHERE account_id = ?1`
  ).bind(account.id).first();
  const rewards = (await env.REFERRAL_DB.prepare(
    `SELECT id, reward_type, status, amount_cents, note, created_at, earned_at, settled_at
     FROM referral_rewards
     WHERE account_id = ?1
     ORDER BY created_at DESC
     LIMIT 50`
  ).bind(account.id).all()).results || [];
  const clientLedgerAdjustments = account.account_type === "client"
    ? ((await env.REFERRAL_DB.prepare(
      `SELECT id, metadata_json, created_at
       FROM referral_audit_events
       WHERE account_id = ?1
         AND event_type = 'client_wallet_adjusted'
       ORDER BY created_at DESC
       LIMIT 50`
    ).bind(account.id).all()).results || [])
    : [];
  const referrals = (await env.REFERRAL_DB.prepare(
    `SELECT id, status, created_at, completed_paid_at, quoted_subtotal_cents, reward_amount_cents, manual_reward_amount_cents, referred_discount_percent,
            quote_reference, referred_name, referred_company
     FROM referral_cases
     WHERE account_id = ?1
     ORDER BY created_at DESC
     LIMIT 50`
  ).bind(account.id).all()).results || [];
  const rollup = buildAccountRollup(account.account_type, referrals, clientLedgerAdjustments);
  const rewardLedger = account.account_type === "client"
    ? [
      ...rewards.map((row) => ({
        id: row.id,
        status: row.status === "settled"
          ? "credit_settled"
          : (row.status === "void" ? "credit_void" : "credit_earned"),
        amountCad: fromCents(row.amount_cents),
        note: row.note || "",
        createdAt: row.created_at,
        earnedAt: row.earned_at || "",
        settledAt: row.settled_at || "",
      })),
      ...clientLedgerAdjustments.map((row) => {
        let metadata = {};
        try {
          metadata = row.metadata_json ? JSON.parse(row.metadata_json) : {};
        } catch {
          metadata = {};
        }
        return {
          id: `adj-${row.id}`,
          status: "balance_adjusted",
          amountCad: fromCents(metadata.deltaCents || 0),
          note: safeTrim(metadata.note, 500) || "",
          createdAt: row.created_at,
          earnedAt: "",
          settledAt: "",
        };
      }),
    ].sort((a, b) => String(b.createdAt || "").localeCompare(String(a.createdAt || ""))).slice(0, 50)
    : rewards.map((row) => ({
      id: row.id,
      status: row.status,
      amountCad: fromCents(row.amount_cents),
      note: row.note || "",
      createdAt: row.created_at,
      earnedAt: row.earned_at || "",
      settledAt: row.settled_at || "",
    }));
  return jsonResponse({
    ok: true,
    account: {
      id: account.id,
      accountType: account.account_type,
      status: account.status,
      locale: normalizeLocale(account.locale),
      name: account.name,
      email: account.email,
      phone: account.phone || "",
      company: account.company || "",
      website: account.website || "",
      currentCode: account.current_code || "",
      currentCreditCode: account.current_credit_code || "",
      shareLink: account.current_code ? absoluteUrl(request, contactPath(account.locale, account.current_code)) : "",
      hasPassword: Boolean(account.password_hash && account.password_salt),
      passwordResetReady: Boolean(session?.passwordResetReady),
      walletBalanceCad: fromCents(rollup.currentOutstandingCents),
      currentOutstandingCad: fromCents(rollup.currentOutstandingCents),
      totalEarnedCad: fromCents(rollup.totalEarnedCents),
    },
    stats: {
      totalReferrals: toNumber(stats?.total_referrals),
      openReferrals: rollup.openCaseCount,
      completedReferrals: rollup.completedCaseCount,
      trackedSubtotalCad: fromCents(stats?.tracked_subtotal_cents || 0),
      earnedRewardsCad: fromCents(rewards.filter((row) => row.status === "earned" || row.status === "settled").reduce((sum, row) => sum + toNumber(row.amount_cents), 0)),
      pendingPayoutCad: fromCents(rollup.currentOutstandingCents),
      settledPayoutCad: fromCents(rewards.filter((row) => row.reward_type === "payout" && row.status === "settled").reduce((sum, row) => sum + toNumber(row.amount_cents), 0)),
    },
    rewards: rewardLedger,
    referrals: referrals.map((row) => ({
      id: row.id,
      status: row.status,
      createdAt: row.created_at,
      completedPaidAt: row.completed_paid_at || "",
      quotedSubtotalCad: row.quoted_subtotal_cents == null ? "" : fromCents(row.quoted_subtotal_cents),
      rewardAmountCad: fromCents(effectiveRewardAmountCents({ ...row, account_type: account.account_type })),
      referredDiscountPercent: toNumber(row.referred_discount_percent),
      quoteReference: row.quote_reference || "",
      referredName: row.referred_name || "",
      referredCompany: row.referred_company || "",
    })),
  });
}

async function fetchAdminSummary(env) {
  const [accounts, cases, rewards, applications] = await Promise.all([
    env.REFERRAL_DB.prepare(
      `SELECT
         SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_accounts,
         SUM(CASE WHEN account_type = 'client' THEN wallet_balance_cents ELSE 0 END) AS wallet_balance_cents
       FROM referral_accounts`
    ).first(),
    env.REFERRAL_DB.prepare(
      `SELECT
         COUNT(*) AS total_cases,
         SUM(CASE WHEN status IN ('new', 'quoted', 'accepted', 'won') THEN 1 ELSE 0 END) AS open_cases,
         SUM(CASE WHEN status IN ('completed_paid', 'member_paid') THEN 1 ELSE 0 END) AS completed_cases
       FROM referral_cases`
    ).first(),
    env.REFERRAL_DB.prepare(
      `SELECT
         SUM(CASE WHEN reward_type = 'payout' AND status = 'earned' THEN amount_cents ELSE 0 END) AS pending_payout_cents,
         SUM(CASE WHEN reward_type = 'credit' AND status IN ('earned', 'settled') THEN amount_cents ELSE 0 END) AS total_credit_cents,
         SUM(CASE WHEN reward_type = 'payout' AND status IN ('earned', 'settled') THEN amount_cents ELSE 0 END) AS total_payout_cents
       FROM referral_rewards`
    ).first(),
    env.REFERRAL_DB.prepare(
      `SELECT
         SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_applications
       FROM referral_partner_applications`
    ).first(),
  ]);
  return {
    activeAccounts: toNumber(accounts?.active_accounts),
    pendingPartners: toNumber(applications?.pending_applications),
    walletBalanceCad: fromCents(accounts?.wallet_balance_cents || 0),
    totalCases: toNumber(cases?.total_cases),
    openCases: toNumber(cases?.open_cases),
    completedCases: toNumber(cases?.completed_cases),
    pendingPayoutCad: fromCents(rewards?.pending_payout_cents || 0),
    totalCreditCad: fromCents(rewards?.total_credit_cents || 0),
    totalPayoutCad: fromCents(rewards?.total_payout_cents || 0),
  };
}

async function handleReferralAdminSummary(_request, env) {
  return jsonResponse({ ok: true, summary: await fetchAdminSummary(env) });
}

async function handleReferralAdminApplications(request, env) {
  const limit = parseLimit(new URL(request.url).searchParams.get("limit"));
  const result = await env.REFERRAL_DB.prepare(
    `SELECT
       id, status, locale, name, email, phone, company, website, notes, review_note, reviewed_at, created_at
     FROM referral_partner_applications
     ORDER BY created_at DESC, id DESC
     LIMIT ?1`
  ).bind(limit).all();
  return jsonResponse({ ok: true, applications: result.results || [] });
}

async function handleReferralAdminAccounts(request, env) {
  const limit = parseLimit(new URL(request.url).searchParams.get("limit"));
  const accountQuery = `
      SELECT
         account.id, account.account_type, account.status, account.locale, account.name, account.email, account.phone,
         account.company, account.website, account.wallet_balance_cents, account.total_earned_cents, account.approved_at,
         account.activated_at, account.created_at, codes.code AS current_code,
         (
           SELECT COALESCE(SUM(rewards.amount_cents), 0)
           FROM referral_rewards AS rewards
           WHERE rewards.account_id = account.id
             AND rewards.reward_type = 'payout'
             AND rewards.status = 'earned'
         ) AS pending_payout_cents,
         (
           SELECT COALESCE(SUM(rewards.amount_cents), 0)
           FROM referral_rewards AS rewards
           WHERE rewards.account_id = account.id
             AND rewards.reward_type = 'payout'
             AND rewards.status IN ('earned', 'settled')
         ) AS total_payout_cents,
         (
           SELECT credit.code
           FROM referral_credit_codes AS credit
           WHERE credit.account_id = account.id AND credit.is_active = 1
           ORDER BY credit.id DESC
           LIMIT 1
         ) AS current_credit_code
       FROM referral_accounts AS account
       LEFT JOIN referral_codes AS codes
         ON codes.id = account.current_code_id
       ORDER BY account.created_at DESC, account.id DESC
       LIMIT ?1`;
  let result = await env.REFERRAL_DB.prepare(
    accountQuery
  ).bind(limit).all();
  let rows = result.results || [];
  let changed = false;
  for (const account of rows) {
    if (account.status === "active" && (!account.current_code || !account.current_credit_code)) {
      await ensureAccountCodesIfActive(env, account, nowIso());
      changed = true;
    }
  }
  if (changed) {
    result = await env.REFERRAL_DB.prepare(
      accountQuery
    ).bind(limit).all();
  }
  rows = result.results || [];
  const accountIds = rows.map((row) => Number(row.id)).filter((value) => Number.isFinite(value) && value > 0);
  let caseRows = [];
  let auditRows = [];
  if (accountIds.length) {
    const placeholders = accountIds.map((_value, index) => `?${index + 1}`).join(", ");
    caseRows = ((await env.REFERRAL_DB.prepare(
      `SELECT account_id, account_type, status, quoted_subtotal_cents, manual_reward_amount_cents, reward_amount_cents
       FROM referral_cases
       WHERE account_id IN (${placeholders})`
    ).bind(...accountIds).all()).results || []);
    auditRows = ((await env.REFERRAL_DB.prepare(
      `SELECT account_id, event_type, metadata_json
       FROM referral_audit_events
       WHERE account_id IN (${placeholders})
         AND event_type = 'client_wallet_adjusted'`
    ).bind(...accountIds).all()).results || []);
  }
  const casesByAccount = new Map();
  for (const row of caseRows) {
    const key = Number(row.account_id);
    if (!casesByAccount.has(key)) casesByAccount.set(key, []);
    casesByAccount.get(key).push(row);
  }
  const auditByAccount = new Map();
  for (const row of auditRows) {
    const key = Number(row.account_id);
    if (!auditByAccount.has(key)) auditByAccount.set(key, []);
    auditByAccount.get(key).push(row);
  }
  const accounts = rows.map((row) => {
    const rollup = buildAccountRollup(row.account_type, casesByAccount.get(Number(row.id)) || [], auditByAccount.get(Number(row.id)) || []);
    return {
      ...row,
      current_outstanding_cents: rollup.currentOutstandingCents,
      open_case_reward_cents: rollup.openCaseRewardCents,
      settled_reward_cents: rollup.settledRewardCents,
      manual_adjustment_cents: rollup.manualAdjustmentCents,
    };
  });
  return jsonResponse({ ok: true, accounts });
}

async function handleReferralAdminCases(request, env) {
  const limit = parseLimit(new URL(request.url).searchParams.get("limit"));
  const result = await env.REFERRAL_DB.prepare(
    `SELECT
       cases.id, cases.account_id, account.name AS account_name, account.email AS account_email, cases.account_type,
       cases.referral_code, cases.status, cases.locale, cases.referred_name, cases.referred_email, cases.referred_phone,
       cases.referred_company, cases.quote_reference,
       cases.referred_discount_percent, cases.quoted_subtotal_cents,
       cases.reward_amount_cents, cases.created_at, cases.completed_paid_at, rewards.status AS reward_status, rewards.reward_type
     FROM referral_cases AS cases
     INNER JOIN referral_accounts AS account
       ON account.id = cases.account_id
     LEFT JOIN referral_rewards AS rewards
       ON rewards.referral_case_id = cases.id
     ORDER BY cases.created_at DESC, cases.id DESC
     LIMIT ?1`
  ).bind(limit).all();
  return jsonResponse({ ok: true, cases: result.results || [] });
}

async function handleReferralAdminRewards(request, env) {
  const limit = parseLimit(new URL(request.url).searchParams.get("limit"));
  const result = await env.REFERRAL_DB.prepare(
    `SELECT
       rewards.id, rewards.account_id, account.name AS account_name, account.email AS account_email, account.account_type,
       rewards.referral_case_id, rewards.reward_type, rewards.status, rewards.amount_cents, rewards.note,
       rewards.created_at, rewards.earned_at, rewards.settled_at
     FROM referral_rewards AS rewards
     INNER JOIN referral_accounts AS account
       ON account.id = rewards.account_id
     ORDER BY rewards.created_at DESC, rewards.id DESC
     LIMIT ?1`
  ).bind(limit).all();
  return jsonResponse({ ok: true, rewards: result.results || [] });
}

async function createAdminReferralAccount(env, data) {
  const now = nowIso();
  const accountType = data.accountType === "partner" ? "partner" : "client";
  const status = ["active", "paused", "pending", "rejected"].includes(data.status) ? data.status : "active";
  const locale = normalizeLocale(data.locale);
  const name = safeTrim(data.name, 160);
  const email = safeTrim(data.email, 320);
  const emailNormalized = normalizeEmail(email);
  const phone = safeTrim(data.phone, 64) || null;
  const company = safeTrim(data.company, 200) || null;
  const companyNormalized = company ? normalizeCompany(company) : null;
  const website = safeTrim(data.website, 300) || null;
  const notes = safeTrim(data.notes, 1200) || null;
  if (!name || !emailNormalized || !isValidEmail(emailNormalized)) {
    throw new Error("A valid name and email are required.");
  }
  if (accountType === "partner" && !company) {
    throw new Error("A company name is required for partner accounts.");
  }
  const existingAccount = await findAccountByEmail(env, emailNormalized);
  if (existingAccount) {
    throw new Error("An account already exists for this email address.");
  }
  const existingApplication = await findPartnerApplicationByEmail(env, emailNormalized);
  if (existingApplication && accountType !== "partner") {
    throw new Error("This email address is already reserved by the partner program.");
  }
  const password = safeTrim(data.password || "", 200);
  let passwordHash = null;
  let passwordSalt = null;
  let passwordSetAt = null;
  if (password) {
    if (!isValidPassword(password)) {
      throw new Error("The password must contain at least 10 characters.");
    }
    const passwordRecord = await createPasswordRecord(password);
    passwordHash = passwordRecord.hash;
    passwordSalt = passwordRecord.salt;
    passwordSetAt = now;
  }
  const insert = await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_accounts (
      account_type, status, locale, name, email, email_normalized, phone, company, company_normalized,
      website, notes, approved_at, activated_at, password_hash, password_salt, password_set_at, created_at, updated_at
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18)`
  ).bind(
    accountType,
    status,
    locale,
    name,
    email,
    emailNormalized,
    phone,
    company,
    companyNormalized,
    website,
    notes,
    status === "active" ? now : null,
    status === "active" ? now : null,
    passwordHash,
    passwordSalt,
    passwordSetAt,
    now,
    now,
  ).run();
  const accountId = insert.meta?.last_row_id;
  if (status === "active") {
    await ensureActiveCode(env, accountId, accountType, now);
    await ensureActiveCreditCode(env, accountId, accountType, now);
  }
  return loadAccountById(env, accountId);
}

async function buildAccountExportPayload(env, accountId) {
  const account = await ensureAccountCodesIfActive(env, await loadAccountById(env, accountId), nowIso());
  if (!account) return null;
  const [codes, creditCodes, cases, rewards, creditUses, auditEvents, application] = await Promise.all([
    env.REFERRAL_DB.prepare(
      `SELECT id, code, is_active, created_at, deactivated_at
       FROM referral_codes
       WHERE account_id = ?1
       ORDER BY id DESC`
    ).bind(accountId).all(),
    env.REFERRAL_DB.prepare(
      `SELECT id, code, is_active, created_at, deactivated_at
       FROM referral_credit_codes
       WHERE account_id = ?1
       ORDER BY id DESC`
    ).bind(accountId).all(),
    env.REFERRAL_DB.prepare(
      `SELECT *
       FROM referral_cases
       WHERE account_id = ?1
       ORDER BY created_at DESC, id DESC`
    ).bind(accountId).all(),
    env.REFERRAL_DB.prepare(
      `SELECT *
       FROM referral_rewards
       WHERE account_id = ?1
       ORDER BY created_at DESC, id DESC`
    ).bind(accountId).all(),
    env.REFERRAL_DB.prepare(
      `SELECT *
       FROM referral_credit_uses
       WHERE account_id = ?1
       ORDER BY created_at DESC, id DESC`
    ).bind(accountId).all(),
    env.REFERRAL_DB.prepare(
      `SELECT *
       FROM referral_audit_events
       WHERE account_id = ?1
       ORDER BY created_at DESC, id DESC
       LIMIT 500`
    ).bind(accountId).all(),
    findPartnerApplicationByEmail(env, account.email_normalized),
  ]);
  const rollup = buildAccountRollup(account.account_type, cases.results || [], auditEvents.results || []);
  return {
    exportedAt: nowIso(),
    account,
    rollup,
    application: application || null,
    referralCodes: codes.results || [],
    creditCodes: creditCodes.results || [],
    referralCases: cases.results || [],
    rewards: rewards.results || [],
    creditUses: creditUses.results || [],
    auditEvents: auditEvents.results || [],
  };
}

async function handleReferralAdminAccountCreate(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const applicationId = Number.parseInt(String(body.applicationId || ""), 10);
  let sourceApplication = null;
  if (Number.isFinite(applicationId) && applicationId > 0) {
    sourceApplication = await env.REFERRAL_DB.prepare(
      `SELECT *
       FROM referral_partner_applications
       WHERE id = ?1
       LIMIT 1`
    ).bind(applicationId).first();
    if (!sourceApplication) {
      return jsonResponse({ ok: false, error: "Partner application not found." }, 404);
    }
  }
  try {
    const account = await createAdminReferralAccount(env, {
      accountType: sourceApplication ? "partner" : body.accountType,
      status: body.status || "active",
      locale: sourceApplication?.locale || body.locale,
      name: sourceApplication?.name || body.name,
      email: sourceApplication?.email || body.email,
      phone: sourceApplication?.phone || body.phone,
      company: sourceApplication?.company || body.company,
      website: sourceApplication?.website || body.website,
      notes: sourceApplication?.notes || body.notes,
      password: body.password || "",
    });
    const now = nowIso();
    let magicLink = { delivery: "none", previewLink: "" };
    if (body.sendSetupLink !== false && account.status === "active") {
      await env.REFERRAL_DB.prepare(`DELETE FROM referral_login_tokens WHERE account_id = ?1`).bind(account.id).run();
      magicLink = await createMagicLink(env, request, account, account.locale, accessPath(account.locale), "password_setup");
    }
    if (sourceApplication) {
      await env.REFERRAL_DB.prepare(
        `UPDATE referral_partner_applications
         SET status = 'approved',
             reviewed_at = ?1,
             review_note = COALESCE(?2, review_note),
             updated_at = ?1
         WHERE id = ?3`
      ).bind(now, safeTrim(body.reviewNote, 500) || null, sourceApplication.id).run();
    }
    await recordAuditEvent(env, {
      accountId: account.id,
      actorType: "admin",
      actorLabel: "basic-auth",
      eventType: "account_created_by_admin",
      metadataJson: {
        accountType: account.account_type,
        status: account.status,
        applicationId: sourceApplication?.id || null,
        setupLinkDelivery: magicLink.delivery,
      },
      createdAt: now,
    });
    return jsonResponse({
      ok: true,
      account,
      magicLink,
      message: magicLink.delivery === "email"
        ? "Account created and setup email sent."
        : "Account created.",
    });
  } catch (error) {
    return jsonResponse({ ok: false, error: String(error?.message || "Unable to create the account.") }, 400);
  }
}

async function handleReferralAdminAccountResetAccess(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  if (!Number.isFinite(accountId) || accountId < 1) {
    return jsonResponse({ ok: false, error: "Invalid account reset request." }, 400);
  }
  const account = await loadAccountById(env, accountId);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  if (account.status !== "active") {
    return jsonResponse({ ok: false, error: "Only active accounts can receive a reset link." }, 400);
  }
  const now = nowIso();
  await env.REFERRAL_DB.batch([
    env.REFERRAL_DB.prepare(
      `UPDATE referral_accounts
       SET password_hash = NULL,
           password_salt = NULL,
           password_set_at = NULL,
           updated_at = ?1
       WHERE id = ?2`
    ).bind(now, accountId),
    env.REFERRAL_DB.prepare(`DELETE FROM referral_login_tokens WHERE account_id = ?1`).bind(accountId),
  ]);
  const refreshed = await loadAccountById(env, accountId);
  const magicLink = body.sendSetupLink === false
    ? { delivery: "none", previewLink: "" }
    : await createMagicLink(env, request, refreshed, refreshed.locale, accessPath(refreshed.locale), "password_reset");
  await recordAuditEvent(env, {
    accountId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "account_access_reset",
    metadataJson: { setupLinkDelivery: magicLink.delivery },
    createdAt: now,
  });
  return jsonResponse({
    ok: true,
    account: refreshed,
    magicLink,
    message: magicLink.delivery === "email"
      ? "Password reset email sent."
      : "Access reset completed.",
  });
}

async function handleReferralAdminAccountDelete(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  if (!Number.isFinite(accountId) || accountId < 1) {
    return jsonResponse({ ok: false, error: "Invalid account delete request." }, 400);
  }
  const account = await loadAccountById(env, accountId);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  const now = nowIso();
  await recordAuditEvent(env, {
    accountId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "account_deleted",
    metadataJson: { email: account.email, accountType: account.account_type },
    createdAt: now,
  });
  await env.REFERRAL_DB.prepare(`DELETE FROM referral_accounts WHERE id = ?1`).bind(accountId).run();
  return jsonResponse({ ok: true, deletedAccountId: accountId });
}

async function handleReferralAdminApplicationDelete(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const applicationId = Number.parseInt(String(body.applicationId || ""), 10);
  if (!Number.isFinite(applicationId) || applicationId < 1) {
    return jsonResponse({ ok: false, error: "Invalid partner application delete request." }, 400);
  }
  const application = await env.REFERRAL_DB.prepare(
    `SELECT *
     FROM referral_partner_applications
     WHERE id = ?1
     LIMIT 1`
  ).bind(applicationId).first();
  if (!application) {
    return jsonResponse({ ok: false, error: "Partner application not found." }, 404);
  }
  const now = nowIso();
  await recordAuditEvent(env, {
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "partner_application_deleted",
    metadataJson: {
      applicationId,
      email: application.email,
      company: application.company,
      previousStatus: application.status,
    },
    createdAt: now,
  });
  await env.REFERRAL_DB.prepare(`DELETE FROM referral_partner_applications WHERE id = ?1`).bind(applicationId).run();
  return jsonResponse({ ok: true, deletedApplicationId: applicationId });
}

async function handleReferralAdminApplicationStatus(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const applicationId = Number.parseInt(String(body.applicationId || ""), 10);
  const nextStatus = safeTrim(body.status, 40);
  if (!Number.isFinite(applicationId) || applicationId < 1 || !["pending", "reviewed", "approved", "rejected", "void"].includes(nextStatus)) {
    return jsonResponse({ ok: false, error: "Invalid application update request." }, 400);
  }
  const application = await env.REFERRAL_DB.prepare(
    `SELECT *
     FROM referral_partner_applications
     WHERE id = ?1
     LIMIT 1`
  ).bind(applicationId).first();
  if (!application) {
    return jsonResponse({ ok: false, error: "Partner application not found." }, 404);
  }
  const now = nowIso();
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_partner_applications
     SET status = ?1,
         reviewed_at = CASE WHEN ?1 IN ('reviewed', 'approved', 'rejected', 'void') THEN ?2 ELSE reviewed_at END,
         review_note = CASE
           WHEN ?3 IS NULL OR ?3 = '' THEN review_note
           WHEN review_note IS NULL OR review_note = '' THEN ?3
           ELSE review_note || ' | ' || ?3
         END,
         updated_at = ?2
     WHERE id = ?4`
  ).bind(nextStatus, now, safeTrim(body.reviewNote, 500) || null, applicationId).run();
  await recordAuditEvent(env, {
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "partner_application_status_changed",
    metadataJson: {
      applicationId,
      email: application.email,
      previousStatus: application.status,
      nextStatus,
    },
    createdAt: now,
  });
  const updated = await env.REFERRAL_DB.prepare(
    `SELECT *
     FROM referral_partner_applications
     WHERE id = ?1
     LIMIT 1`
  ).bind(applicationId).first();
  return jsonResponse({ ok: true, application: updated });
}

async function handleReferralAdminAccountStatus(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  const nextStatus = safeTrim(body.status, 40);
  if (!Number.isFinite(accountId) || accountId < 1 || !["pending", "active", "paused", "rejected"].includes(nextStatus)) {
    return jsonResponse({ ok: false, error: "Invalid account update request." }, 400);
  }
  const account = await loadAccountById(env, accountId);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  const now = nowIso();
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_accounts
     SET status = ?1,
         approved_at = CASE WHEN ?1 = 'active' THEN COALESCE(approved_at, ?2) ELSE approved_at END,
         activated_at = CASE WHEN ?1 = 'active' THEN COALESCE(activated_at, ?2) ELSE activated_at END,
         paused_at = CASE WHEN ?1 = 'paused' THEN ?2 ELSE paused_at END,
         rejected_at = CASE WHEN ?1 = 'rejected' THEN ?2 ELSE rejected_at END,
         updated_at = ?2
     WHERE id = ?3`
  ).bind(nextStatus, now, accountId).run();
  if (nextStatus === "active") {
    await ensureActiveCode(env, accountId, account.account_type, now);
    await ensureActiveCreditCode(env, accountId, account.account_type, now);
  }
  await recordAuditEvent(env, {
    accountId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "account_status_changed",
    metadataJson: { previousStatus: account.status, nextStatus },
    createdAt: now,
  });
  return jsonResponse({ ok: true, account: await loadAccountById(env, accountId) });
}

async function handleReferralAdminAccountBalanceAdjust(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  const deltaCents = toCents(body.deltaCad);
  const note = safeTrim(body.note, 500) || null;
  if (!Number.isFinite(accountId) || accountId < 1 || !Number.isFinite(deltaCents) || deltaCents === 0) {
    return jsonResponse({ ok: false, error: "Invalid balance adjustment request." }, 400);
  }
  const account = await loadAccountById(env, accountId);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  if (account.account_type !== "client") {
    return jsonResponse({ ok: false, error: "Only client balances can be adjusted from this action." }, 400);
  }
  const [cases, auditEvents] = await Promise.all([
    (await env.REFERRAL_DB.prepare(
      `SELECT account_type, status, quoted_subtotal_cents, manual_reward_amount_cents, reward_amount_cents
       FROM referral_cases
       WHERE account_id = ?1`
    ).bind(accountId).all()).results || [],
    (await env.REFERRAL_DB.prepare(
      `SELECT event_type, metadata_json
       FROM referral_audit_events
       WHERE account_id = ?1
         AND event_type = 'client_wallet_adjusted'`
    ).bind(accountId).all()).results || [],
  ]);
  const currentBalanceCents = buildAccountRollup(account.account_type, cases, auditEvents).currentOutstandingCents;
  const nextBalanceCents = currentBalanceCents + deltaCents;
  if (nextBalanceCents < 0) {
    return jsonResponse({ ok: false, error: "The adjustment would reduce the client balance below zero." }, 400);
  }
  const now = nowIso();
  await adjustWalletBalance(env, accountId, deltaCents, now);
  await recordAuditEvent(env, {
    accountId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "client_wallet_adjusted",
    metadataJson: {
      deltaCents,
      previousBalanceCents: currentBalanceCents,
      nextBalanceCents,
      note,
    },
    createdAt: now,
  });
  await syncStoredAccountBalance(env, accountId, now);
  return jsonResponse({
    ok: true,
    account: await loadAccountById(env, accountId),
    balanceCad: fromCents(nextBalanceCents),
  });
}

async function handleReferralAdminCaseCreate(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  const nextStatus = safeTrim(body.status, 40) || "new";
  const referralCodeInput = safeTrim(body.referralCode, 40).toUpperCase();
  const referredName = safeTrim(body.referredName, 160);
  const referredEmail = safeTrim(body.referredEmail, 320);
  const referredEmailNormalized = normalizeEmail(referredEmail);
  const referredPhone = safeTrim(body.referredPhone, 64) || null;
  const referredCompany = safeTrim(body.referredCompany, 200);
  const referredCompanyNormalized = referredCompany ? normalizeCompany(referredCompany) : null;
  const referredProjectNotes = safeTrim(body.note, 1200) || null;
  const quoteReference = safeTrim(body.quoteReference, 120) || null;
  const subtotalRaw = body.quotedSubtotalCad === undefined || body.quotedSubtotalCad === null ? "" : String(body.quotedSubtotalCad).trim();
  const quotedSubtotalCents = subtotalRaw === "" ? null : toCents(subtotalRaw);
  const manualRewardRaw = body.manualRewardCad === undefined || body.manualRewardCad === null ? "" : String(body.manualRewardCad).trim();
  const manualRewardAmountCents = manualRewardRaw === "" ? null : toCents(manualRewardRaw);
  if (!Number.isFinite(accountId) || accountId < 1 || !referralConfig.cases.allStatuses.includes(nextStatus)) {
    return jsonResponse({ ok: false, error: "Invalid manual referral case request." }, 400);
  }
  if (!referredName || !referredEmailNormalized || !isValidEmail(referredEmailNormalized) || !referredCompany) {
    return jsonResponse({ ok: false, error: "Name, email, and company are required to create a case." }, 400);
  }
  if (subtotalRaw !== "" && (!Number.isFinite(quotedSubtotalCents) || quotedSubtotalCents < 0)) {
    return jsonResponse({ ok: false, error: "Use a valid subtotal." }, 400);
  }
  if (manualRewardRaw !== "" && (!Number.isFinite(manualRewardAmountCents) || manualRewardAmountCents < 0)) {
    return jsonResponse({ ok: false, error: "Use a valid reward amount." }, 400);
  }
  if (nextStatus === "completed_paid" && (!Number.isFinite(quotedSubtotalCents) || quotedSubtotalCents <= 0)) {
    return jsonResponse({ ok: false, error: "A completed and paid project needs a valid subtotal." }, 400);
  }
  const account = await loadAccountById(env, accountId);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  if (account.status !== "active") {
    return jsonResponse({ ok: false, error: "Only active accounts can receive manual projects." }, 400);
  }
  const now = nowIso();
  const refreshedAccount = await ensureAccountCodesIfActive(env, account, now);
  const codeRow = referralCodeInput
    ? await findActiveReferralCode(env, referralCodeInput, refreshedAccount.id)
    : {
        id: refreshedAccount.current_code_id,
        code: refreshedAccount.current_code,
      };
  if (!codeRow?.id || !codeRow?.code) {
    return jsonResponse({ ok: false, error: "Use a valid referral code linked to this account." }, 400);
  }
  const referredDiscountPercent = refreshedAccount.account_type === "client" ? referralConfig.clientProgram.discountPercent : 0;
  const referredDiscountCapCents = refreshedAccount.account_type === "client" ? clientDiscountCapCents() : 0;
  const rewardPolicyType = refreshedAccount.account_type === "client" ? "client_credit" : "partner_fixed";
  const projectedRewardAmountCents = effectiveRewardAmountCents({
    account_type: refreshedAccount.account_type,
    quoted_subtotal_cents: quotedSubtotalCents,
    manual_reward_amount_cents: manualRewardAmountCents,
  });
  const insert = await env.REFERRAL_DB.prepare(
    `INSERT INTO referral_cases (
      account_id, referral_code_id, referral_code, account_type, status, locale, referred_name, referred_email,
      referred_email_normalized, referred_phone, referred_company, referred_company_normalized, referred_project_notes,
      referred_discount_percent, referred_discount_cap_cents, quoted_subtotal_cents, reward_policy_type, reward_amount_cents,
      manual_reward_amount_cents, manual_reward_note, quote_reference, created_at, updated_at, completed_paid_at
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18, ?19, ?20, ?21, ?22, ?22, ?23)`
  ).bind(
    refreshedAccount.id,
    codeRow.id,
    codeRow.code,
    refreshedAccount.account_type,
    nextStatus,
    normalizeLocale(body.locale || refreshedAccount.locale),
    referredName,
    referredEmail,
    referredEmailNormalized,
    referredPhone,
    referredCompany,
    referredCompanyNormalized,
    referredProjectNotes,
    referredDiscountPercent,
    referredDiscountCapCents,
    quotedSubtotalCents,
    rewardPolicyType,
    projectedRewardAmountCents,
    manualRewardAmountCents,
    referredProjectNotes,
    quoteReference,
    now,
    nextStatus === "completed_paid" ? now : null,
  ).run();
  const caseId = insert.meta?.last_row_id || 0;
  let caseRow = await loadCaseById(env, caseId);
  await syncRewardForCaseLifecycle(env, caseRow, now, "case_created");
  caseRow = await loadCaseById(env, caseId);
  await recordAuditEvent(env, {
    accountId: refreshedAccount.id,
    caseId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "referral_case_created_manual",
    metadataJson: {
      accountType: refreshedAccount.account_type,
      referredName,
      referredEmail,
      referredCompany,
      referralCode: codeRow.code,
      quoteReference,
      quotedSubtotalCents,
      manualRewardAmountCents,
      status: nextStatus,
    },
    createdAt: now,
  });
  return jsonResponse({ ok: true, referralCase: caseRow });
}

async function handleReferralAdminCaseRewardAdjust(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const caseId = Number.parseInt(String(body.caseId || ""), 10);
  const clearOverride = body.clearOverride === true;
  const amountRaw = body.amountCad === undefined || body.amountCad === null ? "" : String(body.amountCad).trim();
  const nextAmountCents = clearOverride ? null : toCents(amountRaw);
  const note = safeTrim(body.note, 500) || null;
  if (!Number.isFinite(caseId) || caseId < 1) {
    return jsonResponse({ ok: false, error: "Invalid case reward update request." }, 400);
  }
  if (!clearOverride && (!amountRaw || !Number.isFinite(nextAmountCents) || nextAmountCents < 0)) {
    return jsonResponse({ ok: false, error: "Use a valid project amount." }, 400);
  }
  const caseRow = await loadCaseById(env, caseId);
  if (!caseRow) {
    return jsonResponse({ ok: false, error: "Referral case not found." }, 404);
  }
  const now = nowIso();
  const existingReward = await findRewardByCaseId(env, caseId);
  const currentAmountCents = existingReward
    ? toNumber(existingReward.amount_cents)
    : effectiveRewardAmountCents(caseRow);
  const nextEffectiveAmountCents = clearOverride
    ? computedRewardAmountCents({ ...caseRow, manual_reward_amount_cents: null })
    : nextAmountCents;
  if (caseRow.status === "completed_paid" && caseRow.account_type === "client" && nextEffectiveAmountCents < currentAmountCents) {
    const delta = nextEffectiveAmountCents - currentAmountCents;
    const [cases, auditEvents] = await Promise.all([
      (await env.REFERRAL_DB.prepare(
        `SELECT account_type, status, quoted_subtotal_cents, manual_reward_amount_cents, reward_amount_cents
         FROM referral_cases
         WHERE account_id = ?1`
      ).bind(caseRow.account_id).all()).results || [],
      (await env.REFERRAL_DB.prepare(
        `SELECT event_type, metadata_json
         FROM referral_audit_events
         WHERE account_id = ?1
           AND event_type = 'client_wallet_adjusted'`
      ).bind(caseRow.account_id).all()).results || [],
    ]);
    const currentOutstandingCents = buildAccountRollup(caseRow.account_type, cases, auditEvents).currentOutstandingCents;
    if (currentOutstandingCents + delta < 0) {
      return jsonResponse({ ok: false, error: "This change would reduce the client balance below zero." }, 400);
    }
  }
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_cases
     SET manual_reward_amount_cents = ?1,
         manual_reward_note = ?2,
         reward_amount_cents = ?3,
         updated_at = ?4
     WHERE id = ?5`
  ).bind(
    clearOverride ? null : nextAmountCents,
    note,
    nextEffectiveAmountCents,
    now,
    caseId,
  ).run();
  let updated = await loadCaseById(env, caseId);
  await syncRewardForCaseLifecycle(env, updated, now, "manual_reward_adjusted");
  updated = await loadCaseById(env, caseId);
  await recordAuditEvent(env, {
    accountId: updated.account_id,
    caseId,
    rewardId: existingReward?.id || null,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "referral_case_reward_adjusted",
    metadataJson: {
      previousAmountCents: currentAmountCents,
      nextAmountCents: updated.reward_amount_cents,
      previousStatus: caseRow.status,
      nextStatus: updated.status,
      previousSubtotalCents: caseRow.quoted_subtotal_cents,
      nextSubtotalCents: updated.quoted_subtotal_cents,
      clearOverride,
      note,
    },
    createdAt: now,
  });
  return jsonResponse({ ok: true, referralCase: updated });
}

async function handleReferralAdminCaseUpdate(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const caseId = Number.parseInt(String(body.caseId || ""), 10);
  const accountId = Number.parseInt(String(body.accountId || ""), 10);
  const nextStatus = safeTrim(body.status, 40) || "new";
  const referredName = safeTrim(body.referredName, 160);
  const referredEmail = safeTrim(body.referredEmail, 320);
  const referredEmailNormalized = normalizeEmail(referredEmail);
  const referredPhone = safeTrim(body.referredPhone, 64) || null;
  const referredCompany = safeTrim(body.referredCompany, 200);
  const referredCompanyNormalized = referredCompany ? normalizeCompany(referredCompany) : null;
  const referredProjectNotes = safeTrim(body.note, 1200) || null;
  const quoteReference = safeTrim(body.quoteReference, 120) || null;
  const referralCodeInput = safeTrim(body.referralCode, 40).toUpperCase();
  const subtotalRaw = body.quotedSubtotalCad === undefined || body.quotedSubtotalCad === null ? "" : String(body.quotedSubtotalCad).trim();
  const quotedSubtotalCents = subtotalRaw === "" ? null : toCents(subtotalRaw);
  const manualRewardRaw = body.manualRewardCad === undefined || body.manualRewardCad === null ? "" : String(body.manualRewardCad).trim();
  const manualRewardAmountCents = manualRewardRaw === "" ? null : toCents(manualRewardRaw);
  if (!Number.isFinite(caseId) || caseId < 1 || !referralConfig.cases.allStatuses.includes(nextStatus)) {
    return jsonResponse({ ok: false, error: "Invalid project update request." }, 400);
  }
  if (!referredName || !referredEmailNormalized || !isValidEmail(referredEmailNormalized) || !referredCompany) {
    return jsonResponse({ ok: false, error: "Name, email, and company are required." }, 400);
  }
  if (subtotalRaw !== "" && (!Number.isFinite(quotedSubtotalCents) || quotedSubtotalCents < 0)) {
    return jsonResponse({ ok: false, error: "Use a valid subtotal." }, 400);
  }
  if (manualRewardRaw !== "" && (!Number.isFinite(manualRewardAmountCents) || manualRewardAmountCents < 0)) {
    return jsonResponse({ ok: false, error: "Use a valid credit or commission amount." }, 400);
  }
  if (nextStatus === "completed_paid" && (!Number.isFinite(quotedSubtotalCents) || quotedSubtotalCents <= 0)) {
    return jsonResponse({ ok: false, error: "A completed and paid project needs a valid subtotal." }, 400);
  }
  const caseRow = await loadCaseById(env, caseId);
  if (!caseRow) {
    return jsonResponse({ ok: false, error: "Project not found." }, 404);
  }
  if (Number.isFinite(accountId) && accountId > 0 && caseRow.account_id !== accountId) {
    return jsonResponse({ ok: false, error: "This project does not belong to the selected account." }, 400);
  }
  const account = await loadAccountById(env, caseRow.account_id);
  if (!account) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  const now = nowIso();
  const refreshedAccount = await ensureAccountCodesIfActive(env, account, now);
  const codeRow = referralCodeInput
    ? await findActiveReferralCode(env, referralCodeInput, refreshedAccount.id)
    : await findActiveReferralCode(env, caseRow.referral_code, refreshedAccount.id) || {
        id: refreshedAccount.current_code_id,
        code: refreshedAccount.current_code,
      };
  if (!codeRow?.id || !codeRow?.code) {
    return jsonResponse({ ok: false, error: "Use a valid referral code linked to this account." }, 400);
  }
  const existingReward = await findRewardByCaseId(env, caseId);
  const currentEffectiveAmountCents = existingReward
    ? toNumber(existingReward.amount_cents)
    : effectiveRewardAmountCents(caseRow);
  const projectedCase = {
    ...caseRow,
    account_type: refreshedAccount.account_type,
    status: nextStatus,
    referral_code_id: codeRow.id,
    referral_code: codeRow.code,
    locale: normalizeLocale(body.locale || refreshedAccount.locale),
    referred_name: referredName,
    referred_email: referredEmail,
    referred_email_normalized: referredEmailNormalized,
    referred_phone: referredPhone,
    referred_company: referredCompany,
    referred_company_normalized: referredCompanyNormalized,
    referred_project_notes: referredProjectNotes,
    quote_reference: quoteReference,
    quoted_subtotal_cents: quotedSubtotalCents,
    manual_reward_amount_cents: manualRewardAmountCents,
    manual_reward_note: referredProjectNotes,
  };
  const nextEffectiveAmountCents = effectiveRewardAmountCents(projectedCase);
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_cases
     SET referral_code_id = ?1,
         referral_code = ?2,
         status = ?3,
         locale = ?4,
         referred_name = ?5,
         referred_email = ?6,
         referred_email_normalized = ?7,
         referred_phone = ?8,
         referred_company = ?9,
         referred_company_normalized = ?10,
         referred_project_notes = ?11,
         quote_reference = ?12,
         quoted_subtotal_cents = ?13,
         manual_reward_amount_cents = ?14,
         manual_reward_note = ?15,
         reward_amount_cents = ?16,
         completed_paid_at = CASE WHEN ?3 = 'completed_paid' THEN COALESCE(completed_paid_at, ?17) ELSE completed_paid_at END,
         void_reason = CASE WHEN ?3 = 'void' THEN COALESCE(void_reason, 'voided') ELSE NULL END,
         updated_at = ?17
     WHERE id = ?18`
  ).bind(
    codeRow.id,
    codeRow.code,
    nextStatus,
    projectedCase.locale,
    referredName,
    referredEmail,
    referredEmailNormalized,
    referredPhone,
    referredCompany,
    referredCompanyNormalized,
    referredProjectNotes,
    quoteReference,
    quotedSubtotalCents,
    manualRewardAmountCents,
    referredProjectNotes,
    nextEffectiveAmountCents,
    now,
    caseId,
  ).run();
  let updated = await loadCaseById(env, caseId);
  await syncRewardForCaseLifecycle(env, updated, now, nextStatus === "void" ? "voided" : "status_changed");
  updated = await loadCaseById(env, caseId);
  await recordAuditEvent(env, {
    accountId: updated.account_id,
    caseId,
    rewardId: existingReward?.id || null,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "referral_case_updated_manual",
    metadataJson: {
      previousStatus: caseRow.status,
      nextStatus,
      referredName,
      referredEmail,
      referredCompany,
      referralCode: codeRow.code,
      quoteReference,
      previousSubtotalCents: caseRow.quoted_subtotal_cents,
      nextSubtotalCents: quotedSubtotalCents,
      previousRewardAmountCents: currentEffectiveAmountCents,
      nextRewardAmountCents: updated.reward_amount_cents,
    },
    createdAt: now,
  });
  return jsonResponse({ ok: true, referralCase: updated });
}

async function handleReferralAdminCaseStatus(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const caseId = Number.parseInt(String(body.caseId || ""), 10);
  const nextStatus = safeTrim(body.status, 40);
  if (!Number.isFinite(caseId) || caseId < 1 || !referralConfig.cases.allStatuses.includes(nextStatus)) {
    return jsonResponse({ ok: false, error: "Invalid referral case update request." }, 400);
  }
  const caseRow = await loadCaseById(env, caseId);
  if (!caseRow) {
    return jsonResponse({ ok: false, error: "Referral case not found." }, 404);
  }
  const now = nowIso();
  const subtotalCents = body.quotedSubtotalCad === undefined || body.quotedSubtotalCad === null || body.quotedSubtotalCad === ""
    ? caseRow.quoted_subtotal_cents
    : toCents(body.quotedSubtotalCad);
  if (nextStatus === "completed_paid" && (!Number.isFinite(subtotalCents) || subtotalCents <= 0)) {
    return jsonResponse({ ok: false, error: "A completed and paid referral needs a valid subtotal." }, 400);
  }
  const nextRewardAmountCents = effectiveRewardAmountCents({
    ...caseRow,
    status: nextStatus,
    quoted_subtotal_cents: subtotalCents,
  });
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_cases
     SET status = ?1,
         quote_reference = COALESCE(?2, quote_reference),
         quoted_subtotal_cents = ?3,
         reward_amount_cents = ?6,
         void_reason = CASE WHEN ?1 = 'void' THEN COALESCE(?4, void_reason) ELSE NULL END,
         completed_paid_at = CASE WHEN ?1 = 'completed_paid' THEN COALESCE(completed_paid_at, ?5) ELSE completed_paid_at END,
         updated_at = ?5
     WHERE id = ?7`
  ).bind(
    nextStatus,
    safeTrim(body.quoteReference, 120) || null,
    subtotalCents,
    safeTrim(body.voidReason, 500) || null,
    now,
    nextRewardAmountCents,
    caseId,
  ).run();
  const updated = await loadCaseById(env, caseId);
  await syncRewardForCaseLifecycle(env, updated, now, nextStatus === "void" ? (safeTrim(body.voidReason, 500) || "voided") : "status_changed");
  await recordAuditEvent(env, {
    accountId: updated.account_id,
    caseId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "referral_case_status_changed",
    metadataJson: {
      previousStatus: caseRow.status,
      nextStatus,
      previousSubtotalCents: caseRow.quoted_subtotal_cents,
      nextSubtotalCents: subtotalCents,
      previousRewardAmountCents: caseRow.reward_amount_cents,
      nextRewardAmountCents: updated.reward_amount_cents,
      quotedSubtotalCents: subtotalCents,
    },
    createdAt: now,
  });
  return jsonResponse({ ok: true, referralCase: await loadCaseById(env, caseId) });
}

async function handleReferralAdminCaseDelete(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const caseId = Number.parseInt(String(body.caseId || ""), 10);
  if (!Number.isFinite(caseId) || caseId < 1) {
    return jsonResponse({ ok: false, error: "Invalid referral case delete request." }, 400);
  }
  const caseRow = await loadCaseById(env, caseId);
  if (!caseRow) {
    return jsonResponse({ ok: false, error: "Referral case not found." }, 404);
  }
  const now = nowIso();
  await syncRewardForCaseLifecycle(
    env,
    { ...caseRow, status: "void" },
    now,
    "case_deleted"
  );
  await recordAuditEvent(env, {
    accountId: caseRow.account_id,
    caseId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "referral_case_deleted",
    metadataJson: {
      referralCode: caseRow.referral_code,
      referredName: caseRow.referred_name,
      email: caseRow.referred_email,
      referredCompany: caseRow.referred_company,
      quoteReference: caseRow.quote_reference,
      previousStatus: caseRow.status,
      previousSubtotalCents: caseRow.quoted_subtotal_cents,
      previousRewardAmountCents: caseRow.reward_amount_cents,
    },
    createdAt: now,
  });
  await env.REFERRAL_DB.prepare(`DELETE FROM referral_cases WHERE id = ?1`).bind(caseId).run();
  await syncStoredAccountBalance(env, caseRow.account_id, now);
  return jsonResponse({ ok: true, deletedCaseId: caseId });
}

async function handleReferralAdminRewardSettle(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const rewardId = Number.parseInt(String(body.rewardId || ""), 10);
  if (!Number.isFinite(rewardId) || rewardId < 1) {
    return jsonResponse({ ok: false, error: "Invalid reward settlement request." }, 400);
  }
  const reward = await env.REFERRAL_DB.prepare(`SELECT * FROM referral_rewards WHERE id = ?1 LIMIT 1`).bind(rewardId).first();
  if (!reward) {
    return jsonResponse({ ok: false, error: "Reward not found." }, 404);
  }
  if (reward.reward_type !== "payout") {
    return jsonResponse({ ok: false, error: "Only payout rewards can be settled from this action." }, 400);
  }
  const now = nowIso();
  await env.REFERRAL_DB.prepare(
    `UPDATE referral_rewards
     SET status = 'settled',
         settled_at = COALESCE(settled_at, ?1),
         updated_at = ?1,
         note = CASE
           WHEN ?2 IS NULL OR ?2 = '' THEN note
           WHEN note IS NULL OR note = '' THEN ?2
           ELSE note || ' | ' || ?2
         END
     WHERE id = ?3`
  ).bind(now, safeTrim(body.note, 500) || null, rewardId).run();
  await recordAuditEvent(env, {
    accountId: reward.account_id,
    caseId: reward.referral_case_id,
    rewardId,
    actorType: "admin",
    actorLabel: "basic-auth",
    eventType: "reward_settled",
    metadataJson: { note: safeTrim(body.note, 500) || "" },
    createdAt: now,
  });
  return jsonResponse({ ok: true, rewardId, settledAt: now });
}

async function handleReferralAdminAccountExport(request, env) {
  const accountId = Number.parseInt(String(new URL(request.url).searchParams.get("accountId") || ""), 10);
  if (!Number.isFinite(accountId) || accountId < 1) {
    return jsonResponse({ ok: false, error: "A valid accountId is required." }, 400);
  }
  const payload = await buildAccountExportPayload(env, accountId);
  if (!payload) {
    return jsonResponse({ ok: false, error: "Account not found." }, 404);
  }
  return new Response(JSON.stringify(payload, null, 2), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Content-Disposition": `attachment; filename="opticable-referral-account-${accountId}.json"`,
    },
  });
}

function csvEscape(value) {
  const stringValue = value == null ? "" : String(value);
  return `"${stringValue.replace(/"/g, '""')}"`;
}

async function handleReferralAdminExport(request, env) {
  const kind = safeTrim(new URL(request.url).searchParams.get("kind"), 40) || "cases";
  let headings = [];
  let rows = [];
  if (kind === "accounts") {
    headings = ["id", "account_type", "status", "locale", "name", "email", "phone", "company", "website", "wallet_balance_cents", "total_earned_cents", "approved_at", "activated_at", "created_at"];
    rows = (await env.REFERRAL_DB.prepare(
      `SELECT id, account_type, status, locale, name, email, phone, company, website, wallet_balance_cents, total_earned_cents, approved_at, activated_at, created_at
       FROM referral_accounts
       ORDER BY created_at DESC, id DESC`
    ).all()).results || [];
  } else if (kind === "rewards") {
    headings = ["id", "account_id", "referral_case_id", "reward_type", "status", "amount_cents", "note", "created_at", "earned_at", "settled_at", "voided_at"];
    rows = (await env.REFERRAL_DB.prepare(
      `SELECT id, account_id, referral_case_id, reward_type, status, amount_cents, note, created_at, earned_at, settled_at, voided_at
       FROM referral_rewards
       ORDER BY created_at DESC, id DESC`
    ).all()).results || [];
  } else {
    headings = ["id", "account_id", "referral_code", "account_type", "status", "locale", "referred_name", "referred_email", "referred_phone", "referred_company", "quote_reference", "referred_discount_percent", "quoted_subtotal_cents", "reward_policy_type", "reward_amount_cents", "created_at", "completed_paid_at"];
    rows = (await env.REFERRAL_DB.prepare(
      `SELECT id, account_id, referral_code, account_type, status, locale, referred_name, referred_email, referred_phone, referred_company, quote_reference, referred_discount_percent, quoted_subtotal_cents, reward_policy_type, reward_amount_cents, created_at, completed_paid_at
       FROM referral_cases
       ORDER BY created_at DESC, id DESC`
    ).all()).results || [];
  }
  const lines = [headings.join(",")];
  for (const row of rows) {
    lines.push(headings.map((heading) => csvEscape(row[heading])).join(","));
  }
  const filenameDate = new Date().toISOString().slice(0, 10);
  return new Response(`\ufeff${lines.join("\r\n")}\r\n`, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="opticable-referrals-${kind}-${filenameDate}.csv"`,
    },
  });
}

export async function routeReferralApi(request, env) {
  const pathname = new URL(request.url).pathname;
  if (!pathname.startsWith("/api/referrals/")) {
    return null;
  }
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204 });
  }
  if (pathname === "/api/referrals/apply" && request.method === "POST") return handleReferralApply(request, env);
  if (pathname === "/api/referrals/auth/login" && request.method === "POST") return handleReferralPasswordLogin(request, env);
  if (pathname === "/api/referrals/auth/request-link" && request.method === "POST") return handleReferralRequestLink(request, env);
  if (pathname === "/api/referrals/auth/request-reset" && request.method === "POST") return handleReferralRequestLink(request, env);
  if (pathname === "/api/referrals/auth/verify" && request.method === "GET") return handleReferralVerify(request, env);
  if (pathname === "/api/referrals/auth/logout" && request.method === "GET") return handleReferralLogout(request, env);
  if (pathname === "/api/referrals/auth/password" && request.method === "POST") return handleReferralPasswordUpdate(request, env);
  if (pathname === "/api/referrals/portal" && request.method === "GET") return handleReferralPortal(request, env);
  if (pathname === "/api/referrals/admin/summary" && request.method === "GET") return handleReferralAdminSummary(request, env);
  if (pathname === "/api/referrals/admin/applications" && request.method === "GET") return handleReferralAdminApplications(request, env);
  if (pathname === "/api/referrals/admin/accounts" && request.method === "GET") return handleReferralAdminAccounts(request, env);
  if (pathname === "/api/referrals/admin/cases" && request.method === "GET") return handleReferralAdminCases(request, env);
  if (pathname === "/api/referrals/admin/rewards" && request.method === "GET") return handleReferralAdminRewards(request, env);
  if (pathname === "/api/referrals/admin/account-create" && request.method === "POST") return handleReferralAdminAccountCreate(request, env);
  if (pathname === "/api/referrals/admin/account-reset-access" && request.method === "POST") return handleReferralAdminAccountResetAccess(request, env);
  if (pathname === "/api/referrals/admin/account-delete" && request.method === "POST") return handleReferralAdminAccountDelete(request, env);
  if (pathname === "/api/referrals/admin/application-status" && request.method === "POST") return handleReferralAdminApplicationStatus(request, env);
  if (pathname === "/api/referrals/admin/application-delete" && request.method === "POST") return handleReferralAdminApplicationDelete(request, env);
  if (pathname === "/api/referrals/admin/account-status" && request.method === "POST") return handleReferralAdminAccountStatus(request, env);
  if (pathname === "/api/referrals/admin/account-balance-adjust" && request.method === "POST") return handleReferralAdminAccountBalanceAdjust(request, env);
  if (pathname === "/api/referrals/admin/referral-create" && request.method === "POST") return handleReferralAdminCaseCreate(request, env);
  if (pathname === "/api/referrals/admin/referral-update" && request.method === "POST") return handleReferralAdminCaseUpdate(request, env);
  if (pathname === "/api/referrals/admin/referral-reward-adjust" && request.method === "POST") return handleReferralAdminCaseRewardAdjust(request, env);
  if (pathname === "/api/referrals/admin/referral-status" && request.method === "POST") return handleReferralAdminCaseStatus(request, env);
  if (pathname === "/api/referrals/admin/referral-delete" && request.method === "POST") return handleReferralAdminCaseDelete(request, env);
  if (pathname === "/api/referrals/admin/reward-settle" && request.method === "POST") return handleReferralAdminRewardSettle(request, env);
  if (pathname === "/api/referrals/admin/account-export" && request.method === "GET") return handleReferralAdminAccountExport(request, env);
  if (pathname === "/api/referrals/admin/export.csv" && request.method === "GET") return handleReferralAdminExport(request, env);
  return jsonResponse({ ok: false, error: "Not found." }, 404);
}

export { isProtectedReferralAdminPath };
