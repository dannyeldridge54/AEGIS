"""Independent check of D1736: mpmath forms (E2,E4,E6 via nsum, eta via mp product), stationary point via findroot on dV/dx, dV/dy."""
import mpmath as mp
mp.mp.dps=30
def E(k,t):
    q=mp.e**(2j*mp.pi*t); c={2:-24,4:240,6:-504}[k]
    return 1+c*mp.nsum(lambda n: n**(k-1)*q**n/(1-q**n),[1,mp.inf])
def V(x,y,m,n):
    t=mp.mpc(x,y); E2,E4,E6=E(2,t),E(4,t),E(6,t)
    q=mp.e**(2j*mp.pi*t); eta=mp.e**(2j*mp.pi*t/24)*mp.qp(q)
    j=1728*E4**3/(E4**3-E6**2); jp=-2j*mp.pi*j*E6/E4
    H2=abs(j-1728)**m*(abs(j)**(mp.mpf(2*n)/3) if n else 1)
    dl=(m*jp/(2*(j-1728)))+((n*jp/(3*j)) if n else 0)-(1j*mp.pi/2)*E2+3j/(2*y)
    return (2*y)**-3*H2/abs(eta)**12*((4*y*y/3)*abs(dl)**2-3)
def stat(m,n,x0,y0):
    g=lambda x,y:[mp.diff(lambda u:V(u,y,m,n),x),mp.diff(lambda u:V(x,u,m,n),y)]
    return mp.findroot(g,(mp.mpf(x0),mp.mpf(y0)),verify=False)
w=mp.e**(2j*mp.pi/3)
for m,n,x0,y0,ref in ((1,0,-0.4844,0.8842,-0.484440+0.884238j),(8,0,-0.49799,0.86842,-0.497988+0.868420j),(1,1,-0.2378,0.9713,-0.23776+0.97132j)):
    r=stat(m,n,x0,y0); t=complex(r[0],r[1]) if not isinstance(r[0],mp.mpc) else complex(r[0].real,r[1].real)
    print(f"({m},{n}): findroot tau={t.real:.6f}{t.imag:+.6f}i  Q11={ref}  |diff|={abs(t-ref):.1e}  |tau|={abs(t):.6f}  |eps|={abs(t-complex(w)):.5f}")
