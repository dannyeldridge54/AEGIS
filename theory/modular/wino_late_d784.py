"""D784 (locked PREREG_D784). AI-assisted."""
import math, numpy as np
sl=1.6e-27+0.5*1.1e-26
def omega(M2,T,nonth=True):
    Y=1.9e-12*T/1e10; Onth=2.74e8*M2*Y if nonth else 0; Oth=0.12*(M2/2900)**2; return Onth+Oth,Onth,Oth
print("K4 (D732 T_R=3.2e8, M2=660):", f"{omega(660,3.2e8)[0]:.3f} (D732: 0.017)")
Ms=np.linspace(670,2900,2231)
for T in (1e5,1e6,1e7):
    ok=[]
    for M in Ms:
        tot,on,oth=omega(M,T); f=tot/0.12; fmax=math.sqrt(4e-28*(M/1000)**2/sl)
        if f<=fmax: ok.append(M)
    tot,on,oth=omega(700,T)
    print(f"T2={T:.0e}: Y32={1.9e-12*T/1e10:.1e}, at M2=0.7TeV Omega_nth={on:.1e} Omega_th={oth:.3f}; Einasto-allowed window: {min(ok)/1000:.2f}-{max(ok)/1000:.2f} TeV" if ok else f"T2={T:.0e}: none")
print("Thermal fraction at window ends: f(0.67)=%.3f, f(1.85)=%.3f"%((0.67/2.9)**2,(1.85/2.9)**2))
