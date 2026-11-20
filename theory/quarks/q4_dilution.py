import numpy as np
MP=2.435e18; TR=1.34e9; Ns=55
H=np.pi*MP*np.sqrt(2.1e-9*4.46e-4/2); print(f"H_inf = {H:.3e} GeV")
def Tdec(m):
    G=m**3/(4*np.pi*MP**2); T=(90/(np.pi**2*10.75))**.25*np.sqrt(G*MP)
    return np.where(T>1,(90/(np.pi**2*80))**.25*np.sqrt(G*MP),T)
for p0 in (0.1,1.0):
    ms=np.logspace(4,np.log10(H),400); T=Tdec(ms); D=np.maximum(1,TR*p0**2/6/T)
    dns=np.abs(2*(-np.log(D)/3)/Ns**2)
    ok=(T>=5e-3)&(D<=1e3)&(dns<=0.003)
    w=ms[ok]
    print(f"phi0={p0}: T_dec(1e4 GeV)={Tdec(1e4):.2e} GeV; D range {D.min():.2e}-{D.max():.2e}; window: "+(f"{w.min():.2e}-{w.max():.2e} GeV" if w.size else "NONE"))
    for m in (1e5,1e7,1e9,1e11,H): t=Tdec(m); d=max(1,TR*p0**2/6/t); print(f"   m={m:.1e}: Tdec={t:.2e} D={d:.2e} dns={abs(2*np.log(d)/3/Ns**2):.4f}")
