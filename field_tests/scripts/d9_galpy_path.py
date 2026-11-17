import sys, numpy as np; sys.path.insert(0, '.')
from tools.janus_astro import mapper_feed as F
S = [(-8, 0, 0.02, 11, 232, 7), (-8.5, 1, 0.3, 30, 200, 20), (-6, -2, -0.5, -50, 180, 40), (-10, 3, 1.5, 80, 120, -60), (-7, 0.5, 2.0, 150, 60, 100)]
A = np.array(S).T
g = F.orbit_params_galpy(*A, pot='MWPotential2014'); m = F.orbit_params_galpy(*A, pot='McMillan17')
out = []; ok = True
for i, s in enumerate(S):
    o = F.orbit_params(*s, t_gyr=3.0)
    d = [abs(g[k][i]/o[k] - 1) for k in ('rperi', 'rapo', 'zmax')]; ok &= max(d) <= 0.01
    out.append(f"star{i+1}: ours rp/ra/zm {o['rperi']:.3f}/{o['rapo']:.3f}/{o['zmax']:.3f} | galpy-MWP14 {g['rperi'][i]:.3f}/{g['rapo'][i]:.3f}/{g['zmax'][i]:.3f} (max rel {max(d):.1e}) | galpy-McM17 {m['rperi'][i]:.3f}/{m['rapo'][i]:.3f}/{m['zmax'][i]:.3f}")
out.append(f"R1 -> {'PASS' if ok else 'FAIL'}")
open('field_tests/results/d9_galpy_path.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
