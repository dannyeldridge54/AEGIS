/* Night vision (red light) — keeps your eyes dark-adapted at the telescope.
   A red multiply layer over the whole page turns every colour (sky pictures, labels, buttons) into shades of red;
   a dim layer on top lowers brightness further. Works on index.html and ar.html; remembered on this device. */
(function () {
  var KEY = 'aegis-skymap:';
  function get(k, d) { try { var v = localStorage.getItem(KEY + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch (e) {} }

  var css = document.createElement('style');
  css.textContent =
    '#nvRed,#nvDim{position:fixed;inset:0;pointer-events:none;z-index:2147483600;display:none}' +
    '#nvRed{background:#ff0000;mix-blend-mode:multiply}' +
    '#nvDim{background:#000;z-index:2147483601}' +
    'html.night #nvRed,html.night #nvDim{display:block}' +
    'html.night{color-scheme:dark}' +
    '#nvCtl{position:fixed;left:12px;bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:2147483602;display:none;' +
      'align-items:center;gap:8px;padding:6px 10px;border-radius:999px;background:rgba(40,0,0,.85);border:1px solid #600;' +
      'color:#f44;font:13px system-ui,sans-serif;opacity:.35;transition:opacity .3s}' +
    '#nvCtl:hover,#nvCtl:focus-within,#nvCtl.awake{opacity:1}' +
    'html.night #nvCtl{display:flex}' +
    '#nvCtl input{width:110px;accent-color:#c00}' +
    '#nvCtl button{background:none;border:0;color:#f44;font:inherit;cursor:pointer;padding:2px 4px}' +
    '#nightBtn[aria-pressed=true]{background:#400;color:#f55;border-color:#800}';
  document.head.appendChild(css);

  var red = document.createElement('div'); red.id = 'nvRed';
  var dim = document.createElement('div'); dim.id = 'nvDim';
  var ctl = document.createElement('div'); ctl.id = 'nvCtl'; ctl.setAttribute('role', 'group'); ctl.setAttribute('aria-label', 'Night vision');
  ctl.innerHTML = '<span aria-hidden="true">🔴</span><label><span class="sr" style="position:absolute;left:-9999px">Brightness</span>' +
    '<input id="nvLevel" type="range" min="15" max="100" step="5"></label><button id="nvOff" title="Turn night vision off">Off</button>';

  var level = Math.max(15, Math.min(100, get('nightLevel', 70)));
  var meta = document.querySelector('meta[name=theme-color]');
  var metaWas = meta ? meta.getAttribute('content') : null;
  var wakeT;

  function apply(on) {
    document.documentElement.classList.toggle('night', on);
    dim.style.opacity = String((100 - level) / 100);
    var b = document.getElementById('nightBtn'); if (b) b.setAttribute('aria-pressed', String(on));
    if (meta) meta.setAttribute('content', on ? '#000000' : metaWas);
  }
  function wake() { ctl.classList.add('awake'); clearTimeout(wakeT); wakeT = setTimeout(function () { ctl.classList.remove('awake'); }, 3500); }
  function toggle(force) {
    var on = typeof force === 'boolean' ? force : !document.documentElement.classList.contains('night');
    set('night', on); apply(on); if (on) wake();
    return on;
  }

  function mount() {
    document.body.appendChild(red); document.body.appendChild(dim); document.body.appendChild(ctl);
    var r = document.getElementById('nvLevel'); r.value = level;
    r.addEventListener('input', function () { level = +r.value; set('nightLevel', level); dim.style.opacity = String((100 - level) / 100); wake(); });
    document.getElementById('nvOff').addEventListener('click', function () { toggle(false); });
    // header button on the main page (next to A+); Point & See gets the floating control only
    var big = document.getElementById('bigText');
    if (big && !document.getElementById('nightBtn')) {
      var b = document.createElement('button'); b.id = 'nightBtn'; b.className = 'toggle'; b.setAttribute('aria-pressed', 'false');
      b.title = 'Night vision: red light keeps your eyes dark-adapted (N)'; b.textContent = '🔴';
      b.addEventListener('click', function () { toggle(); });
      big.parentNode.insertBefore(b, big);
    }
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'n' || e.key === 'N') && !/INPUT|TEXTAREA|SELECT/.test((e.target.tagName || '')) && !e.ctrlKey && !e.metaKey && !e.altKey) toggle();
    });
    apply(get('night', false));
  }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
  window.SarahNight = { toggle: toggle, isOn: function () { return document.documentElement.classList.contains('night'); } };
})();
