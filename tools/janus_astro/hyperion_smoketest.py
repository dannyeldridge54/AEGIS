"""Hyperion 1.1 smoke test: fast checks of validated results against their recorded values (no new physics).
Run from the repo root:  python tools/janus_astro/hyperion_smoketest.py   (~1 min)"""
import sys, math, time, warnings
warnings.filterwarnings('ignore'); sys.path.insert(0, '.'); sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'field_tests/scripts')
checks = []
def check(name, got, ref, tol, src):
    ok = abs(got/ref - 1) <= tol; checks.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {got:.6g} vs {ref:.6g} (tol {tol:.1%}; {src})", flush=True)
t0 = time.time()
# 1. Relic: Born Omega h^2 at the Born thermal mass with the Saikawa-Shirai EOS (R2e-b, D1238)
from r2e_b_gstar import omega
check("relic Born Omega h^2 at M = 2252.1 GeV", omega(2252.1, lambda x: 1.0)[0], 0.1205, 0.005, "D1238")
# 2. Star Mapper: LSR orbit in McMillan17 is circular (D10, D1197)
from tools.janus_astro import mapper_feed as F
o = F.orbit_params_galpy([-8.21], [0.0], [0.0208], [0.0], [233.1], [0.0], pot='McMillan17')
check("McMillan17 LSR r_apo/R0", o['rapo'][0]/8.21, 1.0, 0.005, "D1197")
# 3. galpy path reproduces Hyperion's own MWPotential2014 integrator (D9, D1196)
s = (-8.5, 1, 0.3, 30, 200, 20); g = F.orbit_params_galpy(*[[c] for c in s], pot='MWPotential2014'); h = F.orbit_params(*s, t_gyr=3.0)
check("galpy vs galaxy.py r_peri (MWP2014)", g['rperi'][0], h['rperi'], 0.001, "D1196")
# 4. 7PN tidal SPA coefficient equals Mandal et al. 2412.01706 Eq. 4.48 (D1211)
from tools.janus_astro import gw
m1, m2, L1, L2, f = 1.4*1.98847e30, 1.3*1.98847e30, 400.0, 600.0, 400.0
d7 = gw.taylorf2_tidal_dphase_hfb(f, m1, m2, L1, L2, order=7) - gw.taylorf2_tidal_dphase_hfb(f, m1, m2, L1, L2, order=6.5)
M = m1 + m2; nu = m1*m2/M**2; D = (m1 - m2)/M; X1, X2 = m1/M, m2/M
mp = 0.5*(X2*X1**4*L1 + X1*X2**4*L2); mm = 0.5*(X2*X1**4*L1 - X1*X2**4*L2); v = (math.pi*gw.G*M*f/gw.c**3)**(1/3)
ref = -(9*v**5/(16*nu**2))*((136190135/27433728 + 978554825/4572288*nu - 281935/6048*nu**2 + 5/3*nu**3)*mp + D*(136190135/27433728 + 213905/2592*nu + 1585/1296*nu**2)*mm)*v**4
check("7PN tidal SPA term (gw.py vs Mandal+ 2412.01706 Eq. 4.48, re-implemented)", d7, ref, 1e-9, "D1211")
# 5. IGS line f_max at 1 TeV for Burkert B0/D1 at rho_sun 0.4 (A2n, D1322) -- quick J
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
import serapis_inputs as SI
Jann = lambda rho: J.J_route_B(rho, 8.178, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, 8.178, psi_max_deg=0.5, b_mask_deg=0.0)
jr = Jann(J.normalise(J.burkert(3.37), 0.40, 8.178))/Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178))
sv0 = N.wino_s_nlo(1000.0, v=1e-3, nlo=False, off_factor=math.sqrt(2))
sv = 2*sv0[1]**2*math.pi*N.ALPHA**2/1e6*0.389379e-27*2.99792458e10*(1 + N.ALPHA2*N.CW2/N.ALPHA)
check("1 TeV wino f_max (Burkert B0/D1, rho_sun 0.4, LO)", math.sqrt(2.3e-28/(sv*0.794*jr)), 0.286, 0.01, "D1322")
# 6. Thermal-fraction bracket at 1 TeV (D1152)
check("wino fraction upper edge at 1 TeV", SI.wino_fraction(1.0)[1], (1/2.207)**2, 1e-9, "D1152")
print(f"{sum(checks)}/{len(checks)} PASS in {time.time()-t0:.0f} s"); sys.exit(0 if all(checks) else 1)
