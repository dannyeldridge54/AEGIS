/* Dark-sky window for one night: sunset, astronomical dusk/dawn (Sun 18° down), sunrise,
   Moon phase name and the dark minutes with the Moon below the horizon.
   Pure function of (Astronomy, date, lat, lon) so it can be tested outside the browser. */
(function (root) {
  var PHASES = ["New moon", "Waxing crescent", "First quarter", "Waxing gibbous", "Full moon", "Waning gibbous", "Last quarter", "Waning crescent"];
  function darkWindow(A, date, lat, lon) {
    var obs = new A.Observer(lat, lon, 0);
    // Start from local solar noon. Before noon: if the Sun is still down we are in last night's
    // darkness, so start from yesterday's noon; if it is up, "tonight" is the coming night.
    var solarOffsetMs = lon / 15 * 3600000, localSolar = new Date(date.getTime() + solarOffsetMs);
    var noon = new Date(Date.UTC(localSolar.getUTCFullYear(), localSolar.getUTCMonth(), localSolar.getUTCDate(), 12) - solarOffsetMs);
    if (noon > date) {
      var tn = A.MakeTime(date), se = A.Equator("Sun", tn, obs, true, true);
      if (A.Horizon(tn, obs, se.ra, se.dec, "normal").altitude < 0) noon = new Date(noon.getTime() - 86400000);
    }
    var t0 = A.MakeTime(noon), ev = function (x) { return x ? x.date : null; };
    var sunset = ev(A.SearchRiseSet("Sun", obs, -1, t0, 1));
    var dusk = ev(A.SearchAltitude("Sun", obs, -1, t0, 1, -18));
    var dawn = dusk ? ev(A.SearchAltitude("Sun", obs, +1, A.MakeTime(dusk), 1, -18)) : null;
    var sunrise = ev(A.SearchRiseSet("Sun", obs, +1, A.MakeTime(sunset || noon), 1));
    var ph = ((A.MoonPhase(date) % 360) + 360) % 360;
    var out = { sunset: sunset, dusk: dusk, dawn: dawn, sunrise: sunrise,
      phase: PHASES[Math.floor((ph + 22.5) / 45) % 8], lit: A.Illumination("Moon", A.MakeTime(date)).phase_fraction,
      darkMin: 0, moonFreeMin: 0 };
    if (dusk && dawn) {
      var step = 5 * 60000;
      for (var ms = dusk.getTime(); ms < dawn.getTime(); ms += step) {
        var t = A.MakeTime(new Date(ms)), eq = A.Equator("Moon", t, obs, true, true);
        out.darkMin += 5;
        if (A.Horizon(t, obs, eq.ra, eq.dec, "normal").altitude < 0) out.moonFreeMin += 5;
      }
    }
    return out;
  }
  /* Best targets: objects ({id, ra°, dec°, mag}) that climb at least minAlt° during the fully dark
     window, brightest first, each with its highest altitude and when it happens. */
  function bestTargets(A, objects, lat, lon, win, minAlt, n) {
    if (!win || !win.dusk || !win.dawn) return [];
    minAlt = minAlt == null ? 30 : minAlt; n = n || 10;
    var obs = new A.Observer(lat, lon, 0), times = [];
    for (var ms = win.dusk.getTime(); ms <= win.dawn.getTime(); ms += 20 * 60000) times.push(A.MakeTime(new Date(ms)));
    var out = [];
    objects.forEach(function (o) {
      if (o.mag == null) return;
      var best = -90, at = null;
      times.forEach(function (t) { var h = A.Horizon(t, obs, o.ra / 15, o.dec, "normal").altitude; if (h > best) { best = h; at = t.date; } });
      if (best >= minAlt) out.push({ id: o.id, common: o.common || "", type: o.type || "", mag: o.mag, ra: o.ra, dec: o.dec, alt: best, at: at });
    });
    out.sort(function (a, b) { return a.mag - b.mag; });
    return out.slice(0, n);
  }
  root.SkyDark = { darkWindow: darkWindow, bestTargets: bestTargets, PHASES: PHASES };
  if (typeof module !== "undefined") module.exports = root.SkyDark;
})(typeof window !== "undefined" ? window : globalThis);
