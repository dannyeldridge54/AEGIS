/* Sarah's Sky — more traditions and tools (Danny 2026-11-19: "continue Sarah's app research").
   Tradition panels are labelled "tradition — not astronomy"; the sky facts they start from are computed with astronomy-engine.
   Sources (checked 19 Nov 2026):
   - Arabic manazil: 28 equal tropical mansions of 12°51'26" from 0° Aries (Agrippa's table, renaissanceastrology.com/mansionsmoon.html).
     English glosses are the common translations of the Arabic names.
   - Chinese xiu: names, Four Symbols and determinative stars from en.wikipedia.org/wiki/Twenty-Eight_Mansions; star positions
     (J2000 RA) from the app's Hipparcos list (d3-celestial, V < 4.5) and d3-celestial stars.6.json for γ² Sgr, η And, 35 Ari, θ Cnc.
     A lodge runs from its determinative star's right ascension to the next one's (the classical equatorial convention).
   - I Ching: King Wen numbering from the standard trigram table; three-coin method; keywords written fresh.
   - Elder Futhark: the 24 runes in their three aettir; keywords written fresh.
   Nothing leaves the device. */
(function () {
  var A = window.Astronomy; if (!A) return;
  var $ = function (id) { return document.getElementById(id); };
  var norm = function (x) { x %= 360; return x < 0 ? x + 360 : x; };
  var rnd = function (n) { var a = new Uint32Array(1); (window.crypto || window.msCrypto).getRandomValues(a); return a[0] % n; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmtD = function (d) { return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }); };
  var fmtT = function (d) { return d.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' }); };
  var R = {};

  function location() {
    var l = null;
    try { l = JSON.parse(localStorage.getItem('aegis-skymap:location') || 'null'); } catch (e) {}
    if (!l) try { l = JSON.parse(localStorage.getItem('sky.loc') || 'null'); } catch (e) {}
    return l && isFinite(l.lat) && isFinite(l.lon) ? { lat: +l.lat, lon: +l.lon, set: true } : { lat: 35.47, lon: -97.52, set: false };   // Oklahoma City fallback
  }

  // ---- Arabic lunar mansions (manazil al-qamar) ----
  var MANAZIL = [['al-Sharatain', 'the two signs'], ['al-Butayn', 'the little belly'], ['al-Thurayya', 'the Pleiades'], ['al-Dabaran', 'the follower'],
    ['al-Haq\'a', 'the white spot'], ['al-Han\'a', 'the brand'], ['al-Dhira\'', 'the forearm'], ['al-Nathra', 'the gap'], ['al-Tarf', 'the glance'],
    ['al-Jabha', 'the forehead'], ['al-Zubra', 'the mane'], ['al-Sarfa', 'the changer'], ['al-\'Awwa', 'the barker'], ['al-Simak', 'the unarmed one'],
    ['al-Ghafr', 'the covering'], ['al-Zubana', 'the claws'], ['al-Iklil', 'the crown'], ['al-Qalb', 'the heart'], ['al-Shawla', 'the sting'],
    ['al-Na\'a\'im', 'the ostriches'], ['al-Balda', 'the empty place'], ['Sa\'d al-Dhabih', 'luck of the slaughterer'], ['Sa\'d Bula\'', 'luck of the swallower'],
    ['Sa\'d al-Su\'ud', 'luck of lucks'], ['Sa\'d al-Akhbiya', 'luck of the tents'], ['al-Fargh al-Muqaddam', 'the front spout'],
    ['al-Fargh al-Mu\'akhkhar', 'the rear spout'], ['Batn al-Hut', 'belly of the fish']];
  R.manazil = function (d) {
    var lon = norm(A.EclipticGeoMoon(d).lon), w = 360 / 28, i = Math.floor(lon / w), into = lon - i * w;
    var m = MANAZIL[i], nextIn = (w - into) / 13.18;   // the Moon moves about 13.2° a day
    return 'Moon in mansion <b>' + (i + 1) + ' · ' + m[0] + '</b> (' + m[1] + ')<br>' + into.toFixed(1) + '° into it · next mansion in about ' +
      (nextIn < 1 ? Math.round(nextIn * 24) + ' h' : nextIn.toFixed(1) + ' days') + '<br><span class="small">Equal tropical mansions from 0° Aries (medieval Arabic and European convention).</span>';
  };

  // ---- Chinese lunar lodges (xiu) ----
  var XIU = [['Jiǎo', 'Horn', 'Azure Dragon', 201.298], ['Kàng', 'Neck', 'Azure Dragon', 213.224], ['Dī', 'Root', 'Azure Dragon', 222.720],
    ['Fáng', 'Room', 'Azure Dragon', 239.713], ['Xīn', 'Heart', 'Azure Dragon', 247.352], ['Wěi', 'Tail', 'Azure Dragon', 252.968],
    ['Jī', 'Winnowing Basket', 'Azure Dragon', 271.452], ['Dǒu', 'Dipper', 'Black Tortoise', 281.414], ['Niú', 'Ox', 'Black Tortoise', 305.253],
    ['Nǚ', 'Girl', 'Black Tortoise', 311.919], ['Xū', 'Emptiness', 'Black Tortoise', 322.890], ['Wēi', 'Rooftop', 'Black Tortoise', 331.446],
    ['Shì', 'Encampment', 'Black Tortoise', 346.190], ['Bì', 'Wall', 'Black Tortoise', 3.309], ['Kuí', 'Legs', 'White Tiger', 14.302],
    ['Lóu', 'Bond', 'White Tiger', 28.660], ['Wèi', 'Stomach', 'White Tiger', 40.863], ['Mǎo', 'Hairy Head', 'White Tiger', 56.219],
    ['Bì', 'Net', 'White Tiger', 67.154], ['Zī', 'Turtle Beak', 'White Tiger', 83.784], ['Shēn', 'Three Stars', 'White Tiger', 85.190],
    ['Jǐng', 'Well', 'Vermilion Bird', 95.740], ['Guǐ', 'Ghost', 'Vermilion Bird', 127.899], ['Liǔ', 'Willow', 'Vermilion Bird', 129.414],
    ['Xīng', 'Star', 'Vermilion Bird', 141.897], ['Zhāng', 'Extended Net', 'Vermilion Bird', 147.870], ['Yì', 'Wings', 'Vermilion Bird', 164.944],
    ['Zhěn', 'Chariot', 'Vermilion Bird', 183.952]];
  R.xiuOf = function (raDeg) {   // index of the lodge holding this J2000 right ascension
    for (var i = 0; i < 28; i++) { var a = XIU[i][3], b = XIU[(i + 1) % 28][3], w = norm(b - a); if (norm(raDeg - a) < w) return i; }
    return 0;
  };
  R.xiu = function (d) {
    var l = location(), ob = new A.Observer(l.lat, l.lon, 0), eq = A.Equator(A.Body.Moon, d, ob, false, true), ra = norm(eq.ra * 15);
    var i = R.xiuOf(ra), x = XIU[i];
    return 'Moon in lodge <b>' + (i + 1) + ' · ' + x[0] + '</b> (' + x[1] + ') of the <b>' + x[2] + '</b><br>' +
      '<span class="small">Lodges run in right ascension from each determinative star to the next (classical convention); widths range from about 1° to 33°.</span>';
  };

  // ---- Planetary hours (Chaldean order, unequal hours from local sunrise and sunset) ----
  var CHALD = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'], SYM = { Saturn: '♄', Jupiter: '♃', Mars: '♂', Sun: '☉', Venus: '♀', Mercury: '☿', Moon: '☽' };
  var DAYRULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];   // Sunday … Saturday
  R.hours = function (d) {
    var l = location(), ob = new A.Observer(l.lat, l.lon, 0);
    var rise = function (t, dir) { var r = A.SearchRiseSet(A.Body.Sun, ob, dir, t, 2); return r ? r.date : null; };
    var start = new Date(d.getTime() - 36 * 3600e3), sr = null, ss = null, nsr = null, t = start;
    for (var k = 0; k < 4; k++) {   // find the sunrise at or before d, then the sunset and next sunrise after it
      var r1 = rise(t, +1); if (!r1) break;
      if (r1 <= d) { sr = r1; t = new Date(r1.getTime() + 60e3); } else break;
    }
    if (!sr) return 'The Sun does not rise or set here today (polar day or night), so planetary hours are not defined.';
    ss = rise(sr, -1); nsr = rise(ss || sr, +1);
    if (!ss || !nsr) return 'Sunrise or sunset not found for this location today.';
    var day = d < ss, a = day ? sr : ss, b = day ? ss : nsr, len = (b - a) / 12, idx = Math.floor((d - a) / len);
    var ruler = DAYRULER[sr.getDay()], first = CHALD.indexOf(ruler), hourN = (day ? 0 : 12) + idx, planet = CHALD[(first + hourN) % 7];
    var endT = new Date(a.getTime() + (idx + 1) * len), nextP = CHALD[(first + hourN + 1) % 7];
    return 'Day of <b>' + SYM[ruler] + ' ' + ruler + '</b> · ' + (day ? 'day' : 'night') + ' hour ' + (idx + 1) + ' of 12: <b>' + SYM[planet] + ' ' + planet + '</b><br>' +
      'until ' + fmtT(endT) + ' (then ' + SYM[nextP] + ' ' + nextP + ') · each ' + (day ? 'day' : 'night') + ' hour is ' + Math.round(len / 60e3) + ' min<br>' +
      '<span class="small">Sunrise ' + fmtT(sr) + ', sunset ' + fmtT(ss) + ' (computed' + (l.set ? '' : ' for Oklahoma City — set your location in the sky map') + ').</span>';
  };

  // ---- Sky events: retrograde planets now, next stations, next eclipses (all astronomy, computed) ----
  var PLAN = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'];
  var geoLon = function (name, t) { return A.Ecliptic(A.GeoVector(A.Body[name], t, true)).elon; };
  var rate = function (name, t) { var a = geoLon(name, new Date(t.getTime() - 6 * 3600e3)), b = geoLon(name, new Date(t.getTime() + 6 * 3600e3)); var x = b - a; if (x > 180) x -= 360; if (x < -180) x += 360; return x * 2; };
  R.nextStation = function (name, d, days) {   // first change of apparent direction within `days`
    var s0 = rate(name, d) < 0, prev = d;
    for (var i = 1; i <= days; i++) { var t = new Date(d.getTime() + i * 864e5); if ((rate(name, t) < 0) !== s0) {
      var lo = prev.getTime(), hi = t.getTime(); for (var k = 0; k < 20; k++) { var m = (lo + hi) / 2; if ((rate(name, new Date(m)) < 0) === s0) lo = m; else hi = m; }
      return { date: new Date(hi), toRetro: !s0 }; } prev = t; }
    return null;
  };
  R.events = function (d) {
    var now = PLAN.map(function (p) { return { p: p, retro: rate(p, d) < 0 }; });
    var retro = now.filter(function (x) { return x.retro; }).map(function (x) { return x.p; });
    var out = '<b>Retrograde now:</b> ' + (retro.length ? retro.join(', ') : 'none of Mercury–Saturn') + '<br>';
    var st = PLAN.map(function (p) { var s = R.nextStation(p, d, 420); return s ? { p: p, s: s } : null; }).filter(Boolean).sort(function (a, b) { return a.s.date - b.s.date; });
    out += '<b>Next turning points</b> (apparent, seen from Earth):<br>' + st.map(function (x) { return x.p + ' turns ' + (x.s.toRetro ? 'retrograde' : 'direct') + ' · ' + fmtD(x.s.date); }).join('<br>') + '<br>';
    try {
      var le = A.SearchLunarEclipse(d), se = A.SearchGlobalSolarEclipse(d);
      out += '<b>Next lunar eclipse:</b> ' + fmtD(le.peak.date) + ' (' + le.kind + ')<br><b>Next solar eclipse:</b> ' + fmtD(se.peak.date) + ' (' + se.kind + ', somewhere on Earth)';
    } catch (e) {}
    return out + '<br><span class="small">These are real sky events, computed on the phone. Their meanings in astrology are a tradition.</span>';
  };

  // ---- I Ching (three-coin method) ----
  var TRI = ['☰', '☳', '☵', '☶', '☷', '☴', '☲', '☱'];   // Qian, Zhen, Kan, Gen, Kun, Xun, Li, Dui (bottom→top lines as bits)
  var TRIBITS = [7, 1, 2, 4, 0, 6, 5, 3];          // line1 = bit0 (bottom)
  var KW = [[1, 34, 5, 26, 11, 9, 14, 43], [25, 51, 3, 27, 24, 42, 21, 17], [6, 40, 29, 4, 7, 59, 64, 47], [33, 62, 39, 52, 15, 53, 56, 31],
    [12, 16, 8, 23, 2, 20, 35, 45], [44, 32, 48, 18, 46, 57, 50, 28], [13, 55, 63, 22, 36, 37, 30, 49], [10, 54, 60, 41, 19, 61, 38, 58]];   // [lower][upper]
  var HEX = ['The Creative · initiative', 'The Receptive · yielding', 'Difficulty at the Beginning · sprouting', 'Youthful Folly · learning', 'Waiting · patience',
    'Conflict · settle it early', 'The Army · discipline', 'Holding Together · alliance', 'Small Taming · gentle restraint', 'Treading · careful conduct',
    'Peace · harmony', 'Standstill · stagnation', 'Fellowship · community', 'Great Possession · abundance', 'Modesty · humility', 'Enthusiasm · readiness',
    'Following · adapting', 'Work on the Spoiled · repair', 'Approach · drawing near', 'Contemplation · overview', 'Biting Through · decision',
    'Grace · beauty and form', 'Splitting Apart · letting go', 'Return · a turning point', 'Innocence · the unexpected', 'Great Taming · stored strength',
    'Nourishment · what you feed', 'Great Exceeding · overload', 'The Abysmal · danger, depth', 'The Clinging · clarity, fire', 'Influence · attraction',
    'Duration · constancy', 'Retreat · stepping back', 'Great Power · strength used well', 'Progress · rising', 'Darkening of the Light · hidden light',
    'The Family · roles', 'Opposition · difference', 'Obstruction · the blocked path', 'Deliverance · release', 'Decrease · simplify', 'Increase · gain',
    'Breakthrough · resolution', 'Coming to Meet · encounter', 'Gathering Together · assembly', 'Pushing Upward · growth', 'Oppression · exhaustion',
    'The Well · the source', 'Revolution · change of form', 'The Cauldron · transformation', 'The Arousing · shock', 'Keeping Still · stillness',
    'Development · gradual progress', 'The Marrying Maiden · subordinate role', 'Abundance · fullness', 'The Wanderer · the traveller', 'The Gentle · penetrating wind',
    'The Joyous · lake, delight', 'Dispersion · dissolving', 'Limitation · measure', 'Inner Truth · sincerity', 'Small Exceeding · small things',
    'After Completion · order achieved', 'Before Completion · almost there'];
  var triOf = function (bits) { return TRIBITS.indexOf(bits); };
  R.hexOf = function (lines) {   // lines[0] = bottom; 1 = yang
    var lo = lines[0] | lines[1] << 1 | lines[2] << 2, up = lines[3] | lines[4] << 1 | lines[5] << 2;
    var l = triOf(lo), u = triOf(up); return { n: KW[l][u], lower: l, upper: u };
  };
  R.iching = function () {
    var vals = [], i; for (i = 0; i < 6; i++) vals.push(2 + rnd(2) + (2 + rnd(2)) + (2 + rnd(2)));   // heads 3, tails 2
    var prim = vals.map(function (v) { return v % 2; }), moving = vals.map(function (v) { return v === 6 || v === 9; });
    var rel = prim.map(function (b, k) { return moving[k] ? 1 - b : b; });
    var a = R.hexOf(prim), b = R.hexOf(rel), mv = moving.map(function (m, k) { return m ? k + 1 : 0; }).filter(Boolean);
    var draw = function (ls, mov) { var s = ''; for (var k = 5; k >= 0; k--) s += '<div style="font:16px monospace;letter-spacing:2px">' + (ls[k] ? '▬▬▬▬▬' : '▬▬ ▬▬') + (mov && mov[k] ? ' ◦' : '') + '</div>'; return s; };
    var h = '<div style="display:flex;gap:18px;align-items:flex-start"><div>' + draw(prim, moving) + '</div><div><b>' + a.n + '. ' + HEX[a.n - 1] + '</b><br>' + TRI[a.upper] + ' over ' + TRI[a.lower];
    h += mv.length ? '<br>moving lines: ' + mv.join(', ') + '<br>→ <b>' + b.n + '. ' + HEX[b.n - 1] + '</b>' : '<br>no moving lines'; h += '</div></div>';
    return h + '<button type="button" id="ichingCast" style="margin-top:6px">Cast again</button>';
  };

  // ---- Elder Futhark runes ----
  var RUNES = [['ᚠ', 'Fehu', 'wealth, what you have earned'], ['ᚢ', 'Uruz', 'raw strength'], ['ᚦ', 'Thurisaz', 'a thorn; force to be handled'], ['ᚨ', 'Ansuz', 'voice, message'],
    ['ᚱ', 'Raidho', 'journey, rhythm'], ['ᚲ', 'Kenaz', 'torch; skill and insight'], ['ᚷ', 'Gebo', 'gift, exchange'], ['ᚹ', 'Wunjo', 'joy, belonging'],
    ['ᚺ', 'Hagalaz', 'hail; disruption'], ['ᚾ', 'Naudhiz', 'need, constraint'], ['ᛁ', 'Isa', 'ice; stillness'], ['ᛃ', 'Jera', 'harvest, a cycle completing'],
    ['ᛇ', 'Eihwaz', 'yew; endurance'], ['ᛈ', 'Perthro', 'the unknown, chance'], ['ᛉ', 'Algiz', 'protection'], ['ᛊ', 'Sowilo', 'the Sun; success'],
    ['ᛏ', 'Tiwaz', 'justice, commitment'], ['ᛒ', 'Berkano', 'birch; growth, care'], ['ᛖ', 'Ehwaz', 'horse; partnership, movement'], ['ᛗ', 'Mannaz', 'humankind; the self among others'],
    ['ᛚ', 'Laguz', 'water; intuition'], ['ᛜ', 'Ingwaz', 'seed; gestation'], ['ᛞ', 'Dagaz', 'day; breakthrough'], ['ᛟ', 'Othala', 'home, inheritance']];
  R.runes = function (n) {
    var pool = RUNES.slice(), pick = [], labels = n === 3 ? ['Situation', 'Challenge', 'Outcome'] : ['Today'];
    for (var i = 0; i < n; i++) pick.push(pool.splice(rnd(pool.length), 1)[0]);
    return '<div style="display:flex;gap:14px;flex-wrap:wrap">' + pick.map(function (r, i) { return '<div style="text-align:center;min-width:84px"><div class="small">' + labels[i] +
      '</div><div style="font-size:34px;line-height:1.2">' + r[0] + '</div><b>' + r[1] + '</b><div class="small">' + r[2] + '</div></div>'; }).join('') + '</div>' +
      '<button type="button" id="rune1">Draw one</button> <button type="button" id="rune3">Draw three</button>';
  };

  // ---- Journal (on this device only; export as a text file) ----
  var J = { get: function () { try { return JSON.parse(localStorage.getItem('sky.journal') || '[]'); } catch (e) { return []; } },
    set: function (v) { try { localStorage.setItem('sky.journal', JSON.stringify(v)); return true; } catch (e) { return false; } } };
  R.journal = function () {
    var es = J.get();
    return '<textarea id="jText" rows="3" style="width:100%;box-sizing:border-box" placeholder="A thought, a dream, what the sky looked like…"></textarea>' +
      '<button type="button" id="jSave">Save entry</button> <button type="button" id="jExport"' + (es.length ? '' : ' disabled') + '>Export all (.txt)</button>' +
      '<div id="jList" style="margin-top:6px">' + es.slice(-5).reverse().map(function (e) { return '<div class="small" style="margin-top:4px"><b>' + esc(new Date(e.t).toLocaleString()) + '</b> · ' + esc(e.moon || '') + '<br>' + esc(e.text) + '</div>'; }).join('') +
      (es.length > 5 ? '<div class="small">… and ' + (es.length - 5) + ' earlier (in the export)</div>' : '') + '</div>';
  };
  function moonWord(d) { var ph = norm(A.MoonPhase(d)); return ['New moon', 'Waxing crescent', 'First quarter', 'Waxing gibbous', 'Full moon', 'Waning gibbous', 'Last quarter', 'Waning crescent'][Math.floor((ph + 22.5) / 45) % 8]; }

  // ---- wiring (same pattern as traditions.js) ----
  function wire(id, outId, fn, after, isTradition) {
    var cb = $(id), out = $(outId); if (!cb || !out) return;
    var show = function () {
      out.style.display = cb.checked ? 'block' : 'none'; if (!cb.checked) return;
      try { out.innerHTML = fn(new Date()) + (isTradition ? '<br><span class="trad">tradition &mdash; not astronomy</span>' : ''); if (after) after(show); }
      catch (e) { out.textContent = 'unavailable on this device'; }
    };
    cb.addEventListener('change', show);
    try { if (localStorage.getItem('sky.' + id) === '1') { cb.checked = true; show(); } } catch (e) {}
    cb.addEventListener('change', function () { try { localStorage.setItem('sky.' + id, cb.checked ? '1' : '0'); } catch (e) {} });
  }
  var runeN = 1;
  wire('ovManazil', 'manazilOut', R.manazil, null, true);
  wire('ovXiu', 'xiuOut', R.xiu, null, true);
  wire('ovHours', 'hoursOut', R.hours, null, true);
  wire('ovEvents', 'eventsOut', R.events, null, false);
  wire('ovIching', 'ichingOut', R.iching, function (show) { var b = $('ichingCast'); if (b) b.onclick = show; }, true);
  wire('ovRunes', 'runesOut', function () { return R.runes(runeN); }, function (show) { var a = $('rune1'), b = $('rune3'); if (a) a.onclick = function () { runeN = 1; show(); }; if (b) b.onclick = function () { runeN = 3; show(); }; }, true);
  wire('ovJournal', 'journalOut', R.journal, function (show) {
    var s = $('jSave'), x = $('jExport');
    if (s) s.onclick = function () { var t = ($('jText').value || '').trim(); if (!t) return; var es = J.get(); var d = new Date(); es.push({ t: d.toISOString(), moon: moonWord(d), text: t }); if (!J.set(es)) alert('Could not save — this device blocked storage.'); show(); };
    if (x) x.onclick = function () { var es = J.get(), txt = es.map(function (e) { return new Date(e.t).toLocaleString() + ' · ' + (e.moon || '') + '\n' + e.text + '\n'; }).join('\n');
      var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([txt], { type: 'text/plain' })); a.download = 'sarahs-sky-journal.txt'; document.body.appendChild(a); a.click(); a.remove(); };
  }, false);
  window.SarahTraditions2 = R;   // for tests
})();
