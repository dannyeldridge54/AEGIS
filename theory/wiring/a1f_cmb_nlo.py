import sys, math, numpy as np; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
CONV = 0.389379e-27*2.99792458e10; PANN = 3.2e-28; R2 = math.sqrt(2)
def sv(M, nlo):
    s = N.wino_s_nlo(M, v=1e-7, nlo=nlo, off_factor=R2)
    return math.pi*N.ALPHA2**2/(2*M*M)*(2*(2*s[0]**2 + 2*R2*s[0]*s[1] + 3*s[1]**2))*CONV
out = []
Ms = np.round(np.arange(2.00, 3.001, 0.02), 3)
for lab, nlo in (('LO', False), ('NLO(sqrt2, post hoc)', True)):
    rows = [(M, sv(M*1e3, nlo)) for M in Ms]
    for fe in (0.14, 0.41):
        ex = [M for M, s in rows if fe*s/(M*1e3) > PANN]
        out.append(f"{lab} f_eff={fe}: excluded {('%.2f-%.2f TeV' % (min(ex), max(ex))) if ex else 'none'} ({len(ex)} pts)")
    for Mt in (2.842, 2.85, 2.86, 2.87):
        s = sv(Mt*1e3, nlo); out.append(f"   {lab} M={Mt}: sv={s:.3e} cm3/s; f_max(f_eff 0.41)={math.sqrt(PANN/(0.41*s/(Mt*1e3))):.3f}, (0.14)={math.sqrt(PANN/(0.14*s/(Mt*1e3))):.3f}")
open('field_tests/results/a1f_cmb_nlo.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
