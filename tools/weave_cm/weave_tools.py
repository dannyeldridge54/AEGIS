"""Weave tools for CubeMind's proposer/self-check (20 Nov 2026). Pure numpy/scipy/mpmath, fast, deterministic.
Every output carries 'label': P (Weave prediction), F (fitted), A (assumed/hosted), S (standard physics), E (estimate).
Sources: D1727-D1748 (theory/pending_docs/D72_D75_weak_spots.md), papers doi:10.5281/zenodo.24399408, 24399447, 24396665."""
import math, cmath, json
import numpy as np

C_RUNG = math.sqrt(3) * 0.0145          # fitted normalisation (Novichkov-Penedo-Petcov 2201.02020), 1/16 = their 0.0625
RUNG_COMPUTED = {1: 0.02395, 2: 0.01228, 3: 0.00825, 4: 0.00622, 5: 0.00499, 6: 0.00416, 7: 0.00357, 8: 0.00313, 9: 0.00278,
                 10: 0.00251, 11: 0.00228, 12: 0.00209, 13: 0.00193, 14: 0.00179, 15: 0.00167, 16: 0.00157, 24: 0.00105, 32: 0.00079}
MZ_MASSES = dict(u=1.29e-3, d=2.80e-3, s=55.7e-3, c=0.629, b=2.794, t=169.0)      # GeV at M_Z (D1728 inputs)
LEPTONS = dict(e=0.51099895, mu=105.6583755, tau=1776.93)                            # MeV, PDG pole


def weave_rung(a):
    """|eps_m| = |tau_m - rho| of the SUGRA (m,0) CP-violating minimum. Formula + directly computed value (Q11, D1736)."""
    m = int(a['m']); f = C_RUNG / (m + 1 / 16)
    return dict(m=m, eps_formula=f, eps_computed=RUNG_COMPUTED.get(m), arg_deg=50.0 if m <= 14 else None,
                m2_over_m3_band=[f / 3, 3 * f], m1_over_m3_band=[(f / 3) ** 2, (3 * f) ** 2], label='P (formula fitted, minima computed)',
                note='phase resolved only for m<=14; minima are AdS; occupied: rung 1 down quarks, rung ~8 (68%: 5-14) up quarks')


def weave_rung_of(a):
    """Which rung a 3-generation family (m1<m2<m3, any units) sits on. Q7 rule: both e_a=m2/m3 and e_b=sqrt(m1/m3) within x3 of eps_m."""
    m1, m2, m3 = sorted(float(x) for x in a['masses'])
    ea, eb = m2 / m3, math.sqrt(m1 / m3); g = math.sqrt(ea * eb)
    match = [m for m in range(1, 65) if all(C_RUNG / (m + 1 / 16) / 3 <= x <= 3 * C_RUNG / (m + 1 / 16) for x in (ea, eb))]
    mstar = C_RUNG / g - 1 / 16
    return dict(e_a=ea, e_b=eb, g=g, rung_estimate=mstar, matching_rungs=match, on_ladder=bool(match),
                label='A (structure; O(1) couplings smear the rung by ~x3)')


def weave_koide(a):
    """Koide Q = sum m / (sum sqrt m)^2 and Brannen amplitude/phase (D1595 convention, delta mod 2pi/3)."""
    m = np.array(sorted(float(x) for x in a['masses'])); v = np.sqrt(m); mu = v.mean()
    c = ((v / mu - 1) * np.exp(-2j * np.pi * np.arange(3) / 3)).sum()
    return dict(Q=float(m.sum() / v.sum() ** 2), A=float(2 * abs(c) / 3), delta=float(np.mod(np.angle(c), 2 * np.pi / 3)),
                lepton_reference=dict(Q=0.6666645, delta=0.222225), label='S (Koide 1982); Weave reads Q=2/3 as Z3 equipartition at rho')


def weave_koide_slip(a):
    """Median |Delta Q| when a Koide circulant sqrt(M) is slipped by |eps| with random O(1) non-circulant terms (Q10, D1737)."""
    eps = float(a['eps']); n = int(a.get('n', 20000)); rng = np.random.default_rng(int(a.get('seed', 7)))
    m = np.array([LEPTONS['e'], LEPTONS['mu'], LEPTONS['tau']]); v = np.sqrt(m)
    F = np.exp(-2j * np.pi * np.outer(range(3), range(3)) / 3) / np.sqrt(3); S0 = F.conj().T @ np.diag(v) @ F
    Q0 = m.sum() / v.sum() ** 2; mag = np.exp(rng.uniform(np.log(1 / 3), np.log(3), (n, 3, 3))); ph = np.exp(2j * np.pi * rng.random((n, 3, 3)))
    s = np.linalg.svd(S0[None] + eps * v.mean() * mag * ph, compute_uv=False) ** 2
    d = np.abs(s.sum(1) / np.sqrt(s).sum(1) ** 2 - Q0)
    return dict(eps=eps, median_dQ=float(np.median(d)), frac_within_3sigma=float((d <= 2.3e-5).mean()), koide_tolerance=2.3e-5,
                label='E (linear response, random O(1) coefficients)')


def weave_tauq(a):
    """Heavy quark modulus window (Q4, D1730): gravitational decay, dilution D, n_s shift."""
    M, p0 = float(a['mass_GeV']), float(a.get('phi0', 1.0)); MP, TR, Ns = 2.435e18, 1.34e9, 55.0
    G = M ** 3 / (4 * math.pi * MP ** 2); g = 10.75 if (90 / (math.pi ** 2 * 10.75)) ** .25 * math.sqrt(G * MP) < 1 else 80
    Td = (90 / (math.pi ** 2 * g)) ** .25 * math.sqrt(G * MP); D = max(1.0, TR * p0 ** 2 / 6 / Td); dns = abs(2 * (-math.log(D) / 3) / Ns ** 2)
    return dict(T_dec_GeV=Td, dilution=D, delta_ns=dns, allowed=(Td >= 5e-3 and D <= 1e3 and dns <= 0.003), H_inf_GeV=5.2e12,
                label='A (hosted mechanism; window edges uncertain x2)')


# ---- A4 level-3 near-omega quark matrices (Petcov-Tanimoto 2212.13336), for CKM checks on rung pairs (Q8/Q12) ----
_YC = {}
def _Y(t):
    if t in _YC: return _YC[t]
    import mpmath as mp
    mp.mp.dps = 20; W = mp.e ** (2j * mp.pi / 3)
    def dl(x):
        q = mp.e ** (2j * mp.pi * x); return (mp.pi * 1j / 12) * (1 - 24 * mp.nsum(lambda n: n * q ** n / (1 - q ** n), [1, mp.inf]))
    t = mp.mpc(t); a, b, c, d = dl(t / 3), dl((t + 1) / 3), dl((t + 2) / 3), dl(3 * t)
    y = np.array([complex((1j / (2 * mp.pi)) * (a + b + c - 27 * d)), complex((-1j / mp.pi) * (a + W ** 2 * b + W * c)), complex((-1j / mp.pi) * (a + W * b + W ** 2 * c))])
    _YC[t] = y / y[0]; return _YC[t]
_TAU = {1: -0.484440 + 0.884238j, 8: -0.497988 + 0.868420j, 9: -0.498207 + 0.868153j, 10: -0.498421 + 0.867971j, 13: -0.498737 + 0.867484j}


def _mat(t, model, p):
    Y1, Y2, Y3 = _Y(t)
    Y4 = np.array([Y1 * Y1 - Y2 * Y3, Y3 * Y3 - Y1 * Y2, Y2 * Y2 - Y1 * Y3])
    Y6 = np.array([Y1 ** 3 + 2 * Y1 * Y2 * Y3, Y1 ** 2 * Y2 + 2 * Y2 ** 2 * Y3, Y1 ** 2 * Y3 + 2 * Y3 ** 2 * Y2])
    Y6p = np.array([Y3 ** 3 + 2 * Y1 * Y2 * Y3, Y3 ** 2 * Y1 + 2 * Y1 ** 2 * Y2, Y3 ** 2 * Y2 + 2 * Y2 ** 2 * Y1])
    A = lambda v: np.array([v[0], v[2], v[1]]); B = lambda v: np.array([v[1], v[0], v[2]]); Cc = lambda v: np.array([v[2], v[1], v[0]])
    g = p.get('g_abs', 1.0) * cmath.exp(1j * p.get('g_arg', 0.0))
    if model == 'w642':
        rows = [A(Y6 + g * Y6p), B(Y4), Cc(np.array([Y1, Y2, Y3]))]
    else:
        f = p.get('f_abs', 1.0) * cmath.exp(1j * p.get('f_arg', 0.0))
        Y8 = (Y1 ** 2 + 2 * Y2 * Y3) * Y4; Y8p = (Y3 ** 2 + 2 * Y1 * Y2) * np.array([Y4[2], Y4[0], Y4[1]])
        rows = [A(Y8 + f * Y8p), B(Y6 + g * Y6p), Cc(Y4)]
    return np.diag([1.0, p.get('r1', 1.0), p.get('r2', 1.0)]) @ np.array(rows)


def weave_ckm(a):
    """Quark mass ratios + |V| + J for down on rung md, up on rung mu (rungs 1,8,9,10,13) with given O(1) couplings.
    model 'w642' (Q8) or 'w864' (Q12). Targets at M_Z: ms/mb .0199, md/mb 1.0e-3, mc/mt 3.72e-3, mu/mt 7.6e-6, Vus .225, Vcb .0418, Vub .00369, J 3.08e-5."""
    model = a.get('model', 'w864'); Md = _mat(_TAU[int(a.get('rung_d', 1))], model, a.get('down', {})); Mu = _mat(_TAU[int(a.get('rung_u', 8))], model, a.get('up', {}))
    def left(M):
        e, V = np.linalg.eigh(M.conj().T @ M); i = np.argsort(e); return np.sqrt(np.abs(e[i])), V[:, i]
    md, Ud = left(Md); mu, Uu = left(Mu); V = Uu.conj().T @ Ud; Ab = np.abs(V)
    return dict(ms_mb=md[1] / md[2], md_mb=md[0] / md[2], mc_mt=mu[1] / mu[2], mu_mt=mu[0] / mu[2], Vus=Ab[0, 1], Vcb=Ab[1, 2], Vub=Ab[0, 2],
                J=float(abs(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))),
                best_known=dict(model='w864', chi2=5.8, fails='ms_mb 0.54x, Vcb 1.27x, Vub 0.73x'), label='A (hosted; fit, not prediction)')


# ---- from quarks to the proton and to chemistry (standard physics, so the loop can propagate a Weave change) ----
def weave_proton(a):
    """Proton-mass response to quark-mass changes via sigma terms (standard QCD): dm_p = sigma_piN*(dmhat/mhat) + sigma_s*(dms/ms).
    sigma_piN 45-60 MeV (lattice vs dispersive tension), sigma_s ~ 40 MeV. Inputs: fractional changes of mhat=(mu+md)/2 and ms."""
    fl, fs = float(a.get('dmhat_over_mhat', 0.0)), float(a.get('dms_over_ms', 0.0)); out = {}
    for s_pin in (45.0, 59.0):
        out[f'dmp_MeV_sigmaPiN_{int(s_pin)}'] = s_pin * fl + 40.0 * fs
    out.update(m_p_MeV=938.272, note='most of m_p is QCD binding (Lambda_QCD), not quark mass; the Weave does not predict Lambda_QCD', label='S')
    return out


def weave_atomic(a):
    """Atomic/molecular scales from m_e, alpha, m_p (standard QED/chemistry): Rydberg, Bohr radius, H2 vibration scaling, mu=m_p/m_e.
    Lets the loop ask: if a Weave change moved m_e or m_p by x, how do molecules move?"""
    me = float(a.get('m_e_MeV', LEPTONS['e'])); al = float(a.get('alpha', 1 / 137.035999)); mp = float(a.get('m_p_MeV', 938.272))
    hbarc = 197.3269804; mu_red = me * mp / (me + mp)
    Ry = 0.5 * mu_red * al ** 2 * 1e6   # eV
    a0 = hbarc / (me * al) * 1e-15 * 1e10   # Angstrom (infinite-mass)
    mu = mp / me
    return dict(Rydberg_eV_H=Ry, bohr_radius_A=a0, mu_p_over_e=mu, H2_vib_scale_rel=(1836.15267 / mu) ** 0.5, H2_bond_rel=1.0 * (LEPTONS['e'] / me),
                note='vibrational frequencies scale as mu^-1/2, rotational as mu^-1, bond lengths as a0 ~ 1/(m_e alpha)', label='S')


# ---- both directions: the i-side / arc of the twin ladder, back in time (dimension ladder), forward (negative space) ----
def _V_sugra(x, y, m, n):
    N = np.arange(1, 41)
    def sig(k): return np.array([sum(d ** k for d in range(1, q + 1) if q % d == 0) for q in N], float)
    global _SIG
    try: S1, S3, S5 = _SIG
    except NameError: _SIG = (sig(1), sig(3), sig(5)); S1, S3, S5 = _SIG
    t = complex(x, y); q = np.exp(2j * np.pi * t); qn = q ** N
    E2 = 1 - 24 * np.sum(S1 * qn); E4 = 1 + 240 * np.sum(S3 * qn); E6 = 1 - 504 * np.sum(S5 * qn)
    eta = np.exp(2j * np.pi * t / 24) * np.prod(1 - qn); j = 1728 * E4 ** 3 / (E4 ** 3 - E6 ** 2); jp = -2j * np.pi * j * E6 / E4
    H2 = abs(j - 1728) ** m * (abs(j) ** (2 * n / 3) if n else 1)
    dl = (m / 2) * jp / (j - 1728) + ((n / 3) * jp / j if n else 0) - (1j * np.pi / 2) * E2 + 3j / (2 * y)
    return (2 * y) ** -3 * H2 / abs(eta) ** 12 * ((4 * y * y / 3) * abs(dl) ** 2 - 3)


def weave_arc(a):
    """Minimum of the SUGRA class (m,n) (W ~ (j-1728)^(m/2) j^(n/3) / eta^6, K = -3 ln(2 Im tau)), computed directly (Q11 method, D1736).
    n=0: CP-violating rung near rho; m=0: at i; both > 0: on the CP-conserving arc |tau| = 1, position set mainly by m:n."""
    from scipy.optimize import minimize
    m, n = int(a.get('m', 1)), int(a.get('n', 0)); best = None
    for x0 in np.linspace(-0.49, -0.02, 8):
        for y0 in (0.88, 0.95, 1.05, 1.3):
            if x0 * x0 + y0 * y0 < 1: continue
            f = lambda v: 1e9 if (v[1] <= .3 or v[0] * v[0] + v[1] * v[1] < 1 - 1e-12 or not -0.5 <= v[0] <= 0) else _V_sugra(v[0], v[1], m, n)
            r = minimize(f, [x0, y0], method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-14, maxiter=3000))
            if best is None or r.fun < best.fun: best = r
    t = complex(*best.x); rho = complex(-0.5, math.sqrt(3) / 2)
    on_arc = abs(abs(t) - 1) < 1e-3
    return dict(m=m, n=n, tau_re=t.real, tau_im=t.imag, abs_tau=abs(t), dist_rho=abs(t - rho), dist_i=abs(t - 1j), on_arc=on_arc,
                cp='conserving' if (on_arc or abs(t.real) < 1e-4 or abs(t.real + 0.5) < 1e-4) else 'violating', V_min=float(best.fun),
                label='P (computed minimum of a fitted SUGRA class; AdS)')


def weave_rladder(a):
    """Back in time: the dimension at horizon exit read from r (r_D = r_10 * 8/(D-2), r_10 = 5.41e-4; exact MS gives r_6 = 1.069e-3)."""
    D = int(a.get('D', 10)); r10 = 5.41e-4
    return dict(D=D, r=r10 * 8 / (D - 2), r_exact={10: 5.41e-4, 6: 1.069e-3}.get(D), detectable_by='LiteBIRD/CMB-S4-class sigma_r ~ 5e-4 to 1e-3',
                label='P (r ladder; n_s is fitted, r is the prediction)')


def weave_negspace(a):
    """Forward/negative space: switch redshift of the effective dark energy when the thread couples to dark matter (D1716-D1717):
    (1+z_dag)^3 = Om_phi / [Om_c (e^{|b| dphi} - 1)]. NOTE: the coupling was NOT detected on full Planck (D1725)."""
    b, dphi = abs(float(a.get('b', 0.074))), float(a.get('dphi', 0.639)); Op, Oc = float(a.get('Om_phi', 0.702)), float(a.get('Om_c', 0.249))
    x = Op / (Oc * (math.exp(b * dphi) - 1)); z = x ** (1 / 3) - 1
    prof = {str(zz): round((Op - Oc * (1 + zz) ** 3 * (math.exp(b * dphi) - 1)) / (Op - Oc * (math.exp(b * dphi) - 1)), 4) for zz in (0, 1, 2, 3, 4, 6)}
    return dict(z_switch=z, rhoDEeff_over_today=prof, label='E (closed form, 2% vs full background); coupling not detected (fail, D1725)')


def weave_basic(a):
    """Closed-form Weave/standard relations used across sectors (for CubeMind's own derivations to be checked against):
    q = 'Omega_nu_h2' {sum_mnu_eV} | 'T_nu' {T_gamma_K} | 'dNstar' {dilution} | 'ns_plateau' {Nstar} | 'r_plateau' {Nstar, D} | 'n_nu_relic' {}"""
    q = a.get('q')
    if q == 'Omega_nu_h2': v = float(a['sum_mnu_eV']) / 93.14; lab = 'S'
    elif q == 'T_nu': v = (4 / 11) ** (1 / 3) * float(a.get('T_gamma_K', 2.7255)); lab = 'S'
    elif q == 'dNstar': v = -math.log(max(1.0, float(a['dilution']))) / 3; lab = 'S'
    elif q == 'ns_plateau': v = 1 - 2 / float(a['Nstar']); lab = 'S (leading order; the Weave tilt C is fitted on top)'
    elif q == 'r_plateau': v = 8 / ((int(a.get('D', 10)) - 2) * float(a['Nstar']) ** 2); lab = 'S (UNTILTED leading order r = 8/((D-2) N^2); the Weave prediction is the TILTED exact value r_10 = 5.41e-4 (x1.37), use weave_rladder; joint audit 20 Nov)'
    elif q == 'n_nu_relic': v = 3 * 2 * (3 / 4) * (4 / 11) * 410.7 / 2; lab = 'S (per cm^3, all flavours)'
    else: return {'error': 'q must be one of Omega_nu_h2, T_nu, dNstar, ns_plateau, r_plateau, n_nu_relic'}
    return dict(q=q, value=v, label=lab)


def weave_paths(a):
    """Connection map: {\"from\":..,\"to\":..} -> shortest chain of shared quantities; {} -> all cross-sector connections."""
    import weave_paths as P
    return P.weave_paths(a)


TOOLS = {'weave_rung': weave_rung, 'weave_rung_of': weave_rung_of, 'weave_koide': weave_koide, 'weave_koide_slip': weave_koide_slip,
         'weave_tauq': weave_tauq, 'weave_ckm': weave_ckm, 'weave_proton': weave_proton, 'weave_atomic': weave_atomic,
         'weave_arc': weave_arc, 'weave_rladder': weave_rladder, 'weave_negspace': weave_negspace, 'weave_paths': weave_paths, 'weave_basic': weave_basic}

if __name__ == '__main__':   # self-test: reproduces the published numbers
    assert abs(weave_rung({'m': 8})['eps_formula'] - 0.003117) < 2e-5
    k = weave_koide({'masses': [0.51099895, 105.6583755, 1776.93]}); assert abs(k['Q'] - 0.6666645) < 2e-7 and abs(k['delta'] - 0.222225) < 2e-6
    q = weave_koide({'masses': [1.29e-3, 0.629, 169.0]}); assert abs(q['Q'] - 0.8870) < 5e-4
    r = weave_rung_of({'masses': [2.80e-3, 55.7e-3, 2.794]}); assert r['matching_rungs'][:2] == [1, 2]
    t = weave_tauq({'mass_GeV': 1e11}); assert t['allowed'] and abs(t['dilution'] - 67.2) < 1
    assert not weave_tauq({'mass_GeV': 1e9})['allowed']
    s = weave_koide_slip({'eps': 0.02395}); assert 5e-3 < s['median_dQ'] < 1.2e-2
    c = weave_ckm({'model': 'w864', 'rung_d': 1, 'rung_u': 8, 'down': {'r1': 1.806, 'r2': 0.701, 'g_abs': 0.773, 'g_arg': 2.885, 'f_abs': 2.234, 'f_arg': 3.142},
                   'up': {'r1': 2.633, 'r2': 0.333, 'g_abs': 0.333, 'g_arg': -3.142, 'f_abs': 1.745, 'f_arg': -3.142}})
    assert abs(c['ms_mb'] - 0.0107) < 5e-4 and abs(c['Vus'] - 0.218) < 3e-3, c
    ar = weave_arc({'m': 1, 'n': 1}); assert ar['on_arc'] and abs(ar['tau_re'] + 0.2378) < 2e-3, ar
    r1 = weave_arc({'m': 1, 'n': 0}); assert abs(r1['dist_rho'] - 0.02395) < 3e-4, r1
    assert abs(weave_negspace({})['z_switch'] - 2.88) < 0.05
    assert abs(weave_rladder({'D': 6})['r'] - 1.082e-3) < 2e-6
    print('weave_tools selftest OK', json.dumps({k: round(v, 5) for k, v in c.items() if isinstance(v, float)}))
