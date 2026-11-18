"""Disk cache for the (ω_b, ω_bc) → (z*, z_drag) recombination grid that L7/L10/L11/L12-type scripts rebuild every run (25 × ~6.7 s ≈ 3 min).
Values are computed by exactly the same calls (Cosmo(67.5, wb, wbc − wb, mnu=0.06); Recomb(c, wb, YHe=0.24)); the cache key is the SHA-256 of
background.py + recomb.py + the grid nodes, so any code change rebuilds it. Returns the same arrays bit-for-bit (checked by selftest_zgrid())."""
import hashlib, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CACHE = os.path.join(HERE, '..', '..', 'field_tests', 'cache')
def _key(wbs, wbcs):
    h = hashlib.sha256()
    for f in ('background.py', 'recomb.py'): h.update(open(os.path.join(HERE, f), 'rb').read())
    h.update(np.asarray(wbs, float).tobytes()); h.update(np.asarray(wbcs, float).tobytes()); return h.hexdigest()[:16]
def _compute(wbs, wbcs):
    from tools.janus_lt.background import Cosmo
    from tools.janus_lt.recomb import Recomb
    ZS = np.zeros((len(wbs), len(wbcs))); ZD = np.zeros_like(ZS)
    for i, wb in enumerate(wbs):
        for j, wbc in enumerate(wbcs):
            c = Cosmo(67.5, wb, wbc - wb, mnu=0.06); r = Recomb(c, wb, YHe=0.24); ZS[i, j] = r.z_star(); ZD[i, j] = r.z_drag()
    return ZS, ZD
def zgrid(wbs, wbcs):
    os.makedirs(CACHE, exist_ok=True); p = os.path.join(CACHE, f'zgrid_{_key(wbs, wbcs)}.npz')
    if os.path.exists(p): d = np.load(p); return d['ZS'], d['ZD']
    ZS, ZD = _compute(wbs, wbcs); np.savez(p, ZS=ZS, ZD=ZD); return ZS, ZD
def selftest_zgrid():
    wbs = np.array([0.0222, 0.0224]); wbcs = np.array([0.141, 0.143]); a = _compute(wbs, wbcs); b = zgrid(wbs, wbcs); c = zgrid(wbs, wbcs)
    return bool(np.array_equal(a[0], b[0]) and np.array_equal(a[1], c[1]))
if __name__ == '__main__':
    import sys; sys.path.insert(0, os.path.join(HERE, '..', '..')); print('zgrid cache bit-identical:', selftest_zgrid())
