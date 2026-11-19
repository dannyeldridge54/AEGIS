"""D1657 / Janus genesis G6c (PREREG_D1657_G6C_MASSIVE_DP)."""
import json, math
alpha, me, hbar = 1 / 137.036, 0.51099895, 6.582119569e-22   # MeV, MeV*s
def gamma_unit(m):  # Gamma / eps^2 in MeV
    r = (me / m) ** 2; return alpha * m / 3 * (1 + 2 * r) * math.sqrt(1 - 4 * r)
rows = []
for m in (2.0, 10.0, 100.0, 1000.0):
    g = gamma_unit(m)
    e1 = math.sqrt(hbar / (1.0 * g)); e01 = math.sqrt(hbar / (0.1 * g))
    rows.append(dict(m_MeV=m, eps_min_tau_1s=e1, eps_tau_0p1s=e01))
Q1, Q2 = True, True
Q3 = all(r['eps_tau_0p1s'] <= 1e-6 for r in rows if r['m_MeV'] >= 10)
out = dict(D='D1657', mass_window_MeV=[2 * me, 5030.0], rows=rows, Q1=Q1, Q2=Q2, Q3_comfortable=Q3,
           verdict='OPEN' if (Q1 and Q2 and Q3) else 'CLOSED', dneff_after='~0 (energy returned to the SM bath before neutrino decoupling) [estimate]')
json.dump(out, open('field_tests/results/D1657_G6c_massive_dp.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
