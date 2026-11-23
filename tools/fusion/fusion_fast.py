"""SPEED-fusion: numpy-vectorised S3 (same formulas, same grid, same iteration path as fusion.py). Pedestal profiles only; anything
else falls back to the reference functions."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F

def sigmav_np(reaction, T):
    p = F.BH[reaction]; C1, C2, C3, C4, C5, C6, C7 = p['C']
    theta = T / (1 - T * (C2 + T * (C4 + T * C6)) / (1 + T * (C3 + T * (C5 + T * C7))))
    xi = (p['BG'] ** 2 / (4 * theta)) ** (1 / 3)
    return C1 * theta * np.sqrt(xi / (p['mrc2'] * T ** 3)) * np.exp(-3 * xi)

_GRID = {}
def _grid(m, N=400):
    key = (m['rho_ped'], m['alpha_n'], m['alpha_T'], m['n_ped'], m['n_sep'], m['T_ped'], m['T_sep'], N)
    g = _GRID.get(key)
    if g: return g
    rho = (np.arange(N) + 0.5) / N; w = 2 * rho / N; w = w / w.sum(); rp = m['rho_ped']; inside = rho <= rp
    def basis(Xp, Xs, alpha):   # X(rho) = a(rho) + X0 * b(rho)
        sh = np.where(inside, (1 - np.clip(rho / rp, 0, 1) ** 2.0) ** alpha, 0.0)
        a = np.where(inside, Xp * (1 - sh), Xs + (Xp - Xs) * (1 - rho) / (1 - rp)); b = np.where(inside, sh, 0.0)
        return a, b
    an, bn = basis(m['n_ped'], m['n_sep'], m['alpha_n']); aT, bT = basis(m['T_ped'], m['T_sep'], m['alpha_T'])
    g = dict(rho=rho, w=w, an=an, bn=bn, aT=aT, bT=bT, N=N); _GRID[key] = g; return g

def _solve_X0(Xavg, a, b, w, Xp):
    # reference uses the two-point secant at X0 = Xp, 2Xp on avg(X0) = sum w (a + X0 b); exact for a linear map
    a0 = float(np.dot(w, a + Xp * b)); a1 = float(np.dot(w, a + 2 * Xp * b)); return Xp + Xp * (Xavg - a0) / (a1 - a0)

def plasma_fast(m, n_avg, Te_avg, E_alpha_MeV, f_He=None):
    if m.get('profile') != 'pedestal': return F.plasma(m, n_avg, Te_avg, E_alpha_MeV, f_He)
    mm = dict(m) if f_He is None else dict(m, f_He=f_He); c = F.composition(mm); g = _grid(mm); w = g['w']; V = mm['V']
    n0 = _solve_X0(n_avg, g['an'], g['bn'], w, mm['n_ped']); T0 = _solve_X0(Te_avg, g['aT'], g['bT'], w, mm['T_ped'])
    ne = g['an'] + n0 * g['bn']; Te = g['aT'] + T0 * g['bT']; Ti = mm['Ti_over_Te'] * Te
    Efus = F.q_value('DT') * F.MEV_J; nD = ne * c['f_DT'] / 2
    hot = Ti > 0.2; sv = np.zeros_like(Ti); sv[hot] = sigmav_np('DT', np.minimum(Ti[hot], 100.0))
    Pf = float(np.dot(w, np.where(hot, nD * nD * sv * 1e-6 * Efus, 0.0))) * V / 1e6
    pb = w * F.C_B * c['Zeff'] * ne * ne * np.sqrt(np.maximum(Te, 0.0)); core = g['rho'] < mm.get('rho_core', 1.0)
    Pb = float(pb.sum()) * V / 1e6; Pb_core = float(pb[core].sum()) * V / 1e6
    ne2 = float(np.dot(w, ne * ne)); ne2_core = float(np.dot(w[core], (ne * ne)[core]))
    Wth = float(np.dot(w, 1.5 * (ne * Te + ne * c['ions_per_e'] * Ti) * F.KEV_J)) * V / 1e6
    nline = float(ne.sum()) / g['N']
    Ps = F.p_synch(mm, n0, T0) if mm.get('synch', True) else 0.0   # PROM-8 DEV-2 (POPCON omits synchrotron)
    if mm.get('line_model') == 'adas':   # PROM-5: line radiation derived from OPEN-ADAS (Ar, Be, He; W if f_W given)
        import adas as AD
        Lfun = AD.Limp_interp if mm.get('line_prb', True) else AD.L_interp   # DEV-1: PLT + PRB - impurity Z_eff bremsstrahlung
        pl = sum(mm.get(f'f_{k}', 0.0) * Lfun(k.lower(), Te) for k in ('Ar', 'Be', 'He', 'W', 'O') if mm.get(f'f_{k}', 0.0) > 0) * ne * ne
        pl = w * np.maximum(pl, 0.0) * V / 1e6; Pline = float(pl.sum()); Pline_core = float(pl[core].sum())
    else:
        Pline = mm['P_line']; Pline_core = Pline * (ne2_core / ne2)
    Prad = Pb + Ps + Pline; Prad_core = Pb_core + Ps + Pline_core
    beta = 2 * F.MU0 * (Wth * 1e6 / 1.5 / V) / mm['B'] ** 2; nG = mm['Ip'] / (math.pi * mm['a'] ** 2) * 1e20
    return dict(P_fus=Pf, P_alpha=Pf * E_alpha_MeV / F.q_value('DT'), P_brems=Pb, P_synch=Ps, P_line=Pline, P_rad=Prad, P_rad_core=Prad_core, W_MJ=Wth,
                beta_N=100 * beta * mm['a'] * mm['B'] / mm['Ip'], n_G=nG, n_line=nline, f_G=nline / nG, Zeff=c['Zeff'], f_DT=c['f_DT'], ions_per_e=c['ions_per_e'], Te0=T0, ne0=n0, f_He=mm['f_He'])

def _op_fixed_he_fast(m, E_alpha_MeV, n_avg, P_aux, f_He):
    from scipy.optimize import brentq
    pop = m.get('convention') == 'popcon'   # PROM-9: cfspopcon convention (tau at P_heat = P_alpha + P_aux; W from volume averages)
    def _w(p, T): return 1.5 * n_avg * T * (1 + p['ions_per_e'] * m['Ti_over_Te']) * F.KEV_J * m['V'] / 1e6
    def _pl(p): return p['P_alpha'] + P_aux if pop else F._ploss(m, p, P_aux)
    def f(T):
        p = plasma_fast(m, n_avg, T, E_alpha_MeV, f_He); Pl = _pl(p); W = _w(p, T) if pop else p['W_MJ']
        return (W / F.tau_ipb98(m, Pl, p['n_line']) - Pl) if Pl > 0 else 1e9
    Ts = [2 + 0.25 * i for i in range(150)]; vals = [f(T) for T in Ts]; roots = []
    for a, b, fa, fb in zip(Ts, Ts[1:], vals, vals[1:]):
        if fa * fb < 0 and abs(fa) < 1e8 and abs(fb) < 1e8: roots.append(brentq(f, a, b, xtol=1e-9))
    if not roots: return None
    T = max(roots); p = plasma_fast(m, n_avg, T, E_alpha_MeV, f_He); Pl = _pl(p)
    if pop: p = dict(p, W_MJ=_w(p, T))
    return dict(p, Te_avg=T, Ti_avg=T * m['Ti_over_Te'], n_avg=n_avg, P_aux=P_aux, P_loss=Pl, tau_E=F.tau_ipb98(m, Pl, p['n_line']),
                Q=p['P_fus'] / P_aux if P_aux > 0 else float('inf'), P_LH=F.p_LH(m, p['n_line']), roots=roots)

def operating_point_fast(m, E_alpha_MeV, n_avg=None, P_aux=None):
    n_avg = m['n_avg'] if n_avg is None else n_avg; P_aux = m['P_aux'] if P_aux is None else P_aux
    fHe = m['f_He']; op = None
    for it in range(30):
        op = _op_fixed_he_fast(m, E_alpha_MeV, n_avg, P_aux, fHe)
        if op is None or not m.get('he_selfconsistent'): break
        S_alpha = op['P_fus'] * 1e6 / (F.q_value('DT') * F.MEV_J); new = S_alpha * m['tauHe_ratio'] * op['tau_E'] / (m['V'] * n_avg)
        if abs(new - fHe) < 1e-7: break
        fHe = 0.5 * fHe + 0.5 * new
    if op is not None: op['he_iterations'] = it + 1
    return op

def goal_dials_fast(m, E_alpha_MeV, plant_in, P_aux_set=(30.0, 40.0, 50.0, 60.0, 73.0), lh_margin=1.3, betaN_max=2.8):
    best = None; nG = m['Ip'] / (math.pi * m['a'] ** 2) * 1e20
    for Pa in P_aux_set:
        for i in range(21):
            n = nG * (0.6 + 0.4 * i / 20); op = operating_point_fast(m, E_alpha_MeV, n_avg=n, P_aux=Pa)
            if op is None: continue
            if op['f_G'] > m['fG_max'] or op['beta_N'] > betaN_max or op['P_loss'] < lh_margin * op['P_LH']: continue
            pl = F.plant(op['P_fus'], Pa, plant_in)
            if best is None or pl['P_net'] > best['P_net']: best = dict(pl, n_avg=n, P_aux=Pa, P_fus=op['P_fus'], Q=op['Q'], f_G=op['f_G'], beta_N=op['beta_N'], lh_ratio=op['P_loss'] / op['P_LH'])
    return best

def binding_limit(m, E_alpha_MeV, P_aux, n_lo, n_hi, lh_margin=1.3, betaN_max=2.8, tol=1e-4):
    """PROM-3 DEV-4: bisect density between a feasible n_lo and an infeasible n_hi; return the edge and the limit that fails first."""
    def bad(n):
        op = operating_point_fast(m, E_alpha_MeV, n_avg=n, P_aux=P_aux)
        if op is None: return ['no hot root']
        return [k for k, b in (('Greenwald', op['f_G'] > m['fG_max']), ('beta_N', op['beta_N'] > betaN_max), ('L-H margin', op['P_loss'] < lh_margin * op['P_LH'])) if b]
    while (n_hi - n_lo) / n_lo > tol:
        mid = 0.5 * (n_lo + n_hi)
        if bad(mid): n_hi = mid
        else: n_lo = mid
    return dict(n_edge=n_lo, limit=bad(n_hi), op=operating_point_fast(m, E_alpha_MeV, n_avg=n_lo, P_aux=P_aux))
