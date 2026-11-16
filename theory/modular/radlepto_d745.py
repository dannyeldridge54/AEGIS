"""D745 (locked PREREG_D745). AI-assisted."""
import math, cmath, itertools, numpy as np
d=math.radians; s12,s13,s23=math.sin(d(33.4)),math.sin(d(8.6)),math.sin(d(49)); c12,c13,c23=[math.sqrt(1-x*x) for x in (s12,s13,s23)]
e=cmath.exp(-1j*d(230))
U=np.array([[c12*c13,s12*c13,s13*e],[-s12*c23-c12*s23*s13/e,c12*c23-s12*s23*s13/e,s23*c13],[s12*s23-c12*c23*s13/e,-c12*s23-s12*c23*s13/e,c23*c13]])
def R12(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,s,0],[-s,c,0],[0,0,1]])
def R13(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def R23(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[1,0,0],[0,c,s],[0,-s,c]])
mphi=1.9e11; M=0.33*mphi; D=np.array([M,M,10*M]); TR=2.9e6; Yobs=8.75e-11
zs=[complex(a,b) for a in (0.3,0.9,1.5) for b in (-0.5,0,0.5)]
for m1 in (1e-4,1e-3,5e-3):
    m=np.array([m1,math.sqrt(m1**2+7.42e-5),math.sqrt(m1**2+2.5e-3)])*1e-9
    for tb in (5,10,20):
        vu=174*math.sin(math.atan(tb)); ytau=1.777/(174*math.cos(math.atan(tb)))
        npass=nbad=0; tot=0; best=0
        for z1,z2,z3 in itertools.product(zs,zs,zs):
            R=R12(z1)@R13(z2)@R23(z3)
            Y=1j*U.conj()@np.diag(np.sqrt(m))@R@np.diag(np.sqrt(D))/vu
            H=Y.conj().T@Y
            # rotate degenerate pair so Re H12 = 0
            h=H[:2,:2].real; th=0.5*math.atan2(2*h[0,1],h[0,0]-h[1,1]); O=np.eye(3); O[:2,:2]=[[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]]
            Yr=Y@O; Hr=Yr.conj().T@Yr
            dH=(Hr[1,1]-Hr[0,0]).real
            if abs(dH)<1e-30: continue
            t=math.log(1e16/M)/(16*math.pi**2); deltaN=abs(2*dH*t); GammaRel=max(Hr[0,0].real,Hr[1,1].real)/(8*math.pi)
            if deltaN<GammaRel: nbad+=1
            pref=3*ytau**2/(32*math.pi)*Hr[1,0].imag*(Yr[2,0].conjugate()*Yr[2,1]).real/dH
            eps=[pref/Hr[0,0].real, pref/Hr[1,1].real]
            YB=(8/23)*(3/4)*(TR/mphi)*(abs(eps[0])+abs(eps[1]))
            tot+=1; npass+=YB>=Yobs; best=max(best,YB)
        print(f"m1={m1:g} eV tanb={tb}: pass {npass}/{tot} ({npass/tot:.1%}), max Y_B={best:.2e}, delta_N<Gamma in {nbad/tot:.1%}")
