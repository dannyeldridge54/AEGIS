"""D708 (locked PREREG_D708). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=20
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def E2lat'):src.index('def Eser')])
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
def eta(t,K=60):
    q=mp.e**(2j*mp.pi*t); p=mp.mpf(1)
    for n in range(1,K): p*=1-q**n
    return mp.e**(2j*mp.pi*t/24)*p
def F(t): return -mp.log(mp.im(t)*abs(eta(t))**4)+KAPPA
rho=mp.mpc(0.5,mp.sqrt(3)/2)
import sys; KAPPA=mp.mpf(sys.argv[1])
print("kappa =",KAPPA)
print("1. checks")
print("  |eta(i)| =",mp.nstr(abs(eta(1j)),12)," exact",mp.nstr(mp.gamma(0.25)/(2*mp.pi**0.75),12))
Fr=F(rho); E2r=Eser(rho)
print(f"  F(rho)={mp.nstr(Fr,8)} F(i)={mp.nstr(F(1j),8)} F(rho+.05)={mp.nstr(F(rho+0.05),8)} F(rho+.05i)={mp.nstr(F(rho+0.05j),8)}")
s2=mp.sqrt(2); H=3.7e12
def V(p,C):
    y=mp.e**(s2*p); t=mp.mpc(0.5,y); return (1-Fr/F(t))*(1+C*(Eser(t)-E2r))
p0=mp.log(mp.sqrt(3)/2)/s2+mp.mpf('1e-4')
m2=3*mp.diff(lambda p:V(p,0),p0,2)
print(f"2. vacuum m^2/H^2 = {mp.nstr(m2,5)}, m_phi ~ {float(mp.sqrt(m2))*H:.2e} GeV")
def obs(C,N):
    d=lambda p,k: mp.diff(lambda q:V(q,C),p,k)
    Vf=lambda p:V(p,C)
    eps=lambda p:(d(p,1)/Vf(p))**2/2
    pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
    ps=mp.findroot(lambda p: mp.quad(lambda w:Vf(w)/d(w,1),[pe,p])-N, mp.log(15)/s2)
    Vv=Vf(ps); e=eps(ps); h=d(ps,2)/Vv; x2=d(ps,1)*d(ps,3)/Vv**2
    return mp.e**(s2*ps),1-6*e+2*h,16*e,16*e*h-24*e**2-2*x2

print("3. scan")
for N in (48.4,49.9):
    prev=None
    for C in (0,1e-7,3e-7,1e-6,3e-6,1e-5):
        try: y,ns,r,a=obs(C,N)
        except Exception as ex: print(f"  N*={N} C={C}: no solution"); continue
        print(f"  N*={N} C={C:.0e}: y*={mp.nstr(y,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha_s={mp.nstr(a,4)}",flush=True)
        if prev and (prev[1]-0.970)*(ns-0.970)<=0:
            t=float((0.970-prev[1])/(ns-prev[1])); lc=math.log10(prev[0] or 1e-9)+t*(math.log10(C)-math.log10(prev[0] or 1e-9))
            print(f"    n_s=0.970 at C~{10**lc:.2e}: r~{float(prev[2]+t*(r-prev[2])):.3e} alpha_s~{float(prev[3]+t*(a-prev[3])):.3e} y*~{float(prev[4]+t*(y-prev[4])):.2f}")
        prev=(C,ns,r,a,y)
