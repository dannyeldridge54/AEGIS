# D888 (L.1): reverse path for the rho lift eps ~ 1.8e-3 (D883). Arithmetic only.
import mpmath as mp
mp.mp.dps=30
rho=mp.e**(2j*mp.pi/3)
def E(k,t,N=400):
    q=mp.e**(2j*mp.pi*t); c={2:-24,4:240,6:-504}[k]
    return 1+c*mp.nsum(lambda n: n**(k-1)*q**n/(1-q**n),[1,N])
E4r,E6r=E(4,rho),E(6,rho)
dE4=mp.diff(lambda t:E(4,t),rho)
print("E4(rho)=",mp.nstr(abs(E4r),3)," E6(rho)=",mp.nstr(E6r,8))
print("E4'(rho)=",mp.nstr(dE4,8)," check -(2pi i/3)E6=",mp.nstr(-(2j*mp.pi/3)*E6r,8))
eps=1.8e-3; lo,hi=3.1e-4,1.1e-2
# weight-matched invariant: eps ~ |E4(tau)|/|E6(tau)|^(2/3)
k=abs(dE4)/abs(E6r)**(2/3.)
for e in (lo,eps,hi): print(f"(a) displacement |tau-rho| for eps={e:.1e}: {e/float(k):.2e}")
print("(c) one-loop 1/16pi^2 =",1/(16*mp.pi**2)," eps/loop =",eps*16*float(mp.pi**2))
for e in (lo,eps,hi): print(f"(d) instanton: Im T/N = {float(-mp.log(e)/(2*mp.pi)):.3f} for eps={e:.1e}")
MP=2.435e18
for e in (lo,eps,hi): print(f"(e) Planck-suppressed Lambda = eps*M_P = {e*MP:.2e} GeV for eps={e:.1e}")
