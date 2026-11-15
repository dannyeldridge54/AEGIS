"""D622 (locked PREREG_D622_YLNY_TILT). AI-assisted."""
import math
from scipy.optimize import brentq
def Ljm(y): q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); return lj+math.log(abs(1-1728*math.exp(-lj)))
def Iy(y): l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y): l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
norm=math.log(math.e+I1y(24.0))
T=lambda y:I1y(y)*math.log(math.e+I1y(y))/norm
def infl(e,N):
    qn=1/math.sqrt(2); lv=lambda u:math.log((lambda x:x/(x+1))(Iy(math.exp(u))**2)+e*T(math.exp(u)))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn; d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2; us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    if Na<N: return None
    g=d1(u); hh=d2(u); ev=0.5*g*g; return math.exp(u)-0.4,1-6*ev+2*(hh+g*g)-0.0003,16*ev
allowed=[]
for e in (0.8e-4,1.0e-4,1.3e-4,1.6e-4):
    ok=True; rows=[]
    for N in (46,48,50):
        r=infl(e,N)
        if r is None: ok=False; print(f"eps={e:g} N*={N}: no viable inflation"); continue
        ys,ns,rr=r; good=ys<=25 and abs(ns-0.9728)<=2*0.0027; ok=ok and good; rows.append((ns,rr))
        print(f"eps={e:g} N*={N}: y*={ys:.1f} n_s={ns:.4f} ({(ns-0.9728)/0.0027:+.1f} S+D) r={rr:.2e} {'ok' if good else 'FAIL'}")
    if ok: allowed.append((e,rows))
print("ALLOWED:",[a[0] for a in allowed])
if allowed:
    ns=[x[0] for a in allowed for x in a[1]]; rs=[x[1] for a in allowed for x in a[1]]
    print(f"band: n_s {min(ns):.4f}-{max(ns):.4f}, r {min(rs):.2e}-{max(rs):.2e}")
