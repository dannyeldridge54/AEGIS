"""D406 (locked PREREG_D406_BALANCE): first centre (balance) check of the two-ladder process. AI-assisted.
Right ladder (D396): pinning releases entropy, dilution D. Left ladder: N* = 57.2 (D391). Cross-effect: ΔN* = −(1/3) ln D (comoving scales
must exit later after extra entropy). n_s from the Twist table (bridges_d403 values, linear interpolation in N*); r = 3(1−n_s)² + B1.
D from pinning_d396.chain for x_E = 29.598 (the robust capture point), λ ∈ {0.004, 0.01, 0.033}, v ∈ {1e9, 1e10, 3e10, 1e11} GeV (v < T_x = 1.45e11)."""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pinning_d396 as P
tab = [(55.0, 0.96371), (56.0, 0.96435), (57.0, 0.96498), (57.2, 0.96510), (58.0, 0.96558), (60.0, 0.96673)]
def ns_of(N):
    for (a, na), (b, nb) in zip(tab, tab[1:]):
        if a <= N <= b: return na + (nb - na) * (N - a) / (b - a)
    (a, na), (b, nb) = (tab[0], tab[1]) if N < tab[0][0] else (tab[-2], tab[-1])
    return na + (nb - na) * (N - a) / (b - a)
xE, Tx, dp = 29.598, 1.451e11, 9.335e-3
print("λ      v[GeV]   trapped  T_d[GeV]  D        ΔN*     N*      n_s      σ(SPA)  σ(SPA+DESI)  right-ladder pass")
for lam in (0.004, 0.01, 0.033):
    for v in (1e9, 1e10, 3e10, 1e11):
        tr, kv, A, mx, Td, rc, D = P.chain(lam, xE, Tx, dp, v)
        dN = -math.log(D) / 3; N = 57.2 + dN; ns = ns_of(N)
        ok = tr and Td >= 5e-3 and D <= 1e3
        print(f"{lam:5.3f}  {v:8.1e}  {str(tr):5s}  {Td:9.2e}  {D:8.2e}  {dN:+.3f}  {N:6.2f}  {ns:.5f}  {(0.9684-ns)/0.0030:5.2f}   {(0.9728-ns)/0.0027:5.2f}        {ok}")
