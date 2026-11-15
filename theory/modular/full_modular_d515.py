import sys, math, cmath; sys.path.insert(0,'theory/modular'); import modular_lib as L
from scipy.optimize import brentq
q=math.sqrt(1.5)
def run(a,N=58.09):
    b=-0.25-a
    def lv(u):   # D1: log-form ln V on the imaginary axis
        y=math.exp(u)
        if y<1.5:
            J=L.j(1j*y); lj=cmath.log(J); ljm=math.log(abs(J-1728)); lje=math.log(abs(L.eta(1j*y)))
        else:
            qq=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*qq+196884*qq**2+21493760*qq**3)
            ljm=lj+math.log(abs(1-1728*math.exp(-lj))); lje=-math.pi*y/12+sum(math.log(1-qq**k) for k in range(1,6))
            lj=complex(lj,0)
        L15=1.5*math.log(abs(lj-math.log(1728)))
        return 2*(a*ljm+b*lj.real+L15)-3*math.log(2*y)-12*lje
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/q
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/q**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.005*i for i in range(800)]           # y from ~1.02 upward
    # end of inflation: largest-u point scanning downward from the plateau where eps crosses 1
    ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<12: Na+=q*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g; eta=hh+g*g
    ns=1-6*ev+2*eta; r=16*ev
    return math.exp(ue),math.exp(u),ns,r
for a in (0.5,1.0,1.5):
    o=run(a)
    if o is None: print(f"a={a}: no end of inflation found"); continue
    ye,ys,ns,r=o; s1=(ns-0.9684)/0.003; s2=(ns-0.9728)/0.0027
    ok=(abs(s1)<=2 or abs(s2)<=2) and r<0.036
    print(f"a={a}: y_end={ye:.3f}, y*={ys:.3f}, n_s={ns:.4f}, r={r:.5f}  ({s1:+.1f} / {s2:+.1f} sigma) -> {'VIABLE' if ok else 'NOT VIABLE'}")
