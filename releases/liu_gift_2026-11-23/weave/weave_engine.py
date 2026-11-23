"""weave_engine v5: the calibrated Weave late-universe engine for CubeMind (from AEGIS D2134 knob_board.py, 22 Nov 2026).
Reverse thread V = V_L(1 - A e^{-beta phi}), A = 16 zeta(2)/(3 zeta(3)), beta = 2 sqrt 2, start u_i = A e^{-beta phi_i}; optional
thread-dark-matter coupling b (Amendola). Early sound horizons are CAMB-calibrated (early_calib.json, error < 1e-4).
Gate (cloud): own late solver vs CAMB, max rel dev 8.3e-5 (D2134 G0 PASS). Data: CHW compressed CMB + DESI DR2 BAO + one SN set.
Data dir: env WEAVE_DATA, default C:/Users/Danny/ufe_data/packages/data/.  NO CAMB needed.
Scored facts (do not contradict): b is NOT adopted (D2134); the Weave (b=0) beats LCDM by dchi2 -4.5 (Dovekie) / -2.8 (Pantheon+) on this
compressed set; w0wa still fits better; H0 stays ~67.5 (the Weave does NOT solve the Hubble tension)."""
import os, sys, json, math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.environ.get('WEAVE_DATA', 'C:/Users/Danny/ufe_data/packages/data/').replace('\\', '/').rstrip('/') + '/'
C = 299792.458; A = 16*1.6449340668482264/(3*1.2020569031595942); BETA = 2*math.sqrt(2)
OG = 2.4728e-5; NEFF = 3.044; T0EV = 2.7255*8.617333e-5*(4/11)**(1/3)
MNU = [0.0, math.sqrt(7.42e-5), 0.0587 - math.sqrt(7.42e-5)]
ORAD1 = OG*(7/8)*(4/11)**(4/3)*NEFF/3          # per species, relativistic, omega units
yg = np.logspace(-4, 4, 400)
def _F(y):
    num = quad(lambda x: x*x*math.sqrt(x*x + y*y)/(math.exp(x) + 1), 0, 60)[0]; return num/(7*math.pi**4/120)
def _P(y):
    num = quad(lambda x: x**4/math.sqrt(x*x + y*y)/(math.exp(x) + 1)/3, 0, 60)[0]; return num/(7*math.pi**4/120)
FG = np.array([_F(y) for y in yg]); PG = np.array([_P(y) for y in yg])   # rho/rho_rel and p/rho_rel
def nu(a):
    r = 0.0; p = 0.0
    for m in MNU:
        y = m*a/T0EV
        if y < 1e-4: f, pp = 1.0, 1/3
        else: f, pp = np.interp(math.log(y), np.log(yg), FG), np.interp(math.log(y), np.log(yg), PG)
        r += ORAD1*f/a**4; p += ORAD1*pp/a**4
    return r, p
def solve(wb, wc, VL, ui, b, a0=1e-6):
    phi_i = math.log(A/ui)/BETA
    def rhs(N, y):
        phi, v, lrc = y; a = math.exp(N); rc = math.exp(lrc)
        rn, pn = nu(a); rr = OG/a**4; rbm = wb/a**3
        V = VL*(1 - A*math.exp(-BETA*phi)); dV = VL*A*BETA*math.exp(-BETA*phi)
        E2 = (rr + rn + rbm + rc + V)/(1 - v*v/6)
        rhop = 4/3*rr + rn + pn + rbm + rc + E2*v*v/3
        dlnH = -1.5*rhop/E2
        return [v, -(3 + dlnH)*v - 3*(dV + b*rc)/E2, -3 + b*v]
    sol = solve_ivp(rhs, (math.log(a0), 0.0), [phi_i, 0.0, math.log(wc/a0**3)], rtol=1e-9, atol=1e-11, dense_output=True)
    if not sol.success: return None
    return sol
def background(wb, wc, VL, ui, b):
    sol = solve(wb, wc, VL, ui, b)
    if sol is None: return None
    N = np.linspace(math.log(1/(1 + 1200.0)), 0, 3000); a = np.exp(N)
    Y = sol.sol(N); phi, v, rc = Y[0], Y[1], np.exp(Y[2])
    V = VL*(1 - A*np.exp(-BETA*phi)); rn = np.array([nu(x)[0] for x in a])
    E2 = (OG/a**4 + rn + wb/a**3 + rc + V)/(1 - v*v/6)
    if np.any(E2 <= 0) or np.any(V*0 != 0): return None
    rphi = E2*v*v/6 + V
    z = 1/a - 1; E = np.sqrt(E2)
    # comoving distance in Mpc: c/100 * int dz/E  (E = H/100)
    zz = z[::-1]; Ez = E[::-1]
    Dc = np.concatenate([[0], np.cumsum(0.5*(1/Ez[1:] + 1/Ez[:-1])*np.diff(zz))])*C/100
    phi_star = float(np.interp(math.log(1/1090.), N, phi))
    return dict(z=zz, E=Ez, Dc=Dc, h=float(E[-1]), a=a, rc=rc, rphi=rphi, phi=phi, v=v, E2=E2, dphi_star=float(phi[-1]*0 + phi_star - Y[0][0]), sol=sol)
def DM(bg, zq): return np.interp(zq, bg['z'], bg['Dc'])
def Hz(bg, zq): return 100*np.interp(zq, bg['z'], bg['E'])
# ---- early-universe sound horizons from CAMB (standard pre-recombination physics)
_CAL = json.load(open(os.path.join(HERE, 'early_calib.json')))
from scipy.interpolate import RegularGridInterpolator as _RGI
_AR = np.log(np.array(_CAL['table'])); _IP = [_RGI((np.array(_CAL['wb']), np.array(_CAL['wc'])), _AR[:, :, k], method='cubic', bounds_error=False, fill_value=None) for k in range(3)]
def early(wb, wc):
    # calibrated to CAMB 2.0.5 on a 9x11 grid; max interpolation error 6.7e-5 (validated at 12 random points)
    return tuple(float(np.exp(f([wb, wc])[0])) for f in _IP)
# ---- data
mu_cmb = np.array([1.7502, 301.471, 0.02236, 0.9649]); sg = np.array([0.0046, 0.0895, 0.00015, 0.0043])
rho = np.array([[1, .46, -.66, -.74], [.46, 1, -.33, -.35], [-.66, -.33, 1, .46], [-.74, -.35, .46, 1]]); ICMB = np.linalg.inv(rho*np.outer(sg, sg))
def _bao():
    global BZ, BV, BQ, IB
    bl = [l.split() for l in open(D + 'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt') if not l.startswith('#')]
    BZ = np.array([float(x[0]) for x in bl]); BV = np.array([float(x[1]) for x in bl]); BQ = [x[2] for x in bl]
    IB = np.linalg.inv(np.loadtxt(D + 'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'))
BZ = None
def load_sn(name):
    if name == 'dovekie':
        import csv
        rows = list(csv.DictReader(open(D + 'sn_data/DES-Dovekie/DES-Dovekie_HD.csv')))
        zhd = np.array([float(r['zHD']) for r in rows]); zhel = np.array([float(r['zHEL']) for r in rows]); m = np.array([float(r['MU']) for r in rows])
        d = np.load(D + 'sn_data/DES-Dovekie/covtot_inv_000.npz'); n = int(d[d.files[0]][0]); IS = np.zeros((n, n)); IS[np.triu_indices(n)] = d[d.files[1]]
        il = np.tril_indices(n, -1); IS[il] = IS.T[il]
    elif name == 'pantheonplus':
        hdr = open(D + 'sn_data/PantheonPlus/Pantheon+SH0ES.dat').readline().split()
        dat = np.genfromtxt(D + 'sn_data/PantheonPlus/Pantheon+SH0ES.dat', names=True, dtype=None, encoding=None)
        cov = np.loadtxt(D + 'sn_data/PantheonPlus/Pantheon+SH0ES_STAT+SYS.cov', skiprows=1); n0 = len(dat); cov = cov.reshape(n0, n0)
        msk = dat['zHD'] > 0.01; zhd = dat['zHD'][msk]; zhel = dat['zHEL'][msk]; m = dat['m_b_corr'][msk]; IS = np.linalg.inv(cov[np.ix_(msk, msk)])
    else:
        dat = np.genfromtxt(D + 'sn_data/Union3/lcparam_full.txt', names=True, dtype=None, encoding=None, comments=None)
        zhd = dat['zcmb'].astype(float); zhel = dat['zhel'].astype(float); m = dat['mb'].astype(float)
        cv = np.loadtxt(D + 'sn_data/Union3/mag_covmat.txt'); n = int(cv[0]); IS = np.linalg.inv(cv[1:].reshape(n, n))
    return zhd, zhel, m, IS, IS.sum(axis=1), IS.sum()
def chi2(p, b, sn, extra=False):
    wb, wc, lVL, ui = p
    if not (0.018 < wb < 0.027 and 0.08 < wc < 0.16 and -3.0 < lVL < 0.5 and 1e-5 <= ui <= 0.21): return 1e9
    try: bg = background(wb, wc, math.exp(lVL), ui, b)
    except Exception: return 1e9
    if bg is None: return 1e9
    h = bg['h']
    if not (0.55 < h < 0.80): return 1e9
    rd, rs, zs = early(wb, wc)
    # CMB: R uses the early (z*) matter density; coupling negligible before z*
    Ds = DM(bg, zs) if zs <= bg['z'][-1] else None
    if Ds is None: return 1e9
    wm = wb + wc + 0.0587/93.14
    x = np.array([math.sqrt(wm)*100*Ds/C, math.pi*Ds/rs, wb, 0.9706]) - mu_cmb; cc = float(x @ ICMB @ x)
    if BZ is None: _bao()
    th = []
    for z, q in zip(BZ, BQ):
        dm = DM(bg, z); dh = C/Hz(bg, z); th.append({'DM_over_rs': dm/rd, 'DH_over_rs': dh/rd, 'DV_over_rs': (z*dm*dm*dh)**(1/3)/rd}[q])
    y = np.array(th) - BV; cb = float(y @ IB @ y)
    zhd, zhel, m, IS, one, Es = sn
    dl = (1 + zhel)*DM(bg, zhd); t = m - 5*np.log10(dl) - 25; cs = float(t @ IS @ t - (one @ t)**2/Es)
    if not extra: return cc + cb + cs
    return cc + cb + cs, dict(cmb=cc, bao=cb, sn=cs, H0=100*h, bg=bg)

_SN = {}
def run(a):
    """a: {"mode": "background"|"chi2"|"fit", "b": 0.0, "ui": 0.13, "wb": 0.02236, "wc": 0.119, "lVL": -1.0, "sn": "dovekie"|"pantheonplus", "maxiter": 300}"""
    mode = a.get('mode', 'background'); b = float(a.get('b', 0.0)); ui = float(a.get('ui', 0.13))
    p = [float(a.get('wb', 0.02236)), float(a.get('wc', 0.119)), float(a.get('lVL', -1.0)), ui]
    if mode == 'background':
        bg = background(p[0], p[1], math.exp(p[2]), ui, b)
        if bg is None: return {'error': 'solver failed (u_i past the collapse edge ~0.22, or bad V_L)'}
        zz = [0, 0.3, 0.5, 1, 1.5, 2, 3]; a_ = bg['a']; w = (bg['E2']*bg['v']**2/6 - (bg['rphi'] - bg['E2']*bg['v']**2/6))/bg['rphi']
        wz = {str(z): float(np.interp(z, (1/a_ - 1)[::-1], w[::-1])) for z in zz}
        rd, rs, zs = early(p[0], p[1])
        return {'H0': 100*bg['h'], 'w_thread(z)': wz, 'DM_Mpc(z)': {str(z): float(DM(bg, z)) for z in zz[1:]}, 'r_d': rd, 'r_s_zstar': rs,
                'Omega_phi0': float(bg['rphi'][-1]/bg['E2'][-1]), 'note': 'w can never go below -1 (single canonical thread)'}
    name = a.get('sn', 'dovekie')
    if name not in _SN: _SN[name] = load_sn(name)
    if mode == 'chi2':
        c, d = chi2(p, b, _SN[name], True); d.pop('bg'); d['chi2'] = c; return d
    r = minimize(chi2, p, args=(b, _SN[name]), method='Nelder-Mead', options={'maxiter': int(a.get('maxiter', 300)), 'xatol': 1e-6, 'fatol': 1e-4})
    return {'chi2': float(r.fun), 'p': [float(x) for x in r.x], 'keys': ['wb', 'wc', 'lVL', 'ui'], 'converged': bool(r.success)}
if __name__ == '__main__':
    print(json.dumps(run(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}), indent=1, default=float))
