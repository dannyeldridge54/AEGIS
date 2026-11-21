import math, json, sys, cmath
sys.path.insert(0, 'tools/weave_cm'); from weave_tools import weave_rg2
from mpmath import mpc, exp, pi, qp
def eta(t):
    q = exp(2j * pi * t); return complex(exp(1j * pi * t / 12) * qp(q))
r = weave_rg2({'m_gluino': 5565}); D3 = r['Delta3']
rho = complex(0.5, math.sqrt(3) / 2); LU = math.log(rho.imag * abs(eta(rho)) ** 4)
sT = 20.15; LT = math.log(sT * abs(eta(1j * sT)) ** 4)
out = dict(Delta3=D3, M12=r['M12_GeV'], eta_rho=abs(eta(rho)), L_U=LU, L_T=LT)
for name, L in (('U', LU), ('U+T', LU + LT)):
    per = -L / (4 * math.pi)          # delta_a per unit b_a
    need = D3 / per                    # b3 - b12
    near = round(need * 2) / 2
    v = 'UNNATURAL' if abs(need) < 0.25 or abs(need) > 6 else ('NATURAL' if abs(need - near) <= 0.25 else 'NEUTRAL')
    out[name] = dict(shift_per_unit_b=per, db_needed=need, nearest_half_integer=near, verdict=v)
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1816_threshold.json', 'w'), indent=1)
