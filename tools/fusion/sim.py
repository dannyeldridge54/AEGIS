"""SIM-1: time-dependent simulations on the fusion engine (0-D burn dynamics; tritium inventory over plant life)."""
import math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
EA = F.two_body_split('DT')[1]

def _T_of_W(m, n, W, fHe):
    return brentq(lambda T: X.plasma_fast(m, n, T, EA, fHe)['W_MJ'] - W, 0.3, 80.0, xtol=1e-12)

def burn_rhs(m, n, P_aux_of_t):
    V = m['V']
    def rhs(t, y):
        W, NHe, _ = y; fHe = NHe / (V * n); T = _T_of_W(m, n, W, fHe); p = X.plasma_fast(m, n, T, EA, fHe)
        Pa = P_aux_of_t(t); PL = F._ploss(m, p, Pa); tau = F.tau_ipb98(m, PL, p['n_line'])
        src = p['P_alpha'] + Pa - m['rad_C3'] * p['P_rad_core']; loss = W / tau
        S_alpha = p['P_fus'] * 1e6 / (F.q_value('DT') * F.MEV_J)
        return [src - loss, S_alpha - NHe / (m['tauHe_ratio'] * tau), src - loss]
    return rhs

def burn(m, n, P_aux_of_t, T0, fHe0, t_end, t_eval=None):
    W0 = X.plasma_fast(m, n, T0, EA, fHe0)['W_MJ']; y0 = [W0, fHe0 * m['V'] * n, 0.0]
    sol = solve_ivp(burn_rhs(m, n, P_aux_of_t), (0, t_end), y0, method='LSODA', rtol=1e-8, atol=[1e-6, 1e12, 1e-6], t_eval=t_eval, dense_output=True)
    out = []
    for t, W, NHe, E in zip(sol.t, *sol.y):
        fHe = NHe / (m['V'] * n); T = _T_of_W(m, n, W, fHe); p = X.plasma_fast(m, n, T, EA, fHe)
        out.append(dict(t=t, W=W, T=T, f_He=fHe, P_fus=p['P_fus'], E_net=E))
    return sol, out

def tritium_life(P_GW, I0, TBR, years, n=2001):
    t12, _ = F.tritium_half_life_y(); lam = math.log(2) / t12; b = F.burn_kg_per_GWfpy('T') * P_GW
    ts = np.linspace(0, years, n)
    def rhs(t, y): I, bred, burned, decayed = y; return [(TBR - 1) * b - lam * I, TBR * b, b, lam * I]
    s = solve_ivp(rhs, (0, years), [I0, 0, 0, 0], t_eval=ts, rtol=1e-12, atol=1e-12)
    return s, dict(b=b, lam=lam)
