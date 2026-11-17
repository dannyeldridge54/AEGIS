import sys, math; sys.path.insert(0, '.')
from galpy.potential import MWPotential2014, NFWPotential, evaluatePotentials
ro, vo = 8.0, 220.0; h = MWPotential2014[2]; out = []
for s in (0.8, 1.0, 1.1, 1.2):
    halo = NFWPotential(amp=s*h._amp, a=h.a); pot = [MWPotential2014[0], MWPotential2014[1], halo]
    rv = float(NFWPotential(amp=s*h._amp, a=h.a, ro=ro, vo=vo).rvir(H=67.66, overdens=200., wrtcrit=True))  # kpc
    P0 = evaluatePotentials(pot, 8.3/ro, 0.0); Pm = evaluatePotentials(pot, 2*rv/ro, 0.0)
    v1 = math.sqrt(2*(Pm - P0))*vo; v2 = math.sqrt(2*(evaluatePotentials(pot, 1e5, 0.0) - P0))*vo
    lab = lambda v: (v-528)/(24 if v > 528 else 25)
    out.append(f"s={s}: r200={rv:.0f} kpc; v_esc(to 2r200)={v1:.0f} km/s pull {lab(v1):+.2f} {'CONSISTENT' if abs(lab(v1))<=2 else 'NOT'}; v_esc(inf)={v2:.0f} pull {lab(v2):+.2f} {'CONSISTENT' if abs(lab(v2))<=2 else 'NOT'}")
open('field_tests/results/c6_vesc.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
