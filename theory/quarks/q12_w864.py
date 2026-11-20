"""Q12 (PREREG_Q12_W864_SPLIT)."""
import numpy as np, sys
from scipy.optimize import minimize
sys.argv=['x']; src=open('theory/quarks/q8_ckm_split.py').read().split('# validation at omega')[0]; ns={}; exec(src,ns)
Y2,w=ns['Y2'],ns['w']
def forms(t):
    Y1,Y2_,Y3=Y2(t)/Y2(t)[0]
    Y4=np.array([Y1*Y1-Y2_*Y3,Y3*Y3-Y1*Y2_,Y2_*Y2_-Y1*Y3])
    Y6=np.array([Y1**3+2*Y1*Y2_*Y3,Y1**2*Y2_+2*Y2_**2*Y3,Y1**2*Y3+2*Y3**2*Y2_])
    Y6p=np.array([Y3**3+2*Y1*Y2_*Y3,Y3**2*Y1+2*Y1**2*Y2_,Y3**2*Y2_+2*Y2_**2*Y1])
    Y8=(Y1**2+2*Y2_*Y3)*np.array([Y1*Y1-Y2_*Y3,Y3*Y3-Y1*Y2_,Y2_*Y2_-Y1*Y3])
    Y8p=(Y3**2+2*Y1*Y2_)*np.array([Y2_*Y2_-Y1*Y3,Y1*Y1-Y2_*Y3,Y3*Y3-Y1*Y2_])
    a=lambda v:np.array([v[0],v[2],v[1]]); b=lambda v:np.array([v[1],v[0],v[2]]); c=lambda v:np.array([v[2],v[1],v[0]])
    return a(Y8),a(Y8p),b(Y6),b(Y6p),c(Y4)
def mats(F,p):  # p: r1,r2,|g|,argg,|f|,argf
    y8,y8p,y6,y6p,y4=F; g=p[:,2]*np.exp(1j*p[:,3]); f=p[:,4]*np.exp(1j*p[:,5]); n=len(p)
    M=np.stack([y8[None]+f[:,None]*y8p[None],y6[None]+g[:,None]*y6p[None],np.broadcast_to(y4,(n,3))],1)
    return M*np.stack([np.ones(n),p[:,0],p[:,1]],1)[:,:,None]
rng=np.random.default_rng(3)
F0=forms(w); sv=np.linalg.svd(mats(F0,np.array([[1.3,0.7,1.1,0.4,0.8,2.0]]))[0],compute_uv=False); ok=sv[1]/sv[0]<1e-10
print('VALIDATION','PASS' if ok else 'FAIL',f'sv2/sv1={sv[1]/sv[0]:.1e}')
T=dict(ms_mb=0.0199,md_mb=1.00e-3,mc_mt=3.72e-3,mu_mt=7.6e-6,Vus=0.2250,Vcb=0.0418,Vub=0.00369,J=3.08e-5)
TOL=dict(ms_mb=1.5,md_mb=1.5,mc_mt=1.5,mu_mt=1.5,Vus=1.1,Vcb=1.2,Vub=1.3,J=1.5)
def obs(Fd,Fu,pd,pu):
    U={};mm={}
    for k,F,p in (('d',Fd,pd),('u',Fu,pu)):
        M=mats(F,p); e,V=np.linalg.eigh(np.conj(np.swapaxes(M,1,2))@M); mm[k]=np.sqrt(np.abs(e)); U[k]=V
    V=np.conj(np.swapaxes(U['u'],1,2))@U['d']; A=np.abs(V)
    return dict(ms_mb=mm['d'][:,1]/mm['d'][:,2],md_mb=mm['d'][:,0]/mm['d'][:,2],mc_mt=mm['u'][:,1]/mm['u'][:,2],mu_mt=mm['u'][:,0]/mm['u'][:,2],
        Vus=A[:,0,1],Vcb=A[:,1,2],Vub=A[:,0,2],J=np.abs(np.imag(V[:,0,1]*V[:,1,2]*np.conj(V[:,0,2])*np.conj(V[:,1,1]))))
chi=lambda o: sum((np.log(np.maximum(o[k],1e-30)/T[k])/np.log(TOL[k]))**2 for k in T)
LO=np.array([1/3,1/3,1/3,-np.pi,1/3,-np.pi]); HI=np.array([3,3,3,np.pi,3,np.pi])
def sample(N):
    x=rng.random((N,6)); p=LO+x*(HI-LO); p[:,[0,1,2,4]]=np.exp(np.log(1/3)+x[:,[0,1,2,4]]*np.log(9)); return p
def search(Fd,Fu,label):
    N=200000; pd,pu=sample(N),sample(N); c=chi(obs(Fd,Fu,pd,pu)); best=None
    f=lambda z: chi(obs(Fd,Fu,np.clip(z[:6],LO,HI)[None],np.clip(z[6:],LO,HI)[None]))[0]
    for i in np.argsort(c)[:20]:
        r=minimize(f,np.r_[pd[i],pu[i]],method='Nelder-Mead',options=dict(maxiter=9000,xatol=1e-7,fatol=1e-10))
        if best is None or r.fun<best.fun: best=r
    z=np.clip(best.x,np.r_[LO,LO],np.r_[HI,HI]); o={k:float(v[0]) for k,v in obs(Fd,Fu,z[None,:6],z[None,6:]).items()}
    fails=[k for k in T if not (1/TOL[k]<=o[k]/T[k]<=TOL[k])]
    print(f"{label}: chi2={best.fun:.2f} {'PASS' if not fails else 'FAIL'} fails={fails}")
    print('   '+' '.join(f"{k}={o[k]:.3g}({o[k]/T[k]:.2f})" for k in T)); print('   d',np.round(z[:6],3),' u',np.round(z[6:],3))
if ok:
    Fd=forms(-0.484440+0.884238j); search(Fd,Fd,'CONTROL one modulus (rung 1)')
    for m,t in ((8,-0.497988+0.868420j),(9,-0.498207+0.868153j),(10,-0.498421+0.867971j),(13,-0.498737+0.867484j)):
        search(Fd,forms(t),f'SPLIT down rung1, up rung{m}'+(' (post-hoc rung)' if m==13 else ''))
