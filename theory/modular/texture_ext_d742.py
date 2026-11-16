"""D742 (locked PREREG_D742). AI-assisted. Vectorised grid scan."""
import cmath, math, itertools, numpy as np
s=open('theory/modular/tr_takagi_d721.py').read(); exec(s[s.index('def sig'):s.index('def takagi')])
Y=Yd(1j); Y4=np.array([2*Y[0]*Y[1], Y[0]**2-Y[1]**2]); Robs=7.42e-5/2.5e-3
def stats(Ms):
    m=np.sort(np.linalg.svd(Ms,compute_uv=False),axis=-1)
    dlo=m[...,1]**2-m[...,0]**2; dhi=m[...,2]**2-m[...,1]**2
    NO=dlo<dhi; R=np.minimum(dlo,dhi)/np.maximum(dlo,dhi)
    sc=np.sqrt(2.5e-3/np.where(NO,dhi,m[...,2]**2-m[...,0]**2)); Sig=sc*m.sum(-1)
    ok=NO&(np.abs(R-Robs)<0.1*Robs)&(Sig<=0.064)
    return ok, Sig, m[...,0]/m[...,2]
def build(b,c,d):
    M=np.zeros(b.shape+(3,3),complex)
    M[...,:2,:2]=A(Y)+c[...,None,None]*A(Y4); M[...,:2,2]=b[...,None]*Y; M[...,2,:2]=b[...,None]*Y; M[...,2,2]=d; return M
def grid(n,nph): 
    mag=np.logspace(-2,2,n); ph=np.exp(1j*np.linspace(0,2*np.pi,nph,endpoint=False)); return (mag[:,None]*ph[None,:]).ravel()
for name,(nb,nc,nd,nph) in {"(a) b,d":(40,0,40,8),"(b) b,c":(40,40,0,8),"(c) b,c,d":(25,25,25,6)}.items():
    B=grid(nb,nph); C=grid(nc,nph) if nc else np.array([0j]); D=grid(nd,nph) if nd else np.array([0j])
    b,c,d=[x.ravel() for x in np.meshgrid(B,C,D,indexing='ij')]
    ok,Sig,ml=stats(build(b,c,d)); n=ok.sum()
    msg=f"{name}: {len(b)} points, PASS {n} ({n/len(b):.2e})"
    if n: msg+=f"; best Sigma {Sig[ok].min():.4f} eV, m1/m3 range {ml[ok].min():.3f}-{ml[ok].max():.3f}"
    print(msg)
