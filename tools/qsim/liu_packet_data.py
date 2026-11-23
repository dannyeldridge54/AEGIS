"""Builds the data files for the Liu-lab packet (D2184/D2185 + D2185a corrections). All THEORY."""
import sys, json, math, csv, numpy as np
sys.path.insert(0, 'tools/qsim'); from d2185_lib import ham, coherent, evolve
from loom_qsim import mf_run
OUT = 'releases/liu_gift_2026-11-23/data/'
d = json.load(open('field_tests/results/d2184_qsim_vs_liu2023.json'))
with open(OUT + 'A_period_vs_q_c2_23.7Hz.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['q_over_h_Hz', 'period_ms', 'rho0_peak_to_peak'])
    for q, T, a in zip(d['T_curve']['q_Hz'], d['T_curve']['T_ms'], d['T_curve']['amp']): w.writerow([q, '' if T is None else round(T, 4), round(a, 5)])
g = json.load(open('field_tests/results/d2185_liu.json'))['G3']
with open(OUT + 'B_beta_order_parameter_S_state.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['q_over_c2', 'beta_2_minus_App_cos_theta_half'])
    for q, b in zip(g['q_over_c2'], g['beta']): w.writerow([q, round(b, 5)])
c2 = 35.0; p = 1/3; ts = np.linspace(0, 40, 801)   # units of 1/c2
def ustate(B, N): return coherent(B, N, math.sqrt(0.2)*np.exp(1j*math.pi/2), math.sqrt(0.6), math.sqrt(0.2)*np.exp(1j*math.pi/2))
rows = []; summary = {}
for N in (6, 10, 20, 40, 80):
    H, B = ham(N, p); v0 = ustate(B, N); V = evolve(H, v0, ts); P = np.abs(V)**2
    n0 = np.array([s[1] for s in B])/N; m = np.array([s[0] - s[2] for s in B])/N
    r = P @ n0; vr = P @ n0**2 - r**2; M = P @ m; F = np.abs(V @ v0.conj())**2
    for t, a, b, c, e in zip(ts, r, vr, M, F): rows.append([N, round(t/c2*1e3, 4), round(a, 6), round(b, 6), round(c, 6), round(e, 8), round(e**(1/N), 6)])
    late = ts > 2; summary[N] = dict(rho0_max_after_57ms=float(r[late].max()), per_atom_fidelity_max_after_57ms=float((F[late]**(1/N)).max()))
with open(OUT + 'C_U_state_time_series_c2_35Hz_p_c2over3.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['N_atoms', 't_ms', 'mean_rho0', 'var_rho0', 'mean_M', 'return_probability_F', 'per_atom_fidelity_F^(1/N)']); w.writerows(rows)
t = json.load(open('field_tests/results/d2185_tuner.json'))
with open(OUT + 'D_tuned_small_N_settings_c2_35Hz.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['N_atoms_per_site', 'p_perp_over_c2', 'rho0_init', 'M_init', 'theta_init', 'eta_init', 'best_return_F', 't_rev_over_c2_inverse', 't_rev_ms_at_c2_35Hz', 'status'])
    for N in ('6', '10'):
        x = t[N]['best_x']; w.writerow([N, round(x['p_over_c2'], 4), round(x['rho0'], 4), 0, 'pi', round(x['eta'], 4), round(t[N]['best_F'], 4), round(t[N]['t_rev_units'], 4), round(t[N]['t_rev_ms_c2_35Hz'], 1), 'local optimum (prediction)'])
    for N in ('16', '24'): w.writerow([N, '', '', '', '', '', '', '', '', 'no revival inside 300 ms window'])
json.dump(summary, open(OUT + 'C_summary.json', 'w'), indent=1); print(summary)
