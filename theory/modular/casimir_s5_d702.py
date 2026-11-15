"""D702 (locked PREREG_D702). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=20
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def E2lat'):src.index('def Eser')])
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
def E3lat(U,M=60):
    s=0
    for n in range(-M,M+1):
        for m in range(-M,M+1):
            if n or m: s+=1/abs(n+m*U)**10
    return mp.im(U)**5*s
def E3ser(t,K=30):  # Sigma' normalisation: 2zeta(6)y^3 + (3pi/4)zeta(5)/y^2 + (8pi^3/Gamma(3)) sqrt(y) sum n^{5/2} sigma_{-5} K_{5/2} cos
    x,y=mp.re(t),mp.im(t)
    s=2*mp.zeta(10)*y**5+2*mp.sqrt(mp.pi)*mp.gamma(4.5)*mp.zeta(9)/mp.gamma(5)/y**4
    for n in range(1,K):
        sig=sum(d**-9 for d in range(1,n+1) if n%d==0)
        s+=8*mp.pi**5/mp.gamma(5)*mp.sqrt(y)*n**4.5*sig*mp.besselk(4.5,2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return s
rho=mp.mpc(0.5,mp.sqrt(3)/2)
print("1. checks")
for U in (mp.mpc(0,1),mp.mpc(0.5,2)): print(f"  U={U}: E3 lattice={mp.nstr(E3lat(U),8)} series={mp.nstr(E3ser(U),8)}")
E3r=E3ser(rho); E2r=Eser(rho)
print(f"  E3(rho)={mp.nstr(E3r,8)} E3(i)={mp.nstr(E3ser(1j),8)} E3(rho+.05)={mp.nstr(E3ser(rho+0.05),8)} E3(rho+.05i)={mp.nstr(E3ser(rho+0.05j),8)}")
s2=mp.sqrt(2); H=3.7e12
def V(p,C):
    y=mp.e**(s2*p); t=mp.mpc(0.5,y); return (1-mp.sqrt(E3r/E3ser(t)))*(1+C*(Eser(t)-E2r))
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
