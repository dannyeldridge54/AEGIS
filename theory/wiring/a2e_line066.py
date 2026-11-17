import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
CONV = 0.389379e-27*2.99792458e10; M = 660.0; LIM = 4e-28*0.66**2; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
out = [f"assumed limit at 0.66 TeV: {LIM:.3e}"]
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv = 2*s[1]**2*math.pi*N.ALPHA**2/M**2*CONV*k
    for h, jr in (('HESS benchmark', 1.0), ('McMillan17', 0.499), ('MWPotential2014', 0.332)):
        fm = math.sqrt(LIM/(sv*jr))
        out.append(f"{lab} {h}: |s+-|^2={s[1]**2:.3f} sv_line={sv:.3e} f_max={fm:.3f} (one-loop {fm*math.sqrt(3):.2f}-{fm*2:.2f}) vs f=0.14 -> {'PASS' if fm >= 0.14 else 'FAIL'}")
open('field_tests/results/a2e_line066.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
