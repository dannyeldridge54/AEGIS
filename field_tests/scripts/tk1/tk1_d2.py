import sys, math, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import build
from tools.serapis_calc.ms import Background, spectra
from tools.janus_calc.core import Model, spectra3
m, V, dV, p0 = build('serapis_e', 1.0e-6); bg = Background(V, dV, p0, Nmax=4000); M = Model(V, dV, p0, Nmax=4000)
print('Janus3', spectra3(M, 50.7), flush=True)
for dl in ((-0.1, -0.05, 0.0, 0.05, 0.1), (-0.05, -0.025, 0.0, 0.025, 0.05)):
    t = time.time(); s = spectra(bg, 50.7, dlnk=dl); print(dl, f"n_s {s['ns']:.6f} r {s['r']:.5e} α_s {s['alpha_s']:.4e} ({time.time()-t:.0f}s)", flush=True)
