"""Resonance run 1 (RESONANCE_RUN1_METHOD): full hexagon settle with the centre tuning C, T_R, s_m32, d_as together (exploratory)."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hex as H
from scipy.optimize import minimize
B = H.B; D_AS_MAX = 0.004
_orig_forces_run = H.Forces.run
def forces_run(self, bus):
    out = _orig_forces_run(self, bus); a = bus.get('alpha_s') + bus.get('d_as', 0.0)
    bus.put(self.name, 'alpha_s', a, 'LIVE'); out['pull_alpha_s'] = H.gauss_pull(a, 0.118, 0.0009); return out
H.Forces.run = forces_run
def centre_score(bus):
    live = dict(n_s=bus.get('ns'), r=bus.get('r'), running=bus.get('running'), theta12=bus.get('theta12'), m_bb=bus.get('m_bb_meV'), sum_mnu=bus.get('sum_mnu'), alpha_s=bus.get('alpha_s'))
    base = B.apply_levers(B.D['terms'], {'lnm32': bus.get('s_m32')})
    return [dict(t, ours=live[t['id']]) if t['id'] in live else t for t in base]
H.centre_score = centre_score
H.ADOPTED = dict(H.ADOPTED, d_as=0.0)
LOG = []
def ev(x):
    C = float(f'{1e-6 * x[0]:.5e}'); TR = float(f'{1e8 * x[1]:.4e}'); s = float(x[2]); d = float(x[3]) * D_AS_MAX
    if not (1.0e-6 <= C <= 1.6e-6 and 1e8 <= TR <= 5e9 and 0.2 <= s <= 3.0 and abs(d) <= D_AS_MAX): return 1e9, None
    E = H.evaluate(dict(C=C, T_R=TR, s_m32=s, d_as=d)); LOG.append(dict(C=C, T_R=TR, s_m32=s, d_as=d, target=E['target'], lnL=E['lnL']))
    return -E['target'], E
if __name__ == '__main__':
    t0 = time.perf_counter(); f0, E0 = ev([1.25, 8.94, 1.0, 0.0])
    best = [f0, E0]
    def obj(x):
        f, E = ev(x)
        if E is not None and f < best[0]: best[0], best[1] = f, E
        return f
    for x0 in ([1.25, 8.94, 1.0, 0.0], [1.25, 8.94, 1.0, 0.9], [1.25, 8.94, 0.5, 0.5]):
        minimize(obj, x0, method='Nelder-Mead', options=dict(maxfev=70, xatol=1e-3, fatol=1e-3, initial_simplex=None))
    E = best[1]
    print('start ', H.board(E0).splitlines()[0]); print(H.board(E))
    res = dict(start=dict(knobs=E0['knobs'], target=E0['target'], lnL=E0['lnL'], local=E0['local']),
               settled=dict(knobs=E['knobs'], target=E['target'], lnL=E['lnL'], k=E['k'], N=E['N'], sweeps=E['sweeps'], local=E['local'],
                            bus={k: (v if not isinstance(v, float) or not math.isnan(v) else None) for k, v in E['bus'].v.items() if isinstance(v, (int, float, str, bool))}),
               evaluations=len(LOG), seconds=time.perf_counter() - t0, trace=LOG[-40:])
    json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'resonance_run1.json'), 'w'), indent=1, default=str)
