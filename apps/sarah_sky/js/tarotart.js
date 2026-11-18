/* Sarah's Sky — original tarot card art: "supersymmetry meets the esoteric".
   Every card is drawn from geometry, not copied from any deck. Each design is a mirror pair: the solid figure
   (the particle) and its dashed reflection (the superpartner), on a hexagonal lattice, with sacred-geometry
   rings counting the card's number. Majors get a unique sigil; minors carry their element. */
(function () {
  var PAL = ['#4cc3ff', '#7a5cff', '#d43cff', '#ff6ec7', '#6fb8ff', '#a07bff'];
  var ROMAN = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI'];
  var SUIT = { Wands: { el: 'fire', col: '#ff6ec7', tri: 'up' }, Cups: { el: 'water', col: '#4cc3ff', tri: 'down' },
               Swords: { el: 'air', col: '#6fb8ff', tri: 'upbar' }, Pentacles: { el: 'earth', col: '#a07bff', tri: 'downbar' } };
  var W = 120, H = 200, CX = 60, CY = 92;
  function f(n) { return Math.round(n * 100) / 100; }
  function poly(n, r, rot, cx, cy) { var p = []; for (var i = 0; i < n; i++) { var a = rot + i * 2 * Math.PI / n; p.push(f(cx + r * Math.sin(a)) + ',' + f(cy - r * Math.cos(a))); } return p.join(' '); }
  function star(n, r1, r2, rot, cx, cy) { var p = []; for (var i = 0; i < 2 * n; i++) { var r = i % 2 ? r2 : r1, a = rot + i * Math.PI / n; p.push(f(cx + r * Math.sin(a)) + ',' + f(cy - r * Math.cos(a))); } return p.join(' '); }
  function lattice(id) {   // faint hexagonal lattice — the same pattern as the A2 / Eisenstein vacuum
    var o = '<g opacity=".16" stroke="#7a5cff" stroke-width=".4" fill="none">';
    for (var y = 0; y < 13; y++) for (var x = 0; x < 9; x++) { var cx = x * 15 + (y % 2) * 7.5, cy = y * 13 + 6; o += '<polygon points="' + poly(6, 7.5, 0, cx, cy) + '"/>'; }
    return o + '</g>';
  }
  function element(kind, cx, cy, r, col) {
    var t = kind === 'up' || kind === 'upbar' ? poly(3, r, 0, cx, cy) : poly(3, r, Math.PI, cx, cy), o = '<polygon points="' + t + '" fill="none" stroke="' + col + '" stroke-width="1.1"/>';
    if (kind === 'upbar' || kind === 'downbar') o += '<line x1="' + f(cx - r * .55) + '" y1="' + f(cy + (kind === 'upbar' ? r * .1 : -r * .1)) + '" x2="' + f(cx + r * .55) + '" y2="' + f(cy + (kind === 'upbar' ? r * .1 : -r * .1)) + '" stroke="' + col + '" stroke-width="1.1"/>';
    return o;
  }
  function mirror(inner) {   // solid particle on the left half, dashed superpartner reflected on the right
    return '<g>' + inner + '</g><g transform="translate(' + (2 * CX) + ',0) scale(-1,1)" stroke-dasharray="2 2" opacity=".7">' + inner + '</g>';
  }
  function rings(n, col) { var o = ''; for (var i = 0; i < n; i++) o += '<circle cx="' + CX + '" cy="' + CY + '" r="' + (14 + i * 4.2) + '" fill="none" stroke="' + col + '" stroke-width=".5" opacity="' + (0.25 + 0.5 * (i + 1) / n) + '"/>'; return o; }

  // a unique sigil for each Major Arcana card, built from its number
  function majorSigil(k) {
    var c1 = PAL[k % 6], c2 = PAL[(k + 2) % 6], o = '';
    var sides = [3, 4, 5, 6, 7, 8, 12][k % 7], pts = 5 + (k % 4);
    o += '<polygon points="' + star(pts, 30, 13, k * 0.17, CX, CY) + '" fill="none" stroke="' + c1 + '" stroke-width="1.2"/>';
    o += '<polygon points="' + poly(sides, 22, k * 0.31, CX, CY) + '" fill="none" stroke="' + c2 + '" stroke-width=".9"/>';
    // half-figure: a "Feynman" vertex — two incoming lines meet, one wavy boson leaves (drawn on the left, mirrored)
    var h = '<path d="M ' + (CX - 34) + ' ' + (CY - 30) + ' L ' + (CX - 8) + ' ' + CY + ' L ' + (CX - 34) + ' ' + (CY + 30) + '" fill="none" stroke="' + c1 + '" stroke-width=".9"/>' +
      '<circle cx="' + (CX - 8) + '" cy="' + CY + '" r="2.2" fill="' + c2 + '"/>';
    o += mirror(h);
    // the card's own mark: special glyphs for a few archetypes
    var marks = { 0: '∅', 1: '∞', 2: '☾', 3: '♀', 4: '♂', 9: '✷', 10: '⟳', 11: '⚖', 13: '☥', 17: '✦', 18: '☽', 19: '☉', 21: '◎' };
    o += '<text x="' + CX + '" y="' + (CY + 5) + '" text-anchor="middle" font-size="15" fill="#fff4c2" font-family="Segoe UI Symbol,Noto Sans Symbols 2,serif">' + (marks[k] || '✧') + '</text>';
    return o + rings(Math.min(k % 8 + 1, 7), c1);
  }
  // pips arranged with mirror symmetry for the minors
  function pipLayout(n) {
    var L = { 1: [[0, 0]], 2: [[0, -24], [0, 24]], 3: [[0, -28], [0, 0], [0, 28]], 4: [[-16, -20], [16, -20], [-16, 20], [16, 20]],
      5: [[-16, -22], [16, -22], [0, 0], [-16, 22], [16, 22]], 6: [[-16, -28], [16, -28], [-16, 0], [16, 0], [-16, 28], [16, 28]],
      7: [[-16, -30], [16, -30], [0, -15], [-16, 0], [16, 0], [-16, 30], [16, 30]], 8: [[-16, -33], [16, -33], [-16, -11], [16, -11], [-16, 11], [16, 11], [-16, 33], [16, 33]],
      9: [[-16, -33], [16, -33], [-16, -11], [16, -11], [0, 0], [-16, 11], [16, 11], [-16, 33], [16, 33]],
      10: [[-16, -36], [16, -36], [0, -24], [-16, -12], [16, -12], [-16, 12], [16, 12], [0, 24], [-16, 36], [16, 36]] };
    return L[n] || [];
  }
  function minorArt(suit, rank) {
    var S = SUIT[suit], o = '';
    if (rank < 10) {
      var n = rank + 1, r = n === 1 ? 24 : (n <= 4 ? 11 : 8.5);
      pipLayout(n).forEach(function (p, i) {
        var dashed = p[0] > 0 ? ' stroke-dasharray="2 1.6"' : '';   // right-hand pips are the superpartners
        o += '<g' + dashed + '>' + element(S.tri, CX + p[0], CY + p[1], r, S.col) + '</g>';
      });
      if (n === 1) o += '<polygon points="' + star(6, 34, 20, 0, CX, CY) + '" fill="none" stroke="' + S.col + '" stroke-width=".6" opacity=".6"/>' + rings(3, S.col);
    } else {   // courts: Page, Knight, Queen, King — a crowned sigil whose number of rays grows with rank
      var lvl = rank - 9, rays = 4 + 2 * lvl;
      o += element(S.tri, CX, CY + 6, 26, S.col);
      o += '<polygon points="' + star(rays, 38, 30, 0, CX, CY + 6) + '" fill="none" stroke="' + S.col + '" stroke-width=".6" opacity=".7"/>';
      var crown = '<path d="M ' + (CX - 18) + ' ' + (CY - 30) + ' L ' + (CX - 12) + ' ' + (CY - 42) + ' L ' + (CX - 6) + ' ' + (CY - 32) + ' L ' + CX + ' ' + (CY - 46) + '" fill="none" stroke="#fff4c2" stroke-width="1"/>';
      o += mirror(crown) + rings(lvl + 1, S.col);
      o += '<text x="' + CX + '" y="' + (CY + 12) + '" text-anchor="middle" font-size="12" fill="#fff4c2" font-family="Segoe UI,system-ui,sans-serif">' + ['P', 'Kn', 'Q', 'K'][lvl - 1] + '</text>';
    }
    return o;
  }

  /* ---------- five deck styles, one palette ---------- */
  var STYLES = ['mirror', 'orbital', 'feynman', 'sacred', 'rosette', 'constellation', 'galaxy', 'neon', 'circuit', 'grid'];
  var STYLE_NAMES = { mirror: 'Mirror Lattice', orbital: 'Orbitals', feynman: 'Feynman Paths', sacred: 'Sacred Geometry', rosette: 'Symmetry Rosette', constellation: 'Constellations', galaxy: 'Spiral Galaxy', neon: 'Neon Sign', circuit: 'Cyber Circuit', grid: 'Neon Horizon' };
  function seedRand(k) { var x = Math.sin(k * 9301 + 49297) * 233280; return x - Math.floor(x); }
  function num(index) { return index < 22 ? index : ((index - 22) % 14) + 1; }
  function colOf(index) { if (index < 22) return PAL[index % 6]; return SUIT[['Wands','Cups','Swords','Pentacles'][Math.floor((index - 22) / 14)]].col; }
  function orbitalArt(index) {   // electron shells: n shells, tilted ellipses as orbitals, spin arrows paired up/down (the superpartner flips spin)
    var n = num(index), c = colOf(index), c2 = PAL[(index + 3) % 6], o = '', lobes = Math.max(2, Math.min(8, (n % 7) + 2));
    for (var i = 0; i < lobes; i++) o += '<ellipse cx="' + CX + '" cy="' + CY + '" rx="38" ry="11" transform="rotate(' + (i * 180 / lobes) + ' ' + CX + ' ' + CY + ')" fill="none" stroke="' + (i % 2 ? c2 : c) + '" stroke-width=".8" opacity=".85"/>';
    for (var j = 0; j < Math.min(n, 10); j++) { var a = j * 2 * Math.PI / Math.min(n, 10), x = CX + 30 * Math.cos(a), y = CY + 30 * Math.sin(a), up = j % 2 === 0;
      o += '<path d="M ' + f(x) + ' ' + f(y + (up ? 4 : -4)) + ' L ' + f(x) + ' ' + f(y + (up ? -4 : 4)) + ' M ' + f(x - 2) + ' ' + f(y + (up ? -1.5 : 1.5)) + ' L ' + f(x) + ' ' + f(y + (up ? -4 : 4)) + ' L ' + f(x + 2) + ' ' + f(y + (up ? -1.5 : 1.5)) + '" stroke="#fff4c2" stroke-width=".8" fill="none"/>'; }
    return o + '<circle cx="' + CX + '" cy="' + CY + '" r="5" fill="' + c + '"/><circle cx="' + CX + '" cy="' + CY + '" r="9" fill="none" stroke="' + c2 + '" stroke-dasharray="1.5 1.5"/>';
  }
  function wave(x1, y1, x2, y2, col, k) {   // a boson (photon) line as a sine wiggle
    var dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, d = 'M ' + f(x1) + ' ' + f(y1), steps = 24;
    for (var i = 1; i <= steps; i++) { var t = i / steps, off = 2.6 * Math.sin(t * Math.PI * (6 + k % 4)); d += ' L ' + f(x1 + dx * t - uy * off) + ' ' + f(y1 + dy * t + ux * off); }
    return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width=".9"/>';
  }
  function feynmanArt(index) {   // a vertex diagram per card: fermion lines in, boson out, and the mirrored sparticle diagram dashed
    var n = num(index), c = colOf(index), c2 = PAL[(index + 2) % 6], o = '', legs = Math.min(2 + (n % 4), 5);
    var vx = CX, vy = CY - 14, wy = CY + 22;
    for (var i = 0; i < legs; i++) { var a = Math.PI + (i + 1) * Math.PI / (legs + 1);
      var x = vx + 40 * Math.cos(a), y = vy + 40 * Math.sin(a);
      o += '<line x1="' + f(x) + '" y1="' + f(y) + '" x2="' + vx + '" y2="' + vy + '" stroke="' + c + '" stroke-width="1"/>';
      o += '<line x1="' + f(2 * CX - x) + '" y1="' + f(2 * wy - y) + '" x2="' + vx + '" y2="' + wy + '" stroke="' + c2 + '" stroke-width="1" stroke-dasharray="2 2"/>'; }
    o += wave(vx, vy, vx, wy, '#fff4c2', index);
    o += '<circle cx="' + vx + '" cy="' + vy + '" r="2.6" fill="' + c + '"/><circle cx="' + vx + '" cy="' + wy + '" r="2.6" fill="' + c2 + '"/>';
    return o + '<text x="' + CX + '" y="' + (CY + 52) + '" text-anchor="middle" font-size="7" fill="#a296d8" font-family="Segoe UI,system-ui,sans-serif">' + n + ' · ' + (n % 2 ? 'fermion' : 'boson') + '</text>';
  }
  function sacredArt(index) {   // flower of life petals = card number, inside Metatron-style circles
    var n = Math.max(1, Math.min(num(index), 12)), c = colOf(index), c2 = PAL[(index + 1) % 6], o = '', r = 13;
    o += '<circle cx="' + CX + '" cy="' + CY + '" r="40" fill="none" stroke="' + c2 + '" stroke-width=".6"/>';
    o += '<circle cx="' + CX + '" cy="' + CY + '" r="' + r + '" fill="none" stroke="' + c + '" stroke-width=".9"/>';
    for (var i = 0; i < n; i++) { var a = i * 2 * Math.PI / n; o += '<circle cx="' + f(CX + r * Math.cos(a)) + '" cy="' + f(CY + r * Math.sin(a)) + '" r="' + r + '" fill="none" stroke="' + (i % 2 ? c2 : c) + '" stroke-width=".8"/>'; }
    var outer = Math.max(3, n); for (var j = 0; j < outer; j++) { var b = j * 2 * Math.PI / outer, b2 = (j + 1) * 2 * Math.PI / outer;
      o += '<line x1="' + f(CX + 34 * Math.cos(b)) + '" y1="' + f(CY + 34 * Math.sin(b)) + '" x2="' + f(CX + 34 * Math.cos(b2)) + '" y2="' + f(CY + 34 * Math.sin(b2)) + '" stroke="' + c2 + '" stroke-width=".5" opacity=".8"/>'; }
    return o + '<circle cx="' + CX + '" cy="' + CY + '" r="2" fill="#fff4c2"/>';
  }
  function rosetteArt(index) {   // an n-fold rotational rosette: the same petal repeated by the card's symmetry group
    var n = Math.max(3, Math.min(num(index) + 2, 12)), c = colOf(index), c2 = PAL[(index + 4) % 6], o = '';
    var petal = '<path d="M ' + CX + ' ' + CY + ' C ' + (CX - 9) + ' ' + (CY - 16) + ' ' + (CX - 6) + ' ' + (CY - 34) + ' ' + CX + ' ' + (CY - 40) + ' C ' + (CX + 6) + ' ' + (CY - 34) + ' ' + (CX + 9) + ' ' + (CY - 16) + ' ' + CX + ' ' + CY + '" fill="none" stroke="';
    for (var i = 0; i < n; i++) { o += '<g transform="rotate(' + f(i * 360 / n) + ' ' + CX + ' ' + CY + ')">' + petal + (i % 2 ? c2 : c) + '" stroke-width=".9"/>' + '<circle cx="' + CX + '" cy="' + (CY - 44) + '" r="1.6" fill="' + (i % 2 ? c2 : c) + '"/></g>'; }
    return o + '<polygon points="' + poly(n, 12, 0, CX, CY) + '" fill="none" stroke="#fff4c2" stroke-width=".7"/><circle cx="' + CX + '" cy="' + CY + '" r="3" fill="' + c + '"/>';
  }

  /* ---- five more decks: stars, neon, cyberpunk ---- */
  var UID = 0;
  function rnd(seed) { var a = seed * 7919 + 13; return function () { a = (a * 16807) % 2147483647; return a / 2147483647; }; }
  function sparkle(x, y, r, col) { return '<path d="M' + f(x) + ' ' + f(y - r) + ' Q' + f(x + r * .18) + ' ' + f(y - r * .18) + ' ' + f(x + r) + ' ' + f(y) + ' Q' + f(x + r * .18) + ' ' + f(y + r * .18) + ' ' + f(x) + ' ' + f(y + r) + ' Q' + f(x - r * .18) + ' ' + f(y + r * .18) + ' ' + f(x - r) + ' ' + f(y) + ' Q' + f(x - r * .18) + ' ' + f(y - r * .18) + ' ' + f(x) + ' ' + f(y - r) + 'Z" fill="' + col + '"/>'; }
  function starfield(seed, n) { var R = rnd(seed + 101), o = '<g>'; for (var i = 0; i < n; i++) { var r = R(); o += '<circle cx="' + f(8 + R() * 104) + '" cy="' + f(8 + R() * 170) + '" r="' + f(.25 + r * r * .9) + '" fill="' + (r > .85 ? '#ffd6f2' : '#cfe6ff') + '" opacity="' + f(.3 + R() * .6) + '"/>'; } return o + '</g>'; }
  function glow(id, sd) { return '<filter id="' + id + '" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="' + sd + '" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'; }
  function constellationArt(index, gid) {   // the card's number as a constellation: n stars joined like a star chart
    var n = Math.max(3, Math.min(num(index) + 2, 12)), c = colOf(index), R = rnd(index + 7), pts = [], o = '';
    for (var i = 0; i < n; i++) { var a = i / n * 2 * Math.PI + (R() - .5) * .9, rr = 14 + R() * 30; pts.push([CX + rr * Math.sin(a), CY - rr * Math.cos(a) * 1.25]); }
    o += '<polyline points="' + pts.map(function (p) { return f(p[0]) + ',' + f(p[1]); }).join(' ') + ' ' + f(pts[0][0]) + ',' + f(pts[0][1]) + '" fill="none" stroke="' + c + '" stroke-width=".7" opacity=".75"/>';
    if (n > 5) o += '<line x1="' + f(pts[0][0]) + '" y1="' + f(pts[0][1]) + '" x2="' + f(pts[Math.floor(n / 2)][0]) + '" y2="' + f(pts[Math.floor(n / 2)][1]) + '" stroke="' + c + '" stroke-width=".5" stroke-dasharray="1.5 2" opacity=".6"/>';
    pts.forEach(function (p, i) { o += sparkle(p[0], p[1], i === 0 ? 5 : 2.4 + R() * 1.6, i === 0 ? '#fff4c2' : '#f3eeff'); });
    return '<g filter="url(#' + gid + ')">' + o + '</g>';
  }
  function galaxyArt(index, gid) {   // a spiral galaxy with one arm per suit-number, glowing core
    var arms = Math.max(2, Math.min((num(index) % 6) + 2, 7)), c = colOf(index), c2 = PAL[(index + 2) % 6], R = rnd(index + 3), o = '';
    for (var a = 0; a < arms; a++) for (var t = 0; t < 34; t++) {
      var th = a * 2 * Math.PI / arms + t * .17, r = 3 + t * 1.25, j = (R() - .5) * 3;
      o += '<circle cx="' + f(CX + (r + j) * Math.cos(th)) + '" cy="' + f(CY + (r + j) * Math.sin(th) * .8) + '" r="' + f(.4 + (1 - t / 34) * 1.1) + '" fill="' + (t % 3 ? c : c2) + '" opacity="' + f(.35 + (1 - t / 34) * .6) + '"/>';
    }
    return '<g filter="url(#' + gid + ')">' + o + '<ellipse cx="' + CX + '" cy="' + CY + '" rx="7" ry="5.5" fill="#fff4c2" opacity=".85"/></g>';
  }
  function neonArt(index, gid) {   // glowing neon tubes: an outer frame tube and the card's sigil bent in glass
    var n = num(index), c = colOf(index), c2 = PAL[(index + 3) % 6], sides = [3, 4, 5, 6, 8][index % 5], o = '';
    o += '<rect x="20" y="40" width="80" height="104" rx="12" fill="none" stroke="' + c2 + '" stroke-width="1.6"/>';
    o += '<polygon points="' + star(Math.max(4, Math.min(n + 3, 12)), 30, 14, 0, CX, CY) + '" fill="none" stroke="' + c + '" stroke-width="1.8" stroke-linejoin="round"/>';
    o += '<polygon points="' + poly(sides, 11, 0, CX, CY) + '" fill="none" stroke="#fff4c2" stroke-width="1.4"/>';
    o += '<text x="' + CX + '" y="' + (CY + 4) + '" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" font-family="Segoe UI,system-ui,sans-serif">' + n + '</text>';
    return '<g filter="url(#' + gid + ')" stroke-linecap="round">' + o + '</g>';
  }
  function circuitArt(index, gid) {   // cyberpunk circuit board: traces at 45° into a central chip that shows the card's number in binary
    var n = num(index), c = colOf(index), c2 = PAL[(index + 1) % 6], R = rnd(index + 11), o = '';
    for (var i = 0; i < 14; i++) {
      var side = i % 4, x = side === 0 ? 14 : side === 1 ? 106 : 18 + R() * 84, y = side === 2 ? 28 : side === 3 ? 160 : 30 + R() * 124;
      var ex = CX + (x < CX ? -16 : 16) * (side < 2 ? 1 : R() * .9), ey = CY + (y < CY ? -16 : 16) * (side > 1 ? 1 : R() * .9);
      var mx = side < 2 ? ex + (x < ex ? -1 : 1) * Math.abs(ey - y) : x, my = side < 2 ? y : ey + (y < ey ? -1 : 1) * Math.abs(ex - x);
      o += '<polyline points="' + f(x) + ',' + f(y) + ' ' + f(mx) + ',' + f(my) + ' ' + f(ex) + ',' + f(ey) + '" fill="none" stroke="' + (i % 3 ? c : c2) + '" stroke-width=".8" opacity=".85"/><circle cx="' + f(x) + '" cy="' + f(y) + '" r="1.8" fill="none" stroke="' + (i % 3 ? c : c2) + '" stroke-width=".8"/>';
    }
    var bits = n.toString(2), chip = '<rect x="' + (CX - 17) + '" y="' + (CY - 17) + '" width="34" height="34" rx="3" fill="#0b0620" stroke="' + c + '" stroke-width="1.3"/>';
    for (var k = 0; k < 5; k++) chip += '<line x1="' + (CX - 13 + k * 6.5) + '" y1="' + (CY - 20) + '" x2="' + (CX - 13 + k * 6.5) + '" y2="' + (CY - 17) + '" stroke="' + c + '"/><line x1="' + (CX - 13 + k * 6.5) + '" y1="' + (CY + 17) + '" x2="' + (CX - 13 + k * 6.5) + '" y2="' + (CY + 20) + '" stroke="' + c + '"/>';
    chip += '<text x="' + CX + '" y="' + (CY + 3) + '" text-anchor="middle" font-size="' + (bits.length > 4 ? 6.5 : 8) + '" fill="#fff4c2" font-family="Consolas,monospace">' + bits + '</text>';
    return o + '<g filter="url(#' + gid + ')">' + chip + '</g>';
  }
  function gridArt(index, gid) {   // synthwave horizon: striped sun (stripes = card number), skyline, perspective grid
    var n = Math.max(1, Math.min(num(index), 12)), c = colOf(index), c2 = PAL[(index + 2) % 6], hz = 112, R = rnd(index + 5), o = '';
    o += '<defs><linearGradient id="sun' + gid + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4c2"/><stop offset=".5" stop-color="#ff6ec7"/><stop offset="1" stop-color="#d43cff"/></linearGradient>' +
         '<clipPath id="sc' + gid + '"><rect x="0" y="0" width="120" height="' + hz + '"/></clipPath></defs>';
    var sun = '<circle cx="' + CX + '" cy="' + (hz - 8) + '" r="30" fill="url(#sun' + gid + ')"/>';
    for (var i = 0; i < n; i++) sun += '<rect x="20" y="' + f(hz - 28 + i * (24 / n)) + '" width="80" height="' + f(.8 + i * .35) + '" fill="#04020b"/>';
    o += '<g clip-path="url(#sc' + gid + ')" filter="url(#' + gid + ')">' + sun + '</g>';
    var x = 8, city = '';
    while (x < 112) { var w = 5 + R() * 8, h = 6 + R() * 24; city += '<rect x="' + f(x) + '" y="' + f(hz - h) + '" width="' + f(w) + '" height="' + f(h) + '" fill="#0b0620" stroke="' + c2 + '" stroke-width=".4"/>'; if (R() > .5) city += '<rect x="' + f(x + w / 2 - .6) + '" y="' + f(hz - h + 2) + '" width="1.2" height="1.2" fill="#fff4c2"/>'; x += w + 1; }
    o += city + '<line x1="6" y1="' + hz + '" x2="114" y2="' + hz + '" stroke="' + c + '" stroke-width="1"/>';
    var g = '';
    for (var k = -7; k <= 7; k++) g += '<line x1="' + f(CX + k * 3) + '" y1="' + hz + '" x2="' + f(CX + k * 16) + '" y2="176" stroke="' + c + '" stroke-width=".5"/>';
    for (var m = 1; m < 8; m++) { var yy = hz + (176 - hz) * Math.pow(m / 8, 1.8); g += '<line x1="6" y1="' + f(yy) + '" x2="114" y2="' + f(yy) + '" stroke="' + c + '" stroke-width=".5"/>'; }
    return o + '<g opacity=".8" clip-path="url(#gc' + gid + ')">' + g + '</g><clipPath id="gc' + gid + '"><rect x="6" y="' + hz + '" width="108" height="64"/></clipPath>';
  }

  function cardSVG(index, reversed, name, style) {
    style = style || currentStyle();
    var major = index < 22, suit = null, rank = 0, gid = 'tgl' + (++UID);
    if (!major) { var k = index - 22; suit = ['Wands', 'Cups', 'Swords', 'Pentacles'][Math.floor(k / 14)]; rank = k % 14; }
    var edge = major ? '#ff6ec7' : SUIT[suit].col, cosmic = style === 'constellation' || style === 'galaxy', cyber = style === 'neon' || style === 'circuit' || style === 'grid';
    var bg = cosmic ? starfield(index, 70) : cyber ? (style === 'grid' ? starfield(index, 25) : '<g opacity=".12" stroke="#4cc3ff" stroke-width=".3">' + (function () { var g = ''; for (var i = 1; i < 12; i++) g += '<line x1="' + i * 10 + '" y1="4" x2="' + i * 10 + '" y2="196"/>'; for (var j = 1; j < 20; j++) g += '<line x1="4" y1="' + j * 10 + '" x2="116" y2="' + j * 10 + '"/>'; return g; })() + '</g>') : lattice(index);
    var art = style === 'orbital' ? orbitalArt(index) : style === 'feynman' ? feynmanArt(index) : style === 'sacred' ? sacredArt(index) : style === 'rosette' ? rosetteArt(index) :
      style === 'constellation' ? constellationArt(index, gid) : style === 'galaxy' ? galaxyArt(index, gid) : style === 'neon' ? neonArt(index, gid) : style === 'circuit' ? circuitArt(index, gid) : style === 'grid' ? gridArt(index, gid) :
      (major ? majorSigil(index) : minorArt(suit, rank));
    var o = '<svg class="tcard" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + (name || '') + (reversed ? ', reversed' : '') + '">' +
      '<defs><clipPath id="ic' + gid + '"><rect x="6" y="6" width="108" height="188" rx="6"/></clipPath><linearGradient id="tg' + gid + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + (cyber ? '#120a2e' : '#1a0b3d') + '"/><stop offset="1" stop-color="#04020b"/></linearGradient>' + glow(gid, style === 'neon' ? 1.6 : 1) + '</defs>' +
      '<g' + (reversed ? ' transform="rotate(180 60 100)"' : '') + '>' +
      '<rect x="1" y="1" width="118" height="198" rx="9" fill="url(#tg' + gid + ')" stroke="' + edge + '" stroke-width="1.4"' + (cyber ? ' filter="url(#' + gid + ')"' : '') + '/>' +
      '<rect x="6" y="6" width="108" height="188" rx="6" fill="none" stroke="' + edge + '" stroke-width=".4" opacity=".6"/>' + bg +
      (cosmic || cyber ? '' : '<line x1="60" y1="16" x2="60" y2="168" stroke="#f3eeff" stroke-width=".3" stroke-dasharray="1 3" opacity=".5"/>') +   // the mirror axis
      '<g clip-path="url(#ic' + gid + ')">' + art + '</g>' +
      '<text x="60" y="17" text-anchor="middle" font-size="9" fill="#a296d8" font-family="' + (cyber ? 'Consolas,monospace' : 'Segoe UI,system-ui,sans-serif') + '" letter-spacing="1.5">' + (major ? ROMAN[index] : (SUIT[suit].el.toUpperCase())) + '</text>' +
      '<rect x="14" y="178" width="92" height="12" rx="3" fill="#04020b" opacity=".55"/>' +
      '<text x="60" y="187" text-anchor="middle" font-size="8.6" fill="#f3eeff" font-family="Segoe UI,system-ui,sans-serif">' + (name || '').replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</text>' +
      '</g></svg>';
    return o;
  }
  function indexOf(name) {
    var T = window.SarahTarot; if (!T) return -1;
    for (var i = 0; i < 22; i++) if (T.MAJOR[i][0] === name) return i;
    var m = /^(\w+) of (\w+)$/.exec(name); if (!m) return -1;
    var r = T.RANKS.findIndex(function (x) { return x[0] === m[1]; }), s = T.SUITS.findIndex(function (x) { return x[0] === m[2]; });
    return r < 0 || s < 0 ? -1 : 22 + s * 14 + r;
  }
  function currentStyle() { try { var s = localStorage.getItem('sky.deck'); return STYLES.indexOf(s) >= 0 ? s : 'mirror'; } catch (e) { return 'mirror'; } }
  function setStyle(s) { try { localStorage.setItem('sky.deck', s); } catch (e) {} }
  window.SarahTarotArt = { cardSVG: cardSVG, indexOf: indexOf, STYLES: STYLES, STYLE_NAMES: STYLE_NAMES, currentStyle: currentStyle, setStyle: setStyle };
})();
