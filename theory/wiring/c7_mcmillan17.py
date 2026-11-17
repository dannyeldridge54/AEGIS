import sys, math; sys.path.insert(0, '.')
from galpy.potential.mwpotentials import McMillan17 as P
from galpy.potential import vcirc, evaluatePotentials
from galpy.df import jeans
from astropy import constants as K, units as u
Gk = (K.G*u.Msun/u.kpc).to(u.km**2/u.s**2).value
ro, vo = 8.21, 233.1; out = []
for r, m, e, lab in [(73, 4.3, 0.95, 'KG'), (52, 4.1, 1.2, 'BHB')]:
    vc = float(vcirc(P, r/ro)); M = r*vc*vc/Gk/1e11; p = (M-m)/e
    out.append(f"C3 {lab} r={r}: v_c={vc:.1f} M={M:.2f}e11 pull {p:+.2f} {'CONSISTENT' if abs(p)<=2 else ('TENSION' if abs(p)<=3 else 'EXCLUDED')}")
h = P[1]; M200 = float(h.mvir(H=67.66, overdens=200., wrtcrit=True, ro=ro, vo=vo))/1e12
r200 = float(h.rvir(H=67.66, overdens=200., wrtcrit=True, ro=ro, vo=vo))
for lab, m, up, lo in [('KG', 0.55, 0.15, 0.11), ('BHB', 1.00, 0.67, 0.33)]:
    p = (M200-m)/(up if M200 > m else lo)
    out.append(f"C4 {lab}: halo M200={M200:.3f}e12 (r200 {r200:.0f} kpc) pull {p:+.2f} {'CONSISTENT' if abs(p)<=2 else ('TENSION' if abs(p)<=3 else 'EXCLUDED')}")
P0 = evaluatePotentials(P, 8.3/ro, 0.0); Pm = evaluatePotentials(P, 2*r200/ro, 0.0)
ve = math.sqrt(2*(Pm-P0)); p = (ve-528)/(24 if ve > 528 else 25)
out.append(f"C6 v_esc(8.3, to 2r200) = {ve:.0f} km/s pull {p:+.2f} {'CONSISTENT' if abs(p)<=2 else ('TENSION' if abs(p)<=3 else 'EXCLUDED')}; v_c(8.21)={float(vcirc(P,1.0)):.1f}")
data = {20: 120, 50: 102, 80: 84, 120: 50}
for b in (0.0, 0.5, 0.8):
    s = {r: float(jeans.sigmar(P, r/ro, dens=lambda x: x**-3.5, beta=b)) for r in data}
    ok = all(abs(s[r]-data[r]) <= 20 for r in (20, 50, 80)) and abs(s[120]-50) <= 44
    out.append(f"C2 beta={b}: " + " ".join(f"{r}:{s[r]:.0f}({s[r]-data[r]:+.0f})" for r in data) + f" -> {'CONSISTENT' if ok else 'NOT'}")
open('field_tests/results/c7_mcmillan17.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
