"""D691 (locked PREREG_D691_EPSTEIN_PLATEAU). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=25
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rho=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rho)
Eh=lambda y: Eser(mp.mpc(0.5,y))-Er
s2=mp.sqrt(2); H=3.7e12
def V(p,C): y=mp.e**(s2*p); e=Eh(y); return e/(e+1)*(1+C*e)
p0=mp.log(mp.sqrt(3)/2)/s2
m2=3*mp.diff(lambda p:V(p,0),p0,2)
print(f"1. vacuum at rho: d2V/dphi2 (V0 units) = {mp.nstr(m2/3,6)}  -> m^2/H^2 = {mp.nstr(m2,6)}, m_phi = {float(mp.sqrt(m2))*H:.3e} GeV")
def obs(C,N):
    d=lambda p,k: mp.diff(lambda q:V(q,C),p,k)
    Vf=lambda p:V(p,C)
    eps=lambda p:(d(p,1)/Vf(p))**2/2
    pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
    ps=mp.findroot(lambda p: mp.quad(lambda w:Vf(w)/d(w,1),[pe,p])-N, mp.log(15)/s2)
    Vv=Vf(ps); e=eps(ps); h=d(ps,2)/Vv; x2=d(ps,1)*d(ps,3)/Vv**2
    return mp.e**(s2*ps),1-6*e+2*h,16*e,16*e*h-24*e**2-2*x2
res={}
for N in (46.09,49.49):
    res[N]=[]
    for lc in (None,-8,-7,-6.5,-6,-5.5,-5):
        C=0 if lc is None else mp.mpf(10)**lc
        try: y,ns,r,a=obs(C,N)
        except Exception as ex: print(f"  N*={N} C={C}: no solution"); continue
        if lc is not None: res[N].append((lc,y,ns,r,a))
        print(f"  N*={N} C={'0' if lc is None else '1e'+str(lc)}: y*={mp.nstr(y,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha_s={mp.nstr(a,4)}",flush=True)
for N in res:
    rr=res[N]
    for target in (0.9682,0.9728):
        for (l1,y1,n1,r1,a1),(l2,y2,n2,r2,a2) in zip(rr,rr[1:]):
            if (n1-target)*(n2-target)<=0:
                t=float((target-n1)/(n2-n1)); lc=l1+t*(l2-l1); C=10**lc
                print(f"  N*={N}: n_s={target} at C~{C:.2e}: y*~{float(y1+t*(y2-y1)):.2f} r~{float(r1+t*(r2-r1)):.3e} alpha_s~{float(a1+t*(a2-a1)):.3e} | Im S*Im rho = {15/(64*math.pi**6*C):.0f} N")
