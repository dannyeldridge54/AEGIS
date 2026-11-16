"""D862 (locked PREREG_D862). alpha' control at string-size tori. AI-assisted."""
import numpy as np, math
from scipy.special import zeta
MP=2.435e18; chi=-96; xi=-chi*zeta(3)/(2*(2*math.pi)**3)
def ralpha(g,a1,a2,a3): VE=a1*a2*a3*g**-1.5; return xi*g**-1.5/(2*VE)
print(f"xi={xi:.4f}; benchmark r_alpha'={ralpha(0.232,40.8,1,1):.4f}")
for A in (1,2,3): print(f"e^(-2 pi A) at A={A}: {math.exp(-2*math.pi*A):.2e}")
G=np.logspace(math.log10(0.05),math.log10(0.5),25)
for Amin in (2,3):
    A=np.logspace(math.log10(Amin),5,60)
    g,a1,a2,a3=np.meshgrid(G,A,A,A,indexing='ij')
    ImS=1/(2*math.sqrt(2)*math.pi*g); Ms=g**0.25*MP/np.sqrt(4*math.pi*a1*a2*a3); T=[a2*a3/g,a1*a3/g,a1*a2/g]
    for f in (1.0,4*math.pi**2):
        for sig in (1.0,0.5,0.25):
            c1=(ImS*f*a1>=750)&(ImS*f*a1<=975); c34=np.zeros_like(c1)
            for Tk in T:
                M=Ms*np.exp(-2*math.pi*sig*Tk); c34|=(Tk>=2)&(Tk<=14.7)&(M>=6e10)&(M<=5e13)
            ok=c1&c34; n=int(ok.sum())
            msg=f"A_min={Amin} f={'1   ' if f==1 else '4pi2'} sigma={sig}: pass={n}"
            if n:
                ra=ralpha(g,a1,a2,a3)[ok]; amin=np.minimum(np.minimum(a1,a2),a3)[ok]
                i=tuple(np.argwhere(ok)[0])
                msg+=f" | max r_alpha'={ra.max():.4f}, min A={amin.min():.2f}; e.g. g_s={g[i]:.3f} A=({a1[i]:.1f},{a2[i]:.2f},{a3[i]:.2f})"
            print(msg)
