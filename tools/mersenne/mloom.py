#!/usr/bin/env python3
"""Mersenne Loom (PREREG_D2005). Layered sieve: N1 exponent prime -> N2 trial-factor layers -> N3 P-1 -> N4 PRP; referee = Lucas-Lehmer.
Hardware-adaptive: uses every logical core (multiprocessing). Usage: mloom.py calib [pmax]   |   mloom.py range lo hi"""
import sys, os, json, time, math, random
from multiprocessing import Pool
import gmpy2
from gmpy2 import mpz, is_prime, powmod, gcd

CHARTER = {
    'N1': 'exponent sieve: keep p only if p is prime (M_p composite otherwise)',
    'N2': 'trial-factor layers: q = 2kp+1, q = +-1 mod 8, one bit level per layer; a factor kills the candidate',
    'N3': 'P-1 stage 1 (B1=1e4): catches factors with smooth q-1',
    'N4': 'PRP base 3: the candidate detector',
    'REF': 'centre referee: independent Lucas-Lehmer on every N4 survivor + spot-check 5% of factors; disagreement = engine fault',
}

def tf_depth(p): return min(64, 16 + int(2 * math.log2(p)))

def trial_factor(p):
    """Return (bit_layer, q) of the first factor found, else None. Layers b: q in [2^b, 2^(b+1))."""
    M = (mpz(1) << p) - 1; top = tf_depth(p); two_p = 2 * p
    k = 1
    while True:
        q = two_p * k + 1
        if q.bit_length() > top: return None
        if q % 8 in (1, 7) and gmpy2.powmod(2, p, q) == 1: return (q.bit_length() - 1, int(q))
        k += 1

def pm1(p, B1=10000):
    M = (mpz(1) << p) - 1; a = powmod(3, 2 * p, M)
    for r in range(2, B1 + 1):
        if is_prime(r):
            e = r
            while e * r <= B1: e *= r
            a = powmod(a, e, M)
    g = gcd(a - 1, M)
    return int(g) if 1 < g < M else None

def prp3(p):
    M = (mpz(1) << p) - 1; return powmod(3, M - 1, M) == 1

def lucas_lehmer(p):
    if p == 2: return True
    M = (mpz(1) << p) - 1; s = mpz(4)
    for _ in range(p - 2): s = (s * s - 2) % M
    return s == 0

def process(p):
    t = {}; r = {'p': p}
    t0 = time.time(); f = trial_factor(p) if p > 2 else None; t['N2'] = time.time() - t0
    if f: r.update(node='N2', layer=f[0], factor=f[1]); r['t'] = t; return r
    t0 = time.time(); g = pm1(p) if p > 2 else None; t['N3'] = time.time() - t0
    if g: r.update(node='N3', factor=g); r['t'] = t; return r
    t0 = time.time(); prp = prp3(p) if p > 2 else True; t['N4'] = time.time() - t0
    t0 = time.time(); ll = lucas_lehmer(p); t['REF'] = time.time() - t0
    r.update(node='N4', prp=bool(prp), ll=bool(ll), agree=bool(prp) == bool(ll)); r['t'] = t; return r

def referee_factor(r):
    """Spot-check: the reported factor must divide M_p and be > 1 and < M_p."""
    M = (mpz(1) << r['p']) - 1; q = mpz(r['factor']); return 1 < q < M and M % q == 0

def run(lo, hi):
    ps = [p for p in range(max(2, lo), hi + 1) if is_prime(p)]          # N1
    cores = os.cpu_count() or 1; t0 = time.time()
    with Pool(cores) as pool: res = sorted(pool.map(process, ps, chunksize=4), key=lambda r: r['p'])
    random.seed(2005); facs = [r for r in res if r['node'] in ('N2', 'N3')]
    spot = random.sample(facs, max(1, len(facs) // 20)) if facs else []
    bad = [r['p'] for r in spot if not referee_factor(r)]
    found = [r['p'] for r in res if r['node'] == 'N4' and r['prp'] and r['ll']]
    faults = [r['p'] for r in res if r['node'] == 'N4' and not r['agree']]
    layers = {}
    for r in res:
        if r['node'] == 'N2': layers[r['layer']] = layers.get(r['layer'], 0) + 1
    # per-layer elimination rate: factors found in layer b / candidates that reached layer b (alive and depth >= b)
    rates = {}
    for b in sorted(layers):
        reached = sum(1 for r in res if r['p'] > 2 and tf_depth(r['p']) > b and not (r['node'] == 'N2' and r['layer'] < b))
        rates[b] = {'killed': layers[b], 'reached': reached, 'rate': layers[b] / reached if reached else None, 'heuristic_1_over_b': 1 / b}
    secs = {n: round(sum(r['t'].get(n, 0) for r in res), 2) for n in ('N2', 'N3', 'N4', 'REF')}
    return {'range': [lo, hi], 'cores': cores, 'n_prime_exponents': len(ps), 'removed_N2': sum(r['node'] == 'N2' for r in res),
            'removed_N3': sum(r['node'] == 'N3' for r in res), 'reached_N4': sum(r['node'] == 'N4' for r in res),
            'found': found, 'referee_faults': faults, 'factor_spotchecks': len(spot), 'bad_factors': bad, 'tf_layers': rates,
            'node_cpu_secs': secs, 'wall_secs': round(time.time() - t0, 1), 'charter': CHARTER}

KNOWN = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213]

if __name__ == '__main__':
    if sys.argv[1] == 'calib':
        pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12000; out = run(2, pmax)
        exp = [p for p in KNOWN if p <= pmax]
        out['calibration'] = {'expected': exp, 'sensitivity': len(set(out['found']) & set(exp)) / len(exp),
                              'false_positives': sorted(set(out['found']) - set(exp)),
                              'PASS': out['found'] == exp and not out['referee_faults'] and not out['bad_factors']}
        fn = os.path.join(os.path.dirname(__file__), '..', '..', 'field_tests', 'results', 'd2005_mersenne_loom.json')
    else:
        out = run(int(sys.argv[2]), int(sys.argv[3])); fn = 'mloom_%s_%s.json' % (sys.argv[2], sys.argv[3])
    json.dump(out, open(fn, 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k not in ('charter', 'tf_layers')}, indent=1))
    for b, v in out['tf_layers'].items(): print('layer', b, v)
