/* Sign-in form for /customer/login/ and /admin/login/.
 * The form declares its endpoint + fields; this script posts JSON, shows a
 * loading state, announces errors (role="alert") and redirects on success. */
(function () {
  'use strict';
  var form = document.querySelector('form[data-login]');
  if (!form) return;

  var endpoint = form.getAttribute('data-endpoint');
  var home = form.getAttribute('data-home');           // e.g. /customer/
  var errorBox = document.getElementById('login-error');
  var button = form.querySelector('button[type="submit"]');
  var buttonLabel = button.innerHTML;

  // Only same-section relative targets (no open redirect).
  function nextUrl() {
    var n = new URLSearchParams(window.location.search).get('next') || '';
    if (n.indexOf(home) === 0 && n.indexOf('//') !== 0 && n.indexOf('\\') === -1) return n;
    return home;
  }

  function showError(msg, field) {
    errorBox.hidden = false;
    errorBox.querySelector('[data-msg]').textContent = msg;
    form.querySelectorAll('.input').forEach(function (i) { i.removeAttribute('aria-invalid'); });
    if (field) {
      field.setAttribute('aria-invalid', 'true');
      field.focus();
    }
  }

  function setBusy(busy) {
    button.disabled = busy;
    button.innerHTML = busy ? '<span class="spinner" aria-hidden="true"></span><span>Signing in...</span>' : buttonLabel;
  }

  document.querySelectorAll('[data-toggle-password]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = document.getElementById(btn.getAttribute('data-toggle-password'));
      var show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      btn.setAttribute('aria-pressed', show ? 'true' : 'false');
      btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
      btn.querySelector('i').className = show ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye';
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var payload = {};
    var firstEmpty = null;
    form.querySelectorAll('[data-field]').forEach(function (input) {
      payload[input.getAttribute('data-field')] = input.value;
      if (!input.value.trim() && !firstEmpty) firstEmpty = input;
    });
    if (firstEmpty) {
      showError('Please fill in both fields.', firstEmpty);
      return;
    }
    errorBox.hidden = true;
    setBusy(true);
    fetch(endpoint, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (body) { return { ok: r.ok, status: r.status, body: body }; });
      })
      .then(function (res) {
        if (res.ok) {
          button.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i><span>Signed in</span>';
          window.location.assign(nextUrl());
          return;
        }
        setBusy(false);
        var pw = form.querySelector('input[type="password"], input[data-field="password"]');
        showError(res.body.error || 'Sign-in failed. Please try again.', res.status === 401 ? pw : null);
      })
      .catch(function () {
        setBusy(false);
        showError('Could not reach the server. Check your connection and try again.');
      });
  });
})();
