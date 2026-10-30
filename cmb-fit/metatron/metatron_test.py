# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 8d2486ab56291283
"""The Metatron test: do our measured numbers match Metatron's Cube more often than chance?
Rule (written before running): build every distance ratio in the figure (13 centres at 0, 2r, 4r on six directions;
all 78 distances, and all ratios between them). A number 'matches' if some ratio lies inside its measured range.
Chance level = the fraction of random numbers (log-uniform over the same span) that would match with the same
relative tolerance. Metatron 'fits' only if our numbers match clearly more often than random numbers do."""
import itertools, math, json, numpy as np
P = [(0.0, 0.0)] + [(d * math.cos(math.radians(60 * k)), d * math.sin(math.radians(60 * k))) for d in (2, 4) for k in range(6)]
D = sorted({round(math.dist(p, q), 9) for p, q in itertools.combinations(P, 2)})
R = sorted({round(a / b, 9) for a in D for b in D if a >= b})        # all ratios >= 1
lens = sorted(set(D) | set(R) | {round(x / 2, 9) for x in D})      # distances in units of r and of 2r too
ours = {   # dimensionless numbers our fits produced, with their measured (approx. 1-sigma) ranges
    "torsion width / fitted width (N)": (8.97, 7.7, 10.1),
    "starting angle theta_i (radians)": (2.79, 2.69, 2.89),
    "field share f_EDE (x100)": (7.8, 6.0, 9.6),
    "H0 ratio Twist / standard": (1.0385, 1.02, 1.057),
    "sound ruler ratio standard / Twist": (1.030, 1.015, 1.045),
}
rng = np.random.default_rng(1)
res = {}
L = np.array(lens)
for name, (v, lo, hi) in ours.items():
    hit = [x for x in lens if lo <= x <= hi]
    tol_lo, tol_hi = lo / v, hi / v
    span = np.exp(rng.uniform(np.log(1.0), np.log(12.0), 200000)) if v >= 1 else None
    if v < 1: span = np.exp(rng.uniform(np.log(0.01), np.log(1.0), 200000))
    chance = np.mean([np.any((L >= s * tol_lo) & (L <= s * tol_hi)) for s in span[:20000]])
    res[name] = dict(value=v, range=[lo, hi], metatron_values_in_range=hit[:6], n_hits=len(hit), chance=round(float(chance), 3))
    print(f"{name:40s} {v:>7}  hits={len(hit):2d} e.g. {[round(h,3) for h in hit[:4]]}  chance of a random number matching = {chance:.0%}")
print(len(D), "distinct distances,", len(R), "distinct ratios;", len(lens), "Metatron numbers in total")
json.dump(dict(distances=D, n_ratios=len(R), results=res), open("/home/claude/cmbwork/metatron/metatron_test.json", "w"), indent=1)
