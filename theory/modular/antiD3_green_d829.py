"""D829 (locked PREREG_D829). Torus Green's function sums for the anti-D3 interaction. AI-assisted."""
import mpmath as mp
mp.mp.dps=30
def eta(U): q=mp.exp(2j*mp.pi*U); return mp.exp(1j*mp.pi*U/12)*mp.qp(q)
def G(z,U):
    q=mp.exp(1j*mp.pi*U); t1=mp.jtheta(1,mp.pi*z,q)
    return -mp.log(abs(t1/eta(U))**2)+2*mp.pi*mp.im(z)**2/mp.im(U)
def Delta(U): return -mp.log(mp.im(U)*abs(eta(U))**4)
pts=[('i',mp.mpc(0,1)),('rho',mp.mpc(0.5,mp.sqrt(3)/2))]+[(f'1/2+{y}i',mp.mpc(0.5,y)) for y in (2,5,10,20)]
for name,U in pts:
    zs=[mp.mpf(0.5),U/2,(1+U)/2]; g=[G(z,U) for z in zs]; S=sum(g)
    print(f"U={name}: G_k=({', '.join(mp.nstr(x,6) for x in g)}) S={mp.nstr(S,8)} Delta={mp.nstr(Delta(U),8)} S/y={mp.nstr(S/mp.im(U),6)} Delta/y={mp.nstr(Delta(U)/mp.im(U),6)}")
