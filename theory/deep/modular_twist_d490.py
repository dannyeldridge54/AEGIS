import math
from scipy.optimize import brentq
m2=4/math.pi; k=math.sqrt(1.5)   # phi = k ln x
def lnG(x,n,e): return math.log(x+e)-0.5*math.log(1+x)-n*(1-math.exp(-x/m2))
def lnF(x,n,e,sym):
    a=lnG(x,n,e)
    if not sym: return a
    b=3*math.log(x)+lnG(1/x,n,e); M=max(a,b); return M+math.log(math.exp(a-M)+math.exp(b-M))
def lnV(u,n,e,sym): x=math.exp(u); return 2*lnF(x,n,e,sym)-3*math.log(2*x)
def d1(u,*p,h=1e-5): return (lnV(u+h,*p)-lnV(u-h,*p))/(2*h)/k          # (V'/V) in phi
def d2(u,*p,h=1e-4): return ((lnV(u+h,*p)-2*lnV(u,*p)+lnV(u-h,*p))/h**2)/k**2   # (lnV)''
def obs(n,e,sym,N=57.2):
    eps=lambda u:0.5*d1(u,n,e,sym)**2
    # end of inflation: first u (scanning up from small x) with eps=1
    us=[-14+0.01*i for i in range(1400)]
    ue=None
    for a,b in zip(us,us[1:]):
        if eps(a)<1<=eps(b): ue=brentq(lambda u:eps(u)-1,a,b); break
    if ue is None: return None
    # integrate N = ∫ dphi / sqrt(2 eps) backwards (field rolls toward larger u? sign by slope)
    u=ue; Nacc=0; du=-1e-3
    while Nacc<N and u>-40:
        s=abs(d1(u,n,e,sym)); Nacc+=k*abs(du)/s; u+=du
    g=d1(u,n,e,sym); h=d2(u,n,e,sym)
    epsv=0.5*g*g; eta=h+g*g          # V''/V = (lnV)'' + (lnV')^2
    return math.exp(u), 1-6*epsv+2*eta, 16*epsv
print("(0) control, original Twist n=124.1:")
for e in (0.0,3.04e-7):
    print(f"   eps={e}: x*, n_s, r =", obs(124.1,e,False))
print("(i) symmetry check:", max(abs(lnV(u,200,0,True)-lnV(-u,200,0,True)) for u in (0.3,1.7,3.4,6.0,9.0)))
for e in (0.0,3.04e-7):
    def gap(n):
        o=obs(n,e,True); xs=o[0]
        return (lnV(0.0,n,e,True)-lnV(math.log(xs),n,e,True))-math.log(6e-111)
    try:
        n=brentq(gap,120,600,xtol=1e-3); o=obs(n,e,True)
        ok=abs(o[1]-0.9728)<=0.0054 and o[2]<0.036
        print(f"(ii-iii) eps={e}: n={n:.2f}, x*={o[0]:.2e}, n_s={o[1]:.4f}, r={o[2]:.4f} -> {'PASS' if ok else 'FAIL'}")
    except Exception as ex: print(f"(ii-iii) eps={e}: failed: {ex}")
