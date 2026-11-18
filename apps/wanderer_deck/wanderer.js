/* The Wanderer — Danny's character for his own tarot deck. Original procedural SVG, (c) Danny Lee Eldridge, AEGIS Community License.
   One figure, many lights: a hooded, bearded ascetic with a deer antler on one side and a ram horn on the other (the mirror),
   one open eye (Odin's price for knowledge), the Algiz rune (ᛉ, protection, the elk) on the brow, Yggdrasil behind him.
   Variants run from full light to full dark. */
(function () {
  function f(n) { return Math.round(n * 10) / 10; }
  function rng(s) { var a = s * 7919 + 17; return function () { a = (a * 16807) % 2147483647; return a / 2147483647; }; }

  var V = [
    { key: 'dawn', skin: '#f2c6a8', beardC: '#c0622e', chart: 'Ascendant 28° Virgo — the Hermit\'s sign', story: 'Born at the Hermit\'s door: Virgo rising carries the lantern into the world.', name: 'The Hermit of Dawn', note: 'lantern lit, robe of morning light', dark: 0.0,
      bg: ['#fff7d6', '#ffc98a'], sky: '#fffbe8', cloak: '#f3eeff', edge: '#d8a54a', face: '#3a2a10', beard: '#ffffff', bone: '#c9a66b', horn: '#b0895a', eye: '#ffcc33', staff: 'lantern', tree: '#e0b070', halo: 1 },
    { key: 'ascetic', skin: '#ecc4a6', beardC: '#b85a2a', chart: 'Saturn 11° Aquarius · 5th house', story: 'Saturn takes the toys away; what is left is the staff and the sun.', name: 'The Ascetic', note: 'nothing kept but the staff and the sun', dark: 0.12,
      bg: ['#ffe9f3', '#c9b8ff'], sky: '#fff4c2', cloak: '#e8dcc8', edge: '#a07bff', face: '#2a1f3a', beard: '#f3eeff', bone: '#d8c8a8', horn: '#b8a07a', eye: '#4cc3ff', staff: 'plain', tree: '#b9a0e8', halo: 1, thin: 1 },
    { key: 'green', skin: '#e0b896', beardC: '#a8501f', chart: 'Venus ☌ Mars, Capricorn · 4th house', story: 'Love and the axe in one house at midwinter: the Green Knight\'s Yule bargain.', name: 'The Green Knight', note: 'holly and axe; the bargain of the turning year', dark: 0.25,
      bg: ['#d9f5c8', '#3f7d3a'], sky: '#f6ffd8', cloak: '#2f7a32', edge: '#b6e36a', face: '#0e2a10', beard: '#6fbf4a', bone: '#d9cfa0', horn: '#8a7a4a', eye: '#e8ff7a', staff: 'axe', tree: '#5a9a40', ivy: 3, holly: 1 },
    { key: 'ygg', skin: '#d8b49c', beardC: '#a0522a', chart: 'Uranus ☌ Neptune, Capricorn · 4th house', story: 'The roots are lightning and dream. The family tree is a world tree, and the Elder stag walks it.', name: 'Yggdrasil Walker', note: 'the World Tree grows out of his crown', dark: 0.35,
      bg: ['#bfe7ff', '#2a4a7a'], sky: '#e8f6ff', cloak: '#3a5a8a', edge: '#4cc3ff', face: '#0b1a2a', beard: '#cfe6ff', bone: '#e8dcc0', horn: '#a08a60', eye: '#6fb8ff', staff: 'plain', tree: '#7aa0d0', bigTree: 1, ivy: 1 },
    { key: 'allfather', skin: '#c8ac9c', beardC: '#9a4e2a', chart: 'Sun ☌ Mercury, Aquarius · 5th house', story: 'Mercury is Woden. The sun travels with the messenger; the ravens are thought and memory.', name: 'The Allfather', note: 'Huginn and Muninn, Gungnir, one eye given for wisdom', dark: 0.48,
      bg: ['#9aa0c0', '#1a1830'], sky: '#d0d4ee', cloak: '#4a4a62', edge: '#a296d8', face: '#08080f', beard: '#d8d8e8', bone: '#cfc4a8', horn: '#7a6a50', eye: '#4cc3ff', staff: 'spear', tree: '#5a5878', ravens: 1 },
    { key: 'ivy', skin: '#a89a7a', beardC: '#7a4a22', chart: 'Jupiter ℞ 11° Virgo · 12th house', story: 'Growth that happens out of sight: the forest grows through him while no one is looking.', name: 'Overgrown', note: 'the forest takes him back, gently', dark: 0.58,
      bg: ['#5a7a50', '#0e1a0c'], sky: '#9ac080', cloak: '#25351f', edge: '#7ac05a', face: '#050a04', beard: '#8aa070', bone: '#b0a880', horn: '#6a5a3a', eye: '#b6ff6a', staff: 'plain', tree: '#3a5a2a', ivy: 9, flowers: 1 },
    { key: 'hanged', skin: '#b8a0c0', beardC: '#8a4a3a', chart: 'Moon 25° Cancer · 10th house', story: 'Hung at the top of the sky by his own heart, nine nights, until the runes come.', name: 'Nine Nights', note: 'hung on the windy tree, wounded by his own spear, he finds the runes', dark: 0.7,
      bg: ['#3a2a5a', '#04020b'], sky: '#7a5cff', cloak: '#2a1f5a', edge: '#d43cff', face: '#000', beard: '#b0a0e0', bone: '#d8d0e8', horn: '#8a7aa0', eye: '#ff6ec7', staff: 'none', tree: '#4a3a7a', hanged: 1, runes: 1 },
    { key: 'decay', skin: '#a0987a', beardC: '#6a4a2a', chart: 'Pluto 23° Scorpio · 2nd house', story: 'What he owns must rot so something can grow. Scorpio\'s card is Death, and Death is rebirth.', name: 'The Rot', note: 'bone antlers, moth-eaten cloak, mushrooms at his feet', dark: 0.8,
      bg: ['#4a4630', '#0a0904'], sky: '#8a8460', cloak: '#3a3524', edge: '#9a9060', face: '#000', beard: '#7a7460', bone: '#d8d0b0', horn: '#5a4a30', eye: '#c8d040', staff: 'plain', tree: '#3a3424', decay: 1 },
    { key: 'blood', skin: '#b88a80', beardC: '#7a2a1a', chart: 'Moon ☍ Mars', story: 'The moon against the warrior. The price is paid in full.', name: 'Blood Moon', note: 'red moon, thorned crown, the price paid in full', dark: 0.9,
      bg: ['#3a0610', '#050102'], sky: '#d01030', cloak: '#1a0306', edge: '#ff3d5b', face: '#000', beard: '#5a1a1e', bone: '#e8d0c8', horn: '#4a1a1a', eye: '#ff2040', staff: 'spear', tree: '#3a0a12', blood: 1, thorns: 1 },
    { key: 'madness', skin: '#a890c8', beardC: '#d43cff', chart: 'Sun □ Pluto', story: 'The self pressed until it splits into colours — and is made again.', name: 'The Unravelling', note: 'too many eyes open at once; the mind splits into colours', dark: 1.0,
      bg: ['#1a0630', '#000'], sky: '#ff6ec7', cloak: '#120a2e', edge: '#d43cff', face: '#000', beard: '#7a5cff', bone: '#f3eeff', horn: '#d43cff', eye: '#ff6ec7', staff: 'plain', tree: '#2a1f5a', madness: 1 }
  ];

  function branch(R, x, y, ang, len, depth, col, w, out) {   // antlers and tree limbs
    var x2 = x + len * Math.cos(ang), y2 = y + len * Math.sin(ang);
    out.push('<path d="M' + f(x) + ' ' + f(y) + ' L' + f(x2) + ' ' + f(y2) + '" stroke="' + col + '" stroke-width="' + f(w) + '" stroke-linecap="round" fill="none"/>');
    if (depth <= 0) return [[x2, y2]];
    var tips = [], n = depth > 2 ? 2 : 2 + (R() > .5 ? 1 : 0);
    for (var i = 0; i < n; i++) {
      var a = ang + (i - (n - 1) / 2) * (0.5 + R() * 0.3) + (R() - .5) * .2;
      tips = tips.concat(branch(R, x2, y2, a, len * (0.62 + R() * .15), depth - 1, col, w * .68, out));
    }
    return tips;
  }
  function antler(R, col, out) {   // royal stag (the Eldridge / Elder crest): beam with brow, bez, trez tines and a crown of three
    var beam = [[86, 88], [76, 74], [70, 56], [70, 38], [74, 20]];
    out.push('<path d="M' + beam.map(function (p) { return p.join(' '); }).join(' L') + '" stroke="' + col + '" stroke-width="4.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>');
    var tines = [[80, 80, 56, 76], [74, 68, 52, 58], [70, 50, 50, 40], [72, 26, 58, 8], [74, 20, 72, 2], [74, 22, 88, 6]], tips = [];
    tines.forEach(function (t) { var mx = (t[0] + t[2]) / 2, my = (t[1] + t[3]) / 2 + 4;
      out.push('<path d="M' + t[0] + ' ' + t[1] + ' Q' + mx + ' ' + my + ' ' + t[2] + ' ' + t[3] + '" stroke="' + col + '" stroke-width="2.8" fill="none" stroke-linecap="round"/>'); tips.push([t[2], t[3]]); });
    return tips;
  }
  function ramHorn(col, out) {   // ram horn, right side: a thick spiral curling out and down past the ear
    var cx = 132, cy = 100, p = [];
    for (var i = 0; i <= 60; i++) { var t = i / 60, a = -2.3 + t * 5.6, r = 22 * (1 - t * .78); p.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
    var d = 'M' + p.map(function (q) { return f(q[0]) + ' ' + f(q[1]); }).join(' L');
    out.push('<path d="' + d + '" stroke="' + col + '" stroke-width="8" fill="none" stroke-linecap="round"/>');
    out.push('<path d="' + d + '" stroke="#000" stroke-opacity=".35" stroke-width="8" stroke-dasharray=".8 2.6" fill="none"/>');   // ridges
    return p[0];
  }
  function leaf(x, y, a, s, col) { return '<path transform="translate(' + f(x) + ' ' + f(y) + ') rotate(' + f(a) + ') scale(' + s + ')" d="M0 0 C-4 -2 -5 -7 -2 -9 C-1 -7 1 -7 2 -9 C5 -7 4 -2 0 0Z" fill="' + col + '"/>'; }
  function ivy(R, n, col, out) {   // vines climbing the cloak with ivy leaves
    for (var k = 0; k < n; k++) {
      var x = 55 + R() * 90, y = 285, d = 'M' + f(x) + ' ' + y, leaves = '';
      for (var s = 0; s < 7; s++) { var nx = x + (R() - .5) * 26, ny = y - 18 - R() * 10; d += ' Q' + f((x + nx) / 2 + (R() - .5) * 14) + ' ' + f((y + ny) / 2) + ' ' + f(nx) + ' ' + f(ny); x = nx; y = ny; if (y < 140) break;
        leaves += leaf(x, y, R() * 360, .9 + R() * .5, col) + leaf(x + 4, y + 6, R() * 360, .7, col); }
      out.push('<path d="' + d + '" stroke="' + col + '" stroke-width="1" fill="none" opacity=".9"/>' + leaves);
    }
  }
  function raven(x, y, s, flip) { return '<path transform="translate(' + x + ' ' + y + ') scale(' + (flip ? -s : s) + ' ' + s + ')" d="M0 0 C6 -8 14 -10 20 -6 C14 -4 12 -1 10 2 L16 6 L8 4 C5 6 2 5 0 0Z M-2 -1 L-6 -2 L-2 1Z" fill="#05040a"/>'; }
  function algiz(x, y, s, col) { return '<path d="M' + x + ' ' + (y + s) + ' L' + x + ' ' + (y - s) + ' M' + (x - s * .7) + ' ' + (y - s) + ' L' + x + ' ' + (y - s * .2) + ' L' + (x + s * .7) + ' ' + (y - s) + '" stroke="' + col + '" stroke-width="1.1" fill="none" stroke-linecap="round"/>'; }
  function eyeDiamond(x, y, s, col) { return '<path d="M' + (x - s) + ' ' + y + ' L' + x + ' ' + (y - s * .55) + ' L' + (x + s) + ' ' + y + ' L' + x + ' ' + (y + s * .55) + 'Z" fill="#000" stroke="' + col + '" stroke-width=".8"/><circle cx="' + x + '" cy="' + y + '" r="' + f(s * .22) + '" fill="' + col + '"/>'; }

  function figure(v, R, uid) {   // Danny: shaved crown, short dark sides, full red beard, blue-grey eyes; hood down on the shoulders
    var o = [], w = v.thin ? .82 : 1, sk = v.skin, bc = v.beardC;
    o.push('<path d="M100 132 C78 130 64 138 ' + f(100 - 46 * w) + ' 156 C' + f(100 - 52 * w) + ' 180 ' + f(100 - 54 * w) + ' 220 ' + f(100 - 60 * w) + ' 286 L' + f(100 + 60 * w) + ' 286 C' + f(100 + 54 * w) + ' 220 ' + f(100 + 52 * w) + ' 180 ' + f(100 + 46 * w) + ' 156 C136 138 122 130 100 132Z" fill="' + v.cloak + '" stroke="' + v.edge + '" stroke-width="1.4"/>');
    o.push('<path d="M64 146 C76 128 124 128 136 146 C124 140 76 140 64 146Z" fill="' + v.edge + '" opacity=".55"/>');   // the hood, down
    o.push('<path d="M100 160 L100 286" stroke="' + v.edge + '" stroke-width=".6" opacity=".5"/>');                  // the mirror seam
    o.push('<ellipse cx="80" cy="108" rx="3.5" ry="6" fill="' + sk + '"/><ellipse cx="120" cy="108" rx="3.5" ry="6" fill="' + sk + '"/>');   // ears
    o.push('<path d="M100 78 C86 78 80 90 80 104 C80 118 88 128 100 128 C112 128 120 118 120 104 C120 90 114 78 100 78Z" fill="' + sk + '"/>');  // head
    o.push('<path d="M81 96 C80 104 81 110 83 114 L85 113 C84 107 84 101 85 95Z M119 96 C120 104 119 110 117 114 L115 113 C116 107 116 101 115 95Z" fill="#4a3a2a" opacity=".85"/>');   // short dark sides
    o.push('<ellipse cx="94" cy="84" rx="7" ry="3.5" fill="#fff" opacity=".22"/>');                                   // light on the shaved crown
    o.push(algiz(100, 89, 3.2, v.eye).replace('stroke-width="1.1"', 'stroke-width=".9" opacity=".8"'));
    o.push('<path d="M88 99 Q93 96 97 99 M103 99 Q107 96 112 99" stroke="#6a3a1e" stroke-width="1.6" fill="none" stroke-linecap="round"/>');   // brows
    if (v.madness) { o.push(eyeDiamond(93, 104, 4, '#4cc3ff'), eyeDiamond(107, 104, 4, '#ff6ec7')); }
    else {
      o.push('<path d="M89 104 Q93 101 97 104 Q93 106 89 104Z" fill="#fff"/><circle cx="93" cy="104" r="1.6" fill="#7a9ab0"/><circle cx="93" cy="104" r="1.6" fill="' + v.eye + '" opacity=".55" filter="url(#gl' + uid + ')"/>');   // the eye kept
      o.push('<path d="M103 104 Q107 106 111 104" stroke="#5a3020" stroke-width="1.1" fill="none" stroke-linecap="round"/>');   // the eye given (closed)
    }
    o.push('<path d="M100 102 L98 112 Q100 114 103 112" stroke="#000" stroke-opacity=".25" stroke-width=".9" fill="none"/>');   // nose
    // the beard: full, wide, red
    var bd = 'M80 106 C78 126 80 146 89 155 C95 161 105 161 111 155 C120 146 122 126 120 106 C117 116 112 120 106 120 L94 120 C88 120 83 116 80 106Z';
    o.push('<path d="' + bd + '" fill="' + bc + '"/>');
    for (var i = 0; i < 14; i++) { var x = 84 + i * 2.4; o.push('<path d="M' + f(x) + ' ' + f(112 + Math.abs(i - 6.5) * .6) + ' Q' + f(x + (R() - .5) * 3) + ' 136 ' + f(x * .55 + 45) + ' ' + f(150 + (6.5 - Math.abs(i - 6.5)) * 1.4) + '" stroke="#000" stroke-opacity=".22" stroke-width=".7" fill="none"/>'); }
    o.push('<path d="M90 117 C94 114 98 115 100 116 C102 115 106 114 110 117 C106 119 103 118 100 118 C97 118 94 119 90 117Z" fill="' + bc + '" stroke="#000" stroke-opacity=".25" stroke-width=".5"/>');   // moustache
    o.push('<path d="M96 120 Q100 121 104 120" stroke="#5a2a1a" stroke-width=".9" fill="none"/>');   // mouth
    return o;
  }
  function staff(v, w, uid) {
    var x = 100 + 46 * w, o = [];
    if (v.staff === 'none') return o;
    o.push('<path d="M' + f(x) + ' 120 L' + f(x + 3) + ' 290" stroke="#5a3a1a" stroke-width="3" stroke-linecap="round"/>');
    if (v.staff === 'lantern') o.push('<path d="M' + f(x) + ' 120 l0 -6" stroke="#5a3a1a" stroke-width="1.5"/><rect x="' + f(x - 6) + '" y="100" width="12" height="16" rx="2" fill="#fff4c2" stroke="#7a5a20" filter="url(#gl' + uid + ')"/><circle cx="' + f(x) + '" cy="108" r="3.5" fill="#ffcc33"/>');
    if (v.staff === 'spear') o.push('<path d="M' + f(x - 4) + ' 122 L' + f(x) + ' 92 L' + f(x + 4) + ' 122Z" fill="#cfd4e8" stroke="#333" stroke-width=".6"/>');
    if (v.staff === 'axe') o.push('<path d="M' + f(x + 1) + ' 126 C' + f(x + 22) + ' 116 ' + f(x + 26) + ' 140 ' + f(x + 22) + ' 152 C' + f(x + 14) + ' 144 ' + f(x + 6) + ' 142 ' + f(x + 1) + ' 144Z" fill="#c8d0c0" stroke="#2a3a2a" stroke-width=".8"/>');
    return o;
  }

  function cardSVG(k, opts) {
    opts = opts || {};
    var v = typeof k === 'number' ? V[k] : V.filter(function (x) { return x.key === k; })[0], R = rng(V.indexOf(v) + 3), uid = 'w' + Math.floor(Math.random() * 1e9);
    var o = [], w = v.thin ? .82 : 1;
    o.push('<defs><linearGradient id="bg' + uid + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + v.bg[0] + '"/><stop offset="1" stop-color="' + v.bg[1] + '"/></linearGradient>' +
      '<radialGradient id="sk' + uid + '"><stop offset="0" stop-color="' + v.sky + '" stop-opacity="1"/><stop offset=".6" stop-color="' + v.sky + '" stop-opacity=".5"/><stop offset="1" stop-color="' + v.sky + '" stop-opacity="0"/></radialGradient>' +
      '<filter id="gl' + uid + '" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
      '<clipPath id="cp' + uid + '"><rect x="4" y="4" width="192" height="292" rx="10"/></clipPath></defs>');
    o.push('<g clip-path="url(#cp' + uid + ')"><rect width="200" height="300" fill="url(#bg' + uid + ')"/>');
    // sky body: sun / moon behind the head
    o.push('<circle cx="100" cy="92" r="' + (v.halo ? 70 : 58) + '" fill="url(#sk' + uid + ')"/>');
    if (v.blood) o.push('<circle cx="100" cy="70" r="40" fill="#b00a20" opacity=".9"/><circle cx="100" cy="70" r="40" fill="none" stroke="#ff3d5b" stroke-width="1"/>');
    if (v.madness) { var sp = ''; for (var s = 0; s < 220; s++) { var a = s * .19, r = 2 + s * .5; sp += (s ? ' L' : 'M') + f(100 + r * Math.cos(a)) + ' ' + f(110 + r * Math.sin(a)); } o.push('<path d="' + sp + '" stroke="#d43cff" stroke-width=".8" fill="none" opacity=".55"/>'); }
    // Yggdrasil behind
    var tr = [];
    if (v.bigTree) { branch(R, 100, 300, -Math.PI / 2, 70, 6, v.tree, 9, tr); }
    else { branch(R, 30, 300, -Math.PI / 2 + .15, 50, 4, v.tree, 5, tr); branch(R, 170, 300, -Math.PI / 2 - .15, 50, 4, v.tree, 5, tr); }
    o.push('<g opacity="' + (v.bigTree ? .95 : .6) + '">' + tr.join('') + '</g>');
    // roots
    var rt = []; for (var q = 0; q < 5; q++) branch(R, 100, 286, Math.PI / 2 + (q - 2) * .5, 14, 2, v.tree, 3, rt); o.push('<g opacity=".7">' + rt.join('') + '</g>');

    var fig = [], at = antler(R, v.bone, fig), hornEnd = ramHorn(v.horn, fig);
    fig = fig.concat(figure(v, R, uid), staff(v, w, uid));
    if (v.ivy) ivy(R, v.ivy, v.key === 'ivy' ? '#5aa040' : '#3f8a32', fig);
    if (v.ravens) fig.push(raven(150, 60, 1.1, false), raven(46, 132, 1, true), raven(146, 150, .8, false));
    if (v.flowers) for (var fl = 0; fl < 10; fl++) fig.push('<circle cx="' + f(55 + R() * 90) + '" cy="' + f(150 + R() * 130) + '" r="1.6" fill="#ffd6f2"/>');
    if (v.holly) for (var h = 0; h < 6; h++) { var hx = 76 + h * 9.6, hy = 86 - Math.abs(h - 2.5) * 3; fig.push(leaf(hx, hy, h * 60, 1.1, '#1f6a28') + '<circle cx="' + hx + '" cy="' + (hy + 2) + '" r="1.5" fill="#e0203a"/>'); }
    if (v.thorns) { var th = 'M80 86'; for (var t = 0; t < 9; t++) th += ' L' + (82 + t * 4.5) + ' ' + (t % 2 ? 76 : 84); fig.push('<path d="' + th + '" stroke="#3a0a0a" stroke-width="1.6" fill="none"/>'); }
    if (v.blood) { at.slice(0, 7).forEach(function (p) { fig.push('<path d="M' + f(p[0]) + ' ' + f(p[1]) + ' q1.5 5 0 ' + f(5 + R() * 9) + '" stroke="#c00020" stroke-width="1.6" fill="none" stroke-linecap="round"/>'); });
      fig.push('<path d="M93 106 q1 6 -1 12" stroke="#ff2040" stroke-width="1.2" fill="none"/>'); }
    if (v.decay) { for (var c = 0; c < 9; c++) { var cx = 60 + R() * 80, cy = 170 + R() * 110; fig.push('<ellipse cx="' + f(cx) + '" cy="' + f(cy) + '" rx="' + f(2 + R() * 4) + '" ry="' + f(1.5 + R() * 3) + '" fill="#0a0904"/>'); }
      for (var m = 0; m < 5; m++) { var mx = 40 + m * 30, my = 286; fig.push('<path d="M' + (mx - 6) + ' ' + my + ' Q' + mx + ' ' + (my - 12) + ' ' + (mx + 6) + ' ' + my + 'Z" fill="#c8b890"/><rect x="' + (mx - 1.2) + '" y="' + my + '" width="2.4" height="6" fill="#d8d0b0"/>'); }
      for (var mo = 0; mo < 4; mo++) { var ox = 30 + R() * 140, oy = 40 + R() * 80; fig.push('<path d="M' + f(ox) + ' ' + f(oy) + ' l-5 -3 l1 6Z M' + f(ox) + ' ' + f(oy) + ' l5 -3 l-1 6Z" fill="#b0a880" opacity=".8"/>'); } }
    if (v.madness) { var cols = ['#4cc3ff', '#ff6ec7', '#d43cff', '#7a5cff'];
      for (var e = 0; e < 14; e++) fig.push(eyeDiamond(f(56 + R() * 88), f(160 + R() * 120), 3 + R() * 4, cols[e % 4]));
      for (var e2 = 0; e2 < 6; e2++) fig.push(eyeDiamond(f(20 + R() * 160), f(20 + R() * 60), 3 + R() * 3, cols[e2 % 4])); }
    if (v.runes) for (var rn = 0; rn < 9; rn++) fig.push(algiz(f(30 + R() * 140), f(160 + R() * 120), 4, v.eye).replace('stroke-width="1.1"', 'stroke-width="1.1" opacity=".75"'));

    var body = '<g>' + fig.join('') + '</g>';
    if (v.hanged) {   // Odin's nine nights: hung from Yggdrasil by one foot, upside down — the Hanged Man
      o.push('<path d="M10 20 C70 6 130 6 190 22" stroke="' + v.tree + '" stroke-width="7" fill="none"/><path d="M100 10 L100 26" stroke="#c8b890" stroke-width="1.4"/>');
      body = '<g transform="translate(100 172) rotate(180) scale(.62) translate(-100 -150)">' + fig.join('') + '</g>';
      o.push('<path d="M100 26 L100 ' + (172 - 0.62 * 136) + '" stroke="#c8b890" stroke-width="1.2"/>');
    }
    if (v.madness) o.push('<g opacity=".35" transform="translate(-3 0)" style="mix-blend-mode:screen">' + fig.slice(0, 4).join('').replace(/fill="#[0-9a-f]{3,6}"/gi, 'fill="#4cc3ff"').replace(/stroke="#[0-9a-f]{3,6}"/gi, 'stroke="#4cc3ff"') + '</g>');
    o.push(body);
    if (v.madness) o.push('<g opacity=".3" transform="translate(3 1)">' + fig.slice(0, 4).join('').replace(/fill="#[0-9a-f]{3,6}"/gi, 'fill="#ff3d8b"').replace(/stroke="#[0-9a-f]{3,6}"/gi, 'stroke="#ff3d8b"') + '</g>');
    o.push('</g>');
    // frame and title plate
    var light = v.dark < .5, ink = light ? '#2a1f3a' : '#f3eeff';
    o.push('<rect x="4" y="4" width="192" height="292" rx="10" fill="none" stroke="' + v.edge + '" stroke-width="2"/>');
    if (opts.title !== false) o.push('<rect x="16" y="254" width="168" height="36" rx="6" fill="' + (light ? '#fff' : '#04020b') + '" opacity=".74"/>' +
      '<text x="100" y="270" text-anchor="middle" font-family="Georgia,serif" font-size="12" fill="' + ink + '">' + v.name + '</text>' +
      '<text x="100" y="284" text-anchor="middle" font-family="Georgia,serif" font-size="7.6" fill="' + ink + '" opacity=".8">' + v.chart + '</text>');
    return '<svg class="wcard" viewBox="0 0 200 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + v.name + '">' + o.join('') + '</svg>';
  }
  var api = { VARIANTS: V, cardSVG: cardSVG };
  if (typeof module !== 'undefined') module.exports = api; else window.WandererArt = api;
})();
