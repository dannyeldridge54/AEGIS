"""D647 (locked PREREG_D647_COVARIANT_W). AI-assisted."""
import mpmath as mp
mp.mp.dps=40
rho=mp.e**(2j*mp.pi/3)
def G(t,cov=True):
    y=mp.im(t); K=-mp.log(2*y)
    return K - (2*mp.log(abs(mp.eta(t))**2) if cov else 0)   # ln|W|^2 with W = eta^{-2}
def Gtau(t,cov,h=mp.mpf('1e-12')):
    gx=(G(t+h,cov)-G(t-h,cov))/(2*h); gy=(G(t+1j*h,cov)-G(t-1j*h,cov))/(2*h)
    return (gx-1j*gy)/2
for name,t in (('i',1j),('rho',rho)):
    print(f"{name}: covariant W=W0 eta^-2: G_tau = {mp.nstr(Gtau(t,True),5)} ; constant W0: G_tau = {mp.nstr(Gtau(t,False),5)}")
print(f"m3/2 (W0=1, covariant) at i = e^(G/2) = {mp.nstr(mp.e**(G(1j)/2),8)}; at rho = {mp.nstr(mp.e**(G(rho)/2),8)}")
# soft masses: V = e^G (G^{ab} G_a G_bbar - 3) with fields tau, S, Q; G = K(tau,S,Q) + ln|W|^2,
# K = -ln 2y + |S|^2 + |Q|^2/(2y)^k ; W = (W0 + f S) eta(tau)^-2 ; f^2 = 2 so that V0 = 0 at S=0 (G_tau=0).
def V(t,S,Q,k):
    y=mp.im(t); f=mp.sqrt(2)
    def Gf(tt,ss,qq,sb=None,qb=None,tb=None):
        pass
    return None
# finite-difference evaluation using real coordinates
def Gfun(x,k):  # x = [tr,ti,Sr,Si,Qr,Qi]
    t=mp.mpc(x[0],x[1]); S=mp.mpc(x[2],x[3]); Q=mp.mpc(x[4],x[5]); y=x[1]
    W=(1+mp.sqrt(3)*S)*mp.eta(t)**(-2)   # D647 deviation D1: f = sqrt3
    K=-mp.log(2*y)+abs(S)**2+abs(Q)**2/(2*y)**k
    return K+mp.log(abs(W)**2)
def Vfun(x,k,h=mp.mpf('1e-7')):
    # holomorphic derivatives d/dz = (d/dx - i d/dy)/2 ; metric G_{a bbar} = d^2 G/dz_a dzbar_b
    n=3; g=lambda xx: Gfun(xx,k)
    def d(xx,i,s):  # partial wrt real coordinate i
        a=list(xx); b=list(xx); a[i]+=h; b[i]-=h; return (g(a)-g(b))/(2*h)
    Gz=[ (d(x,2*a,1)-1j*d(x,2*a+1,1))/2 for a in range(n)]
    M=mp.matrix(n,n)
    for a in range(n):
        for b in range(n):
            # d/dz_a d/dzbar_b = 1/4 (dx_a - i dy_a)(dx_b + i dy_b)
            def dd(i,j):
                hh=mp.mpf('1e-5'); xx=list(x)
                def sh(di,dj):
                    z=list(xx); z[i]+=di; z[j]+=dj; return g(z)
                return (sh(hh,hh)-sh(hh,-hh)-sh(-hh,hh)+sh(-hh,-hh))/(4*hh*hh)
            M[a,b]=(dd(2*a,2*b)+1j*dd(2*a,2*b+1)-1j*dd(2*a+1,2*b)+dd(2*a+1,2*b+1))/4
    Mi=M**-1
    val=sum(Mi[b,a]*Gz[a]*mp.conj(Gz[b]) for a in range(n) for b in range(n))
    return mp.e**g(x)*(val-3)
mp.mp.dps=30
for k in (0,1):
    x0=[0,1,0,0,0,0]
    V0=Vfun(x0,k)
    q=mp.mpf('1e-3'); xq=[0,1,0,0,q,0]
    Vq=Vfun(xq,k)
    m32sq=mp.e**Gfun(x0,k)
    KQQ=1/(2**k)
    mQ2=(Vq-V0)/(q**2*KQQ)
    print(f"k={k}: V0/m3/2^2 = {mp.nstr(mp.re(V0)/m32sq,4)}, m_Q^2/m3/2^2 = {mp.nstr(mp.re(mQ2)/m32sq,5)}",flush=True)
