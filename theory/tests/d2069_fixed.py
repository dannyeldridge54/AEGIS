import math
chi = [1/math.sqrt(20.15)]*3; eps = 1
def vol(st): return math.prod(math.sqrt(n*n + (m*c)**2) for (n, m), c in zip(st, chi))
tot = hit = 0
for b1, b2, rho in [(0.5, 1.0, 1/3), (1.0, 1.0, 1.0), (0.5, 0.5, 1/3)]:
    def st(na2, nd2):
        nc1 = (b2/(2*b1))*(na2 + 3*rho*nd2)
        return [(1/b1, 0), (na2, eps*b2), (1/rho, 0.5)], [(nc1, 3*rho*eps*b1), (1/b2, 0), (0, 1)], [(1/b1, 0), (nd2, -b2*eps/rho), (1, 3*rho/2)], nc1
    for na2 in (1, 2):
        for nd2 in (1, 2):
            a, c, d, nc = st(na2, nd2); K = 27.94/vol(a); iY = lambda c_, d_: (1/6)*27.94 + 0.5*K*vol(c_) + 0.5*K*vol(d_)
            for s in (1, -1, 2, -2):
                a2, c2, d2, nc2 = st(na2, nd2 + s)
                if abs(nc2 - round(nc2)) > 1e-9 or abs(nc - round(nc)) > 1e-9: continue
                if abs(s) == 2 and abs(((b2/(2*b1))*3*rho) - round((b2/(2*b1))*3*rho)) < 1e-9: continue   # use +-1 when integral
                dY = iY(c2, d2) - iY(c, d); al = 1/(1/0.1142 + 0.714*0.6*dY); z = (al - 0.1180)/0.0009; tot += 1; hit += abs(z) <= 2
                print('b1 %.1f b2 %.1f rho %.2f na2 %d nd2 %d step %+d: d(1/aY) %+7.2f alpha_s %.4f z %+6.1f %s' % (b1, b2, rho, na2, nd2, s, dY, al, z, 'HIT' if abs(z) <= 2 else ''))
print('hits %d / %d' % (hit, tot))
