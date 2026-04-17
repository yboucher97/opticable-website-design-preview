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
    let referralAdminDetailTools = null;
    let referralAdminDetailToolsPromise = null;
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
    const loadAdminDetailScript = (src) => new Promise((resolve, reject) => {
      const existing = document.querySelector(`[data-referral-admin-detail-src="${src}"]`);
      const handleLoad = () => resolve();
      const handleError = () => reject(new Error(copy.genericError || ''));
      if (existing) {
        if (existing.dataset.loaded === 'true') {
          resolve();
          return;
        }
        existing.addEventListener('load', handleLoad, { once: true });
        existing.addEventListener('error', handleError, { once: true });
        return;
      }
      const script = document.createElement('script');
      script.src = src;
      script.defer = true;
      script.dataset.referralAdminDetailSrc = src;
      script.addEventListener('load', () => {
        script.dataset.loaded = 'true';
        resolve();
      }, { once: true });
      script.addEventListener('error', handleError, { once: true });
      document.head.appendChild(script);
    });
    const ensureReferralAdminDetailTools = async () => {
      if (referralAdminDetailTools) return referralAdminDetailTools;
      if (!referralAdminDetailToolsPromise) {
        referralAdminDetailToolsPromise = (async () => {
          const scriptUrl = shell.dataset.referralAdminDetailScript || '';
          if (!scriptUrl) {
            throw new Error(copy.genericError || '');
          }
          if (typeof window.createReferralAdminDetailTools !== 'function') {
            await loadAdminDetailScript(scriptUrl);
          }
          if (typeof window.createReferralAdminDetailTools !== 'function') {
            throw new Error(copy.genericError || '');
          }
          referralAdminDetailTools = window.createReferralAdminDetailTools({
            copy,
            lang,
            labels,
            state: {
              get selectedAccountId() { return selectedAccountId; },
              set selectedAccountId(value) { selectedAccountId = value; },
              get selectedAccount() { return selectedAccount; },
              set selectedAccount(value) { selectedAccount = value; },
              get selectedCaseId() { return selectedCaseId; },
              set selectedCaseId(value) { selectedCaseId = value; },
            },
            detailEmpty,
            detailWrap,
            detailName,
            detailMeta,
            detailProgram,
            detailStatus,
            detailEmail,
            detailPhone,
            detailCompany,
            detailWebsite,
            detailShareCode,
            detailCreditCode,
            detailBalance,
            detailEarned,
            detailCreated,
            detailLogin,
            detailNotes,
            detailCasesBody,
            detailRewardsBody,
            detailAuditBody,
            detailExportButton,
            detailResetButton,
            detailDeleteButton,
            detailCaseForm,
            detailCaseSubmit,
            detailCaseCancel,
            detailCaseState,
            setStatus,
            setError,
            clearMessages,
            resetAccountAccess,
            deleteAccount,
            createManualCase,
            updateManualCase,
            adjustCaseReward,
            deleteCase,
            downloadAccount,
            fetchAccountDetail,
            actionStack,
            makeButton,
            programLabel,
            parseMetadata,
            auditNote,
            loadAll: async () => loadAll(),
          });
          return referralAdminDetailTools;
        })().catch((error) => {
          referralAdminDetailToolsPromise = null;
          throw error;
        });
      }
      return referralAdminDetailToolsPromise;
    };
    const openAccountDetail = async (accountId) => {
      try {
        const tools = await ensureReferralAdminDetailTools();
        return await tools.openAccountDetail(accountId);
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
            if (match) {
              const detailTools = await ensureReferralAdminDetailTools();
              detailTools.beginCaseEdit(match);
            }
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
initReferralAdmin();
