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
initReferralAdmin();
