/* Celtic calendar + Aquarius + Weave cosmic clock engine (shared by the CubeMind console and Sarah's Sky).
   Coligny reconstruction used here (stated, not certain): months start on the 6th day of the moon (Pliny),
   the year opens with Samonios at the month nearest Samhain (1 Nov), the 13th month of a long year is the
   intercalary month (placed after Cutios). Moon: Astronomy Engine if loaded, else mean lunation (+-1 day). */
(function (G) {
  const SYN = 29.530588853, NM0 = Date.UTC(2000, 0, 6, 18, 14), DAY = 864e5, TROP = 365.24219;
  const MONTHS = [['Samonios', 'MAT'], ['Dumannios', 'ANM'], ['Riuros', 'MAT'], ['Anagantios', 'ANM'], ['Ogronnios', 'MAT'], ['Cutios', 'MAT'],
    ['Giamonios', 'ANM'], ['Simivisonnios', 'MAT'], ['Equos', 'ANM'], ['Elembivios', 'ANM'], ['Edrinios', 'MAT'], ['Cantlos', 'ANM']];
  const TREES = [['Birch', 12, 24, 1, 20], ['Rowan', 1, 21, 2, 17], ['Ash', 2, 18, 3, 17], ['Alder', 3, 18, 4, 14], ['Willow', 4, 15, 5, 12], ['Hawthorn', 5, 13, 6, 9],
    ['Oak', 6, 10, 7, 7], ['Holly', 7, 8, 8, 4], ['Hazel', 8, 5, 9, 1], ['Vine', 9, 2, 9, 29], ['Ivy', 9, 30, 10, 27], ['Reed', 10, 28, 11, 24], ['Elder', 11, 25, 12, 22]];
  function newMoonNear(t) {                       // nearest new moon to time t (ms)
    const A = G.Astronomy;
    if (A && A.SearchMoonPhase) {
      try { const r = A.SearchMoonPhase(0, new Date(t - 16 * DAY), 32); if (r) { const t1 = r.date.getTime(); if (Math.abs(t1 - t) <= 16 * DAY) return t1;
        const r2 = A.SearchMoonPhase(0, new Date(t1 + DAY), 32); return Math.abs(r2.date.getTime() - t) < Math.abs(t1 - t) ? r2.date.getTime() : t1; } } catch (e) {}
    }
    const k = Math.round((t - NM0) / DAY / SYN); return NM0 + k * SYN * DAY;
  }
  function monthStart(nm) { const d = new Date(nm + 5 * DAY); return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()); }   // 6th day of the moon
  function samonios(y) {                          // Samonios 1 of the Celtic year that starts near 1 Nov of year y
    const s = Date.UTC(y, 10, 1); let best = null;
    for (const off of [-SYN, 0, SYN]) { const m = monthStart(newMoonNear(s + off * DAY)); if (best === null || Math.abs(m - s) < Math.abs(best - s)) best = m; }
    return best;
  }
  function coligny(date) {
    const t = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
    let y = date.getFullYear(), s0 = samonios(y); if (t < s0) { y--; s0 = samonios(y); }
    const s1 = samonios(y + 1), starts = [s0];
    while (true) { const nx = monthStart(newMoonNear(starts[starts.length - 1] + (SYN + 1) * DAY)); if (nx >= s1 - 5 * DAY) break; starts.push(nx); }
    const long = starts.length === 13; let i = 0; while (i + 1 < starts.length && starts[i + 1] <= t) i++;
    let name, status;
    if (long && i === 6) { name = 'Ciallos (intercalary)'; status = 'MAT'; } else { const j = long && i > 6 ? i - 1 : i; [name, status] = MONTHS[j]; }
    const len = Math.round(((i + 1 < starts.length ? starts[i + 1] : s1) - starts[i]) / DAY), day = Math.round((t - starts[i]) / DAY) + 1;
    return { celticYearFrom: y, month: name, status, day, len, half: day <= 15 ? 'first (bright) half' : 'second half, after Atenoux', longYear: long, monthStart: new Date(starts[i]), samonios: new Date(s0), nextSamonios: new Date(s1) };
  }
  function treeSign(m, d) {                       // m 1-12
    if (m === 12 && d === 23) return 'The nameless day';
    for (const [n, m1, d1, m2, d2] of TREES) { const a = m1 * 100 + d1, b = m2 * 100 + d2, x = m * 100 + d; if (a <= b ? (x >= a && x <= b) : (x >= a || x <= b)) return n; }
    return '';
  }
  function sunLon(t) {                            // low-precision apparent solar longitude (deg), Meeus ch. 25, ~0.01 deg
    const A = G.Astronomy; if (A && A.SunPosition) { try { return A.SunPosition(new Date(t)).elon; } catch (e) {} }
    const T = (t / DAY + 2440587.5 - 2451545) / 36525, L0 = 280.46646 + 36000.76983 * T, M = (357.52911 + 35999.05029 * T) * Math.PI / 180;
    const C = (1.914602 - 0.004817 * T) * Math.sin(M) + 0.019993 * Math.sin(2 * M) + 0.000289 * Math.sin(3 * M); return ((L0 + C) % 360 + 360) % 360;
  }
  function sunReaches(lon, from) {                // first time after 'from' the Sun reaches ecliptic longitude lon (day steps, then bisection)
    const diff = t => ((sunLon(t) - lon + 540) % 360) - 180;
    let t0 = from, d0 = diff(t0);
    for (let k = 1; k <= 370; k++) { const t1 = from + k * DAY, d1 = diff(t1);
      if (d0 < 0 && d1 >= 0) { let a = t0, b = t1; for (let j = 0; j < 30; j++) { const m = (a + b) / 2; diff(m) < 0 ? a = m : b = m; } return b; }
      t0 = t1; d0 = d1; }
    return from;
  }
  function festivals(now) {
    const fx = [['Samhain', 10, 1, 225], ['Imbolc', 1, 1, 315], ['Beltane', 4, 1, 45], ['Lughnasadh', 7, 1, 135]], out = [];
    for (const [n, mo, d, lon] of fx) {
      let t = Date.UTC(now.getFullYear(), mo, d); if (t < now.getTime() - DAY) t = Date.UTC(now.getFullYear() + 1, mo, d);
      const sky = sunReaches(lon, now.getTime() - 2 * DAY);
      out.push({ name: n, traditional: new Date(t), astronomical: new Date(sky), days: Math.ceil((t - now.getTime()) / DAY) });
    }
    return out.sort((a, b) => a.days - b.days);
  }
  // Aquarius (IAU 2006 general precession) and its Celtic reckoning from Samonios 2026
  const AQ = [['Fagan-Bradley (Western sidereal)', 2376.5], ['Lahiri (Vedic)', 2439.6], ['IAU star borders (Meeus)', 2597]];
  function aquarius() {
    return AQ.map(([n, yr]) => { const cy = Math.floor(yr - 2026.87), age = Math.floor(cy / 30) + 1, inAge = cy % 30, cyc = Math.floor(inAge / 5) + 1, yc = inAge % 5 + 1;
      return { boundary: n, year: yr, celticYears: cy, age, cycle: cyc, yearInCycle: yc, lunations: Math.round((yr - 2026.87) * TROP / SYN) }; });
  }
  // Weave cosmic clock (calibrated engine, D-notes): t0 13.715 Gyr (H0 67.43), reheating T_R 8.94e8 GeV, r 4.8e-4, N* 68
  function cosmicClock() {
    const MP = 2.435e18, r = 4.81e-4, V14 = 1.04e16 * Math.pow(r / 0.1, 0.25), H = V14 * V14 / (Math.sqrt(3) * MP), hbar = 6.582e-25;
    const tInfl = 1 / H * hbar, tEnd = 68 * tInfl, TR = 8.94e8, tR = 2.42 / Math.sqrt(228.75) * Math.pow(TR * 1e3, -2);
    return [
      ['Inflation: our largest scales leave the horizon (N* = 68 e-folds before the end)', tInfl, 's', 'ESTIMATE from the Weave adopted r'],
      ['End of inflation', tEnd, 's', 'ESTIMATE (N*/H)'],
      ['Reheating, hot Big Bang begins (T_R = 8.9e8 GeV)', tR, 's', 'Weave adopted point'],
      ['First nuclei (Big Bang nucleosynthesis)', 180, 's', 'standard; D/H and Y_p scored IN in the Weave map'],
      ['Light released (cosmic microwave background)', 380e3 * 3.156e7, 's', 'standard'],
      ['Sun and Earth form', (13.715 - 4.567) * 3.156e16, 's', 'Weave age minus solar-system age'],
      ['Today', 13.715 * 3.156e16, 's', 'Weave calibrated age 13.715 Gyr'],
      ['Age of Aquarius begins (2377 / 2440 / 2597 CE)', 13.715 * 3.156e16 + 351 * 3.156e7, 's', '+351 to +571 years; standard astronomy']];
  }
  G.Celtic = { coligny, treeSign, festivals, aquarius, cosmicClock, samonios };
})(typeof window !== 'undefined' ? window : globalThis);
