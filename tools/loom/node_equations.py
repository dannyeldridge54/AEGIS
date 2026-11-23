"""D2144: every negative-space node's equation at the wall and pulled x1.5 / /1.5. PREREG_D2144."""
import json, math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
MP = 2.435e18; f = 1.5; L = lambda x, b: math.log(b/x)
rows = []
def node(n, eq, knob, base, fn, bound_txt, margin):
    vals = {d: fn(base*k) for d, k in (('in', 1/f), ('wall', 1.0), ('out', f))}
    ms = {d: margin(v) for d, v in vals.items()}
    rows.append(dict(node=n, equation=eq, knob=knob, knob_base=base, value=vals, bound=bound_txt, margin=ms,
                     holds={d: (m is None or m >= 0) for d, m in ms.items()}))
# N2 neutrinos: Sum m_nu = m2 + m3 (m1 = 0, normal ordering) [S]; the knob is the lightest-mass offset, so the sum itself is pulled
node('N2', 'Sum m_nu = m1 + sqrt(m1^2 + dm21^2) + sqrt(m1^2 + dm31^2)  [S]; DESI DR2+CMB bound', 'Sum m_nu (eV)', 0.0587, lambda x: x, '< 0.064 eV', lambda v: L(v, 0.064))
# N3 mu -> e gamma [E mass insertion]
node('N3', 'BR = (alpha^3 pi / G_F^2) delta12^2 tan^2(beta) / m_s^4  [E], delta12 = 1, tan(beta) = 4', 'm_s (GeV)', 2.5e5,
     lambda m: (1/137.036)**3*math.pi/1.1664e-5**2*16/m**4, 'MEG II < 1.5e-13', lambda v: L(v, 1.5e-13))
# N4 tau_q dilution [R D1766, S decay]: D = T_R phi0^2 / (6 T_d), T_d ∝ m^{3/2}
def D(m): Td = (90/(math.pi**2*106.75))**0.25*math.sqrt(m**3/(4*math.pi*MP**2)*MP); return 1.34e9/(6*Td)
node('N4a', 'D = T_R phi0^2 / (6 T_d), T_d = (90/pi^2 g*)^(1/4) sqrt(Gamma M_P), Gamma = m^3/(4 pi M_P^2)  [R+S]', 'm_tau_q (GeV)', 2e10, D, 'D <= 1e3', lambda v: L(v, 1e3))
node('N4b', 'Omega_w h^2 = 2.744e8 m_w min(Y_3/2, Y_cap), Y_3/2 = 1.5 Br T_d/m  [S], generic Br = 0.01 (EHT)', 'Br_3/2', 0.01,
     lambda br: 2.744e8*700*min(1.5*br*2.764e5/2e10, 4.8e-11), 'Omega_w h^2 <= 0.036', lambda v: L(v, 0.036))
# N5 gravitino lifetime [S]: tau ∝ m32^-3, base 1.4e-3 s at 2.6e5 GeV (D1946)
node('N5', 'tau_3/2 = 1.4e-3 s (2.6e5 GeV / m3/2)^3  [S scaling, R normalisation]', 'm3/2 (GeV)', 2.6e5, lambda m: 1.4e-3*(2.6e5/m)**3, 'tau < 0.1 s (BBN)', lambda v: L(v, 0.1))
node('N5w', 'm_wino = m3/2 / 375  [R anomaly mediation]', 'm3/2 (GeV)', 2.6e5, lambda m: m/375, 'm_w > 670 GeV (ATLAS 2603.08315)', lambda v: L(670, v))
# N6 r on the plateau [S]: r = r0 (N0/N)^2 with N0 = 2/(1-n_s); pulled through N*
node('N6', 'r = 8/(beta^2 N*^2) on the plateau, r0 = 5.4e-4 at N* = 68  [S]', 'N* (e-folds)', 68.0, lambda N: 5.4e-4*(68/N)**2, 'BK18 r < 0.036', lambda v: L(v, 0.036))
# N7 proton [S scaling]: tau_p ∝ M_X^4 / (alpha_G^2 m_p^5), base 1.6e35 yr
node('N7', 'tau_p = 1.6e35 yr (M_X / M_X0)^4  [S scaling, R normalisation]', 'M_X / M_X0', 1.0, lambda x: 1.6e35*x**4, 'Super-K > 2.4e34 yr', lambda v: L(2.4e34, v))
node('N7e', 'd_e = e m_e (alpha/4pi) sin(phi) / m_s^2  [E one loop], sin(phi) = 1', 'm_s (GeV)', 2.5e5, lambda m: 0.511e-3/137.036/(4*math.pi)/m**2*1.973e-14, 'JILA < 4.1e-30 e cm', lambda v: L(v, 4.1e-30))
# N8 reheating clock [R D1759]
node('N8', 'Delta N* = (1/3) ln(T_R / T_R0)  [R]', 'T_R / T_R0', 1.0, lambda x: math.log(x)/3, 'clock tie (no bound)', lambda v: None)
# N9 alpha leak [R D1887]
node('N9', 'Delta alpha / alpha = zeta_alpha |Delta phi|, zeta_alpha = 3.8e-10, |Delta phi| = 0.19 (b = 0)  [R]', 'zeta_alpha', 3.8e-10, lambda z: z*0.193, 'quasars < 1e-6', lambda v: L(v, 1e-6))
# N12 species room [S]: H = pi sqrt(A_s r / 2) M_P, N_max = (M_P / H)^2
node('N12', 'N_species < (M_P/H)^2, H = pi sqrt(A_s r / 2) M_P  [S]', 'r', 5.4e-4, lambda r: (MP/(math.pi*math.sqrt(2.1e-9*r/2)*MP))**2, 'more room than the visible + hidden species (~1e3)', lambda v: L(1e3, v))
# N13 refined dS [S] along the thread: slope and curvature at today's u0 = 0.272 (path min 0.157 for slope)
node('N13s', '|V\'|/V = beta u/(1-u), beta = 2 sqrt 2  [S], evaluated at the path minimum u_i', 'u_i', 0.1575, lambda u: 2*math.sqrt(2)*u/(1-u), 'slope >= sqrt(2/3)', lambda v: L(math.sqrt(2/3), v))
node('N13c', 'V\'\'/V = -beta^2 u/(1-u)  [S], at u_i', 'u_i', 0.1575, lambda u: -8*u/(1-u), 'V\'\'/V <= -1 (c\' = 1)', lambda v: L(1.0, -v))
out = dict(rows=rows, open=['N1 rung-state masses (no equation yet)', 'N14 pre-inflation (E10 billiard)', 'N16 flux -> D3 charge map (record: |M| = 9 gives 46 vs chi/24 = 2; no derived scaling)'],
           clock_rows_from='D2143a anchored: u_i x/÷1.5 -> +28.6 / -10.6 Myr; b: -0.025 -> -50 Myr, +0.025 collapses',
           trust=['N8 dNeff = 0', 'N11 TCC flag on r', 'N15 Montgomery (no knob)'])
json.dump(out, open('field_tests/results/d2144_node_equations.json', 'w'), indent=1, default=float)
for r in rows:
    print(r['node'].ljust(5), '| in %-10.3g wall %-10.3g out %-10.3g | margin' % (r['value']['in'], r['value']['wall'], r['value']['out']),
          {k: (None if v is None else round(v, 2)) for k, v in r['margin'].items()}, '| holds', r['holds'])
