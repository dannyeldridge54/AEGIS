"""D680 (locked PREREG_D680_RHO_STRIP). AI-assisted."""
import math, numpy as np
srcR=open('theory/modular/rho_running_d634.py').read().splitlines()
endR=[i for i,l in enumerate(srcR) if l.startswith('import numpy as np') and i>40][0]
g={}; exec("\n".join(srcR[:endR]),g)
res={}
for N,eps in ((46.09,(0,0.25e-4,0.5e-4,0.75e-4,1.0e-4,1.25e-4,1.4249e-4)),(49.49,(0,0.25e-4,0.5e-4,0.75e-4,0.9974e-4))):
    res[N]=[]
    for e in eps:
        B=g['background'](e); S=[-0.1,-0.05,0,0.05,0.1]; lp=[]
        for x in S:
            P,Pt,ys=g['spectra'](B,N,math.exp(x)); lp.append(math.log(P))
            if x==0: r=Pt/P; y0=ys
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]; a=(ns[2]-ns[0])/0.1
        res[N].append((ns[1],r)); print(f"N*={N} eps={e:.3e}: y*={y0:.2f} n_s={ns[1]:.5f} r={r:.4e} alpha_s={a:.3e}",flush=True)
for N in res:
    n=np.array([p[0] for p in res[N]]); r=np.array([p[1] for p in res[N]])
    c=np.polyfit(n-0.97,r,2); print(f"edge N*={N}: r = {c[2]:.4e} + {c[1]:.4e}(n_s-0.97) + {c[0]:.4e}(n_s-0.97)^2 ; n_s range {n.min():.4f}-{n.max():.4f}")
    res[N]=(c,n.min(),n.max())
lo=max(res[46.09][1],res[49.49][1]); hi=min(res[46.09][2],res[49.49][2])
w=[]
for ns in np.linspace(lo,hi,20):
    r1=np.polyval(res[46.09][0],ns-0.97); r2=np.polyval(res[49.49][0],ns-0.97); w.append(abs(r1-r2)/((r1+r2)/2))
print(f"overlap n_s {lo:.4f}-{hi:.4f}: max fractional width in r at fixed n_s = {max(w):.3f}")

import numpy as np
ci={46.08:(0.26122,1.7393e-2,5.3360e-4),49.21:(0.24413,1.5347e-2,4.4164e-4)}
off=[]
for ns in np.linspace(max(lo,0.9612),min(hi,0.9795),20):
    ru=np.polyval(res[46.09][0],ns-0.97); rl=np.polyval(res[49.49][0],ns-0.97)
    iu=np.polyval(ci[46.08],ns-0.97); il=np.polyval(ci[49.21],ns-0.97)
    off.append(max(abs(ru-iu)/iu,abs(rl-il)/il))
print(f"max offset rho vs tau=i edges at fixed n_s = {max(off):.3f}")
