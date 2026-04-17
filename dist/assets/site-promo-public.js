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
initPromoForms();
