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
        shell.querySelector('[data-referral-stat-tertiary]').textContent = referralCurrency('1000.00');
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
        const payload = await response.json();
        if (response.status === 401 || payload.authRequired) {
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
        shell.querySelector('[data-referral-credit-panel-cap]').textContent = referralCurrency('1000.00');
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
        const payload = await response.json();
        if (response.status === 401 || payload.authRequired) {
          showRequest(authMessage() || copy.notReady || '', Boolean(authMessage()));
          return;
        }
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
    if (authState || query.searchParams.get('reset') === 'ready') {
      loadAccessState();
    } else {
      showRequest(copy.notReady || '', false);
    }
  });
}
initReferralPortal();
initReferralAccess();
