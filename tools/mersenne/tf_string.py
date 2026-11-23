"""D2175: prime-node gap string. Nodes = primes r; each keeps allowed residues of k (q=2kp+1 allowed mod r);
CRT-nested -> sorted survivor residues mod M -> gap string, walked ascending in k (early exit kept)."""
import sys, time, json
import gmpy2
from sympy import primerange
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from tf_wheel import naive_tf
def node(p, r):
    if r == 8: return [k for k in range(4) if (2*p*k + 1) % 8 in (1, 7)], 4      # q mod 8 depends on k mod 4
    return [k for k in range(r) if (2*p*k + 1) % r], r
def string(p, rs):
    res, M = [0], 1
    for r in rs:                       # CRT nesting: the fractal tree, one prime node per level
        keep, m = node(p, r); new = []
        for a in res:
            for t in range(m):
                k = a + M*t
                if k % m in keep: new.append(k)
        res, M = sorted(new), M*m
    gaps = [b - a for a, b in zip(res, res[1:])] + [res[0] + M - res[-1]]
    return res[0], gaps, M, len(res)
def string_tf(p, bits, rs):
    k, gaps, M, n = string(p, rs); top = 1 << bits; two_p = 2*p; i = 0; L = len(gaps)
    if k == 0: k += gaps[0]; i = 1
    while True:
        q = two_p*k + 1
        if q >= top: return None
        if gmpy2.powmod(2, p, q) == 1: return q
        k += gaps[i]; i += 1
        if i == L: i = 0
if __name__ == '__main__':
    bits = 40; ps = [int(x) for x in primerange(10**6, 10**6 + 20000)][:200]
    R1 = [8, 3, 5, 7, 11]; R2 = R1 + [13]   # DEV-1
    out = {}
    t = time.time(); N = [naive_tf(p, bits) for p in ps]; out['t_naive'] = time.time() - t
    for name, rs in (('R1', R1), ('R2', R2)):
        t = time.time(); S = [string_tf(p, bits, rs) for p in ps]; dt = time.time() - t
        _, g, M, n = string(ps[0], rs)
        out[name] = dict(t=dt, speedup=out['t_naive']/dt, mismatches=sum(a != b for a, b in zip(N, S)), period=M, kept=n, frac_kept=n/M)
    out['C1'] = 'PASS' if out['R1']['mismatches'] == 0 and out['R2']['mismatches'] == 0 else 'FAIL'
    out['C2'] = 'PASS' if out['R1']['speedup'] >= 2.5 else 'FAIL'
    json.dump(out, open('/home/claude/aegis/field_tests/results/d2175_prime_node_string.json', 'w'), indent=1); print(json.dumps(out, indent=1))
