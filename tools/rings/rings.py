"""Ring Engine (PREREG_RING1): the Unified Field's layers in one pass, from where the fields settle out through the rings to the
observed pattern, scored with the Bloom's own likelihood and BIC. In-process and memoised, so a warm pass is milliseconds.
Usage: python rings.py            one pass + scoreboard
       python rings.py --fit      fit C (inflation coefficient) and rescore
       python rings.py --json     machine-readable"""
import functools, json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEGIS = os.path.abspath(os.path.join(HERE, '..', '..'))
for p in (AEGIS, os.path.join(AEGIS, 'tools', 'weave_cm'), os.path.join(AEGIS, 'tools', 'bloom'), os.path.join(AEGIS, 'tools', 'loom')): sys.path.insert(0, p)
import weave_tools as W
import bloom as B

S13SQ = 0.02224          # NuFIT 6.0 (IC19 w/o SK-atm) best fit sin^2 theta13, NO
ADOPTED = dict(C=1.25e-6, T_R=8.94e8, s_m32=1.0)

@functools.lru_cache(maxsize=256)
def pattern(C, T_R):
    """Pattern ring: exact SERAPIS spectra at the self-consistent N* (same code path as the registry's serapis_point)."""
    from tools.serapis_calc.pipeline import build
    from tools.janus_calc.core import Model, spectra3
    from tools.serapis_calc.nstar import Nstar
    m, V, dV, p0 = build('serapis_e', C); M = Model(V, dV, p0, Nmax=4000)
    Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        s = spectra3(M, N); ra = V(M.sol.sol(M.Nend - N)[0]) / Ve; N2 = Nstar(s['r'], ra, T_R)
        if abs(N2 - N) < 1e-3: break
        N = N2
    s = spectra3(M, N2)
    return dict(Nstar=N2, ns=float(s['ns']), r=float(s['r']), running=float(s['alpha_s']), V_ratio=ra)

@functools.lru_cache(maxsize=64)
def ring1(s13sq):
    s12 = 1 - 2 / (3 * (1 - s13sq))                       # TM1: |U_e1|^2 = 2/3
    mb = W.weave_mbb({'s12': s12})
    return dict(theta12=s12, m_bb=mb['mbb_max_meV'], sum_mnu=mb['sum_mnu_eV'], m_bb_min=mb['mbb_min_meV'])

@functools.lru_cache(maxsize=64)
def ring3(T_R):
    g = W.weave_genesis({'T_R_GeV': T_R}); w = W.weave_wino({'T_R_GeV': T_R})
    return dict(genesis_viable=bool(g['viable']), eps_needed=g['eps_needed'], wino_passing=w.get('passing'))

def one_pass(C=ADOPTED['C'], T_R=ADOPTED['T_R'], s_m32=ADOPTED['s_m32']):
    t0 = time.perf_counter()
    settle = W.weave_point({})
    rung = {m: W.weave_rung({'m': m})['eps_formula'] for m in (1, 8, 9)}
    r1 = ring1(S13SQ); r2 = W.weave_rg({}); r3 = ring3(T_R); pat = pattern(C, T_R)
    live = dict(theta12=r1['theta12'], m_bb=r1['m_bb'], sum_mnu=r1['sum_mnu'], n_s=pat['ns'], r=pat['r'], running=pat['running'])
    terms, source = [], {}
    base = B.apply_levers(B.D['terms'], {'lnm32': s_m32})          # wino, gluino, proton, alpha_s move with the m32 lever
    for t in base:
        if t['id'] in live: terms.append(dict(t, ours=live[t['id']])); source[t['id']] = 'LIVE'
        elif t['id'] in B.D['levers']['lnm32']['moves']: terms.append(t); source[t['id']] = 'LINEAR RESPONSE' if s_m32 != 1 else 'LINEAR RESPONSE (s=1)'
        else: terms.append(t); source[t['id']] = 'STORED'
    k_extra = 0
    return dict(knobs=dict(C=C, T_R=T_R, s_m32=s_m32), settle=settle, rings=dict(ring0_rung_eps=rung, ring1=r1, ring2=r2, ring3=r3, pattern=pat),
                terms=terms, source=source, seconds=time.perf_counter() - t0)

def score(P, k_extra=0):
    k_fit = sum(k['n'] for k in B.D['fitted_knobs'])
    lnL, tgt, N, k = B.target(P['terms'], k_fit, k_extra)
    return dict(lnL=lnL, target=tgt, N=N, k=k, pulls={t['id']: B.lnL_term(t)[1] for t in P['terms']})

def fit_C(T_R=ADOPTED['T_R'], lo=1.0e-6, hi=1.6e-6):
    from scipy.optimize import minimize_scalar
    t0 = time.perf_counter()
    f = lambda c: -score(one_pass(C=float(f'{c:.6e}'), T_R=T_R))['lnL']
    r = minimize_scalar(f, bounds=(lo, hi), method='bounded', options=dict(xatol=1e-9))
    C = float(f'{r.x:.6e}'); return dict(C=C, nfev=r.nfev, seconds=time.perf_counter() - t0, P=one_pass(C=C, T_R=T_R))

def board(P, S, title='Ring Engine'):
    lines = [f'{title}: knobs {P["knobs"]}  pass {P["seconds"]*1000:.1f} ms',
             f'  settle: alpha_inv(M12)={P["settle"]["alpha_inv_M12"]} M12={P["settle"]["M12_GeV"]:.3g} GeV N={P["settle"]["N"]} m32={P["settle"]["m32_GeV"]:.3g} GeV',
             f'  ring1: sin2th12={P["rings"]["ring1"]["theta12"]:.4f} m_bb<= {P["rings"]["ring1"]["m_bb"]:.2f} meV sum_mnu={P["rings"]["ring1"]["sum_mnu"]:.4f} eV',
             f'  ring3: genesis viable={P["rings"]["ring3"]["genesis_viable"]}  pattern: n_s={P["rings"]["pattern"]["ns"]:.5f} r={P["rings"]["pattern"]["r"]:.3g} N*={P["rings"]["pattern"]["Nstar"]:.2f}',
             f'  lnL={S["lnL"]:.3f}  target(lnL-BIC)={S["target"]:.3f}  k={S["k"]} N={S["N"]}']
    for t in P['terms']: lines.append(f'    {t["id"]:12s} {P["source"][t["id"]]:24s} ours={t["ours"]:<12.6g} pull={S["pulls"][t["id"]]:+.2f}')
    return '\n'.join(lines)

if __name__ == '__main__':
    P = one_pass(); S = score(P)
    if '--json' in sys.argv: print(json.dumps(dict(P=P, S=S), default=str)); sys.exit()
    print(board(P, S, 'Ring Engine (adopted point)'))
    if '--fit' in sys.argv:
        F = fit_C(); SF = score(F['P'], k_extra=1)
        print(f'\nfit C: {F["C"]:.6e} in {F["nfev"]} evals, {F["seconds"]:.1f} s'); print(board(F['P'], SF, 'Ring Engine (C fitted, +1 knob)'))
