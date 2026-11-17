"""J7d2 (locked PREREG_J7d2_psni)."""
import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.anyV import start_bisect
from tools.janus_calc.core import spectra3
from tools.serapis_calc.ms import Background, spectra_fast
DL = tuple(np.linspace(-1, 1, 9)); A = {}
for l in open('field_tests/results/janus_j7d_aspic_raw.txt'):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
al, f = 1e-3, 5.0; top = f*math.pi/2
V = lambda y: 1 + al*math.log(math.sin(y/f)); dV = lambda y: al*math.cos(y/f)/math.sin(y/f)/f
y60 = f*(math.pi/2 - A[(3, 60.0)]['x']); L = []
try:
    m = start_bisect(V, dV, y60, top*(1 - 1e-12), Nwant=80.0); y0 = m.sol.y[0][0]
    bg = Background(V, dV, y0, Nmax=20000); L.append(f"J1b start y0 = {y0:.10f} (top {top:.10f}), N_tot = {m.Nend:.3f}")
    for N in (50.0, 60.0):
        t = time.time(); j = spectra3(m, N); tj = time.time() - t; b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = A[(3, N)]
        L.append(f"PSNI a=1e-3 f=5 N*={N:.0f} (exact ns {b['ns']:.6f} r {b['r']:.3e} a {b['alpha_s']:.3e}) | dns J {abs(j['ns']-b['ns']):.1e} A {abs(a['ns']-b['ns']):.1e} | dr/r J {abs(j['r']/b['r']-1):.1e} A {abs(a['r']/b['r']-1):.1e} | da J {abs(j['alpha_s']-b['alpha_s']):.1e} A {abs(a['a']-b['alpha_s']):.1e} | J {tj*1e3:.1f} ms")
except Exception as e:
    L.append(f"J1b bisection failed: {e} — stop, as locked")
open('field_tests/results/janus_j7d2_psni.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
