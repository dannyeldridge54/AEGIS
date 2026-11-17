import sys; sys.path.insert(0, '.')
from tools.janus_astro import relic as R, sommerfeld_nlo as N
out = []
for lab, a2 in (('on-shell', N.ALPHA2), ('MSbar(mZ)', 0.00780372/0.232486)):
    m = R.thermal_mass(a2); k = R.sigma_eff_born(m, a2)[1]
    out.append(f"{lab} alpha2={a2:.5f}: sigma_eff = {k:.4f} pi a2^2/m^2; thermal Born mass {m/1e3:.4f} TeV vs 2.207 (rel {m/2207-1:+.3f})")
T1 = abs(R.thermal_mass(N.ALPHA2)/2207 - 1) <= 0.06
out.append("R1 " + ("VALIDATED" if T1 else "NOT VALIDATED"))
open('field_tests/results/r1_relic.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
