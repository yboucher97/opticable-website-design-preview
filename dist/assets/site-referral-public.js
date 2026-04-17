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
initReferralApplyForms();
