"""JANUS tick 12: E(rho,2) lattice sum, I^2 offset B = 1 - E(rho,2), fractional size at the A1 horizon exit (see PREREG)."""
import json, math, sys
import numpy as np
tau = complex(-0.5, math.sqrt(3)/2); y = tau.imag
M = 400
m = np.arange(-M, M+1)[:, None]; n = np.arange(-M, M+1)[None, :]
z = np.abs(m + n*tau)**2
z[M, M] = np.inf
E = float(np.sum(y**2/z**2))
tail = 2*math.pi*y**2/(M**2)/ (math.sqrt(3)/2)       # continuum tail estimate for |w| > ~M: ∫ 2πR dR y²/R⁴ / cell area
z4 = math.pi**4/90
B = 1 - E
res = dict(E_rho_2=E, tail_estimate=tail, two_zeta4=2*z4, B=B)
for ys in (14.1, 14.7):
    I2 = 2*z4*ys**2; d = B/I2
    res[f'y{ys}'] = dict(I2=I2, delta=d, est_alpha_shift=2.1*abs(d))
c, It = math.log(1728)/(2*math.pi), 23.6; res['tau_i_c_over_I'] = c/It; res['tau_i_ratio'] = 0.108/(c/It)
est = max(res['y14.1']['est_alpha_shift'], res['y14.7']['est_alpha_shift'])
res['verdict'] = 'offset can explain it' if 0.034/2 <= est <= 0.034*2 else ('offset too small' if est < 0.0085 else 'inconclusive')
json.dump(res, open(sys.argv[1], 'w'), indent=1); print(json.dumps(res, indent=1))
