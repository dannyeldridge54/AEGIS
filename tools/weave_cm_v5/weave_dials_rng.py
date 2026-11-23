#!/usr/bin/env python3
"""weave_dials_rng v0 (22 Nov 2026) — RESEARCH ONLY, NOT SECURE, NEVER USE FOR REAL KEYS.
Danny's idea: use the Loom engine's dials (the thread potential A = 7.30, beta = 2 sqrt 2, the two knots rho and i, the
slip ladder 0.0251/(m + 1/16)) as a randomizer. This file turns that into a testable stream generator so CubeMind can
measure how random it really is. The bar is the public standard: NIST SP 800-22 / PractRand / dieharder. Passing simple
statistics is NOT security: a cipher is only trusted after years of public cryptanalysis. So weave_vault.py uses AES-GCM,
and this generator stays a research object until it survives the full batteries (and even then only as a non-crypto PRNG).
Usage: python weave_dials_rng.py <seed-int> [n_bytes]   -> runs the quick battery below on its own output."""
import sys, math, lzma, hashlib
A = 16*1.6449340668482264/(3*1.2020569031595942); BETA = 2*math.sqrt(2)
RHO = complex(0.5, math.sqrt(3)/2); I = 1j
def stream(seed, n):
    # dials: a point tau on the upper half plane walks between the knots; each step mixes the slip ladder and the thread curve
    t = complex((seed % 997)/997.0 - 0.5, 0.8 + (seed % 991)/991.0); out = bytearray(); m = 1 + seed % 32
    while len(out) < n:
        eps = 0.0251/(m + 1/16)
        phi = abs(t - RHO)*BETA; v = 1 - A*math.exp(-phi)              # thread curve
        t = complex((t.real*7.30 + v + eps*t.imag) % 1.0 - 0.5, 0.55 + abs(math.sin(1e3*(t.imag + v)))*1.5)
        m = 1 + (m*29 + int(abs(t - I)*1e6)) % 32
        out += bytes([int((t.real + 0.5)*2**32) & 255])
    return bytes(out[:n])
def battery(b):
    n = len(b)*8; ones = sum(bin(x).count('1') for x in b)
    mono_z = (ones - n/2)/math.sqrt(n/4)
    cnt = [0]*256
    for x in b: cnt[x] += 1
    e = len(b)/256; chi = sum((c - e)**2/e for c in cnt)                 # df 255: expect ~255 +- 23
    bits = ''.join(format(x, '08b') for x in b[:20000]); runs = 1 + sum(bits[i] != bits[i-1] for i in range(1, len(bits)))
    nb = len(bits); pi = bits.count('1')/nb; runs_z = (runs - 2*nb*pi*(1 - pi))/(2*math.sqrt(2*nb)*pi*(1 - pi))
    comp = len(lzma.compress(b))/len(b)                                    # a random stream does not compress (ratio ~1.00+)
    ok = abs(mono_z) < 3 and abs(chi - 255) < 3*22.6 and abs(runs_z) < 3 and comp > 0.999
    return dict(monobit_z=round(mono_z, 2), byte_chi2=round(chi, 1), runs_z=round(runs_z, 2), lzma_ratio=round(comp, 4),
                quick_battery='PASS (necessary, not sufficient)' if ok else 'FAIL', secure='NO - research object')
if __name__ == '__main__':
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 1; n = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    print(battery(stream(s, n)))
