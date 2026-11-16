"""D860 (locked PREREG_D860). Moduli feasibility scan. AI-assisted."""
import numpy as np, math
MP=2.435e18
G=np.logspace(math.log10(0.05),math.log10(0.5),25); A=np.logspace(0,5,60)
g,a1,a2,a3=np.meshgrid(G,A,A,A,indexing='ij')
ImS=1/(2*math.sqrt(2)*math.pi*g)
Ms=g**0.25*MP/np.sqrt(4*math.pi*a1*a2*a3)
T=[a2*a3/g,a1*a3/g,a1*a2/g]
for adon in (True,False):
    lo,hi=(563,731) if adon else (750,975)
    for f in (1.0,4*math.pi**2):
        for sig in (1.0,0.5,0.25):
            c1=(ImS*f*a1>=lo)&(ImS*f*a1<=hi); c5=np.ones_like(c1)
            c2=(a2*a3>=2e4*g) if adon else np.ones_like(c1)
            c3=np.zeros_like(c1); c34=np.zeros_like(c1)
            for Tk in T:
                ok3=(Tk>=2)&(Tk<=14.7); M=Ms*np.exp(-2*math.pi*sig*Tk); ok4=(M>=6e10)&(M<=5e13)
                c3|=ok3; c34|=ok3&ok4
            allp=c1&c2&c34&c5; n=int(allp.sum())
            base=c1&c5
            tag=f"antiD3={'on ' if adon else 'off'} f={'1   ' if f==1 else '4pi2'} sigma={sig}: pass={n}"
            if n:
                i=tuple(np.argwhere(allp)[0]); print(tag, f"| e.g. g_s={g[i]:.3f} A=({a1[i]:.1f},{a2[i]:.1f},{a3[i]:.1f}) Ms={Ms[i]:.2e}")
            else:
                print(tag, f"| among C1: fail C2 {int((base&~c2).sum())}, fail C3 {int((base&c2&~c3).sum())}, C3 ok but fail C4 {int((base&c2&c3&~c34).sum())} (of {int(base.sum())})")
