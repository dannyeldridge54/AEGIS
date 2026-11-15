"""D689 (locked PREREG_D689_BHK_TILT). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=25
def E2lat(U,a4=0,a5=0,M=80):
    s=0
    for n in range(-M,M+1):
        for m in range(-M,M+1):
            if n==0 and m==0: continue
            s+=mp.cos(2*mp.pi*(n*a5-m*a4))/abs(n+m*U)**4
    return mp.im(U)**2*s
def Eser(t,K=30):  # Fourier expansion of E(t,2) = sum' y^2/|n+m t|^4
    x,y=mp.re(t),mp.im(t)
    s=2*mp.zeta(4)*y**2+mp.pi*mp.zeta(3)/y
    for n in range(1,K):
        sig=sum(d**-3 for d in range(1,n+1) if n%d==0)
        s+=8*mp.pi**2*mp.sqrt(y)*n**1.5*sig*mp.besselk(1.5,2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return s
print("1. checks")
for U in (mp.mpc(0,1),mp.mpc(0.5,2)):
    E=E2lat(U); S=sum(E2lat(U,a4,a5) for a4,a5 in ((0,0.5),(0.5,0),(0.5,0.5)))
    print(f"  U={U}: E(U,2) lattice={mp.nstr(E,8)} series={mp.nstr(Eser(U),8)}; sum over half-periods={mp.nstr(S,8)} vs -3/4 E={mp.nstr(-0.75*E,8)}")
rho=mp.mpc(0.5,mp.sqrt(3)/2)
print(f"  E(i,2)={mp.nstr(Eser(1j),8)}  E(rho,2)={mp.nstr(Eser(rho),8)}  (min expected at rho)")
for d in (0.02,0.05):
    print(f"  E(rho+{d}i)-E(rho)={mp.nstr(Eser(rho+1j*d)-Eser(rho),4)}, E(rho+{d})-E(rho)={mp.nstr(Eser(rho+d)-Eser(rho),4)}")
Er=Eser(rho)
def jy(y):
    q=-mp.e**(-2*mp.pi*y); return 1/q+744+196884*q+21493760*q*q+864299970*q**3
def Irho(y):
    a=abs(jy(y)); return mp.log(1+(a/1728)**2)/(4*mp.pi)
s2=mp.sqrt(2)
def obs(C,N):
    V=lambda p:(lambda y:(lambda x:x/(x+1))(Irho(y)**2)*(1+C*(Eser(mp.mpc(0.5,y))-Er)))(mp.e**(s2*p))
    d=lambda p,k: mp.diff(V,p,k)
    eps=lambda p:(d(p,1)/V(p))**2/2
    pe=mp.findroot(lambda p:eps(p)-1,mp.log(2.5)/s2)
    ps=mp.findroot(lambda p: mp.quad(lambda w:V(w)/d(w,1),[pe,p])-N, mp.log(22)/s2)
    Vv=V(ps); e=eps(ps); h=d(ps,2)/Vv; x2=d(ps,1)*d(ps,3)/Vv**2
    return mp.e**(s2*ps),1-6*e+2*h,16*e,16*e*h-24*e**2-2*x2
def jan(ns,r):   # D669 general relation, p=2sqrt2, kappa=1
    p=2*s2; k=1; rho_=p*mp.sqrt(r/2)/(1-ns); x=(rho_-1)/(1+k*rho_)
    return -(1-ns)**2/2*(1+x)*(1+k*k*x)/(1-k*x)**2
print("2. scan")
res={}
for N in (46.09,49.49):
    res[N]=[]
    for lc in (-8,-7.5,-7,-6.75,-6.5,-6.25,-6):
        C=mp.mpf(10)**lc
        try: y,ns,r,a=obs(C,N)
        except Exception as ex: print(f"  N*={N} C=1e{lc}: no solution"); continue
        res[N].append((lc,y,ns,r,a)); print(f"  N*={N} C=1e{lc}: y*={mp.nstr(y,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha_s={mp.nstr(a,4)} (Janus k=1: {mp.nstr(jan(ns,r),4)})",flush=True)
print("3. targets and natural size  [Im S Im rho = 15 N /(64 pi^6 C)]")
for N in res:
    rr=res[N]
    for target in (0.9682,0.9728):
        for (l1,y1,n1,r1,a1),(l2,y2,n2,r2,a2) in zip(rr,rr[1:]):
            if (n1-target)*(n2-target)<=0:
                t=float((target-n1)/(n2-n1)); lc=l1+t*(l2-l1); C=10**lc
                prod=15/(64*math.pi**6*C)
                line=f"  N*={N}: n_s={target} at C~{C:.2e}: y*~{float(y1+t*(y2-y1)):.2f} r~{float(r1+t*(r2-r1)):.3e} alpha_s~{float(a1+t*(a2-a1)):.3e} | Im S*Im rho = {prod:.0f} N"
                for gs in (0.1,0.3):
                    ImS=1/(2*math.sqrt(2)*math.pi*gs); line+=f" | g_s={gs}: Im S={ImS:.2f}, Im rho={prod/ImS:.0f}N"
                print(line)
