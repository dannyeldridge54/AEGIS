"""Q2 (PREREG_Q2_KOIDE_QUARKS): Koide Q, Brannen A, delta for quark triplets at M_Z."""
import numpy as np
P=2*np.pi/3
def kq(m):
    v=np.sqrt(m); mu=v.mean(axis=-1)
    Q=m.sum(-1)/v.sum(-1)**2
    k=np.arange(3); c=((v/mu[...,None]-1)*np.exp(-1j*2*np.pi*k/3)).sum(-1)
    A=2*np.abs(c)/3; d=np.mod(np.angle(c),P)
    return Q,A,d
# convention check on leptons (e, mu, tau) must give delta ~ 2/9 mod 2pi/3
Ql,Al,dl=kq(np.array([0.51099895,105.6583755,1776.93]))
print(f"leptons Q={Ql:.7f} A={Al:.6f} delta={dl:.6f} (2/9={2/9:.6f}; conv. check)")
rng=np.random.default_rng(1); N=200000
T={'up (u,c,t)':[(1.29e-3,.20e-3),(.629,.012),(169,1.1)],'down (d,s,b)':[(2.80e-3,.20e-3),(55.7e-3,1.3e-3),(2.794,.034)]}
for n,t in T.items():
    m=np.stack([rng.normal(a,s,N) for a,s in t],-1); m=m[(m>0).all(-1)]
    Q,A,d=kq(m); Q0,A0,d0=kq(np.array([a for a,_ in t]))
    dd=np.mod(d-2/9+P/2,P)-P/2
    print(f"{n}: Q={Q0:.4f}±{Q.std():.4f} pull(2/3)={(Q0-2/3)/Q.std():+.1f}σ  A={A0:.4f}  delta={d0:.4f}±{d.std():.4f} pull(2/9)={np.mean(dd)/dd.std():+.1f}σ")
