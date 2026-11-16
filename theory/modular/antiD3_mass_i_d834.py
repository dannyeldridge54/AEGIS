"""D834 (locked PREREG_D834). Hessian of the anti-D3 term at tau = i. AI-assisted."""
import mpmath as mp
mp.mp.dps=30
def eta(U): q=mp.exp(2j*mp.pi*U); return mp.exp(1j*mp.pi*U/12)*mp.qp(q)
def G(z,U):
    t1=mp.jtheta(1,mp.pi*z,mp.exp(1j*mp.pi*U))
    return -mp.log(abs(t1/eta(U))**2)+2*mp.pi*mp.im(z)**2/mp.im(U)
def Dl(U): return -mp.log(mp.im(U)*abs(eta(U))**4)
def B(U,za):
    fp=[0,mp.mpf(0.5),U/2,(1+U)/2]; N=[2,5,5,5]; tot=0
    for n,z in zip(N,fp):
        d=za-z
        # za and z are both half-periods: coincident iff d is a lattice vector
        g=Dl(U) if any(abs(d-a-b*U)<mp.mpf('1e-25') for a in (-1,0,1) for b in (-1,0,1)) else G(d,U)
        tot+=(n-4)*g
    return tot
kv=2.07e-4
for za,lab in ((0,'0'),(mp.mpf(0.5),'1/2')):
    for h in (mp.mpf('1e-3'),mp.mpf('1e-4')):
        U0=mp.mpc(0,1); f=lambda dx,dy: B(U0+dx+1j*dy,za)
        f0=f(0,0); bx=(f(h,0)-f(-h,0))/(2*h); by=(f(0,h)-f(0,-h))/(2*h)
        bxx=(f(h,0)-2*f0+f(-h,0))/h**2; byy=(f(0,h)-2*f0+f(0,-h))/h**2
        bxy=(f(h,h)-f(h,-h)-f(-h,h)+f(-h,-h))/(4*h**2)
        H=mp.matrix([[-2*bxx,-2*bxy],[-2*bxy,-2*byy]])  # Hessian of V/kappa
        ev=mp.eig(H)[0]
        m2=[3*kv*2*e for e in ev]  # m^2/H^2 = 3 (kappa/V0) * 2 * eig(V/kappa)
        print(f"z_a={lab} h={mp.nstr(h,1)}: grad=({mp.nstr(bx,4)},{mp.nstr(by,4)}) Bxx={mp.nstr(bxx,8)} Byy={mp.nstr(byy,8)} Bxy={mp.nstr(bxy,4)} eig(V''/kappa)={[mp.nstr(mp.re(e),6) for e in ev]} m2/H2={[mp.nstr(mp.re(m),4) for m in m2]}")
