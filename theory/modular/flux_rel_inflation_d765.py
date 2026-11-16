"""D765 (locked PREREG_D765): D692 with doubled Kahler metric (y=e^phi). MS solver = running_d632.py lines 13-41 verbatim. AI-assisted."""
import math, numpy as np
from scipy.special import kv, zeta
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
src=open(__file__.replace('flux_rel_inflation_d765','running_d632')).read().split('\n')
s2=math.sqrt(2)
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,31)]
def Ese(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    for n in range(1,31): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
Er=Ese(0.5,math.sqrt(3)/2)
def V(phi,C):
    y=math.exp(phi); e=Ese(0.5,y)-Er; return e/(e+1)*(1+C*e)
def dlnV(phi,e,h=1e-5): return (math.log(V(phi+h,e))-math.log(V(phi-h,e)))/(2*h)
exec('\n'.join(src[11:41]).replace('math.log(40)','math.log(25)').replace('/s2','').replace('exp(s2*','exp('))  # DEVIATIONS D1
print(f"E(rho,2)={Er:.7f} (D689: 5.7833593)")
for C in (0.0,6e-7,1e-6,1.3e-6):
    B=background(C)
    for Ns in (48.4,49.9):
        S=[-0.1,-0.05,0,0.05,0.1]; out=[spectra(B,Ns,math.exp(x)) for x in S]
        lp=[math.log(o[0]) for o in out]
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
        a=(ns[2]-ns[0])/0.1; r=out[2][1]/out[2][0]
        print(f"C={C:.1e} N*={Ns}: y*={out[2][2]:.2f} n_s={ns[1]:.4f} r={r:.3e} alpha_s={a:.3e}",flush=True)
