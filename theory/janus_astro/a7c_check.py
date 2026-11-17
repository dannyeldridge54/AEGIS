import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import gwb
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
MP, As = gwb.MP, 2.1e-9
# C1
rd = gwb.History([(1/3, math.log(1e12))])   # DEVIATIONS D1
c1 = [rd.T2(k) for k in np.geomspace(1e-3, 1e-1, 5)]; ok1 = max(abs(x-1) for x in c1) <= 1e-3
P('C1 RD plateau T2:', ' '.join(f'{x:.6f}' for x in c1), 'PASS' if ok1 else 'FAIL')
def case(name, T_R, r, phases):
    h = gwb.History(phases); fR = gwb.f_R(T_R); return name, T_R, r, h, fR
cases = []
for (eps, Hx, xr, T_R, r) in [(1.3e-4, 8.4e9, 3.4e-6, 1e6, 4.63e-4), (1.6e-4, 1.0e10, 4.5e-6, 3e6, 5.12e-4)]:
    rho_x = 3*MP**2*Hx**2; rho_R = gwb.rho_rad(T_R)
    cases.append(case(f'tau=i eps={eps} T_R={T_R:.0e}', T_R, r, [(0.0, math.log(rho_x/rho_R)), (0.6, math.log(1/xr))]))
for (T_R, r) in [(3.2e8, 4.70e-4), (3.0e9, 4.61e-4)]:
    rho_end = 1.5*math.pi**2*As*r*MP**4/2.27; rho_R = gwb.rho_rad(T_R)
    cases.append(case(f'SERAPIS-E rho T_R={T_R:.1e}', T_R, r, [(0.0, math.log(rho_end/rho_R))]))
# C2, C3 on the first tau=i case and first rho case
ok2 = ok3 = True
for idx in (0, 2):
    name, T_R, r, h, fR = cases[idx]
    kb = [1.0]
    for (w, dl) in h.phases: kb.append(kb[-1]*math.exp(dl*(1+3*w)/(6*(1+w))))
    for j, (w, dl) in enumerate(h.phases):
        lo, hi = kb[j], kb[j+1]
        if math.log10(hi/lo) < 2.2: P(f'C2 {name} band w={w}: too narrow ({math.log10(hi/lo):.1f} dec), skipped'); continue
        kc = math.sqrt(lo*hi); d = 1.02
        sl = (math.log(h.T2(kc*d)) - math.log(h.T2(kc/d)))/(2*math.log(d)); tgt = 2*(3*w-1)/(3*w+1)
        e = abs(sl - tgt); ok2 &= e <= 0.05
        tb, ta = h.T2(kc), h.T2_routeA(kc); dlog = abs(math.log10(ta) - math.log10(tb)); ok3 &= dlog <= 0.5
        P(f'C2/C3 {name} w={w} band k {lo:.3g}-{hi:.3g}: slope={sl:.4f} (target {tgt:.4f}) | T2_B={tb:.4e} T2_A={ta:.4e} dlog10={dlog:.3f}')
f8 = gwb.f_R(1e8); ok4 = abs(f8/2.65 - 1) <= 3e-2; P(f'C4 f_R(1e8 GeV) = {f8:.4f} Hz vs 2.65', 'PASS' if ok4 else 'FAIL')
P('A7c', 'VALIDATED' if ok1 and ok2 and ok3 and ok4 else 'NOT VALIDATED', f'(C1 {ok1}, C2 {ok2}, C3 {ok3}, C4 {ok4})')
P('Application: Omega_GW h^2 today (route B)')
for name, T_R, r, h, fR in cases:
    kend = h.k_end(); fend = fR*kend
    plateau = gwb.omega_gw_h2(1e-3, 1.0, r)
    row = []
    for f in [1e-9, 1e-3, 1e-1, 1, 10, 100, 1e3]:
        k = f/fR
        T2 = 1.0 if k < 1e-3 else (h.T2(k) if k <= kend*1e-3 else float('nan'))   # DEVIATIONS D1
        row.append(f'{f:g} Hz: {gwb.omega_gw_h2(f, T2, r):.2e}')
    P(f'  {name}: r={r} f_R={fR:.3g} Hz f_end~{fend:.3g} Hz plateau={plateau:.2e}; ' + '; '.join(row))
open('field_tests/results/janus_astro_a7c.txt', 'w').write('\n'.join(out) + '\n')
