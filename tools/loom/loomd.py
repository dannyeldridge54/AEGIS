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
    for key, cmd in (('1_still_point', 'python3 tools/loom/still_point.py'), ('2_resonance', 'python3 tools/loom/resonance.py'), ('2b_lensing', 'python3 tools/loom/lensing.py'),
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
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['pulse', 'status', 'mission']); ap.add_argument('--rounds', type=int, default=1); ap.add_argument('--method', action='store_true')
    a = ap.parse_args()
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
