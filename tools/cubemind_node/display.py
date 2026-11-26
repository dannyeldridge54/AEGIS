"""CubeMind display: one local page with three views per node (timeline, memory map, live activity). Written by the node; refreshes itself.
Open node1_data/dashboard.html in any browser (or Open_Dashboard.bat). Nodes are listed at the top; more appear as they are added."""
import json, time
from pathlib import Path

def snapshot(node):
    """Everything the page draws, from one node."""
    s = node.state; c = s['counts']; day = s.get('day', {}); m = s['models'].get(node.cfg['models']['processor'], [0, 0])
    sheet = node.web.sheet(); leaves = [r for r in sheet if r['leaf'] and r['records']]
    syn = [dict(a=a, b=b, w=round(w, 2)) for a, b, w in node.web.synapses()[:80]]
    busy = day.get('busy', 0.0) + day.get('idle', 0.0)
    return dict(
        node=node.NODE_NAME, updated=time.strftime('%Y-%m-%d %H:%M:%S'), phase=s.get('phase', {}), cycles=s['cycle'], counts=c,
        today=dict(cycles=day.get('cycles', 0), per_hour=round(3600 * day.get('cycles', 0) / busy) if busy else 0, sources=day.get('sources', {}),
                   similar_links=day.get('similar_links', 0)),
        processor=dict(right=m[0], tested=m[1]), levels=s.get('ring', {}), mapper=s.get('mapper', {}),
        records=node.ix.stats()['records'], kinds=node.ix.stats()['kinds'],
        string=node.string_index(), lanes=node.lanes()[:14],
        neurons=[dict(id=r['neuron'], side=r['side'], layer=r['layer'], records=r['records'], engine=r['engine'], acc=r['accuracy'], balance=r['balance']) for r in leaves],
        synapses=syn, goalposts=node.goalposts(), recent=s['recent'][:20], resources=node.resources(),
        sweep=s.get('sweep', {}), dup_web=s.get('dup_web', 0),
        coder=s.get('coder', {}), code_queue=len(s.get('code_queue', [])), board=node.shared_board(), stage=s.get('stage', 'start'),
        library=node.ix.stats()['kinds'].get('library', 0), allow_install=bool(node.cfg.get('allow_install')), route=s.get('route_last', {}), prog=s.get('prog', {}), **_prog(s),
        refine=len(s.get('refine', [])), doorways={k: v for k, v in s.get('doorways', {}).items() if k != 'recent'}, help=len(s.get('help', [])),
        models=node.cfg['models'], log=_tail(node.home / 'node1.log', 8))

def quick(node, snap):
    """Refresh the live parts (phase, today, counts, recent, log, resources) without touching the database; safe from any thread."""
    s = node.state; day = s.get('day', {}); busy = day.get('busy', 0.0) + day.get('idle', 0.0)
    return dict(snap, updated=time.strftime('%Y-%m-%d %H:%M:%S'), phase=dict(s.get('phase', {})), cycles=s['cycle'], counts=dict(s['counts']),
                today=dict(cycles=day.get('cycles', 0), per_hour=round(3600 * day.get('cycles', 0) / busy) if busy else 0, sources=dict(day.get('sources', {})),
                           similar_links=day.get('similar_links', 0)),
                recent=list(s['recent'][:20]), resources=node.resources(), sweep=dict(s.get('sweep', {})), coder=dict(s.get('coder', {})),
                code_queue=len(s.get('code_queue', [])), stage=s.get('stage', 'start'), refine=len(s.get('refine', [])), help=len(s.get('help', [])),
                doorways={k: v for k, v in s.get('doorways', {}).items() if k != 'recent'}, route=s.get('route_last', {}), prog=dict(s.get('prog', {})), **_prog(s), log=_tail(node.home / 'node1.log', 8))

def _prog(s):
    """The programmer's own space: its actions, success per kind, lessons, checkpoints and your instructions."""
    return dict(prog_n=s.get('prog_n', 0), prog_kinds=s.get('prog_kinds', {}), prog_log=list(s.get('prog_log', [])[:12]), prog_lessons=list(s.get('prog_lessons', [])[:6]),
                prog_cp=[dict(at=c['at'], t=c['t'], next=c.get('next', '')) for c in s.get('prog_checkpoints', [])[:4]], prog_next_cp=s.get('prog_next_cp', 25),
                instructions=list(s.get('instructions', [])[:8]), wants=list(s.get('wants', [])[:8]), repos=list(s.get('repos_seen', [])[-8:]))

def _tail(p, n):
    try: return p.read_text(encoding='utf-8', errors='ignore').splitlines()[-n:]
    except OSError: return []

PAGE = r"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="4"><title>CubeMind</title>
<style>
:root{--bg:#0f141a;--panel:#161d25;--ink:#e3e9ef;--muted:#8d9aa7;--line:#26313d;--accent:#5fb0d8;--ok:#62c08a;--warn:#e2b257;--bad:#e27d7d;--q:#a68be0;
--mono:ui-monospace,"Cascadia Mono",Consolas,monospace;--sans:"Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 var(--sans)}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--line)}
h1{font-size:18px;margin:0}.muted{color:var(--muted)}.mono{font-family:var(--mono)}
nav button{background:none;border:1px solid var(--line);color:var(--ink);border-radius:6px;padding:4px 10px;margin-right:6px;cursor:pointer}
nav button.on{border-color:var(--accent);color:var(--accent)}
main{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:14px;padding:14px 18px}
section{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}
section.wide{grid-column:1/-1}h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.kpis{display:flex;flex-wrap:wrap;gap:8px}.kpi{border:1px solid var(--line);border-radius:8px;padding:6px 10px}.kpi b{display:block;font-size:18px}
.phase{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}.ph{border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:12.5px;color:var(--muted)}
.ph.on{border-color:var(--accent);color:var(--bg);background:var(--accent);font-weight:600}
table{width:100%;border-collapse:collapse;font-size:12.5px}td,th{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:500}.PASS,.MET{color:var(--ok)}.UNCLEAR,.NOT{color:var(--warn)}.MISS,.VOID{color:var(--bad)}
.scroll{overflow-x:auto}svg{width:100%;height:auto;display:block}svg text{fill:var(--muted);font:11px var(--sans)}
</style>
<header><h1>CubeMind <span class="muted" id="who"></span></h1><span class="muted mono" id="upd"></span><nav id="nodes"></nav></header>
<main>
 <section class="wide"><h2>Now</h2><div id="now"></div>
   <div id="pcards"></div></section>
 <section class="wide"><h2>Timeline: the single string</h2><div class="scroll" id="tl"></div><p class="muted" id="tlnote"></p></section>
 <section><h2>Memory map: neurons and connections</h2><div id="map"></div><p class="muted">Left to right: early universe, mathematics, late universe. Top to bottom: centre outward through the nine layers. Size = records; lines = links.</p></section>
 <section><h2>Categories: lanes by geometric address</h2><div class="scroll" id="lanes"></div></section>
 <section><h2>Goalposts</h2><div id="goals"></div></section>
 <section><h2>Recent results</h2><div class="scroll" id="recent"></div></section>
</main>
<script>
const NODES = __DATA__;
const esc = s => String(s ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
let pick = (location.hash || '').slice(1); if (!NODES[pick]) pick = Object.keys(NODES)[0];
function draw(){
 const D = NODES[pick]; document.getElementById('who').textContent = '· ' + D.node; document.getElementById('upd').textContent = 'updated ' + D.updated + ' · refreshes every 4 s';
 document.getElementById('nodes').innerHTML = Object.keys(NODES).map(k => `<button class="${k===pick?'on':''}" onclick="location.hash='${k}';pick='${k}';draw()">${esc(k)}</button>`).join('');
 // NOW
 const steps = ['retrieving','mapping','processing','refereeing','filing','waiting'], ph = D.phase || {};
 const ago = ph.since ? Math.round(Date.now()/1000 - ph.since) : null;
 const _pc = (D.board_cards||[]); document.getElementById('pcards').innerHTML = _pc.length ? '<h2 style="margin-top:12px">From the programmer</h2>' + _pc.map(c => `<div class="kpi" style="display:block;margin:4px 0;border-left:3px solid var(--accent)"><b>${esc(c.title)}</b> <span class="muted mono">${esc(c.t)} · ${esc(c.status)}</span><div>${esc(c.body)}</div></div>`).join('') : '';
  document.getElementById('now').innerHTML = `<div class="phase">${['local','web','math'].map((x,k) => `<span class="ph ${x===D.stage?'on':''}">Stage ${k+1}: ${x}</span>`).join('')}</div><div class="phase">${steps.map(s => `<span class="ph ${s===ph.name?'on':''}">${s}</span>`).join('')}</div>
  <p>${esc(ph.detail || 'starting')} ${ago!==null ? `<span class="muted">(${ago} s)</span>` : ''}</p>
  <div class="kpis">${[['Cycles', D.cycles],['Today', D.today.cycles],['Per hour', D.today.per_hour],['Pass', D.counts.PASS||0],['Unclear', D.counts.UNCLEAR||0],['Miss', D.counts.MISS||0],
   ['Processor right', D.processor.tested ? D.processor.right + '/' + D.processor.tested : '-'],['Records', D.records],['Neurons', D.neurons.length],['Links by meaning', D.today.similar_links]]
   .map(([k,v]) => `<div class="kpi"><span class="muted">${k}</span><b class="mono">${esc(v)}</b></div>`).join('')}</div>
  <p class="muted">Sources today: ${Object.entries(D.today.sources).map(([k,v]) => esc(k)+' '+v).join(' · ') || 'none yet'}</p>
  ${D.sweep && D.sweep.total ? `<div class="kpis" style="margin-top:8px">${[['Files found', D.sweep.total],['Handled', D.sweep.unique + D.sweep.duplicates + D.sweep.skipped],['New, catalogued', D.sweep.catalogued],['Copies marked done', D.sweep.duplicates],['Web repeats skipped', D.dup_web]].map(([k,v]) => `<div class="kpi"><span class="muted">${k}</span><b class="mono">${v}</b></div>`).join('')}</div><p class="muted mono" style="overflow-wrap:anywhere">${esc(D.sweep.current)}</p>` : ''}
  ${D.coder && D.coder.seen != null ? `<p class="muted">Code cartographer: ${D.coder.addressed}/${D.coder.seen} modules addressed · ${D.coder.pathways} pathways · ${D.code_queue} waiting</p>` : (D.code_queue ? `<p class="muted">Code cartographer: ${D.code_queue} modules waiting</p>` : '')}
  <p class="muted">Mapper queue: ${D.refine||0} files · help requests waiting: ${D.help||0} · programmer doorways: ${(D.doorways||{}).opened||0} opened, ${(D.doorways||{}).placed||0} data sets placed on the string${D.sweep && D.sweep.auto != null ? ` · placed by code: ${D.sweep.auto}, unrelated: ${D.sweep.unrelated||0}` : ''}</p>
  ${D.prog ? `<p class="muted">Programmer: learning its job — ${D.prog.hints||0} hints from ${D.prog.searches||0} searches · ${D.prog.ideas||0} improvement ideas (in IMPROVEMENTS.md, not applied) · ${D.prog.routes||0} Node 2 route versions</p>` : ''}
  ${D.route && D.route.lane ? `<details open><summary><b>Node 2 route (proposed):</b> ${esc(D.route.sphere)} from lane ${esc(D.route.lane)}</summary><p>${esc(D.route.why)}</p><ol>${(D.route.steps||[]).map(x => `<li>${esc(x)}</li>`).join('')}</ol><p class="muted">Uses: ${esc((D.route.uses||[]).join(', '))}</p></details>` : ''}
  <details open><summary><b>The node network</b> <span class="muted">(switchboard — the programmer turns nodes on as the field fills)</span></summary>
   <div class="kpis">${Object.entries((D.network||{}).nodes||{}).map(([id,n]) => `<div class="kpi"><span class="muted">${esc(n.role)}</span><b>${n.on?'<span style="color:#2f7a4b">ON</span>':'off'}</b><span class="muted mono" style="font-size:11px">${esc(n.note||'')}</span></div>`).join('') || '<span class="muted">registering…</span>'}</div>
   ${D.mind && D.mind.encoded != null ? `<div class="kpi" style="display:block;border-left:3px solid var(--accent);margin:6px 0"><b>Mind — the subconscious (the model we are building)</b><div class="muted">Consciousness now: the programmer runs things. Subconscious: this model learns in the background until it is ready to take the centre.</div><div style="margin-top:4px">Learned <b>${D.mind.encoded}</b> records · ${D.mind.lanes||0} lanes · ${D.mind.assoc||0} associations · readiness <b>${Math.round(100*(D.mind.readiness||0))}%</b></div><div style="background:var(--line);border-radius:6px;height:8px;margin-top:4px"><div style="background:var(--accent);height:8px;border-radius:6px;width:${Math.round(100*(D.mind.readiness||0))}%"></div></div></div>` : ''}
   ${D.health && D.health.last ? `<p class="muted">Maintenance: ${(D.health.diagnoses||[]).length ? '⚠ ' + D.health.diagnoses.map(x => esc(x.alert)+' x'+x.count).join(', ') : '✓ healthy'} <span class="mono">(checked ${esc(D.health.last)})</span></p>` : ''}
   ${((D.network||{}).signals||[]).length ? `<p class="muted">Recent signals: ${(D.network.signals||[]).slice(0,5).map(x => `${esc(x.frm)}→${esc(x.to||'all')}: <b>${esc(x.kind)}</b>`).join(' · ')}</p>` : ''}
  </details>
  <details open><summary><b>Programmer's own space</b> · ${D.prog_n||0} actions filed · next checkpoint at ${D.prog_next_cp||25}</summary>
   <p class="muted">${Object.entries(D.prog_kinds||{}).map(([k,v]) => `${esc(k)} ${v.good}/${v.done}`).join(' · ') || 'no actions yet'}</p>
   ${(D.prog_lessons||[]).length ? `<p><b>Lessons it wrote for itself</b></p><ul>${D.prog_lessons.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}
   ${(D.prog_cp||[]).length ? `<p class="muted">Checkpoints: ${D.prog_cp.map(c => `${c.at} actions (${esc(c.t)})`).join(' · ')}</p>` : ''}
   <p><b>Your instructions</b> <span class="muted">(write one per line in node1\\INSTRUCTIONS.txt; work lands in node1_data\\workbench, saved and syntax-checked, never run)</span></p>
   ${(D.instructions||[]).length ? `<ul>${D.instructions.map(x => `<li>${esc(x.t)} · ${esc(x.task)} → <b>${esc(x.outcome)}</b> <span class="muted mono">${esc(x.folder)}</span></li>`).join('')}</ul>` : '<p class="muted">none yet</p>'}
   <p><b>Recent actions</b></p><ul class="mono" style="font-size:12px">${(D.prog_log||[]).map(a => `<li>${esc(a.t)} ${esc(a.kind)} · ${esc(a.target)} → ${esc(a.outcome)}</li>`).join('')}</ul>
   <p class="muted">Learning from GitHub: ${D.library||0} library files · repos: ${(D.repos||[]).map(esc).join(', ')||'none yet'}</p>
   ${(D.wants||[]).length ? `<p><b>Tools it wants</b> <span class="muted">(installs are ${D.allow_install?'<b>ON</b> — you approved':'<b>OFF</b> — set allow_install:true in node1_config.json to let it install; listed in WANTS.md)'}</span></p><ul>${D.wants.map(w => `<li>${esc(w.what)} — ${esc(w.why)} ${w.done?'<b>'+esc(w.result||'done')+'</b>':'<span class="muted">waiting</span>'}</li>`).join('')}</ul>` : ''}
  </details>
  <details><summary class="muted">Shared board (what every model sees)</summary><pre class="mono" style="white-space:pre-wrap;font-size:12px">${esc(D.board)}</pre></details>
  <p class="muted">Machine: ${['cpu','ram','gpu_busy','gpu_mem'].filter(k => D.resources[k] != null).map(k => ({cpu:'CPU',ram:'RAM',gpu_busy:'GPU working',gpu_mem:'GPU memory (full is normal)'})[k] + ' ' + Math.round(D.resources[k]) + '%').join(' · ') || 'install tools to see load'}</p>
  <p class="muted">Models: ${Object.entries(D.models).map(([k,v]) => esc(k) + ' ' + esc(v)).join(' · ')}</p>
  <details ${D.log.length ? 'open' : ''}><summary class="muted">Latest log lines</summary><pre class="mono" style="white-space:pre-wrap;font-size:12px">${D.log.map(esc).join('\n') || '(empty)'}</pre></details>`;
 // TIMELINE
 const W = 1000, H = 150, x0 = 40, x1 = 980, lo = -10, hi = 61, X = v => x0 + (v - lo) / (hi - lo) * (x1 - x0);
 const maxr = Math.max(1, ...D.string.string.map(e => e.records));
 let g = `<svg viewBox="0 0 ${W} ${H+8}" role="img" aria-label="Records along cosmic time">`;
 g += `<rect x="${x0-14}" y="22" width="${x1-x0+28}" height="88" rx="44" fill="none" stroke="var(--warn)" stroke-dasharray="4 4"/>`;
 g += `<text x="${x0}" y="16">wrapper: limits that hold at every time · ${D.string.wrapper} records</text>`;
 g += `<rect x="${X(lo)}" y="58" width="${X(0)-X(lo)}" height="8" fill="var(--q)" opacity=".35"/><line x1="${X(0)}" y1="40" x2="${X(0)}" y2="90" stroke="var(--ink)"/>`;
 g += `<line x1="${x0}" y1="62" x2="${x1}" y2="62" stroke="var(--line)" stroke-width="2"/><text x="${X(0)+4}" y="38">centre: Planck time</text>`;
 D.string.string.forEach((e, i) => { const cx = X((e.from_ + e.to) / 2), r = 4 + 16 * Math.sqrt(e.records / maxr);
   g += `<line x1="${X(e.from_)}" y1="62" x2="${X(e.to)}" y2="62" stroke="${e.epoch==='quantum'?'var(--q)':'var(--accent)'}" stroke-width="4"/>`;
   g += `<circle cx="${cx}" cy="62" r="${e.records?r:0}" fill="${e.epoch==='quantum'?'var(--q)':'var(--accent)'}" opacity=".75"><title>${esc(e.note)}</title></circle>`;
   g += `<text x="${cx}" y="${i >= 3 ? 110 + (i % 2) * 14 : 118}" text-anchor="${e.epoch==='late'?'end':'middle'}">${esc(e.epoch)} ${e.records}</text>`; });
 [0,10,20,30,40,50,60].forEach(v => g += `<text x="${X(v)}" y="152" text-anchor="middle">${v}</text>`);
 document.getElementById('tl').innerHTML = g + `</svg>`;
 document.getElementById('tlnote').textContent = 'Axis: powers of ten of the Planck time (5.4e-44 s). Today is about 60.9. Left of the centre is the quantum side: speculative, not tested physics. Unplaced: ' + D.string.unplaced + '.';
 // MAP
 const MW = 460, MH = 320, mx = s => 30 + (s + 1) / 2 * (MW - 60), my = l => 24 + l * (MH - 48);
 const pos = {}; D.neurons.forEach(n => { const j = ((n.id * 37) % 17 - 8) * 2; pos[n.id] = [mx(n.side) + j, my(n.layer) + ((n.id * 13) % 11 - 5) * 2]; });
 const maxw = Math.max(1, ...D.synapses.map(s => s.w)), maxn = Math.max(1, ...D.neurons.map(n => n.records));
 let m = `<svg viewBox="0 0 ${MW} ${MH}" role="img" aria-label="Neurons and links">`;
 ['early','maths','late'].forEach((t,i) => m += `<text x="${30 + i * (MW-60)/2}" y="14" text-anchor="middle">${t}</text>`);
 D.synapses.forEach(s => { if (pos[s.a] && pos[s.b]) m += `<line x1="${pos[s.a][0]}" y1="${pos[s.a][1]}" x2="${pos[s.b][0]}" y2="${pos[s.b][1]}" stroke="var(--accent)" stroke-opacity="${.15 + .7 * s.w / maxw}" stroke-width="${1 + 2 * s.w / maxw}"/>`; });
 D.neurons.forEach(n => { const [x,y] = pos[n.id], r = 4 + 12 * Math.sqrt(n.records / maxn), col = n.acc == null ? 'var(--muted)' : n.acc >= .8 ? 'var(--ok)' : n.acc >= .5 ? 'var(--warn)' : 'var(--bad)';
   m += `<circle cx="${x}" cy="${y}" r="${r}" fill="${col}" opacity=".85"><title>neuron ${n.id} · ${esc(n.engine)} · ${n.records} records · accuracy ${n.acc==null?'-':Math.round(n.acc*100)+'%'} · scale balance ${n.balance}</title></circle>`; });
 document.getElementById('map').innerHTML = m + `</svg>`;
 // LANES
 document.getElementById('lanes').innerHTML = `<table><tr><th>Ring</th><th>Anchor</th><th>Shape</th><th>Weight</th><th>Records</th><th>By layer</th></tr>` +
  D.lanes.map(l => `<tr><td>${esc(l.ring)}</td><td>${esc(l.anchor)}</td><td>${esc(l.shape)}</td><td>${esc(l.weight)}</td><td class="mono">${l.total}</td><td>${Object.entries(l.layers).map(([k,v]) => esc(k)+' '+v).join(', ')}</td></tr>`).join('') + `</table>`;
 // GOALS
 document.getElementById('goals').innerHTML = `<table>` + D.goalposts.map(g => `<tr><td>${esc(g.part)}<br><span class="muted">${esc(g.goal)}</span></td><td class="mono">${esc(g.now)}</td><td class="${g.met?'MET':'NOT'}">${g.met?'MET':'NOT YET'}</td></tr>`).join('') + `</table>`;
 // RECENT
 document.getElementById('recent').innerHTML = `<table><tr><th>Time</th><th>Subject</th><th>Calculation</th><th>Verdict</th><th>Referee</th></tr>` +
  D.recent.map(r => `<tr><td class="mono">${esc(r.t.slice(11))}</td><td>${esc(r.subject)}</td><td>${esc(r.tool)} · level ${r.ring}</td><td class="${r.verdict}">${r.verdict}</td><td class="muted">${esc(r.referee)}</td></tr>`).join('') + `</table>`;
}
draw();
</script></html>"""

def render(path, nodes):
    """nodes: {name: snapshot}. Writes the page atomically."""
    data = json.dumps(nodes, default=str).replace('</', '<\\/')
    p = Path(path); tmp = p.with_suffix('.tmp'); tmp.write_text(PAGE.replace('__DATA__', data), encoding='utf-8'); tmp.replace(p)
