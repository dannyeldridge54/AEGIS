"""R4 (locked PREREG_R4_racetrack_sign)."""
import math, mpmath as mp
mp.mp.dps = 40
out = []; signs = []
for N1, N2 in ((5, 6), (6, 7), (8, 9), (10, 11)):
    for A2 in (1, 2):
        a1, a2 = 8*mp.pi**2/N1, 8*mp.pi**2/N2; d = mp.mpf('1e-3')
        Om = lambda s: mp.exp(-a1*s) - A2*mp.exp(-a2*s)
        Oms = lambda s: -a1*mp.exp(-a1*s) + a2*A2*mp.exp(-a2*s)
        def sstar(L):
            f = lambda s: Oms(s) - Om(s)/(2*s - d*L)
            # scan for a sign change of F_S in s in (0.05, 20)
            grid = [mp.mpf(0.05) + i*mp.mpf(0.01) for i in range(2000)]
            for x0, x1 in zip(grid, grid[1:]):
                if f(x0)*f(x1) < 0: return mp.findroot(f, (x0, x1), solver='bisect' if False else 'anderson')
            return None
        L0 = mp.mpf(10); h = mp.mpf('1e-3')
        sp_, sm_, s0 = sstar(L0 + h), sstar(L0 - h), sstar(L0)
        if s0 is None:
            out.append(f"N=({N1},{N2}) A2={A2}: no F_S = 0 minimum in s in (0.05, 20)"); continue
        G = lambda s, L: Om(s)**2/(2*s - d*L)
        dlnG = (mp.log(G(sp_, L0 + h)) - mp.log(G(sm_, L0 - h)))/(2*h)
        Y0 = 2*s0 - d*L0; R = dlnG/(d/Y0); signs.append(R > 0)
        out.append(f"N=({N1},{N2}) A2={A2}: s* = {float(s0):.5f}, Y = {float(Y0):.5f}, a1*Y = {float(a1*Y0):.2f}, R = {float(R):.4f}")
    print(out[-1], flush=True)
verdict = 'TRUE' if signs and all(signs) else ('FALSE' if signs and not any(signs) else 'MIXED')
out.append(f"Claim 'R > 0 for the racetrack': {verdict} ({sum(signs)}/{len(signs)} positive)")
open('field_tests/results/r4_racetrack.txt', 'w').write('\n'.join(out)+'\n'); print('\n'.join(out))
