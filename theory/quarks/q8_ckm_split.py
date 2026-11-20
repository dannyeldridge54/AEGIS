"""Q8 (PREREG_Q8_CKM_SPLIT): A4 near-omega quark matrices (2212.13336 Eq.23) on split rungs."""
import numpy as np, mpmath as mp
from scipy.optimize import minimize
mp.mp.dps=25; w=complex(mp.e**(2j*mp.pi/3))
def dlogeta(t):
    q=mp.e**(2j*mp.pi*t); return (mp.pi*1j/12)*(1-24*mp.nsum(lambda n: n*q**n/(1-q**n),[1,mp.inf]))
def Y2(t):
    t=mp.mpc(t); W=mp.e**(2j*mp.pi/3)
    a,b,c,d=dlogeta(t/3),dlogeta((t+1)/3),dlogeta((t+2)/3),dlogeta(3*t)
    return np.array([complex((1j/(2*mp.pi))*(a+b+c-27*d)),complex((-1j/mp.pi)*(a+W**2*b+W*c)),complex((-1j/mp.pi)*(a+W*b+W**2*c))])
def rows(t):
    Y1,Y2_,Y3=Y2(t)/Y2(t)[0]
    Y4=np.array([Y1*Y1-Y2_*Y3,Y3*Y3-Y1*Y2_,Y2_*Y2_-Y1*Y3])
    Y6=np.array([Y1**3+2*Y1*Y2_*Y3,Y1**2*Y2_+2*Y2_**2*Y3,Y1**2*Y3+2*Y3**2*Y2_])
    Y6p=np.array([Y3**3+2*Y1*Y2_*Y3,Y3**2*Y1+2*Y1**2*Y2_,Y3**2*Y2_+2*Y2_**2*Y1])
    P=lambda v:np.array([v[0],v[2],v[1]])   # (Y1,Y3,Y2)
    return P(Y6),P(Y6p),np.array([Y4[1],Y4[0],Y4[2]]),np.array([Y3,Y2_,Y1])
# validation at omega
r6,r6p,r4,r2=rows(w)
M0=np.vstack([r6+1.0*r6p,r4,r2]); sv=np.linalg.svd(M0,compute_uv=False)
ok=sv[1]/sv[0]<1e-10 and np.allclose((r6+r6p)/(r6+r6p)[0],[1,-2*w**2,-2*w],atol=1e-10) and np.allclose(r4/r4[1],[-w/2,1,w**2],atol=1e-10) and np.allclose(r2/r2[2],[-w**2/2,w,1],atol=1e-10)
print('VALIDATION', 'PASS' if ok else 'FAIL', f'sv2/sv1={sv[1]/sv[0]:.1e}')
T=dict(ms_mb=0.0199,md_mb=1.00e-3,mc_mt=3.72e-3,mu_mt=7.6e-6,Vus=0.2250,Vcb=0.0418,Vub=0.00369,J=3.08e-5)
TOL=dict(ms_mb=1.5,md_mb=1.5,mc_mt=1.5,mu_mt=1.5,Vus=1.1,Vcb=1.2,Vub=1.3,J=1.5)
def mats(R,p):  # p (...,4): r1,r2,|g|,arg g
    r6,r6p,r4,r2=R; g=p[...,2]*np.exp(1j*p[...,3])
    M=np.stack([r6[None,:]+g[:,None]*r6p[None,:],np.broadcast_to(r4,(len(g),3)),np.broadcast_to(r2,(len(g),3))],1)
    return M*np.stack([np.ones_like(p[...,0]),p[...,0],p[...,1]],1)[:,:,None]
def obs(Rd,Ru,pd,pu):
    out={}
    U={}
    for k,R,p in (('d',Rd,pd),('u',Ru,pu)):
        M=mats(R,p); H=np.conj(np.swapaxes(M,1,2))@M; e,V=np.linalg.eigh(H); m=np.sqrt(np.abs(e)); U[k]=V
        out['m'+k]=m
    V=np.conj(np.swapaxes(U['u'],1,2))@U['d']; A=np.abs(V)
    o=dict(ms_mb=out['md'][:,1]/out['md'][:,2],md_mb=out['md'][:,0]/out['md'][:,2],mc_mt=out['mu'][:,1]/out['mu'][:,2],mu_mt=out['mu'][:,0]/out['mu'][:,2],
           Vus=A[:,0,1],Vcb=A[:,1,2],Vub=A[:,0,2],J=np.abs(np.imag(V[:,0,1]*V[:,1,2]*np.conj(V[:,0,2])*np.conj(V[:,1,1]))))
    return o
def chi(o): return sum((np.log(np.maximum(o[k],1e-30)/T[k])/np.log(TOL[k]))**2 for k in T)
LO,HI=np.array([1/3,1/3,1/3,-np.pi]),np.array([3,3,3,np.pi])
def sample(rng,N):
    x=rng.random((N,4)); p=np.empty_like(x); p[:,:3]=np.exp(np.log(1/3)+x[:,:3]*np.log(9)); p[:,3]=-np.pi+2*np.pi*x[:,3]; return p
def search(Rd,Ru,label,rng):
    N=200000; pd,pu=sample(rng,N),sample(rng,N); c=chi(obs(Rd,Ru,pd,pu)); idx=np.argsort(c)[:20]
    best=None
    def f(z):
        a,b=np.clip(z[:4],LO,HI)[None],np.clip(z[4:],LO,HI)[None]; return chi(obs(Rd,Ru,a,b))[0]
    for i in idx:
        r=minimize(f,np.r_[pd[i],pu[i]],method='Nelder-Mead',options=dict(maxiter=6000,xatol=1e-7,fatol=1e-10))
        if best is None or r.fun<best.fun: best=r
    z=np.clip(best.x,np.r_[LO,LO],np.r_[HI,HI]); o={k:float(v[0]) for k,v in obs(Rd,Ru,z[None,:4],z[None,4:]).items()}
    fails=[k for k in T if not (1/TOL[k] <= o[k]/T[k] <= TOL[k])]
    print(f"{label}: chi2={best.fun:.2f} {'PASS' if not fails else 'FAIL'} fails={fails}")
    print('   '+' '.join(f"{k}={o[k]:.3g}({o[k]/T[k]:.2f})" for k in T))
    print('   down r1,r2,|g|,argg =',np.round(z[:4],3),' up =',np.round(z[4:],3))
if ok:
    rng=np.random.default_rng(11)
    Rd=rows(-0.484440+0.884238j)
    search(Rd,Rd,'CONTROL one modulus (both rung 1)',rng)
    for m,t in ((8,-0.497988+0.868420j),(9,-0.498207+0.868153j),(10,-0.498421+0.867971j)):
        search(Rd,rows(t),f'SPLIT down rung1, up rung{m}',rng)
