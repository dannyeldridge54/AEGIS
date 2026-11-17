import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld_nlo as N
k = 1 + N.ALPHA2*N.CW2/N.ALPHA; out = [f"sv_gZ/sv_gg = {2*N.ALPHA2*N.CW2/N.ALPHA:.3f}; line/gg = {k:.3f}; f_max factor {1/math.sqrt(k):.3f}"]
fm = {'HESS benchmark Einasto': (0.355, 0.391), 'McMillan17': (0.503, 0.554), 'MWPotential2014': (0.616, 0.679)}
for h, (lo, nl) in fm.items():
    for lab, f in (('LO', lo), ('NLO', nl)):
        g = f/math.sqrt(k)
        out.append(f"{h} {lab}: f_max(gg) {f:.3f} -> f_max(gg+gZ/2) {g:.3f}; one-loop {g*math.sqrt(3):.3f}-{g*2:.3f} -> tree-SE {'PASS' if g >= 0.26 else 'FAIL'}, one-loop {'PASS' if g*math.sqrt(3) >= 0.26 else 'FAIL'}")
open('field_tests/results/a2c_line_gz.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
