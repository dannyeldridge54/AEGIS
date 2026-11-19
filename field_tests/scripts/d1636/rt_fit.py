"""D1636 (PREREG_D1636_rt_full_likelihood.md): reverse thread vs LCDM / w0wa on DESI DR2 BAO + SN + compressed CMB.
Usage: python3 rt_fit.py <model: lcdm|w0wa|rt10|rt6|rt4> <sn: pantheonplus|union3|desy5> [theta_mean]"""
import sys, json, math, os, time
import numpy as np
import camb
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from cobaya.theory import Theory
from cobaya.model import get_model

PK = '/home/claude/cobaya_pk'
MODEL, SN = sys.argv[1], sys.argv[2]
TH_MEAN = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01041
A_PL = 16 * 1.6449340668482264 / (3 * 1.2020569031595942)          # 7.2983
BETA = {'rt10': 2 * math.sqrt(2), 'rt6': 2.0, 'rt4': math.sqrt(2)}
CMB_MU = np.array([TH_MEAN, 0.02223, 0.14208])
CMB_C = 1e-9 * np.array([[0.006621, 0.12444, -1.1929], [0.12444, 21.344, -94.001], [-1.1929, -94.001, 1488.4]])
CMB_IC = np.linalg.inv(CMB_C)
OMNU = 0.06 / 93.14


def rt_wtable(beta, u_i, Om, Or):
    """Thawing field w(a) for a in [1e-3, 1]; None if V < 0 is reached or the shoot fails."""
    Ode = 1 - Om - Or
    phi_i = math.log(A_PL / u_i) / beta
    def run(VL):
        def V(p): return VL * (1 - A_PL * math.exp(-beta * p))
        def dV(p): return VL * A_PL * beta * math.exp(-beta * p)
        def rhs(N, y):
            p, v = y; a = math.exp(N)
            rm, rr = 3 * Om / a ** 3, 3 * Or / a ** 4
            H2 = (rm + rr + V(p)) / (3 - v * v / 2)
            eps = (rm + 4 * rr / 3 + H2 * v * v) / (2 * H2)
            return [v, -(3 - eps) * v - dV(p) / H2]
        ev = lambda N, y: V(y[0]); ev.terminal = True
        sol = solve_ivp(rhs, (math.log(1e-3), 0.0), [phi_i, 0.0], rtol=1e-8, atol=1e-10, events=ev, dense_output=True)
        if sol.status == 1: return None, None
        p, v = sol.y[:, -1]; rm, rr = 3 * Om, 3 * Or
        H2 = (rm + rr + V(p)) / (3 - v * v / 2)
        return sol, (H2 * v * v / 2 + V(p)) / (3 * H2)
    VL = 3 * Ode / (1 - u_i)
    for _ in range(30):
        sol, Ophi = run(VL)
        if sol is None: return None
        if abs(Ophi / Ode - 1) < 1e-7: break
        VL *= Ode / Ophi
    Ns = np.linspace(math.log(1e-3), 0.0, 400); w = []
    for N in Ns:
        p, v = sol.sol(N); a = math.exp(N)
        Vp = VL * (1 - A_PL * math.exp(-beta * p))
        H2 = (3 * Om / a ** 3 + 3 * Or / a ** 4 + Vp) / (3 - v * v / 2); K = H2 * v * v / 2
        w.append((K - Vp) / (K + Vp))
    a = np.concatenate([[1e-8, 9.99e-4], np.exp(Ns)]); w = np.concatenate([[-1.0, -1.0], w])
    return a, np.array(w)


class BG(Theory):
    params = {'H0': None, 'ombh2': None, 'omch2': None, 'w0': None, 'wa': None, 'ui': None}
    def get_can_provide(self): return ['angular_diameter_distance', 'Hubble', 'comoving_radial_distance']
    def get_can_provide_params(self): return ['rdrag', 'thetastar']
    def calculate(self, state, want_derived=True, **p):
        h = p['H0'] / 100
        pars = camb.set_params(H0=p['H0'], ombh2=p['ombh2'], omch2=p['omch2'], mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                               TCMB=2.7255, dark_energy_model='ppf', w=-1.0, wa=0.0)
        if MODEL == 'w0wa':
            pars.DarkEnergy.set_params(w=p['w0'], wa=p['wa'])
        elif MODEL.startswith('rt'):
            Om = (p['ombh2'] + p['omch2'] + OMNU) / h ** 2; Or = 2.4728e-5 * (1 + 0.2271 * 3.044) / h ** 2
            tab = rt_wtable(BETA[MODEL], p['ui'], Om, Or)
            if tab is None: return False
            pars.DarkEnergy.set_w_a_table(tab[0], tab[1]); state['wtab'] = tab
        r = camb.get_background(pars); d = r.get_derived_params()
        state['res'] = r; state['derived'] = {'rdrag': d['rdrag'], 'thetastar': d['thetastar'] / 100}
    def get_angular_diameter_distance(self, z): return self.current_state['res'].angular_diameter_distance(np.atleast_1d(z))
    def get_comoving_radial_distance(self, z): return self.current_state['res'].comoving_radial_distance(np.atleast_1d(z))
    def get_Hubble(self, z, units='km/s/Mpc'):
        H = self.current_state['res'].hubble_parameter(np.atleast_1d(z))
        return H if units == 'km/s/Mpc' else H / 299792.458
    def get_param(self, p): return self.current_state['derived'][p]


SNL = {'pantheonplus': 'sn.pantheonplus', 'union3': 'sn.union3', 'desy5': 'sn.desy5'}
info = {'packages_path': PK, 'theory': {'bg': {'external': BG}},
        'likelihood': {'bao.desi_dr2.desi_bao_all': None, SNL[SN]: None},
        'params': {k: {'prior': {'min': lo, 'max': hi}} for k, lo, hi in
                   (('H0', 50, 90), ('ombh2', 0.019, 0.026), ('omch2', 0.08, 0.16), ('w0', -3, 1), ('wa', -3, 2), ('ui', 1e-6, 0.3))},
        'debug': False}
info['params']['thetastar'] = None; info['params']['rdrag'] = None
model = get_model(info)
FREE = {'lcdm': ['H0', 'ombh2', 'omch2'], 'w0wa': ['H0', 'ombh2', 'omch2', 'w0', 'wa'],
        'rt10': ['H0', 'ombh2', 'omch2', 'ui'], 'rt6': ['H0', 'ombh2', 'omch2', 'ui'], 'rt4': ['H0', 'ombh2', 'omch2', 'ui']}[MODEL]
BASE = dict(H0=68.0, ombh2=0.02223, omch2=0.1196, w0=-1.0, wa=0.0, ui=0.01)


def chi2(x, detail=False):
    p = dict(BASE); p.update(dict(zip(FREE, x)))
    if MODEL == 'w0wa' and p['w0'] + p['wa'] >= 0: return 1e10
    for k in FREE:
        lo, hi = info['params'][k]['prior']['min'], info['params'][k]['prior']['max']
        if not lo < p[k] < hi: return 1e10
    try:
        lp = model.logposterior(p, as_dict=True, make_finite=False)
    except Exception:
        return 1e10
    ll = lp.get('loglikes', {}) if isinstance(lp, dict) else {}
    if not ll or not all(np.isfinite(v) for v in ll.values()): return 1e10
    der = lp.get('derived', {})
    cv = np.array([der['thetastar'], p['ombh2'], p['ombh2'] + p['omch2'] + OMNU * 0])
    c_cmb = float((cv - CMB_MU) @ CMB_IC @ (cv - CMB_MU))
    parts = {k: -2 * v for k, v in ll.items()}; parts['cmb_compressed'] = c_cmb
    tot = sum(parts.values())
    return (tot, parts, der) if detail else tot


STARTS = {'lcdm': [[68, 0.02223, 0.119], [66, 0.0222, 0.122], [70, 0.0224, 0.116], [67.5, 0.0223, 0.12],
                   [69, 0.0222, 0.118], [65, 0.0221, 0.124], [71, 0.0225, 0.115], [68.5, 0.0224, 0.118]]}
STARTS['w0wa'] = [s + d for s, d in zip(STARTS['lcdm'], [[-0.8, -0.6], [-0.7, -1.0], [-0.9, -0.3], [-1.0, 0.0], [-0.75, -0.8], [-0.6, -1.4], [-0.85, -0.5], [-0.95, -0.2]])]
for m in ('rt10', 'rt6', 'rt4'):
    STARTS[m] = [s + [u] for s, u in zip(STARTS['lcdm'], [0.01, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.22])]

if __name__ == '__main__':
    t0 = time.time(); best = None
    for s in STARTS[MODEL]:
        r = minimize(chi2, s, method='Nelder-Mead', options=dict(maxiter=4000, xatol=1e-6, fatol=1e-4, adaptive=True))
        r = minimize(chi2, r.x, method='Nelder-Mead', options=dict(maxiter=4000, xatol=1e-7, fatol=1e-5, adaptive=True))
        print('start', s, '->', round(r.fun, 4), flush=True)
        if best is None or r.fun < best.fun: best = r
    tot, parts, der = chi2(best.x, detail=True)
    out = dict(model=MODEL, sn=SN, theta_mean=TH_MEAN, chi2=tot, parts=parts, best=dict(zip(FREE, map(float, best.x))),
               rdrag=der['rdrag'], thetastar=der['thetastar'], seconds=round(time.time() - t0, 1))
    if MODEL.startswith('rt'):
        p = dict(BASE); p.update(out['best']); h = p['H0'] / 100
        Om = (p['ombh2'] + p['omch2'] + OMNU) / h ** 2; Or = 2.4728e-5 * (1 + 0.2271 * 3.044) / h ** 2
        a, w = rt_wtable(BETA[MODEL], p['ui'], Om, Or); m = a > 1 / 3.0
        cpl = np.polyfit(1 - a[m], w[m], 1); out['cpl_fit'] = dict(w0=float(cpl[1]), wa=float(cpl[0]))
        out['Om'] = Om
    os.makedirs('field_tests/results/D1636', exist_ok=True)
    tag = f"{MODEL}_{SN}" + ('' if TH_MEAN == 0.01041 else f"_th{TH_MEAN}")
    json.dump(out, open(f'field_tests/results/D1636/{tag}.json', 'w'), indent=1)
    print(json.dumps(out))
