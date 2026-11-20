import numpy as np
m=np.array([0.51099895,105.6583755,1776.93]); v=np.sqrt(m)
C=np.roll(np.eye(3),1,axis=0); F=np.exp(-2j*np.pi*np.outer(range(3),range(3))/3)/np.sqrt(3)
# circulant with eigenvalues sqrt(m_k): S0 = F^dag diag(v) F
S0=F.conj().T@np.diag(v)@F; a=v.mean()
assert np.allclose(np.sort(np.linalg.svd(S0,compute_uv=False)**2),m)
Q=lambda mm: mm.sum()/np.sqrt(mm).sum()**2
Q0=Q(m); rng=np.random.default_rng(7); N=200000
def run(eps):
    mag=np.exp(rng.uniform(np.log(1/3),np.log(3),(N,3,3))); ph=np.exp(2j*np.pi*rng.random((N,3,3)))
    S=S0[None]+eps*a*mag*ph; s=np.linalg.svd(S,compute_uv=False)**2
    return np.abs(s.sum(1)/np.sqrt(s).sum(1)**2-Q0)
d=run(0.02395); tol=2.3e-5; f=(d<=tol).mean()
print(f"Q0={Q0:.7f}  eps=0.02395: median|dQ|={np.median(d):.3e}  f(|dQ|<=2.3e-5)={f:.4f} -> {'COMPATIBLE' if f>=0.05 else 'INCOMPATIBLE'}")
for e in (1e-3,3e-4,1e-4,3e-5):
    print(f"  eps={e:.0e}: median|dQ|={np.median(run(e)):.2e}")
