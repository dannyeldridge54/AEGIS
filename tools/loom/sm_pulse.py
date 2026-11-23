"""D2166: the Standard Model pulsed through the Weave, centre outward (consistency map, not a test).
Each SM item gets: Weave layer, Weave value (from the records), data, status. Status classes:
 P = predicted/derived number, S = structure derived (borrowed model), R = relation (one number from others),
 F = fitted/tuned, I = input chosen, X = fails, M = missing (no derivation), O = obstructed (in a related geometry).
Breathing: INHALE counts only P/S/R (what the Weave gives without spending a dial); EXHALE also counts F/I (balanced by dials)."""
import json, collections
SM = [
 # item, layer, weave value, data, status, source
 ('Gauge group SU(3)xSU(2)xU(1)', 'L7', 'from D6-brane stacks of the published Z6-II model', 'SU(3)xSU(2)xU(1)', 'S', 'D2147/D2152 (Gmeiner-Honecker model reproduced)'),
 ('Three generations', 'L7', '3 crossings in the published Z6-II model', '3', 'S', 'D2147'),
 ('Higgs doublet(s)', 'L7', 'non-chiral b-c strings (a pair, MSSM-like)', '1 doublet seen', 'S', 'D2152'),
 ('alpha_s (g3)', 'L7', '0.1142', '0.1180 +- 0.0009', 'X', 'D1929, -4.2 sigma; balances only with the split-stack fit'),
 ('sin^2 theta_W (g1, g2)', 'L7', 'assumed via unification', '0.2312', 'I', 'v4 chain uses MSSM unification; not computed for Z6-II'),
 ('m_u, m_c, m_t (scale)', 'L1', 'top Yukawa not derived', 'm_t = 172.6 GeV', 'M', 'top Yukawa from brane angles listed as a held-out target (D-note line 20740)'),
 ('Up-quark ratios', 'L1', 'rung ~8 (68%: 5-14); m_u/m_t ~ 3.9e-6, m_c/m_t ~ 1.2e-3 (medians)', 'order-of-magnitude match', 'F', 'rung coefficient C fitted (NPP 2201.02020)'),
 ('Down-quark ratios', 'L1', 'rung 1; m_d/m_b ~ 7.6e-4, m_s/m_b ~ 0.017 (medians)', 'order-of-magnitude match', 'F', 'same fitted C'),
 ('m_e, m_mu', 'L3', 'inputs at the knot rho', 'measured', 'I', 'Koide uses them'),
 ('m_tau', 'L3', '1776.969 MeV from Koide Q = 2/3', '1776.93 +- 0.09 MeV (PDG, recalled)', 'R', 'locked forecast B1; Koide relation, no derivation of Q (D1600s)'),
 ('CKM angles (3)', 'L1', 'V_us 0.16, V_cb 0.017, V_ub 0.0028 (medians)', '0.2245, 0.0410, 0.0038', 'F', 'order-of-magnitude from the fitted ladder; V_us obstructed in the Z2xZ6prime brane model (K9)'),
 ('CKM CP phase', 'L1', 'not derived', '~66 deg', 'M', '-'),
 ('Higgs vev 246 GeV', 'L5', 'not derived (electroweak scale tuned)', '246 GeV', 'M', 'tan beta chain D2099'),
 ('Higgs mass 125 GeV', 'L5', '125 at tan beta 1.9', '125.2 GeV', 'F', 'tan beta chosen for m_h; boundary gives 1.4 (D2099 tension)'),
 ('theta-bar (strong CP)', 'L7', '0 exactly', '< 1e-10', 'P', 'preprint table'),
 ('Neutrino mass sum', 'L2', '0.0587 eV, normal ordering', '< 0.064 eV (DESI DR2)', 'I', 'chosen input'),
 ('Lightest neutrino mass', 'L2', 'near zero', 'unknown', 'P', 'seesaw at M_N ~ 1.8e11 GeV'),
 ('sin^2 theta_12', 'L2', '0.3184 (TM1)', '0.3092 +- 0.0087 (JUNO)', 'I', 'TM1 chosen after JUNO'),
 ('theta_13, theta_23', 'L2', 'inputs to TM1', 'measured', 'I', '-'),
 ('delta_CP (leptons)', 'L2', '262 or 286 deg', 'T2K/NOvA: broad', 'P', 'TM1 + octant'),
 ('Majorana phases (m_bb)', 'L2', 'm_bb 1.6-3.8 meV', 'below reach', 'P', 'D1667'),
]
PRED = {'P', 'S', 'R'}; DIAL = {'F', 'I'}
order = ['L1', 'L2', 'L3', 'L5', 'L7']
rows = []
for L in order:
    items = [s for s in SM if s[1] == L]
    c = collections.Counter(s[4] for s in items)
    inh = sum(c[k] for k in PRED); exh = inh + sum(c[k] for k in DIAL); n = len(items)
    rows.append(dict(layer=L, n=n, inhale=inh, exhale=exh, fails=c['X'], missing=c['M'] + c['O'], counts=dict(c)))
    print(f"{L}: {n} items | inhale (no dials) {inh}/{n} | exhale (with dials) {exh}/{n} | fail {c['X']} | missing {c['M']}")
tot = collections.Counter(s[4] for s in SM)
print('ALL', len(SM), dict(tot), '| inhale', sum(tot[k] for k in PRED), '| exhale', sum(tot[k] for k in PRED | DIAL))
json.dump(dict(items=[dict(zip(['item', 'layer', 'weave', 'data', 'status', 'source'], s)) for s in SM], layers=rows, totals=dict(tot)),
          open('field_tests/results/d2166_sm_pulse.json', 'w'), indent=1)
