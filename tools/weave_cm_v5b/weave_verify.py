"""CubeMind v5b (22 Nov 2026, Danny 20:56): watch the Weave LCDM-parts fit results as they arrive (PC runs + cloud copies), store them as
EVIDENCE, and queue them for CubeMind to RE-DERIVE blind (step_derive grades it against the tools below). Never deletes anything.
Tools (weave_tools.TOOLS): weave_verdict {"chi2_W":..,"chi2_L":..} -> dchi2 + locked D2132 verdict code; weave_wtoday {"ui":..} -> w0 today."""
import json, os, glob, pathlib, time
HERE = pathlib.Path(__file__).resolve().parents[4] if 'aegis_bundle' in __file__ else pathlib.Path('.')
WATCH = [os.environ.get('WEAVE_PC_RESULTS', r'C:\Users\Danny\ufe_data\weave_pc\results')]
CODE = {0: 'PREFERRED (< -2)', 1: 'CONSISTENT (<= +2)', 2: 'MILD TENSION (<= +6)', 3: 'DISFAVOURED (> +6)'}
def weave_verdict(a):
    d = float(a['chi2_W']) - float(a['chi2_L'])
    c = 0 if d < -2 else 1 if d <= 2 else 2 if d <= 6 else 3
    return {'dchi2': d, 'verdict_code': c, 'verdict': CODE[c], 'rule': 'D2132 locked rule (W vs L, same free-parameter count)'}
def weave_wtoday(a):
    import weave_engine as W
    r = W.run({'mode': 'background', 'ui': float(a['ui'])})
    if 'error' in r: return r
    return {'w0': r['w_thread(z)']['0'], 'H0_engine': r['H0']}
def weave_tally(dst):
    """D2153 locked rule: one entry per W/L pair on the same likelihood set; count per D2132 class; never sum dchi2 across entries."""
    dst = pathlib.Path(dst); R = {}
    for p in glob.glob(str(dst / 'pr4_*.json')):
        try: R[os.path.basename(p)[4:-5]] = json.load(open(p))
        except Exception: pass
    entries = []
    for tag, d in sorted(R.items()):
        if not tag.startswith('W_') or ('L_' + tag[2:]) not in R: continue
        rest = tag[2:]; v = weave_verdict({'chi2_W': d['chi2_eff'], 'chi2_L': R['L_' + rest]['chi2_eff']})
        entries.append({'set': rest, 'headline': rest == 'desdovekie', 'dchi2': round(v['dchi2'], 2), 'verdict': v['verdict'],
                        'H0_W': d.get('point', {}).get('H0'), 'u_i': d.get('point', {}).get('rt_ui')})
    counts = {c: sum(e['verdict'] == c for e in entries) for c in CODE.values()}
    out = {'rule': 'PREREG_D2153 (D2132 classes; dchi2 not summed across entries: shared data)', 'updated': time.strftime('%Y-%m-%d %H:%M'),
           'entries': entries, 'counts': counts, 'n_entries': len(entries)}
    (dst / 'WEAVE_TALLY.json').write_text(json.dumps(out, indent=1))
    return out
def step(cm_root):
    """Called from the learn loop. Returns a small status dict."""
    cm = pathlib.Path(cm_root); dst = cm / 'weave_data' / 'lcdm'; dst.mkdir(parents=True, exist_ok=True)
    seen_f = dst / '_seen.txt'; seen = set(seen_f.read_text().split()) if seen_f.exists() else set()
    new = []
    for w in WATCH + [str(dst)]:
        for p in glob.glob(os.path.join(w, 'pr4_*.json')):
            try: raw = open(p, 'rb').read(); d = json.loads(raw)
            except Exception: continue
            import hashlib; key = os.path.basename(p) + '@' + hashlib.sha256(raw).hexdigest()[:16]
            if key in seen: continue
            if not os.path.samefile(os.path.dirname(p), dst):
                (dst / os.path.basename(p)).write_bytes(raw)
            new.append((os.path.basename(p), d)); seen.add(key)
    if not new: return {'lcdm_watch': 'no new results'}
    from mindmem.store import Store
    S = Store(str(cm / 'cubemind_memory.jsonl')); q = cm / 'weave_data' / 'calc_queue.jsonl'
    allres = {os.path.basename(p): json.load(open(p)) for p in glob.glob(str(dst / 'pr4_*.json'))}
    qids = set()
    if q.exists():
        for _l in q.read_text(encoding='utf-8').splitlines():
            try: qids.add(json.loads(_l)['id'])
            except Exception: pass
    class _Q:
        def __init__(s, f): s.f = f
        def write(s, line):
            i = json.loads(line)['id']
            if i not in qids: qids.add(i); s.f.write(line)
    with open(q, 'a', encoding='utf-8') as _fq:
        fq = _Q(_fq)
        for name, d in new:
            pt = d.get('point', {}); txt = (f"WEAVE FIT RESULT {name}: model {d.get('model')} SN {d.get('sn')} chi2_eff {d.get('chi2_eff'):.2f} "
                                         f"H0 {pt.get('H0', float('nan')):.2f}" + (f" u_i {pt['rt_ui']:.4g}" if 'rt_ui' in pt else ''))
            S.add(txt, 'weave_pc_runs', kind='tool_result', tier='EVIDENCE', topic='weave_lcdm', importance=4)
            if 'rt_ui' in pt:
                fq.write(json.dumps({'id': 'wtoday_' + name, 'task': 'The Weave reverse thread V = V_L(1 - 7.30 e^(-2.83 phi)) starts at u_i = A e^(-beta phi_i) with inputs {x}. Estimate the thread equation of state w today (w is between -1 and 0).',
                                     'tool': 'weave_wtoday', 'key': 'w0', 'tol': 0.05, 'args': {'ui': pt['rt_ui']}}) + '\n')
            tag = name.replace('pr4_', '').replace('.json', '')
            m, rest = tag.split('_', 1)
            other = ('pr4_L_' if m == 'W' else 'pr4_W_') + rest + '.json'
            if m in ('W', 'L') and other in allres and ('verdict_' + rest) not in qids:
                W_ = d if m == 'W' else allres[other]; L_ = allres[other] if m == 'W' else d
                args = {'chi2_W': W_['chi2_eff'], 'chi2_L': L_['chi2_eff']}
                v = weave_verdict(args)
                S.add(f"WEAVE VERDICT {rest}: dchi2(W-L) = {v['dchi2']:+.2f} -> {v['verdict']} (computed by weave_verdict)", 'weave_pc_runs',
                      kind='tool_result', tier='EVIDENCE', topic='weave_lcdm', importance=5)
                fq.write(json.dumps({'id': 'verdict_' + rest, 'task': 'Given Weave and LCDM effective chi-squares {x}, compute dchi2 = chi2_W - chi2_L (same number of free parameters).',
                                     'tool': 'weave_verdict', 'key': 'dchi2', 'tol': 0.001, 'args': args}) + '\n')
    seen_f.write_text('\n'.join(sorted(seen)))
    t = weave_tally(dst)
    S.add('WEAVE TALLY (D2153): ' + ', '.join(f"{e['set']} {e['dchi2']:+.2f} {e['verdict']}" for e in t['entries']) + ' | counts ' + json.dumps(t['counts']),
          'weave_pc_runs', kind='tool_result', tier='EVIDENCE', topic='weave_lcdm', importance=5)
    return {'lcdm_watch': f'{len(new)} new result(s) stored and queued for re-derivation', 'tally': t['counts']}
