"""D982 (locked PREREG_D982): Boltzmann vs instantaneous non-thermal leptogenesis yield, SERAPIS-E at rho."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kn
MP=2.435e18; gs=106.75; csph=8/23; m=2.2e13; mnu=0.05e-9; v=174.
ratio={0.3:0.082343/0.38817, 1:0.274478/0.38817, 3:0.38817/0.823433}
cases=[(0.3,1e12,3.175e8),(0.3,1e13,3.033e9),(0.3,5e13,2.076e9),(1,1e12,4.287e8),(1,1e13,2.543e9),(3,1e12,9.459e8)]
def Hof(T): return math.sqrt(math.pi**2*gs/90)*T*T/MP
def solve(M,TR,K,eps=1e-6):
    Gphi=Hof(TR); GN=K*Hof(M)
    # units: GeV; variables x=ln a; y = [ln rho_phi a^3, nN a^3, rhoR a^4, nBL a^3] scaled
    H0=1e4*Gphi; rho0=3*MP**2*H0**2
    S=rho0   # scale
    def rhs(x,y):
        a=math.exp(x); rp=(math.exp(y[0])*S/a**3 if y[0]>-690 else 0.0); nN=y[1]*S/a**3; rR=max(y[2],1e-300)*S/a**4
        H=math.sqrt(max(rp+M*nN+rR,1e-300)/(3*MP**2)); T=(30*rR/(math.pi**2*gs))**0.25
        z=M/max(T,1e-30); neq_ratio=(z*z*kn(2,z)/2 if z<600 else 0.0)  # n_N^eq/n_l^eq (2 dof each, approx)
        W=GN/2*neq_ratio
        d0=-Gphi/H if y[0]>-690 else 0.0
        d1=(2*Gphi*rp/m-GN*nN)*a**3/(H*S)
        d2=(Gphi*rp*(1-2*M/m)+GN*M*nN)*a**4/(H*S)
        d3=(eps*GN*nN-W*y[3]*S/a**3)*a**3/(H*S)
        return [d0,d1,d2,d3]
    # integrate until phi and N gone
    xend=math.log(1e4)+ (2/3)*math.log(H0/Gphi)
    sol=solve_ivp(rhs,[0,xend],[0.0,0.0,1e-30,0.0],t_eval=[xend],method='LSODA',rtol=1e-9,atol=[1e-12,1e-40,1e-40,1e-50])
    a=math.exp(sol.t[-1]); rR=sol.y[2,-1]*S/a**4; T=(30*rR/(math.pi**2*gs))**0.25; s=2*math.pi**2*gs*T**3/45
    nBL=sol.y[3,-1]*S/a**3
    left=((math.exp(sol.y[0,-1]) if sol.y[0,-1]>-690 else 0.0)*S/a**3)/rR
    return csph*nBL/s, left, sol.status
def Yinst(TR,eps=1e-6): return csph*0.75*(TR/m)*2*eps
L=[]
# sanity (not a verdict): fast N decay, light N
y,left,st=solve(1e9,1e7,1e6); L.append(f"sanity M=1e9 T_R=1e7 K=1e6: kappa={y/Yinst(1e7):.3f} (phi left {left:.1e}, status {st}) -> {'ok' if 0.7<y/Yinst(1e7)<1.3 else 'SANITY FAIL'}")
print(L[-1],flush=True)
ks=[]
for c,MH,TR in cases:
    ML=ratio[c]*MH
    for lab,M in (("light",ML),("heavy",MH)):
        if M>=m/2: continue
        for K in (1,10,100):
            y,left,st=solve(M,TR,K); k=y/Yinst(TR); ks.append((c,MH,lab,K,k))
            L.append(f"c={c} M_H={MH:.0e} {lab} M={M:.3e} T_R={TR:.3e} K={K}: kappa={k:.4f} (phi left {left:.1e}, status {st})"); print(L[-1],flush=True)
allin=all(0.85<=k<=1.15 for *_,k in ks)
c03=[k for c,MH,lab,K,k in ks if c==0.3 and MH==1e12]
L.append(f"kappa range {min(k for *_,k in ks):.4f}-{max(k for *_,k in ks):.4f}; all in [0.85,1.15]: {allin} -> {'instantaneous yields stand' if allin else 'CORRECTION NOTE (rescale D775 by kappa)'}")
L.append(f"c=0.3, M_H=1e12 rows: min kappa {min(c03):.4f} -> {'passes (kappa>=1.15)' if min(c03)>=1.15 else 'still fails'}")
open('field_tests/results/lepto_boltz_d982.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L[-2:]))
