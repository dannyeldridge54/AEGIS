/* Sarah's Sky — traditions panel. Every reading below is a cultural / spiritual tradition, not astronomy.
   The positions it starts from (Sun, Moon) are real and computed with astronomy-engine. Nothing leaves the device. */
(function () {
  var A = window.Astronomy;
  if (!A) return;
  var $ = function (id) { return document.getElementById(id); };
  var norm = function (x) { x %= 360; return x < 0 ? x + 360 : x; };
  var SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  var GLYPH = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];
  var RASHI = ['Mesha','Vrishabha','Mithuna','Karka','Simha','Kanya','Tula','Vrishchika','Dhanu','Makara','Kumbha','Meena'];
  var NAK = ['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni',
    'Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha','Uttara Ashadha','Shravana',
    'Dhanishta','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati'];
  var PHASES = ['New moon','Waxing crescent','First quarter','Waxing gibbous','Full moon','Waning gibbous','Last quarter','Waning crescent'];
  var MOONI = ['🌑','🌒','🌓','🌔','🌕','🌖','🌗','🌘'];
  var fmt = function (d) { return d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }); };

  function lahiri(d) {   // Lahiri ayanamsa: 23°51'11" at J2000, about 50.29" per year
    var yrs = (d.getTime() - Date.UTC(2000, 0, 1, 12)) / (365.25 * 864e5);
    return 23.8531 + yrs * 50.29 / 3600;
  }
  function positions(d) { return { sun: norm(A.SunPosition(d).elon), moon: norm(A.EclipticGeoMoon(d).lon), phase: norm(A.MoonPhase(d)) }; }

  var R = {
    zodiac: function (d) {
      var p = positions(d), s = Math.floor(p.sun / 30), m = Math.floor(p.moon / 30);
      return GLYPH[s] + ' Sun in <b>' + SIGNS[s] + '</b> (' + (p.sun % 30).toFixed(0) + '°) · ' + GLYPH[m] + ' Moon in <b>' + SIGNS[m] + '</b> (' + (p.moon % 30).toFixed(0) + '°)';
    },
    vedic: function (d) {
      var p = positions(d), ay = lahiri(d), ms = norm(p.moon - ay), ss = norm(p.sun - ay);
      var k = Math.floor(ms / (360 / 27)), pada = Math.floor((ms % (360 / 27)) / (360 / 108)) + 1;
      var tithi = Math.floor(norm(p.moon - p.sun) / 12) + 1;
      return 'Moon nakshatra: <b>' + NAK[k] + '</b>, pada ' + pada + ' · Moon rashi <b>' + RASHI[Math.floor(ms / 30)] + '</b> · Sun rashi <b>' + RASHI[Math.floor(ss / 30)] +
        '</b><br>Tithi ' + (tithi <= 15 ? 'Shukla ' + tithi : 'Krishna ' + (tithi - 15)) + ' · sidereal (Lahiri ' + ay.toFixed(2) + '°)';
    },
    chinese: function (d) {
      var ANIM = ['Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat','Monkey','Rooster','Dog','Pig'];
      var ELEM = ['Wood','Wood','Fire','Fire','Earth','Earth','Metal','Metal','Water','Water'];
      var STEM = ['Jia','Yi','Bing','Ding','Wu','Ji','Geng','Xin','Ren','Gui'], BRANCH = ['Zi','Chou','Yin','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai'];
      var lunar = '';
      try {
        var parts = new Intl.DateTimeFormat('en-u-ca-chinese', { year: 'numeric', month: 'numeric', day: 'numeric' }).formatToParts(d);
        var get = function (t) { var x = parts.find(function (q) { return q.type === t; }); return x ? x.value : ''; };
        lunar = 'Lunar month ' + get('month') + ', day ' + get('day');
      } catch (e) { lunar = ''; }
      // Year changes at Chinese New Year: use the cyclic year from Intl when available, else the Gregorian year
      var y = d.getFullYear(), cyc = null;
      try { var rel = new Intl.DateTimeFormat('en-u-ca-chinese', { year: 'numeric' }).formatToParts(d).find(function (q) { return q.type === 'relatedYear'; }); if (rel) y = parseInt(rel.value, 10); } catch (e) {}
      cyc = ((y - 4) % 60 + 60) % 60;
      return 'Year of the <b>' + ELEM[cyc % 10] + ' ' + ANIM[cyc % 12] + '</b> (' + STEM[cyc % 10] + '-' + BRANCH[cyc % 12] + ')' + (lunar ? ' · ' + lunar : '');
    },
    moon: function (d) {
      var p = positions(d), q = p.phase, i = [0,90,180,270].map(function (a, k) { return Math.abs(((q - a + 540) % 360) - 180) <= 12 ? 2 * k : -1; }).filter(function (k) { return k >= 0; })[0];
      if (i === undefined) i = 2 * Math.floor(q / 90) + 1;
      var ill = A.Illumination('Moon', d).phase_fraction;
      var nf = A.SearchMoonPhase(180, d, 40), nn = A.SearchMoonPhase(0, d, 40);
      return MOONI[i] + ' <b>' + PHASES[i] + '</b> · ' + Math.round(ill * 100) + '% lit · age ' + (p.phase / 360 * 29.53).toFixed(1) + ' days · Moon in ' + SIGNS[Math.floor(p.moon / 30)] +
        '<br>Next full moon ' + (nf ? fmt(nf.date) : '?') + ' · next new moon ' + (nn ? fmt(nn.date) : '?');
    }
  };

  // ---- Tarot: one card per day (same card all day), with an optional extra draw ----
  var MAJOR = [['The Fool','beginnings, trust, a leap','recklessness, hesitation'],['The Magician','skill, will, making it real','scattered energy, tricks'],
    ['The High Priestess','intuition, the inner voice','secrets, disconnection'],['The Empress','abundance, nurture, creativity','dependence, blocked growth'],
    ['The Emperor','structure, protection, authority','rigidity, control'],['The Hierophant','tradition, teaching, belonging','rebellion, dogma'],
    ['The Lovers','union, choice, values','imbalance, doubt'],['The Chariot','drive, focus, victory','scattered aim, being pulled apart'],
    ['Strength','courage, gentle power','self-doubt, raw force'],['The Hermit','solitude, searching, wisdom','isolation, withdrawal'],
    ['Wheel of Fortune','cycles, turning points','resistance to change'],['Justice','fairness, truth, cause and effect','imbalance, avoidance'],
    ['The Hanged Man','pause, surrender, new view','stalling, needless sacrifice'],['Death','endings that clear the way','clinging, fear of change'],
    ['Temperance','balance, patience, blending','excess, impatience'],['The Devil','attachment, temptation, shadow','release, breaking chains'],
    ['The Tower','sudden change, revelation','avoided upheaval'],['The Star','hope, healing, guidance','discouragement'],
    ['The Moon','dreams, uncertainty, the unseen','confusion lifting'],['The Sun','joy, clarity, success','temporary clouds'],
    ['Judgement','awakening, a calling','self-doubt, ignoring the call'],['The World','completion, wholeness','an unfinished loop']];
  var SUITS = [['Wands','fire: passion, action'],['Cups','water: feeling, relationships'],['Swords','air: thought, truth, conflict'],['Pentacles','earth: work, body, money']];
  var RANKS = [['Ace','a new start'],['Two','choice and balance'],['Three','growth and teamwork'],['Four','stability'],['Five','struggle and change'],
    ['Six','harmony restored'],['Seven','testing and patience'],['Eight','movement and effort'],['Nine','near completion'],['Ten','fullness, an ending'],
    ['Page','curiosity, a message'],['Knight','pursuit'],['Queen','mastery from within'],['King','mastery in the world']];
  function seed(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function card(n) {
    var c = n % 78, rev = ((n >>> 7) & 1) === 1, name, mean;
    if (c < 22) { name = MAJOR[c][0]; mean = rev ? MAJOR[c][2] : MAJOR[c][1]; }
    else { var k = c - 22, s = SUITS[Math.floor(k / 14)], r = RANKS[k % 14]; name = r[0] + ' of ' + s[0]; mean = r[1] + ' in ' + s[1] + (rev ? ' (reversed: blocked or turned inward)' : ''); }
    return '🃏 <b>' + name + (rev ? ' (reversed)' : '') + '</b><br>' + mean;
  }
  var extra = 0;
  R.tarot = function (d) {
    var key = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    return 'Card of the day: ' + card(seed('sarah-sky|' + key)) + (extra ? '<br>Extra draw: ' + card(seed('sarah-sky|' + key + '|' + extra + '|' + Date.now())) : '') +
      '<br><button type="button" id="tarotDraw" class="tbtn">Draw another</button>';
  };

  function wire(id, outId, fn) {
    var cb = $(id), out = $(outId); if (!cb || !out) return;
    var show = function () {
      out.style.display = cb.checked ? 'block' : 'none';
      if (!cb.checked) return;
      try { out.innerHTML = fn(new Date()) + '<br><span class="trad">tradition &mdash; not astronomy</span>'; } catch (e) { out.textContent = 'unavailable on this device'; }
      var b = $('tarotDraw'); if (b && id === 'ovTarot') b.onclick = function () { extra++; show(); };
    };
    cb.addEventListener('change', show);
    try { if (localStorage.getItem('sky.' + id) === '1') { cb.checked = true; show(); } } catch (e) {}
    cb.addEventListener('change', function () { try { localStorage.setItem('sky.' + id, cb.checked ? '1' : '0'); } catch (e) {} });
  }
  wire('ovZodiac', 'zodiacOut', R.zodiac);
  wire('ovVedic', 'vedicOut', R.vedic);
  wire('ovChinese', 'chineseOut', R.chinese);
  wire('ovMoon', 'moonOut', R.moon);
  wire('ovTarot', 'tarotOut', R.tarot);
  window.SarahTraditions = R;   // for tests
})();
