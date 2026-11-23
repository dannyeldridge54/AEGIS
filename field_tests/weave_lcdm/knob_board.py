#!/usr/bin/env python3
"""D2134 knob board: coupled reverse thread (thread-DM coupling b). Late background from own coupled solver, early
sound horizons from CAMB. Data: CHW compressed CMB + DESI DR2 + one SN set.   python knob_board.py gate | scan <dovekie|pantheonplus|union3>"""
import os, sys, json, math, time
import numpy as np, camb
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); D = '/tmp/claude-0/cobaya_pkgs/data/'
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
_cache = {}
def early(wb, wc):
    k = (round(wb, 6), round(wc, 6))
    if k not in _cache:
        P = camb.CAMBparams(); P.set_cosmology(H0=67.5, ombh2=wb, omch2=wc, mnu=0.0587, num_massive_neutrinos=3, neutrino_hierarchy='normal', nnu=NEFF, TCMB=2.7255)
        r = camb.get_background(P); wm = wb + wc + 0.0587/93.14
        g1 = 0.0783*wb**-0.238/(1 + 39.5*wb**0.763); g2 = 0.560/(1 + 21.1*wb**1.81); zs = 1048*(1 + 0.00124*wb**-0.738)*(1 + g1*wm**g2)
        _cache[k] = (r.get_derived_params()['rdrag'], r.sound_horizon(zs), zs)
    return _cache[k]
# ---- data
mu_cmb = np.array([1.7502, 301.471, 0.02236, 0.9649]); sg = np.array([0.0046, 0.0895, 0.00015, 0.0043])
rho = np.array([[1, .46, -.66, -.74], [.46, 1, -.33, -.35], [-.66, -.33, 1, .46], [-.74, -.35, .46, 1]]); ICMB = np.linalg.inv(rho*np.outer(sg, sg))
bl = [l.split() for l in open(D + 'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt') if not l.startswith('#')]
BZ = np.array([float(x[0]) for x in bl]); BV = np.array([float(x[1]) for x in bl]); BQ = [x[2] for x in bl]
IB = np.linalg.inv(np.loadtxt(D + 'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'))
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
    if not (0.018 < wb < 0.027 and 0.08 < wc < 0.16 and 0.0 < lVL < 1.5 and 1e-5 <= ui <= 0.21): return 1e9
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
    th = []
    for z, q in zip(BZ, BQ):
        dm = DM(bg, z); dh = C/Hz(bg, z); th.append({'DM_over_rs': dm/rd, 'DH_over_rs': dh/rd, 'DV_over_rs': (z*dm*dm*dh)**(1/3)/rd}[q])
    y = np.array(th) - BV; cb = float(y @ IB @ y)
    zhd, zhel, m, IS, one, Es = sn
    dl = (1 + zhel)*DM(bg, zhd); t = m - 5*np.log10(dl) - 25; cs = float(t @ IS @ t - (one @ t)**2/Es)
    if not extra: return cc + cb + cs
    return cc + cb + cs, dict(cmb=cc, bao=cb, sn=cs, H0=100*h, bg=bg)
def dials(p, b, sn):
    tot, d = chi2(p, b, sn, True); bg = d.pop('bg'); a = bg['a']; z = 1/a - 1
    rc0 = bg['rc'][-1]; rde = bg['rphi'] + bg['rc'] - rc0/a**3
    o = np.argsort(np.log(a)); lna = np.log(a)
    weff = -1 - np.gradient(np.log(np.abs(rde)), lna)/3
    sel = (z > 0.3) & (z < 2); s2 = (z >= 0) & (z <= 2)
    W = np.vstack([np.ones(s2.sum()), 1 - a[s2]]).T; w0, wa = np.linalg.lstsq(W, weff[s2], rcond=None)[0]
    Om0 = (p[0] + rc0 + 0.0587/93.14)/bg['h']**2
    # growth (Amendola coupled): delta_c'' + (2 + dlnH - b v) delta_c' = 1.5[(1+2b^2) Oc dc + Ob db];  delta_b'' + (2 + dlnH) db' = 1.5(Oc dc + Ob db)
    def grow(bb, bgx):
        aa = bgx['a']; N = np.log(aa); E2 = bgx['E2']; rcx = bgx['rc']; vv = bgx['v']
        Oc = rcx/E2; Ob = (p[0]/aa**3)/E2; lE = 0.5*np.log(E2); dlnH = np.gradient(lE, N)
        i0 = np.searchsorted(N, math.log(1/51))
        def f(Nn, y):
            k = min(max(np.searchsorted(N, Nn), 1), len(N) - 1)
            oc, ob, dh, v = Oc[k], Ob[k], dlnH[k], vv[k]
            return [y[1], -(2 + dh - bb*v)*y[1] + 1.5*((1 + 2*bb*bb)*oc*y[0] + ob*y[2]), y[3], -(2 + dh)*y[3] + 1.5*(oc*y[0] + ob*y[2])]
        s = solve_ivp(f, (N[i0], 0), [math.exp(N[i0]), math.exp(N[i0]), math.exp(N[i0]), math.exp(N[i0])], rtol=1e-7)
        dc, db = s.y[0, -1], s.y[2, -1]; return (rc0*dc + p[0]*db)/(rc0 + p[0])
    g = grow(b, bg); g0 = grow(0.0, background(p[0], p[1], math.exp(p[2]), 1e-4, 0.0))
    S8 = 0.811*(g/g0)*math.sqrt(Om0/0.3)
    d.update(chi2=tot, Om0=Om0, dm_loss_since_zstar=float(1 - bg['rc'][-1]*1.0/(p[1]) ), dphi_zstar=bg['dphi_star'],
             w_eff_cross=bool(np.any(weff[sel] < -1)), w_eff_min=float(weff[sel].min()), cpl=[float(w0), float(wa)], S8_proxy=S8)
    return d
def fit(b, sn, starts):
    best = None
    for s in starts:
        r = minimize(chi2, s, args=(b, sn), method='Nelder-Mead', options={'maxiter': 900, 'xatol': 1e-6, 'fatol': 1e-4})
        if best is None or r.fun < best.fun: best = r
    return best
if __name__ == '__main__':
    if sys.argv[1] == 'gate':
        wb, wc, H0 = 0.02236, 0.1195, 67.5
        # find VL giving H0 with ui = 0.13, b = 0
        from scipy.optimize import brentq
        f = lambda l: background(wb, wc, math.exp(l), 0.13, 0.0)['h']*100 - H0; l = brentq(f, 0.0, 1.4); bg = background(wb, wc, math.exp(l), 0.13, 0.0)
        a = bg['a']; w = (bg['E2']*bg['v']**2/6 - (bg['rphi'] - bg['E2']*bg['v']**2/6))/bg['rphi']
        P = camb.CAMBparams(); P.set_cosmology(H0=H0, ombh2=wb, omch2=wc, mnu=0.0587, num_massive_neutrinos=3, neutrino_hierarchy='normal', nnu=NEFF, TCMB=2.7255)
        P.DarkEnergy = camb.dark_energy.DarkEnergyPPF(); aa = np.concatenate([[1e-8], a]); ww = np.concatenate([[-1.0], w]); P.DarkEnergy.set_w_a_table(aa, ww)
        r = camb.get_background(P); out = {}
        for z in (0.3, 0.51, 1.0, 2.33, 1089.0):
            out[str(z)] = [float(DM(bg, z)/r.comoving_radial_distance(z) - 1), float(Hz(bg, z)/r.hubble_parameter(z) - 1)]
        mx = max(abs(v) for vs in out.values() for v in vs); out['max_rel_dev'] = mx; out['G0'] = 'PASS' if mx < 1.5e-3 else 'FAIL'
        print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, 'knob_gate.json'), 'w'), indent=1); sys.exit()
    name = sys.argv[2]; sn = load_sn(name); res = {}
    ref = fit(0.0, sn, [[0.02236, 0.119, 0.6, 1e-4]])
    # LCDM-like reference: b = 0, ui -> 1e-4 (fix ui by tight bounds through a wrapper)
    lc = minimize(lambda q: chi2([q[0], q[1], q[2], 1e-4], 0.0, sn), [0.02236, 0.119, 0.6], method='Nelder-Mead', options={'maxiter': 900, 'xatol': 1e-6, 'fatol': 1e-4})
    res['LCDM_ref'] = dict(chi2=float(lc.fun), p=[float(x) for x in lc.x])
    for b in [-0.15, -0.10, -0.075, -0.05, -0.025, 0.0, 0.025, 0.05, 0.10]:
        t = time.time(); best = fit(b, sn, [[0.02236, 0.119, 0.6, 0.05], [0.0224, 0.118, 0.6, 0.15]])
        try: dd = dials(list(best.x), b, sn)
        except Exception as e: dd = dict(chi2=float(best.fun), err=str(e))
        dd['p'] = [float(x) for x in best.x]; dd['dchi2_vs_LCDM'] = float(best.fun - lc.fun); dd['sec'] = time.time() - t; res[str(b)] = dd
        print(name, b, round(best.fun, 3), round(dd['dchi2_vs_LCDM'], 2), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in dd.items() if k in ('H0', 'Om0', 'cpl', 'w_eff_cross', 'S8_proxy', 'dphi_zstar')}, flush=True)
    json.dump(res, open(os.path.join(HERE, f'knob_{name}.json'), 'w'), indent=1, default=float)
