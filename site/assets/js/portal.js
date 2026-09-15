/* Streamax Customer Onboarding - customer portal runtime.
 *
 * Every portal section is its own static page (/customer/<section>/), gated
 * server-side by functions/customer/_middleware.js. This script:
 *   - maps legacy switchTab('x') calls in section content to real URLs
 *   - fills the signed-in identity + per-client Key Contacts from /api/customer/me
 *   - runs portal search (Ctrl/Cmd+K), the mobile section menu, the user menu,
 *     sign-out, the language dialog and the fade-up reveals
 *   - opens the accordion a deep link (#anchor) points into
 */
(function () {
  'use strict';

  var ROUTES = {
    'welcome': '/customer/',
    'products': '/customer/products/',
    'installation': '/customer/installation/',
    'platform': '/customer/platform/',
    'ai-features': '/customer/ai-features/',
    'training': '/customer/training/',
    'playbooks': '/customer/playbooks/',
    'support': '/customer/support/'
  };

  window.switchTab = function (tabId) {
    var url = ROUTES[tabId];
    if (url) window.location.href = url;
  };

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* ---- identity + Key Contacts ---- */
  function fillSlots(me) {
    var name = me.company || me.email || 'Customer';
    document.querySelectorAll('[data-slot="identity"]').forEach(function (el) { el.textContent = name; });
    document.querySelectorAll('[data-slot="audience"]').forEach(function (el) { el.textContent = me.audience_label || ''; });
    var rows = (me.contacts || []).filter(function (c) { return c.role || c.contact; }).map(function (c) {
      return '<tr><td><strong>' + escapeHtml(c.role) + '</strong></td><td>' + escapeHtml(c.contact) + '</td></tr>';
    }).join('');
    document.querySelectorAll('[data-slot="contacts"]').forEach(function (el) {
      el.innerHTML = rows || '<tr><td colspan="2">Your Streamax team will be assigned shortly.</td></tr>';
    });
  }

  function loadMe() {
    fetch('/api/customer/me', { credentials: 'same-origin', headers: { 'Accept': 'application/json' } })
      .then(function (r) {
        if (r.status === 401) {
          window.location.href = '/customer/login/?next=' + encodeURIComponent(window.location.pathname);
          return null;
        }
        return r.ok ? r.json() : null;
      })
      .then(function (me) { if (me) fillSlots(me); })
      .catch(function () { /* offline: the page is still readable */ });
  }

  window.signOut = function (evt) {
    if (evt) evt.preventDefault();
    fetch('/api/customer/logout', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' }, body: '{}'
    }).finally(function () { window.location.href = '/customer/login/'; });
    return false;
  };

  /* ---- reveals ---- */
  function observeElements() {
    var els = document.querySelectorAll('.fade-up');
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---- deep links into accordions ---- */
  var ACCORDIONS = ['.aif-feat', '.pfn-feat', '.inst-prod', 'details'];
  function openHashTarget() {
    if (!location.hash || location.hash.length < 2) return;
    var el;
    try { el = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { return; }
    if (!el) return;
    ACCORDIONS.forEach(function (sel) {
      var box = el.closest(sel);
      if (!box) return;
      if (box.tagName === 'DETAILS') box.open = true; else box.classList.add('open');
    });
    el.classList.add('visible');
    var sec = el.closest('.fade-up'); if (sec) sec.classList.add('visible');
    requestAnimationFrame(function () { el.scrollIntoView({ block: 'start' }); });
  }
  window.addEventListener('hashchange', openHashTarget);

  /* ---- user menu ---- */
  window.toggleUserMenu = function (e) {
    e.stopPropagation();
    var nu = document.getElementById('nav-user');
    var open = nu.classList.toggle('open');
    var trig = nu.querySelector('.user-trigger');
    if (trig) trig.setAttribute('aria-expanded', open ? 'true' : 'false');
    closeDrawer();
  };

  /* ---- mobile section menu ---- */
  var drawer = document.getElementById('nav-drawer');
  var menuBtn = document.getElementById('nav-menu-btn');
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
  }
  if (menuBtn && drawer) {
    menuBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = drawer.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var nu = document.getElementById('nav-user'); if (nu) nu.classList.remove('open');
    });
  }

  document.addEventListener('click', function (e) {
    var nu = document.getElementById('nav-user');
    if (nu && !nu.contains(e.target)) nu.classList.remove('open');
    if (drawer && !drawer.contains(e.target) && e.target !== menuBtn) closeDrawer();
  });

  /* ---- search ---- */
  var searchDlg = document.getElementById('search-dialog');
  var searchInput = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var index = null, loading = null, results = [], active = -1, lastFocus = null;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch('/customer/search-index.json', { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (d) { index = d || []; return index; })
        .catch(function () { index = []; return index; });
    }
    return loading;
  }

  function highlight(text, terms) {
    var safe = escapeHtml(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      safe = safe.replace(re, '<mark>$1</mark>');
    });
    return safe;
  }

  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var scored = [];
    index.forEach(function (e) {
      var t = e.t.toLowerCase(), x = (e.x || '').toLowerCase(), s = e.s.toLowerCase();
      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        var term = terms[i];
        if (t.indexOf(term) === 0) score += 6;
        else if (t.indexOf(term) > -1) score += 4;
        else if (s.indexOf(term) > -1) score += 2;
        else if (x.indexOf(term) > -1) score += 1;
        else return; /* every term must match somewhere */
      }
      if (e.s === 'Portal section') score += 2;
      scored.push({ e: e, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score || a.e.t.length - b.e.t.length; });
    return scored.slice(0, 12).map(function (r) { return r.e; });
  }

  function renderResults() {
    var q = searchInput.value.trim();
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!q) {
      results = index.filter(function (e) { return e.s === 'Portal section'; });
    } else {
      results = search(q);
    }
    active = results.length ? 0 : -1;
    if (!results.length) {
      resultsEl.innerHTML = '<li class="search-empty">No matches for <strong>' + escapeHtml(q) +
        '</strong>. Try a product name (e.g. "AD Plus"), a feature ("fatigue") or a task ("install").</li>';
      return;
    }
    resultsEl.innerHTML = results.map(function (e, i) {
      return '<li role="presentation"><a role="option" id="sr-' + i + '" href="' + escapeHtml(e.u) + '"' +
        (i === active ? ' aria-selected="true"' : '') + '>' +
        '<i class="fa-solid ' + escapeHtml(e.i || 'fa-file-lines') + '" aria-hidden="true"></i>' +
        '<span class="sr-title">' + highlight(e.t, terms) + '</span>' +
        '<span class="sr-meta"><b>' + escapeHtml(e.s) + '</b>' + (e.x ? ' &middot; ' + highlight(e.x, terms) : '') + '</span>' +
        '</a></li>';
    }).join('');
    searchInput.setAttribute('aria-activedescendant', active > -1 ? 'sr-' + active : '');
  }

  function moveActive(delta) {
    if (!results.length) return;
    active = (active + delta + results.length) % results.length;
    resultsEl.querySelectorAll('a[role="option"]').forEach(function (a, i) {
      if (i === active) { a.setAttribute('aria-selected', 'true'); a.scrollIntoView({ block: 'nearest' }); }
      else a.removeAttribute('aria-selected');
    });
    searchInput.setAttribute('aria-activedescendant', 'sr-' + active);
  }

  function openSearch() {
    if (!searchDlg) return;
    lastFocus = document.activeElement;
    searchDlg.hidden = false;
    document.body.style.overflow = 'hidden';
    closeDrawer();
    searchInput.value = '';
    resultsEl.innerHTML = '<li class="search-empty">Loading...</li>';
    setTimeout(function () { searchInput.focus(); }, 20);
    loadIndex().then(renderResults);
  }
  function closeSearch() {
    if (!searchDlg || searchDlg.hidden) return;
    searchDlg.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && document.body.contains(lastFocus)) lastFocus.focus();
  }

  if (searchDlg) {
    document.querySelectorAll('[data-open-search]').forEach(function (b) { b.addEventListener('click', openSearch); });
    searchDlg.addEventListener('mousedown', function (e) { if (e.target === searchDlg) closeSearch(); });
    searchInput.addEventListener('input', function () { if (index) renderResults(); });
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); moveActive(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); moveActive(-1); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        if (results[active]) { closeSearch(); window.location.href = results[active].u; }
      }
    });
    resultsEl.addEventListener('click', function (e) {
      var a = e.target.closest('a[role="option"]');
      if (!a) return;
      var sameBase = a.getAttribute('href').split('#')[0] === location.pathname;
      closeSearch();
      if (sameBase) setTimeout(openHashTarget, 0);
    });
  }

  document.addEventListener('keydown', function (e) {
    var typing = /INPUT|TEXTAREA|SELECT/.test((e.target && e.target.tagName) || '') || (e.target && e.target.isContentEditable);
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); openSearch(); return; }
    if (e.key === '/' && !typing) { e.preventDefault(); openSearch(); return; }
    if (e.key === 'Escape') {
      closeSearch();
      window.closeLangModal();
      closeDrawer();
      var nu = document.getElementById('nav-user'); if (nu) nu.classList.remove('open');
    }
  });

  // Show the platform-appropriate shortcut hint.
  if (/Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent)) {
    document.querySelectorAll('.nav-search kbd').forEach(function (k) { k.textContent = '⌘K'; });
  }

  /* ---- language dialog (Google Translate) ---- */
  var LANG_LABELS = { en: 'English', es: 'Español', pt: 'Português', fr: 'Français' };

  window.openLangModal = function () {
    var nu = document.getElementById('nav-user'); if (nu) nu.classList.remove('open');
    var ov = document.getElementById('lang-overlay'); if (ov) ov.classList.add('open');
    var sel = document.querySelector('.lang-card.selected'); if (sel) setTimeout(function () { sel.focus(); }, 30);
  };
  window.closeLangModal = function () {
    var ov = document.getElementById('lang-overlay'); if (ov) ov.classList.remove('open');
  };

  function applyTranslation(lang) {
    var tries = 0;
    var iv = setInterval(function () {
      var combo = document.querySelector('.goog-te-combo');
      tries++;
      if (combo) {
        combo.value = lang;
        combo.dispatchEvent(new Event('change'));
        clearInterval(iv);
      } else if (tries > 50) {
        clearInterval(iv);
      }
    }, 150);
  }

  window.selectLanguage = function (lang, cardEl) {
    document.querySelectorAll('.lang-card').forEach(function (c) { c.classList.remove('selected'); });
    if (cardEl) cardEl.classList.add('selected');
    var cur = document.getElementById('ud-current-lang');
    if (cur) cur.textContent = LANG_LABELS[lang] || 'English';
    try { localStorage.setItem('portal_lang', lang); } catch (e) {}
    applyTranslation(lang);
    setTimeout(window.closeLangModal, 280);
  };

  window.googleTranslateElementInit = function () {
    new google.translate.TranslateElement(
      { pageLanguage: 'en', includedLanguages: 'en,es,pt,fr', autoDisplay: false },
      'google_translate_element'
    );
    try {
      var saved = localStorage.getItem('portal_lang');
      if (saved && saved !== 'en' && LANG_LABELS[saved]) {
        var card = document.querySelector('.lang-card[data-lang="' + saved + '"]');
        if (card) {
          document.querySelectorAll('.lang-card').forEach(function (c) { c.classList.remove('selected'); });
          card.classList.add('selected');
        }
        var cur = document.getElementById('ud-current-lang');
        if (cur) cur.textContent = LANG_LABELS[saved];
        applyTranslation(saved);
      }
    } catch (e) {}
  };

  function boot() {
    observeElements();
    loadMe();
    openHashTarget();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
