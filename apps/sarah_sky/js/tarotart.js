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
  var STYLES = ['mirror', 'orbital', 'feynman', 'sacred', 'rosette'];
  var STYLE_NAMES = { mirror: 'Mirror Lattice', orbital: 'Orbitals', feynman: 'Feynman Paths', sacred: 'Sacred Geometry', rosette: 'Symmetry Rosette' };
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

  function cardSVG(index, reversed, name, style) {
    style = style || currentStyle();
    var major = index < 22, suit = null, rank = 0;
    if (!major) { var k = index - 22; suit = ['Wands', 'Cups', 'Swords', 'Pentacles'][Math.floor(k / 14)]; rank = k % 14; }
    var edge = major ? '#ff6ec7' : SUIT[suit].col;
    var o = '<svg class="tcard" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + (name || '') + (reversed ? ', reversed' : '') + '">' +
      '<defs><linearGradient id="tg' + index + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a0b3d"/><stop offset="1" stop-color="#04020b"/></linearGradient></defs>' +
      '<g' + (reversed ? ' transform="rotate(180 60 100)"' : '') + '>' +
      '<rect x="1" y="1" width="118" height="198" rx="9" fill="url(#tg' + index + ')" stroke="' + edge + '" stroke-width="1.4"/>' +
      '<rect x="6" y="6" width="108" height="188" rx="6" fill="none" stroke="' + edge + '" stroke-width=".4" opacity=".6"/>' + lattice(index) +
      '<line x1="60" y1="16" x2="60" y2="168" stroke="#f3eeff" stroke-width=".3" stroke-dasharray="1 3" opacity=".5"/>' +   // the mirror axis
      (style === 'orbital' ? orbitalArt(index) : style === 'feynman' ? feynmanArt(index) : style === 'sacred' ? sacredArt(index) : style === 'rosette' ? rosetteArt(index) : (major ? majorSigil(index) : minorArt(suit, rank))) +
      '<text x="60" y="17" text-anchor="middle" font-size="9" fill="#a296d8" font-family="Segoe UI,system-ui,sans-serif" letter-spacing="1.5">' + (major ? ROMAN[index] : (SUIT[suit].el.toUpperCase())) + '</text>' +
      '<text x="60" y="186" text-anchor="middle" font-size="8.6" fill="#f3eeff" font-family="Segoe UI,system-ui,sans-serif">' + (name || '').replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</text>' +
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
