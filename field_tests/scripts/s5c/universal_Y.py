import sys, math, cmath, numpy as np; sys.path.insert(0,'.')
from tools.serapis_calc.modint import gamma22, _gamma22_dual
from tools.serapis_calc.shapes import E
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
S3=[sig(n,3) for n in range(1,40)]; S5=[sig(n,5) for n in range(1,40)]; S1=[sig(n,1) for n in range(1,40)]
def eis(tau):
    q=cmath.exp(2j*math.pi*tau); qs=[q**n for n in range(1,40)]
    E2=1-24*sum(a*b for a,b in zip(S1,qs)); E4=1+240*sum(a*b for a,b in zip(S3,qs)); E6=1-504*sum(a*b for a,b in zip(S5,qs))
    D=(E4**3-E6**2)/1728; return E2,E4,E6,D
def Phi(tau):
    E2,E4,E6,D=eis(tau); E2h=E2-3/(math.pi*tau.imag)
    return ((E2h*E4*E6/D).conjugate()/8 + 33).real
def Phi0(y): return 90/(math.pi*y)   # constant term (checked analytically: (1/8)(-264 + 720/(pi y)) + 33)
def jfun(tau):
    q=cmath.exp(2j*math.pi*tau)
    if tau.imag > 2: return 1/q + 744 + 196884*q
    E2,E4,E6,D=eis(tau); return E4**3/D
def Y(T,U,L=40.0,n1q=48,n2q=200,ycut=3.0):
    x,wx=np.polynomial.legendre.leggauss(n1q); y,wy=np.polynomial.legendre.leggauss(n2q); tot=0.0
    for xi,wi in zip(x,wx):            # region |tau1|<=1/2, |tau|>=1, tau2<ycut: full integrand
        t1=0.5*xi; y0=math.sqrt(1-t1*t1); ys=y0+(ycut-y0)*(y+1)/2; wys=wy*(ycut-y0)/2
        tot+=0.5*wi*sum(wj*gamma22(complex(t1,yj),T,U,N=6)*Phi(complex(t1,yj))/yj for yj,wj in zip(ys,wys))
    ys=ycut+(L-ycut)*(y+1)/2; wys=wy*(L-ycut)/2   # tau2>=ycut: tau1-average = Phi0 * degenerate orbit (non-degenerate x qbar^-1 negligible for T2 >> U2)
    tot+=sum(wj*Phi0(yj)*_gamma22_dual(complex(0,yj),T,U)/yj for yj,wj in zip(ys,wys))
    return tot + 0.5*math.log(abs(jfun(T)-jfun(U)))
kappa=E(1j,2)/math.pi**2
for R,yc in ((2.0,2.0),(2.0,2.5)):
    T=complex(0,R*R); U=1j; y=Y(T,U,ycut=yc)
    print(R,'Y numeric %.6f'%y,' PR eq31 %.6f'%(6*math.pi*R*R+90*kappa/(math.pi*R*R)), flush=True)
