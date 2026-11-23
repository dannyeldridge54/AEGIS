"""D2174: trial factoring of 2^p-1 with the mfaktc-style 4620-class wheel + small-prime sieve (numpy), vs the D2005 naive loop."""
import sys, time, json, math
import numpy as np, gmpy2
from sympy import primerange
SMALL = [int(x) for x in primerange(13, 2**13)]
def naive_tf(p, bits):
    two_p = 2*p; k = 1
    while True:
        q = two_p*k + 1
        if q.bit_length() > bits: return None
        if q % 8 in (1, 7) and gmpy2.powmod(2, p, q) == 1: return q
        k += 1
def classes(p):
    out = []
    for c in range(4620):
        q = 2*p*c + 1
        if q % 8 in (1, 7) and q % 3 and q % 5 and q % 7 and q % 11: out.append(c)
    return out
def wheel_tf(p, bits, chunk=1 << 16):
    kmax = ((1 << bits) - 1) // (2*p)          # q <= 2^bits - 1  (same bound as naive: bit_length <= bits)
    best = None
    for c in classes(p):
        # k = c + 4620*j, j = 0..J
        if c == 0: j0 = 1
        else: j0 = 0
        J = (kmax - c) // 4620
        for s in range(j0, J + 1, chunk):
            e = min(J + 1, s + chunk); n = e - s
            alive = np.ones(n, dtype=bool)
            for r in SMALL:
                # q = 2p(c+4620 j)+1 ≡ 0 mod r  ->  j ≡ -(2pc+1) * inv(2p*4620) mod r
                a = (2*p*4620) % r
                if a == 0: continue
                j_hit = (-(2*p*c + 1) * pow(a, -1, r)) % r
                st = (j_hit - s) % r
                alive[st::r] = False   # (q==r itself can't happen for q > 2^13 here)
            for jj in np.nonzero(alive)[0]:
                k = c + 4620*(s + int(jj)); q = 2*p*k + 1
                if best is not None and q >= best: break
                if gmpy2.powmod(2, p, q) == 1:
                    best = q if best is None else min(best, q); break
    return best
if __name__ == '__main__':
    bits = 40; ps = [int(x) for x in primerange(10**6, 10**6 + 20000)][:200]
    t = time.time(); W = [wheel_tf(p, bits) for p in ps]; tw = time.time() - t
    t = time.time(); N = [naive_tf(p, bits) for p in ps]; tn = time.time() - t
    mism = [(p, a, b) for p, a, b in zip(ps, N, W) if a != b]
    cand_naive = sum(((1 << bits) - 1)//(2*p) for p in ps)
    res = dict(n=len(ps), bits=bits, factors_found=sum(x is not None for x in N), mismatches=mism[:10], C1='PASS' if not mism else 'FAIL',
               t_naive=tn, t_wheel=tw, speedup=tn/tw, naive_k_per_s=cand_naive/tn, wheel_k_covered_per_s=cand_naive/tw)
    json.dump(res, open('/home/claude/aegis/field_tests/results/d2174_mersenne_wheel.json', 'w'), indent=1); print(json.dumps(res, indent=1))
