"""The Loom's automatic checks and balances (Danny 17:44). Run before any verdict. Each check returns (ok, message).
C1 INDEPENDENCE  — readings that move together exactly under random input perturbations are the same reading (algebraic duplicates).
C2 POWER         — perturb the inputs over their allowed range; if the verdict never flips, the test cannot discriminate ("structural").
C3 VALIDATION    — the code must reproduce a known reference value before it is used (reproduce-first).
C4 NUMEROLOGY    — chance that ANY of n simple candidates lands within the target's own uncertainty band.
C5 CLAIM LINT    — overclaim words in a D-note need a cited powered test.
C6 FOUR CORNERS  — forward (theory→data), reverse (data→input), early-universe, late-universe readings must agree."""
import math, random, re
def c1_independence(readers, inputs, trials=30, tol=1e-9, seed=1):
    rnd = random.Random(seed); names = list(readers); dup = set()
    base = {k: f(inputs) for k, f in readers.items()}
    same = {(a, b): True for i, a in enumerate(names) for b in names[i + 1:]}
    for _ in range(trials):
        x = {k: v * math.exp(rnd.uniform(-0.3, 0.3)) for k, v in inputs.items()}
        val = {k: f(x) / base[k] for k, f in readers.items()}
        for (a, b) in same:
            if abs(val[a] - val[b]) > tol: same[(a, b)] = False
    dups = [p for p, s in same.items() if s]
    return (not dups, 'independent' if not dups else 'DUPLICATE readings (move together exactly): %s' % dups)
def c2_power(verdict, inputs, ranges, trials=200, seed=2):
    rnd = random.Random(seed); seen = set()
    for _ in range(trials):
        x = dict(inputs)
        for k, (lo, hi) in ranges.items(): x[k] = rnd.uniform(lo, hi)
        seen.add(verdict(x))
    return (len(seen) > 1, 'has power: verdicts seen %s' % sorted(seen) if len(seen) > 1 else 'NO POWER: verdict always %s (structural)' % seen.pop())
def c3_validate(value, reference, tol):
    return (abs(value - reference) <= tol, 'validated (%.6g vs %.6g)' % (value, reference) if abs(value - reference) <= tol else 'VOID: %.6g vs reference %.6g' % (value, reference))
def c4_numerology(target, target_frac_err, candidates):
    hits = [c for c in candidates if abs(c / target - 1) <= target_frac_err]
    # chance a random log-uniform simple ratio in [1/3, 3] lands in the band, for n candidates
    p1 = 2 * target_frac_err / math.log(9); p_any = 1 - (1 - p1) ** len(candidates)
    return (p_any < 0.05, 'chance of a match by luck = %.0f %% (n = %d, band ±%.0f %%); hits %s' % (100 * p_any, len(candidates), 100 * target_frac_err, hits))
BANNED = r'\b(proves?|confirm(s|ed)|favou?rs|strongest|resolved|derived|unique|irrefutable)\b'
def c5_lint(text, powered_refs=()):
    flags = [m.group(0) for m in re.finditer(BANNED, text, re.I)]
    return (not flags or bool(powered_refs), 'clean' if not flags else 'OVERCLAIM words %s — cite a powered test or soften' % sorted(set(f.lower() for f in flags)))
def c6_four_corners(readings, tol_frac):
    v = [x for x in readings.values() if x is not None]; missing = [k for k, x in readings.items() if x is None]
    if len(v) < 2: return (False, 'only %d corner(s); missing %s' % (len(v), missing))
    c = sorted(v)[len(v) // 2]; worst = max(abs(x / c - 1) for x in v)
    return (worst <= tol_frac and not missing, 'corners agree within %.1f %%' % (100 * worst) + ('; MISSING %s' % missing if missing else ''))
# C7 FORMULA BENCHMARKS — every physics formula used in a verdict must reproduce a textbook/literature number first.
BENCH = {
 # name: (function, inputs, reference, rel_tol, source)
 'muon_width': (lambda G, m: G ** 2 * m ** 5 / (192 * math.pi ** 3), (1.1663787e-5, 0.1056584), 2.9960e-19, 1e-2, 'PDG tau_mu 2.1970e-6 s; tree-level formula, QED correction ~0.4 % ⇒ 1 % tolerance'),
 'scalar_to_2photons_per_kappa': (lambda k, m: k ** 2 * m ** 3 / (64 * math.pi), (1.0, 1.0), 1 / (64 * math.pi), 1e-12, 'L = -(k/4) phi F^2 ⇒ Gamma = k^2 m^3 / (64 pi) per massless gauge boson'),
 'gravitino_width_allchannels': (lambda m, MP: 193 / (384 * math.pi) * m ** 3 / MP ** 2, (1.0, 1.0), 193 / (384 * math.pi), 1e-12, 'Moroi: Gamma = (193/384 pi) m^3/M_P^2 (all MSSM channels open)'),
}
def c7_benchmarks():
    out = {}
    for k, (f, args, ref, tol, src) in BENCH.items():
        v = f(*args); out[k] = (abs(v / ref - 1) <= tol, '%s: %.4g vs %.4g (%s)' % (k, v, ref, src))
    return out
