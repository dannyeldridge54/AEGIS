import numpy as np, mpmath as mp
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def xi(s): return mp.pi**(-s/2)*mp.gamma(s/2)*mp.zeta(s)
phi2=xi(3)/xi(4)
def sig(n,a): return sum(d**a for d in range(1,n+1) if n%d==0)
def E2(x,y):
    s=y**2+phi2/y
    for n in range(1,13):
        s+=2*mp.sqrt(y)/xi(4)*n**1.5*sig(n,-3)*mp.besselk(1.5,2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return float(s)
yr=np.sqrt(3)/2; Er=E2(0.5,yr)
# sanity: lattice sum G = sum' y^2/|m+n tau|^4 = 2 zeta(4) E
tau=0.5+1j*yr; G=sum(yr**2/abs(m+n*tau)**4 for m in range(-300,301) for n in range(-300,301) if (m,n)!=(0,0))
chk=G/(2*float(mp.zeta(4)))
C=1.15e-6
ph=np.linspace(np.log(yr)/np.sqrt(2),np.log(200)/np.sqrt(2),6000)
Eh=np.array([E2(0.5,np.exp(np.sqrt(2)*p))-Er for p in ph]); Eh[0]=0.0
Sp=CubicSpline(ph,Eh); dSp=Sp.derivative()
def V1(p): e=Sp(p); return e/(e+1)*(1+C*e)
def dV1(p): e=Sp(p); de=dSp(p); return de*((1+C*e)/(e+1)**2 + C*e/(e+1))
def run(model,M=None):
    # start near the slope zero of V1 (largest phi with dV1>0 before turnaround)
    g=np.array([dV1(p) for p in ph]); idx=np.where(g<=0)[0]
    pmax=ph[idx[idx>10][0]] if len(idx[idx>10]) else ph[-1]
    p0=pmax-1e-3
    if model==1:
        def rhs(N,u):
            p,pd=u; eps=0.5*pd**2; return [pd,-(3-eps)*pd-(3-eps)*dV1(p)/V1(p)]
        u0=[p0,0.0]
    else:
        def V2(p,c): e=Sp(p); return (e*c*c+(1-c)**2)*(1+C*e)
        def rhs(N,u):
            p,s,pd,sd=u; c=s/M; e=Sp(p); de=dSp(p); R=1+C*e; Q=e*c*c+(1-c)**2
            V=Q*R; Vp=de*(c*c*R+Q*C); Vs=(2*e*c-2*(1-c))*R/M
            eps=0.5*(pd**2+sd**2)
            return [pd,sd,-(3-eps)*pd-(3-eps)*Vp/V,-(3-eps)*sd-(3-eps)*Vs/V]
        u0=[p0,M/(Sp(p0)+1),0.0,0.0]
    end=lambda N,u:0.5*(u[-2]**2+(u[-1]**2 if model==2 else 0))-1 if model==2 else 0.5*u[1]**2-1
    end.terminal=True; end.direction=1
    sol=solve_ivp(rhs,[0,3000],u0,events=end,rtol=1e-10,atol=1e-12,dense_output=True,max_step=0.5)
    Nend=sol.t_events[0][0]; Ns=Nend-55
    def epsH(N):
        u=sol.sol(N); return 0.5*(u[-2]**2+u[-1]**2) if model==2 else 0.5*u[1]**2
    h=1e-3; e0=epsH(Ns); dl=(np.log(epsH(Ns+h))-np.log(epsH(Ns-h)))/(2*h)
    out=dict(Ntot=Nend,ns=1-2*e0-dl,r=16*e0)
    if model==2:
        # turn rate and heavy mass estimate at N*
        u=sol.sol(Ns); p,s,pd,sd=u; v=np.array([pd,sd]); a=(sol.sol(Ns+h)[2:]-sol.sol(Ns-h)[2:])/(2*h)
        Om=abs(v[0]*a[1]-v[1]*a[0])/np.dot(v,v)  # turn per e-fold = Omega/H
        c=s/M; e=Sp(p); R=1+C*e; Q=e*c*c+(1-c)**2
        Vss=2*(e+1)*R/M**2; meff2=Vss/(Q*R/3)  # m^2/H^2 (normal direction ~ sigma)
        out.update(OmH=Om,m2H2=meff2,one_minus_cs2=4*Om**2/meff2)
    return out
lines=[f"E(rho,2) Fourier {Er:.6f} vs lattice sum {chk:.6f}"]
r1=run(1); lines.append(f"1-field P3: {r1}")
res={}
for M in (0.1,0.2,0.5):
    r2=run(2,M); res[M]=r2
    dns=r2['ns']-r1['ns']; dr=r2['r']/r1['r']-1
    lines.append(f"M={M}: {r2} | dns={dns:+.2e} dr/r={dr:+.2%}")
ok=all(abs(res[M]['ns']-r1['ns'])<=5e-4 and abs(res[M]['r']/r1['r']-1)<=0.02 and res[M]['one_minus_cs2']<=1e-2 for M in (0.1,0.2))
lines.append('PASS' if ok else 'FAIL')
open('field_tests/results/twofield_p3_d943.txt','w').write('\n'.join(lines)+'\n'); print('\n'.join(lines))
