import sys; sys.path.insert(0, '.')
from galpy.potential import MWPotential2014, NFWPotential, mass
h = MWPotential2014[2]; out = []
db = sum(float(mass(p, 100/8., ro=8, vo=220)) for p in MWPotential2014[:2])
out.append(f"disk+bulge mass within 100 kpc: {db:.3e} Msun")
data = [('KG', 0.55, 0.15, 0.11), ('BHB', 1.00, 0.67, 0.33)]
for s in (0.8, 1.0, 1.2, 1.5):
    p = NFWPotential(amp=s*h._amp, a=h.a, ro=8, vo=220); M = float(p.mvir(H=67.66, overdens=200., wrtcrit=True))/1e12
    pulls = [(M-m)/(up if M > m else lo) for _, m, up, lo in data]; w = max(abs(x) for x in pulls)
    out.append(f"s={s}: M200={M:.3f}e12 pulls KG {pulls[0]:+.2f} BHB {pulls[1]:+.2f} -> {'CONSISTENT' if w<=2 else ('TENSION' if w<=3 else 'EXCLUDED')}")
open('field_tests/results/c4_m200.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
