"""J1d (locked PREREG_J1d_psni_field_end)."""
import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.core import Model, spectra3
from tools.serapis_calc.ms import Background, spectra_fast
DL = tuple(np.linspace(-1, 1, 9)); A = {}
for l in open('field_tests/results/janus_j7d_aspic_raw.txt'):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]), xe=float(c[6]))
al, f = 1e-3, 5.0
V = lambda y: 1 + al*math.log(math.sin(y/f)); dV = lambda y: al*math.cos(y/f)/math.sin(y/f)/f
yend = f*(math.pi/2 - A[(3, 50.0)]['xe']); y0 = 0.6
m = Model(V, dV, y0, Nmax=2000, end_y=yend); bg = Background(V, dV, y0, Nmax=2000, end_y=yend)
L = [f"field-value end y_end = {yend:.6e} (ASPIC x_end); start y0 = {y0}; N_tot Janus {m.Nend:.4f}, exact background {bg.Nend:.4f}"]
for N in (50.0, 60.0):
    t = time.time(); j = spectra3(m, N); tj = time.time() - t; b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = A[(3, N)]
    L.append(f"PSNI a=1e-3 f=5 N*={N:.0f} (exact ns {b['ns']:.6f} r {b['r']:.3e} a {b['alpha_s']:.3e}) | dns J {abs(j['ns']-b['ns']):.1e} A {abs(a['ns']-b['ns']):.1e} | dr/r J {abs(j['r']/b['r']-1):.1e} A {abs(a['r']/b['r']-1):.1e} | da J {abs(j['alpha_s']-b['alpha_s']):.1e} A {abs(a['a']-b['alpha_s']):.1e} | J {tj*1e3:.1f} ms")
open('field_tests/results/janus_j1d_psni.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
