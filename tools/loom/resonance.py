"""Layered resonance (Danny 17:58): build the equation from the centre outwards through 9 layers (torus → pyramid → turnover → cube →
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
KNOBS_OF = {1: ['u'], 2: ['MN'], 3: [], 4: ['u'], 5: ['m32'], 6: ['TR'], 7: ['m32', 'split'], 8: ['TR', 'MN'], 9: []}
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
out = {'sweeps': []}; state = dict(D)
for sweep in (1, 2, 3):
    rows = []; locked = []
    for k in range(1, 10):
        layers = locked + [k]
        passes = []
        for _ in range(3):                                               # lock needs 3 consecutive passing solver passes
            state, it = solve(k, layers, state)
            m = margins(state)[k]
            passes.append(bool(m) and all(v >= 0 for v in m.values()))
        lock = all(passes) and bool(margins(state)[k])
        status = 'LOCKED' if lock else ('TRUST (no margin; cannot lock, G-T5)' if not margins(state)[k] else 'NO LOCK')
        if lock: locked.append(k)
        rows.append(dict(layer=k, name=NAMES[k], status=status, margins={a: round(b, 4) for a, b in margins(state)[k].items()},
                         knobs={x: state[x] for x in ('u', 'MN', 'm32', 'TR', 'split')}, fits_spent=fits_spent(state)))
    out['sweeps'].append(dict(sweep=sweep, rows=rows, locked=locked, final_knobs=dict(state), fits_spent=fits_spent(state)))
print(json.dumps([{s['sweep']: [(r['layer'], r['status'][:9], r['margins'], r['fits_spent']) for r in s['rows']]} for s in out['sweeps']], indent=0, default=str))
json.dump(out, open('field_tests/results/d1972_resonance.json', 'w'), indent=1, default=str)
