"""D672 (locked PREREG_D672_KAPPA_MODULAR). AI-assisted."""
import re, mpmath as mp
mp.mp.dps=30
pts=[]
for l in open('field_tests/results/janus_ext_d665.txt'):
    m=re.match(r"(tau=i|rho) eps=(\S+) N\*=(\S+): y\*=\S+ n_s=(\S+) r=(\S+) alpha=(\S+) beta=(\S+)",l)
    if m: pts.append((m.group(1),m.group(2),m.group(3),*map(mp.mpf,m.group(4,5,6))))
def alpha_pred(ns,r,n):
    p=n*mp.sqrt(2); k=1/n
    rho=p*mp.sqrt(r/2)/(1-ns); x=(rho-1)/(1+k*rho)
    return -(1-ns)**2/2*(1+x)*(1+k**2*x)/(1-k*x)**2
ok=True
for mdl,e,N,ns,r,al in pts:
    n=mp.findroot(lambda n: alpha_pred(ns,r,n)-al, 2)
    ok&= abs(n-2)<=0.2
    print(f"{mdl} eps={e} N*={N}: inferred plateau power n = {mp.nstr(n,4)}  (alpha at n=2: {mp.nstr(alpha_pred(ns,r,2),4)} vs exact {mp.nstr(al,4)})")
print("VERDICT:", "PASS" if ok else "FAIL")
