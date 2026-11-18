/* Sarah's Sky — phone navigation: a bottom tab bar (Sky · Tonight · Signs · Readings · More), a "More" sheet,
   and the Android back button closing whatever is open instead of leaving the app. */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var tab = function (name) { var b = document.querySelector('.tabs button[data-tab="' + name + '"]'); if (b) b.click(); };
  var panelOpen = function () { var p = $('panel'); return p && !p.hidden; };
  var readingsOpen = function () { var r = $('readings'); return r && !r.hidden; };
  var signsOpen = function () { var d = $('sarahOverlays'); return d && d.open; };
  var moreOpen = function () { var m = $('moreSheet'); return m && !m.hidden; };

  function closeAll() {
    if (panelOpen()) $('closePanel').click();
    if (readingsOpen()) $('readings').hidden = true;
    if (signsOpen()) $('sarahOverlays').open = false;
    if (moreOpen()) $('moreSheet').hidden = true;
    var info = $('info'); if (info) info.hidden = true;
  }
  function mark(which) {
    document.querySelectorAll('#bottomNav button').forEach(function (b) { b.classList.toggle('on', b.dataset.nav === which); });
  }
  function pushNav() { try { history.pushState({ sky: 1 }, ''); } catch (e) {} }

  var ITEMS = [['sky', '✦', 'Sky'], ['tonight', '☾', 'Tonight'], ['signs', '♓︎', 'Signs'], ['readings', '🔮', 'Readings'], ['more', '☰', 'More']];
  var nav = document.createElement('nav'); nav.id = 'bottomNav'; nav.setAttribute('aria-label', 'Main');
  nav.innerHTML = ITEMS.map(function (i) { return '<button data-nav="' + i[0] + '"><span class="ni" aria-hidden="true">' + i[1] + '</span><span class="nl">' + i[2] + '</span></button>'; }).join('');
  document.body.appendChild(nav);

  var more = document.createElement('div'); more.id = 'moreSheet'; more.hidden = true;
  more.innerHTML = '<div class="ms"><div class="msh"><b>More</b><button id="moreX" aria-label="Close">×</button></div>' +
    [['layers', '🗺️', 'Layers', 'Sky pictures and what is drawn on top'], ['tour', '🧭', 'Guided tour', 'Ten stops around the sky'],
     ['learn', '📖', 'Learn', 'Short lessons'], ['aegis', '⭐', 'AEGIS stars', 'Unusual stars from the AEGIS survey'],
     ['ar', '📷', 'Point & See', 'Hold the phone up to the sky'], ['tarot', '🃏', 'Tarot spreads', 'One card to the Celtic Cross'],
     ['about', 'ℹ️', 'About', 'Credits and privacy']].map(function (i) {
      return '<button data-more="' + i[0] + '"><span class="mi">' + i[1] + '</span><span><b>' + i[2] + '</b><small>' + i[3] + '</small></span></button>'; }).join('') + '</div>';
  document.body.appendChild(more);

  nav.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var w = b.dataset.nav, wasOn = b.classList.contains('on');
    closeAll();
    if (w === 'sky' || wasOn) { mark('sky'); return; }
    pushNav(); mark(w);
    if (w === 'tonight') tab('tonight');
    else if (w === 'signs') { var d = $('sarahOverlays'); d.open = true; }
    else if (w === 'readings') window.SarahReadings && SarahReadings.open('chart');
    else if (w === 'more') more.hidden = false;
  });
  more.addEventListener('click', function (e) {
    if (e.target === more || e.target.id === 'moreX') { more.hidden = true; mark('sky'); return; }
    var b = e.target.closest('button[data-more]'); if (!b) return;
    var w = b.dataset.more; more.hidden = true;
    if (w === 'ar') { location.href = 'ar.html'; return; }
    if (w === 'tarot') { window.SarahReadings && SarahReadings.open('tarot'); mark('readings'); return; }
    tab(w);
  });
  // closing things by their own × also resets the bar
  document.addEventListener('click', function (e) {
    if (e.target.id === 'closePanel' || e.target.id === 'rClose') setTimeout(function () { if (!panelOpen() && !readingsOpen()) mark('sky'); }, 0);
  });

  // Android back / browser back: close the open layer first; only leave the app from the bare sky
  window.addEventListener('popstate', function () {
    if (panelOpen() || readingsOpen() || signsOpen() || moreOpen()) { closeAll(); mark('sky'); }
  });
  // panels opened from elsewhere (top tabs on wide screens) also get a back entry
  var p = $('panel');
  if (p) new MutationObserver(function () { if (!p.hidden && !(history.state && history.state.sky)) pushNav(); }).observe(p, { attributes: true, attributeFilter: ['hidden'] });
  mark('sky');
})();
