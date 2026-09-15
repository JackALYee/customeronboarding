/* Onboarding admin - talks to /api/admin/* (gated by functions/api/admin/_middleware.js). */
(function () {
  'use strict';

  var AUDIENCE = { fleet: 'Fleet Operator', tsp: 'TSP / Channel Partner' };
  var DEFAULT_CONTACTS = [
    { role: 'Customer Success', contact: 'csm@streamax.com' },
    { role: 'Technical Support', contact: 'support@streamax.com' },
    { role: 'Hardware RMA', contact: 'rma@streamax.com' },
    { role: 'Billing', contact: 'billing@streamax.com' },
    { role: 'Emergency hotline', contact: 'Available 24/7 via your CSM' }
  ];
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var MIN_PASSWORD = 8;

  var state = { customers: [], events: [], eventsTotal: 0, current: null, filter: '' };
  var $ = function (id) { return document.getElementById(id); };

  // ---------------------------------------------------------------- helpers
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function api(method, path, body) {
    var opts = { method: method, credentials: 'same-origin', headers: { 'Accept': 'application/json' } };
    if (body !== undefined) {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(body);
    }
    return fetch(path, opts).then(function (r) {
      if (r.status === 401) { window.location.href = '/admin/login/'; throw new Error('signed out'); }
      return r.json().catch(function () { return {}; }).then(function (data) {
        if (!r.ok) throw new Error(data.error || ('Request failed (' + r.status + ')'));
        return data;
      });
    });
  }

  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    return isNaN(d) ? '' : d.toLocaleString(undefined, { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  }

  function relTime(iso) {
    if (!iso) return '';
    var diff = (Date.now() - new Date(iso).getTime()) / 1000;
    if (isNaN(diff)) return '';
    if (diff < 60) return 'just now';
    var units = [[86400 * 365, 'year'], [86400 * 30, 'month'], [86400 * 7, 'week'], [86400, 'day'], [3600, 'hour'], [60, 'minute']];
    for (var i = 0; i < units.length; i++) {
      if (diff >= units[i][0]) {
        var n = Math.floor(diff / units[i][0]);
        return n + ' ' + units[i][1] + (n > 1 ? 's' : '') + ' ago';
      }
    }
    return 'just now';
  }

  function timeCell(iso, emptyLabel) {
    if (!iso) return '<span class="muted">' + (emptyLabel || 'Never') + '</span>';
    return '<time datetime="' + esc(iso) + '" title="' + esc(fmtDate(iso)) + '">' + esc(relTime(iso)) + '</time>';
  }

  function statusBadge(c) {
    if (c.disabled) return '<span class="badge badge-red"><span class="dot"></span>Access off</span>';
    if (!c.first_login_at) return '<span class="badge badge-amber"><span class="dot"></span>Not signed in yet</span>';
    return '<span class="badge badge-green"><span class="dot"></span>Active</span>';
  }

  function audienceBadge(a) {
    return a === 'tsp' ? '<span class="badge badge-blue">TSP</span>' : '<span class="badge badge-grey">Fleet</span>';
  }

  function toast(msg, isError) {
    var el = document.createElement('div');
    el.className = 'toast' + (isError ? ' toast-error' : '');
    el.setAttribute('role', isError ? 'alert' : 'status');
    el.innerHTML = '<i class="fa-solid ' + (isError ? 'fa-circle-exclamation' : 'fa-circle-check') + '" aria-hidden="true"></i><span></span>';
    el.querySelector('span').textContent = msg;
    $('toasts').appendChild(el);
    setTimeout(function () { el.remove(); }, isError ? 6000 : 3500);
  }

  function generatePassword() {
    var alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789';
    var bytes = new Uint32Array(14);
    crypto.getRandomValues(bytes);
    var out = '';
    for (var i = 0; i < bytes.length; i++) out += alphabet[bytes[i] % alphabet.length];
    return out.slice(0, 4) + '-' + out.slice(4, 9) + '-' + out.slice(9);
  }

  function busy(btn, on, label) {
    if (on) {
      btn.dataset.label = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner" aria-hidden="true"></span><span>' + (label || 'Saving...') + '</span>';
    } else {
      btn.disabled = false;
      if (btn.dataset.label) btn.innerHTML = btn.dataset.label;
    }
  }

  // ---------------------------------------------------------------- dialogs
  var lastFocus = null;
  function openLayer(id, focusSel) {
    lastFocus = document.activeElement;
    var layer = $(id);
    layer.hidden = false;
    document.body.style.overflow = 'hidden';
    var f = focusSel ? layer.querySelector(focusSel) : layer.querySelector('input, select, button');
    if (f) setTimeout(function () { f.focus(); }, 30);
  }
  function closeLayer(id) {
    $(id).hidden = true;
    if (!document.querySelector('.scrim:not([hidden])')) document.body.style.overflow = '';
    if (lastFocus && document.body.contains(lastFocus)) lastFocus.focus();
  }
  document.querySelectorAll('.scrim').forEach(function (scrim) {
    scrim.addEventListener('mousedown', function (e) { if (e.target === scrim) closeLayer(scrim.id); });
    scrim.querySelectorAll('[data-close]').forEach(function (b) {
      b.addEventListener('click', function () { closeLayer(scrim.id); });
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = Array.prototype.slice.call(document.querySelectorAll('.scrim:not([hidden])'));
    if (open.length) closeLayer(open[open.length - 1].id);
  });
  // Keep Tab inside the top-most open layer.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;
    var open = document.querySelectorAll('.scrim:not([hidden])');
    if (!open.length) return;
    var layer = open[open.length - 1];
    var f = layer.querySelectorAll('button:not([disabled]), [href], input:not([disabled]), select, textarea');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-toggle-password]');
    if (t) {
      var input = $(t.getAttribute('data-toggle-password'));
      var show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      t.setAttribute('aria-pressed', show ? 'true' : 'false');
      t.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
      t.querySelector('i').className = show ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye';
      return;
    }
    var g = e.target.closest('[data-generate]');
    if (g) {
      var target = $(g.getAttribute('data-generate'));
      target.value = generatePassword();
      target.type = 'text';
      var tog = document.querySelector('[data-toggle-password="' + target.id + '"]');
      if (tog) { tog.setAttribute('aria-pressed', 'true'); tog.querySelector('i').className = 'fa-solid fa-eye-slash'; }
      target.removeAttribute('aria-invalid');
      target.focus();
      target.select();
    }
  });

  // ---------------------------------------------------------------- tabs
  function selectTab(name, focus) {
    document.querySelectorAll('.adm-tab').forEach(function (t) {
      var on = t.getAttribute('data-tab') === name;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    $('panel-clients').hidden = name !== 'clients';
    $('panel-activity').hidden = name !== 'activity';
    if (history.replaceState) history.replaceState(null, '', name === 'activity' ? '#activity' : '#');
    if (name === 'activity') loadEvents();
  }
  document.querySelectorAll('.adm-tab').forEach(function (t, i, all) {
    t.addEventListener('click', function () { selectTab(t.getAttribute('data-tab')); });
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var next = all[(i + (e.key === 'ArrowRight' ? 1 : all.length - 1)) % all.length];
      selectTab(next.getAttribute('data-tab'), true);
    });
  });

  // ---------------------------------------------------------------- data
  function renderKpis() {
    var cs = state.customers;
    var fleet = cs.filter(function (c) { return c.audience !== 'tsp'; }).length;
    $('kpi-total').textContent = cs.length;
    $('kpi-split').innerHTML = fleet + '<span class="unit">fleet</span>' + (cs.length - fleet) + '<span class="unit">TSP</span>';
    $('kpi-active').textContent = cs.filter(function (c) { return !!c.first_login_at; }).length;
  }

  function renderClients() {
    var q = state.filter.trim().toLowerCase();
    var rows = state.customers.filter(function (c) {
      return !q || (c.company || '').toLowerCase().indexOf(q) > -1 || c.email.indexOf(q) > -1;
    });
    $('clients-count').textContent = state.customers.length ? '(' + state.customers.length + ')' : '';
    $('clients-empty').hidden = state.customers.length > 0;
    $('clients-nomatch').hidden = !(state.customers.length > 0 && rows.length === 0);
    $('clients-table').hidden = state.customers.length === 0 || rows.length === 0;
    $('clients-body').innerHTML = rows.map(function (c) {
      return '<tr>' +
        '<td class="cell-strong">' + esc(c.company || '-') + '</td>' +
        '<td>' + esc(c.email) + '</td>' +
        '<td>' + audienceBadge(c.audience) + '</td>' +
        '<td>' + statusBadge(c) + '</td>' +
        '<td class="tabular">' + timeCell(c.created_at, '-') + '</td>' +
        '<td class="tabular">' + timeCell(c.last_login_at) + '</td>' +
        '<td class="actions"><button class="btn btn-secondary btn-sm" type="button" data-manage="' + esc(c.email) + '">' +
        '<i class="fa-solid fa-sliders" aria-hidden="true"></i><span>Manage</span></button></td>' +
        '</tr>';
    }).join('');
  }

  function loadClients() {
    return api('GET', '/api/admin/customers').then(function (d) {
      state.customers = d.customers || [];
      renderKpis();
      renderClients();
    }).catch(function (e) { if (e.message !== 'signed out') toast(e.message, true); });
  }

  function upsertLocal(c) {
    var summary = {
      email: c.email, company: c.company, audience: c.audience, created_at: c.created_at,
      created_by: c.created_by, first_login_at: c.first_login_at, last_login_at: c.last_login_at, disabled: c.disabled
    };
    var i = state.customers.findIndex(function (x) { return x.email === c.email; });
    if (i > -1) state.customers[i] = summary; else state.customers.unshift(summary);
    renderKpis();
    renderClients();
  }

  function loadEvents() {
    return api('GET', '/api/admin/events?limit=50').then(function (d) {
      state.events = d.events || [];
      state.eventsTotal = d.total || 0;
      $('kpi-logins').textContent = d.total_capped ? d.total + '+' : d.total;
      $('events-count').textContent = state.eventsTotal ? '(' + state.eventsTotal + (d.total_capped ? '+' : '') + ' total)' : '';
      $('events-empty').hidden = state.events.length > 0;
      $('events-body').innerHTML = state.events.map(function (e) {
        var role = e.role === 'staff' ? '<span class="badge badge-blue">Staff</span>' : '<span class="badge badge-grey">Client</span>';
        return '<tr><td>' + role + '</td><td class="cell-strong">' + esc(e.email) + '</td>' +
          '<td><span class="muted">' + esc(e.method) + '</span></td>' +
          '<td class="tabular">' + timeCell(e.at) + ' <span class="muted">&middot; ' + esc(fmtDate(e.at)) + '</span></td></tr>';
      }).join('');
    }).catch(function (e) { if (e.message !== 'signed out') toast(e.message, true); });
  }

  // ---------------------------------------------------------------- new client
  function newError(msg, field) {
    var box = $('new-error');
    box.hidden = !msg;
    box.querySelector('[data-msg]').textContent = msg || '';
    document.querySelectorAll('#form-new .input').forEach(function (i) { i.removeAttribute('aria-invalid'); });
    if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); }
  }

  function openNew() {
    $('form-new').reset();
    $('form-new').hidden = false;
    $('new-done').hidden = true;
    newError('');
    $('new-password').type = 'password';
    openLayer('dlg-new', '#new-company');
  }
  $('btn-new-client').addEventListener('click', openNew);
  document.querySelectorAll('[data-open-new]').forEach(function (b) { b.addEventListener('click', openNew); });

  $('form-new').addEventListener('submit', function (e) {
    e.preventDefault();
    var company = $('new-company').value.trim();
    var email = $('new-email').value.trim().toLowerCase();
    var password = $('new-password').value;
    if (!company) return newError('Enter the company name.', $('new-company'));
    if (!EMAIL_RE.test(email)) return newError('Enter a valid email address.', $('new-email'));
    if (password.length < MIN_PASSWORD) return newError('Password must be at least ' + MIN_PASSWORD + ' characters.', $('new-password'));
    newError('');
    var btn = $('btn-create');
    busy(btn, true, 'Creating...');
    api('POST', '/api/admin/customers', { company: company, email: email, audience: $('new-audience').value, password: password })
      .then(function (d) {
        busy(btn, false);
        upsertLocal(d.customer);
        $('done-url').textContent = window.location.origin + '/customer';
        $('done-email').textContent = d.customer.email;
        $('done-password').textContent = password;
        $('btn-done-manage').dataset.email = d.customer.email;
        $('form-new').hidden = true;
        $('new-done').hidden = false;
        $('btn-copy-creds').focus();
      })
      .catch(function (err) {
        busy(btn, false);
        if (err.message !== 'signed out') newError(err.message, /exists/i.test(err.message) ? $('new-email') : null);
      });
  });

  $('btn-copy-creds').addEventListener('click', function () {
    var text = 'Streamax onboarding portal: ' + $('done-url').textContent +
      '\nEmail: ' + $('done-email').textContent + '\nPassword: ' + $('done-password').textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject())
      .then(function () { toast('Sign-in details copied.'); })
      .catch(function () { toast('Copy failed - select the text and copy it manually.', true); });
  });
  $('btn-done-manage').addEventListener('click', function () {
    var email = this.dataset.email;
    closeLayer('dlg-new');
    openDrawer(email);
  });

  // ---------------------------------------------------------------- drawer
  function contactRow(c) {
    var row = document.createElement('div');
    row.className = 'contact-row';
    row.innerHTML =
      '<label class="visually-hidden">Role</label><input class="input c-role" type="text" placeholder="Role (e.g. Customer Success)">' +
      '<label class="visually-hidden">Contact</label><input class="input c-contact" type="text" placeholder="Name, email or phone">' +
      '<button class="icon-btn" type="button" aria-label="Remove contact"><i class="fa-solid fa-trash-can"></i></button>';
    row.querySelector('.c-role').value = c.role || '';
    row.querySelector('.c-contact').value = c.contact || '';
    row.querySelector('button').addEventListener('click', function () { row.remove(); renderPreview(); });
    row.querySelectorAll('input').forEach(function (i) { i.addEventListener('input', renderPreview); });
    return row;
  }

  function readContacts() {
    return Array.prototype.map.call(document.querySelectorAll('#contacts-rows .contact-row'), function (r) {
      return { role: r.querySelector('.c-role').value.trim(), contact: r.querySelector('.c-contact').value.trim() };
    }).filter(function (c) { return c.role || c.contact; });
  }

  function renderPreview() {
    var list = readContacts();
    $('contacts-preview').innerHTML = list.length
      ? list.map(function (c) { return '<tr><td>' + esc(c.role || '-') + '</td><td>' + esc(c.contact || '-') + '</td></tr>'; }).join('')
      : '<tr><td colspan="2" class="muted">No contacts - the client will see the Streamax defaults.</td></tr>';
  }

  function fillContacts(list) {
    var box = $('contacts-rows');
    box.innerHTML = '';
    list.forEach(function (c) { box.appendChild(contactRow(c)); });
    renderPreview();
  }

  function fillDrawer(c) {
    state.current = c;
    $('drawer-title').textContent = c.company || c.email;
    $('drawer-email').textContent = c.email;
    $('drawer-status').innerHTML = statusBadge(c);
    $('p-company').value = c.company || '';
    $('p-audience').value = c.audience === 'tsp' ? 'tsp' : 'fleet';
    $('f-created').innerHTML = c.created_at ? esc(fmtDate(c.created_at)) + (c.created_by ? ' <span class="muted">by ' + esc(c.created_by.replace(/^staff:/, '')) + '</span>' : '') : '-';
    $('f-first').innerHTML = c.first_login_at ? esc(fmtDate(c.first_login_at)) : '<span class="muted">Not yet</span>';
    $('f-last').innerHTML = c.last_login_at ? esc(fmtDate(c.last_login_at)) : '<span class="muted">Not yet</span>';
    $('p-password').value = '';
    $('p-password').type = 'password';
    $('btn-toggle-access').innerHTML = c.disabled
      ? '<i class="fa-solid fa-lock-open" aria-hidden="true"></i><span>Turn access back on</span>'
      : '<i class="fa-solid fa-lock" aria-hidden="true"></i><span>Turn access off</span>';
    $('contacts-default-badge').hidden = !c.contacts_are_default;
    fillContacts(c.contacts || []);
  }

  function openDrawer(email) {
    $('drawer-title').textContent = 'Loading...';
    $('drawer-email').textContent = email;
    $('drawer-status').innerHTML = '';
    openLayer('drawer', '.drawer-head [data-close]');
    api('GET', '/api/admin/customers/' + encodeURIComponent(email))
      .then(function (d) { fillDrawer(d.customer); $('p-company').focus(); })
      .catch(function (e) { if (e.message !== 'signed out') { toast(e.message, true); closeLayer('drawer'); } });
  }

  $('clients-body').addEventListener('click', function (e) {
    var b = e.target.closest('[data-manage]');
    if (b) openDrawer(b.getAttribute('data-manage'));
  });

  function patchCurrent(body, btn, okMsg) {
    if (!state.current) return;
    busy(btn, true);
    return api('PATCH', '/api/admin/customers/' + encodeURIComponent(state.current.email), body)
      .then(function (d) { busy(btn, false); fillDrawer(d.customer); upsertLocal(d.customer); toast(okMsg); })
      .catch(function (e) { busy(btn, false); if (e.message !== 'signed out') toast(e.message, true); });
  }

  $('form-profile').addEventListener('submit', function (e) {
    e.preventDefault();
    var company = $('p-company').value.trim();
    if (!company) { $('p-company').setAttribute('aria-invalid', 'true'); $('p-company').focus(); toast('Company name cannot be empty.', true); return; }
    $('p-company').removeAttribute('aria-invalid');
    patchCurrent({ company: company, audience: $('p-audience').value }, e.submitter || this.querySelector('button[type=submit]'), 'Profile saved.');
  });

  $('form-password').addEventListener('submit', function (e) {
    e.preventDefault();
    var pw = $('p-password').value;
    if (pw.length < MIN_PASSWORD) {
      $('p-password').setAttribute('aria-invalid', 'true'); $('p-password').focus();
      toast('Password must be at least ' + MIN_PASSWORD + ' characters.', true);
      return;
    }
    $('p-password').removeAttribute('aria-invalid');
    patchCurrent({ password: pw }, e.submitter || this.querySelector('button[type=submit]'), 'Password reset. Share it with the client securely.')
      .then(function () { /* keep the new value visible so it can be copied */ $('p-password').value = pw; $('p-password').type = 'text'; });
  });

  $('btn-toggle-access').addEventListener('click', function () {
    var off = !state.current.disabled;
    patchCurrent({ disabled: off }, this, off ? 'Access turned off. They are signed out on their next page view.' : 'Access turned back on.');
  });

  $('btn-add-contact').addEventListener('click', function () {
    var row = contactRow({ role: '', contact: '' });
    $('contacts-rows').appendChild(row);
    row.querySelector('.c-role').focus();
    renderPreview();
  });
  $('btn-save-contacts').addEventListener('click', function () {
    var list = readContacts();
    patchCurrent({ contacts: list.length ? list : null }, this, list.length ? 'Key contacts saved.' : 'Contacts cleared - defaults will show.');
  });
  $('btn-reset-contacts').addEventListener('click', function () {
    fillContacts(DEFAULT_CONTACTS);
    patchCurrent({ contacts: null }, this, 'Reset to the default Streamax contacts.');
  });

  // ---------------------------------------------------------------- delete
  $('btn-delete').addEventListener('click', function () {
    $('del-email').textContent = state.current.email;
    $('del-confirm').value = '';
    $('btn-confirm-delete').disabled = true;
    openLayer('dlg-delete', '#del-confirm');
  });
  $('del-confirm').addEventListener('input', function () {
    $('btn-confirm-delete').disabled = this.value.trim().toLowerCase() !== state.current.email;
  });
  $('form-delete').addEventListener('submit', function (e) {
    e.preventDefault();
    var email = state.current.email;
    var btn = $('btn-confirm-delete');
    busy(btn, true, 'Deleting...');
    api('DELETE', '/api/admin/customers/' + encodeURIComponent(email))
      .then(function () {
        busy(btn, false);
        closeLayer('dlg-delete');
        closeLayer('drawer');
        state.customers = state.customers.filter(function (c) { return c.email !== email; });
        renderKpis();
        renderClients();
        toast('Deleted ' + email + '.');
      })
      .catch(function (err) { busy(btn, false); if (err.message !== 'signed out') toast(err.message, true); });
  });

  // ---------------------------------------------------------------- misc
  $('client-search').addEventListener('input', function () { state.filter = this.value; renderClients(); });
  $('btn-refresh-events').addEventListener('click', loadEvents);
  $('btn-signout').addEventListener('click', function () {
    fetch('/api/admin/logout', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: '{}' })
      .finally(function () { window.location.href = '/admin/login/'; });
  });

  api('GET', '/api/admin/me').then(function (d) { $('adm-username').textContent = d.username; }).catch(function () {});
  loadClients();
  loadEvents();
  if (window.location.hash === '#activity') selectTab('activity');
})();
