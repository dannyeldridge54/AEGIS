import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import modular_twist_d490 as M
from scipy.optimize import brentq
def obs(n,e,kk,N=58.09):
    q=math.sqrt(kk/2)                       # phi = q ln x
    d1=lambda u,h=1e-5:(M.lnV(u+h,n,e,True)-M.lnV(u-h,n,e,True))/(2*h)/q
    d2=lambda u,h=1e-4:((M.lnV(u+h,n,e,True)-2*M.lnV(u,n,e,True)+M.lnV(u-h,n,e,True))/h**2)/q**2
    eps=lambda u:0.5*d1(u)**2
    us=[-20+0.01*i for i in range(2000)]
    ue=next(brentq(lambda u:eps(u)-1,a,b) for a,b in zip(us,us[1:]) if eps(a)<1<=eps(b))
    u=ue; Na=0; du=-1e-3
    while Na<N and u>-60: Na+=q*abs(du)/abs(d1(u)); u+=du
    g=d1(u); h=d2(u); ev=0.5*g*g; eta=h+g*g
    return math.exp(u),1-6*ev+2*eta,16*ev
n=234.017
print("control k=3:",obs(n,1.494e-7,3))
x,ns,r=obs(n,1.494e-7,1); print(f"(a) k=1, eps=1.494e-7: x*={x:.2e} n_s={ns:.4f} r={r:.5f}")
try:
    e=brentq(lambda e:obs(n,e,1)[1]-0.9736,1e-10,1.494e-7,xtol=1e-13)   # D1; x,ns,r=obs(n,e,1)
    a=-(obs(n,e,1,58.34)[1]-obs(n,e,1,57.84)[1])/0.5
    Vs=1.5*math.pi**2*2.1e-9*r*(2.435e18)**4; tgt=2.5e-47/Vs
    n2=brentq(lambda nn:(M.lnV(0.0,nn,e,True)-M.lnV(math.log(obs(nn,e,1)[0]),nn,e,True))-math.log(tgt),100,500,xtol=1e-3)
    print(f"(b) k=1 refit: eps={e:.3e} x*={x:.2e} n_s={ns:.4f} r={r:.5f} alpha_s={a:.2e}; (c) n={n2:.2f} (was 234.02)")
    v="STICKS" if r<0.036 and abs(n2/234.017-1)<0.1 else ("STICKS WITH CHANGED PREDICTIONS" if r<0.036 else "DOES NOT STICK")
    if abs(r/0.00435-1)>0.3 or abs(n2/234.017-1)>0.3: v="STICKS WITH CHANGED PREDICTIONS"
    print("VERDICT:",v)
except Exception as ex: print("(b) no fit:",ex,"\nVERDICT: DOES NOT STICK")
