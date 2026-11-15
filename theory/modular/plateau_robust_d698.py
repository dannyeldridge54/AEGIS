"""D698 (locked PREREG_D698). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=25
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rho=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rho)
Eh=lambda y: Eser(mp.mpc(0.5,y))-Er
s2=mp.sqrt(2); H=3.7e12

FORMS={'a':lambda e:e/(e+1),'b':lambda e:1-(1-mp.e**(-e))/e}
for key,P in FORMS.items():
    def V(p,C,P=P): y=mp.e**(s2*p); e=Eh(y); return P(e)*(1+C*e)
    p0=mp.log(mp.sqrt(3)/2)/s2+mp.mpf('1e-4')
    m2=3*mp.diff(lambda p:V(p,0),p0,2)
    def obs(C,N):
        d=lambda p,k: mp.diff(lambda q:V(q,C),p,k)
        Vf=lambda p:V(p,C)
        eps=lambda p:(d(p,1)/Vf(p))**2/2
        pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
        ps=mp.findroot(lambda p: mp.quad(lambda w:Vf(w)/d(w,1),[pe,p])-N, mp.log(15)/s2)
        Vv=Vf(ps); e=eps(ps); h=d(ps,2)/Vv; x2=d(ps,1)*d(ps,3)/Vv**2
        return mp.e**(s2*ps),1-6*e+2*h,16*e,16*e*h-24*e**2-2*x2
    
    print(f"form {key}: m^2/H^2 at rho ~ {mp.nstr(m2,5)}")
    for C in (1.0e-6,1.3e-6):
        y,ns,r,a=obs(C,49.15)
        print(f"  C={C:.1e}: y*={mp.nstr(y,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha_s={mp.nstr(a,4)}",flush=True)
