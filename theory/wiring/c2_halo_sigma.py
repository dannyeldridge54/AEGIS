import sys, copy; sys.path.insert(0, '.')
from galpy.potential import MWPotential2014, NFWPotential
from galpy.df import jeans
ro, vo = 8.0, 220.0; data = {20: 120, 50: 102, 80: 84, 120: 50}
nu = lambda r: r**-3.5
h = MWPotential2014[2]; heavy = [MWPotential2014[0], MWPotential2014[1], NFWPotential(amp=1.5*h._amp, a=h.a)]
out = []
for lab, pot in [('MWPotential2014', MWPotential2014), ('halo x1.5', heavy)]:
    for b in (0.0, 0.5, 0.8):
        s = {r: float(jeans.sigmar(pot, r/ro, dens=nu, beta=b))*vo for r in data}
        ok = all(abs(s[r]-data[r]) <= 20 for r in (20, 50, 80)) and abs(s[120]-50) <= 44
        out.append(f"{lab} beta={b}: " + " ".join(f"{r}kpc {s[r]:.1f}(d {s[r]-data[r]:+.1f})" for r in data) + f" -> {'CONSISTENT' if ok else 'NOT CONSISTENT'}")
open('field_tests/results/c2_halo_sigma.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
