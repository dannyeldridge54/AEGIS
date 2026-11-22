#!/usr/bin/env python3
"""Spec for planner.py, written BEFORE the planner (lock-first). Each case is a synthetic round state with the action the planner
must (or must not) produce. Run: python3 tools/loom/test_planner.py  -> one line per case, 'ok' or 'FAIL', exit 1 on any FAIL."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import planner as P
M = json.load(open(os.path.join(os.path.dirname(__file__), 'mission.json')))
LM = {'1': 'LOCKED', '2': 'LOCKED-BY-FIT', '3': 'TRUST (no margin)', '4': 'NO LOCK', '5': 'LOCKED-BY-FIT', '6': 'LOCKED-BY-FIT',
      '7': 'LOCKED-BY-FIT', '8': 'LOCKED-BY-FIT', '9': 'TRUST (no margin)'}
def st(**kw):
    s = dict(round=3, void=False, null=False, null_streak=0, state=dict(lock_map=dict(LM), fits_spent=['MN', 'm32', 'TR', 'split'], ledger_len=14),
             work_order=dict(node_agents=[], referee=False))
    s.update({k: v for k, v in kw.items() if k != 'state'}); s['state'].update(kw.get('state', {})); return s
def plan(cur, prev=None, pft=None, n0=None): return P.plan(cur, prev, M, pft=pft, n0=n0, owed_done=set())
CASES = []
def case(f): CASES.append(f); return f
@case
def void_first():          # a VOID self-test means nothing else may run
    a = plan(st(void=True)); return a['actions'][0]['kind'] == 'fix_selftest' and len(a['actions']) == 1
@case
def innermost_unlocked_first():   # N0 inside-out rule: layer 4 (NO LOCK) before any outer layer
    a = plan(st()); d = [x for x in a['actions'] if x['kind'] == 'derive']; return d and d[0]['layer'] == '4'
@case
def no_lock_beats_by_fit():  # a NO LOCK layer outranks a LOCKED-BY-FIT layer even if further out
    lm = dict(LM); lm['4'] = 'LOCKED'; lm['8'] = 'NO LOCK'; a = plan(st(state=dict(lock_map=lm)))
    d = [x for x in a['actions'] if x['kind'] == 'derive']; return d[0]['layer'] == '8'
@case
def fits_become_targets():   # every spent fit appears as a derive target with its mission node
    a = plan(st()); t = {x.get('fit') for x in a['all'] if x['kind'] == 'derive_fit'}; return t == {'MN', 'm32', 'TR', 'split'}
@case
def fit_rise_alarm():        # G-T3: more fits than last round -> alarm, at the top
    a = plan(st(state=dict(fits_spent=['MN', 'm32', 'TR', 'split', 'C'])), prev=st()); return a['actions'][0]['kind'] == 'alarm' and 'G-T3' in a['actions'][0]['guard']
@case
def killable_fall_alarm():   # G-T4: killable count below the floor -> alarm
    a = plan(st(), pft=dict(predictions=3, fits=4, trust=3, killable=3)); return any(x['kind'] == 'alarm' and 'G-T4' in x['guard'] for x in a['actions'])
@case
def relabel_not_progress():  # G-T1: a layer that went NO LOCK -> TRUST is flagged, not counted
    lm = dict(LM); lm['4'] = 'TRUST (relabel)'; a = plan(st(state=dict(lock_map=lm)), prev=st())
    return any(x['kind'] == 'alarm' and 'G-T1' in x['guard'] for x in a['actions']) and a['mission']['progress_this_round'] is False
@case
def referee_when_due():
    a = plan(st(work_order=dict(node_agents=[], referee=True))); return any(x['kind'] == 'referee' for x in a['actions'])
@case
def n0_lead_overrides_order():  # if N0 says derive layer 5 first, the first derive follows N0
    n0 = [dict(layer='5', action='derive', next_step='W0 without the wino window', why='N0'), dict(layer='4', action='hold')]
    a = plan(st(), n0=n0); d = [x for x in a['actions'] if x['kind'] == 'derive']; return d[0]['layer'] == '5' and all(x['layer'] != '4' for x in d)
@case
def stalled_null_explores():  # 7 nulls without balance is a stall, not the endpoint: must add an exploration action, endpoint not reached
    a = plan(st(null=True, null_streak=7)); return a['mission']['endpoint_reached'] is False and any(x['kind'] == 'explore' for x in a['actions'])
@case
def endpoint_only_when_all():  # every layer LOCKED, no fits, 7 nulls, killable ok, referee signed -> endpoint
    lm = {str(i): 'LOCKED' for i in range(1, 10)}
    a = P.plan(st(null=True, null_streak=7, state=dict(lock_map=lm, fits_spent=[])), None, M, pft=dict(predictions=6, fits=0, trust=0, killable=4), n0=None, owed_done=set(o['id'] for o in M['owed']), referee_signed=True)
    return a['mission']['endpoint_reached'] is True
@case
def every_action_has_why_tool_guard():  # awareness: each action says why, which toolkit, which guard
    a = plan(st()); return all(x.get('why') and 'tools' in x and x.get('guard') for x in a['actions'])
@case
def derive_needs_lock():     # any action that computes is marked needs_lock
    a = plan(st()); return all(x['needs_lock'] for x in a['actions'] if x['kind'] in ('derive', 'derive_fit', 'test'))
@case
def owed_listed():           # owed items appear until done
    a = plan(st()); return any(x['kind'] == 'owed' for x in a['all'])
@case
def capped():
    a = plan(st()); return len(a['actions']) <= M['max_actions']
@case
def toolkits_exist():        # integration: every toolkit named in toolkits.json resolves
    return P.check_toolkits()['missing'] == []
if __name__ == '__main__':
    bad = 0
    for f in CASES:
        try: ok = bool(f())
        except Exception as e: ok = False; print(f.__name__, 'FAIL', type(e).__name__, e); bad += 1; continue
        print(f.__name__, 'ok' if ok else 'FAIL'); bad += (not ok)
    sys.exit(1 if bad else 0)
