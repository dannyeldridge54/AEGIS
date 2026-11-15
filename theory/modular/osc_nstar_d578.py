"""D578 (locked PREREG_D578_OSC_NSTAR). AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=40
MP=2.435e18; As=2.1e-9; gs=106.75; lnk=math.log(0.05*4282.7)
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
J=lambda t:complex(kleinj(t))*1728
I =lambda t:math.log(1+abs(J(t)-1728)**2/1728**2)/(4*math.pi)
I1=lambda t:math.log(1+abs(J(t)-1728)/1728)/(4*math.pi)
def E2(t): q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,120))
def lneta(t): q=cmath.exp(2j*math.pi*t); return 2j*math.pi*t/24+sum(cmath.log(1-q**n) for n in range(1,200))
def VCI(t,N0): y=t.imag; L=math.log(2*y)+4*lneta(t).real; g=E2(t)-3/(math.pi*y); return y*y*abs(g)**2/(-6*L+N0)**2
def Ljm(y): q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); return lj+math.log(abs(1-1728*math.exp(-lj)))
def Iy(y): l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y): l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
def VCIy(y,N0):
    q=math.exp(-2*math.pi*y); e2=1-24*sum(sig(n,1)*q**n for n in range(1,40)); g=e2-3/(math.pi*y)
    le=-math.pi*y/12+sum(math.log(1-q**n) for n in range(1,60)); return y*y*g*g/(-6*(math.log(2*y)+4*le)+N0)**2
models={'K1 kappa=1e-3':('k',1e-3),'K2 kappa=1e-2':('k',1e-2),'C1 eps=1e-4':('e',1e-4)}
def Vy(y,m):
    x=Iy(y)**2; b=x/(x+1); return b+(m[1]*VCIy(y,25) if m[0]=='k' else m[1]*I1y(y))
def Vmass(t,m): return m[1]*VCI(t,25) if m[0]=='k' else m[1]*I1(t)
def infl(m,N):
    qn=1/math.sqrt(2); lv=lambda u:math.log(Vy(math.exp(u),m))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    u=ue; Na=0; du=1e-3
    while Na<N: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return dict(yend=math.exp(ue),ys=math.exp(u),ns=1-6*ev+2*(hh+g*g),r=16*ev,Vs=Vy(math.exp(u),m),Vend=Vy(math.exp(ue),m))
d=1e-3; c8=I(1j+1j*d)**2/d**8
print(f"octic coefficient: V ~ c8 delta^8, c8 = {c8:.4e}")
def nstar(m,res,cG,w):
    Vs=1.5*math.pi**2*As*res['r']*MP**4; H=math.sqrt(Vs/3)/MP
    mh2=2*Vmass(1j+1j*1e-4,m)/(1e-4/math.sqrt(2))**2      # V0 units, canonical phi
    mass=math.sqrt(3*mh2/res['Vs'])*H
    scale=Vs/res['Vs']; rho_end=res['Vend']*scale
    phx6=mh2/(32*c8); rho_x=mh2*phx6**(1/3)*scale            # 2*(1/2 m^2 phi^2)
    G=cG/(8*math.pi)*mass**3/MP**2; TR=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP); rho_R=math.pi**2*gs/30*TR**4
    N=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))
    rA=max(min(rho_x,rho_end),rho_R)
    N+=(1-3*w)/(12*(1+w))*math.log(rA/rho_end)
    if rA>rho_R: N+=(1/12)*math.log(rho_R/rA)
    return N,dict(H=H,m=mass,TR=TR,rho_end=rho_end,rho_x=rho_x,rho_R=rho_R)
for name,m in models.items():
    for cG in (1,10):
        for w,lab in ((0.6,'stiff bound w=3/5'),(0.0,'matter bound w=0')):
            res=infl(m,54); N,info=nstar(m,res,cG,w)
            res=infl(m,N); N2,info=nstar(m,res,cG,w); res=infl(m,N2)
            print(f"{name} c_G={cG} [{lab}]: m={info['m']:.2e} GeV (m/H={info['m']/info['H']:.4f}) T_RH={info['TR']:.2e} GeV rho_x/rho_end={info['rho_x']/info['rho_end']:.1e} "
                  f"N*={N2:.2f} -> y*={res['ys']:.1f} {'HOME-SAFE' if res['ys']<=25 else 'outside'} n_s={res['ns']:.4f} r={res['r']:.2e} ({(res['ns']-0.9684)/0.003:+.1f} SPA, {(res['ns']-0.9728)/0.0027:+.1f} SPA+DESI) inWindow={52<=N2<=55.6}")
