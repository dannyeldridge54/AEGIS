import math, mpmath as mp
from scipy.optimize import brentq
mp.mp.dps=200
def lnV_y(y,kap):        # imaginary axis, log form, c-term negligible on the plateau
    if y<1.5:
        t=mp.mpc(0,y); J=jj(t); e=abs(eta(t))
        H=(J-1728)**mp.mpf(0.5)*J**(-mp.mpf(7)/12)*(mp.log(J/1728)+kap)**mp.mpf(0.5)
        return float(2*mp.log(abs(H))-mp.log(2*y)-4*mp.log(e))
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj))); le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,6))
    return 2*(0.5*ljm-7/12*lj+0.5*math.log(lj-math.log(1728)+kap))-math.log(2*y)-4*le
def eta(t,N=300):
    q=mp.e**(2j*mp.pi*t); p=mp.mpf(1)
    for n in range(1,N): p*=1-q**n
    return mp.e**(2j*mp.pi*t/24)*p
def E4(t,N=300):
    q=mp.e**(2j*mp.pi*t); return 1+240*mp.fsum(mp.fsum(d**3 for d in range(1,n+1) if n%d==0)*q**n for n in range(1,N))
def jj(t): return E4(t)**3/eta(t)**24
def infl(kap,N=58.09):
    q=1/math.sqrt(2)
    lv=lambda u:lnV_y(math.exp(u),kap)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/q
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/q**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.45+0.005*i for i in range(1200)]
    ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=q*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g; ns=1-6*ev+2*(hh+g*g); r=16*ev
    g2=lambda uu:d1(uu)
    return math.exp(ue),math.exp(u),ns,r
for kap in (1.0,2*math.pi):
    ye,ys,ns,r=infl(kap); s1=(ns-0.9684)/0.003; s2=(ns-0.9728)/0.0027
    tag="" if kap==1.0 else " [sensitivity only]"
    print(f"kappa={kap:.3f}{tag}: y_end={ye:.3f}, y*={ys:.2f}, n_s={ns:.4f}, r={r:.5f} ({s1:+.1f}/{s2:+.1f} sigma) ->", "VIABLE" if (abs(s1)<=2 or abs(s2)<=2) and r<0.036 else "NOT VIABLE")
# vacuum (kappa=1) at 50 digits
kap=mp.mpf(1); MP=mp.mpf('2.435e18'); r=mp.mpf(r)
def V(t,c):
    J=jj(t); H=(J-1728)**mp.mpf(0.5)*J**(-mp.mpf(7)/12)*(mp.log(J/1728)+kap)**mp.mpf(0.5)+c*J**(-mp.mpf(7)/12)
    return abs(H)**2/((2*mp.im(t))*abs(eta(t))**4)
_,_,ns1,r1=infl(1.0); r1=mp.mpf(r1)
Vs=mp.mpf(1.5)*mp.pi**2*mp.mpf('2.1e-9')*r1*MP**4; Lam=mp.mpf('2.5e-47')
Vpl=V(mp.mpc(0,20),0)
base=abs(mp.mpf(1728)**(-mp.mpf(7)/12))**2/(2*abs(eta(mp.mpc(0,1)))**4)
c=mp.sqrt(Lam/Vs*Vpl/base); V0=V(mp.mpc(0,1),c)
k=1/mp.sqrt(2); h=mp.mpf('1e-6')
Vy=lambda d:V(mp.mpc(0,mp.e**(d/k)),c); Vx=lambda d:V(mp.mpc(d/k,1),c)
myy=(Vy(h)-2*V0+Vy(-h))/h**2; mxx=(Vx(h)-2*V0+Vx(-h))/h**2; sc=Vs/Vpl/MP**4
print(f"vacuum: V(i)/V_pl={mp.nstr(V0/Vpl,3)} (target {mp.nstr(Lam/Vs,3)}); c={mp.nstr(c,3)}, S=-ln c={mp.nstr(-mp.log(c),5)} (=2pi x {mp.nstr(-mp.log(c)/2/mp.pi,4)})")
for lab,m2 in (("y",myy),("x",mxx)):
    m=mp.sqrt(abs(m2)*sc)*MP; print(f"   {lab}: curvature {'>0' if m2>0 else '<0'}; m = {mp.nstr(m,3)} GeV ->", "STIFF" if m>=1e5 else "NOT STIFF")
print(f"   ratio m/H_inf: H_inf ~ {mp.nstr(mp.sqrt(Vs/3)/MP,3)} GeV")
