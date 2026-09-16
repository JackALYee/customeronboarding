/* Streamax eSIM — one small script for every page. No framework, no CDN.
   Everything below is progressive: the pages are complete and readable with
   JavaScript switched off. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------------------------------------------------------- mobile nav -- */
  var hdr = $('#hdr'), burger = $('#burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = hdr.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (hdr.classList.contains('open') && !hdr.contains(e.target)) {
        hdr.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && hdr.classList.contains('open')) {
        hdr.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

  /* ---------------------------------------------------- coverage explorer -- */
  var covList = $('#cov-list');
  if (covList) {
    var rows = $$('.covrow', covList),
        q = $('#cov-q'), reg = $('#cov-r'),
        count = $('#cov-count'), empty = $('#cov-empty'),
        tip = $('#maptip'), mapbox = $('#mapbox'),
        shapes = $$('.cty.on, .pin', mapbox),
        byName = {};

    rows.forEach(function (r) { byName[r.dataset.n] = r; });

    function filter() {
      var t = (q.value || '').trim().toLowerCase(), r0 = reg.value, n = 0;
      rows.forEach(function (row) {
        var ok = (!t || row.dataset.s.indexOf(t) > -1) && (!r0 || row.dataset.r === r0);
        row.hidden = !ok;
        if (ok) n++;
      });
      empty.hidden = n > 0;
      count.textContent = n + (n === 1 ? ' country' : ' countries') + ' of ' + rows.length;
      // dim the map to match the filter
      shapes.forEach(function (s) {
        var row = byName[s.dataset.n];
        s.style.opacity = (row && !row.hidden) ? '' : '.28';
      });
    }
    q.addEventListener('input', filter);
    reg.addEventListener('change', filter);
    filter();

    /* --- selection, shared by the map and the list --- */
    var selected = null;
    function select(name, scroll) {
      if (selected === name) { name = null; }
      selected = name;
      shapes.forEach(function (s) { s.classList.toggle('sel', s.dataset.n === name); });
      rows.forEach(function (r) { r.classList.toggle('sel', r.dataset.n === name); });
      if (name && scroll) {
        var row = byName[name];
        if (row && !row.hidden) row.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }
    }

    /* --- map tooltip --- */
    function showTip(el, ev) {
      var row = byName[el.dataset.n];
      if (!row) {
        tip.innerHTML = '<b>' + el.dataset.n + '</b><span class="pill grey">Not provisioned</span>';
      } else {
        var ops = $('.ops', row).textContent.split(' · ');
        tip.innerHTML = '<b>' + el.dataset.n + '</b><ul>' +
          ops.map(function (o) { return '<li>' + o + '</li>'; }).join('') + '</ul>';
      }
      var box = mapbox.getBoundingClientRect(),
          x = ev.clientX - box.left, y = ev.clientY - box.top;
      tip.classList.add('show');
      var w = tip.offsetWidth, h = tip.offsetHeight;
      tip.style.left = Math.max(8, Math.min(x + 16, box.width - w - 8)) + 'px';
      tip.style.top = Math.max(8, y - h - 12) + 'px';
    }
    shapes.forEach(function (s) {
      s.addEventListener('mousemove', function (e) { showTip(s, e); });
      s.addEventListener('mouseleave', function () { tip.classList.remove('show'); });
      s.addEventListener('click', function () { select(s.dataset.n, true); });
    });
    mapbox.addEventListener('mouseleave', function () { tip.classList.remove('show'); });

    rows.forEach(function (r) {
      r.addEventListener('click', function () { select(r.dataset.n, false); });
      r.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(r.dataset.n, false); }
      });
    });
  }

  /* ------------------------------------------- FT Cloud simulator iframe -- */
  /* The component has no fixed height: the SIM list is far shorter than the
     overview. Same origin, so the parent can just measure it and follow. */
  var frame = $('.simwrap iframe');
  if (frame) {
    var fit = function () {
      try {
        var d = frame.contentDocument;
        if (!d || !d.body) return;
        // body's own box, not scrollHeight: scrollHeight can never report less than
        // the iframe's current height, so the frame could grow but never shrink.
        var h = d.body.getBoundingClientRect().height;
        if (h > 200) frame.style.height = Math.ceil(h + 2) + 'px';
      } catch (e) { /* cross-origin or not ready — keep the CSS height */ }
    };
    frame.addEventListener('load', function () {
      fit();
      try {
        var d = frame.contentDocument;
        d.addEventListener('click', function () { setTimeout(fit, 40); });
        if (window.ResizeObserver) new ResizeObserver(fit).observe(d.documentElement);
      } catch (e) { /* nothing to observe */ }
    });
    window.addEventListener('resize', fit);
  }

  /* ------------------------------------------------------- pricing search -- */
  var prTable = $('#pr-table');
  if (prTable) {
    var prRows = $$('tbody tr', prTable), prQ = $('#pr-q'), prC = $('#pr-count');
    function prFilter() {
      var t = (prQ.value || '').trim().toLowerCase(), n = 0;
      prRows.forEach(function (r) {
        var ok = !t || r.dataset.s.indexOf(t) > -1;
        r.hidden = !ok;
        if (ok) n++;
      });
      prC.textContent = n + ' of ' + prRows.length + ' destinations';
    }
    prQ.addEventListener('input', prFilter);
    prFilter();
  }

  /* ------------------------------------------------------- pool calculator -- */
  var calc = $('#calc');
  if (calc && window.ESIM_PRICES) {
    var ALW = [1, 2, 3, 5, 10];
    var mode = 'dynamic';
    var sel = $('#c-country'), dev = $('#c-dev'), alw = $('#c-alw'),
        blk = $('#c-blk'), use = $('#c-use');

    ESIM_PRICES.forEach(function (p, i) {
      var o = document.createElement('option');
      o.value = String(i);
      o.textContent = p.c;
      sel.appendChild(o);
    });
    var def = ESIM_PRICES.findIndex(function (p) { return p.c === 'EU'; });
    sel.value = String(def > -1 ? def : 0);

    function fmtGB(v) {
      // fleets budget in GB; switching units mid-slider just makes the number harder to read
      var n = v >= 100 ? Math.round(v) : Math.round(v * 10) / 10;
      return n.toLocaleString('en-US') + ' GB';
    }
    function fmt$(v) {
      return '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function render() {
      var p = ESIM_PRICES[+sel.value] || ESIM_PRICES[0],
          x = +dev.value,
          a = ALW[+alw.value],
          d = +blk.value,
          pool = mode === 'dynamic' ? a * x : d,
          used = Math.round(pool * (+use.value) / 100),
          within = Math.min(used, pool),
          over = Math.max(0, used - pool),
          bundleKey = { 1: 'b1', 2: 'b2', 3: 'b3', 5: 'b5', 10: 'b10' }[a],
          base = mode === 'dynamic'
            ? (p[bundleKey] != null ? p[bundleKey] * x : p.g * a * x)
            : d * p.g,
          overCost = over * p.o,
          total = base + overCost;

      $('#c-dev-v').textContent = x.toLocaleString('en-US');
      $('#c-alw-v').textContent = a + ' GB';
      $('#c-blk-v').textContent = fmtGB(d);
      $('#c-use-v').textContent = fmtGB(used);

      var scale = Math.max(pool, used) || 1;
      $('#g-fill').style.width = (within / scale * 100) + '%';
      $('#g-over').style.width = (over / scale * 100) + '%';

      $('#k-pool').textContent = fmtGB(pool);
      $('#k-used').textContent = fmtGB(used);
      $('#k-left').textContent = over > 0 ? '0 GB' : fmtGB(pool - used);
      $('#k-base').textContent = fmt$(base);
      $('#k-over').textContent = fmt$(overCost);
      $('#k-over').className = over > 0 ? 'over' : '';
      $('#k-total').textContent = fmt$(total);
      $('#k-per').innerHTML = 'That is <strong>' + fmt$(total / x) +
        '</strong> per device per month across ' + x.toLocaleString('en-US') +
        ' device' + (x === 1 ? '' : 's') + ' in ' + p.c +
        (over > 0 ? ' — including ' + fmtGB(over) + ' of overage at ' + fmt$(p.o) + '/GB.' : '.');
    }

    $$('.seg button', calc).forEach(function (b) {
      b.addEventListener('click', function () {
        mode = b.dataset.mode;
        $$('.seg button', calc).forEach(function (o) {
          o.setAttribute('aria-selected', o === b ? 'true' : 'false');
        });
        $('#f-alw').hidden = mode !== 'dynamic';
        $('#f-blk').hidden = mode !== 'static';
        render();
      });
    });
    [sel, dev, alw, blk, use].forEach(function (el) {
      el.addEventListener('input', render);
      el.addEventListener('change', render);
    });
    render();
  }
})();
