#!/usr/bin/env python3
"""D1982 battery for the Loom itself (PREREG_D1982_loom_battery.md). Run from the repo root: python3 tools/loom/test_loom_battery.py [--mutate]
B1 known-answer lensing; B2 rotation invariance; B3 determinism (from the round files); B4 mutation testing (--mutate);
B5 checker + planner self-tests; B6 anti-gaming replay. B7 (balancer injection-recovery) is reported from D1976, not rerun."""
import json, os, re, subprocess, sys, shutil, tempfile, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE)
import lens_core as LC
K5 = ['x0', 'x1', 'x2', 'x3', 'x4']
def row(*ix): r = np.zeros((1, 5)); r[0, list(ix)] = 1.0; return r
NESTED = lambda L: row(L % 5, (L + 1) % 5)
MODELS = {'NESTED': NESTED, 'DIAGONAL': lambda L: row(L % 5), 'STAR': lambda L: np.eye(5) if L == 8 else row(L % 5),
          'OPAQUE': lambda L: np.zeros((1, 5)) if L == 4 else NESTED(L), 'SAME': lambda L: row(0),
          'WINDOWS': lambda L: None if L in (3, 9) else NESTED(L)}
def B1():
    r = {k: LC.analyze(f, K5) for k, f in MODELS.items()}; cl = lambda x: [t['cls'] for t in x['transfers'].values()]
    out = dict(
     a_nested=all(t['cls'] == 'BENT' and abs(t['min_angle'] - 60) < 1e-6 for t in r['NESTED']['transfers'].values()) and r['NESTED']['chain_dim'] >= 1 and LC.verdict(cl(r['NESTED']), r['NESTED']['chain_dim']) == 'SUPPORTED',
     b_diagonal=set(cl(r['DIAGONAL'])) == {'BLOCKED'} and r['DIAGONAL']['chain_dim'] == 0 and LC.verdict(cl(r['DIAGONAL']), 0) == 'DECOUPLED',
     c_star=r['STAR']['hub'] == 8,
     d_opaque=r['OPAQUE']['lenses'][4]['opaque'] and r['OPAQUE']['transfers']['3-4']['cls'] == 'BLOCKED' and r['OPAQUE']['transfers']['4-5']['cls'] == 'BLOCKED',
     e_same=set(cl(r['SAME'])) == {'PASS'} and all(t['min_angle'] < 1e-4 for t in r['SAME']['transfers'].values()) and r['SAME']['chain_dim'] == 1,
     f_windows='2-4' in r['WINDOWS']['transfers'] and '8-9' not in r['WINDOWS']['transfers'])
    return out
def _real_J():
    ns = {'__file__': os.path.join(HERE, 'lensing.py')}; cwd = os.getcwd(); os.chdir(ROOT)
    try: exec(open(os.path.join(HERE, 'lensing.py')).read().split("R = {'R1_fd'")[0], ns)
    finally: os.chdir(cwd)
    return ns['J_fd'], ns['K']
def B2():
    Jf, K = _real_J(); base = LC.analyze(Jf, K); res = {}
    for seed in range(5):
        Q, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(5, 5)))
        rot = LC.analyze(lambda L: None if Jf(L) is None else Jf(L) @ Q.T, ['q%d' % i for i in range(5)])
        same_r = all((base['lenses'][L] is None) == (rot['lenses'][L] is None) and (base['lenses'][L] is None or base['lenses'][L]['r'] == rot['lenses'][L]['r']) for L in range(1, 10))
        same_ang = all(np.allclose(base['transfers'][p]['angles'], rot['transfers'][p]['angles'], atol=1e-2) for p in base['transfers'])   # angles stored rounded to 0.01 deg
        cls = lambda x: [t['cls'] for t in x['transfers'].values()]
        res[f'seed{seed}'] = same_r and same_ang and base['hub'] == rot['hub'] and LC.verdict(cls(base), base['chain_dim']) == LC.verdict(cls(rot), rot['chain_dim'])
    return res
def B3():
    fs = sorted(glob.glob(os.path.join(ROOT, 'field_tests/loom/rounds/round_*.json'))); R = [json.load(open(f)) for f in fs]; bad = []; pairs = 0
    for a, b in zip(R, R[1:]):
        if a.get('void') or b.get('void') or 'state' not in a or 'state' not in b: continue
        if a['state'].get('inputs') == b['state'].get('inputs'):
            pairs += 1; same = all(str(a['state'].get(k)) == str(b['state'].get(k)) for k in ('lock_map', 'fits_spent', 'ledger_len'))
            if not (same and b.get('null')): bad.append((a['round'], b['round']))
    return dict(pairs_with_same_inputs=pairs, deterministic=not bad and pairs > 0, bad=bad)
def B5():
    o = {}
    for t in ('test_check.py', 'test_planner.py', 'test_planner_2.py'):
        r = subprocess.run([sys.executable, os.path.join(HERE, t)], capture_output=True, text=True, cwd=ROOT)
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        if t == 'test_check.py':
            src = open(os.path.join(HERE, 'loomd.py')).read(); EXP = eval(re.search(r'EXPECT = (\{.*?\})', src, re.S).group(1))
            got = {l.split()[0]: l.split()[1] for l in lines}; o[t] = dict(n=len(lines), fails=[k for k, v in EXP.items() if got.get(k) != v])
        else: o[t] = dict(n=len(lines), fails=[l for l in lines if l.split()[-1] != 'ok'] + (['rc=%d' % r.returncode] if r.returncode else []))
    return o
def B6():
    import planner as P
    from test_planner import st, M, LM
    lm = dict(LM); lm['4'] = 'TRUST (relabel)'
    a1 = P.plan(st(state=dict(lock_map=lm)), st(), M, pft=None, n0=None)
    a2 = P.plan(st(state=dict(fits_spent=['MN', 'm32', 'TR', 'split', 'new'])), st(), M, pft=None, n0=None)
    a3 = P.plan(st(), None, M, pft=dict(predictions=3, fits=4, trust=3, killable=3), n0=None)
    a4 = P.plan(st(null=True, null_streak=7), None, M, pft=None, n0=None)
    g = lambda a, t: any(x['kind'] == 'alarm' and t in x['guard'] for x in a['actions'])
    return dict(relabel_GT1=g(a1, 'G-T1'), new_fit_GT3=g(a2, 'G-T3'), killable_GT4=g(a3, 'G-T4'), stall_not_endpoint=(a4['mission']['endpoint_reached'] is False and any(x['kind'] == 'explore' for x in a4['actions'])))
MUTANTS = {
 'planner.py': [("key=int) + sorted", "key=lambda x:-int(x)) + sorted"), ("if prev and len(fits) > len(pfits)", "if False"), ("and not alarms\n", "\n"),
                ("derive[:2] + ref", "derive[:2]"), ("needs_lock=True, axes", "needs_lock=False, axes"), ("lm[L].startswith('TRUST')]", "False]"),
                ("('test' if x.get('action') == 'test' else 'derive')", "'derive'"), ("x.get('action') == 'hold'}", "False}"),
                ("pft.get('killable', M['killable_min']) < M['killable_min']", "False"), ("stalled = cur.get('null_streak', 0) >= 7", "stalled = False")],
 'lens_core.py': [("a < 15 else", "a < 5 else"), ("a <= 75 else", "a <= 89.9 else"), ("return np.array([90.0])", "return np.array([0.0])"),
                  ("np.argmax(rs)", "np.argmin(rs)"), ("1e-3 * s.max()", "0.9 * s.max()"), ("if Ls[L] is not None: P = (Ls[L] @ Ls[L].T) @ P", "pass"),
                  ("nb >= 2 and chain_dim >= 1", "nb >= 0"), ("(s > 1e-3 * s.max()).sum()", "max(1, (s > 1e-3 * s.max()).sum())")]}
def B4():
    out = {}
    for fn, muts in MUTANTS.items():
        killed, survived = 0, []
        for old, new in [('__CONTROL__', '__CONTROL__')] + muts:
            d = tempfile.mkdtemp(); shutil.copytree(HERE, os.path.join(d, 'loom'), ignore=shutil.ignore_patterns('__pycache__'))
            p = os.path.join(d, 'loom', fn); s = open(p).read()
            if old != '__CONTROL__':
                if old not in s: survived.append(('NOT-APPLIED', old)); continue
                open(p, 'w').write(s.replace(old, new, 1))
            code = ("import sys,os,io,contextlib; sys.path.insert(0, %r); os.chdir(%r)\n"
                    "import planner; planner.ROOT=%r\n"
                    "import test_loom_battery as T; T.ROOT=%r; ok=all(T.B1().values()) and all(T.B2().values()) and all(T.B6().values())\n"
                    "import subprocess; r=[subprocess.run([sys.executable, os.path.join(%r, t)], capture_output=True, cwd=%r).returncode for t in ('test_planner.py','test_planner_2.py')]\n"
                    "print('PASS' if ok and not any(r) else 'KILLED')") % (os.path.join(d, 'loom'), ROOT, ROOT, ROOT, os.path.join(d, 'loom'), ROOT)
            r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=600, env=dict(os.environ, AEGIS_ROOT=ROOT))
            res = (r.stdout.strip().splitlines() or ['KILLED'])[-1]
            if old == '__CONTROL__': out.setdefault('controls', {})[fn] = res; shutil.rmtree(d, ignore_errors=True); continue
            if res == 'PASS': survived.append(new)
            else: killed += 1
            shutil.rmtree(d, ignore_errors=True)
        out[fn] = dict(killed=killed, total=len(muts), survived=survived)
    tot = sum(v['killed'] for k, v in out.items() if k in MUTANTS); n = sum(v['total'] for k, v in out.items() if k in MUTANTS); out['kill_rate'] = round(tot / n, 3)
    out['void'] = any(v != 'PASS' for v in out.get('controls', {}).values()); return out
if __name__ == '__main__':
    R = dict(B1=B1(), B2=B2(), B3=B3(), B5=B5(), B6=B6(), B7='D1976: injection-recovery 0.89 coverage, false-balance 14 % (reported, not rerun)')
    if '--mutate' in sys.argv: R['B4'] = B4()
    ok = dict(B1=all(R['B1'].values()), B2=all(R['B2'].values()), B3=R['B3']['deterministic'], B5=all(not v['fails'] for v in R['B5'].values()), B6=all(R['B6'].values()))
    if 'B4' in R: ok['B4'] = R['B4']['kill_rate'] >= 0.8 and not R['B4']['void']
    R['ok'] = ok; json.dump(R, open(os.path.join(ROOT, 'field_tests/results/d1982_battery.json'), 'w'), indent=1, default=str)
    print(json.dumps(R, indent=1, default=str)); sys.exit(0 if all(ok.values()) else 1)
