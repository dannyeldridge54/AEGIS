/* Sarah's Sky — AR "Point & See" engine.
   Point the phone at the sky; stars/planets/constellations are drawn where they really are.
   Honest status: positions are real (Hipparcos bright stars + Astronomy Engine planets).
   The device-compass heading is approximate on many phones, so "Set North" lets Sarah
   nudge it against a star she knows. The catalog is swappable: AR.updateCatalog(stars)
   drops in the deeper AEGIS/Gaia list when it's ready, no app rebuild.
   Palette + feel match the Janus apps. No network, no accounts, nothing leaves the phone. */
(function () {
  'use strict';
  var A = window.Astronomy;
  var D2R = Math.PI / 180, R2D = 180 / Math.PI;

  var cam = document.getElementById('cam'), cv = document.getElementById('sky'), ctx = cv.getContext('2d');
  var gate = document.getElementById('gate'), hud = document.getElementById('hud'),
      readout = document.getElementById('readout'), retic = document.getElementById('retic'),
      lookB = document.getElementById('look'), info = document.getElementById('info'), errBox = document.getElementById('err');

  var state = {
    stars: [], cons: [], deep: [], planets: [],
    show: { stars: true, lines: true, planets: true, deep: false, zodiac: false },
    observer: null, flip: false, headingOffset: (function () { try { return parseFloat(localStorage.getItem('sky.headingOffset')) || 0; } catch (e) { return 0; } })(), zoom: 35,
    R: null, haveOrient: false, calMode: false, DPR: Math.min(2, window.devicePixelRatio || 1),
    locked: false, manAz: 0, manAlt: 30, manRoll: 0   // locked view: phone can move; touch pans on the az/alt axes
  };
  window.AR = {
    // swap in a deeper catalog later: [{name,ra,dec,mag,bv?,desig?}] (ra/dec in degrees)
    updateCatalog: function (stars) { if (Array.isArray(stars) && stars.length) { state.stars = prep(stars); toast(stars.length + ' stars loaded'); } },
    get state() { return state; }
  };

  var panMoved = false;   // true when the last single-finger gesture was a drag (so it isn't treated as a tap)
  function showErr(m) { errBox.textContent = m; errBox.style.display = 'block'; }
  function toast(m) { showErr(m); setTimeout(function () { errBox.style.display = 'none'; }, 2200); }

  /* ---------- catalog prep ---------- */
  function bvColor(bv) {
    bv = parseFloat(bv); if (isNaN(bv)) bv = 0.6;
    // warm (red) high bv -> cool (blue) low bv, tinted toward the Janus palette
    var t = Math.max(0, Math.min(1, (bv + 0.3) / 1.8)); // 0 blue .. 1 red
    var r = Math.round(150 + 105 * t), g = Math.round(180 + 30 * Math.abs(0.5 - t) * -1 + 200 * (1 - Math.abs(t - 0.5))), b = Math.round(255 - 120 * t);
    g = Math.max(150, Math.min(240, g));
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }
  function prep(list) {
    return list.map(function (s) {
      return { name: s.name || s.desig || '', desig: s.desig || '', mag: s.mag == null ? 5 : s.mag,
        ra: s.ra, dec: s.dec, col: bvColor(s.bv), v: raDecToVec(s.ra, s.dec) };
    });
  }
  // RA/Dec (deg, J2000-ish) -> unit vector in an equatorial frame (we only need Horizon for az/alt, kept for deep lines)
  function raDecToVec(ra, dec) { var r = ra * D2R, d = dec * D2R; return [Math.cos(d) * Math.cos(r), Math.cos(d) * Math.sin(r), Math.sin(d)]; }

  /* ---------- load data ---------- */
  function loadJSON(u) { return fetch(u).then(function (r) { return r.json(); }); }
  function loadAll() {
    return Promise.all([
      loadJSON('data/stars.json').then(function (d) { state.stars = prep(d.stars || d); }).catch(function(){}),
      loadJSON('data/constellations.json').then(function (d) { state.cons = d.features || d.constellations || d; }).catch(function(){}),
      loadJSON('data/messier.json').then(function (d) { state.deep = (d.objects || d).map(function (o) { return { name: o.name || o.id, ra: o.ra, dec: o.dec, kind: o.type || 'deep sky', v: raDecToVec(o.ra, o.dec) }; }); }).catch(function(){})
    ]);
  }

  /* ---------- geolocation ---------- */
  function getLoc() {
    // Best fix within ~12 s (watchPosition keeps improving), remembered on the device for next time.
    // Note: for the sky, 1 km of GPS error moves stars by less than 0.01 deg - the compass matters far more.
    return new Promise(function (res) {
      var saved = null; try { saved = JSON.parse(localStorage.getItem('sky.loc') || 'null'); } catch (e) {}
      var fallback = function () {
        if (saved) { toast('Using your last saved location'); return res(mk(saved.lat, saved.lon, saved.h)); }
        toast('Location unavailable - using Oklahoma City. The view may be shifted if you are far away.');
        res(mk(35.47, -97.52, 390));
      };
      if (!navigator.geolocation) return fallback();
      var best = null, done = false, id = null;
      var finish = function () {
        if (done) return; done = true; if (id != null) navigator.geolocation.clearWatch(id);
        if (!best) return fallback();
        var c = best.coords, h = (c.altitude != null && isFinite(c.altitude)) ? c.altitude : 300;
        try { localStorage.setItem('sky.loc', JSON.stringify({ lat: c.latitude, lon: c.longitude, h: h })); } catch (e) {}
        toast('Location set (±' + Math.round(c.accuracy) + ' m)');
        res(mk(c.latitude, c.longitude, h));
      };
      id = navigator.geolocation.watchPosition(function (p) {
        if (!best || p.coords.accuracy < best.coords.accuracy) best = p;
        if (best.coords.accuracy <= 30) finish();
      }, function () { finish(); }, { enableHighAccuracy: true, maximumAge: 60000, timeout: 15000 });
      setTimeout(finish, 12000);
    });
    function mk(lat, lon, h) { return new A.Observer(lat, lon, h); }
  }

  /* ---------- planets ---------- */
  var PLANETS = [
    ['Mercury', A.Body.Mercury, '#c9b7ff'], ['Venus', A.Body.Venus, '#fff3c0'],
    ['Mars', A.Body.Mars, '#ff6e6e'], ['Jupiter', A.Body.Jupiter, '#ffd9a0'],
    ['Saturn', A.Body.Saturn, '#f0e2b0'], ['Moon', A.Body.Moon, '#dfe7ff'], ['Sun', A.Body.Sun, '#ffd34c']
  ];
  function computePlanets(date) {
    var out = [];
    for (var i = 0; i < PLANETS.length; i++) {
      try {
        var eq = A.Equator(PLANETS[i][1], date, state.observer, true, true);
        out.push({ name: PLANETS[i][0], col: PLANETS[i][2], ra: eq.ra * 15, dec: eq.dec, moon: PLANETS[i][0] === 'Moon', sun: PLANETS[i][0] === 'Sun' });
      } catch (e) {}
    }
    state.planets = out;
  }

  /* ---------- horizon (alt/az) ---------- */
  function altaz(date, raDeg, decDeg) {
    var h = A.Horizon(date, state.observer, raDeg / 15, decDeg, 'normal');
    return { alt: h.altitude, az: h.azimuth }; // az from North, clockwise
  }
  // alt/az (+heading offset) -> ENU unit vector (x=East,y=North,z=Up)
  function altazToENU(alt, az) {
    var a = (az + state.headingOffset) * D2R, e = alt * D2R, ce = Math.cos(e);
    return [ce * Math.sin(a), ce * Math.cos(a), Math.sin(e)];
  }

  /* ---------- device orientation -> world rotation ---------- */
  // Returns matrix mapping device axes to a world frame x=East,y=North,z=Up.
  function rotFromEuler(alpha, beta, gamma) {
    var _x = beta * D2R, _y = gamma * D2R, _z = alpha * D2R;
    var cX = Math.cos(_x), cY = Math.cos(_y), cZ = Math.cos(_z),
        sX = Math.sin(_x), sY = Math.sin(_y), sZ = Math.sin(_z);
    // W3C deviceorientation ZXY intrinsic
    return [
      cZ * cY - sZ * sX * sY, -cX * sZ, cZ * sY + cY * sZ * sX,
      cY * sZ + cZ * sX * sY,  cX * cZ, sZ * sY - cZ * cY * sX,
      -cX * sY,                sX,      cX * cY
    ];
  }
  function mulVec(m, v) { return [m[0]*v[0]+m[1]*v[1]+m[2]*v[2], m[3]*v[0]+m[4]*v[1]+m[5]*v[2], m[6]*v[0]+m[7]*v[1]+m[8]*v[2]]; }
  function rotZ(v, ang) { var c = Math.cos(ang), s = Math.sin(ang); return [c*v[0]-s*v[1], s*v[0]+c*v[1], v[2]]; }

  // Locked view: build the camera basis from a manual az/alt (+roll) instead of the live phone orientation,
  // so the sky holds still and the phone can move. Touch drag changes manAz/manAlt; pinch changes zoom.
  function setManualR() {
    var az = (state.manAz + state.headingOffset) * D2R, alt = state.manAlt * D2R, ce = Math.cos(alt);
    var look = [ce * Math.sin(az), ce * Math.cos(az), Math.sin(alt)];
    var wUp = [0, 0, 1];
    // right = normalize(worldUp x look); up = normalize(look x right); then apply roll about look
    var right = norm(cross(wUp, look)); if (!isFinite(right[0])) right = [1, 0, 0];
    var up = norm(cross(look, right));
    var rr = state.manRoll * D2R, c = Math.cos(rr), s = Math.sin(rr), i, R2 = [0, 0, 0], U2 = [0, 0, 0];
    for (i = 0; i < 3; i++) { R2[i] = right[i] * c + up[i] * s; U2[i] = up[i] * c - right[i] * s; }
    state.R = { look: look, up: U2, right: R2 };
  }
  function cross(a, b) { return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]; }
  function norm(v) { var n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0]/n, v[1]/n, v[2]/n]; }

  var compassHeading = null;   // iOS magnetic heading if available
  var absSeen = false, iosOffset = null, SM = 0.25, prevR = null;
  function blend(a, b) { return norm([a[0] + SM * (b[0] - a[0]), a[1] + SM * (b[1] - a[1]), a[2] + SM * (b[2] - a[2])]); }
  function onOrient(ev) {
    if (ev.alpha == null) return;
    var isAbs = ev.type === 'deviceorientationabsolute' || ev.absolute === true;
    if (isAbs) absSeen = true;
    else if (absSeen) return;            // Android: ignore the relative stream once the compass-referenced one exists
    var alpha = ev.alpha;
    if (typeof ev.webkitCompassHeading === 'number' && !isNaN(ev.webkitCompassHeading)) {
      compassHeading = ev.webkitCompassHeading;
      // iOS alpha is relative; tie it to the compass while the phone is near flat, then keep that offset
      if (Math.abs(ev.beta) < 50 && Math.abs(ev.gamma) < 50) {
        var off = ((360 - compassHeading) - ev.alpha + 540) % 360 - 180;
        iosOffset = iosOffset == null ? off : iosOffset + 0.1 * (((off - iosOffset + 540) % 360) - 180);
      }
      if (iosOffset != null) alpha = ev.alpha + iosOffset;
    }
    state.haveOrient = true;
    if (state.locked) return;   // frozen: the phone no longer drives the view
    var scr = (screen.orientation && screen.orientation.angle) || window.orientation || 0;
    var m = rotFromEuler(alpha, ev.beta, ev.gamma);
    // back camera look = device -Z ; screen up = device +Y ; screen right = device +X (rotated by screen angle)
    var look = mulVec(m, [0, 0, -1]), up0 = mulVec(m, [0, 1, 0]), right0 = mulVec(m, [1, 0, 0]);
    var sa = scr * D2R, c = Math.cos(sa), s = Math.sin(sa), i;
    var up = [0, 0, 0], right = [0, 0, 0];
    for (i = 0; i < 3; i++) { up[i] = up0[i] * c + right0[i] * s; right[i] = right0[i] * c - up0[i] * s; }
    if (prevR) { look = blend(prevR.look, look); up = blend(prevR.up, up); right = blend(prevR.right, right); }   // steady the jitter
    prevR = { look: look, up: up, right: right };
    state.R = prevR;
  }
  function dot(a, b) { return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]; }

  /* ---------- projection ---------- */
  function fov() { // zoom 0..100 -> vertical FOV 90deg .. 2deg on a log scale (each step feels the same)
    return 90 * Math.pow(2 / 90, state.zoom / 100) * D2R;
  }
  function project(enu, W, H) {
    var R = state.R; if (!R) return null;
    var dep = dot(enu, R.look); if (dep <= 0.02) return null;
    var x = dot(enu, R.right) / dep, y = dot(enu, R.up) / dep;
    var vf = fov(), hf = 2 * Math.atan(Math.tan(vf / 2) * (W / H));
    var sx = W / 2 + (x / Math.tan(hf / 2)) * (W / 2);
    var sy = H / 2 - (y / Math.tan(vf / 2)) * (H / 2);
    if (sx < -40 || sx > W + 40 || sy < -40 || sy > H + 40) return null;
    return { x: sx, y: sy, dep: dep };
  }

  /* ---------- render loop ---------- */
  var lastDate = 0, cache = { stars: [], planets: [], deep: [] };
  function recompute(date) {
    // alt/az changes with time; recompute a few times a minute is plenty
    var i, s;
    cache.stars = [];
    for (i = 0; i < state.stars.length; i++) { s = state.stars[i]; var aa = altaz(date, s.ra, s.dec); if (aa.alt > -2) cache.stars.push({ s: s, enu: altazToENU(aa.alt, aa.az), alt: aa.alt, az: aa.az }); }
    cache.deep = [];
    for (i = 0; i < state.deep.length; i++) { s = state.deep[i]; var ad = altaz(date, s.ra, s.dec); if (ad.alt > -2) cache.deep.push({ s: s, enu: altazToENU(ad.alt, ad.az), alt: ad.alt, az: ad.az }); }
    computePlanets(date);
    cache.planets = [];
    for (i = 0; i < state.planets.length; i++) { s = state.planets[i]; var ap = altaz(date, s.ra, s.dec); cache.planets.push({ s: s, enu: altazToENU(ap.alt, ap.az), alt: ap.alt, az: ap.az }); }
    // constellation star lookup by designation for lines
  }

  function sizeCanvas() {
    var W = window.innerWidth, H = window.innerHeight, d = state.DPR;
    cv.width = W * d; cv.height = H * d; cv.style.width = W + 'px'; cv.style.height = H + 'px';
    ctx.setTransform(d, 0, 0, d, 0, 0);
  }

  var hitList = [];
  function draw() {
    var W = window.innerWidth, H = window.innerHeight;
    ctx.clearRect(0, 0, W, H);
    var now = Date.now();
    if (now - lastDate > 4000 && state.observer) { recompute(new Date()); lastDate = now; }
    hitList = [];
    if (!state.R) { requestAnimationFrame(draw); return; }

    // constellation lines (polylines of [ra,dec])
    if (state.show.lines) drawLines(W, H);

    // zodiac band (tradition): draw the ecliptic + 12 sign ticks + Sun/Moon sign readout
    if (state.show.zodiac) drawZodiac(W, H);
    updateTraditions();
    drawCompass(W, H);
    drawMiniMap(W, H);

    // deep sky
    if (state.show.deep) {
      for (var di = 0; di < cache.deep.length; di++) {
        var pd = project(cache.deep[di].enu, W, H); if (!pd) continue;
        ctx.strokeStyle = 'rgba(111,184,255,.8)'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(pd.x, pd.y, 6, 0, 6.2832); ctx.stroke();
        hitList.push({ x: pd.x, y: pd.y, r: 14, o: cache.deep[di].s, kind: 'deep' });
      }
    }

    // stars
    if (state.show.stars) {
      for (var i = 0; i < cache.stars.length; i++) {
        var p = project(cache.stars[i].enu, W, H); if (!p) continue;
        var s = cache.stars[i].s, r = Math.max(0.7, 3.2 - s.mag * 0.52);
        ctx.globalAlpha = Math.max(.35, Math.min(1, 1.3 - s.mag * 0.12));
        ctx.fillStyle = s.col;
        ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, 6.2832); ctx.fill();
        if (s.mag < 1.6) { ctx.globalAlpha = .25; ctx.beginPath(); ctx.arc(p.x, p.y, r + 3, 0, 6.2832); ctx.fill(); }
        ctx.globalAlpha = 1;
        if (s.mag < 2.2 && s.name) { ctx.fillStyle = 'rgba(243,238,255,.75)'; ctx.font = '11px Segoe UI,sans-serif'; ctx.fillText(s.name, p.x + r + 3, p.y + 3); }
        if (s.mag < 3) hitList.push({ x: p.x, y: p.y, r: 16, o: s, kind: 'star' });
      }
    }

    // planets
    if (state.show.planets) {
      for (var pi = 0; pi < cache.planets.length; pi++) {
        var cp = cache.planets[pi]; if (cp.s.sun && cp.alt > -6) { /* skip blazing sun marker at day? still show */ }
        var pp = project(cp.enu, W, H); if (!pp) continue;
        var rad = cp.s.moon ? 9 : (cp.s.sun ? 10 : 5);
        ctx.fillStyle = cp.s.col; ctx.globalAlpha = .95;
        ctx.beginPath(); ctx.arc(pp.x, pp.y, rad, 0, 6.2832); ctx.fill();
        ctx.globalAlpha = .3; ctx.beginPath(); ctx.arc(pp.x, pp.y, rad + 5, 0, 6.2832); ctx.fill(); ctx.globalAlpha = 1;
        ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Segoe UI,sans-serif'; ctx.fillText(cp.s.name, pp.x + rad + 4, pp.y + 4);
        hitList.push({ x: pp.x, y: pp.y, r: 20, o: cp.s, kind: 'planet' });
      }
    }

    // readout
    var la = lookAltAz();
    var _az = ((Math.round(la.az) % 360) + 360) % 360, _al = Math.round(la.alt) || 0;
    var _fv = fov() * R2D, _mag = 24 / _fv;   // ×1 = the starting view
    lookB.innerHTML = 'alt <b>' + _al + '°</b> · az <b>' + _az + '°</b> · view <b>' + (_fv < 10 ? _fv.toFixed(1) : _fv.toFixed(0)) + '°</b>' + (Math.abs(_mag - 1) >= 0.1 ? ' (×' + _mag.toFixed(_mag < 10 ? 1 : 0) + ')' : '') + ((compassHeading != null || absSeen) ? '' : ' <span style="color:#ff9" title="no compass: tap Set North">~</span>');
    requestAnimationFrame(draw);
  }

  function drawLines(W, H) {
    if (!state.consPolys) return;
    ctx.strokeStyle = 'rgba(160,123,255,.30)'; ctx.lineWidth = 1;
    var date = new Date(lastDate || Date.now());
    for (var i = 0; i < state.consPolys.length; i++) {
      var ln = state.consPolys[i], started = false; ctx.beginPath();
      for (var j = 0; j < ln.length; j++) {
        var ra = ln[j][0], dec = ln[j][1]; if (ra < 0) ra += 360;
        var aa = altaz(date, ra, dec); if (aa.alt < -6) { started = false; continue; }
        var p = project(altazToENU(aa.alt, aa.az), W, H); if (!p) { started = false; continue; }
        if (!started) { ctx.moveTo(p.x, p.y); started = true; } else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }
  }
  function lookAltAz() {
    var L = state.R ? state.R.look : [0, 1, 0];
    var alt = Math.asin(Math.max(-1, Math.min(1, L[2]))) * R2D;
    var az = Math.atan2(L[0], L[1]) * R2D; if (az < 0) az += 360;
    return { alt: alt, az: (az - state.headingOffset + 360) % 360 };
  }

  var SIGNS12 = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  var PHASES = ['New moon','Waxing crescent','First quarter','Waxing gibbous','Full moon','Waning gibbous','Last quarter','Waning crescent'];
  var tradEl = document.getElementById('trad'), tradTxt = document.getElementById('tradText'), tradAt = 0;
  function updateTraditions() {
    if (!state.show.zodiac) { if (tradEl) tradEl.style.display = 'none'; return; }
    if (tradEl) tradEl.style.display = 'block';
    var now = Date.now(); if (now - tradAt < 5000) return; tradAt = now;
    try {
      var d = new Date();
      var sun = A.SunPosition(d), moon = A.EclipticGeoMoon(d), ph = A.MoonPhase(d);
      var sunSign = SIGNS12[Math.floor((sun.elon % 360) / 30) % 12];
      var moonSign = SIGNS12[Math.floor((moon.lon % 360) / 30) % 12];
      var phase = PHASES[Math.floor(((ph % 360) + 22.5) / 45) % 8];
      if (tradTxt) tradTxt.innerHTML = '☉ Sun in <b>' + sunSign + '</b> · ☾ Moon in <b>' + moonSign + '</b> · ' + phase;
    } catch (e) {}
  }
  // --- cosmic compass (top-left): a rose whose needle shows the view azimuth; tinted magenta when locked ---
  function drawCompass(W, H) {
    var la = lookAltAz(), r = 30, cx = 20 + r + safeL(), cy = 56 + r;
    ctx.save();
    ctx.fillStyle = 'rgba(6,2,20,.62)'; ctx.beginPath(); ctx.arc(cx, cy, r + 7, 0, 6.2832); ctx.fill();
    ctx.strokeStyle = state.locked ? 'rgba(255,79,216,.75)' : 'rgba(76,195,255,.6)'; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, 6.2832); ctx.stroke();
    ctx.fillStyle = 'rgba(185,169,230,.9)'; ctx.font = '9px Segoe UI,sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('N', cx, cy - r + 7); ctx.fillText('S', cx, cy + r - 7); ctx.fillText('E', cx + r - 7, cy); ctx.fillText('W', cx - r + 7, cy);
    // needle to the current azimuth (N up, E right)
    var a = la.az * D2R, nx = cx + Math.sin(a) * (r - 9), ny = cy - Math.cos(a) * (r - 9);
    ctx.strokeStyle = '#ff4fd8'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(nx, ny); ctx.stroke();
    ctx.fillStyle = '#ff6ec7'; ctx.beginPath(); ctx.arc(nx, ny, 2.6, 0, 6.2832); ctx.fill();
    // altitude pip: a little tick ring, filled toward zenith
    ctx.fillStyle = '#4cc3ff'; ctx.beginPath(); ctx.arc(cx, cy, 2, 0, 6.2832); ctx.fill();
    ctx.fillStyle = 'rgba(243,238,255,.9)'; ctx.font = '8px Segoe UI,sans-serif';
    ctx.fillText(la.alt.toFixed(0) + '°', cx, cy + r + 9);
    ctx.restore();
  }
  function safeL() { return 0; }

  // --- sky mini-map (top-right): azimuthal all-sky radar, zenith at centre, horizon at the rim. Shows where you're aimed. ---
  function drawMiniMap(W, H) {
    var R = 44, cx = W - 18 - R, cy = 56 + R;
    ctx.save();
    ctx.fillStyle = 'rgba(6,2,20,.62)'; ctx.beginPath(); ctx.arc(cx, cy, R + 7, 0, 6.2832); ctx.fill();
    ctx.strokeStyle = 'rgba(76,195,255,.5)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832); ctx.stroke();
    ctx.strokeStyle = 'rgba(160,123,255,.18)'; ctx.beginPath(); ctx.arc(cx, cy, R * 0.5, 0, 6.2832); ctx.stroke();
    ctx.fillStyle = 'rgba(185,169,230,.75)'; ctx.font = '8px Segoe UI,sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('N', cx, cy - R + 6); ctx.fillText('S', cx, cy + R - 6); ctx.fillText('E', cx + R - 6, cy); ctx.fillText('W', cx - R + 6, cy);
    function pt(alt, az) { var rr = (1 - Math.max(0, alt) / 90) * R, aa = az * D2R; return [cx + rr * Math.sin(aa), cy - rr * Math.cos(aa)]; }
    function dot(alt, az, col, rad) { if (alt < 0) return; var p = pt(alt, az); ctx.fillStyle = col; ctx.beginPath(); ctx.arc(p[0], p[1], rad, 0, 6.2832); ctx.fill(); }
    var i;
    for (i = 0; i < cache.stars.length; i++) if (cache.stars[i].s.mag < 1.7) dot(cache.stars[i].alt, cache.stars[i].az, 'rgba(243,238,255,.8)', 1.2);
    for (i = 0; i < cache.planets.length; i++) { var cp = cache.planets[i]; dot(cp.alt, cp.az, cp.s.col, cp.s.moon || cp.s.sun ? 2.6 : 1.8); }
    // current view marker + a little field-of-view wedge
    var la = lookAltAz();
    if (la.alt > -4) {
      var p = pt(la.alt, la.az), vf = fov() * R2D, a0 = la.az;
      ctx.strokeStyle = 'rgba(255,79,216,.5)'; ctx.fillStyle = 'rgba(255,79,216,.12)';
      var p1 = pt(Math.max(0, la.alt), a0 - vf * 0.7), p2 = pt(Math.max(0, la.alt), a0 + vf * 0.7);
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(p1[0], p1[1]); ctx.lineTo(p[0], p[1]); ctx.lineTo(p2[0], p2[1]); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#ff4fd8'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(p[0], p[1], 4, 0, 6.2832); ctx.stroke();
    }
    ctx.restore();
    state._mini = { cx: cx, cy: cy, R: R };   // for tap-to-aim
  }
  // tap on the mini-map -> aim there (locks the view so the tap holds)
  function miniAim(sx, sy) {
    var m = state._mini; if (!m) return false;
    var dx = sx - m.cx, dy = sy - m.cy, rr = Math.hypot(dx, dy); if (rr > m.R + 4) return false;
    var alt = 90 * (1 - rr / m.R), az = (Math.atan2(dx, -dy) * R2D + 360) % 360;
    state.manAz = (az - state.headingOffset + 360) % 360; state.manAlt = Math.max(-5, Math.min(89, alt));
    if (!state.locked) toggleLock(true);
    setManualR(); toast('aimed: ' + cardinal(az) + ' ' + alt.toFixed(0) + '°'); return true;
  }
  function cardinal(az) { return ['N','NE','E','SE','S','SW','W','NW'][Math.round(az / 45) % 8]; }

  function drawZodiac(W, H) {
    // ecliptic as a smooth band of points (tradition label lives in the UI)
    ctx.strokeStyle = 'rgba(255,79,216,.5)'; ctx.setLineDash([4, 6]); ctx.lineWidth = 1.4; ctx.beginPath();
    var started = false, date = new Date(lastDate || Date.now());
    var SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
    for (var lon = 0; lon <= 360; lon += 4) {
      // ecliptic longitude -> RA/Dec (obliquity 23.436)
      var eps = 23.436 * D2R, l = lon * D2R;
      var ra = Math.atan2(Math.cos(eps) * Math.sin(l), Math.cos(l)) * R2D; if (ra < 0) ra += 360;
      var dec = Math.asin(Math.sin(eps) * Math.sin(l)) * R2D;
      var aa = altaz(date, ra, dec); if (aa.alt < -6) { started = false; continue; }
      var p = project(altazToENU(aa.alt, aa.az), W, H);
      if (!p) { started = false; continue; }
      if (!started) { ctx.moveTo(p.x, p.y); started = true; } else ctx.lineTo(p.x, p.y);
      if (lon % 30 === 0) { ctx.save(); ctx.setLineDash([]); ctx.fillStyle = 'rgba(255,110,199,.9)'; ctx.font = '10px Segoe UI'; ctx.fillText(SIGNS[(lon / 30) % 12], p.x + 4, p.y - 4); ctx.restore(); }
    }
    ctx.stroke(); ctx.setLineDash([]);
  }

  /* ---------- constellation line prep ---------- */
  function prepLines() {
    // constellations.json: [{id,name,lines:[ [ [ra,dec],... ], ... ]}] — flatten to polylines of [ra,dec]
    var polys = [];
    var arr = (state.cons && state.cons.constellations) || state.cons;
    if (Array.isArray(arr)) arr.forEach(function (con) { (con.lines || []).forEach(function (poly) { if (poly && poly.length > 1) polys.push(poly); }); });
    state.consPolys = polys;
  }

  /* ---------- interaction ---------- */
  cv.addEventListener('click', function (e) {
    if (panMoved) { panMoved = false; return; }   // a drag, not a tap
    if (miniAim(e.clientX, e.clientY)) return;     // tapped the mini-map -> aim there
    var best = null, bd = 1e9;
    for (var i = 0; i < hitList.length; i++) {
      var h = hitList[i], dx = e.clientX - h.x, dy = e.clientY - h.y, d = Math.sqrt(dx*dx+dy*dy);
      if (d < h.r && d < bd) { bd = d; best = h; }
    }
    if (state.calMode) { calibrateTo(e.clientX, e.clientY, best); return; }
    if (best) showInfo(best); else info.style.display = 'none';
  });
  function showInfo(h) {
    var o = h.o;
    document.getElementById('iName').textContent = o.name || o.desig || 'Object';
    document.getElementById('iSub').textContent = h.kind === 'planet' ? 'planet · right now' :
      h.kind === 'deep' ? (o.kind || 'deep-sky object') : ('star' + (o.desig ? ' · ' + o.desig : '') + (o.mag != null ? ' · mag ' + o.mag : ''));
    var body = '';
    if (h.kind === 'star') body = 'One of the bright stars Sarah can see by eye. Its colour here follows its real colour.';
    else if (h.kind === 'planet') body = o.moon ? 'The Moon, in its place in the sky right now.' : o.sun ? 'The Sun.' : 'A planet of our solar system, shown where it is tonight.';
    else body = 'A deep-sky object — a cluster, nebula or galaxy. Needs binoculars or a telescope.';
    document.getElementById('iBody').textContent = body;
    info.style.display = 'block';
  }
  document.getElementById('infoX').onclick = function () { info.style.display = 'none'; };

  // "Set North": tap the star you're actually pointing the reticle at; we rotate heading so it lines up
  function calibrateTo(cx, cy, best) {
    if (!best || best.kind !== 'star' && best.kind !== 'planet') { toast('Tap the Sun, Moon, a planet or a bright star you can see to set North'); return; }
    var date = new Date(lastDate || Date.now());
    var aa = altaz(date, best.o.ra, best.o.dec);
    var la = lookAltAz(); // current pointing az (true)
    // we want that star's true az to equal where the phone points -> adjust offset
    state.headingOffset += (la.az - aa.az);
    try { localStorage.setItem('sky.headingOffset', String(state.headingOffset)); } catch (e) {}
    state.calMode = false; retic.hidden = true; document.getElementById('tCal').setAttribute('aria-pressed', 'false');
    toast('North set on ' + (best.o.name || 'star'));
  }

  function toggleLock(on) {
    state.locked = (on === undefined) ? !state.locked : on;
    var b = document.getElementById('tLock'); if (b) b.setAttribute('aria-pressed', state.locked);
    if (state.locked) {   // freeze where we're currently aimed, then let touch pan/zoom
      var la = lookAltAz(); state.manAz = la.az; state.manAlt = la.alt; setManualR();
      toast('Locked — drag to look around, pinch to zoom. Phone can move.');
    } else {
      prevR = null;   // start fresh from the sensors, no slide from the frozen view
      toast('Live — the sky follows your phone again.');
    }
    if (b) b.textContent = state.locked ? '🔓 Unlock' : '🔒 Lock';
    document.body.classList.toggle('ar-locked', state.locked);
  }

  /* ---------- controls ---------- */
  function wire() {
    document.getElementById('zoom').addEventListener('input', function (e) { state.zoom = +e.target.value; });
    function tog(id, key) { var b = document.getElementById(id); b.addEventListener('click', function () { state.show[key] = !state.show[key]; b.setAttribute('aria-pressed', state.show[key]); }); }
    tog('tStars', 'stars'); tog('tLines', 'lines'); tog('tPlanets', 'planets'); tog('tDeep', 'deep'); tog('tZodiac', 'zodiac');
    document.getElementById('tFlip').addEventListener('click', function () { state.flip = !state.flip; this.setAttribute('aria-pressed', state.flip); startCam(); });
    document.getElementById('tCal').addEventListener('click', function () {
      state.calMode = !state.calMode; this.setAttribute('aria-pressed', state.calMode); retic.hidden = !state.calMode;
      if (state.calMode) toast('Aim the ring at a bright star you know, then tap it');
    });
    document.getElementById('tLock').addEventListener('click', function () { toggleLock(); });
    // Gestures with pointer events (work the same on Android WebView, iPhone and desktop):
    //  two fingers = pinch zoom (always); one finger drag = look around (when locked); double-tap = zoom in; wheel = zoom
    var ptrs = {}, pinch0 = null, zoom0 = 0, lastTap = 0, Z = Math.log(45);
    var setZoom = function (z) { state.zoom = Math.max(0, Math.min(100, z)); document.getElementById('zoom').value = state.zoom; try { localStorage.setItem('sky.arZoom', String(state.zoom)); } catch (e) {} };
    var dist = function () { var k = Object.keys(ptrs); if (k.length < 2) return 0; var a = ptrs[k[0]], b = ptrs[k[1]]; return Math.hypot(a.x - b.x, a.y - b.y); };
    cv.addEventListener('pointerdown', function (e) {
      ptrs[e.pointerId] = { x: e.clientX, y: e.clientY }; try { cv.setPointerCapture(e.pointerId); } catch (x) {}
      if (Object.keys(ptrs).length === 2) { pinch0 = dist(); zoom0 = state.zoom; panMoved = true; }
      else { panMoved = false; var now = Date.now(); if (now - lastTap < 300) { setZoom(state.zoom + 18); panMoved = true; } lastTap = now; }
    });
    cv.addEventListener('pointermove', function (e) {
      var p = ptrs[e.pointerId]; if (!p) return;
      var mx = e.clientX - p.x, my = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY;
      var n = Object.keys(ptrs).length;
      if (n >= 2 && pinch0) { var d = dist(); if (d > 0) setZoom(zoom0 + 100 * Math.log(d / pinch0) / Z); return; }
      if (n === 1 && state.locked) {
        if (Math.abs(mx) + Math.abs(my) > 1) panMoved = true;
        var sens = (fov() * R2D) / window.innerHeight;   // drag one screen-height = one field of view
        state.manAz = (state.manAz - mx * sens + 360) % 360;
        state.manAlt = Math.max(-80, Math.min(88, state.manAlt + my * sens));
        setManualR();
      }
    });
    var up = function (e) { delete ptrs[e.pointerId]; if (Object.keys(ptrs).length < 2) pinch0 = null; };
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up); cv.addEventListener('pointerleave', up);
    cv.addEventListener('wheel', function (e) { e.preventDefault(); setZoom(state.zoom - e.deltaY * 0.05); }, { passive: false });
    try { var z = parseFloat(localStorage.getItem('sky.arZoom')); if (isFinite(z)) setZoom(z); } catch (e) {}
    window.addEventListener('resize', sizeCanvas);
  }

  /* ---------- camera ---------- */
  function startCam() {
    if (cam.srcObject) { cam.srcObject.getTracks().forEach(function (t) { t.stop(); }); }
    navigator.mediaDevices.getUserMedia({ video: { facingMode: state.flip ? 'user' : { ideal: 'environment' } }, audio: false })
      .then(function (st) { cam.srcObject = st; cam.play(); })
      .catch(function () { showErr('No camera — showing the sky on black. Tap Start again to retry, or use the main map.'); cam.style.background = '#05010f'; });
  }

  /* ---------- sensors permission (iOS gated) ---------- */
  function askOrient() {
    // Listen first (Android and desktop send events without asking); then ask where the browser gates it (iOS).
    window.addEventListener('deviceorientationabsolute', onOrient, true);
    window.addEventListener('deviceorientation', onOrient, true);
    if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
      return DeviceOrientationEvent.requestPermission().then(function (r) {
        if (r !== 'granted' && !state.haveOrient) showErr('Motion access was declined — the sky can’t follow the phone. Tap Start to try again.');
      }).catch(function () {});
    }
    return Promise.resolve();
  }

  /* ---------- start ---------- */
  document.getElementById('start').addEventListener('click', function () {
    gate.style.display = 'none'; hud.hidden = false; readout.hidden = false;
    sizeCanvas();
    startCam();
    getLoc().then(function (ob) { state.observer = ob; });
    askOrient();
    requestAnimationFrame(draw);
    try { if (!localStorage.getItem('sky.arTip')) { localStorage.setItem('sky.arTip', '1');
      setTimeout(function () { showErr('Tip for accuracy: move the phone in a slow figure-8 once to wake the compass, then use Set North on the Moon, the Sun or a bright star you can see. It is remembered.'); setTimeout(function () { errBox.style.display = 'none'; }, 7000); }, 3200); } } catch (e) {}
    setTimeout(function () { if (!state.haveOrient) showErr('Your phone isn’t sending motion data. On iPhone use Safari; make sure Motion & Orientation Access is on in Settings → Safari.'); }, 2500);
  });

  loadAll().then(function () { prepLines(); });
  wire();
  if (!A) showErr('Sky engine failed to load.');
})();
