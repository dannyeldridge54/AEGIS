/* Janus · Data overlay: SERAPIS predictions on the (n_s, r) plane against measured constraints, live with the knobs and the PC collector.
   Values from the D-notes: CMB-SPA n_s 0.9684 ± 0.0030, CMB-SPA+DESI 0.9728 ± 0.0027 (D1248 inputs), r < 0.036 (BK18, 95 %);
   SERAPIS point (D1262, MSSM g*): 0.974393, 4.821e-4; audited box (D1262); frozen band (D693); τ = i point (D1247); attractors (D751, D752);
   SO+SPHEREx forecast σ(n_s) = 0.0016 (2212.04115), LiteBIRD optimistic σ(r) = 5e-5 (D749a). */
(() => {
const cv = document.getElementById('dataplot'); if (!cv) return; const x = cv.getContext('2d'); const W = cv.width, H = cv.height, m = {l: 62, r: 14, t: 14, b: 44};
const NS = [0.955, 0.982], LR = [Math.log10(1e-4), Math.log10(2e-2)];
const X = v => m.l + (v - NS[0])/(NS[1] - NS[0])*(W - m.l - m.r), Y = r => H - m.b - (Math.log10(r) - LR[0])/(LR[1] - LR[0])*(H - m.t - m.b);
const box = [[0.971663, 4.52911e-4], [0.974828, 4.89722e-4], [0.975959, 4.76299e-4], [0.972710, 4.38906e-4]];
let pts = []; const api = () => window.pywebview && window.pywebview.api;
async function poll() { try { if (api() && api().collector_points) pts = await api().collector_points(); } catch (e) {} }
poll(); setInterval(poll, 30000);
function band(c, s, col, a) { for (const k of [2, 1]) { x.fillStyle = col.replace('A', (a/k).toFixed(3)); x.fillRect(X(c - k*s), m.t, X(c + k*s) - X(c - k*s), H - m.t - m.b); } }
function txt(s, px, py, col, f = '12px Cascadia Mono, Consolas, monospace') { x.font = f; x.fillStyle = col; x.fillText(s, px, py); }
function draw() {
  x.clearRect(0, 0, W, H); x.fillStyle = '#05010f'; x.fillRect(0, 0, W, H);
  band(0.9684, 0.0030, 'rgba(47,139,255,A)', 0.22); band(0.9728, 0.0027, 'rgba(212,60,255,A)', 0.22);
  x.fillStyle = 'rgba(255,61,139,0.14)'; x.fillRect(m.l, m.t, W - m.l - m.r, Y(0.036) - m.t);
  x.strokeStyle = 'rgba(160,140,255,.18)'; x.lineWidth = 1;
  for (const v of [0.96, 0.965, 0.97, 0.975, 0.98]) { x.beginPath(); x.moveTo(X(v), m.t); x.lineTo(X(v), H - m.b); x.stroke(); txt(v.toFixed(3), X(v) - 18, H - m.b + 16, '#a296d8'); }
  for (const r of [1e-4, 1e-3, 1e-2]) { x.beginPath(); x.moveTo(m.l, Y(r)); x.lineTo(W - m.r, Y(r)); x.stroke(); txt(r.toExponential(0), 6, Y(r) + 4, '#a296d8'); }
  txt('n_s', W/2, H - 8, '#f3eeff'); txt('r', 8, m.t + 10, '#f3eeff');
  x.strokeStyle = '#6fb8ff'; x.setLineDash([4, 4]); x.strokeRect(X(0.970), Y(5.12e-4), X(0.975) - X(0.970), Y(4.55e-4) - Y(5.12e-4)); x.setLineDash([]); txt('frozen band', X(0.970), Y(5.12e-4) - 4, '#6fb8ff', '11px Segoe UI');
  x.beginPath(); box.forEach(([n, r], k) => k ? x.lineTo(X(n), Y(r)) : x.moveTo(X(n), Y(r))); x.closePath(); x.fillStyle = 'rgba(255,79,216,0.25)'; x.fill(); x.strokeStyle = '#ff4fd8'; x.stroke();
  for (const p of pts) { x.fillStyle = 'rgba(76,195,255,0.65)'; x.beginPath(); x.arc(X(p.ns), Y(p.r), 2, 0, 7); x.fill(); }
  for (const [N, lab] of [[55, 'attractor N*=55'], [60, 'N*=60']]) { const n = 1 - 2/N, r = 12/(N*N); x.fillStyle = '#ffb347'; x.beginPath(); x.arc(X(n), Y(r), 4, 0, 7); x.fill(); txt(lab, X(n) + 6, Y(r) + 4, '#ffb347', '11px Segoe UI'); }
  x.fillStyle = '#a07bff'; x.beginPath(); x.arc(X(0.97462), Y(4.8335e-4), 5, 0, 7); x.fill(); txt('τ = i', X(0.97462) + 7, Y(4.8335e-4) - 8, '#a07bff', '11px Segoe UI');
  const P = [0.974393, 4.821e-4]; x.strokeStyle = 'rgba(255,255,255,.55)'; x.setLineDash([3, 3]);
  x.beginPath(); x.ellipse(X(P[0]), Y(P[1]), X(P[0] + 0.0016) - X(P[0]), Math.abs(Y(P[1] + 5e-5) - Y(P[1])), 0, 0, 7); x.stroke(); x.setLineDash([]);
  x.fillStyle = '#ffffff'; x.shadowColor = '#ff4fd8'; x.shadowBlur = 14; x.beginPath(); x.arc(X(P[0]), Y(P[1]), 6, 0, 7); x.fill(); x.shadowBlur = 0; txt('SERAPIS point', X(P[0]) + 8, Y(P[1]) + 18, '#ffffff', 'bold 12px Segoe UI');
  const ns = parseFloat(document.getElementById('rns')?.textContent), r = parseFloat(document.getElementById('rr')?.textContent);
  if (isFinite(ns) && isFinite(r)) { x.strokeStyle = '#4cc3ff'; x.lineWidth = 2; x.beginPath(); x.arc(X(ns), Y(r), 9, 0, 7); x.stroke(); x.lineWidth = 1; txt('knobs', X(ns) - 18, Y(r) - 13, '#4cc3ff', '11px Segoe UI'); }
  // zoom inset: n_s 0.9705–0.9770 × r 4.3–5.2e-4 (linear)
  const zx = W - 250, zy = m.t + 4, zw = 232, zh = 150, zn = [0.9705, 0.9770], zr = [4.3e-4, 5.2e-4];
  const ZX = v => zx + (v - zn[0])/(zn[1] - zn[0])*zw, ZY = r => zy + zh - (r - zr[0])/(zr[1] - zr[0])*zh;
  x.fillStyle = 'rgba(11,6,32,0.92)'; x.fillRect(zx, zy, zw, zh); x.strokeStyle = '#7a5cff'; x.strokeRect(zx, zy, zw, zh);
  x.save(); x.beginPath(); x.rect(zx, zy, zw, zh); x.clip();
  x.fillStyle = 'rgba(212,60,255,0.18)'; x.fillRect(ZX(0.9728 - 0.0027), zy, ZX(0.9728 + 0.0027) - ZX(0.9728 - 0.0027), zh);
  x.strokeStyle = '#6fb8ff'; x.setLineDash([4, 4]); x.strokeRect(ZX(0.970), ZY(5.12e-4), ZX(0.975) - ZX(0.970), ZY(4.55e-4) - ZY(5.12e-4)); x.setLineDash([]);
  x.beginPath(); box.forEach(([n, r], k) => k ? x.lineTo(ZX(n), ZY(r)) : x.moveTo(ZX(n), ZY(r))); x.closePath(); x.fillStyle = 'rgba(255,79,216,0.28)'; x.fill(); x.strokeStyle = '#ff4fd8'; x.stroke();
  for (const p of pts) { x.fillStyle = 'rgba(76,195,255,0.75)'; x.beginPath(); x.arc(ZX(p.ns), ZY(p.r), 1.8, 0, 7); x.fill(); }
  x.fillStyle = '#a07bff'; x.beginPath(); x.arc(ZX(0.97462), ZY(4.8335e-4), 4, 0, 7); x.fill();
  x.fillStyle = '#fff'; x.beginPath(); x.arc(ZX(0.974393), ZY(4.821e-4), 4.5, 0, 7); x.fill();
  { const ns = parseFloat(document.getElementById('rns')?.textContent), r = parseFloat(document.getElementById('rr')?.textContent);
    if (isFinite(ns) && isFinite(r)) { x.strokeStyle = '#4cc3ff'; x.lineWidth = 2; x.beginPath(); x.arc(ZX(ns), ZY(r), 7, 0, 7); x.stroke(); x.lineWidth = 1; } }
  x.restore(); txt('zoom: n_s 0.9705–0.977, r 4.3–5.2e-4', zx + 4, zy + zh + 12, '#a296d8', '10px Segoe UI');
  txt('white SERAPIS · violet τ=i · pink audited box · dashed frozen · dots collector', zx - 150, zy + zh + 26, '#a296d8', '10px Segoe UI');
  const sig = v => ((v - 0.9684)/0.0030).toFixed(2), sig2 = v => ((v - 0.9728)/0.0027).toFixed(2);
  document.getElementById('datacap').textContent = `point: SPA ${sig(P[0])}σ, SPA+DESI ${sig2(P[0])}σ · knobs: ${isFinite(ns) ? `SPA ${sig(ns)}σ, SPA+DESI ${sig2(ns)}σ` : '—'} · ${pts.length} collector points`;
}
draw(); setInterval(draw, 500);
})();
