"""D589 (locked PREREG_D589_N_COUPLING). AI-assisted."""
import math, cmath
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
q=math.exp(-2*math.pi); E2=1-24*sum(sig(n,1)*q**n for n in range(1,60))
print(f"E2(i) = {E2:.12f}, 3/pi = {3/math.pi:.12f}, diff = {abs(E2-3/math.pi):.1e}")
MP=2.435e18; m=1.9e11; gs=106.75; m3=0.05e-9; v=174.; Yt=8.75e-11
def run(lam,x):
    c=0.5*x*x*(1-4*x*x)**1.5*lam*lam; G=c*m**3/(8*math.pi*MP**2)
    T=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP); M1=x*m
    eps1=3*M1*m3/(16*math.pi*v**2); Y=(8/23)*(3/4)*2*(T/m)*eps1
    return c,T,Y
for x in (1/3,0.316):
    for lam in (1,math.sqrt(2),3,6.6,10):
        c,T,Y=run(lam,x); print(f"M1/m={x:.3f} lambda={lam:.3f}: c_eff={c:.3f} T_RH={T:.2e} GeV Y_B,max={Y:.2e} {'PASS' if Y>=Yt else 'FAIL'}")
    lo,hi=0.1,100
    for _ in range(80):
        mid=(lo+hi)/2; lo,hi=(mid,hi) if run(mid,x)[2]<Yt else (lo,mid)
    print(f"  -> lambda needed (M1/m={x:.3f}): {hi:.2f}")
