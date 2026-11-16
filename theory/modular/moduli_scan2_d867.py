"""D867 (locked PREREG_D867). Corrected-mapping moduli scan. AI-assisted."""
import numpy as np, math
MP=2.435e18
G=np.logspace(-3,math.log10(0.5),30); A=np.logspace(0,5,60)
g,a1,a2,a3=np.meshgrid(G,A,A,A,indexing='ij')
ImS=1/(2*math.sqrt(2)*math.pi*g); T=[a2*a3/g,a1*a3/g,a1*a2/g]
Ms=g**0.25*MP/np.sqrt(4*math.pi*a1*a2*a3); amin=np.minimum(np.minimum(a1,a2),a3)
for on in (True,False):
    lo,hi=(563,731) if on else (750,975)
    c1=(ImS*T[0]>=lo)&(ImS*T[0]<=hi); c2=(a2*a3>=2e4*g) if on else np.ones_like(c1)
    for k in range(3):
        for sig in (1.0,0.5,0.25):
            c3=(T[k]>=2)&(T[k]<=14.7); M=Ms*np.exp(-2*math.pi*sig*T[k]); c4=(M>=6e10)&(M<=5e13)
            ok=c1&c2&c3&c4; n=int(ok.sum()); tag=f"antiD3={'on ' if on else 'off'} racetrack T{k+1} sigma={sig}: pass={n}"
            if n:
                i=tuple(np.argwhere(ok)[np.argmax(amin[ok])]); tag+=f" | max min(A)={amin[ok].max():.2f}; e.g. g_s={g[i]:.4f} A=({a1[i]:.1f},{a2[i]:.1f},{a3[i]:.1f}) ImT={T[k][i]:.2f} M={M[i]:.1e} Ms={Ms[i]:.1e}"
            else:
                tag+=f" | C1 {int(c1.sum())}, C1&C2 {int((c1&c2).sum())}, C1&C2&C3 {int((c1&c2&c3).sum())}"
            print(tag)
