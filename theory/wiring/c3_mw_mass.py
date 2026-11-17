import sys; sys.path.insert(0, '.')
from galpy.potential import MWPotential2014, NFWPotential, vcirc
from astropy import constants as K, units as u
Gk = (K.G*u.Msun/u.kpc).to(u.km**2/u.s**2).value      # kpc (km/s)^2 / Msun
ro, vo = 8.0, 220.0; data = [(73, 4.3, 0.95, 'KG'), (52, 4.1, 1.2, 'BHB')]
h = MWPotential2014[2]; out = [f"G = {Gk:.6e} kpc (km/s)^2/Msun"]
for s in (0.8, 1.0, 1.2, 1.5):
    pot = [MWPotential2014[0], MWPotential2014[1], NFWPotential(amp=s*h._amp, a=h.a)]
    pulls = []
    for r, m, e, lab in data:
        vc = float(vcirc(pot, r/ro))*vo; M = r*vc*vc/Gk/1e11; pulls.append((M-m)/e)
        out.append(f"s={s} {lab} r={r}: v_c={vc:.1f} km/s M={M:.2f}e11 vs {m}+-{e} pull {(M-m)/e:+.2f}")
    w = max(abs(p) for p in pulls); out.append(f"s={s}: {'CONSISTENT' if w<=2 else ('TENSION' if w<=3 else 'EXCLUDED')}")
open('field_tests/results/c3_mw_mass.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
