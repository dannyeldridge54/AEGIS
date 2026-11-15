import sys, math, cmath; sys.path.insert(0,'theory/modular'); import modular_lib as L
MP=2.435e18; Vs=1.5*math.pi**2*2.1e-9*0.00323*MP**4; Lam=2.5e-47
def lnV_c(tau,a,c):
    b=-0.25-a
    def H(J): return (J-1728)**a*J**b*cmath.log(J/1728)**1.5 + c*J**b
    return L.lnV(tau,H)
for a in (0.5,1.0):
    # plateau normalisation: V_plateau (c=0) at large y in model units -> physical V_* ; take V at y*=146 as V_* proxy via log-form asymptote
    # use y=20 (deep on plateau, below overflow): V_pl ~ (2pi y)^3/(8 y^3)=pi^3 ; check numerically
    Vpl=math.exp(L.lnV(20j,lambda J:(J-1728)**a*J**(-0.25-a)*cmath.log(J/1728)**1.5))
    # V(i) with c: V(i)=|c|^2 |1728^b|^2/(8|eta(i)|^12)
    b=-0.25-a; base=abs(1728**b)**2/(8*abs(L.eta(1j))**12)
    c=math.sqrt(Lam/Vs*Vpl/base)
    print(f"a={a}: V_plateau(model)={Vpl:.3f} (pi^3={math.pi**3:.3f}); c={c:.2e}, S=-ln c={-math.log(c):.1f} (=2pi x {-math.log(c)/2/math.pi:.1f})")
    lv=lambda x,y:lnV_c(complex(x,y),a,c)
    V0=math.exp(lv(0,1))
    # Hessian in canonical fields at tau=i (y-direction: phi_y = sqrt(3/2) ln y; x-direction: dphi_x = sqrt(3/2) dx/y)
    h=1e-3; k=math.sqrt(1.5)
    Vy=lambda d: math.exp(lv(0,math.exp(d/k)))
    Vx=lambda d: math.exp(lv(d/k,1.0))
    myy=(Vy(h)-2*V0+Vy(-h))/h**2; mxx=(Vx(h)-2*V0+Vx(-h))/h**2
    scale=Vs/Vpl/MP**4          # converts model V to M_P^4 units
    for lab,m2 in (("y",myy),("x",mxx)):
        mm=math.sqrt(abs(m2)*scale)*MP
        print(f"   direction {lab}: curvature {'>0' if m2>0 else '<0'}; m = {mm:.2e} GeV ->", ("HEAVY" if mm>1e-12 else "LIGHT"), "and", ("MODULI-SAFE" if mm>=1e5 else "moduli-risk"))
    print(f"   V(i)/V_plateau = {V0/Vpl:.2e} (target {Lam/Vs:.2e}) ->", "VACUUM OK" if myy>0 and mxx>0 else "NOT A MINIMUM")
