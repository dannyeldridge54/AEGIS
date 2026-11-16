"""D758 (locked PREREG_D758). AI-assisted. Fourier form of E(tau,2) along Re tau = 1/2 (exact series)."""
import math, mpmath as mp
mp.mp.dps=25
z3=mp.zeta(3); z4=mp.zeta(4)
def E(y,x=mp.mpf('0.5')):
    # E(tau,2) = sum' y^2/|m+n tau|^4 = 2z4 y^2 + (pi z3) / y  + (8 pi^2/ y) sum_{n>=1} sigma_{-3}(n) n^{3/2} ... use direct Bessel form
    s=2*z4*y**2 + mp.pi*z3/y
    tot=0
    for n in range(1,60):
        sig=sum(mp.mpf(d)**-3 for d in range(1,n+1) if n%d==0)
        tot+= sig*n**1.5*mp.besselk(1.5,2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return s + 8*mp.pi**2*mp.sqrt(y)*tot/mp.gamma(2)
def V(y,alpha=1):   # G^{tt} |d_tau ln E|^2 along x=1/2: d_tau = -(i/2) d_y (x-derivative zero by symmetry)
    d=mp.diff(lambda t: mp.log(E(t)), y)
    return (4*y**2/alpha)*(d**2)/4
yr=mp.sqrt(3)/2
print("checks: V(rho)=",mp.nstr(V(yr),5)," V(i)=",mp.nstr(V(mp.mpf(1),),5)," E(rho)=",mp.nstr(E(yr),8)," (D689: 5.7833593)")
Vinf=4/4
for y in (5,10,20,40):
    print(f"y={y}: V={mp.nstr(V(mp.mpf(y)),10)}, 1-V/Vinf={mp.nstr(1-V(mp.mpf(y))/Vinf,6)}")
p=mp.log((1-V(mp.mpf(10)))/(1-V(mp.mpf(20))))/mp.log(2); print("approach exponent p =",mp.nstr(p,5))
for alpha in (1,mp.mpf(1)/3):
    # canonical: phi = ln(y)/sqrt(2 alpha)  -> y = exp(sqrt(2 alpha) phi)
    k=mp.sqrt(2*alpha)
    Vp=lambda f: V(mp.e**(k*f),alpha)
    d1=lambda f: mp.diff(Vp,f); d2=lambda f: mp.diff(Vp,f,2)
    eps=lambda f:(d1(f)/Vp(f))**2/2
    fe=mp.findroot(lambda f: eps(f)-1, mp.log(2)/k)
    for N in (48,50,52):
        fs=mp.findroot(lambda f: mp.quad(lambda g: Vp(g)/d1(g),[fe,f])-N, mp.log(15)/k)
        e=eps(fs); eta=d2(fs)/Vp(fs)
        print(f"alpha={mp.nstr(alpha,3)} N*={N}: y*={mp.nstr(mp.e**(k*fs),4)}, n_s={mp.nstr(1-6*e+2*eta,6)}, r={mp.nstr(16*e,4)}")
