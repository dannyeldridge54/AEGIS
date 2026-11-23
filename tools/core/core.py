"""AEGIS Core (PREREG_CORE1): one door for every AEGIS tool.
Every tool gets one self-description (MCP-style: name, title, field, description, inputSchema with x-unit, limits, lock, status, cost)
and one call path: validate -> content-hash cache -> worker process with timeout -> output check -> MCP-shaped result -> provenance
ledger (JSONL). Backends: the CubeMind registry (aegis_tools.registry, subprocess worker) and direct module adapters (adapters.py).
Usage:  python core.py list | status | call <tool> '<json args>' | board"""
import hashlib, json, math, os, pathlib, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
AEGIS = pathlib.Path(os.environ.get('AEGIS_DIR') or next((p for p in [HERE.parent.parent, HERE.parent / 'aegis_tools' / 'aegis_bundle',
                     pathlib.Path.home() / 'aegis'] if (p / 'tools').is_dir()), HERE.parent.parent))
os.environ.setdefault('AEGIS_DIR', str(AEGIS))
from aegis_tools import registry as R
import adapters as AD
STATE = pathlib.Path(os.environ.get('AEGIS_CORE_STATE', HERE / 'state')); STATE.mkdir(parents=True, exist_ok=True)
LEDGER, CACHE = STATE / 'ledger.jsonl', STATE / 'cache'; CACHE.mkdir(exist_ok=True)

# ------------------------------------------------------------------ self-descriptions
FIELDS = [('chronos_', 'nuclear (Chronos)'), ('lhc_', 'collider (CERN+1)'), ('janus_lt', 'late universe (Janus-LT)'), ('janus_', 'inflation (Janus)'),
          ('kaluza_', 'extra dimensions (KALUZA)'), ('serapis_', 'SERAPIS inflation'), ('string_meter', 'string theory'), ('nstar_match', 'SERAPIS inflation'),
          ('lock_', 'method (LOCKBENCH)'), ('lattice_', 'lattices'), ('hyperion_', 'astrophysics (Hyperion)'), ('evidence_', 'the Weave'), ('weave_', 'the Weave'),
          ('zurvan_', 'SUSY naturalness (Zurvan)'), ('aion_', 'neutrino mass (Aion)')]
UNIT_HINTS = [('_GeV', 'GeV'), ('_MeV', 'MeV'), ('_eV', 'eV'), ('_kms', 'km/s'), ('_TeV', 'TeV'), ('_Msun', 'M_sun'), ('_erg_s', 'erg/s'), ('GBq', 'GBq'),
              ('MBq', 'MBq'), ('hours', 'h'), ('days', 'd'), ('years', 'y'), ('grams', 'g'), ('period_s', 's'), ('lumi', 'fb^-1'), ('sqrts', 'TeV'),
              ('_kpc', 'kpc'), ('rho_sun', 'GeV/cm^3'), ('r_sun', 'kpc'), ('T_R', 'GeV')]
REQUIRED = {  # curated where the tool code makes a field mandatory (others are optional; the example shows typical use)
    'chronos_half_life': ['nuclide'], 'chronos_activity_after': ['nuclide', 'A0', 'hours'], 'chronos_make_now': ['nuclide', 'A_needed', 'hours'],
    'chronos_generator': ['parent'], 'chronos_release_age': ['pair', 'ratio_now', 'ratio_at_release'], 'chronos_ac225': ['Ac225_MBq_at_purification'],
    'chronos_pu_age': ['am_over_pu_activity'], 'chronos_tritium': ['grams', 'years'], 'chronos_decay_heat': ['days_operated', 'hours_after_shutdown'],
    'chronos_supernova': ['M_Ni_Msun', 'days'], 'chronos_nickel_mass': ['L_erg_s', 'days'], 'chronos_wd_merger': ['period_s', 'm1', 'm2'],
    'chronos_kilonova': ['M_ej_Msun', 'days'], 'chronos_star_age': ['pair', 'log_eps_observed', 'production_ratio']}

def _jtype(v):
    if isinstance(v, bool): return 'boolean'
    if isinstance(v, int): return 'integer'
    if isinstance(v, float): return 'number'
    if isinstance(v, str): return 'string'
    if isinstance(v, list): return 'array'
    if isinstance(v, dict): return 'object'
    return 'null'

def _schema_from_example(name, ex):
    props = {}
    for k, v in ex.items():
        t = _jtype(v); p = {'type': ['number', 'integer'] if t in ('number', 'integer') else t}
        u = next((u for h, u in UNIT_HINTS if h in k), None)
        if u: p['x-unit'] = u
        props[k] = p
    return {'type': 'object', 'properties': props, 'required': REQUIRED.get(name, []), 'additionalProperties': True}

def _field(name): return next((f for p, f in FIELDS if name.startswith(p)), 'other')

_LOCKS = None
def _locks_for(name):
    global _LOCKS
    if _LOCKS is None:
        d = AEGIS / 'field_tests' / 'rules'; _LOCKS = {f.name: f.read_text(errors='ignore') for f in d.glob('PREREG_*.md')} if d.is_dir() else {}
    fam = name.split('_')[0]
    hits = [f for f, t in _LOCKS.items() if name in t]
    return sorted(hits)[:4] or sorted(f for f, t in _LOCKS.items() if f.lower().find(fam) >= 0)[:3]

EXAMPLE_FIX = {  # DEV-2: registry examples that were placeholders or doc strings
    'lock_verdict': {'lock_text': '```claims\n- {id: C1, quantity: x, op: "<=", value: 1}\n```', 'results': {'x': 0.5}},
    'lhc_dt_limit': {'lumi': 136, 'sqrts': '13', 'search': 'ATLAS_136', 'boost': 'fixed', 'band': False}}
_SPECS = None
def specs():
    global _SPECS   # DEV-1: built once per process
    if _SPECS is None: _SPECS = _build_specs()
    return _SPECS

def _build_specs():
    out = {}
    for name, (ex, timeout) in R.TOOLS.items():
        try: exd = EXAMPLE_FIX.get(name) or json.loads(ex)
        except Exception: exd = {}
        doc = next((l.strip() for l in (R.__doc__ or '').splitlines() if l.strip().startswith(name + ' ')), '')
        out[name] = dict(name=name, title=name.replace('_', ' '), field=_field(name), backend='registry', example=exd, timeout_s=timeout,
                         cost='fast' if timeout <= 10 else 'slow', description=doc, inputSchema=_schema_from_example(name, exd), locks=_locks_for(name))
    for name, a in AD.ADAPTERS.items():
        out[name] = dict(name=name, title=a['title'], field=_field(name), backend='module', example=a['example'], timeout_s=a['timeout'],
                         cost='fast' if a['timeout'] <= 10 else 'slow', description=a['description'], inputSchema=a['inputSchema'],
                         limits=a.get('limits', ''), locks=a.get('locks', []))
    return out

# ------------------------------------------------------------------ validation (JSON Schema subset: types, required)
_PY = {'number': (int, float), 'integer': (int,), 'string': (str,), 'array': (list,), 'object': (dict,), 'boolean': (bool,)}
def validate(schema, args):
    if not isinstance(args, dict): return ['arguments must be a JSON object']
    errs = [f'missing required field "{k}"' for k in schema.get('required', []) if k not in args]
    for k, v in args.items():
        p = schema.get('properties', {}).get(k)
        if not p: continue
        ts = p['type'] if isinstance(p['type'], list) else [p['type']]
        ok = any(isinstance(v, _PY[t]) and not (t in ('number', 'integer') and isinstance(v, bool)) for t in ts if t in _PY)
        if not ok: errs.append(f'field "{k}" should be {" or ".join(ts)}, got {_jtype(v)}')
    return errs

# ------------------------------------------------------------------ content-hash cache + provenance
_CODE = None
def code_hash():
    """Content hash of every .py under AEGIS/tools + the core (Consist/AiiDA style: contents, not mtimes)."""
    global _CODE
    if _CODE is None:
        h = hashlib.sha256()
        for root in [AEGIS / 'tools', HERE]:
            for f in sorted(root.rglob('*.py')):
                if 'state' in f.parts or '__pycache__' in f.parts: continue
                try: h.update(str(f.relative_to(root)).encode()); h.update(f.read_bytes())
                except OSError: pass
        _CODE = h.hexdigest()[:16]
    return _CODE

def _canon(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), default=str)
def _h(x): return hashlib.sha256(_canon(x).encode()).hexdigest()[:16]

def _nonfinite(x, path=''):
    if isinstance(x, float) and not math.isfinite(x): return [path or '.']
    if isinstance(x, dict): return [q for k, v in x.items() for q in _nonfinite(v, f'{path}.{k}')]
    if isinstance(x, list): return [q for i, v in enumerate(x[:2000]) for q in _nonfinite(v, f'{path}[{i}]')]
    return []

_MEM = False
def _memory():
    """DEV-3: CubeMind's own memory store (mindmem), if this core sits inside a CubeMind folder."""
    global _MEM
    if _MEM is False:
        _MEM = None
        for root in [HERE.parent, pathlib.Path(os.environ.get('CUBEMIND_DIR', HERE.parent))]:
            if (root / 'mindmem' / 'store.py').is_file():
                try:
                    sys.path.insert(0, str(root)); from mindmem.store import Store
                    _MEM = Store(str(root / 'cubemind_memory.jsonl')); break
                except Exception: _MEM = None
    return _MEM

def learn(name, field, args, out, is_err, rec_id):
    m = _memory()
    if m is None: return False
    try:
        body = _canon({k: v for k, v in out.items() if k not in ('chart',)})[:700] if isinstance(out, dict) else str(out)[:700]
        m.add(text=f'AEGIS Core {name} ({field}) inputs {_canon(args)[:300]} -> {"ERROR " if is_err else ""}{body} [ledger {rec_id}]',
              source='aegis_core', kind='error' if is_err else 'result', tier='HYPOTHESIS' if is_err else 'EVIDENCE', topic=field, importance=2 if is_err else 3)
        return True
    except Exception: return False

def _ledger(rec):
    with open(LEDGER, 'a', encoding='utf-8') as f: f.write(_canon(rec) + '\n')

def call(name, args, parents=()):
    """One door. Returns {structuredContent, isError, content, provenance}."""
    t0 = time.time(); S = specs().get(name)
    def done(out, is_err, cached=False, source=None):
        rec = dict(id=_h([name, args, time.time_ns()]), tool=name, args=args, args_hash=_h(args), code_hash=code_hash(),
                   result_hash=_h(out), isError=is_err, cached=cached, source_id=source, parents=list(parents),
                   t=time.strftime('%Y-%m-%dT%H:%M:%S'), seconds=round(time.time() - t0, 4))
        _ledger(rec)
        if not cached: rec['learned'] = learn(name, S['field'] if S else 'other', args, out, is_err, rec['id'])
        msg = out.get('error') if is_err and isinstance(out, dict) else None
        return dict(structuredContent=None if is_err else out, isError=is_err,
                    content=[dict(type='text', text=msg or _canon(out)[:4000])], provenance=rec)
    if S is None: return done({'error': f'unknown tool {name}'}, True)
    errs = validate(S['inputSchema'], args)
    if errs: return done({'error': 'invalid input: ' + '; '.join(errs)}, True)
    key = _h([name, args, code_hash()]); cp = CACHE / f'{name}_{key}.json'
    if cp.exists() and not os.environ.get('AEGIS_NOCACHE'):
        c = json.loads(cp.read_text()); return done(c['out'], False, cached=True, source=c['id'])
    if S['backend'] == 'registry':
        out = R._call_fresh(name, args)
    else:
        out = AD.run(name, args, S['timeout_s'])
    is_err = not isinstance(out, dict) or 'error' in out
    if not is_err:
        bad = _nonfinite(out)
        if bad: out = dict(out, _warnings=[f'non-finite value at {", ".join(bad[:5])}'])
    r = done(out if isinstance(out, dict) else {'error': str(out)}, is_err)
    if not is_err: cp.write_text(_canon(dict(id=r['provenance']['id'], out=out)))
    return r

# ------------------------------------------------------------------ status board
def status():
    S = specs(); last = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding='utf-8').splitlines():
            try: r = json.loads(line); last[r['tool']] = r
            except Exception: pass
    led = (AEGIS / 'tools' / 'gifts' / 'REFEREE_LEDGER.md'); led = led.read_text(errors='ignore') if led.exists() else ''
    rows = []
    for n, s in sorted(S.items(), key=lambda kv: (kv[1]['field'], kv[0])):
        fam = n.split('_')[0]; L = last.get(n)
        rows.append(dict(tool=n, field=s['field'], backend=s['backend'], cost=s['cost'], locks=s['locks'],
                         refereed_auto=fam.lower() in led.lower(), last_run=L and L['t'], last_ok=L and not L['isError'],
                         last_error=L and L['isError'] and L.get('result_hash')))
    return rows

def board_html(rows):
    tr = ''.join(f"<tr><td>{r['field']}</td><td><code>{r['tool']}</code></td><td>{r['backend']}</td><td>{r['cost']}</td>"
                 f"<td>{'<br>'.join(r['locks']) or '&mdash;'}</td><td>{'yes' if r['refereed_auto'] else 'no'}</td>"
                 f"<td class='{'ok' if r['last_ok'] else ('bad' if r['last_run'] else '')}'>{r['last_run'] or 'never'}</td></tr>" for r in rows)
    n_ok = sum(1 for r in rows if r['last_ok']); n_run = sum(1 for r in rows if r['last_run'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>AEGIS Core Board</title><style>
body{{background:#07040f;color:#ece6ff;font:14px Segoe UI,system-ui,sans-serif;padding:20px max(16px,3vw)}}h1{{margin:0}}.s{{color:#a69ccc}}
table{{border-collapse:collapse;width:100%;margin-top:12px}}td,th{{border-bottom:1px solid #2c2147;padding:5px 8px;text-align:left;vertical-align:top}}
th{{color:#b18cff;font-weight:600}}.ok{{color:#7ee787}}.bad{{color:#ff6fa8}}code{{color:#e0b24a}}</style></head><body>
<h1>AEGIS Core</h1><p class="s">{len(rows)} tools behind one door &middot; {n_run} run &middot; {n_ok} last run OK &middot; code {code_hash()} &middot; built {time.strftime('%Y-%m-%d %H:%M')}</p>
<table><tr><th>Field</th><th>Tool</th><th>Backend</th><th>Cost</th><th>Locks</th><th>Refereed (auto)</th><th>Last run</th></tr>{tr}</table></body></html>"""

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'list': print(json.dumps({n: dict(field=s['field'], example=s['example']) for n, s in specs().items()}, indent=1))
    elif cmd == 'call': print(json.dumps(call(sys.argv[2], json.loads(sys.argv[3] if len(sys.argv) > 3 else '{}')), indent=1, default=str)[:6000])
    elif cmd == 'status': print(json.dumps(status(), indent=1, default=str))
    elif cmd == 'board': (STATE / 'board.html').write_text(board_html(status()), encoding='utf-8'); print(STATE / 'board.html')
