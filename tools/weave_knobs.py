"""Central-equation engine (Danny 16:49-16:55; UFE v4 §8). Three knob equations feed one central map O(K_S, K_T, K_U).
K_S = g_s; K_T = (sigma_vis, Vol, A) with N = 6; K_U = |u| (decoupled from these observables in the current chain: I_TU = 0).
Outputs: (1) the knob Jacobian d ln O / d ln K at three step sizes (three vectors) + the step-size floor; (2) targeting ("steer each
body to the destination"): the knob setting closest to the data, with the wino bound enforced; the residual sizes the missing seam."""
import json, math, sys
sys.path.insert(0, 'tools/weave_cm'); from weave_tools import weave_rg2
MP = 2.435e18; N = 6; a2, a3g = 1 / 29.9, 0.092
base = dict(g_s=2 / math.sqrt(3), sigma=20.15, Vol=4.0e4, A=0.54)
def chain(k):
    x = 2 * math.pi * k['sigma'] / N; W0 = k['A'] * math.exp(-x) * (1 + 2 * x / 3)
    m32 = math.sqrt(k['g_s'] / 2) / k['Vol'] * W0 * MP
    wino = a2 / (4 * math.pi) * m32; gluino = 3 * a3g / (4 * math.pi) * m32 * (4926.4 / (3 * a3g / (4 * math.pi) * 257945.66))
    r = weave_rg2(dict(m_wino=wino, m_gluino=gluino, m_scalar=4.7e5 * m32 / 257945.66))
    return dict(m32=m32, wino=wino, gluino=gluino, alpha_s=r['alpha_s_unif'], M12=r['M12_GeV'], tau_p=1.6e35 * (r['M12_GeV'] / 1.0729587e16) ** 4)
O0 = chain(base); obs = list(O0)
jac = json.load(open('field_tests/results/d1937_knobs_run1.json'))['jacobian_dlnO_dlnK'] if len(sys.argv) > 1 else {}
for kn in ([] if len(sys.argv) > 1 else base):
    rows = []
    for h in (0.02, 0.05, 0.10):
        up, dn = dict(base), dict(base); up[kn] *= 1 + h; dn[kn] /= 1 + h
        Ou, Od = chain(up), chain(dn)
        rows.append({o: (math.log(Ou[o]) - math.log(Od[o])) / (2 * math.log(1 + h)) for o in obs})
    jac[kn] = {o: dict(values=[r[o] for r in rows], centre=sorted(r[o] for r in rows)[1], floor=max(r[o] for r in rows) - min(r[o] for r in rows)) for o in obs}
# targeting: every observable here depends on the knobs only through m3/2 (the seam I_ST). Scan m3/2 via sigma (the T knob).
def at_sigma(s): k = dict(base); k['sigma'] = s; return chain(k)
# bisection on sigma for the wino bound (deterministic: report as bisection to res)
lo, hi = 20.15, 20.40      # DEVIATIONS: wino(lo) > 660 > wino(hi)
assert at_sigma(lo)['wino'] > 660 > at_sigma(hi)['wino'], 'VOID bracket'
for _ in range(40):
    mid = (lo + hi) / 2; (lo, hi) = (mid, hi) if at_sigma(mid)['wino'] > 660 else (lo, mid)
edge = at_sigma(lo)
pull_edge = (edge['alpha_s'] - 0.1180) / 0.0009
need = 0.1180 - edge['alpha_s']
out = dict(base_knobs=base, base_observables=O0, jacobian_dlnO_dlnK=jac,
           targeting=dict(note='all these observables move only through m3/2 (seam I_ST); best alpha_s allowed by the wino bound is at the bound',
                          sigma_at_wino_bound=lo, m32_at_bound=edge['m32'], alpha_s_best=edge['alpha_s'], pull_best=pull_edge,
                          balanced=abs(pull_edge) <= 2, missing_seam_delta_alpha_s=need,
                          verdict='NO KNOB SETTING BALANCES: residual must come from a new I_ST term' if abs(pull_edge) > 2 else 'BALANCED'))
print(json.dumps(out, indent=1, default=float)); json.dump(out, open('field_tests/results/d1937_knobs.json', 'w'), indent=1, default=float)
