#!/usr/bin/env python3
"""Ancient-number lens (Danny 08:34): factor the traditional cycle numbers, compare with the modular structure, and apply the
'2s-and-3s only' rule to the KL racetrack ranks. Analogy/numerology lens; no evidence credit."""
import math
def fac(n):
    out = {}; m = n
    for p in (2, 3, 5, 7, 11, 13):
        while m % p == 0: out[p] = out.get(p, 0) + 1; m //= p
    return out, m
CAT = [('Kali yuga (yrs)', 432000), ('Dvapara', 864000), ('Treta', 1296000), ('Satya/Krita', 1728000), ('Mahayuga', 4320000),
       ('Kalpa (day of Brahma)', 4320000000), ('mala beads', 108), ('nakshatras', 27), ('Berossus pre-flood reign (yrs)', 432000),
       ('Valhalla 540 doors x 800', 540*800), ('Plato nuptial number', 12960000), ('degrees of circle (Babylon)', 360), ('Maya 13 baktun (days)', 1872000)]
print('%-32s %14s  factorisation (primes 2,3,5; rest)' % ('number', 'value'))
for name, v in CAT:
    f, rest = fac(v); print('%-32s %14d  %s%s' % (name, v, ' * '.join('%d^%d' % (p, k) for p, k in sorted(f.items())), '' if rest == 1 else ' * %d' % rest))
print('\nmodular structure: PSL(2,Z) = Z2 * Z3 (free product of the stabilisers of i and rho); j(i) = 1728 = 12^3 = 2^6 3^3; j(rho) = 0')
print('Yuga ratio Satya:Treta:Dvapara:Kali = 4:3:2:1 ; Satya = 1728 x 1000')
smooth = lambda n: fac(n)[1] == 1 and all(p in (2, 3) for p in fac(n)[0])
pairs = [(n, n + 1) for n in range(1, 10000) if smooth(n) and smooth(n + 1)]
print('\nconsecutive 3-smooth pairs (Stormer: finite):', pairs)
s0 = 20.15
for N, Np in [(N, N+1) for N in range(5, 17)]:
    a, b = 2*math.pi/N, 2*math.pi/Np; ba = (Np/N)*math.exp(-(a - b)*s0)
    if 0.1 <= ba <= 10: print('  natural racetrack (%d,%d) B/A %.3f  3-smooth pair: %s' % (N, Np, ba, (N, Np) in pairs))
