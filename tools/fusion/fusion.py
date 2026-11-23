"""Fusion engine (PREREG_FUSION1). Goal at the top: net electricity from D-T fusion. Sections are child engines on one bus.
Units: T in keV, <sigma v> in cm^3/s (Bosch-Hale) and m^3/s where noted, n in m^-3, energies in MeV or J as labelled."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from net import Bus, Engine, settle, tree

# ------------------------------------------------------------------ constants (CODATA 2018 / AME 2020 atomic masses in u)
U_MEV = 931.49410242; MEV_J = 1.602176634e-13; KEV_J = 1.602176634e-16; ALPHA_FS = 7.2973525693e-3; YEAR = 3.15576e7; NA = 6.02214076e23
M = dict(n=1.00866491595, H1=1.00782503223, D=2.01410177812, T=3.01604928132, He3=3.01602932197, He4=4.00260325413)
ME_U = 5.48579909065e-4          # electron mass in u (for nuclear masses)
def nuc(k, Z): return M[k] - Z * ME_U   # nuclear mass (electron binding neglected, < 30 eV)

# ------------------------------------------------------------------ S1 reactions
BH = {  # Bosch & Hale, Nucl. Fusion 32 (1992) 611: BG [keV^1/2], mrc2 [keV], C1..C7; valid 0.2-100 keV (D-He3 0.5-190 keV)
    'DT':   dict(BG=34.3827, mrc2=1124656.0, C=(1.17302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3, 1.35000e-2, -1.06750e-4, 1.36600e-5), src='listing (tokamak_neutron_source)'),
    'DDn':  dict(BG=31.3970, mrc2=937814.0, C=(5.43360e-12, 5.85778e-3, 7.68222e-3, 0.0, -2.96400e-6, 0.0, 0.0), src='listing (tokamak_neutron_source)'),
    'DDp':  dict(BG=31.3970, mrc2=937814.0, C=(5.65718e-12, 3.41267e-3, 1.99167e-3, 0.0, 1.05060e-5, 0.0, 0.0), src='listing (tokamak_neutron_source)'),
    'DHe3': dict(BG=68.7508, mrc2=1124572.0, C=(5.51036e-10, 6.41918e-3, -2.02896e-3, -1.91080e-5, 1.35776e-4, 0.0, 0.0), src='confirmed vs METIS, ASCOT5, PROCESS, PlasmaPy (R81)'),
}
def sigmav(reaction, T_keV):
    """Bosch-Hale thermal reactivity <sigma v> in cm^3/s for a Maxwellian at ion temperature T (keV)."""
    p = BH[reaction]; C1, C2, C3, C4, C5, C6, C7 = p['C']; T = T_keV
    theta = T / (1 - T * (C2 + T * (C4 + T * C6)) / (1 + T * (C3 + T * (C5 + T * C7))))
    xi = (p['BG'] ** 2 / (4 * theta)) ** (1 / 3)
    return C1 * theta * math.sqrt(xi / (p['mrc2'] * T ** 3)) * math.exp(-3 * xi)

REACTIONS = {  # (reactants, products) with atomic masses (electrons balance)
    'DT': (('D', 'T'), ('He4', 'n')), 'DDn': (('D', 'D'), ('He3', 'n')), 'DDp': (('D', 'D'), ('T', 'H1')), 'DHe3': (('D', 'He3'), ('He4', 'H1'))}
def q_value(r):
    a, b = REACTIONS[r]; return (sum(M[x] for x in a) - sum(M[x] for x in b)) * U_MEV

def two_body_split(r, relativistic=True):
    """Kinetic energies of the two products for reactants at rest (the thermal energy is neglected). Returns (E_light, E_heavy) in MeV
    as (product 2, product 1) of the reaction tuple's products."""
    Z = dict(n=0, H1=1, D=1, T=1, He3=2, He4=2)
    (p1, p2) = REACTIONS[r][1]; m1, m2 = nuc(p1, Z[p1]) * U_MEV, nuc(p2, Z[p2]) * U_MEV; Q = q_value(r)
    if not relativistic: return Q * m1 / (m1 + m2), Q * m2 / (m1 + m2)
    W = m1 + m2 + Q; E2 = (W * W + m2 * m2 - m1 * m1) / (2 * W) - m2; return E2, Q - E2

# ------------------------------------------------------------------ S7 stars: the Gamow peak
K_B_KEV = 8.617333262e-8   # keV per K
def gamow(Z1, Z2, mu_u, T_K=None, kT_keV=None):
    """Gamow peak E0 = (b kT / 2)^(2/3), b = pi alpha Z1 Z2 sqrt(2 mu c^2); width Delta = 4 sqrt(E0 kT / 3). keV."""
    kT = kT_keV if kT_keV is not None else K_B_KEV * T_K
    b = math.pi * ALPHA_FS * Z1 * Z2 * math.sqrt(2 * mu_u * U_MEV * 1000.0)     # keV^1/2
    E0 = (b * kT / 2) ** (2 / 3); return dict(E0_keV=E0, width_keV=4 * math.sqrt(E0 * kT / 3), b_keV_half=b, kT_keV=kT)


# ------------------------------------------------------------------ S2 ignition (0-D, flat profiles, D-T 50:50, n_e = n)
C_B = 5.35e-37   # W m^3 keV^-1/2, bremsstrahlung P_br = C_B Z_eff n_e^2 sqrt(T)
def ignition_ntau(T, E_alpha_MeV, Zeff=1.0):
    """n tau_E (s m^-3) for ignition: (n^2/4)<sv> E_alpha = 3 n T / tau_E + C_B Zeff n^2 sqrt(T). Returns inf below ideal ignition."""
    heat = sigmav('DT', T) * 1e-6 * E_alpha_MeV * MEV_J / 4 - C_B * Zeff * math.sqrt(T)
    return 3 * T * KEV_J / heat if heat > 0 else float('inf')
def ignition_min(E_alpha_MeV, Zeff=1.0):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda T: T * ignition_ntau(T, E_alpha_MeV, Zeff) if math.isfinite(ignition_ntau(T, E_alpha_MeV, Zeff)) else 1e30, bounds=(5, 40), method='bounded', options=dict(xatol=1e-6))
    return r.x, r.fun
def ideal_ignition_T(E_alpha_MeV, Zeff=1.0):
    from scipy.optimize import brentq
    return brentq(lambda T: sigmav('DT', T) * 1e-6 * E_alpha_MeV * MEV_J / 4 - C_B * Zeff * math.sqrt(T), 1.0, 20.0, xtol=1e-10)

# ------------------------------------------------------------------ S3 tokamak 0-D with profiles + dials (DEV-4..8)
MU0 = 4e-7 * math.pi
ITER = dict(R=6.2, a=2.0, kappa=1.85, B=5.3, Ip=15.0, V=831.0, S=683.0, P_aux=50.0, M=2.5, alpha_n=0.1, alpha_T=1.0, beta_T=2.0,
            f_He=0.032, f_Be=0.020, f_Ar=0.0014, Ti_over_Te=8.1 / 8.9, f_reflect=0.6, P_line=27.0, n_avg=1.13e20, fG_max=0.94,
            src='ITER FDR Physics Table 4.3.1-1, 500 MW column; Be/Ar are axis values used as averages; P_line is an INPUT',
            # PROM-1 (cycle 1): pedestal profiles (C2), radiation correction (C1), self-consistent He ash (C3)
            profile='pedestal', rho_ped=0.94, T_ped=3.5, n_ped=0.8e20, T_sep=0.1, n_sep=0.4e20, rad_C3=0.6, rho_core=0.75, tauHe_ratio=5.0, he_selfconsistent=True, lh_isotope=True)
ITER_400 = dict(ITER, P_aux=40.0, n_avg=1.01e20, P_line=27.0, Ti_over_Te=8.0 / 8.8, src='ITER FDR Table 4.3.1-1, 400 MW column (held out in PROM-1)')
Z_IMP = dict(He=2, Be=4, Ar=18)
def composition(m):
    """Fully stripped impurities as fractions of n_e: fuel fraction n_DT/n_e, ion count per electron, Z_eff."""
    f = dict(He=m['f_He'], Be=m['f_Be'], Ar=m['f_Ar'])
    f_DT = 1 - sum(f[k] * Z_IMP[k] for k in f)
    zeff = f_DT + sum(f[k] * Z_IMP[k] ** 2 for k in f)
    return dict(f_DT=f_DT, ions_per_e=f_DT + sum(f.values()), Zeff=zeff)
def line_avg_factor(alpha_n):
    """n_line / n_avg for n = n0 (1 - rho^2)^alpha_n: n_avg = n0/(1+alpha_n), n_line = n0 sqrt(pi) Gamma(alpha_n+1) / (2 Gamma(alpha_n+1.5))."""
    return (math.sqrt(math.pi) * math.gamma(alpha_n + 1) / (2 * math.gamma(alpha_n + 1.5))) * (1 + alpha_n)
def _ped_shape(rho, X0, Xp, Xs, rp, alpha, beta=2.0):
    return Xp + (X0 - Xp) * (1 - (rho / rp) ** beta) ** alpha if rho <= rp else Xs + (Xp - Xs) * (1 - rho) / (1 - rp)
def _profiles(m, n_avg, Te_avg, N=400):
    """Returns ([(n_e, T_e, w, rho)], n0, T0, n_line). Weights w are volume fractions (sum 1). Parabolic (FUSION-1) or pedestal (PROM-1 C2)."""
    rhos = [(i + 0.5) / N for i in range(N)]; w = [2 * r / N for r in rhos]; ws = sum(w); w = [x / ws for x in w]
    if m.get('profile') != 'pedestal':
        n0 = n_avg * (1 + m['alpha_n']); T0 = Te_avg * (1 + m['alpha_T'])
        prof = [(n0 * (1 - r * r) ** m['alpha_n'], T0 * (1 - r * r) ** m['alpha_T'], wi, r) for r, wi in zip(rhos, w)]
        return prof, n0, T0, n_avg * line_avg_factor(m['alpha_n'])
    rp = m['rho_ped']
    def solve(Xavg, Xp, Xs, alpha):
        avg = lambda X0: sum(wi * _ped_shape(r, X0, Xp, Xs, rp, alpha) for r, wi in zip(rhos, w))
        a0, a1 = avg(Xp), avg(2 * Xp); return Xp + Xp * (Xavg - a0) / (a1 - a0)
    n0 = solve(n_avg, m['n_ped'], m['n_sep'], m['alpha_n']); T0 = solve(Te_avg, m['T_ped'], m['T_sep'], m['alpha_T'])
    prof = [(_ped_shape(r, n0, m['n_ped'], m['n_sep'], rp, m['alpha_n']), _ped_shape(r, T0, m['T_ped'], m['T_sep'], rp, m['alpha_T']), wi, r) for r, wi in zip(rhos, w)]
    nline = sum(p[0] for p in prof) / N
    return prof, n0, T0, nline
def p_synch(m, ne0, Te0):
    """Albajar et al. 2001 fit with the Fidone reflection term (UKAEA PROCESS docs), MW."""
    r = m['f_reflect']; aT, an, bT = m['alpha_T'], m['alpha_n'], m['beta_T']; A = m['R'] / m['a']; n20 = ne0 / 1e20
    pa0 = 6.04e3 * m['a'] * n20 / m['B']
    K = (an + 3.87 * aT + 1.46) ** -0.79 * (1.98 + aT) ** 1.36 * bT ** 2.14 * (bT ** 1.53 + 1.87 * aT - 0.16) ** -1.33
    G = 0.93 * (1 + 0.85 * math.exp(-0.82 * A))
    return (3.84e-8 * (1 - r) ** 0.62 / (1 + 0.12 * Te0 / pa0 ** 0.41 * (1 - r) ** 0.41) ** 1.51
            * m['R'] * m['a'] ** 1.38 * m['kappa'] ** 0.79 * m['B'] ** 2.62 * n20 ** 0.38 * Te0 * (16 + Te0) ** 2.61 * K * G)
def plasma(m, n_avg, Te_avg, E_alpha_MeV, f_He=None):
    mm = dict(m) if f_He is None else dict(m, f_He=f_He)
    c = composition(mm); prof, ne0, Te0, nline = _profiles(mm, n_avg, Te_avg); V = mm['V']; Pf = Pb = Wth = Pb_core = ne2 = ne2_core = 0.0
    Efus = q_value('DT') * MEV_J; r = mm['Ti_over_Te']; rc = mm.get('rho_core', 1.0)
    for ne, Te, wi, rho in prof:
        Ti = r * Te
        if Ti > 0.2:
            nD = nT = ne * c['f_DT'] / 2; Pf += wi * nD * nT * sigmav('DT', min(Ti, 100.0)) * 1e-6 * Efus
        pb = wi * C_B * c['Zeff'] * ne * ne * math.sqrt(max(Te, 0.0)); Pb += pb; ne2 += wi * ne * ne
        if rho < rc: Pb_core += pb; ne2_core += wi * ne * ne
        Wth += wi * 1.5 * (ne * Te + ne * c['ions_per_e'] * Ti) * KEV_J
    Pf *= V / 1e6; Pb *= V / 1e6; Pb_core *= V / 1e6; Wth *= V / 1e6
    Ps = p_synch(mm, ne0, Te0); Pline = mm['P_line']; Prad = Pb + Ps + Pline
    Prad_core = Pb_core + Ps + Pline * (ne2_core / ne2)          # C1: line radiation shaped like n_e^2 (L_z flat, interim); synchrotron all core
    beta = 2 * MU0 * (Wth * 1e6 / 1.5 / V) / mm['B'] ** 2
    nG = mm['Ip'] / (math.pi * mm['a'] ** 2) * 1e20
    return dict(P_fus=Pf, P_alpha=Pf * E_alpha_MeV / q_value('DT'), P_brems=Pb, P_synch=Ps, P_line=Pline, P_rad=Prad, P_rad_core=Prad_core, W_MJ=Wth,
                beta_N=100 * beta * mm['a'] * mm['B'] / mm['Ip'], n_G=nG, n_line=nline, f_G=nline / nG, Zeff=c['Zeff'], f_DT=c['f_DT'], Te0=Te0, ne0=ne0, f_He=mm['f_He'])
def _ploss(m, p, P_aux):
    if m.get('profile') == 'pedestal': return p['P_alpha'] + P_aux - m['rad_C3'] * p['P_rad_core']    # C1 (Lux et al.)
    return p['P_alpha'] + P_aux - p['P_rad']
def tau_ipb98(m, P_loss, n_line):
    eps = m['a'] / m['R']; ka = m['V'] / (2 * math.pi ** 2 * m['R'] * m['a'] ** 2)
    return 0.0562 * m['Ip'] ** 0.93 * m['B'] ** 0.15 * P_loss ** -0.69 * (n_line / 1e19) ** 0.41 * m['M'] ** 0.19 * m['R'] ** 1.97 * eps ** 0.58 * ka ** 0.78
def p_LH(m, n_line):   # Martin 2008 (deuterium), S = plasma surface (m^2); PROM-2 C1: isotope factor 2/A_eff
    return 0.0488 * (n_line / 1e20) ** 0.717 * m['B'] ** 0.803 * m['S'] ** 0.941 * (2.0 / m['M'] if m.get('lh_isotope') else 1.0)
def _op_fixed_he(m, E_alpha_MeV, n_avg, P_aux, f_He):
    from scipy.optimize import brentq
    def f(T):
        p = plasma(m, n_avg, T, E_alpha_MeV, f_He); Pl = _ploss(m, p, P_aux)
        return (p['W_MJ'] / tau_ipb98(m, Pl, p['n_line']) - Pl) if Pl > 0 else 1e9
    Ts = [2 + 0.25 * i for i in range(150)]; vals = [f(T) for T in Ts]; roots = []
    for a, b, fa, fb in zip(Ts, Ts[1:], vals, vals[1:]):
        if fa * fb < 0 and abs(fa) < 1e8 and abs(fb) < 1e8: roots.append(brentq(f, a, b, xtol=1e-9))
    if not roots: return None
    T = max(roots); p = plasma(m, n_avg, T, E_alpha_MeV, f_He); Pl = _ploss(m, p, P_aux)
    return dict(p, Te_avg=T, Ti_avg=T * m['Ti_over_Te'], n_avg=n_avg, P_aux=P_aux, P_loss=Pl, tau_E=tau_ipb98(m, Pl, p['n_line']),
                Q=p['P_fus'] / P_aux if P_aux > 0 else float('inf'), P_LH=p_LH(m, p['n_line']), roots=roots)
def operating_point(m, E_alpha_MeV, n_avg=None, P_aux=None):
    """Power balance W/tau_E(P_loss) = P_loss; hottest root. PROM-1 C3: f_He iterated to (alpha birth rate) x 5 tau_E / (V <n_e>)."""
    n_avg = m['n_avg'] if n_avg is None else n_avg; P_aux = m['P_aux'] if P_aux is None else P_aux
    fHe = m['f_He']; op = None
    for it in range(30):
        op = _op_fixed_he(m, E_alpha_MeV, n_avg, P_aux, fHe)
        if op is None or not m.get('he_selfconsistent'): break
        S_alpha = op['P_fus'] * 1e6 / (q_value('DT') * MEV_J); new = S_alpha * m['tauHe_ratio'] * op['tau_E'] / (m['V'] * n_avg)
        if abs(new - fHe) < 1e-7: break
        fHe = 0.5 * fHe + 0.5 * new
    if op is not None: op['he_iterations'] = it + 1
    return op
def dials(m, E_alpha_MeV, betaN_max=2.8):
    """Dials: <n> scanned with P_aux fixed; maximise Q subject to f_G <= fG_max, beta_N <= betaN_max, P_loss >= P_LH. Names the binding limit."""
    best = None; nG = m['Ip'] / (math.pi * m['a'] ** 2) * 1e20; lf = line_avg_factor(m['alpha_n'])
    for i in range(41):
        n = nG / lf * (0.5 + 0.5 * i / 40); op = operating_point(m, E_alpha_MeV, n_avg=n)
        if op is None: continue
        bind = [k for k, bad in (('Greenwald', op['f_G'] > m['fG_max']), ('beta_N', op['beta_N'] > betaN_max), ('L-H threshold', op['P_loss'] < op['P_LH'])) if bad]
        if bind: continue
        if best is None or op['Q'] > best['Q']: best = dict(op, binding=None)
    if best:   # which limit stops it: step just past the best density
        nxt = operating_point(m, E_alpha_MeV, n_avg=best['n_avg'] * 1.0125)
        best['binding'] = 'Greenwald' if nxt and nxt['f_G'] > m['fG_max'] else ('beta_N' if nxt and nxt['beta_N'] > betaN_max else 'L-H threshold or scan edge')
    return best

class Ignition(Engine):
    name = 'S2 ignition'
    def run(self, bus):
        Ea = bus.get('E_alpha_DT_MeV'); T, ntt = ignition_min(Ea); Ti = ideal_ignition_T(Ea)
        bus.put(self.name, 'ignition_T_keV', T, 'LIVE', 'keV'); bus.put(self.name, 'ignition_nTtau', ntt, 'LIVE', 'keV s m^-3'); bus.put(self.name, 'ideal_ignition_T_keV', Ti, 'LIVE', 'keV')
        return {}

class Tokamak(Engine):
    name = 'S3 tokamak (dials)'
    def run(self, bus):
        Ea = bus.get('E_alpha_DT_MeV'); op = operating_point(ITER, Ea)
        for k in ('P_fus', 'Q', 'tau_E', 'Te_avg', 'Ti_avg', 'beta_N', 'P_loss', 'P_LH', 'W_MJ', 'P_rad', 'P_brems', 'P_synch', 'Zeff', 'f_G'): bus.put(self.name, f'iter_{k}', op[k], 'LIVE')
        d = dials(ITER, Ea)
        if d: bus.put(self.name, 'dials_best_n', d['n_avg'], 'LIVE', 'm^-3'); bus.put(self.name, 'dials_best_Q', d['Q'], 'LIVE'); bus.put(self.name, 'dials_binding', d['binding'], 'LIVE')
        return dict(roots=op['roots'])


# ------------------------------------------------------------------ S4 inertial fusion (OU: IFE-STARFIRE)
H_B = 6.0   # g/cm^2, burn parameter in Phi = rhoR/(rhoR + H_B) (Fraley et al. 1974; ~6-7 g/cm^2 at 20-30 keV burn)
def specific_yield_J_per_g():
    return q_value('DT') * MEV_J * NA / (M['D'] + M['T'])
def burn_fraction(rhoR): return rhoR / (rhoR + H_B)
def rhoR_for(yield_J, fuel_mg):
    """Areal density needed to release yield_J from fuel_mg of D-T (inverts Phi)."""
    phi = yield_J / (fuel_mg * 1e-3 * specific_yield_J_per_g())
    return float('inf') if phi >= 1 else H_B * phi / (1 - phi)
NIF = [dict(shot='2022-12-05', yield_MJ=3.15, laser_MJ=2.05), dict(shot='2025 (5.0 MJ; date unconfirmed)', yield_MJ=5.0, laser_MJ=2.05, gain_reported=2.44),
       dict(shot='2025-04-07', yield_MJ=8.6, laser_MJ=2.08, gain_reported=4.13, src='LLNL Annual 2025')]   # DEV-11

class Inertial(Engine):
    name = 'S4 inertial (IFE)'
    def run(self, bus):
        bus.put(self.name, 'specific_yield_J_per_g', specific_yield_J_per_g(), 'LIVE', 'J/g'); bus.put(self.name, 'Phi_rhoR3', burn_fraction(3.0), 'LIVE')
        for s in NIF:
            if s['laser_MJ']: bus.put(self.name, f'NIF_target_gain_{s["shot"]}', s['yield_MJ'] / s['laser_MJ'], 'DATA (target gain = yield / laser energy on target; not wall-plug)')
        bus.put(self.name, 'IFE_gain_needed_eta0.1', 10 / 0.1, 'LIVE')
        return dict(note='NIF entries are data bookkeeping, not derivations')

# ------------------------------------------------------------------ S5 fuel cycle (links into the Chronos nuclear engine for tritium decay)
def tritium_half_life_y():
    try:
        sys.path.insert(0, os.path.join(HERE, '..', 'gifts', 'chronos')); import chronos_a3 as A3
        return A3.T12x['H-3'] / A3.Y, 'Chronos (D2189)'
    except Exception: return 12.32, 'fallback 12.32 y'
def burn_kg_per_GWfpy(species='T'):
    rate = 1e9 / (q_value('DT') * MEV_J)                          # reactions per second per GW of fusion power
    molar = dict(T=M['T'], D=M['D'], Li6=6.0151228874)[species]   # g/mol (atomic)
    return rate * YEAR * molar / NA / 1e3
def tbr_required(P_GW, inventory_kg, doubling_years, losses_frac=0.0):
    """DEV-12: breeding ratio to double a start-up inventory I0 in t_d at constant burn b (kg/y) with tritium decay (Chronos half-life):
    dI/dt = (TBR - 1 - losses) b - lambda I, I(t_d) = 2 I0  ->  TBR = 1 + losses + lambda I0 (2 - e^-lt) / (b (1 - e^-lt)).
    Leaves out burn fraction, fuelling efficiency and residence times, which dominate real requirements (Abdou et al. 2021)."""
    t12, _ = tritium_half_life_y(); lam = math.log(2) / t12; b = burn_kg_per_GWfpy('T') * P_GW; e = math.exp(-lam * doubling_years)
    return 1 + losses_frac + lam * inventory_kg * (2 - e) / (b * (1 - e))

class FuelCycle(Engine):
    name = 'S5 fuel cycle'
    def run(self, bus):
        t12, src = tritium_half_life_y()
        bus.put(self.name, 'T_burn_kg_per_GWfpy', burn_kg_per_GWfpy('T'), 'LIVE', 'kg'); bus.put(self.name, 'Li6_use_kg_per_GWfpy', burn_kg_per_GWfpy('Li6'), 'LIVE (per bred T, Li-6 only)', 'kg')
        bus.put(self.name, 'D_burn_kg_per_GWfpy', burn_kg_per_GWfpy('D'), 'LIVE', 'kg'); bus.put(self.name, 'tritium_half_life_y', t12, 'LINK', 'y')
        bus.put(self.name, 'TBR_example_1GW_10kg_5y', tbr_required(1.0, 10.0, 5.0), 'EXAMPLE')
        return dict(half_life_source=src)

# ------------------------------------------------------------------ S6 neutrons and materials
ITER_WALL = dict(area_m2=730.0, fw_only_m2=670.0, label='first wall + divertor (FW only 670 m^2)', src='ITER FDR PDD 2.14: inboard ~200 + outboard ~470 + divertor ~60 m^2; average 0.55 MW/m^2 at 500 MW')
STORK = dict(dpa_per_MWa_m2=10.0, He_appm_per_dpa=12.0, src='Stork et al. 2014, arXiv:1408.3546: >= 2 MW yr/m^2 ~ 20 dpa in front-wall steel; ~12 appm He/dpa')
GILBERT = dict(He_appm_per_fpy=140.0, flux_n_cm2_s=8.25e14, conditions='pure Fe, DEMO outboard equatorial FW armour, 3.0 GWt (Gilbert et al. 2013, arXiv:1311.5079)')
class Neutrons(Engine):
    name = 'S6 neutrons & materials'
    def run(self, bus):
        share = bus.get('E_n_DT_MeV') / bus.get('Q_DT_MeV'); P = bus.get('iter_P_fus') or 500.0
        bus.put(self.name, 'iter_neutron_power_MW', P * share, 'LIVE', 'MW'); bus.put(self.name, 'iter_wall_load_MW_m2', P * share / ITER_WALL['area_m2'], 'LIVE', 'MW/m^2')
        bus.put(self.name, 'design_wall_load_500MW', 500 * share / ITER_WALL['area_m2'], 'LIVE', 'MW/m^2')
        bus.put(self.name, 'He_appm_per_fpy_DEMO_Fe', GILBERT['He_appm_per_fpy'], 'LIT', 'appm')
        L = P * share / ITER_WALL['area_m2']
        bus.put(self.name, 'iter_wall_load_FW_only_MW_m2', P * share / ITER_WALL['fw_only_m2'], 'LIVE', 'MW/m^2')
        bus.put(self.name, 'dpa_per_fpy_at_model_load', STORK['dpa_per_MWa_m2'] * L, 'LIT x LIVE', 'dpa/fpy')   # DEV-14
        bus.put(self.name, 'He_appm_per_dpa_steel', STORK['He_appm_per_dpa'], 'LIT', 'appm/dpa')
        return dict(area_src=ITER_WALL['src'], gilbert=GILBERT['conditions'])

# ------------------------------------------------------------------ engines
class Reactions(Engine):
    name = 'S1 reactions'
    def run(self, bus):
        for r in BH: bus.put(self.name, f'Q_{r}_MeV', q_value(r), 'LIVE', 'MeV')
        En, Ea = two_body_split('DT'); bus.put(self.name, 'E_n_DT_MeV', En, 'LIVE', 'MeV'); bus.put(self.name, 'E_alpha_DT_MeV', Ea, 'LIVE', 'MeV')
        for T in (1, 10, 20, 50, 100): bus.put(self.name, f'sv_DT_{T}keV', sigmav('DT', T), 'LIVE', 'cm^3/s')
        return dict(n_share=En / q_value('DT'))

class Stars(Engine):
    name = 'S7 stars'
    def run(self, bus):
        mu_pp = nuc('H1', 1) / 2; g = gamow(1, 1, mu_pp, T_K=15.7e6)
        mu_dt = nuc('D', 1) * nuc('T', 1) / (nuc('D', 1) + nuc('T', 1)); gd = gamow(1, 1, mu_dt, kT_keV=10.0)
        bus.put(self.name, 'gamow_pp_sun_E0_keV', g['E0_keV'], 'LIVE', 'keV'); bus.put(self.name, 'gamow_pp_sun_width_keV', g['width_keV'], 'LIVE', 'keV')
        bus.put(self.name, 'gamow_DT_10keV_E0_keV', gd['E0_keV'], 'LIVE', 'keV')
        return dict(pp=g, dt=gd)

class Fusion(Engine):
    name = 'FUSION (goal: net electricity from D-T)'

def build(sections=None):
    secs = sections or [Reactions(), Ignition(), Tokamak(), Inertial(), FuelCycle(), Neutrons(), Stars()]
    return Fusion(secs)

if __name__ == '__main__':
    root = build(); bus = Bus(); sw, ok = settle(root, bus)
    print('\n'.join(tree(root))); print(f'settled in {sw} sweeps')
    for k, v in bus.v.items(): print(f'  {k:28s} {v:.6g} {bus.meta[k]["unit"]}' if isinstance(v, float) else f'  {k} {v}')
