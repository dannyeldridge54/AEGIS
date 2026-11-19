import json, math, sys
P = math.sqrt(8)
def d635(y, x): return 16/y**2*(1-x/2), 64/y**4*(1+x)**2, -128/y**4*(1+x/4)*(1+x)
def d1405(ns1, r, k=0.5):
    q = P*math.sqrt(r/2)/ns1; return -0.5*ns1**2*q*(1+k*(q-1))
def d640(u, x, c):
    return 8*u*u*((2-x)+c*u*(5-x)), 64*u**4*(1+x)**2*(1+2*c*u), -32*u**4*(1+x)*((4+x)+c*u*(23+2*x))
m1 = m2 = 0
for i in range(41):
    for j in range(41):
        y, x = 10+20*i/40, j/40
        a, b, al = d635(y, x)
        m1 = max(m1, abs(d1405(a, b)/al-1))
        e = d640(1/y, x, 1e-12); m2 = max(m2, max(abs(e[0]/a-1), abs(e[1]/b-1), abs(e[2]/al-1)))
out = dict(max_rel_D1405_vs_D635=m1, max_rel_D640c0_vs_D635=m2, verdict='PASS' if m1 < 1e-10 and m2 < 1e-10 else 'FAIL')
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
