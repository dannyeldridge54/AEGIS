/* Janus · MEMORY STARS — CubeMind's memory as a star field.
   Each star is one D-note it remembers (public titles only; no private memory text).
   Magenta = passed/adopted, grey = killed, cyan = note. Search lights matches and draws a constellation to them. */
(() => {
const MS = (window.AEGIS && window.AEGIS.memstars) || []; if (!MS.length) return;
const g = new THREE.Group(); g.visible = false; scene.add(g);
const COL = {pass: new THREE.Color('#ff4fd8'), killed: new THREE.Color('#6a6a8a'), note: new THREE.Color('#4cc3ff')};
const S = 46;
const geo = new THREE.BufferGeometry(); const pos = new Float32Array(MS.length*3); const col = new Float32Array(MS.length*3);
MS.forEach((m, i) => { pos[3*i] = m.pos[0]*S; pos[3*i+1] = m.pos[1]*S; pos[3*i+2] = m.pos[2]*S;
  const c = COL[m.topic] || COL.note; col[3*i] = c.r; col[3*i+1] = c.g; col[3*i+2] = c.b; });
geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
const mat = new THREE.PointsMaterial({size: 1.4, vertexColors: true, transparent: true, opacity: 0.92, sizeAttenuation: true});
const pts = new THREE.Points(geo, mat); g.add(pts);
// constellation lines for search matches
const lgeo = new THREE.BufferGeometry(); const lmat = new THREE.LineBasicMaterial({color: new THREE.Color('#a07bff'), transparent: true, opacity: 0.7});
const lines = new THREE.LineSegments(lgeo, lmat); g.add(lines);
const title = (() => { const cv = document.createElement('canvas'); cv.width = 512; cv.height = 64; const x = cv.getContext('2d');
  x.fillStyle = '#6fb8ff'; x.font = 'bold 30px Segoe UI'; x.fillText(`${MS.length} memories`, 8, 42);
  const t = new THREE.CanvasTexture(cv); const sp = new THREE.Sprite(new THREE.SpriteMaterial({map: t, transparent: true, depthWrite: false})); sp.scale.set(26, 3.3, 1); sp.position.set(0, S*0.95, 0); return sp; })();
g.add(title);
const q = document.getElementById('memq'), read = document.getElementById('memread');
let pulse = []; // indices of matches
function search(str) {
  str = (str || '').toLowerCase().trim(); pulse = [];
  if (str) MS.forEach((m, i) => { if (m.id.toLowerCase().includes(str) || m.title.toLowerCase().includes(str)) pulse.push(i); });
  // constellation: connect matches in sequence
  const lp = []; for (let k = 0; k + 1 < pulse.length && k < 40; k++) { const a = pulse[k], b = pulse[k+1];
    lp.push(pos[3*a], pos[3*a+1], pos[3*a+2], pos[3*b], pos[3*b+1], pos[3*b+2]); }
  lgeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(lp), 3)); lgeo.attributes.position && (lgeo.attributes.position.needsUpdate = true);
  if (read) read.textContent = str ? `${pulse.length} match${pulse.length===1?'':'es'}` + (pulse.length ? ': ' + pulse.slice(0,5).map(i=>MS[i].id).join(', ') + (pulse.length>5?'…':'') : '') : 'type to light the matches and draw the constellation';
}
q && q.addEventListener('input', () => search(q.value));
tabs.memstars = 't-memstars';
const _sv = setView;
setView = function (v) { if (v === 'memstars') { view = v; Object.entries(tabs).forEach(([k, id]) => document.getElementById(id)?.setAttribute('aria-selected', String(k === v)));
    weave.visible = false; land.visible = false; scene.children.forEach(c => { if (c !== g && c.type === 'Group' && c !== weave && c !== land) c.visible = false; });
    g.visible = true; document.getElementById('hud').hidden = true; const mc = document.getElementById('memcard'); if (mc) mc.hidden = false;
    setCam(true); persp.position.set(0, 0, 120); ctl.target.set(0, 0, 0); return; }
  g.visible = false; const mc = document.getElementById('memcard'); if (mc) mc.hidden = true; _sv(v); };
document.getElementById('t-memstars')?.addEventListener('click', () => setView('memstars'));
function loop(t) { requestAnimationFrame(loop); if (view !== 'memstars') return; g.rotation.y = 0.03*t/1000;
  const s = 1 + 0.5*Math.sin(t/300); pulse.forEach(() => {}); mat.size = 1.4; if (pulse.length) lmat.opacity = 0.4 + 0.3*Math.sin(t/200); }
requestAnimationFrame(loop);
})();
