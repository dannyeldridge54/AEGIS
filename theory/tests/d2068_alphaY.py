import math, random
b1, b2, rho, eps = 0.5, 1.0, 1/3, 1
def vol(st, chi): return math.prod(math.sqrt(n*n + (m*c)**2) for (n, m), c in zip(st, chi))
def stacks(na2, nd2):
    nc1 = (b2/(2*b1))*(na2 + 3*rho*nd2)
    a = [(1/b1, 0), (na2, eps*b2), (1/rho, 0.5)]; c = [(nc1, 3*rho*eps*b1), (1/b2, 0), (0, 1)]; d = [(1/b1, 0), (nd2, -b2*eps/rho), (1, 3*rho/2)]
    return a, c, d
rng = random.Random(11); hits = tot = 0; dys = []
for na2, nd2 in [(1, 1), (1, 2), (2, 1), (2, 2)]:
    for sgn in (1, -1):
        for _ in range(20000):
            chi = [math.exp(rng.uniform(math.log(0.2), math.log(5))) for _ in range(3)]
            a, c, d = stacks(na2, nd2); K = 27.94/vol(a, chi)
            iY = lambda c_, d_: (1/6)*27.94 + 0.5*K*vol(c_, chi) + 0.5*K*vol(d_, chi)
            a2, c2, d2 = stacks(na2, nd2 + sgn); dY = iY(c2, d2) - iY(c, d)
            al = 1/(1/0.1142 + 0.714*0.6*dY); z = (al - 0.1180)/0.0009; tot += 1; hits += abs(z) <= 2; dys.append(abs(dY))
dys.sort(); print('fraction |z|<=2: %.3f   median |d(1/alpha_Y)|: %.2f   (needed about -0.68 for z=0)' % (hits/tot, dys[len(dys)//2]))
