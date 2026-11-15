"""D719 (locked PREREG_D719): N* for SERAPIS-E from the matching equation (Planck 2018 X, eq. 47 form). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=20
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rho=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rho); s2=mp.sqrt(2); C=mp.mpf('1.15e-6')
Eh=lambda y: Eser(mp.mpc(0.5,y))-Er
V=lambda p: (lambda e: e/(e+1)*(1+C*e))(Eh(mp.e**(s2*p)))
d=lambda p,k: mp.diff(V,p,k)
eps=lambda p:(d(p,1)/V(p))**2/2
pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
def at(N):
    ps=mp.findroot(lambda p: mp.quad(lambda w:V(w)/d(w,1),[pe,p])-N, mp.log(15)/s2)
    e=eps(ps); h=d(ps,2)/V(ps); return float(1-6*e+2*h), float(16*e), float(V(ps)/V(pe))
Mp=2.435e18; As=2.1e-9; g=106.75; lnk=math.log(0.05/(67.4/299792.458))
print(f"ln(k/a0H0) = {lnk:.3f}; end of inflation at y_end = {float(mp.e**(s2*pe)):.3f}")
for TR in (1e4,1e6,1e7,1e8,1e10):
    N=49.0
    for it in range(30):
        ns,r,ratio=at(N)
        Vs=1.5*math.pi**2*As*r*Mp**4; rho_end=1.5*Vs/ratio; rho_th=math.pi**2/30*g*TR**4
        Nn=67-lnk+0.25*math.log(Vs**2/(Mp**4*rho_end))+(1/12)*math.log(rho_th/rho_end)-(1/12)*math.log(g)
        if abs(Nn-N)<0.01: N=Nn; break
        N=Nn
    print(f"T_R={TR:.0e} GeV: N*={N:.2f}  (n_s={ns:.4f}, r={r:.3e}, V*^(1/4)={Vs**0.25:.3e} GeV, V*/V_end={ratio:.3f})")
