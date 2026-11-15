"""D669 (locked PREREG_D669_JANUS_GENERAL). AI-assisted. Exact first-order slow roll with mpmath."""
import mpmath as mp
mp.mp.dps=40
def model(al,gm,be,de):
    m=1/mp.sqrt(6*al)
    return lambda f: mp.tanh(m*f)**(2*gm)*(1+de*mp.cosh(m*f)**(2*be))
def obs(V,N):
    d=lambda f,n: mp.diff(V,f,n)
    eps=lambda f:(d(f,1)/V(f))**2/2
    fe=mp.findroot(lambda f:eps(f)-1,1.0)
    fs=mp.findroot(lambda f: mp.quad(lambda u:V(u)/d(u,1),[fe,f])-N, fe+5)
    e=eps(fs); h=d(fs,2)/V(fs); x2=d(fs,1)*d(fs,3)/V(fs)**2
    return 1-6*e+2*h, 16*e, 16*e*h-24*e**2-2*x2
def predict(ns,r,p,k):
    rho=p*mp.sqrt(r/2)/(1-ns); x=(rho-1)/(1+k*rho)
    return -(1-ns)**2/2*(1+x)*(1+k**2*x)/(1-k*x)**2, x
worst=0
for be in (1,mp.mpf(1)/2):
    al=mp.mpf(1)/3; p=mp.sqrt(2/(3*al)); k=be
    for de in (3e-6,1e-5,3e-5):
        V=model(al,1,be,de)
        for N in (50,55):
            try:
                ns,r,a=obs(V,N)
            except Exception as ex:
                print(f"beta={be} delta={de} N={N}: failed ({ex})"); continue
            ap,x=predict(ns,r,p,k); err=100*(ap/a-1); worst=max(worst,abs(err))
            print(f"beta={mp.nstr(be,2)} delta={de:.0e} N={N}: n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha={mp.nstr(a,4)} | x={mp.nstr(x,3)} pred={mp.nstr(ap,4)} err={mp.nstr(err,3)}% | attractor {mp.nstr(-(1-ns)**2/2,4)}",flush=True)
print(f"max |err| = {mp.nstr(worst,3)}%  VERDICT: {'PASS' if worst<=15 else 'FAIL'}")
