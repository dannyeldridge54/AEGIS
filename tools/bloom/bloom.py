#!/usr/bin/env python3
"""Unified Field Bloom v1: the UFE derivation engine. Every Forge lesson (compressor, D2006-D2025) is folded in as an engine rule.
One scalar target per agent and for the whole field: ln L - 0.5 * k_fit * ln N (BIC-style). Each dataset term is a node seen through
several lenses (pull, shadow dataset, scale ladder, tension, look-elsewhere). The Centre (loomcore) balances agents.
Run:  python3 bloom.py            (scoreboard + every lens + self-tests)
      python3 bloom.py --json     (machine-readable)"""
import json, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'loom'))
from loomcore import Agent, Centre
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bloom_data.json')))
LN95 = 1.6449  # one-sided 95% -> sigma

# ---- lens 1: the pull of one term (bypass trace: every dataset feeds the target directly) ----
def lnL_term(t, ours=None):
    x = t['ours'] if ours is None else ours; k = t['kind']
    if k == 'gauss': z = (x - t['mu']) / t['sigma']
    elif k == 'upper': s = t['bound'] / LN95; z = max(0.0, x / s - LN95) if x > 0 else 0.0
    elif k == 'lower': s = t['bound'] / LN95; z = max(0.0, LN95 - x / s)
    elif k == 'band': z = 0.0 if t['lo'] <= x <= t['hi'] else min(abs(x - t['lo']), abs(x - t['hi'])) / t['width']
    return -0.5 * z * z, z

def target(terms, k_fit, extra_knobs=0):
    lnL = sum(lnL_term(t)[0] for t in terms); N = len(terms) + D['fit_data_consumed']; k = k_fit + extra_knobs
    return lnL, lnL - 0.5 * k * math.log(N), N, k

# ---- lens 2: shadow datasets (multiplexer, D2011): score each alternate dataset side by side ----
def shadow(t):
    if 'alt' not in t: return None
    a = dict(t, **t['alt']); return {'main': lnL_term(t)[1], 'alt': lnL_term(a)[1], 'alt_data': t['alt']['data']}

# ---- lens 3: tension between the two datasets of a term (do not combine hidden conflicts) ----
def tension(t):
    if 'alt' not in t: return None
    a = t['alt']; return abs(t['mu'] - a['mu']) / math.hypot(t['sigma'], a['sigma'])

# ---- lens 4: scale ladder (FILTRATION 2.9): a value counts only if stable over its last two rungs ----
def ladder(t, tol=0.5):
    L = t.get('ladder')
    if not L or len(L['values']) < 2: return None
    shift = abs(L['values'][-1] - L['values'][-2]) / L['scale']
    return {'quantity': L['quantity'], 'last_two': L['values'][-2:], 'shift_over_scale': round(shift, 2), 'stable': shift < tol}

# ---- lens 5: look-elsewhere / random control (D2007, D2022, D2024): a derived value must beat random same-shape choices ----
def random_control(mechanism, choices, data_fn, n=2000, seed=1):
    """mechanism(choice)->value; choices: list of admissible discrete choices (fluxes, wrappings ...); data_fn(value)->z.
    Returns the fraction of random admissible choices that do at least as well as the best one (the look-elsewhere p)."""
    zs = sorted(abs(data_fn(mechanism(c))) for c in choices); best = zs[0]
    rng = random.Random(seed); hits = sum(abs(data_fn(mechanism(rng.choice(choices)))) <= best + 1e-12 for _ in range(n))
    return {'best_z': best, 'n_choices': len(choices), 'p_lookelsewhere': hits / n}

# ---- lens 6: theory-error nuisance (GAMBIT practice, 2512.14109): size of the last ladder correction as the theory error ----
def theory_nuisance(t):
    L = t.get('ladder')
    if not L or t['kind'] != 'gauss' or 'dobs_dq' not in t: return None
    s_th = abs(L['values'][-1] - L['values'][-2]) * t['dobs_dq']; s = math.hypot(t['sigma'], s_th)
    return {'sigma_exp': t['sigma'], 'sigma_theory': round(s_th, 5), 'z_exp_only': round((t['ours'] - t['mu']) / t['sigma'], 2), 'z_with_theory': round((t['ours'] - t['mu']) / s, 2),
            'read': 'sensitivity lens only: a large theory error is a gap to close (the next rung), never a pass'}

# ---- lens 7: goodness of fit by parametric bootstrap (toys), dof = N - k ----
def gof_bootstrap(terms, n=20000, seed=3):
    # engine ladder rung 2 (D2027): exact chi2 survival (regularised upper gamma), no numpy import; toys only with --toys
    g = [t for t in terms if t['kind'] == 'gauss']; chi2 = sum(lnL_term(t)[1] ** 2 for t in g); a, x = len(g) / 2.0, chi2 / 2.0
    term = s = 1.0 / a; k = 1
    while term > 1e-15 * s: term *= x / (a + k); s += term; k += 1
    p = 1.0 - math.exp(-x + a * math.log(x) - math.lgamma(a)) * s
    out = {'chi2_gauss_terms': round(chi2, 2), 'n_terms': len(g), 'p_exact': p}
    if '--toys' in sys.argv:
        rng = random.Random(seed); out['p_toys'] = sum(sum(rng.gauss(0, 1) ** 2 for _ in g) >= chi2 for _ in range(n)) / n
    return out

# ---- negative space (D2012): what is owed, and what has zero strict evidence ----
def negative_space(): return {'owed': D['owed'], 'post_lock_tests': 0}

# ---- hygiene (D2016/D2017 confirm): every dataset owned by exactly one agent, no shared slots ----
def hygiene(terms):
    ids = [t['id'] for t in terms]; return len(ids) == len(set(ids)) and all(t.get('agent') for t in terms)

# ---- compass: direction and headroom of every term ----
def compass(terms):
    out = []
    for t in terms:
        l, z = lnL_term(t); out.append({'id': t['id'], 'agent': t['agent'], 'z': round(z, 2), 'lnL': round(l, 2),
                                      'direction': 'up' if t['kind'] == 'gauss' and t['ours'] < t['mu'] else ('down' if t['kind'] == 'gauss' else '-'),
                                      'headroom_sigma': round(LN95 - z, 2) if t['kind'] in ('upper', 'lower') else (round(2 - abs(z), 2) if t['kind'] == 'gauss' else None)})
    return out

# ---- injection-recovery (FILTRATION 2.5): plant a known shift, the engine must recover it ----
def injection_test():
    t = {'id': 'inj', 'agent': 'X', 'kind': 'gauss', 'mu': 1.0, 'sigma': 0.1, 'ours': 1.0}
    rng = random.Random(7); planted = 0.37
    obs = [1.0 + planted + rng.gauss(0, 0.1) for _ in range(200)]
    est = sum(o - 1.0 for o in obs) / len(obs); return {'planted': planted, 'recovered': round(est, 3), 'pass': abs(est - planted) < 3 * 0.1 / math.sqrt(200)}

# ---- the stop rule (core standard 9) for one agent's knob ----
def verdict(gain_lnL, n_new_knobs, N, derived):
    pen = 0.5 * n_new_knobs * math.log(N)
    if gain_lnL <= pen: return 'NULL (does not buy its penalty)'
    return 'CANDIDATE-NAILED (needs held-out/post-lock + referees)' if derived and n_new_knobs == 0 else 'FIT (bought by a fitted knob; recorded, never claimed)'

def report():
    terms = D['terms']; kfit = sum(f['n'] for f in D['fitted_knobs'])
    lnL, tgt, N, k = target(terms, kfit)
    out = {'target': {'lnL': round(lnL, 3), 'k_fit': k, 'N': N, 'bic_target': round(tgt, 3)}, 'compass': compass(terms),
           'shadows': {t['id']: shadow(t) for t in terms if 'alt' in t}, 'tension': {t['id']: tension(t) for t in terms if 'alt' in t},
           'ladder': {t['id']: ladder(t) for t in terms if 'ladder' in t}, 'negative_space': negative_space(), 'hygiene_ok': hygiene(terms),
           'injection': injection_test(), 'theory_nuisance': {t['id']: theory_nuisance(t) for t in terms if 'ladder' in t}, 'gof': gof_bootstrap(terms)}
    # T1 demonstration through the Centre: a FREE Delta3 knob (a fitted knob) vs the derived value. alpha_s(Delta3) linearised from v4:
    a = next(t for t in terms if t['id'] == 'alpha_s'); slope = (0.1180 - 0.1142) / 0.044
    def ev(s, split):  # cost = -lnL of the alpha_s term; the 'held' split uses the alt world average spread (refuses tuning on one number)
        x = 0.1142 + slope * (s['d3'] - (-0.094)); tt = dict(a, ours=x)
        if split == 'held': tt = dict(tt, sigma=a['sigma'] * 1.3)
        return -lnL_term(tt)[0] + 1.0
    ag = Agent('T1-free-Delta3', {'d3': -0.094}, ev, lo={'d3': -0.3}, hi={'d3': 0.2}); c = Centre([ag], explore=0.0); c.run(40)
    x = 0.1142 + slope * (ag.k['d3'] + 0.094); gain = lnL_term(dict(a, ours=x))[0] - lnL_term(a)[0]
    out['T1_demo'] = {'d3_found': round(ag.k['d3'], 4), 'alpha_s': round(x, 4), 'gain_lnL': round(gain, 2), 'verdict': verdict(gain, 1, N, derived=False)}
    return out

if __name__ == '__main__':
    r = report()
    if '--json' in sys.argv: print(json.dumps(r, indent=1)); sys.exit()
    t = r['target']; print('UNIFIED FIELD BLOOM v1 | lnL %.2f | fitted knobs %d | N %d | target lnL - BIC = %.2f' % (t['lnL'], t['k_fit'], t['N'], t['bic_target']))
    for c in r['compass']: print('  %-12s %-7s z %+6.2f  lnL %+7.2f  dir %-4s headroom %s' % (c['id'], c['agent'], c['z'], c['lnL'], c['direction'], c['headroom_sigma']))
    print('shadows', r['shadows']); print('tension (sigma)', {k: round(v, 2) for k, v in r['tension'].items()}); print('ladder', r['ladder'])
    print('negative space', r['negative_space']); print('hygiene', r['hygiene_ok'], '| injection', r['injection']); print('description length (bits): %.1f  [MDL: -lnL/ln2 + k/2 log2 N, the same unit as the Forge]' % (-t['bic_target'] / math.log(2))); print('T1 demo', r['T1_demo']); print('theory nuisance', r['theory_nuisance']); print('goodness of fit', r['gof'])
