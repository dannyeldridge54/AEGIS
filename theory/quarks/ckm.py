"""Quark toolkit piece: Yukawa/mass matrices -> masses, CKM, angles, Jarlskog J, delta (PDG convention).
Convention: L = -dbar_R M_d d_L - ubar_R M_u u_L  (left-handed rotations from M^dagger M)."""
import numpy as np
def _left(M):
    w,V=np.linalg.eigh(M.conj().T@M); i=np.argsort(w); return np.sqrt(np.abs(w[i])),V[:,i]
def ckm(Mu,Md):
    mu,Uu=_left(Mu); md,Ud=_left(Md); V=Uu.conj().T@Ud
    a=np.abs(V); s13=a[0,2]; c13=np.sqrt(1-s13**2)
    s12=a[0,1]/c13; s23=a[1,2]/c13
    J=np.imag(V[0,1]*V[1,2]*np.conj(V[0,2])*np.conj(V[1,1]))
    c12,c23=np.sqrt(1-s12**2),np.sqrt(1-s23**2)
    sd=J/(s12*c12*s23*c23*s13*c13**2) if s13>0 else 0.0
    # cos(delta) from |V_ub|... use |V_td| relation for quadrant
    num=a[2,0]**2-(s12*s23)**2-(c12*c23*s13)**2; den=-2*s12*s23*c12*c23*s13
    cd=num/den if den else 1.0
    return dict(m_u=mu,m_d=md,V=V,absV=a,s12=s12,s23=s23,s13=s13,J=J,delta=float(np.arctan2(sd,cd)))
def pdg_matrix(s12,s23,s13,d):
    c12,c23,c13=[np.sqrt(1-x*x) for x in (s12,s23,s13)]; e=np.exp(1j*d)
    return np.array([[c12*c13,s12*c13,s13/e],
        [-s12*c23-c12*s23*s13*e,c12*c23-s12*s23*s13*e,s23*c13],
        [s12*s23-c12*c23*s13*e,-c12*s23-s12*c23*s13*e,c23*c13]])
if __name__=='__main__':
    # self-test: Md = V diag(md) (left-handed) , Mu diagonal -> recover input angles & delta
    s12,s23,s13,d=0.22500,0.04182,0.00369,1.144
    V=pdg_matrix(s12,s23,s13,d); md=np.diag([2.8e-3,55.7e-3,2.794]); Mu=np.diag([1.29e-3,.629,169.])
    Md=md@V.conj().T
    r=ckm(Mu,Md)
    print({k:round(float(r[k]),6) for k in ('s12','s23','s13','J','delta')}, 'masses d', np.round(r['m_d'],5))
    assert abs(r['s12']-s12)<1e-9 and abs(r['s23']-s23)<1e-9 and abs(r['s13']-s13)<1e-9
    assert abs(r['delta']-d)<1e-6; print('selftest OK')
