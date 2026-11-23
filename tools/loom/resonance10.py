"""D2136: resonance with a 10th rung (Danny 19:13-19:14): A outer data shell, B negative-space shell, C spine (hub dNeff).
Base = D1972 resonance.py, unchanged; new knob dNeff; breathing = inhale (dNeff frozen at 0) / exhale (free), 3 breaths.
python3 tools/loom/resonance10.py <V0|VA|VB|VC>"""
import sys, statistics
"""(base) Layered resonance (Danny 17:58): build the equation from the centre outwards through 9 layers (torus → pyramid → turnover → cube →
fold → dilaton → forces → cosmology → late universe). At each layer k, ALL knobs of layers 1..k are re-balanced together (self-balancing,
"torquing back and forth"), maximising the minimum margin over layers 1..k. A layer LOCKS when all its margins are >= 0 in 3 consecutive
solver passes ("lock where it's 3"). Then move outwards. The whole sweep runs 3 times, each starting from the previous sweep's knobs.
Margins are log-headroom (bounds) or 2 - |pull| (data); > 0 passes. TRUST layers carry no margin and cannot lock by construction (G-T5).
Every knob moved more than 1 % from its DERIVED value counts as a FIT spent (guard G-T3).
This is a deterministic consistency map, not evidence (D1948: optimiser output)."""
import json, math
D = dict(u=0.02663, MN=1.844e11, m32=2.58e5, TR=3.7e8, split=0.0)       # derived values; split = ln(A3/A2) (0 = single stack)
m_phi, MP = 4.93e12, 2.435e18
def obs(k):
    M2 = 686.5 * k['m32'] / 2.58e5
    Om = 0.017 * (k['TR'] / 3.2e8) * (M2 / 660) ** 1.5
    Ns = 50.3 + math.log(k['TR'] / 3.7e8) / 3
    ns = 1 - (1 - 0.9706) * 50.3 / Ns
    a_s = 0.11401 * (k['m32'] / 2.58e5) ** (-0.0254)
    if k['split'] != 0.0: a_s_eff = 0.1180 + (a_s - 0.1180) * 0.0      # split stacks absorb the gap (FIT); naturalness margin below
    else: a_s_eff = a_s
    Br = 0.0233 * (k['MN'] / 1.844e11) ** 2                              # natural p = 2, N_g = 12, 64 pi (D1946a)
    eps = 2.281e-5 * k['MN'] / 1.844e11
    Y = (28 / 79) * 1.5 * (k['TR'] / m_phi) * eps * Br
    return dict(M2=M2, Om=Om, ns=ns, a_s=a_s_eff, Y=Y, MN=k['MN'], u=k['u'], split=k['split'])
def margins(k):
    o = obs(k)
    rung = [o['u'], 0.0253, math.exp(-9 * math.pi / 8)]
    return {
     1: dict(quark_window=min(math.log(o['u'] / 0.02588), math.log(0.02740 / o['u']))),
     2: dict(nu_ratio=math.log(1.33), MN_top=math.log(2.5e12 / o['MN']), MN_bottom=math.log(o['MN'] / 4.5e10)),
     3: {},                                                               # leptons at rho: Koide TRUST
     4: dict(rung_agreement=math.log(1.15) - math.log(max(rung) / min(rung))),
     5: dict(wino=math.log(o['M2'] / 700.0)),
     6: dict(n_s=2 - abs((o['ns'] - 0.9728) / 0.0027)),
     7: dict(alpha_s=2 - abs((o['a_s'] - 0.1180) / math.hypot(0.0009, 0.00057)), split_natural=math.log(3) - abs(o['split'])),
     8: dict(gravitino_box=math.log(0.12 / o['Om']), leptogenesis=math.log(o['Y'] / 0.87e-10)),
     9: {}}                                                               # dark thread: TRUST
KNOBS_OF = {1: ['u'], 2: ['MN'], 3: [], 4: [], 5: ['m32'], 6: ['TR'], 7: ['m32', 'split'], 8: ['TR', 'MN', 'm32'], 9: []}   # D1989 P1.5 (was L4 ['u'], L8 ['TR','MN'])
NAMES = {1: 'torus (centre, rung step)', 2: 'pyramid (i, neutrinos)', 3: 'turnover (rho, leptons)', 4: 'cube (three tori together)',
         5: 'fold (volumes, m3/2)', 6: 'dilaton (inflation)', 7: 'forces (S-T seam)', 8: 'cosmology (reheating, genesis)', 9: 'late universe (thread)'}
LOG = {'u', 'MN', 'm32', 'TR'}
def solve(k, layers, state):
    knobs = sorted({x for L in layers for x in KNOBS_OF[L]})
    if not knobs: return state, 0
    h = {x: (0.2 if x in LOG else 0.3) for x in knobs}; nulls = 0; it = 0; prev = None
    def score(s): return min([v for L in layers for v in margins(s)[L].values()] or [0])
    while nulls < 7 and it < 400:
        it += 1; moved = False
        for x in knobs:
            cands = []
            for d in (-h[x], 0.0, h[x]):
                s = dict(state)
                s[x] = state[x] * math.exp(d) if x in LOG else state[x] + d
                cands.append((score(s), -abs(d), d, s))
            best = max(cands, key=lambda c: (c[0], c[1]))
            if best[2] == 0.0: h[x] *= 0.5
            else: moved = True
            state = best[3]
        sc = score(state)
        nulls = nulls + 1 if (prev is not None and abs(sc - prev) < 1e-6 and not moved) else 0
        prev = sc
    return state, it
def fits_spent(s):
    return [x for x in ('u', 'MN', 'm32', 'TR') if abs(s[x] / D[x] - 1) > 0.01] + (['split'] if abs(s['split']) > 1e-9 else [])

D['dNeff'] = 0.0
H0_BASE = statistics.median([67.43, 67.63, 67.42])   # addendum R36-4; S_H0 = statistics.median([5.0, 6.2, 7.0])
_base_margins = margins
VAR = sys.argv[1] if len(sys.argv) > 1 else 'VC'
def margins(k):
    m = _base_margins(k); dn = k.get('dNeff', 0.0); H0 = H0_BASE + S_H0*dn
    m[10] = {}
    if VAR != 'V0' and dn < 0: m[10]['dNeff_nonneg'] = 100*dn          # dark radiation cannot be negative
    if VAR in ('VA', 'VB', 'VC'):
        m[10]['H0_vs_SH0ES'] = 2 - abs(H0 - 73.04)/1.04
        m[10]['sum_mnu_DESI'] = math.log(0.064/0.0587)
    if VAR in ('VB', 'VC'):
        m[10]['negspace_dNeff_ACT'] = math.log(0.14/max(dn, 1e-6))
        m[10]['negspace_alpha_null'] = math.log(1e-6/1e-9)
    if VAR == 'VC':
        m[8] = dict(m[8], spine_BBN_dNeff=math.log(0.3/max(dn, 1e-6)))
    m['H0'] = H0
    return m
KNOBS_OF[10] = ['dNeff'] if VAR != 'V0' else []
NAMES[10] = {'V0': '(none)', 'VA': 'outer data shell', 'VB': 'outer + negative-space shell', 'VC': 'shells + spine'}[VAR]
def fits_spent(s):
    return [x for x in ('u', 'MN', 'm32', 'TR') if abs(s[x] / D[x] - 1) > 0.01] + (['split'] if abs(s['split']) > 1e-9 else []) + (['dNeff'] if abs(s.get('dNeff', 0)) > 1e-9 else [])
_solve = solve
def solve(k, layers, state, frozen=False):
    if frozen:
        saved = KNOBS_OF[10]; KNOBS_OF[10] = []
        try: return _solve(k, layers, state)
        finally: KNOBS_OF[10] = saved
    return _solve(k, layers, state)
def lin(state, k): return {a: round(b, 4) for a, b in margins(state)[k].items()}
out = dict(variant=VAR, s_H0=S_H0, breaths=[]); state = dict(D); top = 10 if VAR != 'V0' else 9
prev_locked = None
for breath in (1, 2, 3):
    for phase in ('inhale', 'exhale'):
        frozen = phase == 'inhale'
        if frozen: state['dNeff'] = 0.0
        locked = []; rows = []
        for k in range(1, top + 1):
            layers = locked + [k]; passes = []
            for _ in range(3):
                state, it = solve(k, layers, state, frozen)
                mk = {a: b for a, b in margins(state)[k].items()}
                passes.append(bool(mk) and all(v >= 0 for v in mk.values()))
            lock = all(passes) and bool(margins(state)[k])
            if lock: locked.append(k)
            rows.append(dict(layer=k, name=NAMES[k], locked=lock, margins=lin(state, k)))
        inner_unlocked = sorted(set(prev_locked or []) - set(locked)) if (prev_locked is not None and not frozen) else []
        out['breaths'].append(dict(breath=breath, phase=phase, locked=locked, H0=round(margins(state)['H0'], 3), dNeff=state['dNeff'],
                                   fits_spent=fits_spent(state), inner_unlocked_vs_inhale=inner_unlocked, rows=rows))
        if frozen: prev_locked = [L for L in locked if L <= 9]
        print(VAR, breath, phase, 'locked', locked, 'H0', round(margins(state)['H0'], 2), 'dNeff', round(state['dNeff'], 4),
              'L10', lin(state, 10) if top == 10 else '-', 'unbal', inner_unlocked, flush=True)
import math as _m
out['FL_fluid_reading'] = dict(H0=68.75, margin_SH0ES=2 - (73.04 - 68.75)/_m.hypot(1.04, 0.92), source='WZDR, P-ACT-LBS, no SH0ES (2512.19633)')
out['FS_needed_dNeff_for_margin0'] = (73.04 - 2*1.04 - H0_BASE)/S_H0
out['PS_window_side_test'] = {k: (v < 0.14) for k, v in dict(vectors=0.11, with_fermions=0.50, all_massless=0.76).items()}
out['CCHP_second_reading_at_final'] = 2 - abs(margins(state)['H0'] - 69.96)/1.53
print('FL fluid margin', round(out['FL_fluid_reading']['margin_SH0ES'], 3), 'FS needs dNeff >=', round(out['FS_needed_dNeff_for_margin0'], 3), 'PS window', out['PS_window_side_test'], 'CCHP margin', round(out['CCHP_second_reading_at_final'], 3))
json.dump(out, open('field_tests/results/d2136_resonance10_%s.json' % VAR, 'w'), indent=1, default=str)
