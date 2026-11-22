#!/usr/bin/env python3
"""D2007 class maps (256-byte files). Non-letter classes fixed: digit, space, newline, punct, markup, other."""
import random, sys, os
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def base():
    m = [0] * 256
    for b in range(256):
        ch = chr(b)
        if ch.isdigit(): m[b] = 1
        elif ch == ' ': m[b] = 2
        elif ch == '\n': m[b] = 3
        elif ch in '[]{}<>|=': m[b] = 4
        elif 33 <= b < 127: m[b] = 5
        else: m[b] = 6
    return m
def write(name, groups):
    m = base(); cid = 7
    for g in groups:
        for L in g: m[ord(L)] = cid; m[ord(L.lower())] = cid
        cid += 1
    assert cid <= 32 and all(m[ord(c)] >= 7 for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    open(os.path.join(out, name + '.map'), 'wb').write(bytes(m))
PHOEN = ['A', 'B', 'CG', 'D', 'E', 'FUVWY', 'Z', 'H', 'IJ', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X']
write('PHOEN', PHOEN)
write('PHON', ['AEIOU', 'Y', 'BDGKPTCQ', 'FVSZHX', 'MN', 'LR', 'WJ'])
write('VC', ['AEIOUY', 'BCDFGHJKLMNPQRSTVWXZ'])
for seed in (1, 2, 3):
    r = random.Random(seed); L = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); r.shuffle(L)
    sizes = [len(g) for g in PHOEN]; r.shuffle(sizes); groups = []; i = 0
    for k in sizes: groups.append(''.join(L[i:i + k])); i += k
    write('RAND%d' % seed, groups)
print(sorted(os.listdir(out)))
