/* Sarah's Sky — Readings: birth chart and tarot spreads.
   Positions are real astronomy (astronomy-engine: true ecliptic of date, apparent geocentric positions).
   The meanings are traditional astrology and tarot: tradition, not astronomy. Everything stays on the device. */
(function () {
  var A = window.Astronomy; if (!A) return;
  var D2R = Math.PI / 180, R2D = 180 / Math.PI;
  var norm = function (x) { x %= 360; return x < 0 ? x + 360 : x; };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  var SG = ['♈︎','♉︎','♊︎','♋︎','♌︎','♍︎','♎︎','♏︎','♐︎','♑︎','♒︎','♓︎'];
  var ELEM = ['Fire','Earth','Air','Water'], MODE = ['Cardinal','Fixed','Mutable'];
  var SIGN_KEY = ['bold, pioneering, direct','steady, sensual, loyal','curious, quick, talkative','caring, protective, moody','proud, warm, expressive',
    'precise, helpful, analytical','fair, social, harmonising','intense, private, transforming','free, seeking, optimistic','ambitious, disciplined, patient',
    'original, independent, humane','dreamy, compassionate, intuitive'];
  var PLANETS = [
    ['Sun', '☉︎', A.Body.Sun, 'identity, vitality, purpose'], ['Moon', '☽︎', A.Body.Moon, 'feelings, needs, home'],
    ['Mercury', '☿︎', A.Body.Mercury, 'mind, speech, learning'], ['Venus', '♀︎', A.Body.Venus, 'love, beauty, values'],
    ['Mars', '♂︎', A.Body.Mars, 'drive, courage, desire'], ['Jupiter', '♃︎', A.Body.Jupiter, 'growth, luck, faith'],
    ['Saturn', '♄︎', A.Body.Saturn, 'structure, limits, mastery'], ['Uranus', '♅︎', A.Body.Uranus, 'change, freedom, surprise'],
    ['Neptune', '♆︎', A.Body.Neptune, 'dreams, spirit, illusion'], ['Pluto', '♇︎', A.Body.Pluto, 'power, depth, rebirth']];
  var HOUSE_KEY = ['self, body, first impressions','money, possessions, worth','siblings, speech, neighbourhood','home, family, roots','creativity, romance, children',
    'work, health, daily routine','partners, marriage, others','shared resources, intimacy, change','travel, study, beliefs','career, reputation, calling',
    'friends, groups, hopes','solitude, the hidden, the spiritual'];
  var ASPECTS = [[0, 'conjunction', '☌', 8, 'blends and intensifies'], [60, 'sextile', '⚹', 5, 'opportunity and ease'], [90, 'square', '□', 7, 'tension that drives growth'],
    [120, 'trine', '△', 7, 'natural flow and talent'], [180, 'opposition', '☍', 8, 'balance between two poles']];

  /* ---------- time: local wall time in a time zone -> UTC ---------- */
  function zoneOffsetMin(utcMs, tz) {
    var p = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }).formatToParts(new Date(utcMs));
    var g = function (t) { return +p.find(function (x) { return x.type === t; }).value; };
    return (Date.UTC(g('year'), g('month') - 1, g('day'), g('hour') % 24, g('minute'), g('second')) - utcMs) / 6e4;
  }
  function toUTC(y, mo, d, h, mi, tz, lon) {
    var wall = Date.UTC(y, mo - 1, d, h, mi);
    if (tz === 'LMT') return new Date(wall - lon / 15 * 36e5);           // local mean time from longitude (old births)
    var t = wall; for (var i = 0; i < 3; i++) t = wall - zoneOffsetMin(t, tz) * 6e4;
    return new Date(t);
  }

  /* ---------- the chart ---------- */
  function lonOfDate(body, date) {
    if (body === A.Body.Sun) return norm(A.SunPosition(date).elon);
    if (body === A.Body.Moon) return norm(A.EclipticGeoMoon(date).lon);
    var v = A.GeoVector(body, date, true);
    return norm(A.SphereFromVector(A.RotateVector(A.Rotation_EQJ_ECT(date), v)).lon);
  }
  function speed(body, date) {   // degrees per day, negative = retrograde
    var a = lonOfDate(body, new Date(date.getTime() - 432e5)), b = lonOfDate(body, new Date(date.getTime() + 432e5));
    return ((b - a + 540) % 360) - 180;
  }
  function angles(date, lat, lon) {
    var eps = A.e_tilt(A.MakeTime(date)).tobl * D2R;
    var ramc = norm(A.SiderealTime(date) * 15 + lon) * D2R, phi = lat * D2R;
    var mc = norm(Math.atan2(Math.sin(ramc), Math.cos(ramc) * Math.cos(eps)) * R2D);
    var asc = norm(Math.atan2(Math.cos(ramc), -(Math.sin(ramc) * Math.cos(eps) + Math.tan(phi) * Math.sin(eps))) * R2D);
    return { asc: asc, mc: mc, ramc: ramc * R2D, eps: eps * R2D };
  }
  function placidus(an, lat) {   // semi-arc trisection, iterated; falls back to Porphyry near the poles
    var eps = an.eps * D2R, phi = lat * D2R, cusps = new Array(12);
    cusps[0] = an.asc; cusps[9] = an.mc; cusps[6] = norm(an.asc + 180); cusps[3] = norm(an.mc + 180);
    if (Math.abs(lat) > 66) return porphyry(an);
    var lamFromRA = function (ra) { return norm(Math.atan2(Math.sin(ra * D2R), Math.cos(ra * D2R) * Math.cos(eps)) * R2D); };
    var spec = [[10, 1 / 3, true], [11, 2 / 3, true], [1, 2 / 3, false], [2, 1 / 3, false]];   // house index, fraction, above horizon
    for (var k = 0; k < spec.length; k++) {
      var idx = spec[k][0], f = spec[k][1], above = spec[k][2], ra = above ? an.ramc + f * 90 : an.ramc + 180 - f * 90, lam = lamFromRA(ra);
      for (var it = 0; it < 30; it++) {
        var dec = Math.asin(Math.sin(eps) * Math.sin(lam * D2R)), x = Math.tan(phi) * Math.tan(dec);
        if (Math.abs(x) >= 1) return porphyry(an);
        var ad = Math.asin(x) * R2D;
        ra = above ? an.ramc + f * (90 + ad) : an.ramc + 180 - f * (90 - ad);
        lam = lamFromRA(ra);
      }
      cusps[idx] = lam; cusps[(idx + 6) % 12] = norm(lam + 180);
    }
    return cusps;
  }
  function porphyry(an) {
    var c = new Array(12);
    var asc = an.asc, mc = an.mc, ic = norm(mc + 180), dsc = norm(asc + 180);
    var tri = function (a, b, n) { var d = norm(b - a); return norm(a + d * n / 3); };
    c[0] = asc; c[1] = tri(asc, ic, 1); c[2] = tri(asc, ic, 2); c[3] = ic; c[4] = tri(ic, dsc, 1); c[5] = tri(ic, dsc, 2);
    c[6] = dsc; c[7] = tri(dsc, mc, 1); c[8] = tri(dsc, mc, 2); c[9] = mc; c[10] = tri(mc, asc, 1); c[11] = tri(mc, asc, 2);
    return c;
  }
  function houseOf(l, cusps) { for (var i = 0; i < 12; i++) { var a = cusps[i], b = cusps[(i + 1) % 12]; if (norm(l - a) < norm(b - a)) return i + 1; } return 1; }

  function compute(inp) {
    var date = toUTC(inp.y, inp.mo, inp.d, inp.h, inp.mi, inp.tz, inp.lon);
    var an = angles(date, inp.lat, inp.lon);
    var ay = inp.sidereal ? 23.8531 + ((date.getTime() - Date.UTC(2000, 0, 1, 12)) / (365.25 * 864e5)) * 50.29 / 3600 : 0;
    var cusps;
    if (inp.houses === 'whole') { var s0 = Math.floor(norm(an.asc - ay) / 30) * 30; cusps = []; for (var i = 0; i < 12; i++) cusps.push(norm(s0 + 30 * i + ay)); }
    else if (inp.houses === 'equal') { cusps = []; for (var j = 0; j < 12; j++) cusps.push(norm(an.asc + 30 * j)); }
    else cusps = placidus(an, inp.lat);
    var pl = PLANETS.map(function (p) { var l = lonOfDate(p[2], date); return { name: p[0], g: p[1], lon: l, slon: norm(l - ay), retro: p[0] !== 'Sun' && p[0] !== 'Moon' && speed(p[2], date) < 0, key: p[3] }; });
    pl.forEach(function (p) { p.house = houseOf(p.lon, cusps); });
    var asp = [];
    for (var a = 0; a < pl.length; a++) for (var b = a + 1; b < pl.length; b++) {
      var sep = Math.abs(((pl[a].lon - pl[b].lon + 540) % 360) - 180);
      ASPECTS.forEach(function (x) { var orb = Math.abs(sep - x[0]); var lim = x[3] + ((pl[a].name === 'Sun' || pl[a].name === 'Moon' || pl[b].name === 'Sun' || pl[b].name === 'Moon') ? 2 : 0); if (orb <= lim) asp.push({ a: pl[a], b: pl[b], x: x, orb: orb }); });
    }
    asp.sort(function (p, q) { return p.orb - q.orb; });
    var bal = [0, 0, 0, 0], mod = [0, 0, 0];
    pl.forEach(function (p) { var s = Math.floor(p.slon / 30); bal[s % 4]++; mod[s % 3]++; });
    return { date: date, an: an, ay: ay, cusps: cusps, pl: pl, asp: asp, bal: bal, mod: mod, inp: inp };
  }

  /* ---------- drawing ---------- */
  function fmtDeg(l) { var s = Math.floor(l / 30), d = l - 30 * s, dd = Math.floor(d), mm = Math.round((d - dd) * 60); if (mm === 60) { dd++; mm = 0; } return dd + '°' + (mm < 10 ? '0' : '') + mm + '′ ' + SG[s] + ' ' + SIGNS[s]; }
  function wheel(c) {
    var W = 340, C = W / 2, R1 = 160, R2 = 132, R3 = 104, R4 = 70, asc = norm(c.an.asc - c.ay);
    var pt = function (l, r) { var a = (180 + (norm(l - c.ay) - asc)) * D2R; return [C + r * Math.cos(a), C - r * Math.sin(a)]; };
    var ptS = function (sl, r) { var a = (180 + (sl - asc)) * D2R; return [C + r * Math.cos(a), C - r * Math.sin(a)]; };
    var o = '<svg viewBox="0 0 ' + W + ' ' + W + '" class="cw" role="img" aria-label="Birth chart wheel"><defs><linearGradient id="cwg" x1="0" x2="1"><stop offset="0" stop-color="#4cc3ff"/><stop offset=".5" stop-color="#7a5cff"/><stop offset="1" stop-color="#ff6ec7"/></linearGradient></defs>';
    o += '<circle cx="' + C + '" cy="' + C + '" r="' + R1 + '" fill="#0b0620" stroke="url(#cwg)"/><circle cx="' + C + '" cy="' + C + '" r="' + R2 + '" fill="none" stroke="#2a1f5a"/><circle cx="' + C + '" cy="' + C + '" r="' + R4 + '" fill="#04020b" stroke="#2a1f5a"/>';
    for (var s = 0; s < 12; s++) {
      var a = ptS(s * 30, R1), b = ptS(s * 30, R2), m = ptS(s * 30 + 15, (R1 + R2) / 2);
      o += '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" stroke="#2a1f5a"/>';
      o += '<text x="' + m[0] + '" y="' + m[1] + '" fill="' + ['#ff6ec7', '#4cc3ff', '#6fb8ff', '#a07bff'][s % 4] + '" font-size="15" text-anchor="middle" dominant-baseline="central">' + SG[s] + '</text>';
    }
    c.cusps.forEach(function (l, i) {
      var a = pt(l, R2), b = pt(l, R4), n = pt(norm(l + norm(c.cusps[(i + 1) % 12] - l) / 2), R4 + 10), ang = (i === 0 || i === 9);
      o += '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" stroke="' + (ang ? '#ff6ec7' : '#3a2d78') + '" stroke-width="' + (ang ? 1.6 : 0.8) + '"/>';
      o += '<text x="' + n[0] + '" y="' + n[1] + '" fill="#a296d8" font-size="8" text-anchor="middle" dominant-baseline="central">' + (i + 1) + '</text>';
    });
    c.asp.forEach(function (x) {
      var a = pt(x.a.lon, R4), b = pt(x.b.lon, R4), col = { square: '#ff3d8b', opposition: '#ff3d8b', trine: '#4cc3ff', sextile: '#6fb8ff', conjunction: '#d43cff' }[x.x[1]];
      if (x.x[0]) o += '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" stroke="' + col + '" stroke-width=".9" opacity=".75"/>';
    });
    var placed = c.pl.slice().sort(function (p, q) { return p.lon - q.lon; }), lastL = -99, shift = 0;
    placed.forEach(function (p) {
      var l = p.lon; if (norm(l - lastL) < 7) shift = (shift + 1) % 3; else shift = 0; lastL = l;
      var g = pt(l, R3 - shift * 14), t = pt(l, R2);
      o += '<line x1="' + t[0] + '" y1="' + t[1] + '" x2="' + pt(l, R2 - 5)[0] + '" y2="' + pt(l, R2 - 5)[1] + '" stroke="#f3eeff"/>';
      o += '<text x="' + g[0] + '" y="' + g[1] + '" fill="#f3eeff" font-size="15" text-anchor="middle" dominant-baseline="central">' + p.g + '</text>';
    });
    return o + '</svg>';
  }

  function report(c) {
    var p = c.pl, h = '';
    var sun = p[0], moon = p[1], ascS = Math.floor(norm(c.an.asc - c.ay) / 30);
    h += '<p class="big3">' + SG[Math.floor(sun.slon / 30)] + ' Sun in <b>' + SIGNS[Math.floor(sun.slon / 30)] + '</b> · ' + SG[Math.floor(moon.slon / 30)] + ' Moon in <b>' + SIGNS[Math.floor(moon.slon / 30)] +
      '</b> · ' + SG[ascS] + ' Rising <b>' + SIGNS[ascS] + '</b></p>';
    h += '<p>The <b>Sun</b> (' + sun.key + ') in ' + SIGNS[Math.floor(sun.slon / 30)] + ' reads as ' + SIGN_KEY[Math.floor(sun.slon / 30)] + ', shown through house ' + sun.house + ' (' + HOUSE_KEY[sun.house - 1] + '). ' +
      'The <b>Moon</b> (' + moon.key + ') in ' + SIGNS[Math.floor(moon.slon / 30)] + ': ' + SIGN_KEY[Math.floor(moon.slon / 30)] + ', in house ' + moon.house + ' (' + HOUSE_KEY[moon.house - 1] + '). ' +
      'The <b>Rising sign</b> ' + SIGNS[ascS] + ' colours the first impression: ' + SIGN_KEY[ascS] + '.</p>';
    h += '<table class="ct"><tr><th>Planet</th><th>Position</th><th>House</th></tr>';
    p.forEach(function (x) { h += '<tr><td>' + x.g + ' ' + x.name + (x.retro ? ' <span title="retrograde">℞</span>' : '') + '</td><td>' + fmtDeg(x.slon) + '</td><td>' + x.house + '</td></tr>'; });
    h += '<tr><td>AC Ascendant</td><td>' + fmtDeg(norm(c.an.asc - c.ay)) + '</td><td>1</td></tr><tr><td>MC Midheaven</td><td>' + fmtDeg(norm(c.an.mc - c.ay)) + '</td><td>10</td></tr></table>';
    h += '<h4>Planets through the signs and houses</h4><ul class="rd">';
    p.slice(2).forEach(function (x) { var s = Math.floor(x.slon / 30); h += '<li><b>' + x.g + ' ' + x.name + '</b> (' + x.key + ') in ' + SIGNS[s] + ' — ' + SIGN_KEY[s] + '; house ' + x.house + ': ' + HOUSE_KEY[x.house - 1] + (x.retro ? '; retrograde: turned inward, revisited' : '') + '.</li>'; });
    h += '</ul><h4>Main aspects</h4><ul class="rd">';
    c.asp.slice(0, 12).forEach(function (x) { h += '<li>' + x.a.g + ' ' + x.a.name + ' ' + x.x[2] + ' ' + x.b.g + ' ' + x.b.name + ' — ' + x.x[1] + ' (orb ' + x.orb.toFixed(1) + '°): ' + x.x[4] + '.</li>'; });
    h += '</ul><h4>Balance</h4><p>' + ELEM.map(function (e, i) { return e + ' ' + c.bal[i]; }).join(' · ') + '<br>' + MODE.map(function (m, i) { return m + ' ' + c.mod[i]; }).join(' · ') + '</p>';
    h += '<p class="trad">' + (c.inp.sidereal ? 'Sidereal zodiac (Lahiri ' + c.ay.toFixed(2) + '°). ' : 'Tropical zodiac. ') + ({ placidus: 'Placidus', whole: 'Whole-sign', equal: 'Equal' })[c.inp.houses] +
      ' houses. Positions computed from the real sky at ' + c.date.toISOString().replace('T', ' ').slice(0, 16) + ' UTC. Meanings are astrological tradition, not astronomy.</p>';
    return h;
  }

  /* ---------- tarot spreads ---------- */
  var SPREADS = {
    one: ['The answer'],
    three: ['Past', 'Present', 'Future'],
    mind: ['Mind', 'Body', 'Spirit'],
    celtic: ['The heart of the matter', 'What crosses it', 'The root below', 'The recent past', 'The best that can be', 'The near future', 'You, as you are', 'Your surroundings', 'Hopes and fears', 'The outcome']
  };
  function rnd(n) { var a = new Uint32Array(1); (window.crypto || window.msCrypto).getRandomValues(a); return a[0] % n; }
  function tarotCard(i, rev) {
    var T = window.SarahTarot; if (!T) return { name: '?', mean: '' };
    if (i < 22) return { name: T.MAJOR[i][0], mean: rev ? T.MAJOR[i][2] : T.MAJOR[i][1], major: true };
    var k = i - 22, s = T.SUITS[Math.floor(k / 14)], r = T.RANKS[k % 14];
    return { name: r[0] + ' of ' + s[0], mean: r[1] + ' in ' + s[1] + (rev ? ' — reversed: blocked or turned inward' : '') };
  }
  function drawSpread(kind) {
    var pos = SPREADS[kind], deck = []; for (var i = 0; i < 78; i++) deck.push(i);
    for (var j = deck.length - 1; j > 0; j--) { var r = rnd(j + 1), t = deck[j]; deck[j] = deck[r]; deck[r] = t; }   // Fisher-Yates
    return pos.map(function (p, n) { var rev = rnd(2) === 1; var c = tarotCard(deck[n], rev); return { pos: p, card: c, rev: rev }; });
  }
  function spreadHTML(cards, q) {
    var h = q ? '<p class="q">“' + esc(q) + '”</p>' : '';
    h += '<div class="spread">';
    cards.forEach(function (x, i) {
      h += '<div class="tc' + (x.rev ? ' rev' : '') + (x.card.major ? ' maj' : '') + '" style="animation-delay:' + (i * 0.18) + 's"><div class="tcp">' + (i + 1) + '. ' + x.pos + '</div><div class="tcn">' + esc(x.card.name) + (x.rev ? ' ↺' : '') + '</div><div class="tcm">' + esc(x.card.mean) + '</div></div>';
    });
    var maj = cards.filter(function (x) { return x.card.major; }).length;
    h += '</div><p class="trad">' + maj + ' of ' + cards.length + ' cards are Major Arcana' + (maj * 2 > cards.length ? ' — a reading about big themes.' : '.') + ' Tarot is a tradition for reflection, not prediction.</p>';
    return h;
  }

  /* ---------- UI ---------- */
  function zones() {
    var here = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC', list = [];
    try { list = Intl.supportedValuesOf('timeZone'); } catch (e) { list = [here, 'UTC']; }
    return '<option value="' + here + '">' + here + ' (this device)</option><option value="LMT">Local mean time (from longitude, for old births)</option>' +
      list.map(function (z) { return '<option>' + z + '</option>'; }).join('');
  }
  function build() {
    var m = document.createElement('div'); m.id = 'readings'; m.hidden = true;
    m.innerHTML = '<div class="rbox"><div class="rhead"><b>✨ Readings</b><div class="rtabs"><button data-r="chart" class="on">Birth chart</button><button data-r="tarot">Tarot</button></div><button id="rClose" aria-label="Close">×</button></div>' +
      '<div class="rbody" id="rChart"><form id="cForm" class="cf">' +
      '<label>Name <input id="cName" placeholder="optional"></label>' +
      '<label>Birth date <input id="cDate" type="date" required></label>' +
      '<label>Birth time <input id="cTime" type="time" value="12:00" required></label>' +
      '<label>Time zone <select id="cTz">' + zones() + '</select></label>' +
      '<label>Birthplace <span class="row"><input id="cPlace" placeholder="City, country"><button type="button" id="cFind">Find</button></span></label>' +
      '<label class="half">Latitude <input id="cLat" type="number" step="any" required placeholder="35.47"></label><label class="half">Longitude <input id="cLon" type="number" step="any" required placeholder="-97.52"></label>' +
      '<label class="half">Houses <select id="cHouses"><option value="placidus">Placidus</option><option value="whole">Whole sign</option><option value="equal">Equal</option></select></label>' +
      '<label class="half">Zodiac <select id="cZod"><option value="trop">Tropical (Western)</option><option value="sid">Sidereal (Vedic, Lahiri)</option></select></label>' +
      '<div class="row"><button type="submit" class="go">Cast chart</button><button type="button" id="cHere">Use my location</button><select id="cSaved"><option value="">Saved charts…</option></select></div>' +
      '<p class="trad">“Find” looks the place up on OpenStreetMap (only the place name is sent). Charts are saved only on this device.</p></form><div id="cOut"></div></div>' +
      '<div class="rbody" id="rTarot" hidden><label>Your question (optional) <input id="tQ" placeholder="What do I need to know about…"></label>' +
      '<div class="row tb"><button data-s="one">One card</button><button data-s="three">Past · Present · Future</button><button data-s="mind">Mind · Body · Spirit</button><button data-s="celtic">Celtic Cross</button></div><div id="tOut"></div></div></div>';
    document.body.appendChild(m);
    m.querySelectorAll('.rtabs button').forEach(function (b) { b.onclick = function () { m.querySelectorAll('.rtabs button').forEach(function (x) { x.classList.toggle('on', x === b); }); $('rChart').hidden = b.dataset.r !== 'chart'; $('rTarot').hidden = b.dataset.r !== 'tarot'; }; });
    $('rClose').onclick = function () { m.hidden = true; };
    $('cHere').onclick = function () { navigator.geolocation && navigator.geolocation.getCurrentPosition(function (p) { $('cLat').value = p.coords.latitude.toFixed(4); $('cLon').value = p.coords.longitude.toFixed(4); }, function () {}, { enableHighAccuracy: true, timeout: 10000 }); };
    $('cFind').onclick = function () {
      var q = $('cPlace').value.trim(); if (!q) return; $('cFind').textContent = '…';
      fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(q)).then(function (r) { return r.json(); }).then(function (j) {
        if (j && j[0]) { $('cLat').value = (+j[0].lat).toFixed(4); $('cLon').value = (+j[0].lon).toFixed(4); $('cPlace').value = j[0].display_name.split(',').slice(0, 3).join(','); }
        else $('cPlace').value = q + ' (not found — enter latitude/longitude)';
      }).catch(function () { $('cPlace').value = q + ' (offline — enter latitude/longitude)'; }).then(function () { $('cFind').textContent = 'Find'; });
    };
    var saved = function () { try { return JSON.parse(localStorage.getItem('sky.charts') || '[]'); } catch (e) { return []; } };
    var fillSaved = function () { $('cSaved').innerHTML = '<option value="">Saved charts…</option>' + saved().map(function (s, i) { return '<option value="' + i + '">' + esc(s.name || s.date) + '</option>'; }).join(''); };
    fillSaved();
    $('cSaved').onchange = function () { var s = saved()[+this.value]; if (!s) return; ['Name', 'Date', 'Time', 'Tz', 'Place', 'Lat', 'Lon', 'Houses', 'Zod'].forEach(function (k) { if (s[k.toLowerCase()] != null) $('c' + k).value = s[k.toLowerCase()]; }); $('cForm').requestSubmit(); };
    $('cForm').onsubmit = function (e) {
      e.preventDefault();
      var dt = $('cDate').value.split('-'), tm = $('cTime').value.split(':');
      var inp = { y: +dt[0], mo: +dt[1], d: +dt[2], h: +tm[0], mi: +tm[1], tz: $('cTz').value, lat: +$('cLat').value, lon: +$('cLon').value, houses: $('cHouses').value, sidereal: $('cZod').value === 'sid' };
      if (!isFinite(inp.lat) || !isFinite(inp.lon) || !inp.y) { $('cOut').innerHTML = '<p>Please enter the date, time and place (latitude/longitude).</p>'; return; }
      try {
        var c = compute(inp);
        $('cOut').innerHTML = '<h3>' + esc($('cName').value || 'Birth chart') + '</h3>' + wheel(c) + report(c);
        var rec = { name: $('cName').value, date: $('cDate').value, time: $('cTime').value, tz: inp.tz, place: $('cPlace').value, lat: inp.lat, lon: inp.lon, houses: inp.houses, zod: $('cZod').value };
        var all = saved().filter(function (s) { return !(s.name === rec.name && s.date === rec.date && s.time === rec.time); }); all.unshift(rec);
        try { localStorage.setItem('sky.charts', JSON.stringify(all.slice(0, 30))); } catch (e2) {} fillSaved();
        $('cOut').scrollIntoView({ behavior: 'smooth', block: 'start' });
      } catch (err) { $('cOut').innerHTML = '<p>Could not compute this chart: ' + esc(err.message || err) + '</p>'; }
    };
    m.querySelectorAll('.tb button').forEach(function (b) { b.onclick = function () { $('tOut').innerHTML = spreadHTML(drawSpread(b.dataset.s), $('tQ').value.trim()); $('tOut').scrollIntoView({ behavior: 'smooth', block: 'start' }); }; });
  }
  window.SarahReadings = { compute: compute, open: function (tab) { var m = $('readings'); if (!m) { build(); m = $('readings'); } m.hidden = false; if (tab) m.querySelector('[data-r="' + tab + '"]').click(); } };
})();
