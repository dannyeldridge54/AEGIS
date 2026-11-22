#!/usr/bin/env python3
"""loomd — the Loom as one toolkit / daemon (Danny 18:19). Runs consecutive pulses of the deterministic core and writes the agent work
orders for the parts only agents can do (centre referee N0, node agents, referee). Usage:
  python3 tools/loom/loomd.py pulse [--rounds N] [--method]   # N consecutive pulses (default 1); --method also reruns the method tests
  python3 tools/loom/loomd.py status                          # print the latest round summary
Each pulse, in order (datasheet layers A→G):
  0  self-test of the checks (C1–C7 on known past mistakes)  — must all FLAG/ok as expected or the pulse stops (VOID)
  1  still point + inward/outward directions (D8)              2  resonance map centre→out, 3 sweeps (D1972, LOCKED-BY-FIT labels)
  3  [optional] method tests on three axes (T1–T3)             4  compass + review (D1, D6)
  5  centre brief for N0 (F6)                                   6  ledger snapshot; NULL-round test (G-T6: state unchanged)
  7  agent work order: N0 always; node agents only for nodes whose inputs changed; referee every 2nd round
  8  mission awareness: planner.py (mission.json + round + N0 lead) -> next_actions.{json,md}, axis and edge agents to wake
  python3 tools/loom/loomd.py mission                         # print the mission status and next actions
Stops early after 7 consecutive NULL pulses (a STALL unless the endpoint is reached). Agents are spawned by the session (the daemon cannot); it writes their briefs."""
import json, os, subprocess, sys, time, hashlib, argparse
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(ROOT)
RD = 'field_tests/loom/rounds'; os.makedirs(RD, exist_ok=True)
def run(cmd, timeout=900):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout); return r.returncode, r.stdout[-4000:], r.stderr[-2000:]
def H(path):
    try: return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:12]
    except FileNotFoundError: return None
def last_round():
    fs = sorted(f for f in os.listdir(RD) if f.startswith('round_')); return (json.load(open(os.path.join(RD, fs[-1]))), len(fs)) if fs else (None, 0)
EXPECT = {'D1941_mphi_independence': 'FLAG', 'D1938_seam_power': 'FLAG', 'D1926_run1_validation': 'FLAG', 'D1946_numerology_real': 'FLAG',
          'D1931_lint': 'FLAG', 'clean_lint': 'ok', 'ns_four_corners': 'ok', 'D1946_gauge_width_formula': 'FLAG'}
NODE_INPUTS = {'N1': ['tools/project_docs/WEAVE_UNIFIED_EQUATION.md'], 'N2': ['field_tests/results/d1978_still_point.json'],
               'N3': ['field_tests/results/d1937_knobs.json'], 'N4': ['field_tests/results/d1932_ring0_rungstep.json'],
               'N5': ['field_tests/results/d1944_as_yukawa.json'], 'N6': ['tools/project_docs/WEAVE_TEST_BATTERY.md'],
               'N7': ['field_tests/results/d1946_three.json'], 'N8': ['tools/project_docs/WEAVE_UNIFIED_EQUATION.md'],
               'N9': ['tools/project_docs/WEAVE_TEST_BATTERY.md']}
def pulse(method):
    prev, n = last_round(); rid = n + 1; rec = dict(round=rid, t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), steps={})
    c, out, err = run('python3 tools/loom/test_check.py')
    got = {l.split()[0]: l.split()[1] for l in out.splitlines() if l.strip()}
    bad = [k for k, v in EXPECT.items() if got.get(k) != v]
    rec['steps']['0_selftest'] = dict(ok=not bad, mismatches=bad)
    if bad: rec['void'] = True; json.dump(rec, open(f'{RD}/round_{rid:03d}.json', 'w'), indent=1); return rec
    for key, cmd in (('1_still_point', 'python3 tools/loom/still_point.py'), ('2_resonance', 'python3 tools/loom/resonance.py'), ('2b_lensing', 'python3 tools/loom/lensing.py'), ('2c_pass_labels', 'python3 tools/loom/pass_label_check.py field_tests/results/d1989_woven_run.json'),
                     ('3_method_tests', 'python3 tools/loom/method_tests_3axis.py' if method else None),
                     ('4_compass', 'python3 tools/loom/compass.py'), ('4b_review', 'python3 tools/loom/review.py'),
                     ('5_centre_brief', 'python3 tools/loom/centre_brief.py')):
        if cmd is None: rec['steps'][key] = dict(skipped=True); continue
        c, o, e = run(cmd); rec['steps'][key] = dict(rc=c, tail=o[-600:], err=e[-300:] if c else '')
    rs = json.load(open('field_tests/results/d1972_resonance.json'))['sweeps'][-1]
    led = json.load(open('field_tests/loom/knockon_ledger.json'))
    state = dict(lock_map={r['layer']: r['status'] for r in rs['rows']}, fits_spent=rs['fits_spent'], ledger_len=len(led),
                 inputs={k: [H(p) for p in v] for k, v in NODE_INPUTS.items()})
    rec['state'] = state
    same = prev is not None and prev.get('state', {}).get('lock_map') == {str(k): v for k, v in state['lock_map'].items()} \
           and prev['state'].get('fits_spent') == state['fits_spent'] and prev['state'].get('ledger_len') == state['ledger_len']
    rec['null'] = bool(same); rec['null_streak'] = (prev.get('null_streak', 0) + 1) if same and prev else 0
    changed = [k for k, v in state['inputs'].items() if not prev or prev.get('state', {}).get('inputs', {}).get(k) != v]
    rec['work_order'] = dict(N0=dict(brief='field_tests/loom/centre_brief.md', charter='tools/project_docs/WEAVE_NODE_CHARTER.md'),
                             node_agents=changed, referee=(rid % 2 == 0))
    fn = f'{RD}/round_{rid:03d}.json'; json.dump(rec, open(fn, 'w'), indent=1, default=str)
    # 8  mission awareness (Danny 18:20): the planner reads mission.json + this round + N0's lead and writes next_actions.{json,md}
    sys.path.insert(0, os.path.join(ROOT, 'tools/loom')); import planner
    p = planner.main(os.path.abspath(fn)); rec['plan'] = dict(endpoint_reached=p['mission']['endpoint_reached'], satisfied=p['mission']['satisfied'],
        next=[(a['kind'], a['layer']) for a in p['actions']], agents=p['agents'], toolkits_missing=p['toolkits']['missing'])
    rec['work_order'].update(axis_agents=list(p['agents']['axis_agents']), edge_agents=list(p['agents']['edge_agents']))
    json.dump(rec, open(fn, 'w'), indent=1, default=str); return rec
# ---------------- D1989 P4: self-driving
def auto_decide(rec, plan):
    if rec.get('void'): return 'VOID'
    if (plan or {}).get('mission', {}).get('endpoint_reached'): return 'ENDPOINT'
    if rec.get('null_streak', 0) >= 7: return 'STALL'
    return 'CONTINUE'
def fdr_update(field):
    """Online FDR (LORD++) over band-goalpost tension p-values, accumulated across rounds."""
    import math; sys.path.insert(0, os.path.join(ROOT, 'tools/loom')); import online_fdr
    G = {g['id']: g for g in json.load(open('tools/loom/goalposts.json'))['goalposts']}; led_p = 'field_tests/loom/fdr_ledger.json'
    led = json.load(open(led_p)) if os.path.exists(led_p) else []
    for L, rows in field.get('scoreboard', {}).items():
        for r in rows:
            g = G[r['id']]
            if g['data']['type'] == 'band' and r['value'] is not None and g['kind'] in ('PRED', 'FIT', 'NULL'):
                led.append(dict(round=field.get('round'), id=r['id'], pull=r['value'], p=math.erfc(abs(r['value']) / math.sqrt(2))))
    rej, al = online_fdr.lord_pp([x['p'] for x in led]); json.dump(led, open(led_p, 'w'), indent=1)
    return dict(tests=len(led), significant_tensions=sorted({led[i]['id'] for i, r in enumerate(rej) if r}))
def auto(n, field_s):
    sys.path.insert(0, os.path.join(ROOT, 'tools/loom')); import planner, importlib
    os.makedirs('field_tests/loom/reports', exist_ok=True); os.makedirs('field_tests/results/auto', exist_ok=True)
    for _ in range(n):
        rec = pulse(False); rid = rec['round']; fn = f'{RD}/round_{rid:03d}.json'
        if rec.get('void'): print('round %d VOID' % rid); break
        import loom_rt4; importlib.reload(loom_rt4)
        field = loom_rt4.scored(field_s, seed=2026 + rid, out_name=f'auto/round_{rid:03d}_field.json', archive=False); field['round'] = rid
        c, o, e = run('python3 tools/loom/test_loom_battery.py'); bat = json.load(open('field_tests/results/d1982_battery.json'))['ok']
        c2, o2, e2 = run(f'python3 tools/loom/pass_label_check.py field_tests/results/auto/round_{rid:03d}_field.json'); c8 = (c2 == 0)
        fdr = fdr_update(field); p = planner.main(os.path.abspath(fn))
        rec['auto'] = dict(field=dict(verdict=field['verdict'], accuracy=field['accuracy'], pulses_per_s=field['pulses_per_s'], tally=field['goalpost_tally'],
                                      done=field['done_seconds'], stuck=field['stuck_events'], fits=field['fits_spent'], no_free=field['no_free_knob_share']),
                           battery=bat, pass_label_ok=c8, fdr=fdr, decision=auto_decide(rec, p))
        json.dump(rec, open(fn, 'w'), indent=1, default=str)
        m = p['mission']; L = ['# Loom auto round %d' % rid, '', '**Decision:** %s. Null %s (streak %s). Endpoint %s (%s).' % (rec['auto']['decision'], rec['null'], rec['null_streak'], m['endpoint_reached'], m['satisfied']),
             '', '**Field run** (%.0f s, seed %d): %s; %s pulses/s; accuracy %s' % (field_s, 2026 + rid, field['verdict'], field['pulses_per_s'], field['accuracy']),
             '**Goalposts:** %s. **Nodes DONE (s):** %s. **STUCK:** %s. **Fits spent:** %s.' % (field['goalpost_tally'], field['done_seconds'], field['stuck_events'], field['fits_spent']),
             '**Battery:** %s. **PASS-label check:** %s. **Online FDR:** %d tests, significant tensions %s.' % (bat, 'ok' if c8 else 'VIOLATIONS', fdr['tests'], fdr['significant_tensions']),
             '', '**Lock map:** %s' % rec['state']['lock_map'], '', '**Next actions:**'] + ['- %s L%s: %s' % (a['kind'], a.get('layer'), a['why']) for a in p['actions']]
        open(f'field_tests/loom/reports/round_{rid:03d}.md', 'w').write('\n'.join(L) + '\n')
        print('round %d: %s | field %s %s/s | tally %s | DONE %s | FDR tensions %s' % (rid, rec['auto']['decision'], field['verdict'], field['pulses_per_s'], field['goalpost_tally'], {k: v for k, v in field['done_seconds'].items() if v}, fdr['significant_tensions']))
        if rec['auto']['decision'] != 'CONTINUE': break
def selftest():
    """P1.7 determinism (two real pulses) + P4 decision logic."""
    a = pulse(False); b = pulse(False)
    same = all(str(a['state'].get(k)) == str(b['state'].get(k)) for k in ('lock_map', 'fits_spent', 'ledger_len'))
    dec = dict(stall=auto_decide(dict(null_streak=7), {}) == 'STALL', endpoint=auto_decide(dict(null_streak=7), dict(mission=dict(endpoint_reached=True))) == 'ENDPOINT',
               void=auto_decide(dict(void=True), {}) == 'VOID', cont=auto_decide(dict(null_streak=2), {}) == 'CONTINUE')
    out = dict(determinism=dict(same_state=same, second_null=bool(b.get('null')), rounds=[a['round'], b['round']]), decision_logic=dec, ok=same and bool(b.get('null')) and all(dec.values()))
    json.dump(out, open('field_tests/results/d1989_selftest.json', 'w'), indent=1); print(out); return out
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['pulse', 'status', 'mission', 'auto', 'selftest']); ap.add_argument('--rounds', type=int, default=1); ap.add_argument('--method', action='store_true'); ap.add_argument('--pulses', type=int, default=12); ap.add_argument('--field-seconds', type=float, default=20.0)
    a = ap.parse_args()
    if a.cmd == 'auto': auto(a.pulses, a.field_seconds); sys.exit()
    if a.cmd == 'selftest': selftest(); sys.exit()
    if a.cmd == 'mission':
        sys.path.insert(0, os.path.join(ROOT, 'tools/loom')); import planner; planner.main(); print(open('field_tests/loom/next_actions.md').read()); sys.exit()
    if a.cmd == 'status':
        r, n = last_round(); print(json.dumps(r, indent=1, default=str) if r else 'no rounds yet'); sys.exit()
    for _ in range(a.rounds):
        r = pulse(a.method)
        print('round %d: %s; null=%s streak=%s; lock map %s; fits %s; work order: N0 + nodes %s%s' % (
            r['round'], 'VOID (self-test mismatch %s)' % r['steps']['0_selftest']['mismatches'] if r.get('void') else 'ok', r.get('null'), r.get('null_streak'),
            r.get('state', {}).get('lock_map'), r.get('state', {}).get('fits_spent'), r.get('work_order', {}).get('node_agents'),
            ' + REFEREE' if r.get('work_order', {}).get('referee') else ''))
        if r.get('plan'): print('  mission: endpoint %s (%s); next %s' % ('REACHED' if r['plan']['endpoint_reached'] else 'not reached', r['plan']['satisfied'], r['plan']['next']))
        if r.get('void') or (r.get('plan') or {}).get('endpoint_reached'): break
        if r.get('null_streak', 0) >= 7: print('  STALL: 7 null pulses without balance -> the planner switches to exploration'); break
