"""D747 (locked PREREG_D747). AI-assisted."""
import mpmath as mp
mp.mp.dps=30
def th(k,U):
    q=mp.exp(1j*mp.pi*U)
    return {2:mp.jtheta(2,0,q),3:mp.jtheta(3,0,q),4:mp.jtheta(4,0,q)}[k]
def eta(U):
    q=mp.exp(2j*mp.pi*U); return mp.exp(2j*mp.pi*U/24)*mp.qp(q)
for y in (2,5,10,14,20):
    U=mp.mpc(0.5,y); t2,t3,t4,e=th(2,U),th(3,U),th(4,U),eta(U)
    ident=abs(t2*t3*t4/(2*e**3)-1)
    L=[float(mp.log(abs(t/e)**2)) for t in (t2,t3,t4)]
    E2=float(mp.re(sum(y**2/abs(m+n*U)**4 for m in range(-40,41) for n in range(-40,41) if (m,n)!=(0,0))))
    print(f"y={y}: |t2 t3 t4/(2 eta^3)-1|={float(ident):.1e}; ln|t_k/eta|^2 = {L[0]:.3f}, {L[1]:.3f}, {L[2]:.3f}; slope check pi*y/6={float(mp.pi*y/6):.3f}; E(U,2)~{E2:.2f} (plateau needs 1/E ~ y^-2)")
