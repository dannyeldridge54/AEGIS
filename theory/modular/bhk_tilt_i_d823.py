"""D823 (locked PREREG_D823). AI-assisted."""
import math, sys
sys.path.insert(0,'theory/modular')
src=open('theory/modular/running_d632.py').read().splitlines()
exec('\n'.join(src[:41]))
from inflaton_ad_d790 import Ese
Ei=Ese(0.0,1.0)
def V(phi,C):
    y=math.exp(s2*phi); x=Iy(y)**2; return x/(x+1)*(1+C*(Ese(0.0,y)-Ei))
for C in (0.0,2e-7,4e-7,6e-7,8e-7,1e-6,1.5e-6):
    B=background(C)
    for Ns in (46.08,49.21):
        S=[-0.1,-0.05,0,0.05,0.1]; out=[spectra(B,Ns,math.exp(x)) for x in S]; lp=[math.log(o[0]) for o in out]
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]; a=(ns[2]-ns[0])/0.1; r=out[2][1]/out[2][0]
        print(f"C={C:.1e} N*={Ns}: y*={out[2][2]:.2f} n_s={ns[1]:.4f} r={r:.3e} alpha_s={a:.2e}",flush=True)
