"""D835 (locked PREREG_D835): SERAPIS-E + anti-D3 term, exact MS (D692 code, V replaced). MS solver = running_d632.py lines 13-41 verbatim. AI-assisted."""
import math, numpy as np
from scipy.special import kv, zeta
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
src=open(__file__.replace('antiD3_serapis_e_d835','running_d632')).read().split('\n')
s2=math.sqrt(2)
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,31)]
def Ese(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    for n in range(1,31): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
Er=Ese(0.5,math.sqrt(3)/2)
def lneta4(x,y):
    q=complex(math.exp(-2*math.pi*y)*math.cos(2*math.pi*x),math.exp(-2*math.pi*y)*math.sin(2*math.pi*x))
    return -math.pi*y/3+4*sum(math.log(abs(1-q**n)) for n in range(1,31))
def Dl(x,y): return -math.log(y)-lneta4(x,y)
Dr=Dl(0.5,math.sqrt(3)/2)
def V(phi,Ck):
    C,k=Ck; y=math.exp(s2*phi); e=Ese(0.5,y)-Er; return e/(e+1)*(1+C*e)+4*k*(Dl(0.5,y)-Dr)
def dlnV(phi,e,h=1e-5): return (math.log(V(phi+h,e))-math.log(V(phi-h,e)))/(2*h)
exec('\n'.join(src[11:41]).replace('math.log(40)','math.log(25)'))
print(f"check B(i)=-2Dl(i)-2ln2 = {-2*Dl(0,1)-2*math.log(2):.4f} (D831 -3.4957)")
C=1.0e-6
for k in (0.0,0.5e-4,1e-4,2.07e-4):
    B=background((C,k))
    for Ns in (48.4,49.9):
        S=[-0.1,-0.05,0,0.05,0.1]; out=[spectra(B,Ns,math.exp(x)) for x in S]
        lp=[math.log(o[0]) for o in out]
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
        a=(ns[2]-ns[0])/0.1; r=out[2][1]/out[2][0]; ys=out[2][2]
        e=Ese(0.5,ys)-Er; wall=4*k*(Dl(0.5,ys)-Dr); bhk=C*e
        e25=Ese(0.5,25)-Er; w25=4*k*(Dl(0.5,25)-Dr)
        hx=1e-3; dxx=4*k*(Dl(0.5+hx,ys)-2*Dl(0.5,ys)+Dl(0.5-hx,ys))/hx**2
        print(f"k={k:.2e} N*={Ns}: y*={ys:.2f} n_s={ns[1]:.4f} r={r:.3e} alpha_s={a:.3e} | wall/BHK at y*={wall/bhk if bhk else float('nan'):.3f}, at y=25={w25/(C*e25):.3f} | d2x V_add={dxx:.2e}",flush=True)
