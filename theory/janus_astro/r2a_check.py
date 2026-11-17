import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld as S
M = 2000.0; w1 = w2 = w3 = 0.0; out = []
for a in (0.01, 0.0335):
    for v in (0.01, 0.1, 0.3):
        eta = a/v; att = 2*math.pi*eta/(1 - math.exp(-2*math.pi*eta)); rep = -2*math.pi*eta/(1 - math.exp(2*math.pi*eta))
        s1 = S.single_channel(M, v, lambda r: -a/r, a); s2 = S.single_channel(M, v, lambda r: a/r, -a)
        s3 = S.single_channel(M, v, lambda r: -a*math.exp(-1e-7*r)/r, a)
        e1, e2, e3 = abs(s1/att-1), abs(s2/rep-1), abs(s3/att-1); w1, w2, w3 = max(w1, e1), max(w2, e2), max(w3, e3)
        out.append(f"a={a} v={v}: att {s1:.6f}/{att:.6f} ({e1:.1e}) rep {s2:.6f}/{rep:.6f} ({e2:.1e}) yuk->coul {e3:.1e}")
ok = w1 <= 1e-4 and w2 <= 1e-4 and w3 <= 1e-3
out.append(f"worst T1 {w1:.1e} T2 {w2:.1e} T3 {w3:.1e} -> R2a {'VALIDATED' if ok else 'NOT VALIDATED'}")
open('field_tests/results/r2a_single.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
