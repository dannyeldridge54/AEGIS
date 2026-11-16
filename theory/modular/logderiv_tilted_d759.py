"""D759 (locked PREREG_D759 + DEVIATIONS D1). AI-assisted. mpmath derivatives, analytic E for y >= 1.2."""
import mpmath as mp
mp.mp.dps=30
z3,z4=mp.zeta(3),mp.zeta(4)
def E(y):
    s=2*z4*y**2+mp.pi*z3/y
    if y<1.2:
        s+=8*mp.pi**2*mp.sqrt(y)*sum(sum(mp.mpf(d)**-3 for d in range(1,n+1) if n%d==0)*n**1.5*mp.besselk(1.5,2*mp.pi*n*y)*(-1)**n for n in range(1,12))
    return s
Er=E(mp.sqrt(3)/2); print("E(rho) =",mp.nstr(Er,9))
def V(y,C): return y**2*mp.diff(lambda t: mp.log(E(t)),y)**2*(1+C*(E(y)-Er))
for alpha in (1, mp.mpf(1)/3):
    k=mp.sqrt(2*alpha)
    for C in (0,5e-7,1e-6,1.15e-6,1.3e-6,2e-6,4e-6):
        Vp=lambda f: V(mp.e**(k*f),C)
        d1=lambda f: mp.diff(Vp,f); d2=lambda f: mp.diff(Vp,f,2)
        eps=lambda f:(d1(f)/Vp(f))**2/2
        fe=mp.findroot(lambda f: eps(f)-1, mp.log(2.0)/k)
        row=[]
        for N in (48,50,52):
            fs=mp.findroot(lambda f: mp.quad(lambda g: Vp(g)/d1(g),[fe,f])-N, mp.log(16)/k)
            e=eps(fs); et=d2(fs)/Vp(fs)
            row.append(f"N={N}: y*={mp.nstr(mp.e**(k*fs),4)} n_s={mp.nstr(1-6*e+2*et,5)} r={mp.nstr(16*e,3)}")
        print(f"alpha={mp.nstr(alpha,3)} C={C:g}: "+" | ".join(row), flush=True)
