"""D775 (locked PREREG_D775). PMNS/R grid as D745. AI-assisted."""
import math, cmath, itertools, numpy as np
d=math.radians; s12,s13,s23=math.sin(d(33.4)),math.sin(d(8.6)),math.sin(d(49)); c12,c13,c23=[math.sqrt(1-x*x) for x in (s12,s13,s23)]
e=cmath.exp(-1j*d(230))
U=np.array([[c12*c13,s12*c13,s13*e],[-s12*c23-c12*s23*s13/e,c12*c23-s12*s23*s13/e,s23*c13],[s12*s23-c12*c23*s13/e,-c12*s23-s12*c23*s13/e,c23*c13]])
def R12(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,s,0],[-s,c,0],[0,0,1]])
def R13(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def R23(z): c,s=cmath.cos(z),cmath.sin(z); return np.array([[1,0,0],[0,c,s],[0,-s,c]])
zs=[complex(a,b) for a in (0.3,0.9,1.5) for b in (-0.5,0,0.5)]
v=174.; mphi=3.1746e13; Yobs=8.75e-11; mnu3=0.05e-9
f=lambda x: math.sqrt(x)*(1-(1+x)*math.log((1+x)/x)); g=lambda x: math.sqrt(x)/(1-x)
spec={0.3:(0.212,1.0),1:(0.707,1.0),3:(1.0,0.471)}   # (pair, single) in units of M_H
cases=[(0.3,1e12,6.608e8),(1,1e12,8.937e8),(3,1e12,1.986e9),(0.3,1e13,6.463e9),(1,1e13,7.258e9),(3,1e13,1.432e9)]   # NA6: T_R from tr_2p1_na6 (c=3 M_H=1e13 newly open, reported only)
allpass=True
for c,MH,TR in cases:
    Mp,Ms=spec[c][0]*MH,spec[c][1]*MH; Dm=np.array([Mp,Mp,Ms])
    for m1 in (1e-4,1e-3):
        m=np.array([m1,math.sqrt(m1**2+7.42e-5),math.sqrt(m1**2+2.5e-3)])*1e-9
        npass={'pair':0,'single':0}; tot=0; mx={'pair':0,'single':0}
        for z1,z2,z3 in itertools.product(zs,zs,zs):
            R=R12(z1)@R13(z2)@R23(z3)
            Y=1j*U.conj()@np.diag(np.sqrt(m))@R@np.diag(np.sqrt(Dm))/v
            H=Y.conj().T@Y
            h=H[:2,:2].real; th=0.5*math.atan2(2*h[0,1],h[0,0]-h[1,1]); O=np.eye(3); O[:2,:2]=[[math.cos(th),-math.sin(th)],[math.sin(th),math.cos(th)]]
            Y=Y@O; H=Y.conj().T@Y
            eps=[]
            for i in range(3):
                s=0
                for j in range(3):
                    if j==i or abs(Dm[j]-Dm[i])<1e-6*Dm[i]: continue
                    x=Dm[j]**2/Dm[i]**2; s+=(H[i,j]**2).imag/H[i,i].real*(f(x)+g(x))
                eps.append(-s/(8*math.pi))
            ep=abs(0.5*(eps[0]+eps[1])); es=abs(eps[2]); tot+=1
            for lab,ev,M in (('pair',ep,Mp),('single',es,Ms)):
                if lab=='single' and Ms>=mphi/2: continue
                Yb=0.9391*(8/23)*(3/4)*(TR/mphi)*2*ev; npass[lab]+=Yb>=Yobs; mx[lab]=max(mx[lab],ev)
        eDI=lambda M:3*M*mnu3/(16*math.pi*v**2)
        line=f"c={c} M_H={MH:.0e} T_R={TR:.2e} m1={m1:g}: "
        for lab,M in (('pair',Mp),('single',Ms)):
            fr=npass[lab]/tot; line+=f"{lab} M={M:.2e} pass={fr:.1%} max|eps|={mx[lab]:.2e} (eps_DI={eDI(M):.2e}, ratio {mx[lab]/eDI(M):.2f}); "
            if MH==1e12 and max(npass.values())/tot<0.10: allpass=False
        print(line,flush=True)
        if c==0.3 and m1==1e-3 and MH==1e12: print(f"K4: max|eps_pair|/eps_DI = {mx['pair']/eDI(Mp):.2f} (need 0.3-1.3)")
print("VERDICT:","lepto_rho computed: PASS (all M_H=1e12 cases >=10%)" if allpass else "lepto_rho: some M_H=1e12 case below 10%")
