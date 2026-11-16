"""D728 (locked PREREG_D728). AI-assisted."""
import math, numpy as np
MP=2.435e18; m=1.9e11; mnu=0.05e-9; v=174.; gs=106.75; lam=math.sqrt(2)*1.2635
for xM in (0.1,0.2,0.33,0.45):
    M=xM*m; G=(M*lam/MP)**2*m*(1-4*xM*xM)**0.5/(8*math.pi); T=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
    GN=mnu*M**2/(8*math.pi*v**2); eDI=3*M*mnu/(16*math.pi*v**2)
    print(f"M/m={xM}: M={M:.2e}, T_R={T:.3e} GeV, T_R/M={T/M:.1e}, Gamma_N/M={GN/M:.2e}, eps_DI={eDI:.2e}")
    ok=[]
    for r in list(np.logspace(-8,np.log10(0.5),16))+[0.08,0.2,0.5]:
        x=r*M/GN; e=x/(1+x*x); Y=(8/23)*(3/4)*(T/m)*2*e
        if Y>=8.75e-11 and T>=150: ok.append(r)
        print(f"   dM/M={r:.2e}: x={x:.2e}, eps={e:.2e} (eps/eps_DI={e/eDI:.1e}), Y_B={Y:.2e} {'PASS' if Y>=8.75e-11 else 'fail'}")
    print(f"   passing dM/M: {min(ok):.1e} .. {max(ok):.1e}" if ok else "   none pass")
