"""D671 (locked PREREG_D671_BETA_GENERAL). AI-assisted."""
import mpmath as mp, sympy as sp
mp.mp.dps=40
# algebra check vs D666 (SERAPIS p=2sqrt2, kappa=1/2), u = 1/I*, s = u^2, 1-n_s = 2 p^2 s (1-kx)
x,u=sp.symbols('x u'); k=sp.Rational(1,2); p=2*sp.sqrt(2)
s=u**2; one_m_ns=2*p**2*s*(1-k*x)
gen=-sp.Rational(1,4)*one_m_ns**3*(1+x)*((1-k*x)*(1+k**2*x)+(1+x)*(1-k**3*x))/(1-k*x)**3
d666=128*u**6*(1+x)*(2*x**2-5*x-16)
print("algebra check (general - D666):",sp.simplify(gen-d666))
def model(al,gm,be,de):
    m=1/mp.sqrt(6*al)
    return lambda f: mp.tanh(m*f)**(2*gm)*(1+de*mp.cosh(m*f)**(2*be))
def obs(V,N):
    d=lambda f,n: mp.diff(V,f,n)
    eps=lambda f:(d(f,1)/V(f))**2/2
    fe=mp.findroot(lambda f:eps(f)-1,1.0)
    fs=mp.findroot(lambda f: mp.quad(lambda w:V(w)/d(w,1),[fe,f])-N, fe+5)
    Vv=V(fs); e=eps(fs); h=d(fs,2)/Vv; x2=d(fs,1)*d(fs,3)/Vv**2; v3=d(fs,1)**2*d(fs,4)/Vv**3
    ns=1-6*e+2*h; r=16*e
    b=-192*e**3+192*e**2*h-32*e*h**2-24*e*x2+2*h*x2+2*v3
    return ns,r,b
def predict(ns,r,p,k):
    rho=p*mp.sqrt(r/2)/(1-ns); x=(rho-1)/(1+k*rho)
    return -(1-ns)**3/4*(1+x)*((1-k*x)*(1+k**2*x)+(1+x)*(1-k**3*x))/(1-k*x)**3
worst=0
for be in (1,mp.mpf(1)/2):
    al=mp.mpf(1)/3; p=mp.sqrt(2/(3*al)); k=be
    for de in (3e-6,1e-5,3e-5):
        V=model(al,1,be,de)
        for N in (50,55):
            try: ns,r,b=obs(V,N)
            except Exception as ex: print(f"beta={be} delta={de} N={N}: not converged"); continue
            bp=predict(ns,r,p,k); err=100*(bp/b-1); worst=max(worst,abs(err))
            print(f"beta={mp.nstr(be,2)} delta={de:.0e} N={N}: n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} beta_s={mp.nstr(b,4)} pred={mp.nstr(bp,4)} err={mp.nstr(err,3)}% | -4/N^3={mp.nstr(-4/mp.mpf(N)**3,3)}",flush=True)
print(f"max |err| = {mp.nstr(worst,3)}%  VERDICT: {'PASS' if worst<=15 else 'FAIL'}")
