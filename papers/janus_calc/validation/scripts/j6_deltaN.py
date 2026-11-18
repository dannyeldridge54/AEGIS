# AEGIS-FP WUM6XKQXL7XY2Y7I · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J6 (locked PREREG_J6_two_field_deltaN): two-field delta-N for Janus. M_P (reduced) = 1.
Formulas fetched 16 Nov 2026 from Vernizzi & Wands, astro-ph/0603799 (ar5iv):
  Eq.(11) P_zeta = sum_I N_I^2 H*^2/(4 pi^2);  Eq.(17) n-1 = -2eps - 2/(sum N_K^2) + 2 sum V_IJ N_I N_J/(V sum N_K^2);
  Eq.(28) r = 8 P*/P_zeta = 8/sum N_K^2;  Eq.(30) -(6/5) f_NL^(4) = sum N_I N_J N_IJ/(sum N_K^2)^2.
  The lock writes (6/5) f_NL = N_a N_b N_ab/(N_c N_c)^2 (WMAP sign); VW's footnote: their sign is opposite.
  So F := sum N N N_ab/(sum N^2)^2 is the same number in both; we report F.
  Sum-separable analytic (W=U+V): Eqs.(51)-(53),(57),(61),(66)-(68), with eta^phi = U''/W (Eq.41);
  eps^phi = U'^2/(2W^2) [derived from Eq.(51) at Z_c=0 matching single-field N_phi = W/U'] and eps = eps^phi+eps^chi.
  T3 point (Sec 5.2): R = m_chi/m_phi = 1/9, Hubble exit (phi*,chi*) = (8.2, 12.9); quoted -(6/5)f^(4) = 0.008 at eps_e ~ 1.
Pivot n_s uses Eq.(17) with eps = eps_H at the slice (fixed in this header before running)."""
import sys, json, time, numpy as np; sys.path.insert(0, '.')
from tools.serapis_calc.multifield import run
from tools.janus_calc import core
t0 = time.time()
def Nof(V, g, f):
    f = np.array(f, float); v0 = -np.array(g(f))/V(f)
    s, Ne = run(V, g, f, Nmax=400, v0=v0); return Ne, s
def deltaN(V, g, H2, f, h):
    n = len(f); f = np.array(f, float); E = np.eye(n)
    N0 = Nof(V, g, f)[0]
    Na = np.array([(Nof(V, g, f+h*E[a])[0] - Nof(V, g, f-h*E[a])[0])/(2*h) for a in range(n)])
    Nab = np.zeros((n, n))
    for a in range(n):
        Nab[a, a] = (Nof(V, g, f+h*E[a])[0] - 2*N0 + Nof(V, g, f-h*E[a])[0])/h**2
        for b in range(a+1, n):
            Nab[a, b] = Nab[b, a] = (Nof(V, g, f+h*(E[a]+E[b]))[0] - Nof(V, g, f+h*(E[a]-E[b]))[0]
                                     - Nof(V, g, f-h*(E[a]-E[b]))[0] + Nof(V, g, f-h*(E[a]+E[b]))[0])/(4*h*h)
    S = Na @ Na; v0 = -np.array(g(f))/V(f); eps = 0.5*v0 @ v0
    ns = 1 - 2*eps - 2/S + 2*(Na @ H2(f) @ Na)/(V(f)*S)
    return dict(N=N0, Na=Na, Nab=Nab, ns=ns, r=8/S, F=(Na @ Nab @ Na)/S**2)
def both(V, g, H2, f, h=2e-3):
    a, b = deltaN(V, g, H2, f, h), deltaN(V, g, H2, f, h/2)
    rel = lambda x, y: float(np.max(np.abs(x-y))/max(np.max(np.abs(y)), 1e-30))
    return b, rel(a['Na'], b['Na']), abs(a['F']-b['F'])/max(abs(b['F']), 1e-30), a
L = []; P = lambda s: (L.append(s), print(s, flush=True))
# T1 single field
V1 = lambda f: 0.5*f[0]**2; g1 = lambda f: [f[0]]; H1 = lambda f: np.array([[1.0]])
d1, ra1, rf1, _ = both(V1, g1, H1, [15.3])
m = core.Model(lambda p: 0.5*p*p, lambda p: p, 30.0); c = m.spectra(d1['N'])
dns1 = abs(d1['ns']-c['ns']); dr1 = abs(d1['r']-c['r'])/c['r']
T1 = dns1 < 2e-4 and dr1 < 1e-3
P(f"T1 single m^2phi^2 phi*=15.3 N*={d1['N']:.3f}: deltaN ns {d1['ns']:.6f} r {d1['r']:.5f} F {d1['F']:.5f} | core ns {c['ns']:.6f} r {c['r']:.5f} | |dns| {dns1:.1e} |dr|/r {dr1:.1e} -> {'PASS' if T1 else 'FAIL'}")
# T2 equal mass
V2 = lambda f: 0.5*(f[0]**2+f[1]**2); g2 = lambda f: [f[0], f[1]]; H22 = lambda f: np.eye(2)
res = []
for th in [0.1, 0.5, 0.9, 1.3]:
    d, ra, rf, _ = both(V2, g2, H22, [15.3*np.cos(th), 15.3*np.sin(th)]); res.append((th, d, ra, rf))
    P(f"T2 theta={th}: N {d['N']:.4f} ns {d['ns']:.6f} r {d['r']:.5f} F {d['F']:.5f}")
spread = max(x[1]['ns'] for x in res) - min(x[1]['ns'] for x in res); dF2 = max(abs(x[1]['F']-d1['F']) for x in res)
T2 = spread < 1e-4 and dF2 < 0.01
P(f"T2 ns spread {spread:.1e}, max |F - F_single| {dF2:.1e} -> {'PASS' if T2 else 'FAIL'}")
# T3 Vernizzi-Wands R = 1/9
R = 1/9; V3 = lambda f: 0.5*f[0]**2 + 0.5*R*R*f[1]**2; g3 = lambda f: [f[0], R*R*f[1]]; H3 = lambda f: np.diag([1.0, R*R])
fs = np.array([8.2, 12.9]); d3, ra3, rf3, _ = both(V3, g3, H3, fs)
_, s = Nof(V3, g3, fs); fc = s.sol(s.t_events[0][0])[:2]
def sr(f):
    U, Vv = 0.5*f[0]**2, 0.5*R*R*f[1]**2; W = U+Vv
    ep, ec = (f[0])**2/(2*W*W), (R*R*f[1])**2/(2*W*W); return U, Vv, W, ep, ec, 1/W, R*R/W
Us, Vs, Ws, eps_p, eps_c, eta_p, eta_c = sr(fs); Uc, Vc, Wc, ep_c, ec_c, et_pc, et_cc = sr(fc); e_c = ep_c+ec_c
Zc = (Vc*ep_c - Uc*ec_c)/e_c; u = (Us+Zc)/Ws; v = (Vs-Zc)/Ws
etass = (ec_c*et_pc + ep_c*et_cc)/e_c; A = -(Wc**2/Ws**2)*(ep_c*ec_c/e_c)*(1 - etass/e_c)
den = u*u/eps_p + v*v/eps_c
F_an = 2*((u*u/eps_p)*(1 - eta_p*u/(2*eps_p)) + (v*v/eps_c)*(1 - eta_c*v/(2*eps_c)) + (u/eps_p - v/eps_c)**2*A)/den**2
ns_an = 1 - 2*(eps_p+eps_c) - 4*(u*(1 - eta_p*u/(2*eps_p)) + v*(1 - eta_c*v/(2*eps_c)))/den
tol = max(0.05*abs(F_an), 0.02); T3 = abs(d3['F']-F_an) < tol
P(f"T3 VW R=1/9 (8.2,12.9): N {d3['N']:.3f}, end (phi,chi)=({fc[0]:.3f},{fc[1]:.3f}); numeric ns {d3['ns']:.5f} r {d3['r']:.5f} F {d3['F']:.5f} | analytic Eq68 F {F_an:.5f}, Eq61 ns {ns_an:.5f} | VW quoted 0.008 | |dF| {abs(d3['F']-F_an):.1e} tol {tol:.2f} -> {'PASS' if T3 else 'FAIL'}")
# T4 Richardson
worstNa = max(ra1, ra3, *[x[2] for x in res]); worstF = max(rf1, rf3, *[x[3] for x in res])
T4 = worstNa < 1e-3 and worstF < 1e-2
P(f"T4 h vs h/2: worst rel N_a {worstNa:.1e}, worst rel F {worstF:.1e} -> {'PASS' if T4 else 'FAIL'}")
v = 'VALIDATED' if (T1 and T2 and T3 and T4) else 'NOT VALIDATED'
P(f"J6 verdict: {v}  (runtime {time.time()-t0:.0f}s)")
open('field_tests/results/janus_j6_deltaN.txt', 'w').write('\n'.join(L)+'\n')
