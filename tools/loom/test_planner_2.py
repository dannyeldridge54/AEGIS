#!/usr/bin/env python3
"""Spec addendum (22 Nov 2026 00:35Z), written after a mutation test of planner.py showed two blind spots in test_planner.py
(locked d1803df7, unchanged): (a) reversing the inside-out order of several unlocked layers was not caught; (b) declaring the
endpoint while an alarm fires was not caught. Also covers the N0 rule 'outer layers may not derive until L4 is locked or held'
and the 18:24 agents (axis agents S/T/U, edge agents). Locked before the planner fixes below."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from test_planner import st, plan, M, LM, P
CASES = []
def case(f): CASES.append(f); return f
@case
def two_unlocked_inside_out():
    lm = dict(LM); lm['2'] = 'NO LOCK'; lm['7'] = 'NO LOCK'; d = [x['layer'] for x in plan(st(state=dict(lock_map=lm)))['all'] if x['kind'] == 'derive']
    return d[:3] == ['2', '4', '7']
@case
def by_fit_inside_out():
    d = [x['layer'] for x in plan(st())['all'] if x['kind'] == 'derive']; return d == ['4', '2', '5', '6', '7', '8']
@case
def no_endpoint_with_alarm():
    lm = {str(i): 'LOCKED' for i in range(1, 10)}
    a = P.plan(st(null=True, null_streak=7, state=dict(lock_map=lm, fits_spent=[])), None, M, pft=dict(predictions=6, fits=0, trust=0, killable=3), n0=None, owed_done=set(), referee_signed=True)
    return a['mission']['endpoint_reached'] is False
@case
def n0_blocks_outer_until_l4():   # N0: derive L4, test L5/L8; tests on outer layers are 'test', not 'derive', and come after L4
    n0 = [dict(layer='4', action='derive'), dict(layer='5', action='test'), dict(layer='8', action='test'), dict(layer='7', action='hold')]
    a = plan(st(), n0=n0); k = [(x['kind'], x['layer']) for x in a['all'] if x['kind'] in ('derive', 'test')]
    return k == [('derive', '4'), ('test', '5'), ('test', '8')]
@case
def held_layer_fit_not_derived_first():   # a fit whose layer N0 holds must not appear in actions ahead of L4
    n0 = [dict(layer='4', action='derive'), dict(layer='7', action='hold')]
    a = plan(st(), n0=n0)['actions']; i4 = next(i for i, x in enumerate(a) if x.get('layer') == '4')
    return all(not (x['kind'] == 'derive_fit' and x['layer'] == '7' and i < i4) for i, x in enumerate(a))
@case
def axis_agents_follow_fits():
    g = plan(st(state=dict(fits_spent=['m32'])))['agents']['axis_agents']; return 'T' in g and 'U' in g   # T from the fit, U from L4
@case
def edge_agents_quiet_when_locked():
    lm = {str(i): 'LOCKED' for i in range(1, 10)}; return plan(st(state=dict(lock_map=lm, fits_spent=[])))['agents']['edge_agents'] == {}
if __name__ == '__main__':
    bad = 0
    for f in CASES:
        try: ok = bool(f())
        except Exception as e: print(f.__name__, 'FAIL', type(e).__name__, e); bad += 1; continue
        print(f.__name__, 'ok' if ok else 'FAIL'); bad += (not ok)
    sys.exit(1 if bad else 0)
