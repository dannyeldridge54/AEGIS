#!/usr/bin/env python3
"""The Loom's planner: mission awareness (Danny 18:20). Reads the mission (mission.json), the latest round state (loomd), the
prediction/FIT/TRUST ledger and N0's lead, and says: what the mission is, how far we are, what is blocking, which guard is at risk,
and the next actions in order, each with why, which toolkit, which guard, and whether it must be locked first.
It also says which agents to wake: N0, node agents, the three axis agents (S, T, U) and the two edge agents (Danny 18:24).
It decides nothing irreversible and runs nothing: it writes field_tests/loom/next_actions.{json,md}.
Usage: python3 tools/loom/planner.py [round_file]"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RANK = lambda s: 3 if s.startswith('LOCKED') and 'FIT' not in s else 2 if s.startswith('LOCKED-BY') else 1 if s.startswith('TRUST') else 0
AXES = {'S': 'dilaton S (ln T_R, n_s, reheating)', 'T': 'volumes T (ln m3/2, KKLT, spectrum)', 'U': 'complex structure U (ln u, flavour rungs)'}
AXIS_OF_FIT = {'MN': 'S', 'TR': 'S', 'm32': 'T', 'split': 'T', 'u': 'U', 'C': 'S', 'A': 'T'}
AXIS_OF_LAYER = {'1': 'STU', '2': 'U', '3': 'U', '4': 'U', '5': 'T', '6': 'S', '7': 'ST', '8': 'ST', '9': 'ST'}
def _j(p, d=None):
    try: return json.load(open(p))
    except (FileNotFoundError, json.JSONDecodeError): return d
def load_mission(): return _j(os.path.join(HERE, 'mission.json'))
def tools_for(key, kind='layers'):
    tk = _j(os.path.join(HERE, 'toolkits.json'), {}); return [t['name'] for t in tk.get(kind, {}).get(key, [])]
def check_toolkits():
    """Integration check: every toolkit named in toolkits.json resolves to a real tool."""
    tk = _j(os.path.join(HERE, 'toolkits.json'), {}); src = open(os.path.join(ROOT, 'tools/weave_cm/weave_tools.py')).read()
    weave = set(re.findall(r"'(weave_\w+)':\s*weave_\w+", src))
    regp = next((p for p in (os.environ.get('CUBEMIND_DIR', ''), '/home/claude/cubemind', os.path.expanduser('~/cubemind')) if p and os.path.isfile(os.path.join(p, 'aegis_tools/registry.py'))), None)
    cm = set(re.findall(r"^ '(\w+)': \(", open(os.path.join(regp, 'aegis_tools/registry.py')).read(), re.M)) if regp else None
    missing, unverified = [], []
    for group in tk.get('layers', {}), tk.get('kinds', {}):
        for k, lst in group.items():
            for t in lst:
                if t['kind'] == 'weave' and t['name'] not in weave: missing.append(t['name'])
                elif t['kind'] == 'script' and not os.path.isfile(os.path.join(ROOT, t['name'])): missing.append(t['name'])
                elif t['kind'] == 'cm':
                    if cm is None: unverified.append(t['name'])
                    elif t['name'] not in cm: missing.append(t['name'])
    return dict(missing=sorted(set(missing)), unverified=sorted(set(unverified)))
def act(kind, why, guard, layer=None, tools=None, needs_lock=False, **kw):
    return dict(kind=kind, layer=layer, why=why, guard=guard, tools=tools or [], needs_lock=needs_lock, **kw)
def plan(cur, prev, M, pft=None, n0=None, owed_done=frozenset(), referee_signed=False):
    lm = {str(k): v for k, v in (cur.get('state') or {}).get('lock_map', {}).items()}
    plm = {str(k): v for k, v in ((prev or {}).get('state') or {}).get('lock_map', {}).items()}
    fits = list((cur.get('state') or {}).get('fits_spent', [])); pfits = list(((prev or {}).get('state') or {}).get('fits_spent', []))
    out, alarms = [], []
    if cur.get('void'):
        a = act('fix_selftest', 'the self-test of the checks did not reproduce the known past mistakes; nothing downstream can be trusted', 'LOCK', tools=['tools/loom/test_check.py'])
        return dict(actions=[a], all=[a], agents=dict(), mission=dict(goal=M['goal'], endpoint_reached=False, progress_this_round=False, blocking=['VOID self-test']))
    # guards
    if prev and len(fits) > len(pfits):
        alarms.append(act('alarm', 'FIT count rose %d -> %d (%s): balance bought with a new fit' % (len(pfits), len(fits), sorted(set(fits) - set(pfits))), 'G-T3 FIT/TRUST must not rise'))
    relabel = [L for L in lm if L in plm and RANK(plm[L]) in (0, 2) and lm[L].startswith('TRUST')]
    for L in relabel: alarms.append(act('alarm', 'layer %s went %s -> %s: a relabel, counted as null' % (L, plm[L], lm[L]), 'G-T1 relabelling is not progress', layer=L))
    if pft and pft.get('killable', M['killable_min']) < M['killable_min']:
        alarms.append(act('alarm', 'killable predictions %s < floor %s' % (pft['killable'], M['killable_min']), 'G-T4 killable must not fall'))
    improved = [L for L in lm if L in plm and RANK(lm[L]) > RANK(plm[L]) and L not in relabel]
    progress = bool(improved or (prev and len(fits) < len(pfits))) and not any('G-T3' in a['guard'] for a in alarms)
    # derive order: N0 lead if present, else NO LOCK innermost first, then LOCKED-BY-FIT innermost first
    if n0:
        held = {str(x['layer']) for x in n0 if x.get('action') == 'hold'}
        order = [str(x['layer']) for x in n0 if x.get('action') in ('derive', 'move', 'test')]
        why0 = {str(x['layer']): x.get('next_step') or x.get('why') for x in n0}
        kind0 = {str(x['layer']): ('test' if x.get('action') == 'test' else 'derive') for x in n0}
    else:
        held = set(); why0 = {}; kind0 = {}
        order = sorted([L for L in lm if RANK(lm[L]) == 0], key=int) + sorted([L for L in lm if RANK(lm[L]) == 2], key=int)
    derive = [act(kind0.get(L, 'derive'), (why0.get(L) or ('layer %s (%s) is %s: derive it without a new fit before moving outward' % (L, M['layers'].get(L, '?'), lm.get(L, '?')))),
                  'N0 inside-out; G-T3; LOCK', layer=L, tools=tools_for(L), needs_lock=True, axes=AXIS_OF_LAYER.get(L, '')) for L in order if L not in held]
    dfit = [act('derive_fit', 'fit %s is spent to lock layer %s; derive it: %s' % (f, M['fit_targets'][f]['layer'], M['fit_targets'][f]['derive']), 'G-T3 turn fits into predictions',
                layer=M['fit_targets'][f]['layer'], tools=tools_for(M['fit_targets'][f]['layer']), needs_lock=True, fit=f, node=M['fit_targets'][f]['node']) for f in fits if f in M['fit_targets'] and M['fit_targets'][f]['layer'] not in held]
    ref = [act('referee', 'referee due this round (every 2nd round): fresh-context review of the board and of the last overclaims', 'E5 independent referee', tools=tools_for('referee', 'kinds'))] if (cur.get('work_order') or {}).get('referee') else []
    owed = [act('owed', o['what'], 'HONEST', tools=tools_for(o['kind'], 'kinds'), owed=o['id']) for o in M.get('owed', []) if o['id'] not in owed_done and not (o.get('file') and os.path.isfile(os.path.join(ROOT, o['file'])))]
    stalled = cur.get('null_streak', 0) >= 7
    explore = [act('explore', ('7 null rounds without balance is a STALL, not the endpoint: change the approach (broad then narrow; mine the loose still-point directions; a tournament of competing explanations for the strained layer)' if stalled
                    else 'null round: spend the exploration share on the loosest direction'), 'G-T6 null rounds count only with every node balanced', tools=tools_for('explore', 'kinds'))] if (stalled or cur.get('null')) else []
    # endpoint
    trust_ok = (pft or {}).get('trust_signed', False)
    E = dict(E1=all(RANK(v) == 3 or (RANK(v) == 1 and trust_ok) for v in lm.values()) and bool(lm), E2=stalled, E3=None,
             E4=not fits and bool(pft) and pft.get('killable', 0) >= M['killable_min'], E5=bool(referee_signed))
    reached = E['E1'] and E['E2'] and E['E4'] and E['E5'] and not alarms
    blocking = ['layer %s %s' % (L, lm[L]) for L in sorted(lm, key=int) if RANK(lm[L]) != 3] + (['%d fits spent: %s' % (len(fits), ', '.join(fits))] if fits else []) + \
               ([] if pft else ['no prediction/FIT/TRUST ledger yet'])
    allv = alarms + derive + ref + dfit + owed + explore
    actions = (alarms + derive[:2] + ref + (explore if stalled else []) + dfit[:1] + owed[:1] + ([] if stalled else explore))[:M['max_actions']]
    # agents to wake (Danny 18:24): axis agents trace their direction through all 9 layers; edge agents look in from outside L9 / inside L1
    hot_axes = sorted({a for f in fits for a in AXIS_OF_FIT.get(f, '')} | {a for x in derive[:2] for a in x.get('axes', '')})
    agents = dict(N0=True, node_agents=(cur.get('work_order') or {}).get('node_agents', []),
                  axis_agents={a: AXES[a] for a in hot_axes},
                  edge_agents={k: v for k, v in (('edge_out', 'outside layer 9: what the late-universe and collider data push back toward the centre'),
                                                 ('edge_in', 'inside layer 1: what the rung step / knot geometry pushes outward')) if
                               (k == 'edge_out' and any(RANK(lm.get(L, 'NO')) != 3 for L in '789')) or (k == 'edge_in' and any(RANK(lm.get(L, 'NO')) != 3 for L in '12'))},
                  referee=bool(ref))
    sat = sum(1 for v in E.values() if v)
    return dict(actions=actions, all=allv, agents=agents,
                mission=dict(goal=M['goal'], endpoint=E, endpoint_reached=bool(reached), satisfied='%d/5' % sat, progress_this_round=progress,
                             improved_layers=improved, blocking=blocking, fits_spent=fits, alarms=len(alarms)))
def to_md(p, rid):
    m = p['mission']; L = ['# Loom planner, round %s' % rid, '', '**Mission:** ' + m['goal'], '',
         '**Endpoint:** %s (%s conditions met). Progress this round: %s.' % ('REACHED' if m['endpoint_reached'] else 'not reached', m['satisfied'], m['progress_this_round']),
         '**Blocking:** ' + '; '.join(m['blocking']), '', '## Next actions (in order)']
    for i, a in enumerate(p['actions'], 1):
        L.append('%d. **%s**%s: %s. Guard: %s. Tools: %s.%s' % (i, a['kind'], ' L%s' % a['layer'] if a['layer'] else '', a['why'], a['guard'], ', '.join(a['tools']) or 'none mapped', ' **Lock first.**' if a['needs_lock'] else ''))
    g = p['agents']; L += ['', '## Agents to wake', '- N0 centre referee: always', '- node agents: %s' % (', '.join(g.get('node_agents', [])) or 'none (no inputs changed)'),
                         '- axis agents: %s' % ('; '.join('%s = %s' % kv for kv in g.get('axis_agents', {}).items()) or 'none'),
                         '- edge agents: %s' % ('; '.join('%s = %s' % kv for kv in g.get('edge_agents', {}).items()) or 'none'), '- referee: %s' % g.get('referee')]
    return '\n'.join(L) + '\n'
def main(round_file=None):
    rd = os.path.join(ROOT, 'field_tests/loom/rounds'); fs = sorted(glob.glob(os.path.join(rd, 'round_*.json')))
    cur_f = round_file or (fs[-1] if fs else None)
    if not cur_f: print('no rounds'); return
    i = fs.index(cur_f) if cur_f in fs else len(fs); cur = _j(cur_f); prev = _j(fs[i - 1]) if i > 0 else None
    M = load_mission(); pft = _j(os.path.join(ROOT, 'field_tests/loom/pft_ledger.json')); n0 = _j(os.path.join(ROOT, 'field_tests/loom/n0_lead.json'))
    p = plan(cur, prev, M, pft=pft, n0=(n0 or {}).get('lead') if isinstance(n0, dict) else n0, owed_done=set(_j(os.path.join(ROOT, 'field_tests/loom/owed_done.json'), [])))
    p['round'] = cur.get('round'); p['toolkits'] = check_toolkits()
    json.dump(p, open(os.path.join(ROOT, 'field_tests/loom/next_actions.json'), 'w'), indent=1)
    open(os.path.join(ROOT, 'field_tests/loom/next_actions.md'), 'w').write(to_md(p, cur.get('round'))); return p
if __name__ == '__main__':
    p = main(sys.argv[1] if len(sys.argv) > 1 else None); print(open(os.path.join(ROOT, 'field_tests/loom/next_actions.md')).read()); print('toolkits:', p['toolkits'])
