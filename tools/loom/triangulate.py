"""NOTE (referee D1935): for a DETERMINISTIC boolean, bracket() is plain bisection (x4 per round); its null rounds are vacuous
(they only start once width < res). The 7-null rule carries evidence only for multi-reader / stochastic readings (fixed_point,
or bracket with independent readers / seeds). Report bracket results as "bisection to <res>", not as 7-null convergence.
Loom rule 6h: triangulate to convergence, stopping after 7 null rounds in a row (Danny 16:04-16:05).
A round is NULL when the centre moves < res AND the spread shrinks < 10 %.
bracket(f, lo, hi, res): edge where boolean f flips; 3 readings per round at the quarter points.
fixed_point(readers, x0, res): 3 readers x -> estimate; centre = median; x <- centre."""
import statistics
NULLS = 7
def bracket(f, lo, hi, res, maxit=200, log=None):
    flo = f(lo); c_prev = (lo + hi) / 2; w_prev = hi - lo; nulls = 0; it = 0
    for it in range(1, maxit + 1):
        pts = [lo + (hi - lo) * k / 4 for k in (1, 2, 3)]; vals = [f(p) for p in pts]
        seq = [(lo, flo)] + list(zip(pts, vals)) + [(hi, not flo)]
        for (a, fa), (b, fb) in zip(seq, seq[1:]):
            if fa != fb: lo, hi, flo = a, b, fa; break
        c, w = (lo + hi) / 2, hi - lo
        null = abs(c - c_prev) < res and (w_prev - w) < 0.1 * w_prev if w > res else abs(c - c_prev) < res
        nulls = nulls + 1 if null else 0
        if log is not None: log.append(dict(round=it, lo=lo, hi=hi, null=bool(null), readings=list(zip(pts, map(bool, vals)))))
        c_prev, w_prev = c, w
        if nulls >= NULLS: break
    return (lo + hi) / 2, hi - lo, it
def fixed_point(readers, x0, res, maxit=200, log=None):
    x, s_prev, nulls, it = x0, None, 0, 0
    for it in range(1, maxit + 1):
        r = [g(x) for g in readers]; c = statistics.median(r); s = max(r) - min(r)
        null = abs(c - x) < res and (s_prev is None or (s_prev - s) < 0.1 * max(s_prev, 1e-300))
        nulls = nulls + 1 if null else 0
        if log is not None: log.append(dict(round=it, x=x, readings=r, centre=c, spread=s, null=bool(null)))
        x, s_prev = c, s
        if nulls >= NULLS: break
    return x, s, it
