const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-site-nav]');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('is-open', !expanded);
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });
  });
}
document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});
const cookieBanner = document.querySelector('[data-cookie-banner]');
const cookieAccept = document.querySelector('[data-cookie-accept]');
const cookieBannerKey = "opticable-cookie-banner-accepted";
if (cookieBanner && cookieAccept) {
  let accepted = false;
  try {
    accepted = window.localStorage.getItem(cookieBannerKey) === 'accepted';
  } catch (error) {
    accepted = false;
  }
  if (!accepted) {
    cookieBanner.hidden = false;
  }
  cookieAccept.addEventListener('click', () => {
    try {
      window.localStorage.setItem(cookieBannerKey, 'accepted');
    } catch (error) {}
    cookieBanner.hidden = true;
  });
}
const lightbox = document.querySelector('[data-image-lightbox]');
const lightboxImage = lightbox?.querySelector('[data-lightbox-image]');
const lightboxCaption = lightbox?.querySelector('[data-lightbox-caption]');
const lightboxClose = lightbox?.querySelector('[data-lightbox-close]');
let lastLightboxTrigger = null;
if (lightbox && lightboxImage && lightboxCaption && lightboxClose) {
  const closeLightbox = () => {
    if (lightbox.hidden) return;
    lightbox.hidden = true;
    document.body.classList.remove('lightbox-open');
    lightboxImage.removeAttribute('src');
    lightboxImage.alt = '';
    lightboxImage.style.removeProperty('--lightbox-image-width');
    lightboxImage.style.removeProperty('--lightbox-image-height');
    lightboxCaption.textContent = '';
    if (lastLightboxTrigger) {
      lastLightboxTrigger.focus();
      lastLightboxTrigger = null;
    }
  };
  document.querySelectorAll('[data-lightbox-trigger]').forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      const src = trigger.getAttribute('data-lightbox-src');
      if (!src) return;
      event.preventDefault();
      lastLightboxTrigger = trigger;
      lightboxImage.src = src;
      lightboxImage.alt = trigger.getAttribute('data-lightbox-alt') || '';
      const lightboxWidth = trigger.getAttribute('data-lightbox-width');
      const lightboxHeight = trigger.getAttribute('data-lightbox-height');
      if (lightboxWidth) {
        lightboxImage.style.setProperty('--lightbox-image-width', lightboxWidth + 'px');
      } else {
        lightboxImage.style.removeProperty('--lightbox-image-width');
      }
      if (lightboxHeight) {
        lightboxImage.style.setProperty('--lightbox-image-height', lightboxHeight + 'px');
      } else {
        lightboxImage.style.removeProperty('--lightbox-image-height');
      }
      lightboxCaption.textContent = trigger.getAttribute('data-lightbox-caption') || lightboxImage.alt;
      lightbox.hidden = false;
      document.body.classList.add('lightbox-open');
      lightboxClose.focus();
    });
  });
  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !lightbox.hidden) {
      closeLightbox();
    }
  });
}
document.querySelectorAll('[data-service-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('[data-carousel-track]');
  const prev = carousel.querySelector('[data-carousel-prev]');
  const next = carousel.querySelector('[data-carousel-next]');
  if (!track || !prev || !next) {
    return;
  }
  const getStep = () => {
    const firstCard = track.querySelector('.service-carousel-card');
    const styles = window.getComputedStyle(track);
    const gap = parseFloat(styles.columnGap || styles.gap || '0');
    return (firstCard ? firstCard.getBoundingClientRect().width : track.clientWidth) + gap;
  };
  const updateButtons = () => {
    const maxScroll = Math.max(track.scrollWidth - track.clientWidth - 4, 0);
    prev.disabled = track.scrollLeft <= 4;
    next.disabled = track.scrollLeft >= maxScroll;
  };
  prev.addEventListener('click', () => {
    track.scrollBy({ left: -getStep(), behavior: 'smooth' });
  });
  next.addEventListener('click', () => {
    track.scrollBy({ left: getStep(), behavior: 'smooth' });
  });
  track.addEventListener('scroll', updateButtons, { passive: true });
  window.addEventListener('resize', updateButtons);
  updateButtons();
});

const promoStorageKey = 'opticable-promo-entry';
const promoLocaleMap = { en: 'en-CA', fr: 'fr-CA' };
let promoTurnstileScriptPromise = null;
function readPromoEntry() {
  try {
    const raw = window.localStorage.getItem(promoStorageKey);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}
function writePromoEntry(entry) {
  try {
    window.localStorage.setItem(promoStorageKey, JSON.stringify(entry));
  } catch (error) {}
}
function clearPromoEntry() {
  try {
    window.localStorage.removeItem(promoStorageKey);
  } catch (error) {}
}
function promoDateLabel(value, lang) {
  if (!value) return '';
  try {
    return new Intl.DateTimeFormat(promoLocaleMap[lang] || 'en-CA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: 'America/Toronto',
    }).format(new Date(value));
  } catch (error) {
    return value;
  }
}
function promoEntryActive(entry) {
  if (!entry || !entry.promoExpiresAt) return false;
  return new Date(entry.promoExpiresAt).getTime() > Date.now();
}
function promoPayloadCopy(node, selector) {
  const source = node.querySelector(selector);
  if (!source) return {};
  try {
    return JSON.parse(source.textContent || '{}');
  } catch (error) {
    return {};
  }
}
function promoUtms() {
  const url = new URL(window.location.href);
  return {
    utmSource: url.searchParams.get('utm_source') || '',
    utmMedium: url.searchParams.get('utm_medium') || '',
    utmCampaign: url.searchParams.get('utm_campaign') || '',
    utmContent: url.searchParams.get('utm_content') || '',
    utmTerm: url.searchParams.get('utm_term') || '',
  };
}
function trackPromoAnalyticsEvent(eventName, detail) {
  if (!eventName || typeof window === 'undefined') return;
  const payload = {
    event_category: 'promo',
    promo_campaign_id: detail && detail.campaignId ? detail.campaignId : '',
    promo_discount_percent: detail && typeof detail.discountPercent !== 'undefined' ? detail.discountPercent : null,
    promo_locale: detail && detail.locale ? detail.locale : '',
    promo_code: detail && detail.promoCode ? detail.promoCode : '',
    promo_duplicate: detail && detail.duplicate ? 'true' : 'false',
  };
  if (Array.isArray(window.dataLayer)) {
    window.dataLayer.push({ event: eventName, ...payload });
  }
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, payload);
    if (detail && detail.googleAdsSendTo) {
      window.gtag('event', 'conversion', { send_to: detail.googleAdsSendTo });
    }
  }
}
function applyPromoResult(shell, copy, payload, stateLabel, title, description) {
  const panel = shell.querySelector('[data-promo-result]');
  if (!panel || !payload) return;
  const state = panel.querySelector('[data-promo-result-state]');
  const titleNode = panel.querySelector('[data-promo-result-title]');
  const copyNode = panel.querySelector('[data-promo-result-copy]');
  const discountNode = panel.querySelector('[data-promo-result-discount]');
  const codeInput = panel.querySelector('[data-promo-result-code-input]');
  const expiryNode = panel.querySelector('[data-promo-result-expiry]');
  const copyButton = panel.querySelector('[data-promo-result-copy-button]');
  const saveButton = panel.querySelector('[data-promo-result-save-button]');
  if (state) {
    state.textContent = stateLabel || '';
    state.hidden = !stateLabel;
  }
  if (titleNode) titleNode.textContent = title || copy.resultTitle || '';
  if (copyNode) copyNode.textContent = description || copy.resultCopy || '';
  if (discountNode) discountNode.textContent = payload.discountLabel || '';
  if (codeInput) codeInput.value = payload.promoCode || '';
  if (expiryNode) expiryNode.textContent = promoDateLabel(payload.promoExpiresAt, payload.locale || shell.dataset.lang || 'en');
  if (copyButton) {
    copyButton.textContent = copyButton.dataset.copyDefault || copyButton.textContent;
  }
  if (saveButton) {
    saveButton.textContent = saveButton.dataset.saveDefault || saveButton.textContent;
  }
  panel.hidden = false;
  document.body.classList.add('lightbox-open');
}
function loadPromoTurnstileScript() {
  if (window.turnstile) {
    return Promise.resolve(window.turnstile);
  }
  if (!promoTurnstileScriptPromise) {
    promoTurnstileScriptPromise = new Promise((resolve, reject) => {
      const existing = document.querySelector('script[data-promo-turnstile-script]');
      if (existing) {
        existing.addEventListener('load', () => resolve(window.turnstile));
        existing.addEventListener('error', reject);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
      script.async = true;
      script.defer = true;
      script.dataset.promoTurnstileScript = 'true';
      script.onload = () => resolve(window.turnstile);
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
  return promoTurnstileScriptPromise;
}
async function initPromoForms() {
  const promoRoots = document.querySelectorAll('[data-promo-root]');
  if (!promoRoots.length) {
    return;
  }
  clearPromoEntry();
  for (const shell of promoRoots) {
    const lang = shell.dataset.lang || 'en';
    const copy = promoPayloadCopy(shell, '[data-promo-copy]');
    const configUrl = shell.dataset.configUrl;
    const entryUrl = shell.dataset.entryUrl;
    const form = shell.querySelector('[data-promo-form]');
    const submit = shell.querySelector('[data-promo-submit]');
    const status = shell.querySelector('[data-promo-status]');
    const errorNode = shell.querySelector('[data-promo-error]');
    const skillShell = shell.querySelector('[data-promo-skill-shell]');
    const skillPrompt = shell.querySelector('[data-promo-skill-prompt]');
    const turnstileMount = shell.querySelector('[data-promo-turnstile]');
    const resultPanel = shell.querySelector('[data-promo-result]');
    if (!configUrl || !entryUrl || !form || !submit || !status || !errorNode || !skillShell || !skillPrompt || !turnstileMount) {
      continue;
    }
    let config = null;
    let turnstileToken = '';
    let widgetId = null;
    const showError = (message) => {
      errorNode.textContent = message || copy.genericError || '';
      errorNode.hidden = !message;
    };
    const showStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const closePromoResult = () => {
      if (!resultPanel || resultPanel.hidden) return;
      resultPanel.hidden = true;
      document.body.classList.remove('lightbox-open');
    };
    if (resultPanel) {
      resultPanel.querySelectorAll('[data-promo-result-close]').forEach((button) => {
        button.addEventListener('click', closePromoResult);
      });
      resultPanel.addEventListener('click', (event) => {
        if (event.target === resultPanel) {
          closePromoResult();
        }
      });
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !resultPanel.hidden) {
          closePromoResult();
        }
      });
      const copyButton = resultPanel.querySelector('[data-promo-result-copy-button]');
      const saveButton = resultPanel.querySelector('[data-promo-result-save-button]');
      const codeInput = resultPanel.querySelector('[data-promo-result-code-input]');
      const titleNode = resultPanel.querySelector('[data-promo-result-title]');
      const discountNode = resultPanel.querySelector('[data-promo-result-discount]');
      const expiryNode = resultPanel.querySelector('[data-promo-result-expiry]');
      let copyResetTimer = null;
      let saveResetTimer = null;
      if (copyButton && codeInput) {
        copyButton.addEventListener('click', async () => {
          const code = codeInput.value || '';
          if (!code) return;
          let copied = false;
          try {
            await navigator.clipboard.writeText(code);
            copied = true;
          } catch (error) {
            codeInput.focus();
            codeInput.select();
            try {
              copied = document.execCommand('copy');
            } catch (fallbackError) {
              copied = false;
            }
          }
          if (!copied) return;
          copyButton.textContent = copyButton.dataset.copySuccess || copyButton.textContent;
          window.clearTimeout(copyResetTimer);
          copyResetTimer = window.setTimeout(() => {
            copyButton.textContent = copyButton.dataset.copyDefault || copyButton.textContent;
          }, 1800);
        });
      }
      if (saveButton && codeInput) {
        saveButton.addEventListener('click', () => {
          const code = (codeInput.value || '').trim();
          if (!code) return;
          const labels = copy.resultLabels || {};
          const lines = [
            titleNode ? titleNode.textContent.trim() : (copy.resultTitle || ''),
            '',
            `${labels.code || 'Promo code'}: ${code}`,
            `${labels.discount || 'Discount'}: ${discountNode ? discountNode.textContent.trim() : ''}`,
            `${labels.expires || 'Valid until'}: ${expiryNode ? expiryNode.textContent.trim() : ''}`,
            '',
            `${copy.saveQuoteLabel || 'Quote page'}: ${new URL(copy.quotePath || '/', window.location.origin).toString()}`,
          ].filter(Boolean);
          try {
            const blob = new Blob(['\ufeff', lines.join('\r\n')], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            const objectUrl = URL.createObjectURL(blob);
            link.href = objectUrl;
            link.download = `${copy.saveFilePrefix || 'opticable-promo-code'}-${code.toLowerCase()}.txt`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.setTimeout(() => URL.revokeObjectURL(objectUrl), 2000);
            saveButton.textContent = saveButton.dataset.saveSuccess || saveButton.textContent;
            window.clearTimeout(saveResetTimer);
            saveResetTimer = window.setTimeout(() => {
              saveButton.textContent = saveButton.dataset.saveDefault || saveButton.textContent;
            }, 1800);
          } catch (error) {}
        });
      }
    }
    showStatus(copy.statusLoading || '');
    showError('');
    try {
      const response = await fetch(configUrl, { headers: { Accept: 'application/json' } });
      config = await response.json();
    } catch (error) {
      config = { available: false };
    }
    if (!config || !config.available || !config.turnstileSiteKey || !config.challenge) {
      showStatus(copy.statusUnavailable || '');
      submit.disabled = true;
      continue;
    }
    skillShell.hidden = false;
    skillPrompt.textContent = config.challenge.prompt || '';
    const skillTokenField = form.elements.namedItem('skill_token');
    if (skillTokenField) {
      skillTokenField.value = config.challenge.token || '';
    }
    try {
      const turnstile = await loadPromoTurnstileScript();
      widgetId = turnstile.render(turnstileMount, {
        sitekey: config.turnstileSiteKey,
        action: config.turnstileAction || 'promo-entry',
        callback(token) {
          turnstileToken = token || '';
        },
        'expired-callback'() {
          turnstileToken = '';
        },
        'error-callback'() {
          turnstileToken = '';
        },
      });
      submit.disabled = false;
      showStatus('');
    } catch (error) {
      showStatus(copy.statusUnavailable || '');
      showError(copy.turnstileError || copy.genericError || '');
      submit.disabled = true;
      continue;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      showError('');
      if (!form.reportValidity()) {
        showError(copy.requiredField || '');
        return;
      }
      if (!form.elements.namedItem('quebec_attestation').checked || !form.elements.namedItem('rules_attestation').checked) {
        showError(copy.requiredConsent || '');
        return;
      }
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showError(copy.invalidEmail || '');
        return;
      }
      if (!turnstileToken) {
        showError(copy.turnstileError || '');
        return;
      }
      const payload = {
        locale: lang,
        name: String(form.elements.namedItem('name').value || '').trim(),
        email,
        phone: String(form.elements.namedItem('phone').value || '').trim(),
        company: String(form.elements.namedItem('company').value || '').trim(),
        skillAnswer: String(form.elements.namedItem('skill_answer').value || '').trim(),
        skillToken: String(form.elements.namedItem('skill_token').value || '').trim(),
        turnstileToken,
        quebecAttestation: form.elements.namedItem('quebec_attestation').checked,
        rulesAttestation: form.elements.namedItem('rules_attestation').checked,
        marketingOptIn: form.elements.namedItem('marketing_opt_in').checked,
        landingPath: window.location.pathname,
        landingUrl: window.location.href,
        referrerUrl: document.referrer || '',
        ...promoUtms(),
      };
      submit.disabled = true;
      const previousLabel = submit.textContent;
      submit.textContent = copy.submitLoading || previousLabel;
      try {
        const response = await fetch(entryUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          showError(result.error || copy.genericError || '');
        } else {
          const entry = result.entry || {};
          const stored = {
            campaignId: result.campaignId,
            discountPercent: entry.discountPercent,
            discountLabel: entry.discountLabel,
            promoCode: entry.promoCode,
            promoExpiresAt: entry.promoExpiresAt,
            locale: lang,
          };
          showStatus('');
          applyPromoResult(
            shell,
            copy,
            stored,
            '',
            result.duplicate ? copy.duplicateTitle : copy.resultTitle,
            result.duplicate ? copy.duplicateCopy : copy.resultCopy
          );
          trackPromoAnalyticsEvent(
            result.duplicate ? 'promo_code_retrieved' : 'promo_code_generated',
            {
              campaignId: result.campaignId || '',
              discountPercent: entry.discountPercent,
              promoCode: entry.promoCode || '',
              locale: lang,
              duplicate: Boolean(result.duplicate),
              googleAdsSendTo: result.duplicate ? '' : "AW-18043353221/d5WVCLvr0JgcEIXx3ptD",
            }
          );
          if (resultPanel) {
            const focusTarget = resultPanel.querySelector('[data-promo-result-copy-button]') || resultPanel.querySelector('[data-promo-result-close]');
            if (focusTarget) {
              window.setTimeout(() => focusTarget.focus(), 40);
            }
          }
        }
        if (window.turnstile && widgetId !== null) {
          window.turnstile.reset(widgetId);
          turnstileToken = '';
        }
      } catch (error) {
        showError(copy.genericError || '');
      } finally {
        submit.disabled = false;
        submit.textContent = previousLabel;
      }
    });
  }
}
function initPromoUnsubscribe() {
  document.querySelectorAll('[data-promo-unsubscribe]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-promo-unsubscribe-copy]');
    const form = shell.querySelector('[data-promo-unsubscribe-form]');
    const status = shell.querySelector('[data-promo-unsubscribe-status]');
    const errorNode = shell.querySelector('[data-promo-unsubscribe-error]');
    const url = shell.dataset.unsubscribeUrl;
    const lang = shell.dataset.lang || 'en';
    if (!form || !status || !errorNode || !url) return;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      status.hidden = true;
      errorNode.hidden = true;
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errorNode.textContent = copy.invalidEmail || '';
        errorNode.hidden = false;
        return;
      }
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang }),
        });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          throw new Error(result.error || copy.genericError || '');
        }
        status.textContent = result.message || copy.success || '';
        status.hidden = false;
        form.reset();
      } catch (error) {
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    });
  });
}
function promoAdminAttribution(entry, copy) {
  const utmBits = [entry.utm_source, entry.utm_medium, entry.utm_campaign].filter(Boolean);
  if (utmBits.length) {
    return utmBits.join(' / ');
  }
  return entry.referrer_host || copy.none || '—';
}
function promoAdminMarketingLabel(entry, copy) {
  if (entry.marketing_opt_out_at) return copy.marketingOut || copy.none || '—';
  if (entry.marketing_opt_in) return copy.marketingYes || copy.none || '—';
  return copy.marketingNo || copy.none || '—';
}
function promoAdminTableCell(value, className) {
  const cell = document.createElement('td');
  if (className) {
    cell.className = className;
  }
  cell.textContent = value == null || value === '' ? '—' : String(value);
  return cell;
}
function initPromoAdmin() {
  document.querySelectorAll('[data-promo-admin]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-promo-admin-copy]');
    const lang = shell.dataset.lang || 'en';
    const entriesUrl = shell.dataset.entriesUrl;
    const exportUrl = shell.dataset.exportUrl;
    const subscribersExportUrl = shell.dataset.subscribersExportUrl;
    const deleteUrl = shell.dataset.deleteUrl;
    const status = shell.querySelector('[data-promo-admin-status]');
    const errorNode = shell.querySelector('[data-promo-admin-error]');
    const refreshButton = shell.querySelector('[data-promo-admin-refresh]');
    const exportLink = shell.querySelector('[data-promo-admin-export]');
    const subscribersExportLink = shell.querySelector('[data-promo-admin-export-subscribers]');
    const deleteSelectedButton = shell.querySelector('[data-promo-admin-delete-selected]');
    const deleteViewButton = shell.querySelector('[data-promo-admin-delete-view]');
    const scopeButtons = shell.querySelectorAll('[data-promo-admin-scope]');
    const selectAll = shell.querySelector('[data-promo-admin-select-all]');
    const tableBody = shell.querySelector('[data-promo-admin-table-body]');
    const emptyNode = shell.querySelector('[data-promo-admin-empty]');
    const totalEntries = shell.querySelector('[data-promo-admin-total]');
    const marketingEntries = shell.querySelector('[data-promo-admin-marketing]');
    const recentEntries = shell.querySelector('[data-promo-admin-recent]');
    const latestEntry = shell.querySelector('[data-promo-admin-latest]');
    const campaignName = shell.querySelector('[data-promo-admin-current-name]');
    const campaignWindow = shell.querySelector('[data-promo-admin-window]');
    const activeView = shell.querySelector('[data-promo-admin-view]');
    if (!entriesUrl || !exportUrl || !subscribersExportUrl || !deleteUrl || !status || !errorNode || !refreshButton || !exportLink || !subscribersExportLink || !deleteSelectedButton || !deleteViewButton || !selectAll || !tableBody) {
      return;
    }
    let currentScope = 'current';
    let activeRows = [];
    const selectedIds = new Set();
    const exportLinks = [exportLink, subscribersExportLink];
    const setStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const setError = (message) => {
      errorNode.textContent = message || '';
      errorNode.hidden = !message;
    };
    const syncSelectionUi = () => {
      deleteSelectedButton.disabled = selectedIds.size === 0 || activeRows.length === 0;
      selectAll.checked = activeRows.length > 0 && activeRows.every((entry) => selectedIds.has(entry.id));
      selectAll.indeterminate = selectedIds.size > 0 && !selectAll.checked;
    };
    const resetSelection = () => {
      selectedIds.clear();
      syncSelectionUi();
    };
    const setScope = (scope) => {
      currentScope = scope === 'all' ? 'all' : 'current';
      scopeButtons.forEach((button) => {
        const pressed = button.dataset.promoAdminScope === currentScope;
        button.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      });
      const nextExportUrl = new URL(exportUrl, window.location.origin);
      nextExportUrl.searchParams.set('scope', currentScope);
      exportLink.href = nextExportUrl.toString();
      const nextSubscribersExportUrl = new URL(subscribersExportUrl, window.location.origin);
      nextSubscribersExportUrl.searchParams.set('scope', currentScope);
      subscribersExportLink.href = nextSubscribersExportUrl.toString();
      deleteViewButton.textContent = currentScope === 'all'
        ? (copy.deleteViewAllLabel || copy.deleteViewLabel || deleteViewButton.textContent)
        : (copy.deleteViewLabel || deleteViewButton.textContent);
      resetSelection();
    };
    const renderEntries = (entries) => {
      tableBody.textContent = '';
      activeRows = Array.isArray(entries) ? entries : [];
      if (!activeRows.length) {
        emptyNode.hidden = false;
        resetSelection();
        return;
      }
      emptyNode.hidden = true;
      activeRows.forEach((entry) => {
        const row = document.createElement('tr');
        const selectCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = selectedIds.has(entry.id);
        checkbox.setAttribute('aria-label', entry.email || entry.name || String(entry.id));
        checkbox.addEventListener('change', () => {
          if (checkbox.checked) {
            selectedIds.add(entry.id);
          } else {
            selectedIds.delete(entry.id);
          }
          syncSelectionUi();
        });
        selectCell.appendChild(checkbox);
        row.appendChild(selectCell);
        row.appendChild(promoAdminTableCell(promoDateLabel(entry.created_at, lang) || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.campaign_id || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.name || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.email || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.phone || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.company || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.discount_percent ? `${entry.discount_percent}%` : (copy.none || '—')));
        row.appendChild(promoAdminTableCell(entry.promo_code || copy.none || '—', 'promo-admin-code'));
        row.appendChild(promoAdminTableCell(promoDateLabel(entry.promo_expires_at, lang) || copy.none || '—'));
        row.appendChild(promoAdminTableCell(promoAdminMarketingLabel(entry, copy)));
        row.appendChild(promoAdminTableCell(promoAdminAttribution(entry, copy)));
        tableBody.appendChild(row);
      });
      syncSelectionUi();
    };
    const setBusy = (busy) => {
      refreshButton.disabled = busy;
      deleteViewButton.disabled = busy;
      deleteSelectedButton.disabled = busy || selectedIds.size === 0 || activeRows.length === 0;
      exportLinks.forEach((link) => {
        link.setAttribute('aria-disabled', busy ? 'true' : 'false');
        if (busy) {
          link.classList.add('is-disabled');
        } else {
          link.classList.remove('is-disabled');
        }
      });
      scopeButtons.forEach((button) => {
        button.disabled = busy;
      });
      selectAll.disabled = busy || activeRows.length === 0;
    };
    const deleteEntries = async (mode) => {
      if (mode === 'selected' && selectedIds.size === 0) {
        setError(copy.deleteNone || copy.deleteError || '');
        return;
      }
      const confirmed = window.confirm(mode === 'all' ? (copy.deleteViewConfirm || '') : (copy.deleteSelectedConfirm || ''));
      if (!confirmed) {
        return;
      }
      setError('');
      setStatus(copy.loading || '');
      setBusy(true);
      try {
        const response = await fetch(deleteUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            mode,
            scope: currentScope,
            ids: mode === 'selected' ? Array.from(selectedIds) : [],
          }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.deleteError || '');
        }
        resetSelection();
        await loadEntries(mode === 'all' ? (copy.deleteViewSuccess || '') : (copy.deleteSelectedSuccess || ''));
      } catch (error) {
        setError(error.message || copy.deleteError || '');
        setStatus('');
      } finally {
        setBusy(false);
      }
    };
    const loadEntries = async (successMessage = '') => {
      setError('');
      setStatus(successMessage || copy.loading || '');
      setBusy(true);
      try {
        const requestUrl = new URL(entriesUrl, window.location.origin);
        requestUrl.searchParams.set('scope', currentScope);
        requestUrl.searchParams.set('limit', shell.dataset.limit || '200');
        const response = await fetch(requestUrl.toString(), { headers: { Accept: 'application/json' } });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.loadError || '');
        }
        if (totalEntries) totalEntries.textContent = String(payload.summary.totalEntries || 0);
        if (marketingEntries) marketingEntries.textContent = String(payload.summary.marketingActive || 0);
        if (recentEntries) recentEntries.textContent = String(payload.summary.recentEntries || 0);
        if (latestEntry) latestEntry.textContent = payload.summary.latestEntryAt ? promoDateLabel(payload.summary.latestEntryAt, lang) : (copy.none || '—');
        if (campaignName) {
          campaignName.textContent = `${payload.campaign.currentName || ''} (${payload.campaign.currentId || ''})`.trim();
        }
        if (campaignWindow) {
          campaignWindow.textContent = `${promoDateLabel(payload.campaign.startsAt, lang)} - ${promoDateLabel(payload.campaign.endsAt, lang)}`;
        }
        if (activeView) {
          activeView.textContent = currentScope === 'all' ? (copy.scopeAll || '') : (copy.scopeCurrent || '');
        }
        renderEntries(payload.entries || []);
        if (!successMessage) {
          setStatus('');
        }
      } catch (error) {
        activeRows = [];
        emptyNode.hidden = true;
        tableBody.textContent = '';
        resetSelection();
        setError(error.message || copy.loadError || '');
        setStatus('');
      } finally {
        setBusy(false);
        syncSelectionUi();
      }
    };
    scopeButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (button.dataset.promoAdminScope === currentScope) return;
        setScope(button.dataset.promoAdminScope);
        loadEntries();
      });
    });
    selectAll.addEventListener('change', () => {
      if (selectAll.checked) {
        activeRows.forEach((entry) => selectedIds.add(entry.id));
      } else {
        activeRows.forEach((entry) => selectedIds.delete(entry.id));
      }
      renderEntries(activeRows);
    });
    refreshButton.addEventListener('click', loadEntries);
    deleteSelectedButton.addEventListener('click', () => deleteEntries('selected'));
    deleteViewButton.addEventListener('click', () => deleteEntries('all'));
    setScope(currentScope);
    loadEntries();
  });
}
function referralCurrency(value) {
  if (value == null || value === '') return '—';
  return `${value} CAD`;
}
function referralDate(value, lang) {
  return promoDateLabel(value, lang) || '—';
}
function referralDateTime(value, lang) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return referralDate(value, lang);
  try {
    return new Intl.DateTimeFormat(lang === 'fr' ? 'fr-CA' : 'en-CA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  } catch {
    return referralDate(value, lang);
  }
}
function referralLabel(group, key, fallback = '—') {
  if (!group || !Object.prototype.hasOwnProperty.call(group, key)) return fallback;
  return group[key];
}
function initReferralApplyForms() {
  document.querySelectorAll('[data-referral-apply]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-apply-copy]');
    const lang = shell.dataset.lang || 'en';
    const form = shell.querySelector('[data-referral-apply-form]');
    const status = shell.querySelector('[data-referral-apply-status]');
    const errorNode = shell.querySelector('[data-referral-apply-error]');
    const linkWrap = shell.querySelector('[data-referral-apply-link]');
    const linkAnchor = shell.querySelector('[data-referral-apply-link-anchor]');
    const url = shell.dataset.applyUrl;
    const portalUrl = shell.dataset.portalUrl || (lang === 'fr' ? '/fr/portail-references/' : '/en/referral-portal/');
    const companyRequired = shell.dataset.companyRequired === 'true';
    const requiresPassword = shell.dataset.requiresPassword === 'true';
    if (!form || !status || !errorNode || !linkWrap || !linkAnchor || !url) return;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      status.hidden = true;
      errorNode.hidden = true;
      linkWrap.hidden = true;
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errorNode.textContent = copy.invalidEmail || '';
        errorNode.hidden = false;
        return;
      }
      if (!String(form.elements.namedItem('name').value || '').trim()) {
        errorNode.textContent = copy.requiredField || '';
        errorNode.hidden = false;
        return;
      }
      if (companyRequired && !String(form.elements.namedItem('company').value || '').trim()) {
        errorNode.textContent = copy.requiredField || '';
        errorNode.hidden = false;
        return;
      }
      const passwordField = form.elements.namedItem('password');
      const confirmPasswordField = form.elements.namedItem('password_confirm');
      const password = passwordField ? String(passwordField.value || '') : '';
      const confirmPassword = confirmPasswordField ? String(confirmPasswordField.value || '') : '';
      if (requiresPassword) {
        if (password.length < 10) {
          errorNode.textContent = copy.invalidPassword || '';
          errorNode.hidden = false;
          return;
        }
        if (password !== confirmPassword) {
          errorNode.textContent = copy.passwordMismatch || '';
          errorNode.hidden = false;
          return;
        }
      }
      if (!form.elements.namedItem('rules_attestation').checked) {
        errorNode.textContent = copy.requiredConsent || '';
        errorNode.hidden = false;
        return;
      }
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            locale: lang,
            accountType: shell.dataset.accountType || 'client',
            name: String(form.elements.namedItem('name').value || '').trim(),
            email,
            phone: String(form.elements.namedItem('phone').value || '').trim(),
            company: String(form.elements.namedItem('company').value || '').trim(),
            website: form.elements.namedItem('website') ? String(form.elements.namedItem('website').value || '').trim() : '',
            notes: form.elements.namedItem('notes') ? String(form.elements.namedItem('notes').value || '').trim() : '',
            password: requiresPassword ? password : '',
            rulesAttestation: form.elements.namedItem('rules_attestation').checked,
          }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        status.textContent = payload.message || (payload.duplicate ? (copy.duplicate || payload.magicLink?.message || '') : (copy.success || payload.magicLink?.message || ''));
        status.hidden = false;
        if (!payload.duplicate && payload.portalUrl) {
          window.setTimeout(() => {
            window.location.assign(payload.portalUrl || portalUrl);
          }, 180);
          return;
        }
        if (payload.magicLink && payload.magicLink.previewLink) {
          linkAnchor.href = payload.magicLink.previewLink;
          linkWrap.hidden = false;
          window.setTimeout(() => {
            window.location.assign(payload.magicLink.previewLink);
          }, 180);
        }
      } catch (error) {
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    });
  });
}
function initReferralPortal() {
  document.querySelectorAll('[data-referral-portal]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-portal-copy]');
    const lang = shell.dataset.lang || 'en';
    const loginUrl = shell.dataset.loginUrl;
    const requestLinkUrl = shell.dataset.requestLinkUrl;
    const passwordUrl = shell.dataset.passwordUrl;
    const portalUrl = shell.dataset.portalUrl;
    const accessUrl = shell.dataset.accessUrl || portalUrl;
    const authBox = shell.querySelector('[data-referral-portal-auth]');
    const loginForm = shell.querySelector('[data-referral-portal-login]');
    const recoveryForm = shell.querySelector('[data-referral-portal-link-form]');
    const status = shell.querySelector('[data-referral-portal-status]');
    const errorNode = shell.querySelector('[data-referral-portal-error]');
    const dashboard = shell.querySelector('[data-referral-portal-dashboard]');
    const shareCopyButton = shell.querySelector('[data-referral-portal-share-copy]');
    const shareStatus = shell.querySelector('[data-referral-portal-share-status]');
    const creditMeta = shell.querySelector('[data-referral-credit-meta]');
    const creditPanel = shell.querySelector('[data-referral-credit-panel]');
    const passwordForm = shell.querySelector('[data-referral-password-form]');
    const passwordStatus = shell.querySelector('[data-referral-password-status]');
    const passwordError = shell.querySelector('[data-referral-password-error]');
    const passwordCurrentWrap = shell.querySelector('[data-referral-password-current-wrap]');
    const passwordSubmit = shell.querySelector('[data-referral-password-submit]');
    if (!loginUrl || !requestLinkUrl || !passwordUrl || !portalUrl || !authBox || !loginForm || !recoveryForm || !status || !errorNode || !dashboard || !creditMeta || !creditPanel || !passwordForm || !passwordStatus || !passwordError || !passwordCurrentWrap || !passwordSubmit) return;
    const labels = copy.labels || {};
    let activeAccount = null;
    const queryState = new URL(window.location.href);
    const authState = queryState.searchParams.get('auth') || '';
    const resetState = queryState.searchParams.get('reset') || '';
    const clearAuthState = () => {
      const current = new URL(window.location.href);
      if (!current.searchParams.has('auth')) return;
      current.searchParams.delete('auth');
      window.history.replaceState({}, '', current.toString());
    };
    const clearResetState = () => {
      const current = new URL(window.location.href);
      if (!current.searchParams.has('reset')) return;
      current.searchParams.delete('reset');
      window.history.replaceState({}, '', current.toString());
    };
    const authMessage = () => {
      if (authState === 'expired') return copy.authExpired || '';
      if (authState === 'used') return copy.authUsed || '';
      if (authState === 'invalid') return copy.authInvalid || '';
      return '';
    };
    const resetMessage = () => {
      if (resetState === 'ready') return copy.resetReady || '';
      return '';
    };
    const viewCopy = (accountType) => {
      const views = copy.views || {};
      return accountType === 'partner' ? (views.partner || {}) : (views.client || {});
    };
    const caseReference = (item) => {
      if (item.quoteReference) return item.quoteReference;
      if (item.referredCompany) return item.referredCompany;
      if (item.referredName) return item.referredName;
      return '—';
    };
    const setInlineMessage = (node, message) => {
      node.textContent = message || '';
      node.hidden = !message;
    };
    const renderTableRows = (target, rows, cells) => {
      target.textContent = '';
      if (!rows.length) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = cells.length;
        cell.textContent = '—';
        row.appendChild(cell);
        target.appendChild(row);
        return;
      }
      rows.forEach((item) => {
        const row = document.createElement('tr');
        cells.forEach((cellBuilder) => {
          row.appendChild(promoAdminTableCell(cellBuilder(item)));
        });
        target.appendChild(row);
      });
    };
    const showAuth = (show) => {
      authBox.hidden = !show;
      dashboard.hidden = show;
    };
    const populateView = (payload) => {
      const accountType = payload.account.accountType === 'partner' ? 'partner' : 'client';
      const view = viewCopy(accountType);
      shell.classList.toggle('is-partner', accountType === 'partner');
      shell.classList.toggle('is-client', accountType !== 'partner');
      creditMeta.hidden = false;
      creditPanel.hidden = accountType === 'partner';
      shell.querySelector('[data-referral-portal-banner-eyebrow]').textContent = view.bannerEyebrow || '';
      shell.querySelector('[data-referral-portal-banner-title]').textContent = view.bannerTitle || '';
      shell.querySelector('[data-referral-portal-banner-copy]').textContent = view.bannerCopy || '';
      shell.querySelector('[data-referral-help-title]').textContent = view.helpTitle || '';
      const helpList = shell.querySelector('[data-referral-help-list]');
      helpList.textContent = '';
      (view.help || []).forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        helpList.appendChild(li);
      });
      const stats = view.stats || {};
      shell.querySelector('[data-referral-stat-label-total]').textContent = stats.total || '';
      shell.querySelector('[data-referral-stat-label-open]').textContent = stats.open || '';
      shell.querySelector('[data-referral-stat-label-completed]').textContent = stats.completed || '';
      shell.querySelector('[data-referral-stat-label-primary]').textContent = stats.primary || '';
      shell.querySelector('[data-referral-stat-label-secondary]').textContent = stats.secondary || '';
      shell.querySelector('[data-referral-stat-label-tertiary]').textContent = stats.tertiary || '';
      shell.querySelector('[data-referral-stat-total]').textContent = String(payload.stats.totalReferrals || 0);
      shell.querySelector('[data-referral-stat-open]').textContent = String(payload.stats.openReferrals || 0);
      shell.querySelector('[data-referral-stat-completed]').textContent = String(payload.stats.completedReferrals || 0);
      shell.querySelector('[data-referral-portal-referrals-title]').textContent = view.referralsTitle || '';
      shell.querySelector('[data-referral-portal-referrals-intro]').textContent = view.referralsIntro || '';
      shell.querySelector('[data-referral-portal-rewards-title]').textContent = view.rewardsTitle || '';
      shell.querySelector('[data-referral-portal-rewards-intro]').textContent = view.rewardsIntro || '';
      shell.querySelector('[data-referral-portal-amount-label]').textContent = view.amountLabel || '';
      shell.querySelector('[data-referral-portal-summary-note]').textContent = view.summaryNote || '';
      if (accountType === 'partner') {
        shell.querySelector('[data-referral-stat-primary]').textContent = referralCurrency(payload.stats.pendingPayoutCad);
        shell.querySelector('[data-referral-stat-secondary]').textContent = referralCurrency(payload.stats.settledPayoutCad);
        shell.querySelector('[data-referral-stat-tertiary]').textContent = referralCurrency(payload.stats.trackedSubtotalCad);
      } else {
        shell.querySelector('[data-referral-stat-primary]').textContent = referralCurrency(payload.account.walletBalanceCad);
        shell.querySelector('[data-referral-stat-secondary]').textContent = referralCurrency(payload.account.totalEarnedCad);
        shell.querySelector('[data-referral-stat-tertiary]').textContent = referralCurrency('1500.00');
      }
      shell.querySelector('[data-referral-password-title]').textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeTitle || '')
        : (copy.passwordPanel?.createTitle || '');
      shell.querySelector('[data-referral-password-intro]').textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeIntro || '')
        : (copy.passwordPanel?.createIntro || '');
      passwordSubmit.textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeButton || '')
        : (copy.passwordPanel?.createButton || '');
      passwordCurrentWrap.hidden = !payload.account.hasPassword;
    };
    const loadPortal = async () => {
      try {
        status.hidden = true;
        errorNode.hidden = true;
        const response = await fetch(portalUrl, { headers: { Accept: 'application/json' } });
        if (response.status === 401) {
          showAuth(true);
          if (authMessage()) {
            status.hidden = true;
            errorNode.textContent = authMessage();
            errorNode.hidden = false;
          } else {
            status.textContent = copy.notSignedIn || '';
            status.hidden = false;
          }
          return;
        }
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        if (payload.account.passwordResetReady && accessUrl) {
          const target = new URL(accessUrl, window.location.origin);
          window.location.assign(target.toString());
          return;
        }
        activeAccount = payload.account;
        clearAuthState();
        clearResetState();
        showAuth(false);
        shell.querySelector('[data-referral-portal-name]').textContent = payload.account.name || payload.account.email || '—';
        const accountTypeLabel = referralLabel(labels.accountTypes, payload.account.accountType, payload.account.accountType || '—');
        const accountStatusLabel = referralLabel(labels.accountStatuses, payload.account.status, payload.account.status || '—');
        shell.querySelector('[data-referral-portal-meta]').textContent = `${accountTypeLabel} · ${accountStatusLabel} · ${payload.account.email}`;
        populateView(payload);
        shell.querySelector('[data-referral-portal-code]').textContent = payload.account.currentCode || '—';
        shell.querySelector('[data-referral-portal-credit-code]').textContent = payload.account.currentCreditCode || '—';
        shell.querySelector('[data-referral-portal-email]').textContent = payload.account.email || '—';
        const share = shell.querySelector('[data-referral-portal-share]');
        share.textContent = payload.account.shareLink || '—';
        share.href = payload.account.shareLink || shell.dataset.contactUrl || '#';
        share.dataset.shareLink = payload.account.shareLink || '';
        share.title = payload.account.shareLink || '';
        if (shareStatus) {
          shareStatus.textContent = '';
          shareStatus.hidden = true;
        }
        renderTableRows(shell.querySelector('[data-referral-portal-referrals]'), payload.referrals || [], [
          (item) => item.id,
          (item) => caseReference(item),
          (item) => referralLabel(labels.caseStatuses, item.status, item.status || '—'),
          (item) => referralDate(item.createdAt, lang),
          (item) => item.quotedSubtotalCad ? referralCurrency(item.quotedSubtotalCad) : '—',
          (item) => item.rewardAmountCad ? referralCurrency(item.rewardAmountCad) : '—',
        ]);
        renderTableRows(shell.querySelector('[data-referral-portal-rewards]'), payload.rewards || [], [
          (item) => item.id,
          (item) => referralLabel(copy.ledgerStatuses || labels.rewardStatuses, item.status, referralLabel(labels.rewardStatuses, item.status, item.status || '—')),
          (item) => referralCurrency(item.amountCad),
          (item) => referralDate(item.createdAt, lang),
          (item) => item.note || '—',
        ]);
        shell.querySelector('[data-referral-credit-panel-code]').textContent = payload.account.currentCreditCode || '—';
        shell.querySelector('[data-referral-credit-panel-balance]').textContent = referralCurrency(payload.account.walletBalanceCad);
        shell.querySelector('[data-referral-credit-panel-cap]').textContent = referralCurrency('1500.00');
        const creditInstruction = shell.querySelector('[data-referral-credit-panel-instruction]');
        if (creditInstruction) {
          creditInstruction.textContent = (copy.creditPanel && copy.creditPanel.manualCopy) || '';
        }
        setInlineMessage(passwordStatus, '');
        setInlineMessage(passwordError, '');
        passwordForm.reset();
      } catch (error) {
        showAuth(true);
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    };
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      clearAuthState();
      clearResetState();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(loginForm.elements.namedItem('email').value || '').trim();
      const password = String(loginForm.elements.namedItem('password').value || '');
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      if (password.length < 10) {
        setInlineMessage(errorNode, copy.invalidPassword || '');
        return;
      }
      try {
        const response = await fetch(loginUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, password, locale: lang }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.invalidCredentials || copy.genericError || '');
        }
        window.location.assign(payload.portalUrl || window.location.pathname);
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.invalidCredentials || copy.genericError || '');
      }
    });
    recoveryForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      clearAuthState();
      clearResetState();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(recoveryForm.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      try {
        const response = await fetch(requestLinkUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang, redirectPath: accessUrl }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(status, payload.message || copy.loginSent || '');
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.genericError || '');
      }
    });
    passwordForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(passwordStatus, '');
      setInlineMessage(passwordError, '');
      const currentPassword = String(passwordForm.elements.namedItem('current_password').value || '');
      const newPassword = String(passwordForm.elements.namedItem('new_password').value || '');
      const confirmPassword = String(passwordForm.elements.namedItem('confirm_password').value || '');
      if (newPassword.length < 10) {
        setInlineMessage(passwordError, copy.invalidPassword || '');
        return;
      }
      if (newPassword !== confirmPassword) {
        setInlineMessage(passwordError, copy.passwordMismatch || '');
        return;
      }
      try {
        const response = await fetch(passwordUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ locale: lang, currentPassword, newPassword }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(passwordStatus, payload.message || copy.passwordSaved || '');
        await loadPortal();
      } catch (error) {
        setInlineMessage(passwordError, error.message || copy.genericError || '');
      }
    });
    if (shareCopyButton) {
      shareCopyButton.addEventListener('click', async () => {
        const share = shell.querySelector('[data-referral-portal-share]');
        const value = share?.dataset.shareLink || '';
        if (!value) return;
        try {
          await navigator.clipboard.writeText(value);
          if (shareStatus) setInlineMessage(shareStatus, copy.shareCopied || '');
        } catch {
          if (shareStatus) setInlineMessage(shareStatus, copy.shareCopyError || '');
        }
      });
    }
    loadPortal();
  });
}
function initReferralAccess() {
  document.querySelectorAll('[data-referral-access]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-access-copy]');
    const lang = shell.dataset.lang || 'en';
    const requestLinkUrl = shell.dataset.requestLinkUrl;
    const passwordUrl = shell.dataset.passwordUrl;
    const portalUrl = shell.dataset.portalUrl;
    const portalPageUrl = shell.dataset.portalPageUrl || (lang === 'fr' ? '/fr/portail-references/' : '/en/referral-portal/');
    const accessUrl = shell.dataset.accessUrl || portalPageUrl;
    const status = shell.querySelector('[data-referral-access-status]');
    const errorNode = shell.querySelector('[data-referral-access-error]');
    const readyWrap = shell.querySelector('[data-referral-access-ready]');
    const readyAccount = shell.querySelector('[data-referral-access-account]');
    const requestWrap = shell.querySelector('[data-referral-access-request]');
    const requestForm = shell.querySelector('[data-referral-access-request-form]');
    const passwordForm = shell.querySelector('[data-referral-access-password-form]');
    const passwordStatus = shell.querySelector('[data-referral-access-password-status]');
    const passwordError = shell.querySelector('[data-referral-access-password-error]');
    if (!requestLinkUrl || !passwordUrl || !portalUrl || !status || !errorNode || !readyWrap || !readyAccount || !requestWrap || !requestForm || !passwordForm || !passwordStatus || !passwordError) return;
    const query = new URL(window.location.href);
    const authState = query.searchParams.get('auth') || '';
    const setInlineMessage = (node, message) => {
      node.textContent = message || '';
      node.hidden = !message;
    };
    const authMessage = () => {
      if (authState === 'expired') return copy.authExpired || '';
      if (authState === 'used') return copy.authUsed || '';
      if (authState === 'invalid') return copy.authInvalid || '';
      return '';
    };
    const showReset = (payload) => {
      requestWrap.hidden = true;
      readyWrap.hidden = false;
      const accountType = payload.account.accountType === 'partner'
        ? (lang === 'fr' ? 'Programme de partenaires référents' : 'Referral Partner Program')
        : (lang === 'fr' ? 'Programme de référence' : 'Referral Program');
      readyAccount.textContent = `${payload.account.name || payload.account.email || '—'} · ${accountType} · ${payload.account.email || '—'}`;
    };
    const showRequest = (message = '', isError = false) => {
      readyWrap.hidden = true;
      requestWrap.hidden = false;
      setInlineMessage(status, isError ? '' : message);
      setInlineMessage(errorNode, isError ? message : '');
    };
    const loadAccessState = async () => {
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      try {
        const response = await fetch(portalUrl, { headers: { Accept: 'application/json' } });
        if (response.status === 401) {
          showRequest(authMessage() || copy.notReady || '', Boolean(authMessage()));
          return;
        }
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        if (!payload.account.passwordResetReady) {
          window.location.assign(portalPageUrl);
          return;
        }
        showReset(payload);
      } catch (error) {
        showRequest(error.message || copy.genericError || '', true);
      }
    };
    requestForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(requestForm.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      try {
        const response = await fetch(requestLinkUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang, redirectPath: accessUrl }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(status, payload.message || copy.requestSent || '');
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.genericError || '');
      }
    });
    passwordForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(passwordStatus, '');
      setInlineMessage(passwordError, '');
      const newPassword = String(passwordForm.elements.namedItem('new_password').value || '');
      const confirmPassword = String(passwordForm.elements.namedItem('confirm_password').value || '');
      if (newPassword.length < 10) {
        setInlineMessage(passwordError, copy.invalidPassword || '');
        return;
      }
      if (newPassword !== confirmPassword) {
        setInlineMessage(passwordError, copy.passwordMismatch || '');
        return;
      }
      try {
        const response = await fetch(passwordUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ locale: lang, newPassword }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(passwordStatus, payload.message || copy.passwordSaved || '');
        window.setTimeout(() => {
          window.location.assign(portalPageUrl);
        }, 250);
      } catch (error) {
        setInlineMessage(passwordError, error.message || copy.genericError || '');
      }
    });
    loadAccessState();
  });
}
function initReferralAdmin() {
  document.querySelectorAll('[data-referral-admin]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-admin-copy]');
    const lang = shell.dataset.lang || 'en';
    const status = shell.querySelector('[data-referral-admin-status]');
    const errorNode = shell.querySelector('[data-referral-admin-error]');
    const refreshButton = shell.querySelector('[data-referral-admin-refresh]');
    const applicationsBody = shell.querySelector('[data-referral-admin-applications]');
    const accountsBody = shell.querySelector('[data-referral-admin-accounts]');
    const casesBody = shell.querySelector('[data-referral-admin-cases]');
    const rewardsBody = shell.querySelector('[data-referral-admin-rewards]');
    const createForm = shell.querySelector('[data-referral-admin-create-form]');
    const applicationStatusFilter = shell.querySelector('[data-referral-filter-applications-status]');
    const applicationSearchFilter = shell.querySelector('[data-referral-filter-applications-search]');
    const accountProgramFilter = shell.querySelector('[data-referral-filter-accounts-program]');
    const accountStatusFilter = shell.querySelector('[data-referral-filter-accounts-status]');
    const accountSearchFilter = shell.querySelector('[data-referral-filter-accounts-search]');
    const caseProgramFilter = shell.querySelector('[data-referral-filter-cases-program]');
    const caseStatusFilter = shell.querySelector('[data-referral-filter-cases-status]');
    const caseSearchFilter = shell.querySelector('[data-referral-filter-cases-search]');
    const rewardTypeFilter = shell.querySelector('[data-referral-filter-rewards-type]');
    const rewardStatusFilter = shell.querySelector('[data-referral-filter-rewards-status]');
    const rewardSearchFilter = shell.querySelector('[data-referral-filter-rewards-search]');
    const detailEmpty = shell.querySelector('[data-referral-admin-detail-empty]');
    const detailWrap = shell.querySelector('[data-referral-admin-detail]');
    const detailName = shell.querySelector('[data-referral-admin-detail-name]');
    const detailMeta = shell.querySelector('[data-referral-admin-detail-meta]');
    const detailProgram = shell.querySelector('[data-referral-admin-detail-program]');
    const detailStatus = shell.querySelector('[data-referral-admin-detail-status]');
    const detailEmail = shell.querySelector('[data-referral-admin-detail-email]');
    const detailPhone = shell.querySelector('[data-referral-admin-detail-phone]');
    const detailCompany = shell.querySelector('[data-referral-admin-detail-company]');
    const detailWebsite = shell.querySelector('[data-referral-admin-detail-website]');
    const detailShareCode = shell.querySelector('[data-referral-admin-detail-share-code]');
    const detailCreditCode = shell.querySelector('[data-referral-admin-detail-credit-code]');
    const detailBalance = shell.querySelector('[data-referral-admin-detail-balance]');
    const detailEarned = shell.querySelector('[data-referral-admin-detail-earned]');
    const detailCreated = shell.querySelector('[data-referral-admin-detail-created]');
    const detailLogin = shell.querySelector('[data-referral-admin-detail-login]');
    const detailNotes = shell.querySelector('[data-referral-admin-detail-notes]');
    const detailCasesBody = shell.querySelector('[data-referral-admin-detail-cases]');
    const detailRewardsBody = shell.querySelector('[data-referral-admin-detail-rewards]');
    const detailAuditBody = shell.querySelector('[data-referral-admin-detail-audit]');
    const detailExportButton = shell.querySelector('[data-referral-admin-detail-export]');
    const detailResetButton = shell.querySelector('[data-referral-admin-detail-reset]');
    const detailDeleteButton = shell.querySelector('[data-referral-admin-detail-delete]');
    const detailCaseForm = shell.querySelector('[data-referral-admin-case-form]');
    const detailCaseSubmit = shell.querySelector('[data-referral-admin-case-submit]');
    const detailCaseCancel = shell.querySelector('[data-referral-admin-case-cancel]');
    const detailCaseState = shell.querySelector('[data-referral-admin-case-state]');
    if (!status || !errorNode || !refreshButton || !applicationsBody || !accountsBody || !casesBody || !rewardsBody || !createForm) return;
    const labels = copy.labels || {};
    let selectedAccountId = null;
    let selectedAccount = null;
    let selectedCaseId = null;
    const setStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const setError = (message) => {
      errorNode.textContent = message || '';
      errorNode.hidden = !message;
    };
    const clearMessages = () => {
      setStatus('');
      setError('');
    };
    const adminBaseUrl = (() => {
      const current = new URL(window.location.href);
      current.username = '';
      current.password = '';
      current.hash = '';
      current.search = '';
      return current.toString();
    })();
    const resolveAdminUrl = (value) => {
      try {
        return new URL(value, adminBaseUrl).toString();
      } catch {
        return value;
      }
    };
    const programLabel = (accountType) => referralLabel(labels.programTypes || labels.accountTypes, accountType, referralLabel(labels.accountTypes, accountType, accountType || '—'));
    const accountLabel = (item) => `${item.name || '—'} (${item.email || '—'})`;
    const searchBlob = (...values) => values.filter(Boolean).join(' ').toLowerCase();
    const setDetailEmptyState = (message) => {
      selectedAccount = null;
      selectedCaseId = null;
      if (detailEmpty) {
        detailEmpty.textContent = message || copy.messages?.detailEmpty || '';
        detailEmpty.hidden = false;
      }
      if (detailWrap) detailWrap.hidden = true;
    };
    const parseMetadata = (value) => {
      if (!value) return {};
      try {
        return JSON.parse(value);
      } catch {
        return {};
      }
    };
    const auditNote = (entry) => {
      const metadata = parseMetadata(entry.metadata_json);
      const subtotalLabel = lang === 'fr' ? 'Sous-total' : 'Subtotal';
      const rewardLabel = lang === 'fr' ? 'Récompense' : 'Reward';
      const parts = [];
      if (typeof metadata.previousBalanceCents === 'number' && typeof metadata.nextBalanceCents === 'number') {
        parts.push(`${referralCurrency((metadata.previousBalanceCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextBalanceCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.previousAmountCents === 'number' && typeof metadata.nextAmountCents === 'number') {
        parts.push(`${referralCurrency((metadata.previousAmountCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextAmountCents / 100).toFixed(2))}`);
      }
      if (metadata.referredName) parts.push(metadata.referredName);
      if (metadata.referredCompany) parts.push(metadata.referredCompany);
      if (metadata.quoteReference) parts.push(metadata.quoteReference);
      if (metadata.referralCode) parts.push(metadata.referralCode);
      if (metadata.email) parts.push(metadata.email);
      if (metadata.referredEmail) parts.push(metadata.referredEmail);
      if (typeof metadata.deltaCents === 'number') parts.push(referralCurrency((metadata.deltaCents / 100).toFixed(2)));
      if (typeof metadata.previousSubtotalCents === 'number' && typeof metadata.nextSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.previousSubtotalCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextSubtotalCents / 100).toFixed(2))}`);
      } else if (typeof metadata.quotedSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.quotedSubtotalCents / 100).toFixed(2))}`);
      } else if (typeof metadata.nextSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.nextSubtotalCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.previousRewardAmountCents === 'number' && typeof metadata.nextRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.previousRewardAmountCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextRewardAmountCents / 100).toFixed(2))}`);
      } else if (typeof metadata.previousRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.previousRewardAmountCents / 100).toFixed(2))}`);
      } else if (typeof metadata.nextRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.nextRewardAmountCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.manualRewardAmountCents === 'number') parts.push(`${rewardLabel}: ${referralCurrency((metadata.manualRewardAmountCents / 100).toFixed(2))}`);
      if (metadata.previousStatus || metadata.nextStatus) {
        parts.push(`${referralLabel(labels.caseStatuses, metadata.previousStatus, metadata.previousStatus || '—')} → ${referralLabel(labels.caseStatuses, metadata.nextStatus, metadata.nextStatus || '—')}`);
      } else if (metadata.status) {
        parts.push(referralLabel(labels.caseStatuses, metadata.status, metadata.status));
      }
      if (metadata.note) parts.push(metadata.note);
      if (parts.length) return parts.join(' · ');
      return '—';
    };
    const requestJson = async (url, init = {}) => {
      const response = await fetch(resolveAdminUrl(url), {
        headers: { Accept: 'application/json', ...(init.headers || {}) },
        ...init,
      });
      const payload = await response.json();
      if (!response.ok || !payload.ok) {
        throw new Error(payload.error || copy.genericError || '');
      }
      return payload;
    };
    const applyAccountStatus = async (accountId, statusValue) => {
      return requestJson(shell.dataset.accountStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, status: statusValue }),
      });
    };
    const adjustAccountBalance = async (accountId, deltaCad, note) => {
      return requestJson(shell.dataset.accountBalanceAdjustUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, deltaCad, note }),
      });
    };
    const createManualCase = async (payload) => {
      return requestJson(shell.dataset.caseCreateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const updateManualCase = async (payload) => {
      return requestJson(shell.dataset.caseUpdateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const applyCaseStatus = async (caseId, statusValue, subtotal, quoteReference) => {
      return requestJson(shell.dataset.caseStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId, status: statusValue, quotedSubtotalCad: subtotal, quoteReference }),
      });
    };
    const adjustCaseReward = async (caseId, amountCad, note, clearOverride = false) => {
      return requestJson(shell.dataset.caseRewardAdjustUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId, amountCad, note, clearOverride }),
      });
    };
    const settleReward = async (rewardId) => {
      return requestJson(shell.dataset.rewardSettleUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ rewardId }),
      });
    };
    const changeApplicationStatus = async (applicationId, nextStatus) => {
      return requestJson(shell.dataset.applicationStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ applicationId, status: nextStatus }),
      });
    };
    const deleteApplication = async (applicationId) => {
      return requestJson(shell.dataset.applicationDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ applicationId }),
      });
    };
    const createAccount = async (payload) => {
      return requestJson(shell.dataset.accountCreateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const resetAccountAccess = async (accountId) => {
      return requestJson(shell.dataset.accountResetAccessUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, sendSetupLink: true }),
      });
    };
    const deleteAccount = async (accountId) => {
      return requestJson(shell.dataset.accountDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId }),
      });
    };
    const deleteCase = async (caseId) => {
      return requestJson(shell.dataset.caseDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId }),
      });
    };
    const downloadAccount = (accountId) => {
      const url = new URL(resolveAdminUrl(shell.dataset.accountExportUrl));
      url.searchParams.set('accountId', String(accountId));
      window.location.assign(url.toString());
    };
    const fetchAccountDetail = async (accountId) => {
      const url = new URL(resolveAdminUrl(shell.dataset.accountDetailUrl || shell.dataset.accountExportUrl));
      url.searchParams.set('accountId', String(accountId));
      const response = await fetch(url.toString(), { headers: { Accept: 'application/json' } });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || copy.genericError || '');
      }
      return payload;
    };
    const actionStack = () => {
      const wrap = document.createElement('div');
      wrap.className = 'referral-admin-action-stack';
      return wrap;
    };
    const makeButton = (label, className = 'button button-secondary') => {
      const button = document.createElement('button');
      button.className = className;
      button.type = 'button';
      button.textContent = label;
      return button;
    };
    const resetCaseForm = () => {
      selectedCaseId = null;
      if (!detailCaseForm) return;
      detailCaseForm.reset();
      const statusField = detailCaseForm.elements.namedItem('status');
      if (statusField) statusField.value = 'new';
      const referralCodeField = detailCaseForm.elements.namedItem('referral_code');
      if (referralCodeField) referralCodeField.value = selectedAccount?.current_code || '';
      if (detailCaseSubmit) detailCaseSubmit.textContent = copy.actions.saveCase || 'Add project';
      if (detailCaseCancel) detailCaseCancel.hidden = true;
      if (detailCaseState) detailCaseState.textContent = '';
    };
    const beginCaseEdit = (item) => {
      if (!detailCaseForm) return;
      selectedCaseId = Number(item.id);
      const normalizedStatus = item.status === 'won' ? 'accepted' : (item.status || 'new');
      detailCaseForm.elements.namedItem('referral_code').value = item.referral_code || selectedAccount?.current_code || '';
      detailCaseForm.elements.namedItem('referred_name').value = item.referred_name || '';
      detailCaseForm.elements.namedItem('referred_email').value = item.referred_email || '';
      detailCaseForm.elements.namedItem('referred_phone').value = item.referred_phone || '';
      detailCaseForm.elements.namedItem('referred_company').value = item.referred_company || '';
      detailCaseForm.elements.namedItem('quote_reference').value = item.quote_reference || '';
      detailCaseForm.elements.namedItem('status').value = normalizedStatus;
      detailCaseForm.elements.namedItem('quoted_subtotal').value = item.quoted_subtotal_cents == null ? '' : (Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2);
      detailCaseForm.elements.namedItem('manual_reward').value = item.manual_reward_amount_cents == null ? '' : (Number(item.manual_reward_amount_cents || 0) / 100).toFixed(2);
      detailCaseForm.elements.namedItem('note').value = item.referred_project_notes || item.manual_reward_note || '';
      if (detailCaseSubmit) detailCaseSubmit.textContent = copy.actions.updateCase || 'Update project';
      if (detailCaseCancel) detailCaseCancel.hidden = false;
      if (detailCaseState) detailCaseState.textContent = `${copy.labels?.caseIdLabel || 'Project ID'}: ${item.id}`;
      detailCaseForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    const applyRowFilters = () => {
      Array.from(applicationsBody.querySelectorAll('tr')).forEach((row) => {
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const statusMatch = !applicationStatusFilter || applicationStatusFilter.value === 'all' || statusValue === applicationStatusFilter.value;
        const searchMatch = !applicationSearchFilter || !applicationSearchFilter.value.trim() || searchValue.includes(applicationSearchFilter.value.trim().toLowerCase());
        row.hidden = !(statusMatch && searchMatch);
      });
      Array.from(accountsBody.querySelectorAll('tr')).forEach((row) => {
        const programValue = row.dataset.program || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const programMatch = !accountProgramFilter || accountProgramFilter.value === 'all' || programValue === accountProgramFilter.value;
        const statusMatch = !accountStatusFilter || accountStatusFilter.value === 'all' || statusValue === accountStatusFilter.value;
        const searchMatch = !accountSearchFilter || !accountSearchFilter.value.trim() || searchValue.includes(accountSearchFilter.value.trim().toLowerCase());
        row.hidden = !(programMatch && statusMatch && searchMatch);
      });
      Array.from(casesBody.querySelectorAll('tr')).forEach((row) => {
        const programValue = row.dataset.program || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const programMatch = !caseProgramFilter || caseProgramFilter.value === 'all' || programValue === caseProgramFilter.value;
        const statusMatch = !caseStatusFilter || caseStatusFilter.value === 'all' || statusValue === caseStatusFilter.value;
        const searchMatch = !caseSearchFilter || !caseSearchFilter.value.trim() || searchValue.includes(caseSearchFilter.value.trim().toLowerCase());
        row.hidden = !(programMatch && statusMatch && searchMatch);
      });
      Array.from(rewardsBody.querySelectorAll('tr')).forEach((row) => {
        const typeValue = row.dataset.type || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const typeMatch = !rewardTypeFilter || rewardTypeFilter.value === 'all' || typeValue === rewardTypeFilter.value;
        const statusMatch = !rewardStatusFilter || rewardStatusFilter.value === 'all' || statusValue === rewardStatusFilter.value;
        const searchMatch = !rewardSearchFilter || !rewardSearchFilter.value.trim() || searchValue.includes(rewardSearchFilter.value.trim().toLowerCase());
        row.hidden = !(typeMatch && statusMatch && searchMatch);
      });
    };
    const renderAccountDetail = (payload) => {
      const account = payload.account || {};
      const rollup = payload.rollup || {};
      const rewardRows = payload.rewards || [];
      const auditRows = payload.auditEvents || [];
      const isPartner = account.account_type === 'partner';
      const pendingPayoutCents = rewardRows
        .filter((item) => item.reward_type === 'payout' && item.status === 'earned')
        .reduce((sum, item) => sum + Number(item.amount_cents || 0), 0);
      const totalPayoutCents = rewardRows
        .filter((item) => item.reward_type === 'payout' && (item.status === 'earned' || item.status === 'settled'))
        .reduce((sum, item) => sum + Number(item.amount_cents || 0), 0);
      selectedAccountId = account.id || null;
      selectedAccount = account;
      resetCaseForm();
      if (detailEmpty) detailEmpty.hidden = true;
      if (detailWrap) detailWrap.hidden = false;
      if (detailName) detailName.textContent = account.name || account.email || '—';
      if (detailMeta) detailMeta.textContent = `${programLabel(account.account_type)} · ${referralLabel(labels.accountStatuses, account.status, account.status || '—')} · ${account.email || '—'}`;
      if (detailProgram) detailProgram.textContent = programLabel(account.account_type);
      if (detailStatus) detailStatus.textContent = referralLabel(labels.accountStatuses, account.status, account.status || '—');
      if (detailEmail) detailEmail.textContent = account.email || '—';
      if (detailPhone) detailPhone.textContent = account.phone || '—';
      if (detailCompany) detailCompany.textContent = account.company || '—';
      if (detailWebsite) detailWebsite.textContent = account.website || '—';
      if (detailShareCode) detailShareCode.textContent = account.current_code || '—';
      if (detailCreditCode) detailCreditCode.textContent = account.current_credit_code || '—';
      if (detailBalance) detailBalance.textContent = referralCurrency((Number(rollup.currentOutstandingCents || 0) / 100).toFixed(2));
      if (detailEarned) detailEarned.textContent = isPartner
        ? referralCurrency((Number(rollup.totalEarnedCents || totalPayoutCents) / 100).toFixed(2))
        : referralCurrency((Number(rollup.totalEarnedCents || 0) / 100).toFixed(2));
      if (detailCreated) detailCreated.textContent = referralDate(account.created_at, lang);
      if (detailLogin) detailLogin.textContent = referralDate(account.last_login_at, lang);
      if (detailNotes) detailNotes.textContent = account.notes || '—';
      if (detailCasesBody) {
        detailCasesBody.textContent = '';
        const rows = payload.referralCases || [];
        if (!rows.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 6;
          cell.textContent = '—';
          row.appendChild(cell);
          detailCasesBody.appendChild(row);
        } else {
          rows.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(item.id));
            row.appendChild(promoAdminTableCell(referralLabel(labels.caseStatuses, item.status, item.status || '—')));
            row.appendChild(promoAdminTableCell([
              item.quote_reference || '—',
              item.referred_name || '—',
              item.referred_company || '—',
            ].join(' · ')));
            row.appendChild(promoAdminTableCell(item.quoted_subtotal_cents == null ? '—' : referralCurrency((Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2))));
            row.appendChild(promoAdminTableCell(item.reward_amount_cents == null ? '—' : referralCurrency((Number(item.reward_amount_cents || 0) / 100).toFixed(2))));
            const actionCell = document.createElement('td');
            const stack = actionStack();
            const editButton = makeButton(copy.actions.editCase || 'Edit project');
            editButton.addEventListener('click', () => beginCaseEdit(item));
            stack.appendChild(editButton);
            const adjustButton = makeButton(copy.actions.adjustReward || 'Adjust amount');
            adjustButton.addEventListener('click', async () => {
              const currentValue = item.reward_amount_cents == null ? '' : (Number(item.reward_amount_cents || 0) / 100).toFixed(2);
              const amountRaw = window.prompt(copy.messages?.caseRewardPrompt || copy.genericError || '', currentValue);
              if (amountRaw == null) return;
              const normalized = String(amountRaw).trim().replace(',', '.');
              const note = window.prompt(copy.messages?.caseRewardNotePrompt || '', '') || '';
              try {
                if (!normalized) {
                  await adjustCaseReward(item.id, '', note, true);
                } else {
                  const amount = Number.parseFloat(normalized);
                  if (!Number.isFinite(amount) || amount < 0) {
                    setError(copy.messages?.caseRewardPrompt || copy.genericError || '');
                    return;
                  }
                  await adjustCaseReward(item.id, amount.toFixed(2), note, false);
                }
                setStatus(copy.messages?.caseRewardAdjusted || '');
                await loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(adjustButton);
            const deleteButton = makeButton(copy.actions.delete || 'Delete');
            deleteButton.addEventListener('click', async () => {
              if (!window.confirm(copy.messages?.confirmDeleteCase || 'Delete this project?')) return;
              try {
                await deleteCase(item.id);
                setStatus(copy.messages?.caseDeleted || '');
                await loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(deleteButton);
            actionCell.appendChild(stack);
            row.appendChild(actionCell);
            detailCasesBody.appendChild(row);
          });
        }
      }
      if (detailRewardsBody) {
        detailRewardsBody.textContent = '';
        const rewardLedger = [
          ...rewardRows.map((item) => ({
            id: item.id,
            status: referralLabel(labels.rewardStatuses, item.status, item.status || '—'),
            amount: referralCurrency((Number(item.amount_cents || 0) / 100).toFixed(2)),
            created: referralDateTime(item.created_at, lang),
            note: item.note || '—',
          })),
          ...auditRows
            .filter((item) => item.event_type === 'client_wallet_adjusted')
            .map((item) => {
              const metadata = parseMetadata(item.metadata_json);
              return {
                id: `audit-${item.id}`,
                status: lang === 'fr' ? 'Solde ajusté' : 'Balance adjusted',
                amount: referralCurrency(((Number(metadata.deltaCents || 0)) / 100).toFixed(2)),
                created: referralDateTime(item.created_at, lang),
                note: metadata.note || '—',
              };
            }),
        ];
        if (!rewardLedger.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 5;
          cell.textContent = '—';
          row.appendChild(cell);
          detailRewardsBody.appendChild(row);
        } else {
          rewardLedger.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(item.id));
            row.appendChild(promoAdminTableCell(item.status));
            row.appendChild(promoAdminTableCell(item.amount));
            row.appendChild(promoAdminTableCell(item.created));
            row.appendChild(promoAdminTableCell(item.note));
            detailRewardsBody.appendChild(row);
          });
        }
      }
      if (detailAuditBody) {
        detailAuditBody.textContent = '';
        if (!auditRows.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 3;
          cell.textContent = '—';
          row.appendChild(cell);
          detailAuditBody.appendChild(row);
        } else {
          auditRows.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(referralDateTime(item.created_at, lang)));
            row.appendChild(promoAdminTableCell(item.event_type || '—'));
            row.appendChild(promoAdminTableCell(auditNote(item)));
            detailAuditBody.appendChild(row);
          });
        }
      }
    };
    const openAccountDetail = async (accountId) => {
      try {
        setError('');
        setStatus(copy.messages?.detailLoading || copy.loading || 'Loading…');
        const payload = await fetchAccountDetail(accountId);
        renderAccountDetail(payload);
        setStatus('');
        return payload;
      } catch (error) {
        setError(error.message || copy.genericError || '');
        setStatus('');
        return null;
      }
    };
    const loadAll = async () => {
      setError('');
      setStatus(copy.loading || 'Loading…');
      try {
        const [summaryResponse, applicationsResponse, accountsResponse, casesResponse, rewardsResponse] = await Promise.all([
          fetch(resolveAdminUrl(shell.dataset.summaryUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.applicationsUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.accountsUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.casesUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.rewardsUrl), { headers: { Accept: 'application/json' } }),
        ]);
        const [summaryPayload, applicationsPayload, accountsPayload, casesPayload, rewardsPayload] = await Promise.all([
          summaryResponse.json(),
          applicationsResponse.json(),
          accountsResponse.json(),
          casesResponse.json(),
          rewardsResponse.json(),
        ]);
        if (!summaryResponse.ok || !applicationsResponse.ok || !accountsResponse.ok || !casesResponse.ok || !rewardsResponse.ok) {
          throw new Error(summaryPayload.error || applicationsPayload.error || accountsPayload.error || casesPayload.error || rewardsPayload.error || copy.genericError || '');
        }
        shell.querySelector('[data-referral-summary-active]').textContent = String(summaryPayload.summary.activeAccounts || 0);
        shell.querySelector('[data-referral-summary-pending]').textContent = String(summaryPayload.summary.pendingPartners || 0);
        shell.querySelector('[data-referral-summary-open]').textContent = String(summaryPayload.summary.openCases || 0);
        shell.querySelector('[data-referral-summary-payouts]').textContent = referralCurrency(summaryPayload.summary.pendingPayoutCad);
        applicationsBody.textContent = '';
        (applicationsPayload.applications || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.name, item.email, item.company);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(referralLabel(labels.applicationStatuses, item.status, item.status || '—')));
          row.appendChild(promoAdminTableCell(item.name || '—'));
          row.appendChild(promoAdminTableCell(item.email || '—'));
          row.appendChild(promoAdminTableCell(item.company || '—'));
          row.appendChild(promoAdminTableCell(referralDate(item.created_at, lang)));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const createButton = makeButton(copy.actions.createAccount || 'Create account');
          createButton.addEventListener('click', async () => {
            try {
              const payload = await createAccount({ applicationId: item.id, status: 'active', sendSetupLink: true });
              setStatus(payload.message || copy.messages?.accountCreated || '');
              await loadAll();
              if (payload?.account?.id) {
                await openAccountDetail(payload.account.id);
              }
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(createButton);
          const rejectButton = makeButton(copy.actions.reject || 'Reject');
          rejectButton.addEventListener('click', async () => {
            try {
              await changeApplicationStatus(item.id, 'rejected');
              setStatus(copy.messages?.applicationUpdated || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(rejectButton);
          const voidButton = makeButton(copy.actions.delete || 'Delete');
          voidButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteApplication || 'Delete this partner application?')) return;
            try {
              await deleteApplication(item.id);
              setStatus(copy.messages?.applicationDeleted || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(voidButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          applicationsBody.appendChild(row);
        });
        accountsBody.textContent = '';
        (accountsPayload.accounts || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.program = item.account_type || '';
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.name, item.email, item.company, item.current_code, item.current_credit_code);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(programLabel(item.account_type)));
          const statusCell = document.createElement('td');
          const select = document.createElement('select');
          ['pending', 'active', 'paused', 'rejected'].forEach((value) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = referralLabel(labels.accountStatuses, value, value);
            option.selected = value === item.status;
            select.appendChild(option);
          });
          statusCell.appendChild(select);
          row.appendChild(statusCell);
          const nameCell = document.createElement('td');
          const nameButton = makeButton(item.name || '—', 'button button-link referral-admin-view-button');
          nameButton.addEventListener('click', async () => {
            await openAccountDetail(item.id);
          });
          nameCell.appendChild(nameButton);
          row.appendChild(nameCell);
          row.appendChild(promoAdminTableCell(item.email || '—'));
          const codeCell = document.createElement('td');
          const codeWrap = document.createElement('div');
          codeWrap.className = 'referral-admin-code-stack';
          const shareCode = document.createElement('p');
          shareCode.className = 'promo-admin-code';
          shareCode.textContent = item.current_code || '—';
          codeWrap.appendChild(shareCode);
          if (item.current_credit_code) {
            const creditCode = document.createElement('p');
            creditCode.className = 'promo-admin-code';
            creditCode.textContent = item.current_credit_code;
            codeWrap.appendChild(creditCode);
          }
          codeCell.appendChild(codeWrap);
          row.appendChild(codeCell);
          row.appendChild(promoAdminTableCell(
            referralCurrency((Number(item.current_outstanding_cents || 0) / 100).toFixed(2))
          ));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const applyButton = makeButton(copy.actions.apply || 'Apply');
          applyButton.addEventListener('click', async () => {
            try {
              await applyAccountStatus(item.id, select.value);
              setStatus(copy.messages?.accountUpdated || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(applyButton);
          if (item.account_type === 'client') {
            const adjustButton = makeButton(copy.actions.adjustCredit || 'Adjust credit');
            adjustButton.addEventListener('click', async () => {
              const amountLabel = copy.messages?.creditAdjustPrompt || copy.genericError || '';
              const amountRaw = window.prompt(amountLabel, '');
              if (amountRaw == null) return;
              const normalized = String(amountRaw).trim().replace(',', '.');
              if (!normalized) return;
              const amount = Number.parseFloat(normalized);
              if (!Number.isFinite(amount) || amount === 0) {
                setError(copy.messages?.creditAdjustPrompt || copy.genericError || '');
                return;
              }
              const note = window.prompt(copy.messages?.creditAdjustNotePrompt || '', '') || '';
              try {
                await adjustAccountBalance(item.id, amount.toFixed(2), note);
                setStatus(copy.messages?.creditAdjusted || '');
                loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(adjustButton);
          }
          const exportButton = makeButton(copy.actions.exportOne || 'Download');
          exportButton.addEventListener('click', () => downloadAccount(item.id));
          stack.appendChild(exportButton);
          const detailButton = makeButton(copy.actions.viewDetails || 'View details');
          detailButton.addEventListener('click', async () => {
            await openAccountDetail(item.id);
          });
          stack.appendChild(detailButton);
          const resetButton = makeButton(copy.actions.resetAccess || 'Reset access');
          resetButton.disabled = item.status !== 'active';
          resetButton.addEventListener('click', async () => {
            try {
              const payload = await resetAccountAccess(item.id);
              setStatus(payload.message || copy.messages?.accessReset || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(resetButton);
          const deleteButton = makeButton(copy.actions.delete || 'Delete');
          deleteButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteAccount || 'Delete this account and all related referral data?')) return;
            try {
              await deleteAccount(item.id);
              setStatus(copy.messages?.accountDeleted || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(deleteButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          accountsBody.appendChild(row);
        });
        casesBody.textContent = '';
        (casesPayload.cases || []).forEach((item) => {
          const normalizedCaseStatus = item.status === 'won' ? 'accepted' : (item.status || '');
          const row = document.createElement('tr');
          row.dataset.program = item.account_type || '';
          row.dataset.status = normalizedCaseStatus;
          row.dataset.search = searchBlob(item.account_name, item.account_email, item.referral_code, item.quote_reference, item.referred_name, item.referred_email, item.referred_company);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(`${item.account_name || '—'} (${item.account_email || '—'})`));
          row.appendChild(promoAdminTableCell(item.referral_code || '—', 'promo-admin-code'));
          const statusCell = document.createElement('td');
          const statusSelect = document.createElement('select');
          ['new', 'quoted', 'accepted', 'completed_paid', 'member_paid', 'void'].forEach((value) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = referralLabel(labels.caseStatuses, value, value);
            option.selected = value === normalizedCaseStatus;
            statusSelect.appendChild(option);
          });
          statusCell.appendChild(statusSelect);
          row.appendChild(statusCell);
          const subtotalCell = document.createElement('td');
          const subtotalInput = document.createElement('input');
          subtotalInput.type = 'number';
          subtotalInput.step = '0.01';
          subtotalInput.value = item.quoted_subtotal_cents == null ? '' : (Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2);
          subtotalCell.appendChild(subtotalInput);
          row.appendChild(subtotalCell);
          const refCell = document.createElement('td');
          const refInput = document.createElement('input');
          refInput.value = item.quote_reference || '';
          refCell.appendChild(refInput);
          const refMeta = document.createElement('div');
          refMeta.className = 'form-note';
          refMeta.textContent = [item.referred_name || '—', item.referred_company || '—'].join(' · ');
          refCell.appendChild(refMeta);
          row.appendChild(refCell);
          row.appendChild(promoAdminTableCell(item.reward_amount_cents == null ? '—' : referralCurrency((Number(item.reward_amount_cents || 0) / 100).toFixed(2))));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const editButton = makeButton(copy.actions.editCase || 'Edit project');
          editButton.addEventListener('click', async () => {
            const payload = await openAccountDetail(item.account_id);
            const match = (payload?.referralCases || []).find((entry) => Number(entry.id) === Number(item.id));
            if (match) beginCaseEdit(match);
          });
          stack.appendChild(editButton);
          const button = document.createElement('button');
          button.className = 'button button-secondary';
          button.type = 'button';
          button.textContent = copy.actions.apply || 'Apply';
          button.addEventListener('click', async () => {
            try {
              await applyCaseStatus(item.id, statusSelect.value, subtotalInput.value, refInput.value);
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(button);
          const adjustRewardButton = makeButton(copy.actions.adjustReward || 'Adjust amount');
          adjustRewardButton.addEventListener('click', async () => {
            const currentValue = item.reward_amount_cents == null ? '' : (Number(item.reward_amount_cents || 0) / 100).toFixed(2);
            const amountRaw = window.prompt(copy.messages?.caseRewardPrompt || copy.genericError || '', currentValue);
            if (amountRaw == null) return;
            const normalized = String(amountRaw).trim().replace(',', '.');
            const note = window.prompt(copy.messages?.caseRewardNotePrompt || '', '') || '';
            try {
              if (!normalized) {
                await adjustCaseReward(item.id, '', note, true);
              } else {
                const amount = Number.parseFloat(normalized);
                if (!Number.isFinite(amount) || amount < 0) {
                  setError(copy.messages?.caseRewardPrompt || copy.genericError || '');
                  return;
                }
                await adjustCaseReward(item.id, amount.toFixed(2), note, false);
              }
              setStatus(copy.messages?.caseRewardAdjusted || '');
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(adjustRewardButton);
          const deleteButton = makeButton(copy.actions.delete || 'Delete');
          deleteButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteCase || 'Delete this referral case?')) return;
            try {
              await deleteCase(item.id);
              setStatus(copy.messages?.caseDeleted || '');
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(deleteButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          casesBody.appendChild(row);
        });
        rewardsBody.textContent = '';
        (rewardsPayload.rewards || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.type = item.reward_type || '';
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.account_name, item.account_email, item.note, item.reward_type);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(`${item.account_name || '—'} (${item.account_email || '—'})`));
          row.appendChild(promoAdminTableCell(referralLabel(labels.rewardTypes, item.reward_type, item.reward_type || '—')));
          row.appendChild(promoAdminTableCell(referralLabel(labels.rewardStatuses, item.status, item.status || '—')));
          row.appendChild(promoAdminTableCell(referralCurrency((Number(item.amount_cents || 0) / 100).toFixed(2))));
          row.appendChild(promoAdminTableCell(item.note || '—'));
          const actionCell = document.createElement('td');
          if (item.reward_type === 'payout' && item.status === 'earned') {
            const button = document.createElement('button');
            button.className = 'button button-secondary';
            button.type = 'button';
            button.textContent = copy.actions.settle || 'Settle';
            button.addEventListener('click', async () => {
              try {
                await settleReward(item.id);
                loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            actionCell.appendChild(button);
          } else {
            actionCell.textContent = '—';
          }
          row.appendChild(actionCell);
          rewardsBody.appendChild(row);
        });
        applyRowFilters();
        if (selectedAccountId) {
          await openAccountDetail(selectedAccountId);
        } else {
          setDetailEmptyState(copy.messages?.detailEmpty || '');
        }
        setStatus('');
      } catch (error) {
        setError(error.message || copy.genericError || '');
        setStatus('');
      }
    };
    [
      applicationStatusFilter,
      applicationSearchFilter,
      accountProgramFilter,
      accountStatusFilter,
      accountSearchFilter,
      caseProgramFilter,
      caseStatusFilter,
      caseSearchFilter,
      rewardTypeFilter,
      rewardStatusFilter,
      rewardSearchFilter,
    ].filter(Boolean).forEach((control) => {
      control.addEventListener('input', applyRowFilters);
      control.addEventListener('change', applyRowFilters);
    });
    refreshButton.addEventListener('click', loadAll);
    if (detailExportButton) {
      detailExportButton.addEventListener('click', () => {
        if (!selectedAccountId) return;
        downloadAccount(selectedAccountId);
      });
    }
    if (detailResetButton) {
      detailResetButton.addEventListener('click', async () => {
        if (!selectedAccountId) return;
        try {
          const payload = await resetAccountAccess(selectedAccountId);
          setStatus(payload.message || copy.messages?.accessReset || '');
          await loadAll();
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailDeleteButton) {
      detailDeleteButton.addEventListener('click', async () => {
        if (!selectedAccountId) return;
        if (!window.confirm(copy.messages?.confirmDeleteAccount || 'Delete this account and all related referral data?')) return;
        try {
          await deleteAccount(selectedAccountId);
          selectedAccountId = null;
          setStatus(copy.messages?.accountDeleted || '');
          setDetailEmptyState(copy.messages?.detailEmpty || '');
          await loadAll();
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailCaseForm) {
      detailCaseForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!selectedAccountId || !selectedAccount) {
          setError(copy.messages?.detailEmpty || copy.genericError || '');
          return;
        }
        const referralCode = String(detailCaseForm.elements.namedItem('referral_code').value || '').trim().toUpperCase();
        const referredName = String(detailCaseForm.elements.namedItem('referred_name').value || '').trim();
        const referredEmail = String(detailCaseForm.elements.namedItem('referred_email').value || '').trim();
        const referredPhone = String(detailCaseForm.elements.namedItem('referred_phone').value || '').trim();
        const referredCompany = String(detailCaseForm.elements.namedItem('referred_company').value || '').trim();
        const quoteReference = String(detailCaseForm.elements.namedItem('quote_reference').value || '').trim();
        const statusValue = String(detailCaseForm.elements.namedItem('status').value || 'new');
        const subtotal = String(detailCaseForm.elements.namedItem('quoted_subtotal').value || '').trim();
        const manualReward = String(detailCaseForm.elements.namedItem('manual_reward').value || '').trim();
        const note = String(detailCaseForm.elements.namedItem('note').value || '').trim();
        if (!referralCode || !referredName || !referredEmail || !referredCompany) {
          setError(copy.messages?.caseCreateRequired || copy.genericError || '');
          return;
        }
        if (statusValue === 'completed_paid' && !subtotal) {
          setError(copy.messages?.caseCreateSubtotalRequired || copy.genericError || '');
          return;
        }
        try {
          let successMessage = '';
          if (selectedCaseId) {
            const payload = await updateManualCase({
              caseId: selectedCaseId,
              accountId: selectedAccountId,
              locale: selectedAccount.locale || lang,
              referralCode,
              referredName,
              referredEmail,
              referredPhone,
              referredCompany,
              quoteReference,
              status: statusValue,
              quotedSubtotalCad: subtotal,
              manualRewardCad: manualReward,
              note,
            });
            successMessage = `${copy.messages?.caseUpdated || ''} #${payload?.referralCase?.id || selectedCaseId} ${quoteReference || referredName || ''}`.trim();
          } else {
            const payload = await createManualCase({
              accountId: selectedAccountId,
              locale: selectedAccount.locale || lang,
              referralCode,
              referredName,
              referredEmail,
              referredPhone,
              referredCompany,
              quoteReference,
              status: statusValue,
              quotedSubtotalCad: subtotal,
              manualRewardCad: manualReward,
              note,
            });
            successMessage = `${copy.messages?.caseCreated || ''} #${payload?.referralCase?.id || ''} ${quoteReference || referredName || ''}`.trim();
          }
          resetCaseForm();
          await loadAll();
          setStatus(successMessage);
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailCaseCancel) {
      detailCaseCancel.addEventListener('click', () => {
        clearMessages();
        resetCaseForm();
      });
    }
    createForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setError('');
      const accountType = String(createForm.elements.namedItem('account_type').value || 'client');
      const locale = String(createForm.elements.namedItem('locale').value || 'fr');
      const name = String(createForm.elements.namedItem('name').value || '').trim();
      const email = String(createForm.elements.namedItem('email').value || '').trim();
      const phone = String(createForm.elements.namedItem('phone').value || '').trim();
      const company = String(createForm.elements.namedItem('company').value || '').trim();
      const website = String(createForm.elements.namedItem('website').value || '').trim();
      const notes = String(createForm.elements.namedItem('notes').value || '').trim();
      const statusValue = String(createForm.elements.namedItem('status').value || 'active');
      const sendSetupLink = Boolean(createForm.elements.namedItem('send_setup_link').checked);
      if (!name || !email) {
        setError(copy.messages?.createAccountRequired || copy.genericError || '');
        return;
      }
      if (accountType === 'partner' && !company) {
        setError(copy.messages?.createPartnerCompanyRequired || copy.genericError || '');
        return;
      }
      try {
        const payload = await createAccount({
          accountType,
          locale,
          status: statusValue,
          name,
          email,
          phone,
          company,
          website,
          notes,
          sendSetupLink,
        });
        createForm.reset();
        createForm.elements.namedItem('account_type').value = 'client';
        createForm.elements.namedItem('locale').value = locale;
        createForm.elements.namedItem('status').value = 'active';
        createForm.elements.namedItem('send_setup_link').checked = true;
        setStatus(payload.message || copy.messages?.accountCreated || '');
        loadAll();
      } catch (error) {
        setError(error.message || copy.genericError || '');
      }
    });
    setDetailEmptyState(copy.messages?.detailEmpty || '');
    loadAll();
  });
}
async function initSiteConfig() {
  try {
    const response = await fetch('/api/site-config', { headers: { Accept: 'application/json' } });
    const config = await response.json();
    if (!config || !config.analyticsToken || document.querySelector('script[data-cf-beacon-script]')) {
      return;
    }
    const script = document.createElement('script');
    script.defer = true;
    script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    script.dataset.cfBeaconScript = 'true';
    script.setAttribute('data-cf-beacon', JSON.stringify({ token: config.analyticsToken }));
    document.head.appendChild(script);
  } catch (error) {}
}
initPromoForms();
initPromoUnsubscribe();
initPromoAdmin();
initReferralApplyForms();
initReferralPortal();
initReferralAccess();
initReferralAdmin();
initSiteConfig();
