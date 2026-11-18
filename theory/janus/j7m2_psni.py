"""J7m2 (locked PREREG_J7m2_psni)."""
import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.anyV import start_bisect
from tools.janus_calc.core import spectra3
from tools.serapis_calc.ms import Background, spectra_fast
DL = tuple(np.linspace(-1, 1, 9)); A = {}
for l in open('theory/janus/aspic/aspic_j7m_clean.txt'):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
L = []; nb = 0; tot = 0
for i, (al, f) in ((7, (1e-4, 5.0)), (8, (1e-2, 5.0)), (9, (1e-3, 10.0))):
    top = f*math.pi/2; V = lambda y, al=al, f=f: 1 + al*math.log(math.sin(y/f)); dV = lambda y, al=al, f=f: al*math.cos(y/f)/math.sin(y/f)/f
    y60 = f*(math.pi/2 - A[(i, 60.0)]['x'])
    try:
        m = start_bisect(V, dV, y60, top*(1 - 1e-12), Nwant=80.0); y0 = m.sol.y[0][0]; bg = Background(V, dV, y0, Nmax=20000)
        L.append(f"PSNI a={al} f={f}: J1b start y0 = {y0:.10f} (top {top:.10f}), N_tot = {m.Nend:.3f}")
        for N in (50.0, 60.0):
            j = spectra3(m, N); b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = A[(i, N)]
            dj, da = abs(j['ns'] - b['ns']), abs(a['ns'] - b['ns']); nb += dj < da; tot += 1
            L.append(f"  N*={N:.0f} (exact ns {b['ns']:.6f} r {b['r']:.3e} a {b['alpha_s']:.3e}) | dns J {dj:.1e} A {da:.1e} | dr/r J {abs(j['r']/b['r']-1):.1e} A {abs(a['r']/b['r']-1):.1e} | da J {abs(j['alpha_s']-b['alpha_s']):.1e} A {abs(a['a']-b['alpha_s']):.1e}")
    except Exception as e:
        L.append(f"PSNI a={al} f={f}: J1b bisection failed: {e} — reported, stop for this point")
    print('\n'.join(L[-3:]), flush=True)
L.append(f"J7m2: Janus n_s better on {nb}/{tot} scored PSNI comparisons")
open('field_tests/results/janus_j7m2_psni.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
