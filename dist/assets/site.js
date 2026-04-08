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
      if (!form.elements.namedItem('business_attestation').checked || !form.elements.namedItem('quebec_attestation').checked || !form.elements.namedItem('rules_attestation').checked) {
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
        businessAttestation: form.elements.namedItem('business_attestation').checked,
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
    const deleteUrl = shell.dataset.deleteUrl;
    const status = shell.querySelector('[data-promo-admin-status]');
    const errorNode = shell.querySelector('[data-promo-admin-error]');
    const refreshButton = shell.querySelector('[data-promo-admin-refresh]');
    const exportLink = shell.querySelector('[data-promo-admin-export]');
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
    if (!entriesUrl || !exportUrl || !deleteUrl || !status || !errorNode || !refreshButton || !exportLink || !deleteSelectedButton || !deleteViewButton || !selectAll || !tableBody) {
      return;
    }
    let currentScope = 'current';
    let activeRows = [];
    const selectedIds = new Set();
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
      exportLink.setAttribute('aria-disabled', busy ? 'true' : 'false');
      if (busy) {
        exportLink.classList.add('is-disabled');
      } else {
        exportLink.classList.remove('is-disabled');
      }
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
initSiteConfig();
