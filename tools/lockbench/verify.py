"""L-5 verification kit. Formulas [fetched 2026-11-17: Celik et al. 2008 ASME J. Fluids Eng. 130 078001, as reproduced on volupe.com GCI page]:
 eps21 = phi2 - phi1, eps32 = phi3 - phi2, s = sign(eps32/eps21); p ln r21 = ln|eps32/eps21| + ln[(r21^p - s)/(r32^p - s)] (fixed-point solve);
 phi_ext = (r21^p phi1 - phi2)/(r21^p - 1); e_a = |(phi1-phi2)/phi1|; e_ext = |(phi_ext - phi1)/phi_ext|; GCI_fine = 1.25 e_a/(r21^p - 1).
Grid 1 = finest. Also: observed_order on a sequence with known exact value, two_solver agreement, mms_orders for manufactured/exact solutions."""
import math
def gci3(phi1, phi2, phi3, r21, r32, Fs=1.25, it=200):
    e21, e32 = phi2 - phi1, phi3 - phi2
    if e21 == 0 or e32 == 0: return dict(ok=False, why='zero difference (converged or degenerate)')
    s = 1.0 if e32/e21 > 0 else -1.0; R = e32/e21
    if not ((s > 0 and R > math.log(r32)/math.log(r21)) or (s < 0 and abs(R) > 1)) and abs(r21 - r32) > 1e-12:
        exist = False
    else: exist = True
    p = abs(math.log(abs(R)))/math.log(r21)
    for _ in range(it):
        q = math.log((r21**p - s)/(r32**p - s)) if (r21**p - s) > 0 and (r32**p - s) > 0 else 0.0
        pn = abs(math.log(abs(R)) + q)/math.log(r21)
        if abs(pn - p) < 1e-12: p = pn; break
        p = pn
    ext = (r21**p*phi1 - phi2)/(r21**p - 1); ea = abs((phi1 - phi2)/phi1)
    return dict(ok=True, p=p, oscillatory=s < 0, exists=exist, phi_ext=ext, e_a=ea, e_ext=abs((ext - phi1)/ext), GCI_fine=Fs*ea/(r21**p - 1))
def observed_order(hs, vals, exact):
    """pairwise orders from errors vs a known exact value: p_i = ln(e_i/e_{i+1})/ln(h_i/h_{i+1})."""
    e = [abs(v - exact) for v in vals]
    return [math.log(e[i]/e[i+1])/math.log(hs[i]/hs[i+1]) for i in range(len(e) - 1)], e
def two_solver(a, b, tol_rel):
    d = abs(a - b)/max(abs(a), abs(b)); return dict(rel=d, ok=d <= tol_rel)
def mms_orders(solve, hs, exact):
    """solve(h) -> approximate value(s); exact: value(s). Returns per-quantity observed orders."""
    S = [solve(h) for h in hs]; S = [s if isinstance(s, (list, tuple)) else [s] for s in S]; X = exact if isinstance(exact, (list, tuple)) else [exact]
    return [observed_order(hs, [s[k] for s in S], X[k])[0] for k in range(len(X))]
