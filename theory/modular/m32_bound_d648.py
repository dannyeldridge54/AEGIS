"""D648 (locked PREREG_D648_M32_PLATEAU_BOUND). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=40
def L(t): return -mp.log(2*mp.im(t)*abs(mp.eta(t))**4)
def dL(t,h=mp.mpf('1e-15')):
    gx=(L(t+h)-L(t-h))/(2*h); gy=(L(t+1j*h)-L(t-1j*h))/(2*h); return (gx-1j*gy)/2
Li=L(1j)
def f(y): t=1j*y; return mp.e**(L(t)-Li)*4*y**2*abs(dL(t))**2
def Ljm(y):
    q=mp.e**(-2*mp.pi*y); lj=2*mp.pi*y+mp.log(1+744*q+196884*q*q); return lj+mp.log(abs(1-1728*mp.e**(-lj)))
def Iy(y): return mp.log(mp.e**(2*(Ljm(y)-mp.log(1728)))+1)/(4*mp.pi)
def I1y(y): return mp.log(mp.e**(Ljm(y)-mp.log(1728))+1)/(4*mp.pi)
def Vpl(y,e): x=Iy(y)**2; return x/(x+1)+e*I1y(y)
s2=mp.sqrt(2)
def dphi(F,y,n):   # d^n/dphi^n with y = e^{sqrt2 phi}
    g=lambda p: F(mp.e**(s2*p)); p0=mp.log(y)/s2
    return mp.diff(g,p0,n)
H=3.7e12
for e in (1.3e-4,1.6e-4):
    for ys in (23,24.5):
        ys=mp.mpf(ys); V=Vpl(ys,e)
        F1=dphi(f,ys,1); F2=dphi(f,ys,2); f0=f(ys)
        # V_F/V0 = R0 f, R0 = m32^2/(3H^2); dn_s = 2 dEta - 6 dEps; dEta = R0 F2/V ; dEps ~ (V'/V) * R0 F1/V (cross term)
        Vp=dphi(lambda y: Vpl(y,e),ys,1)
        coef=2*F2/V - 6*(Vp/V)*(F1/V)
        R0max=1e-3/abs(coef)
        m=math.sqrt(3*float(R0max))*H
        print(f"eps={e} y*={float(ys)}: f(y*)={mp.nstr(f0,4)}, d2f/dphi2={mp.nstr(F2,4)}, |dn_s|/R0={mp.nstr(abs(coef),4)} -> m3/2/H < {math.sqrt(3*float(R0max)):.2e}, m3/2 < {m:.2e} GeV",flush=True)
