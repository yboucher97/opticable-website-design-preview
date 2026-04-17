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
initPromoAdmin();
