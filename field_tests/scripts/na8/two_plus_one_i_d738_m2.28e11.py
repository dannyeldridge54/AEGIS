"""D738 (locked PREREG_D738). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_2p1_d725.py').read(); exec(s[s.index('import cmath'):s.index('rho=complex')])
h=1e-6; t0=1j; MP=2.435e18; m=2.28e11; gs=106.75; mnu=0.05e-9; v=174.
for c in (0.3,1,3):
    M0=Mphys(t0,c); S,U,res=takagi(M0); dM=(Mphys(t0*(1+h),c)-Mphys(t0*(1-h),c))/(2*h); P=U.conj().T@dM@U.conj()
    o=np.argsort(S); S=S[o]; P=P[np.ix_(o,o)]
    dMM=(S[1]-S[0])/S[0]
    print(f"c={c}: SV={np.round(S,6)} residual {res:.1e}; lightest pair dM/M={dMM:.4f}; |P|=\n{np.round(np.abs(P),5)}")
    for dl in (1e-4,1e-5):
        Sd=np.sort(np.linalg.svd(Mphys(t0*(1+dl),c),compute_uv=False)); print(f"   delta={dl:g}: shifts/delta={np.round((Sd-S)/dl,5)}")
    for x in (0.2,0.33,0.45):
        sc=x*m/S[0]; xs=S*sc/m; Gt=0; ch=[]
        for a in range(3):
            for b in range(a,3):
                if xs[a]+xs[b]>=1: continue
                g=math.sqrt(2)*abs(P[a,b])*sc/MP
                if a==b: G=g*g*m*(1-4*xs[a]**2)**0.5/(16*math.pi)
                else:
                    lam=(1-(xs[a]+xs[b])**2)*(1-(xs[a]-xs[b])**2); G=g*g*m*math.sqrt(lam)/(8*math.pi)
                if G>1e-40: Gt+=G; ch.append(f"{a}{b}")
        TR=(90/(math.pi**2*gs))**0.25*math.sqrt(Gt*MP)
        M1=S[0]*sc; GN=mnu*M1**2/(8*math.pi*v**2); xx=dMM*M1/GN; e=xx/(1+xx*xx); Y=(8/23)*(3/4)*(TR/m)*2*e
        print(f"   M1/m={x}: masses/m={np.round(xs,3)}, channels {ch}, T_R={TR:.2e} GeV, x=dM/Gamma_N={xx:.1e}, eps={e:.1e}, Y_B={Y:.2e} {'PASS' if Y>=8.75e-11 else 'fail'}")
