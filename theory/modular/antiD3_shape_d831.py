"""D831 (locked PREREG_D831). Anti-D3 T²-shape at the D830 placement. AI-assisted."""
import mpmath as mp
mp.mp.dps=30
def eta(U): q=mp.exp(2j*mp.pi*U); return mp.exp(1j*mp.pi*U/12)*mp.qp(q)
def G(z,U):
    t1=mp.jtheta(1,mp.pi*z,mp.exp(1j*mp.pi*U))
    return -mp.log(abs(t1/eta(U))**2)+2*mp.pi*mp.im(z)**2/mp.im(U)
def Gt(z,U): # regularised: coincident -> Delta
    return -mp.log(mp.im(U)*abs(eta(U))**4) if abs(z)<1e-20 else G(z,U)
def red(z,U): # reduce to fundamental cell representative among half-periods
    for w in (0,mp.mpf(0.5),U/2,(1+U)/2):
        for a in (-1,0,1):
            for b in (-1,0,1):
                if abs(z-w-a-b*U)<1e-20: return w
    return z
pts=[('i',mp.mpc(0,1)),('rho',mp.mpc(0.5,mp.sqrt(3)/2))]+[(f'1/2+{y}i',mp.mpc(0.5,y)) for y in (2,5,10,20)]
res={}
for name,U in pts:
    fp=[0,mp.mpf(0.5),U/2,(1+U)/2]; N=[2,5,5,5]
    out=[]
    for za in (0,mp.mpf(0.5)):
        B=sum(n*Gt(red(za-z,U),U) for n,z in zip(N,fp))-4*sum(Gt(red(za-z,U),U) for z in fp)
        out.append(B)
    res[name]=out
    print(f"U={name}: B(0)={mp.nstr(out[0],8)} B(1/2)={mp.nstr(out[1],8)}")
for k in (0,1):
    s=(res['1/2+20i'][k]-res['1/2+10i'][k])/10
    print(f"slope dB/dy (10->20), z_a={'0' if k==0 else '1/2'}: {mp.nstr(s,6)}  vs -2pi/3={mp.nstr(-2*mp.pi/3,6)}")
