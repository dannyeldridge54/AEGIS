import warnings; warnings.filterwarnings('ignore')
from galpy.potential import MWPotential2014, vcirc, epifreq
from galpy.potential.mwpotentials import McMillan17
def pull(x, m, up, dn): r = x - m; return r/(up if r > 0 else dn)
out = []
for name, pot, phys in (('MWPotential2014', MWPotential2014, False), ('McMillan17', McMillan17, True)):
    for R in (8.178, 8.256):
        if phys:
            ro = 8.21; v = float(vcirc(pot, R/ro)); k = float(epifreq(pot, R/ro))   # physical outputs: km/s, km/s/kpc
        else:
            ro, vo = 8.0, 220.0; v = float(vcirc(pot, R/ro))*vo; k = float(epifreq(pot, R/ro))*vo/ro
        O = v/R; pv = pull(v, 235.3, 2.8, 3.7); pO = pull(O, 28.5, 0.4, 0.1); pk = pull(k, 36.9, 0.8, 1.0)
        tag = 'PASS' if abs(pv) <= 2 and abs(pO) <= 2 else 'FAIL'
        out.append(f"{name} R={R}: v_c={v:.1f} (pull {pv:+.2f}) Omega={O:.2f} (pull {pO:+.2f}) kappa={k:.2f} (pull {pk:+.2f})" + (f" -> {tag}" if R == 8.178 else " [reported]"))
open('field_tests/results/c8_horta.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
