/* Time machine: slide the named stars and constellation lines through time using their proper motions.
   Straight-line motion on the sky from today's proper motions (Yale Bright Star Catalogue). It ignores radial
   velocity, parallax change and galactic orbits, so it is a sketch: good for tens of thousands of years, rough
   beyond ~100,000. ESA's Gaia team made the famous version of this idea for 1.6 million years. */
import A from "../vendor/aladin.js";

const MAX_V = 100, YEARS_PER_V2 = 20;                      // slider -100..100 -> years = sign * v^2 * 20 (±200,000)
const yearsFor = (v) => Math.sign(v) * v * v * YEARS_PER_V2;
const NOW = new Date().getUTCFullYear();
const MAS = Math.PI / 180 / 3.6e6;                          // mas -> radians

function move(ra, dec, pm, t) {                              // exact great-circle step along the proper-motion direction
  if (!pm || !t) return [ra, dec];
  const a = ra * Math.PI / 180, d = dec * Math.PI / 180;
  const u = [Math.cos(d) * Math.cos(a), Math.cos(d) * Math.sin(a), Math.sin(d)];
  const ea = [-Math.sin(a), Math.cos(a), 0], ed = [-Math.sin(d) * Math.cos(a), -Math.sin(d) * Math.sin(a), Math.cos(d)];
  const w = [0, 1, 2].map((i) => (pm[0] * ea[i] + pm[1] * ed[i]) * MAS);   // angular velocity vector, rad/yr
  const mu = Math.hypot(w[0], w[1], w[2]); if (!mu) return [ra, dec];
  const th = mu * t, k = w.map((x) => x / mu);
  const p = [0, 1, 2].map((i) => u[i] * Math.cos(th) + k[i] * Math.sin(th));
  return [((Math.atan2(p[1], p[0]) * 180 / Math.PI) + 360) % 360, Math.asin(Math.max(-1, Math.min(1, p[2]))) * 180 / Math.PI];
}

function label(t) {
  const y = Math.round(NOW + t);
  if (Math.abs(t) < 1) return `Today (${NOW})`;
  const f = (n) => Math.abs(n).toLocaleString();
  return (y > 0 ? `AD ${f(y)}` : `${f(1 - y)} BC`) + ` · ${t > 0 ? "+" : "−"}${f(Math.round(t))} years`;
}

function ready(cb) {
  const s = window.__skymap;
  if (s && s.layers && s.layers.stars && s.data && s.data.cons) cb(s); else setTimeout(() => ready(cb), 300);
}

ready(async (state) => {
  let pm; try { pm = await (await fetch("data/proper_motions.json")).json(); } catch { return; }
  const L = state.layers, D = state.data;
  const css = document.createElement("style");
  css.textContent = `
#tmBar{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:30;
 width:min(640px,calc(100vw - 24px));display:none;flex-direction:column;gap:6px;padding:10px 14px 12px;border-radius:14px;
 background:rgba(8,6,28,.88);border:1px solid #2a2f6a;color:#e8ecff;font:13px system-ui,sans-serif;backdrop-filter:blur(6px)}
#tmBar.on{display:flex} #tmBar .row{display:flex;align-items:center;gap:10px}
#tmBar b{font-size:15px;letter-spacing:.02em;flex:1;font-variant-numeric:tabular-nums}
#tmBar input{flex:1;accent-color:#8fa6ff;height:28px} #tmBar button{background:#1a1f4a;color:#e8ecff;border:1px solid #33407a;
 border-radius:8px;padding:4px 10px;font:inherit;cursor:pointer;min-width:38px;min-height:32px} #tmBar small{color:#9aa3d8;line-height:1.35}
#tmBtn[aria-pressed=true]{background:#1a1f4a;border-color:#8fa6ff}`;
  document.head.appendChild(css);
  const bar = document.createElement("div"); bar.id = "tmBar"; bar.setAttribute("role", "group"); bar.setAttribute("aria-label", "Time machine");
  bar.innerHTML = `<div class="row"><b id="tmYear">${label(0)}</b>
    <button id="tmPlay" title="Play: run time forward (Space)">▶</button><button id="tmRev" title="Play backward">◀</button>
    <button id="tmNow" title="Back to today">Now</button><button id="tmX" aria-label="Close time machine">×</button></div>
    <div class="row"><span aria-hidden="true">−200k</span><input id="tmSlide" type="range" min="-${MAX_V}" max="${MAX_V}" step="1" value="0" aria-label="Years from today"><span aria-hidden="true">+200k</span></div>
    <small>Stars drift across the sky by their measured proper motions (Yale Bright Star Catalogue). Straight-line sketch: good for tens of thousands of years, rough beyond ~100,000. Try the Big Dipper or Orion.</small>`;
  document.body.appendChild(bar);
  const big = document.getElementById("bigText");
  const btn = document.createElement("button"); btn.id = "tmBtn"; btn.className = "toggle"; btn.textContent = "⏳";
  btn.title = "Time machine: watch the constellations change over 200,000 years (T)"; btn.setAttribute("aria-pressed", "false");
  big.parentNode.insertBefore(btn, big);

  let t = 0, raf = 0, dir = 0, last = 0;
  function redraw() {
    raf = 0;
    if (L.constellations) {
      L.constellations.removeAll();
      for (const c of D.cons.constellations) c.lines.forEach((seg, si) => {
        const pms = (pm.lines[c.id] || [])[si] || [];
        const pts = seg.map((p, i) => move(p[0], p[1], pms[i], t));
        let cur = [pts[0]];
        for (let i = 1; i < pts.length; i++) { if (Math.abs(pts[i][0] - pts[i - 1][0]) > 180) { if (cur.length > 1) L.constellations.add(A.polyline(cur)); cur = []; } cur.push(pts[i]); }
        if (cur.length > 1) L.constellations.add(A.polyline(cur));
      });
    }
    const src = (list) => list.map((s) => { const [ra, dec] = move(s.ra, s.dec, pm.stars[s.name], t); return A.source(ra, dec, { kind: "star", label: s.name, ...s, ra, dec }); });
    if (L.stars) { L.stars.removeAll(); L.stars.addSources(src(D.stars.stars)); }
    if (L.starsBright) { L.starsBright.removeAll(); L.starsBright.addSources(src(D.stars.stars.filter((s) => s.mag < 1.0))); }
    document.getElementById("tmYear").textContent = label(t);
    window.__skymap.timeYears = t;
  }
  const schedule = () => { if (!raf) raf = requestAnimationFrame(redraw); };
  const slide = document.getElementById("tmSlide");
  function setV(v) { slide.value = v; t = yearsFor(+v); schedule(); }
  slide.addEventListener("input", () => { dir = 0; setPlay(); setV(slide.value); });
  function setPlay() { document.getElementById("tmPlay").textContent = dir > 0 ? "❚❚" : "▶"; document.getElementById("tmRev").textContent = dir < 0 ? "❚❚" : "◀"; }
  function tick(ts) {
    if (!dir) return;
    if (ts - last > 60) { last = ts; let v = +slide.value + dir; if (v > MAX_V || v < -MAX_V) { dir = 0; setPlay(); return; } setV(v); }
    requestAnimationFrame(tick);
  }
  function play(d) { dir = dir === d ? 0 : d; setPlay(); if (dir) requestAnimationFrame(tick); }
  document.getElementById("tmPlay").onclick = () => play(1);
  document.getElementById("tmRev").onclick = () => play(-1);
  document.getElementById("tmNow").onclick = () => { dir = 0; setPlay(); setV(0); };
  function open(on) { bar.classList.toggle("on", on); btn.setAttribute("aria-pressed", String(on)); if (!on) { dir = 0; setPlay(); setV(0); } }
  document.getElementById("tmX").onclick = () => open(false);
  btn.onclick = () => open(!bar.classList.contains("on"));
  document.addEventListener("keydown", (e) => {
    if (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName || "") || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "t" || e.key === "T") open(!bar.classList.contains("on"));
    else if (e.key === " " && bar.classList.contains("on")) { e.preventDefault(); play(1); }
  });
  window.__skymap.timeMachine = { setYears: (y) => { const v = Math.sign(y) * Math.sqrt(Math.abs(y) / YEARS_PER_V2); setV(Math.round(v)); }, open, move };
});
