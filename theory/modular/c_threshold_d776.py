"""D776 (locked PREREG_D776). D775 code path with a c scan. AI-assisted."""
import math, cmath, itertools, numpy as np
d=math.radians; s12,s13,s23=math.sin(d(33.4)),math.sin(d(8.6)),math.sin(d(49)); c12,c13,c23=[math.sqrt(1-x*x) for x in (s12,s13,s23)]
e=cmath.exp(-1j*d(230))
U=np.array([[c12*c13,s12*c13,s13*e],[-s12*c23-c12*s23*s13/e,c12*c23-s12*s23*s13/e,s23*c13],[s12*s23-c12*c23*s13/e,-c12*s23-s12*c23*s13/e,c23*c13]])
def R12(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,s,0],[-s,c,0],[0,0,1]])
def R13(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def R23(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[1,0,0],[0,c,s],[0,-s,c]])
zs=[complex(a,b) for a in (0.3,0.9,1.5) for b in (-0.5,0,0.5)]
v=174.; mphi=2.2e13; Yobs=8.75e-11; mnu3=0.05e-9
f=lambda x: math.sqrt(x)*(1-(1+x)*math.log((1+x)/x)); g=lambda x: math.sqrt(x)/(1-x)
mphi=2.2e13; Yobs=8.75e-11; mnu3=0.05e-9; v=174.

import numpy as np
cs=[0.3,0.35,0.4,0.5,0.6,0.7,0.85,1.0]; MH=1e12; m1=1e-3
lc=np.log([0.3,1,3]); lt=np.log([3.175e8,4.287e8,9.459e8])
m=np.array([m1,math.sqrt(m1**2+7.42e-5),math.sqrt(m1**2+2.5e-3)])*1e-9
cstar=None
for c in cs:
    TR=float(np.exp(np.interp(np.log(c),lc,lt))); Mp=0.7072*c*MH; Ms=MH; Dm=np.array([Mp,Mp,Ms])
    npass={'pair':0,'single':0}; tot=0
    for z1,z2,z3 in itertools.product(zs,zs,zs):
        R=R12(z1)@R13(z2)@R23(z3)
        Y=1j*U.conj()@np.diag(np.sqrt(m))@R@np.diag(np.sqrt(Dm))/v
        H=Y.conj().T@Y
        h=H[:2,:2].real; th=0.5*math.atan2(2*h[0,1],h[0,0]-h[1,1]); O=np.eye(3); O[:2,:2]=[[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]]
        Y=Y@O; H=Y.conj().T@Y; eps=[]
        for i in range(3):
            s=0
            for j in range(3):
                if j==i or abs(Dm[j]-Dm[i])<1e-6*Dm[i]: continue
                x=Dm[j]**2/Dm[i]**2; s+=(H[i,j]**2).imag/H[i,i].real*(f(x)+g(x))
            eps.append(-s/(8*math.pi))
        tot+=1
        for lab,ev in (('pair',abs(0.5*(eps[0]+eps[1]))),('single',abs(eps[2]))):
            npass[lab]+=(8/23)*(3/4)*(TR/mphi)*2*ev>=Yobs
    fr=max(npass.values())/tot
    print(f"c={c}: T_R={TR:.3e} M_pair={Mp:.2e} pass pair={npass['pair']/tot:.1%} single={npass['single']/tot:.1%}",flush=True)
    if cstar is None and fr>=0.10: cstar=c
P=math.log(10/cstar)/math.log(100) if cstar else 0
print(f"c* = {cstar}; P(c>=c*) under log-uniform [0.1,10] = {P:.2f}")
