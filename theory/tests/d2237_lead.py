"""D2237 (PREREG_D2237_LEAD_PASS)."""
import json, math, sys
sys.path.insert(0, 'theory/tests'); sys.argv = ['x']
src = open('theory/tests/d2236_helm.py').read().split('out = []')[0]; g = {}; exec(src, g)
F, X, EA, machine, I0, SHARE = g['F'], g['X'], g['EA'], g['machine'], g['I0'], g['SHARE']
D = json.load(open('field_tests/results/d2236_helm_rerun.json'))
pick = lambda R, B: next(o for o in D['machines'] if o['variant'] == 'adas' and o['P_other'] == 'fixed100' and o['R'] == R and o['B'] == B)['best']
cases = [('ITER control', 6.2, 5.3, dict(n_over_nG=D['control_old_rules'] and 0.936, P_aux=73.0)), ('Nb3Sn R9 B6', 9.0, 6.0, pick(9.0, 6.0)), ('Nb3Sn R8 B8', 8.0, 8.0, pick(8.0, 8.0))]
q95 = 3.0; rows = []
for name, R, B, b in cases:
    m = machine(R, B)
    if name != 'ITER control': m['line_model'] = 'adas'
    nG = m['Ip'] / (math.pi * m['a'] ** 2) * 1e20; Pa = b['P_aux']; op = X.operating_point_fast(m, EA, n_avg=b['n_over_nG'] * nG, P_aux=Pa)
    Psep = op['P_alpha'] + Pa - op['P_rad_core']; A = R / m['a']
    Bp = 4e-7 * math.pi * m['Ip'] * 1e6 / (2 * math.pi * m['a'] * math.sqrt((1 + m['kappa'] ** 2) / 2)); lam = 0.63 * Bp ** -1.19 * 1e-3
    qpk = (2 / 3) * Psep / (2 * math.pi * R * lam * 5); seed = max(0.0, 1 - 10 / qpk)
    wl = op['P_fus'] * SHARE / m['S']; life = 20 / (7.11 * wl); pl = F.plant(op['P_fus'], Pa, dict(F.PLANT_DEMO, M=1.161))
    E1, E2 = Psep / R, Psep * B / (q95 * A * R)
    ready = E1 <= 17 and E2 <= 9.2 and seed <= 0.9 and life >= 2 and 1.021 >= 1.05
    rows.append(dict(machine=name, P_fus=op['P_fus'], P_net=pl['P_net'], Q_e=pl['Q_e'], P_sep=Psep, E1_PsepR=E1, E2_PsepB_qAR=E2, lambda_q_mm=lam * 1e3,
                     q_peak_unmitigated=qpk, seeding_needed=seed, wall_load=wl, fw_life_fpy=life, burn_kg_y=56.08 * op['P_fus'] / 1000, TBR=1.021, TBR_margin_met=False, lead_ready=ready))
json.dump(rows, open('field_tests/results/d2237_lead.json', 'w'), indent=1)
for r in rows: print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
