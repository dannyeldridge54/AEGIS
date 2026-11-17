"""D986 (locked PREREG_D986): positivity scan of the hatted anti-D5 Moebius trace."""
import mpmath as mp, numpy as np
def hat(t, dps):
    mp.mp.dps = dps; t = mp.mpf(t); nmax = int(mp.ceil(150/t)) + 50
    x = 1j*mp.e**(-t/2); q = -mp.e**(-t)
    D = A = B = RA = RD = mp.mpf(1)
    for n in range(1, nmax+1):
        D *= (1-x**(2*n))**8; A *= (1+x**(2*n-1))**8; B *= (1-x**(2*n-1))**8; RA *= (1+q**n)**8; RD *= (1-q**n)**8
    return ((A-B)/(2*x*D) + 8*RA/RD).real
L = []; vals = []; inconclusive = False
for t in np.geomspace(0.012, 60, 120):
    a, b = hat(t, 200), hat(t, 400); ok = abs(a/b - 1) < 1e-8 if b != 0 else a == b
    if not ok:
        c = hat(t, 800); ok = abs(b/c - 1) < 1e-8; b = c
        inconclusive |= not ok
    vals.append((float(t), b)); L.append(f"t={float(t):.5f}: H={mp.nstr(b, 12)} {'' if ok else 'PRECISION FAIL'}"); print(L[-1], flush=True)
pos = all(v > 0 for _, v in vals)
tmin, vmin = min(vals, key=lambda z: z[1])
sm = [(t, float(mp.log(v))) for t, v in vals if t < 0.02 and v > 0]
c = np.polyfit([1/t for t, _ in sm], [l for _, l in sm], 1)[0] if len(sm) > 2 else float('nan')
L.append(f"min H = {mp.nstr(vmin, 6)} at t = {tmin:.4f}; small-t growth c = {c:.4f} (pi^2/2 = {np.pi**2/2:.4f})")
L.append('INCONCLUSIVE' if inconclusive else ('POSITIVE: m_chi^2 > 0 for every T4 radius and T2 shape' if pos else 'SIGN CHANGE'))
open('field_tests/results/s3b_positivity_d986.txt', 'w').write('\n'.join(L)+'\n'); print(L[-2]); print(L[-1])
