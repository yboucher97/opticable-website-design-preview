import promoConfig from './promo-config.json';
import { isProtectedReferralAdminPath, routeReferralApi } from './referral-worker.js';

const APEX_HOST = "opticable.ca";
const WWW_HOST = "www.opticable.ca";
const HSTS_VALUE = "max-age=31536000; includeSubDomains; preload";
const LONG_CACHE = "public, max-age=31536000, immutable";
const HTML_CACHE = "public, max-age=0, must-revalidate";
const API_CACHE = "no-store";
const TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify";
const PROMO_STORAGE_KEY = "opticable-promo-entry";
const TURNSTILE_ACTION = "promo-entry";
const LEGACY_REDIRECTS = new Map([
  ["/fr", "/"],
  ["/fr/", "/"],
  ["/fr/index.html", "/"],
  ["/fr/secteurs", "/fr/clientele/"],
  ["/fr/secteurs/", "/fr/clientele/"],
  ["/fr/secteurs/index.html", "/fr/clientele/"],
  ["/en/blog/why-turning-up-wifi-power-usually-makes-things-worse", "/en/blog/why-more-wifi-power-makes-things-worse/"],
  ["/en/blog/why-turning-up-wifi-power-usually-makes-things-worse/", "/en/blog/why-more-wifi-power-makes-things-worse/"],
  ["/en/blog/why-turning-up-wifi-power-usually-makes-things-worse/index.html", "/en/blog/why-more-wifi-power-makes-things-worse/"],
  ["/fr/blogue/pourquoi-monter-la-puissance-du-wifi-empire-les-choses", "/fr/blogue/pourquoi-plus-de-puissance-wifi-aggrave-le-probleme/"],
  ["/fr/blogue/pourquoi-monter-la-puissance-du-wifi-empire-les-choses/", "/fr/blogue/pourquoi-plus-de-puissance-wifi-aggrave-le-probleme/"],
  ["/fr/blogue/pourquoi-monter-la-puissance-du-wifi-empire-les-choses/index.html", "/fr/blogue/pourquoi-plus-de-puissance-wifi-aggrave-le-probleme/"],
  ["/fr/etudes-de-cas/immeuble-multilocatif", "/fr/etudes-de-cas/immeuble-multilogement/"],
  ["/fr/etudes-de-cas/immeuble-multilocatif/", "/fr/etudes-de-cas/immeuble-multilogement/"],
  ["/fr/etudes-de-cas/immeuble-multilocatif/index.html", "/fr/etudes-de-cas/immeuble-multilogement/"],
  ["/fr/clientele/immeuble-multilocatif", "/fr/clientele/immeuble-multilogement/"],
  ["/fr/clientele/immeuble-multilocatif/", "/fr/clientele/immeuble-multilogement/"],
  ["/fr/clientele/immeuble-multilocatif/index.html", "/fr/clientele/immeuble-multilogement/"],
  ["/fr/prix-intercom-immeuble-multilocatif", "/fr/prix-intercom-immeuble-multilogement/"],
  ["/fr/prix-intercom-immeuble-multilocatif/", "/fr/prix-intercom-immeuble-multilogement/"],
  ["/fr/prix-intercom-immeuble-multilocatif/index.html", "/fr/prix-intercom-immeuble-multilogement/"],
]);

const PROMO_TEXT = {
  en: {
    configUnavailable: "The promo is not configured yet.",
    promoClosed: "The promo is not accepting entries right now.",
    databaseUnavailable: "The promo database is not configured.",
    invalidRequest: "The request body is invalid.",
    invalidEmail: "Use a valid email address.",
    requiredField: "Complete all required fields.",
    requiredConsent: "Confirm the required eligibility and rules checkboxes.",
    invalidSkill: "The skill-testing question answer is invalid.",
    invalidTurnstile: "The security check failed.",
    genericError: "The promo request could not be completed.",
    unsubscribed: "Marketing consent has been withdrawn for this email address.",
  },
  fr: {
    configUnavailable: "La promo n'est pas encore configurée.",
    promoClosed: "La promo n'accepte pas d'entrées pour le moment.",
    databaseUnavailable: "La base de données promo n'est pas configurée.",
    invalidRequest: "Le corps de la requête est invalide.",
    invalidEmail: "Utilisez une adresse courriel valide.",
    requiredField: "Remplissez tous les champs requis.",
    requiredConsent: "Confirmez les cases obligatoires liées à l'admissibilité et au règlement.",
    invalidSkill: "La réponse à la question d'habileté est invalide.",
    invalidTurnstile: "La vérification de sécurité a échoué.",
    genericError: "La demande promo n'a pas pu être complétée.",
    unsubscribed: "Le consentement marketing a été retiré pour cette adresse courriel.",
  },
};

function cacheControlForPath(pathname) {
  if (pathname.startsWith("/api/")) {
    return API_CACHE;
  }
  if (pathname.startsWith("/assets/")) {
    return LONG_CACHE;
  }
  if (pathname === "/site.webmanifest") {
    return "public, max-age=86400";
  }
  if (pathname === "/robots.txt" || pathname === "/sitemap.xml" || pathname === "/ads.txt") {
    return "public, max-age=3600";
  }
  return HTML_CACHE;
}

function withResponseHeaders(response, pathname) {
  const headers = new Headers(response.headers);
  headers.set("Strict-Transport-Security", HSTS_VALUE);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Cache-Control", cacheControlForPath(pathname));
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function jsonResponse(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
  });
}

function normalizeLocale(value) {
  return typeof value === "string" && value.toLowerCase().startsWith("fr") ? "fr" : "en";
}

function messagesFor(locale) {
  return PROMO_TEXT[normalizeLocale(locale)];
}

function campaignWindowOpen(now = new Date()) {
  return now >= new Date(promoConfig.startAt) && now <= new Date(promoConfig.endAt);
}

function hasPromoEnv(env) {
  return Boolean(env.PROMO_DB && env.PROMO_TURNSTILE_SITE_KEY && env.PROMO_TURNSTILE_SECRET);
}

function safeTrim(value, max = 500) {
  if (typeof value !== "string") return "";
  return value.trim().slice(0, max);
}

function normalizeEmail(value) {
  return safeTrim(value, 320).toLowerCase();
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function hashPayload(value) {
  if (!value) return Promise.resolve("");
  return crypto.subtle.digest("SHA-256", new TextEncoder().encode(value)).then((buffer) =>
    Array.from(new Uint8Array(buffer)).map((item) => item.toString(16).padStart(2, "0")).join("")
  );
}

function base64UrlEncodeBytes(bytes) {
  let binary = "";
  for (const item of bytes) {
    binary += String.fromCharCode(item);
  }
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

async function createSkillChallenge(env, locale) {
  const secret = env.PROMO_SIGNING_SECRET || env.PROMO_TURNSTILE_SECRET;
  if (!secret) {
    return null;
  }
  const values = new Uint32Array(2);
  crypto.getRandomValues(values);
  const left = (values[0] % 8) + 2;
  const right = (values[1] % 8) + 2;
  const payload = {
    left,
    right,
    exp: Date.now() + (15 * 60 * 1000),
  };
  const payloadString = base64UrlEncodeBytes(new TextEncoder().encode(JSON.stringify(payload)));
  const signature = await signHmac(secret, payloadString);
  return {
    prompt: locale === "fr" ? `Combien font ${left} + ${right} ?` : `What is ${left} + ${right}?`,
    token: `${payloadString}.${signature}`,
  };
}

async function verifySkillChallenge(env, token, answer, locale) {
  const secret = env.PROMO_SIGNING_SECRET || env.PROMO_TURNSTILE_SECRET;
  if (!secret || !token) {
    return { ok: false };
  }
  const [payloadString, signature] = token.split(".");
  if (!payloadString || !signature) {
    return { ok: false };
  }
  const expected = await signHmac(secret, payloadString);
  if (expected !== signature) {
    return { ok: false };
  }
  let payload;
  try {
    payload = JSON.parse(new TextDecoder().decode(base64UrlDecodeBytes(payloadString)));
  } catch {
    return { ok: false };
  }
  if (!payload || payload.exp < Date.now()) {
    return { ok: false };
  }
  const numericAnswer = Number.parseInt(String(answer), 10);
  if (!Number.isFinite(numericAnswer) || numericAnswer !== payload.left + payload.right) {
    return { ok: false };
  }
  return {
    ok: true,
    question: locale === "fr" ? `Combien font ${payload.left} + ${payload.right} ?` : `What is ${payload.left} + ${payload.right}?`,
  };
}

async function verifyTurnstile(request, env, responseToken) {
  if (!env.PROMO_TURNSTILE_SECRET) {
    return { success: false };
  }
  const body = new URLSearchParams();
  body.set("secret", env.PROMO_TURNSTILE_SECRET);
  body.set("response", responseToken || "");
  const remoteIp = request.headers.get("CF-Connecting-IP");
  if (remoteIp) {
    body.set("remoteip", remoteIp);
  }
  const response = await fetch(TURNSTILE_VERIFY_URL, {
    method: "POST",
    body,
  });
  return response.json();
}

function weightedDiscount() {
  const total = promoConfig.discounts.reduce((sum, item) => sum + item.weight, 0);
  const values = new Uint32Array(1);
  crypto.getRandomValues(values);
  let cursor = (values[0] / 0xffffffff) * total;
  for (const item of promoConfig.discounts) {
    cursor -= item.weight;
    if (cursor <= 0) {
      return item.percent;
    }
  }
  return promoConfig.discounts[promoConfig.discounts.length - 1].percent;
}

function promoExpiryFrom(nowIso) {
  const now = new Date(nowIso);
  now.setUTCDate(now.getUTCDate() + promoConfig.codeValidityDays);
  return now.toISOString();
}

function promoCodeFor(percent) {
  const values = new Uint32Array(2);
  crypto.getRandomValues(values);
  const suffix = values[0].toString(36).slice(-3).toUpperCase() + values[1].toString(36).slice(-3).toUpperCase();
  return `OPT-${percent}-${suffix}`;
}

function entryResult(row) {
  return {
    discountPercent: row.discount_percent,
    discountLabel: `${row.discount_percent}%`,
    promoCode: row.promo_code,
    promoExpiresAt: row.promo_expires_at,
  };
}

function parseAdminScope(value) {
  return value === "all" ? "all" : "current";
}

function parseAdminLimit(value, fallback = 200, maximum = 500) {
  const parsed = Number.parseInt(String(value || ""), 10);
  if (!Number.isFinite(parsed) || parsed < 1) {
    return fallback;
  }
  return Math.min(parsed, maximum);
}

function toNumber(value) {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : 0;
}

function adminCredentials(env) {
  const username = safeTrim(env.PROMO_ADMIN_USERNAME, 120);
  const password = typeof env.PROMO_ADMIN_PASSWORD === "string" ? env.PROMO_ADMIN_PASSWORD : "";
  return username && password ? { username, password } : null;
}

function parseBasicAuthorization(header) {
  if (!header || !header.startsWith("Basic ")) {
    return null;
  }
  try {
    const decoded = atob(header.slice(6));
    const separatorIndex = decoded.indexOf(":");
    if (separatorIndex < 0) {
      return null;
    }
    return {
      username: decoded.slice(0, separatorIndex),
      password: decoded.slice(separatorIndex + 1),
    };
  } catch {
    return null;
  }
}

async function secureStringEqual(left, right) {
  const encoder = new TextEncoder();
  const leftBytes = encoder.encode(String(left));
  const rightBytes = encoder.encode(String(right));
  const length = Math.max(leftBytes.length, rightBytes.length);
  let diff = leftBytes.length ^ rightBytes.length;
  for (let index = 0; index < length; index += 1) {
    diff |= (leftBytes[index] || 0) ^ (rightBytes[index] || 0);
  }
  return diff === 0;
}

function adminChallengeResponse(status = 401, message = "Authentication required.") {
  return new Response(message, {
    status,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "WWW-Authenticate": 'Basic realm="Opticable Promo Admin", charset="UTF-8"',
    },
  });
}

async function requireAdminAuth(request, env) {
  const credentials = adminCredentials(env);
  if (!credentials) {
    return new Response("Promo admin access is not configured.", {
      status: 503,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
      },
    });
  }
  const authorization = parseBasicAuthorization(request.headers.get("Authorization"));
  if (!authorization) {
    return adminChallengeResponse();
  }
  const [usernameOk, passwordOk] = await Promise.all([
    secureStringEqual(authorization.username, credentials.username),
    secureStringEqual(authorization.password, credentials.password),
  ]);
  if (!usernameOk || !passwordOk) {
    return adminChallengeResponse();
  }
  return null;
}

function isProtectedAdminPath(pathname) {
  return pathname.startsWith("/en/admin/")
    || pathname.startsWith("/fr/admin/")
    || pathname.startsWith("/api/promo/admin/")
    || isProtectedReferralAdminPath(pathname);
}

async function fetchPromoAdminSummary(env, scope) {
  const sevenDaysAgo = new Date(Date.now() - (7 * 24 * 60 * 60 * 1000)).toISOString();
  if (scope === "all") {
    return env.PROMO_DB.prepare(
      `SELECT
         COUNT(*) AS total_entries,
         SUM(CASE WHEN marketing_opt_in = 1 AND marketing_opt_out_at IS NULL THEN 1 ELSE 0 END) AS marketing_active,
         SUM(CASE WHEN marketing_opt_out_at IS NOT NULL THEN 1 ELSE 0 END) AS marketing_opt_outs,
         SUM(CASE WHEN created_at >= ?1 THEN 1 ELSE 0 END) AS recent_entries,
         MAX(created_at) AS latest_entry_at
       FROM promo_entries`
    ).bind(sevenDaysAgo).first();
  }
  return env.PROMO_DB.prepare(
    `SELECT
       COUNT(*) AS total_entries,
       SUM(CASE WHEN marketing_opt_in = 1 AND marketing_opt_out_at IS NULL THEN 1 ELSE 0 END) AS marketing_active,
       SUM(CASE WHEN marketing_opt_out_at IS NOT NULL THEN 1 ELSE 0 END) AS marketing_opt_outs,
       SUM(CASE WHEN created_at >= ?2 THEN 1 ELSE 0 END) AS recent_entries,
       MAX(created_at) AS latest_entry_at
     FROM promo_entries
     WHERE campaign_id = ?1`
  ).bind(promoConfig.campaignId, sevenDaysAgo).first();
}

async function fetchPromoAdminEntries(env, scope, limit) {
  const columns = `id, campaign_id, created_at, locale, name, email, phone, company, discount_percent, promo_code,
    promo_expires_at, marketing_opt_in, marketing_opt_in_at, marketing_opt_out_at, status,
    referrer_host, utm_source, utm_medium, utm_campaign`;
  if (scope === "all") {
    return env.PROMO_DB.prepare(
      `SELECT ${columns}
       FROM promo_entries
       ORDER BY created_at DESC
       LIMIT ?1`
    ).bind(limit).all();
  }
  return env.PROMO_DB.prepare(
    `SELECT ${columns}
     FROM promo_entries
     WHERE campaign_id = ?1
     ORDER BY created_at DESC
     LIMIT ?2`
  ).bind(promoConfig.campaignId, limit).all();
}

async function fetchPromoAdminExportRows(env, scope) {
  const columns = `campaign_id, created_at, locale, name, email, phone, company, business_attestation,
    quebec_attestation, rules_version, privacy_version, marketing_opt_in, marketing_opt_in_at,
    marketing_opt_out_at, status, discount_percent, discount_cap_cad, promo_code, promo_expires_at,
    skill_question, result_created_at, landing_path, landing_url, referrer_url, referrer_host,
    utm_source, utm_medium, utm_campaign, utm_content, utm_term, turnstile_hostname`;
  if (scope === "all") {
    return env.PROMO_DB.prepare(
      `SELECT ${columns}
       FROM promo_entries
       ORDER BY created_at DESC`
    ).all();
  }
  return env.PROMO_DB.prepare(
    `SELECT ${columns}
     FROM promo_entries
     WHERE campaign_id = ?1
     ORDER BY created_at DESC`
  ).bind(promoConfig.campaignId).all();
}

async function fetchPromoAdminSubscriberRows(env, scope) {
  const scopeClause = scope === "all" ? "" : "WHERE campaign_id = ?1";
  const statement = env.PROMO_DB.prepare(
    `WITH scoped_entries AS (
       SELECT
         id, campaign_id, locale, name, email, email_normalized, phone, company,
         marketing_opt_in, marketing_opt_in_at, marketing_opt_out_at,
         referrer_host, utm_source, utm_medium, utm_campaign, created_at
       FROM promo_entries
       ${scopeClause}
     ),
     subscriber_emails AS (
       SELECT
         email_normalized,
         MIN(CASE WHEN marketing_opt_in = 1 AND marketing_opt_out_at IS NULL THEN marketing_opt_in_at END) AS first_marketing_opt_in_at,
         MAX(CASE WHEN marketing_opt_in = 1 AND marketing_opt_out_at IS NULL THEN marketing_opt_in_at END) AS latest_marketing_opt_in_at,
         COUNT(DISTINCT campaign_id) AS campaigns_count
       FROM scoped_entries
       GROUP BY email_normalized
       HAVING MAX(CASE WHEN marketing_opt_in = 1 AND marketing_opt_out_at IS NULL THEN 1 ELSE 0 END) = 1
     ),
     ranked_entries AS (
       SELECT
         scoped_entries.*,
         ROW_NUMBER() OVER (
           PARTITION BY scoped_entries.email_normalized
           ORDER BY datetime(scoped_entries.created_at) DESC, scoped_entries.id DESC
         ) AS row_number
       FROM scoped_entries
       INNER JOIN subscriber_emails
         ON subscriber_emails.email_normalized = scoped_entries.email_normalized
     )
     SELECT
       ranked_entries.email,
       ranked_entries.email_normalized,
       ranked_entries.name,
       ranked_entries.phone,
       ranked_entries.company,
       ranked_entries.locale,
       ranked_entries.campaign_id AS latest_campaign_id,
       ranked_entries.created_at AS latest_entry_at,
       subscriber_emails.first_marketing_opt_in_at,
       subscriber_emails.latest_marketing_opt_in_at,
       subscriber_emails.campaigns_count,
       ranked_entries.referrer_host,
       ranked_entries.utm_source,
       ranked_entries.utm_medium,
       ranked_entries.utm_campaign
     FROM ranked_entries
     INNER JOIN subscriber_emails
       ON subscriber_emails.email_normalized = ranked_entries.email_normalized
     WHERE ranked_entries.row_number = 1
     ORDER BY
       datetime(subscriber_emails.latest_marketing_opt_in_at) DESC,
       datetime(ranked_entries.created_at) DESC,
       ranked_entries.email_normalized ASC`
  );
  if (scope === "all") {
    return statement.all();
  }
  return statement.bind(promoConfig.campaignId).all();
}

function parseAdminIds(values) {
  if (!Array.isArray(values)) {
    return [];
  }
  const ids = [];
  const seen = new Set();
  for (const value of values) {
    const parsed = Number.parseInt(String(value), 10);
    if (!Number.isFinite(parsed) || parsed < 1 || seen.has(parsed)) {
      continue;
    }
    seen.add(parsed);
    ids.push(parsed);
    if (ids.length >= 500) {
      break;
    }
  }
  return ids;
}

async function countPromoEntriesForScope(env, scope) {
  if (scope === "all") {
    return env.PROMO_DB.prepare(`SELECT COUNT(*) AS total_entries FROM promo_entries`).first();
  }
  return env.PROMO_DB.prepare(
    `SELECT COUNT(*) AS total_entries
     FROM promo_entries
     WHERE campaign_id = ?1`
  ).bind(promoConfig.campaignId).first();
}

async function fetchPromoEntriesForDeletion(env, scope, ids) {
  if (!ids.length) {
    return [];
  }
  const placeholders = ids.map((_, index) => `?${index + 1}`).join(", ");
  const params = [...ids];
  let sql = `SELECT id, campaign_id, email_normalized FROM promo_entries WHERE id IN (${placeholders})`;
  if (scope === "current") {
    sql += ` AND campaign_id = ?${params.length + 1}`;
    params.push(promoConfig.campaignId);
  }
  const result = await env.PROMO_DB.prepare(sql).bind(...params).all();
  return result.results || [];
}

async function deletePromoEventsForPairs(env, pairs) {
  if (!pairs.length) {
    return 0;
  }
  const statements = pairs.map((pair) =>
    env.PROMO_DB.prepare(
      `DELETE FROM promo_marketing_events
       WHERE campaign_id = ?1 AND email_normalized = ?2`
    ).bind(pair.campaignId, pair.emailNormalized)
  );
  const results = await env.PROMO_DB.batch(statements);
  return results.reduce((sum, item) => sum + toNumber(item?.meta?.changes), 0);
}

async function deletePromoEntriesByIds(env, scope, ids) {
  const rows = await fetchPromoEntriesForDeletion(env, scope, ids);
  if (!rows.length) {
    return { deletedEntries: 0, deletedEvents: 0 };
  }
  const uniquePairs = [];
  const pairKeys = new Set();
  for (const row of rows) {
    const key = `${row.campaign_id}::${row.email_normalized}`;
    if (pairKeys.has(key)) {
      continue;
    }
    pairKeys.add(key);
    uniquePairs.push({ campaignId: row.campaign_id, emailNormalized: row.email_normalized });
  }
  const deletedEvents = await deletePromoEventsForPairs(env, uniquePairs);
  const placeholders = rows.map((_, index) => `?${index + 1}`).join(", ");
  const deleteResult = await env.PROMO_DB.prepare(
    `DELETE FROM promo_entries
     WHERE id IN (${placeholders})`
  ).bind(...rows.map((row) => row.id)).run();
  return {
    deletedEntries: toNumber(deleteResult.meta?.changes),
    deletedEvents,
  };
}

async function deletePromoEntriesForScope(env, scope) {
  if (scope === "all") {
    const countRow = await countPromoEntriesForScope(env, scope);
    const [eventDelete, entryDelete] = await Promise.all([
      env.PROMO_DB.prepare(`DELETE FROM promo_marketing_events`).run(),
      env.PROMO_DB.prepare(`DELETE FROM promo_entries`).run(),
    ]);
    return {
      deletedEntries: toNumber(countRow?.total_entries),
      deletedEvents: toNumber(eventDelete.meta?.changes),
      deletedRowsByQuery: toNumber(entryDelete.meta?.changes),
    };
  }
  const countRow = await countPromoEntriesForScope(env, scope);
  const [eventDelete, entryDelete] = await Promise.all([
    env.PROMO_DB.prepare(
      `DELETE FROM promo_marketing_events
       WHERE campaign_id = ?1`
    ).bind(promoConfig.campaignId).run(),
    env.PROMO_DB.prepare(
      `DELETE FROM promo_entries
       WHERE campaign_id = ?1`
    ).bind(promoConfig.campaignId).run(),
  ]);
  return {
    deletedEntries: toNumber(countRow?.total_entries),
    deletedEvents: toNumber(eventDelete.meta?.changes),
    deletedRowsByQuery: toNumber(entryDelete.meta?.changes),
  };
}

function csvEscape(value) {
  const stringValue = value == null ? "" : String(value);
  return `"${stringValue.replace(/"/g, '""')}"`;
}

function isPromoCodeConflict(error) {
  return String(error?.message || "").includes("promo_entries_campaign_code_idx");
}

function isPromoEmailConflict(error) {
  return String(error?.message || "").includes("promo_entries_campaign_email_idx");
}

async function findExistingPromoEntry(env, emailNormalized) {
  return env.PROMO_DB.prepare(
    `SELECT id, discount_percent, promo_code, promo_expires_at, marketing_opt_in
     FROM promo_entries
     WHERE campaign_id = ?1 AND email_normalized = ?2
     LIMIT 1`
  ).bind(promoConfig.campaignId, emailNormalized).first();
}

function referrerHost(urlString) {
  if (!urlString) return "";
  try {
    return new URL(urlString).hostname;
  } catch {
    return "";
  }
}

async function recordMarketingEvent(env, event) {
  if (!env.PROMO_DB) return;
  await env.PROMO_DB.prepare(
    `INSERT INTO promo_marketing_events (
      campaign_id, email_normalized, locale, event_type, source, created_at, client_ip_hash, user_agent_hash
    ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)`
  ).bind(
    event.campaignId || null,
    event.emailNormalized,
    event.locale || null,
    event.eventType,
    event.source,
    event.createdAt,
    event.clientIpHash || null,
    event.userAgentHash || null,
  ).run();
}

async function handlePromoConfig(request, env) {
  const url = new URL(request.url);
  const locale = normalizeLocale(url.searchParams.get("lang"));
  const challenge = await createSkillChallenge(env, locale);
  return jsonResponse({
    ok: true,
    available: hasPromoEnv(env) && campaignWindowOpen() && Boolean(challenge),
    campaignId: promoConfig.campaignId,
    campaignName: promoConfig.campaignName[locale],
    startsAt: promoConfig.startAt,
    endsAt: promoConfig.endAt,
    turnstileSiteKey: env.PROMO_TURNSTILE_SITE_KEY || "",
    turnstileAction: TURNSTILE_ACTION,
    challenge,
  });
}

async function handlePromoEntry(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: PROMO_TEXT.en.invalidRequest }, 400);
  }
  const locale = normalizeLocale(body.locale);
  const text = messagesFor(locale);
  if (!hasPromoEnv(env)) {
    return jsonResponse({ ok: false, error: text.configUnavailable }, 503);
  }
  if (!campaignWindowOpen()) {
    return jsonResponse({ ok: false, error: text.promoClosed }, 409);
  }
  const name = safeTrim(body.name, 160);
  const email = safeTrim(body.email, 320);
  const emailNormalized = normalizeEmail(body.email);
  const phone = safeTrim(body.phone, 64) || null;
  const company = safeTrim(body.company, 200) || null;
  if (!name || !emailNormalized || !isValidEmail(emailNormalized)) {
    return jsonResponse({ ok: false, error: text.invalidEmail }, 400);
  }
  if (!body.quebecAttestation || !body.rulesAttestation) {
    return jsonResponse({ ok: false, error: text.requiredConsent }, 400);
  }
  const skill = await verifySkillChallenge(env, safeTrim(body.skillToken, 500), safeTrim(body.skillAnswer, 20), locale);
  if (!skill.ok) {
    return jsonResponse({ ok: false, error: text.invalidSkill }, 400);
  }
  const turnstile = await verifyTurnstile(request, env, safeTrim(body.turnstileToken, 2048));
  if (!turnstile.success) {
    return jsonResponse({ ok: false, error: text.invalidTurnstile }, 400);
  }
  const nowIso = new Date().toISOString();
  const landingPath = safeTrim(body.landingPath, 300) || null;
  const landingUrl = safeTrim(body.landingUrl, 1000) || null;
  const referrerUrl = safeTrim(body.referrerUrl, 1000) || null;
  const clientIpHash = await hashPayload(request.headers.get("CF-Connecting-IP") || "");
  const userAgentHash = await hashPayload(request.headers.get("User-Agent") || "");
  let existing = await findExistingPromoEntry(env, emailNormalized);
  if (existing) {
    if (body.marketingOptIn && !existing.marketing_opt_in) {
      await env.PROMO_DB.prepare(
        `UPDATE promo_entries
         SET marketing_opt_in = 1,
             marketing_opt_in_at = COALESCE(marketing_opt_in_at, ?1),
             marketing_opt_out_at = NULL,
             updated_at = ?2
         WHERE id = ?3`
      ).bind(nowIso, nowIso, existing.id).run();
      await recordMarketingEvent(env, {
        campaignId: promoConfig.campaignId,
        emailNormalized,
        locale,
        eventType: "opt_in",
        source: "duplicate_entry",
        createdAt: nowIso,
        clientIpHash,
        userAgentHash,
      });
    }
    return jsonResponse({
      ok: true,
      duplicate: true,
      campaignId: promoConfig.campaignId,
      entry: entryResult(existing),
    });
  }
  const discountPercent = weightedDiscount();
  const promoExpiresAt = promoExpiryFrom(nowIso);
  let inserted = false;
  let promoCode = "";
  for (let attempt = 0; attempt < 5 && !inserted; attempt += 1) {
    promoCode = promoCodeFor(discountPercent);
    try {
      await env.PROMO_DB.prepare(
        `INSERT INTO promo_entries (
          campaign_id, locale, name, email, email_normalized, phone, company,
          business_attestation, quebec_attestation, rules_version, privacy_version,
          marketing_opt_in, marketing_opt_in_at, discount_percent, discount_cap_cad,
          promo_code, promo_expires_at, skill_question, result_created_at, landing_path,
          landing_url, referrer_url, referrer_host, utm_source, utm_medium, utm_campaign,
          utm_content, utm_term, turnstile_hostname, client_ip_hash, user_agent_hash,
          created_at, updated_at
        ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18, ?19, ?20, ?21, ?22, ?23, ?24, ?25, ?26, ?27, ?28, ?29, ?30, ?31, ?32, ?33)`
      ).bind(
        promoConfig.campaignId,
        locale,
        name,
        email,
        emailNormalized,
        phone,
        company,
        0,
        body.quebecAttestation ? 1 : 0,
        promoConfig.rulesVersion,
        promoConfig.privacyVersion,
        body.marketingOptIn ? 1 : 0,
        body.marketingOptIn ? nowIso : null,
        discountPercent,
        promoConfig.discountCapCad,
        promoCode,
        promoExpiresAt,
        skill.question,
        nowIso,
        landingPath,
        landingUrl,
        referrerUrl,
        referrerHost(referrerUrl),
        safeTrim(body.utmSource, 160) || null,
        safeTrim(body.utmMedium, 160) || null,
        safeTrim(body.utmCampaign, 160) || null,
        safeTrim(body.utmContent, 160) || null,
        safeTrim(body.utmTerm, 160) || null,
        safeTrim(turnstile.hostname || "", 255) || null,
        clientIpHash || null,
        userAgentHash || null,
        nowIso,
        nowIso,
      ).run();
      inserted = true;
    } catch (error) {
      if (isPromoEmailConflict(error)) {
        existing = await findExistingPromoEntry(env, emailNormalized);
        if (existing) {
          if (body.marketingOptIn && !existing.marketing_opt_in) {
            await env.PROMO_DB.prepare(
              `UPDATE promo_entries
               SET marketing_opt_in = 1,
                   marketing_opt_in_at = COALESCE(marketing_opt_in_at, ?1),
                   marketing_opt_out_at = NULL,
                   updated_at = ?2
               WHERE id = ?3`
            ).bind(nowIso, nowIso, existing.id).run();
            await recordMarketingEvent(env, {
              campaignId: promoConfig.campaignId,
              emailNormalized,
              locale,
              eventType: "opt_in",
              source: "duplicate_entry_race",
              createdAt: nowIso,
              clientIpHash,
              userAgentHash,
            });
          }
          return jsonResponse({
            ok: true,
            duplicate: true,
            campaignId: promoConfig.campaignId,
            entry: entryResult(existing),
          });
        }
      }
      if (!isPromoCodeConflict(error)) {
        throw error;
      }
    }
  }
  if (!inserted) {
    return jsonResponse({ ok: false, error: text.genericError }, 500);
  }
  if (body.marketingOptIn) {
    await recordMarketingEvent(env, {
      campaignId: promoConfig.campaignId,
      emailNormalized,
      locale,
      eventType: "opt_in",
      source: "entry_form",
      createdAt: nowIso,
      clientIpHash,
      userAgentHash,
    });
  }
  return jsonResponse({
    ok: true,
    duplicate: false,
    campaignId: promoConfig.campaignId,
    entry: {
      discountPercent,
      discountLabel: `${discountPercent}%`,
      promoCode,
      promoExpiresAt,
    },
  });
}

async function handlePromoUnsubscribe(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const locale = normalizeLocale(body.locale);
  const text = messagesFor(locale);
  if (!env.PROMO_DB) {
    return jsonResponse({ ok: false, error: text.databaseUnavailable }, 503);
  }
  const emailNormalized = normalizeEmail(body.email);
  if (!emailNormalized || !isValidEmail(emailNormalized)) {
    return jsonResponse({ ok: false, error: text.invalidEmail }, 400);
  }
  const nowIso = new Date().toISOString();
  const clientIpHash = await hashPayload(request.headers.get("CF-Connecting-IP") || "");
  const userAgentHash = await hashPayload(request.headers.get("User-Agent") || "");
  await env.PROMO_DB.prepare(
    `UPDATE promo_entries
     SET marketing_opt_in = 0,
         marketing_opt_out_at = ?1,
         updated_at = ?2
     WHERE email_normalized = ?3`
  ).bind(nowIso, nowIso, emailNormalized).run();
  await recordMarketingEvent(env, {
    campaignId: promoConfig.campaignId,
    emailNormalized,
    locale,
    eventType: "opt_out",
    source: "unsubscribe_form",
    createdAt: nowIso,
    clientIpHash,
    userAgentHash,
  });
  return jsonResponse({
    ok: true,
    message: text.unsubscribed,
  });
}

async function handleSiteConfig(_request, env) {
  return jsonResponse({
    ok: true,
    analyticsToken: env.PROMO_WEB_ANALYTICS_TOKEN || "",
    promoStorageKey: PROMO_STORAGE_KEY,
  });
}

async function handlePromoAdminEntries(request, env) {
  if (!env.PROMO_DB) {
    return jsonResponse({ ok: false, error: "The promo database is not configured." }, 503);
  }
  const url = new URL(request.url);
  const locale = normalizeLocale(url.searchParams.get("lang"));
  const scope = parseAdminScope(url.searchParams.get("scope"));
  const limit = parseAdminLimit(url.searchParams.get("limit"));
  const [summaryRow, entryRows] = await Promise.all([
    fetchPromoAdminSummary(env, scope),
    fetchPromoAdminEntries(env, scope, limit),
  ]);
  return jsonResponse({
    ok: true,
    locale,
    scope,
    limit,
    campaign: {
      currentId: promoConfig.campaignId,
      currentName: promoConfig.campaignName[locale],
      startsAt: promoConfig.startAt,
      endsAt: promoConfig.endAt,
    },
    summary: {
      totalEntries: toNumber(summaryRow?.total_entries),
      marketingActive: toNumber(summaryRow?.marketing_active),
      marketingOptOuts: toNumber(summaryRow?.marketing_opt_outs),
      recentEntries: toNumber(summaryRow?.recent_entries),
      latestEntryAt: summaryRow?.latest_entry_at || "",
    },
    entries: entryRows.results || [],
  });
}

async function handlePromoAdminExport(request, env) {
  if (!env.PROMO_DB) {
    return new Response("The promo database is not configured.", {
      status: 503,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
  const url = new URL(request.url);
  const scope = parseAdminScope(url.searchParams.get("scope"));
  const exportRows = await fetchPromoAdminExportRows(env, scope);
  const filenameDate = new Date().toISOString().slice(0, 10);
  const filenameScope = scope === "all" ? "all-campaigns" : promoConfig.campaignId;
  const headings = [
    "campaign_id",
    "created_at",
    "locale",
    "name",
    "email",
    "phone",
    "company",
    "business_attestation",
    "quebec_attestation",
    "rules_version",
    "privacy_version",
    "marketing_opt_in",
    "marketing_opt_in_at",
    "marketing_opt_out_at",
    "status",
    "discount_percent",
    "discount_cap_cad",
    "promo_code",
    "promo_expires_at",
    "skill_question",
    "result_created_at",
    "landing_path",
    "landing_url",
    "referrer_url",
    "referrer_host",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "turnstile_hostname",
  ];
  const lines = [headings.join(",")];
  for (const row of exportRows.results || []) {
    lines.push(headings.map((heading) => csvEscape(row[heading])).join(","));
  }
  return new Response(`\ufeff${lines.join("\r\n")}\r\n`, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="opticable-promo-entries-${filenameScope}-${filenameDate}.csv"`,
    },
  });
}

async function handlePromoAdminSubscribersExport(request, env) {
  if (!env.PROMO_DB) {
    return new Response("The promo database is not configured.", {
      status: 503,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
  const url = new URL(request.url);
  const scope = parseAdminScope(url.searchParams.get("scope"));
  const exportRows = await fetchPromoAdminSubscriberRows(env, scope);
  const filenameDate = new Date().toISOString().slice(0, 10);
  const filenameScope = scope === "all" ? "all-campaigns" : promoConfig.campaignId;
  const headings = [
    "email",
    "email_normalized",
    "name",
    "phone",
    "company",
    "locale",
    "latest_campaign_id",
    "latest_entry_at",
    "first_marketing_opt_in_at",
    "latest_marketing_opt_in_at",
    "campaigns_count",
    "referrer_host",
    "utm_source",
    "utm_medium",
    "utm_campaign",
  ];
  const lines = [headings.join(",")];
  for (const row of exportRows.results || []) {
    lines.push(headings.map((heading) => csvEscape(row[heading])).join(","));
  }
  return new Response(`\ufeff${lines.join("\r\n")}\r\n`, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="opticable-promo-subscribers-${filenameScope}-${filenameDate}.csv"`,
    },
  });
}

async function handlePromoAdminDelete(request, env) {
  if (!env.PROMO_DB) {
    return jsonResponse({ ok: false, error: "The promo database is not configured." }, 503);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    body = {};
  }
  const mode = body.mode === "all" ? "all" : "selected";
  const scope = parseAdminScope(body.scope);
  if (mode === "all") {
    const result = await deletePromoEntriesForScope(env, scope);
    return jsonResponse({
      ok: true,
      mode,
      scope,
      deletedEntries: result.deletedEntries,
      deletedEvents: result.deletedEvents,
    });
  }
  const ids = parseAdminIds(body.ids);
  if (!ids.length) {
    return jsonResponse({ ok: false, error: "No promo entries were selected." }, 400);
  }
  const result = await deletePromoEntriesByIds(env, scope, ids);
  return jsonResponse({
    ok: true,
    mode,
    scope,
    deletedEntries: result.deletedEntries,
    deletedEvents: result.deletedEvents,
  });
}

async function routeApi(request, env) {
  const url = new URL(request.url);
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204 });
  }
  const referralResponse = await routeReferralApi(request, env);
  if (referralResponse) {
    return referralResponse;
  }
  if (url.pathname === "/api/promo/config" && request.method === "GET") {
    return handlePromoConfig(request, env);
  }
  if (url.pathname === "/api/promo/entry" && request.method === "POST") {
    return handlePromoEntry(request, env);
  }
  if (url.pathname === "/api/promo/unsubscribe" && request.method === "POST") {
    return handlePromoUnsubscribe(request, env);
  }
  if (url.pathname === "/api/promo/admin/entries" && request.method === "GET") {
    return handlePromoAdminEntries(request, env);
  }
  if (url.pathname === "/api/promo/admin/export.csv" && request.method === "GET") {
    return handlePromoAdminExport(request, env);
  }
  if (url.pathname === "/api/promo/admin/subscribers.csv" && request.method === "GET") {
    return handlePromoAdminSubscribersExport(request, env);
  }
  if (url.pathname === "/api/promo/admin/delete" && request.method === "POST") {
    return handlePromoAdminDelete(request, env);
  }
  if (url.pathname === "/api/site-config" && request.method === "GET") {
    return handleSiteConfig(request, env);
  }
  return jsonResponse({ ok: false, error: "Not found." }, 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const redirectUrl = new URL(url);
    let shouldRedirect = false;

    if (redirectUrl.hostname === WWW_HOST) {
      redirectUrl.hostname = APEX_HOST;
      shouldRedirect = true;
    }

    const legacyTarget = LEGACY_REDIRECTS.get(redirectUrl.pathname);
    if (legacyTarget) {
      redirectUrl.pathname = legacyTarget;
      shouldRedirect = true;
    }

    if (shouldRedirect) {
      return Response.redirect(redirectUrl.toString(), 301);
    }

    if (isProtectedAdminPath(url.pathname)) {
      const authResponse = await requireAdminAuth(request, env);
      if (authResponse) {
        return withResponseHeaders(authResponse, url.pathname);
      }
    }

    if (url.pathname.startsWith("/api/")) {
      const apiResponse = await routeApi(request, env);
      return withResponseHeaders(apiResponse, url.pathname);
    }

    let response = await env.ASSETS.fetch(request);

    if (response.status === 404 && url.pathname !== "/404.html") {
      const notFoundUrl = new URL("/404.html", url.origin);
      const notFoundRequest = new Request(notFoundUrl.toString(), request);
      const notFoundResponse = await env.ASSETS.fetch(notFoundRequest);
      if (notFoundResponse.ok) {
        response = new Response(notFoundResponse.body, {
          status: 404,
          statusText: "Not Found",
          headers: notFoundResponse.headers,
        });
      }
    }

    return withResponseHeaders(response, url.pathname);
  },
};
