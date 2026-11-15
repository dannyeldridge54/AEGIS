"""D655 (locked PREREG_D655_RHO_COVARIANT). AI-assisted."""
import mpmath as mp
mp.mp.dps=40
rho=mp.e**(2j*mp.pi/3)
def L(t): return -mp.log(2*mp.im(t)*abs(mp.eta(t))**4)
def dL(t,h=mp.mpf('1e-15')):
    gx=(L(t+h)-L(t-h))/(2*h); gy=(L(t+1j*h)-L(t-1j*h))/(2*h); return (gx-1j*gy)/2
Lr=L(rho)
def Irho(t): return mp.log(1+abs(mp.kleinj(t)*1728)**2/1728**2)/(4*mp.pi)
H=3.7e12
for y in (23,24,26,28,30):
    t=mp.mpf(1)/2+1j*mp.mpf(y)
    Vp=(lambda x: x/(x+1))(Irho(t)**2)+6e-5*(L(t)-Lr)
    br=mp.e**(L(t)-Lr)*(4*mp.mpf(y)**2*abs(dL(t))**2-3)
    b=mp.sqrt(3*Vp/br)
    print(f"y={y}: V_pl={mp.nstr(Vp,6)}, bracket={mp.nstr(br,4)} -> m3/2/H < {mp.nstr(b,3)}, m3/2 < {float(b)*H:.2e} GeV",flush=True)
