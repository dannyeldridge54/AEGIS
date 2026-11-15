"""D541 SERAPIS-2 (locked PREREG_D541_SERAPIS2). Method copied from PC job J4 (janus_j4.py). AI-assisted."""
import math
from scipy.optimize import brentq
def lnV_y(y,kp):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj))); le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,6))
    L=-math.log(2*y)-4*le+kp
    return ljm-7/6*lj+math.log(L)-math.log(2*y)-4*le
def infl(kp,N):
    qn=1/math.sqrt(2); lv=lambda u:lnV_y(math.exp(u),kp)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.30+0.005*i for i in range(1300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for kp in (0,1,2*math.pi):
    for N in (52,55.6):
        res=infl(kp,N)
        if res is None: print(f"kappa'={kp:.3f} N*={N}: no end found"); continue
        ye,ys,ns,r=res
        print(f"kappa'={kp:.3f} N*={N}: y_end={ye:.2f} y*={ys:.1f} n_s={ns:.4f} r={r:.5f} ({(ns-0.9684)/0.0030:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} sigma SPA+DESI)")
