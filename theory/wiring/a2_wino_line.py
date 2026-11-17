import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
CONV = 0.389379e-27*2.99792458e10; M = 1000.0; LIM = 4e-28
out = []
for lab, nlo in (('LO', False), ('NLO(sqrt2, post hoc)', True)):
    s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2))
    sv = 2*s[1]**2*math.pi*N.ALPHA**2/M**2*CONV; fm = math.sqrt(LIM/sv)
    out.append(f"{lab}: |s+-|^2={s[1]**2:.3f} sv_gg={sv:.3e} cm3/s f_max={fm:.3f} (one-loop x1/3-1/4: {fm*math.sqrt(3):.3f}-{fm*2:.3f}); SERAPIS-E f=0.26 -> {'PASS' if fm >= 0.26 else 'FAIL'} at tree-SE")
open('field_tests/results/a2_wino_line.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
