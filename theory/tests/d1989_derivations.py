#!/usr/bin/env python3
"""D1989 P3 derivation tests (PREREG_D1989_complete_field.md). C1: cube axis H_Imtau, out-of-sample on quarks. C2: baryogenesis feasibility scan."""
import json, math, sys
sys.path.insert(0, 'tools/loom'); import check as C
ns_ = {}; exec(open('tools/loom/resonance.py').read().split("out = {'sweeps'")[0], ns_); obs, D = ns_['obs'], ns_['D']
step_i = math.exp(-9 * math.pi / 8); im_rho = math.sqrt(3) / 2
# C1
pred = {'rho': step_i * im_rho, 'i': step_i * 1.0}; lo, hi = 0.02588, 0.02740
c1_in = dict(lepton_slip=0.0253, H_Imtau_rho=round(pred['rho'], 5), frac_diff=round(pred['rho'] / 0.0253 - 1, 5))
cands = [step_i * f for f in (im_rho, 1 / im_rho, im_rho ** 2, 1 / im_rho ** 2, 0.5, 2, math.sqrt(2), 1 / math.sqrt(2), 1.0, 0.75)]
nflag, nmsg = C.c4_numerology(0.0253, 0.002, cands)
c1_out = {k: dict(pred=round(v, 5), in_window=lo <= v <= hi, miss_frac=round(min(abs(v - lo), abs(v - hi)) / (lo if v < lo else hi), 4) if not lo <= v <= hi else 0) for k, v in pred.items()}
c1_verdict = 'PASS' if any(x['in_window'] for x in c1_out.values()) else 'FAIL'
# C2
rows = []; TRd = D['TR']; mphi = ns_['m_phi']
for i in range(0, 401):
    TR = TRd * (mphi / TRd) ** (i / 400); k = dict(D); k['TR'] = TR; o = obs(k)
    ok = o['Y'] >= 0.87e-10 and o['Om'] <= 0.12 and abs(o['ns'] - 0.9728) / 0.0027 <= 2
    rows.append((TR, o['Y'], o['Om'], o['ns'], ok))
feas = [r for r in rows if r[4]]
c2 = dict(TR_derived=TRd, feasible=bool(feas), TR_min=feas[0][0] if feas else None, TR_max=feas[-1][0] if feas else None,
          fit_factor_min=round(feas[0][0] / TRd, 2) if feas else None, at_TR_min=dict(Y=feas[0][1], Om=feas[0][2], ns=feas[0][3]) if feas else None,
          verdict='FEASIBLE-BY-FIT' if feas else 'INFEASIBLE',
          why_upper=('Omega_wino h^2 reaches 0.12' if feas and feas[-1][2] > 0.11 else 'n_s leaves 2 sigma' if feas else None))
out = dict(prereg='PREREG_D1989_complete_field.md P3', C1=dict(in_sample=c1_in, numerology=nmsg, numerology_note='target is a best-fit point inside a broad natural range (0.0066-0.0435, D1877); the chance figure does not give evidential weight', out_of_sample=c1_out, verdict=c1_verdict), C2=c2)
json.dump(out, open('field_tests/results/d1989_derivations.json', 'w'), indent=1, default=str); print(json.dumps(out, indent=1, default=str))
