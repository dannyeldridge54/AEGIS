import math, random
x = 21.10; bound = 1.2e-3*17.8; rng = random.Random(5)
for n in (2, 4, 6, 8, 9):
    s = [1]*(n//2) + [-1]*(n - n//2); L = []
    for _ in range(20000):
        xi = [x + rng.uniform(math.log(0.1), math.log(10)) for _ in range(n)]
        L.append(abs(sum(si/xx for si, xx in zip(s, xi)))/(1/x))
    L.sort(); frac = sum(l <= bound for l in L)/len(L)
    print('n=%d (%s) median leak_rel %.4f  frac(leak_rel <= %.4f) = %.3f' % (n, 'balanced' if sum(s) == 0 else 'unbalanced', L[len(L)//2], bound, frac))
