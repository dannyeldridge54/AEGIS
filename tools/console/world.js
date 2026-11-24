/* World calendars engine: today's date in ancient and living calendars, plus each calendar's own measurement of the
   year and the month, and its starting epoch, for the median analysis. Uses Celtic.* (celtic.js) for the Sun and Moon.
   Algorithms: Reingold & Dershowitz (Calendrical Calculations) style fixed-day arithmetic; checked against convertdate
   and lunardate (Python) for 2000-2030. Islamic is the tabular civil calendar (sighting can differ by 1-2 days). */
(function (G) {
  const DAY = 864e5, mod = (a, b) => ((a % b) + b) % b, fl = Math.floor;
  const jdOf = d => Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / DAY + 2440587.5;        // JD at 0h UTC of the local date
  // --- Julian calendar ---
  function julian(jd) { const c = fl(jd + 0.5) + 32082, d = fl((4 * c + 3) / 1461), e = c - fl(1461 * d / 4), m = fl((5 * e + 2) / 153);
    return { y: d - 4800 + fl(m / 10), m: m + 3 - 12 * fl(m / 10), d: e - fl((153 * m + 2) / 5) + 1 }; }
  // --- Hebrew (arithmetic, molad + postponements) ---
  const HEB_EPOCH = 347997.5;    // JD of 1 Tishrei AM 1 (R.D. -1373427)
  const hLeap = y => mod(7 * y + 1, 19) < 7;
  function hElapsed(y) { const m = fl((235 * y - 234) / 19), p = 12084 + 13753 * m, d = m * 29 + fl(p / 25920); return mod(3 * (d + 1), 7) < 3 ? d + 1 : d; }
  function hNewYearDelay(y) { const a = hElapsed(y - 1), b = hElapsed(y), c = hElapsed(y + 1); return c - b === 356 ? 2 : b - a === 382 ? 1 : 0; }
  const hNewYear = y => HEB_EPOCH + hElapsed(y) + hNewYearDelay(y);
  const hDaysInYear = y => hNewYear(y + 1) - hNewYear(y);
  function hMonthLen(y, m) { if ([2, 4, 6, 10, 13].includes(m)) return 29; if (m === 12 && !hLeap(y)) return 29; if (m === 8 && mod(hDaysInYear(y), 10) !== 5) return 29;
    if (m === 9 && mod(hDaysInYear(y), 10) === 3) return 29; return 30; }
  const HMN = ['', 'Nisan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul', 'Tishrei', 'Cheshvan', 'Kislev', 'Tevet', 'Shevat', 'Adar', 'Adar II'];
  function hebrew(jd) {
    let y = fl((jd - HEB_EPOCH) / 365.2468) + 1; while (hNewYear(y + 1) <= jd) y++; while (hNewYear(y) > jd) y--;
    const order = hLeap(y) ? [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6] : [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6];
    let t = hNewYear(y);
    for (const m of order) { const L = hMonthLen(y, m); if (jd < t + L) return { y, m: (m === 12 && hLeap(y)) ? 'Adar I' : HMN[m], d: fl(jd - t) + 1 }; t += L; }
  }
  // --- Islamic tabular (civil epoch 16 July 622 Julian) ---
  const IMN = ['Muharram', 'Safar', "Rabi' al-awwal", "Rabi' al-thani", 'Jumada al-awwal', 'Jumada al-thani', 'Rajab', "Sha'ban", 'Ramadan', 'Shawwal', "Dhu al-Qi'dah", 'Dhu al-Hijjah'];
  function islamic(jd) { const n = fl(jd - 1948439.5), y = fl((30 * n + 10646) / 10631), d0 = n - ((y - 1) * 354 + fl((3 + 11 * y) / 30));
    let m = 0, acc = 0; while (m < 11 && d0 >= acc + (m % 2 === 0 ? 30 : 29)) { acc += m % 2 === 0 ? 30 : 29; m++; } return { y, m: IMN[m], d: d0 - acc + 1 }; }
  // --- Persian (Solar Hijri, astronomical: Nowruz on the day of the March equinox before Tehran noon) ---
  const PMN = ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'];
  function nowruz(gy) { const C = G.Celtic, t = C.sunReachesExported(0, Date.UTC(gy, 2, 15)), tehran = t + 3.5 * 3600e3, d = new Date(tehran);
    let day = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()); if (d.getUTCHours() >= 12) day += DAY; return day / DAY + 2440587.5; }
  function persian(jd, gy) { let n0 = nowruz(gy); if (jd < n0) { gy--; n0 = nowruz(gy); } const k = fl(jd - n0), m = k < 186 ? fl(k / 31) : 6 + fl((k - 186) / 30);
    return { y: gy - 621, m: PMN[m], d: k < 186 ? k - 31 * m + 1 : k - 186 - 30 * (m - 6) + 1 }; }
  // --- Coptic and Ethiopian (Julian-type, 13 months) ---
  const CMN = ['Thout', 'Paopi', 'Hathor', 'Koiak', 'Tobi', 'Meshir', 'Paremhat', 'Parmouti', 'Pashons', 'Paoni', 'Epip', 'Mesori', 'Pi Kogi Enavot'];
  const EMN = ['Meskerem', 'Tikimt', 'Hidar', 'Tahsas', 'Tir', 'Yakatit', 'Magabit', 'Miyazya', 'Ginbot', 'Sene', 'Hamle', 'Nehase', 'Pagume'];
  function alex(jd, epoch, names) { const n = fl(jd - epoch), y = fl((4 * n + 1463) / 1461), d0 = n - (365 * (y - 1) + fl(y / 4)); return { y, m: names[fl(d0 / 30)], d: mod(d0, 30) + 1 }; }
  // --- Egyptian civil (Era of Nabonassar, 365-day wandering year) ---
  const EGM = ['Thoth', 'Phaophi', 'Athyr', 'Choiak', 'Tybi', 'Mechir', 'Phamenoth', 'Pharmuthi', 'Pachons', 'Payni', 'Epiphi', 'Mesore', 'Epagomenal days'];
  function egyptian(jd) { const n = fl(jd - 1448638 + 0.5), y = fl(n / 365) + 1, d0 = mod(n, 365); return { y, m: EGM[fl(d0 / 30)], d: mod(d0, 30) + 1 }; }
  // --- Maya (GMT correlation 584283) ---
  const TZ = ['Imix', "Ik'", "Ak'b'al", "K'an", 'Chikchan', 'Kimi', "Manik'", 'Lamat', 'Muluk', 'Ok', 'Chuwen', "Eb'", "B'en", 'Ix', 'Men', "K'ib'", "Kab'an", "Etz'nab'", 'Kawak', 'Ajaw'];
  const HB = ['Pop', "Wo'", 'Sip', "Sotz'", 'Sek', 'Xul', "Yaxk'in", 'Mol', "Ch'en", 'Yax', "Sak'", 'Keh', 'Mak', "K'ank'in", 'Muwan', 'Pax', "K'ayab", "Kumk'u", 'Wayeb'];
  function maya(jd) { const n = fl(jd + 0.5) - 584283, lc = [fl(n / 144000), fl(mod(n, 144000) / 7200), fl(mod(n, 7200) / 360), fl(mod(n, 360) / 20), mod(n, 20)];
    const tz = `${mod(n + 3, 13) + 1} ${TZ[mod(n + 19, 20)]}`, h = mod(n + 348, 365), hb = `${mod(h, 20)} ${HB[fl(h / 20)]}`; return { lc: lc.join('.'), tz, hb }; }
  // --- Chinese (astronomical: months start at new moon, China time; leap month has no principal term) ---
  const STEM = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'], BR = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai'];
  const ANI = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig'];
  const cnDay = t => fl((t + 8 * 3600e3) / DAY);   // day number in China time
  function nmOnOrAfter(day) { const C = G.Celtic; let t = C.newMoonExported(day * DAY); while (cnDay(t) < day) t = C.newMoonExported(t + 29.53 * DAY); while (cnDay(t - 29.53 * DAY) >= day) t = C.newMoonExported(t - 29.53 * DAY); return cnDay(t); }
  function solsticeDay(gy) { return cnDay(G.Celtic.sunReachesExported(270, Date.UTC(gy, 11, 1))); }
  function monthsBetween(s1, s2) { const out = []; let m = nmOnOrAfter(s1 + 1); while (m <= s2) { out.push(m); m = nmOnOrAfter(m + 1); } return out; }
  function chinese(date) {
    const d = cnDay(date.getTime() + 0), gy = date.getFullYear();
    for (const y of [gy, gy - 1]) {
      const s0 = solsticeDay(y - 1), s1 = solsticeDay(y), s2 = solsticeDay(y + 1);
      // month 11 contains the solstice; count months from month 11 of (y-1) to month 11 of y
      const m11a = nmOnOrAfter(s0 - 29) <= s0 ? nmOnOrAfter(s0 - 29) : nmOnOrAfter(s0 - 59);
      const list = [m11a].concat(monthsBetween(m11a, s1)).filter((v, i, a) => a.indexOf(v) === i);
      let leapIdx = -1;
      if (list.length === 14) {   // 13 months between the two month-11s: first month without a principal term is leap
        for (let i = 0; i + 1 < list.length; i++) { const a = list[i], b = list[i + 1]; let hasZ = false;
          for (let k = 0; k < 12; k++) { const z = cnDay(G.Celtic.sunReachesExported(270 + 30 * k, a * DAY - 40 * DAY)); if (z >= a && z < b) { hasZ = true; break; } }
          if (!hasZ) { leapIdx = i; break; } }
      }
      let num = 11, cny = null, labels = [];
      for (let i = 0; i < list.length; i++) { if (i === leapIdx) { labels.push([list[i], num, true]); continue; } if (i > 0) num = num % 12 + 1; labels.push([list[i], num, false]); }
      for (const l of labels) if (l[1] === 1 && !l[2]) { cny = l[0]; break; }
      if (cny === null || d < cny) continue;
      // months from CNY onward (extend into the next cycle if needed)
      let ms = labels.filter(l => l[0] >= cny);
      const next = monthsBetween(ms[ms.length - 1][0], s2 + 60).map(v => [v, null, false]);
      let n = ms[ms.length - 1][1]; for (const x of next) { n = n % 12 + 1; x[1] = n; } ms = ms.concat(next);
      let cur = ms[0]; for (const l of ms) if (l[0] <= d) cur = l;
      const cy = y, sb = mod(cy - 4, 60);
      return { y: cy, cycle: `${STEM[sb % 10]}-${BR[sb % 12]}`, animal: ANI[sb % 12], m: (cur[2] ? 'leap ' : '') + cur[1], d: d - cur[0] + 1 };
    }
  }
  // --- year counts ---
  function eras(date, jd) {
    const y = date.getFullYear(), mo = date.getMonth() + 1, after = (m, d) => (mo > m || (mo === m && date.getDate() >= d)) ? 1 : 0;
    const ol = y + 775 + after(7, 1) - 1, auc = y + 753, byz = y + 5508 + after(9, 1);
    return [
      ['Byzantine Anno Mundi (creation, 5509 BCE)', `${byz}`],
      ['Hindu Kali Yuga (3102 BCE)', `${y + 3101 + after(4, 14)}`],
      ['Korean Dangi (Dangun, 2333 BCE)', `${y + 2333}`],
      ['Greek Olympiad (776 BCE)', `Olympiad ${fl(ol / 4) + 1}, year ${mod(ol, 4) + 1}`],
      ['Roman Ab Urbe Condita (753 BCE)', `${auc}`],
      ['Japanese Kōki (660 BCE)', `${y + 660}`],
      ['Buddhist Era (543 BCE)', `${y + 543}`],
      ['Seleucid Era (Babylonian, 312/311 BCE)', `${y + 311 + after(4, 1)}`],
      ['Hindu Vikram Samvat (57 BCE)', `${y + 56 + after(4, 1)}`],
      ['Indian national Saka (78 CE)', `${y - 78 - (after(3, 22) ? 0 : 1)}`],
      ['Zoroastrian Yazdegerdi (632 CE, Fasli)', `${y - 631 - (after(3, 21) ? 0 : 1)}`]];
  }
  function today(date) {
    const jd = jdOf(date), j = julian(jd), h = hebrew(jd), i = islamic(jd), p = persian(jd, date.getFullYear()), c = alex(jd, 1825029.5, CMN), e = alex(jd, 1724220.5, EMN), eg = egyptian(jd), m = maya(jd);
    let cn = null; try { cn = chinese(date); } catch (err) {}
    const col = G.Celtic.coligny(date);
    return [
      ['Gregorian', date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }), 'solar (365.2425 d)'],
      ['Julian (Roman, 45 BCE)', `${j.d} ${['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][j.m - 1]} ${j.y}`, 'solar (365.25 d)'],
      ['Hebrew', `${h.d} ${h.m} ${h.y} AM`, 'lunisolar, 19-year cycle'],
      ['Islamic (Hijri, tabular)', `${i.d} ${i.m} ${i.y} AH`, 'lunar (354.37 d)'],
      ['Persian (Solar Hijri)', `${p.d} ${p.m} ${p.y} SH`, 'solar, equinox-based'],
      ['Chinese', cn ? `${cn.cycle} (${cn.animal}) year, month ${cn.m}, day ${cn.d}` : '—', 'lunisolar, astronomical'],
      ['Maya Long Count', `${m.lc}  ·  ${m.tz}  ·  ${m.hb}`, 'day count + 260 d + 365 d'],
      ['Egyptian civil (Nabonassar)', `${eg.d} ${eg.m}, year ${eg.y}`, 'wandering 365 d'],
      ['Coptic', `${c.d} ${c.m} ${c.y} AM`, 'solar (365.25 d)'],
      ['Ethiopian', `${e.d} ${e.m} ${e.y}`, 'solar (365.25 d)'],
      ['Celtic Coligny (reconstruction)', `${col.month} ${col.day}`, 'lunisolar, 30-year age']].concat(eras(date, jd).map(r => [r[0], r[1], 'year count']));
  }
  // Each calendar's own measurement of the year and the month (days), and its epoch (astronomical year; 1 BCE = 0)
  const YEARS = [['Egyptian civil', 365], ['Maya Haab', 365], ['Zoroastrian (ancient)', 365], ['Celtic Coligny (30-year age)', 10956 / 30],
    ['Julian / Coptic / Ethiopian', 365.25], ['Hebrew (molad, 19 years)', 6939.689622 / 19], ['Babylonian (Metonic, 235 months / 19 years)', 235 * 29.530594 / 19],
    ['Hindu Surya Siddhanta (sidereal)', 365.258756], ['Chinese Sifen (ancient, 484 BCE onward)', 365.25], ['Persian Jalali (Khayyam, 1079 CE)', 365.24219858],
    ['Gregorian (1582)', 365.2425], ['Maya (Dresden Venus/solar corrections, est.)', 365.2420]];
  const MONTHS = [['Babylonian (System B, adopted by Hipparchus)', 29.530594], ['Hebrew molad', 29.530594], ['Islamic tabular (10631 d / 360 months)', 10631 / 360],
    ['Hindu Surya Siddhanta', 29.530587946], ['Chinese Sifen (499/940)', 29 + 499 / 940], ['Maya Palenque formula (2392 d / 81 moons)', 2392 / 81],
    ['Celtic Coligny (10956 d / 371 months)', 10956 / 371], ['Greek Metonic (6940 d / 235 months)', 6940 / 235]];
  const EPOCHS = [['Byzantine creation', -5508], ['Hebrew creation', -3760], ['Maya creation (4 Ajaw 8 Kumk\'u)', -3113], ['Hindu Kali Yuga', -3101],
    ['Chinese Huangdi (traditional)', -2696], ['Korean Dangun', -2332], ['Greek first Olympiad', -775], ['Rome founded (AUC)', -752], ['Egypt Nabonassar', -746],
    ['Japan Jimmu (traditional)', -659], ['Buddha parinirvana (Theravada)', -542], ['Seleucid Era', -311], ['Vikram Samvat', -56], ['Ethiopian incarnation', 8],
    ['Saka Era', 78], ['Coptic Era of Martyrs', 284], ['Hijra', 622], ['Yazdegerdi', 632]];
  const CREATION = ['Byzantine creation', 'Hebrew creation', 'Maya creation (4 Ajaw 8 Kumk\'u)', 'Hindu Kali Yuga', 'Chinese Huangdi (traditional)', 'Korean Dangun'];
  const median = a => { const s = a.slice().sort((x, y) => x - y), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
  function medians() {
    const my = median(YEARS.map(r => r[1])), mm = median(MONTHS.map(r => r[1])), me = median(EPOCHS.map(r => r[1])), mc = median(EPOCHS.filter(r => CREATION.includes(r[0])).map(r => r[1]));
    const TROP = 365.24219, SID = 365.25636, SYN = 29.530588853, AQ = 2147.6;
    return { year: my, month: mm, epoch: me, creation: mc, trop: TROP, sid: SID, syn: SYN,
      yearErrMin: (my - TROP) * 1440, monthErrSec: (mm - SYN) * 86400,
      aquariusAgeInMedianYears: AQ * TROP / my, YEARS, MONTHS, EPOCHS, CREATION };
  }
  G.World = { today, medians, jdOf, hebrew, islamic, persian, maya, chinese, julian, egyptian };
})(typeof window !== 'undefined' ? window : globalThis);
