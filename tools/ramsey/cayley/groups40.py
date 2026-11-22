#!/usr/bin/env python3
"""All groups of order 40 (and Z35 / Z40 controls) as multiplication tables: G = Z5 x|phi P, |P| = 8, phi: P -> Aut(Z5) = {1,2,3,4} (mult. mod 5).
Writes one file per (P, phi): line 1 = n, then n lines of the n x n table. Isomorphic duplicates are allowed (PREREG_D2018)."""
import itertools, sys, os
def cyc(n): return list(range(n)), (lambda a, b: (a + b) % n)
def prod_group(*ns):
    els = list(itertools.product(*[range(n) for n in ns])); return els, (lambda a, b: tuple((x + y) % n for x, y, n in zip(a, b, ns)))
def d4():   # (r^i s^j): r^4 = s^2 = 1, s r = r^-1 s
    els = [(i, j) for j in range(2) for i in range(4)]
    def m(a, b): (i, j), (k, l) = a, b; return ((i + (k if j == 0 else -k)) % 4, (j + l) % 2)
    return els, m
def q8():   # quaternions as (sign, unit) with units 1,i,j,k
    t = {('1', x): (1, x) for x in '1ijk'}; t.update({(x, '1'): (1, x) for x in '1ijk'})
    t.update({('i', 'i'): (-1, '1'), ('j', 'j'): (-1, '1'), ('k', 'k'): (-1, '1'), ('i', 'j'): (1, 'k'), ('j', 'k'): (1, 'i'), ('k', 'i'): (1, 'j'),
              ('j', 'i'): (-1, 'k'), ('k', 'j'): (-1, 'i'), ('i', 'k'): (-1, 'j')})
    els = [(s, u) for s in (1, -1) for u in '1ijk']
    def m(a, b): s, u = t[(a[1], b[1])]; return (a[0] * b[0] * s, u)
    return els, m
PS = {'Z8': cyc(8), 'Z4xZ2': prod_group(4, 2), 'Z2^3': prod_group(2, 2, 2), 'D4': d4(), 'Q8': q8()}
def homs(els, m):   # maps P -> {1,2,3,4} (mult mod 5) that are homomorphisms
    idx = {e: i for i, e in enumerate(els)}; out = []
    for img in itertools.product((1, 2, 3, 4), repeat=len(els)):
        if all(img[idx[m(a, b)]] == img[idx[a]] * img[idx[b]] % 5 for a in els for b in els): out.append(img)
    return out
def semidirect(els, m, phi):   # (z, p)(z', p') = (z + phi(p) z', p p')
    idx = {e: i for i, e in enumerate(els)}; G = [(z, p) for z in range(5) for p in els]; gi = {g: i for i, g in enumerate(G)}
    def mul(a, b): return gi[((a[0] + phi[idx[a[1]]] * b[0]) % 5, m(a[1], b[1]))]
    return [[mul(a, b) for b in G] for a in G], gi[(0, els[[e for e in els if all(m(e, x) == x for x in els)][0] and 0 or 0])]
os.makedirs('tables', exist_ok=True); n_out = 0
for name, (els, m) in PS.items():
    e = [x for x in els if all(m(x, y) == y and m(y, x) == y for y in els)][0]; els = [e] + [x for x in els if x != e]   # identity first
    for k, phi in enumerate(homs(els, m)):
        tab, _ = semidirect(els, m, phi)
        assert all(tab[0][j] == j for j in range(40))                        # (0, e) is index 0 = identity
        for a in range(40):                                                   # group checks: closure, latin square
            assert sorted(tab[a]) == list(range(40))
        open('tables/%s_phi%d.txt' % (name.replace('^', ''), k), 'w').write('40\n' + '\n'.join(' '.join(map(str, r)) for r in tab)); n_out += 1
for n in (35, 40):
    open('tables/Z%d_control.txt' % n, 'w').write('%d\n' % n + '\n'.join(' '.join(str((a + b) % n) for b in range(n)) for a in range(n)))
print('group tables written:', n_out, '+ 2 controls')
