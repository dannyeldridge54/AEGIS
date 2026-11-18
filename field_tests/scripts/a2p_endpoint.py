# A2p: LL line+endpoint photon ratio for the wino (2507.15937 Eqs. 2.6-2.13). ESTIMATE, no pass bar.
import sys, math, numpy as np; sys.path.insert(0,'tools')
from scipy.integrate import quad
from janus_astro.sommerfeld import wino_s, ALPHA_W, M_W
a=ALPHA_W; c=4*a/math.pi
def R(M, Delta, v=1e-3):
    s00,s01=wino_s(M,v)
    M00=16*M*s01; Mpm=4*math.sqrt(2)*M*2*s00+8*M*s01
    F0=(M00**2+2*Mpm**2)/(192*M*M); F1=(M00**2-Mpm**2)/(96*M*M)
    Lc=math.log(M_W/(2*M))
    def end(z):
        y=1-z; tJ=y>M_W**2/(4*M*M); tS=y>M_W/(2*M)
        LJ=math.log(M_W/(2*M*math.sqrt(y))); LS=math.log(M_W/(2*M*y))
        L1J=LJ/y*tJ; L1S=LS/y*tS
        return -(2*a/math.pi)*(2*F0*L1J*math.exp(c*LJ**2)+F1*(2*L1J-3*L1S)*math.exp(c*(tJ*LJ**2-0.75*tS*LS**2)))
    pts=[1-M_W**2/(4*M*M),1-M_W/(2*M)]
    I=quad(end,1-Delta,1-1e-12,points=[p for p in pts if p>1-Delta],limit=400)[0]
    return F0,F1,2*(F0+F1),I,1+I/(2*(F0+F1))
if __name__=='__main__':
    sf=wino_s(1000,1e-3,alpha_w=0.0); print('check free (alpha=0) s =',np.round(sf,6))
    for M in (1000,1250,1500,2900):
        for D in (0.05,0.10,0.15):
            F0,F1,L,I,r=R(M,D); print(f'M={M} Delta={D:.2f} F0={F0:.4g} F1={F1:.4g} line(2(F0+F1))={L:.4g} endpoint={I:.4g} R={r:.4f}')
