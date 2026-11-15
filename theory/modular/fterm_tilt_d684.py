"""D684 (locked PREREG_D684_FTERM_TILT). AI-assisted."""
import mpmath as mp, math
mp.mp.dps=30
def L(t): return -mp.log(2*mp.im(t)*abs(mp.eta(t))**4)
def dL(t,h=mp.mpf('1e-12')):
    gx=(L(t+h)-L(t-h))/(2*h); gy=(L(t+1j*h)-L(t-1j*h))/(2*h); return (gx-1j*gy)/2
Li=L(1j)
def f(y): t=1j*y; return mp.e**(L(t)-Li)*4*y**2*abs(dL(t))**2
def Ljm(y):
    q=mp.e**(-2*mp.pi*y); lj=2*mp.pi*y+mp.log(1+744*q+196884*q*q); return lj+mp.log(abs(1-1728*mp.e**(-lj)))
def I(y): return mp.log(mp.e**(2*(Ljm(y)-mp.log(1728)))+1)/(4*mp.pi)
print("1. near-vacuum behaviour of f along tau = i(1+d):")
for d in (1e-2,1e-3,1e-4):
    print(f"   d={d}: f={mp.nstr(f(1+mp.mpf(d)),6)}  f/d^2={mp.nstr(f(1+mp.mpf(d))/mp.mpf(d)**2,6)}")
s2=mp.sqrt(2)
fpp=mp.diff(lambda p: f(mp.e**(s2*p)),0,2)
print(f"   f''(phi) at vacuum = {mp.nstr(fpp,6)}  -> m^2/H^2 = 3 R f'' = {mp.nstr(3*fpp,6)} * R")
def obs(R,N):
    V=lambda p: (lambda x: x/(x+1))(I(mp.e**(s2*p))**2)+R*f(mp.e**(s2*p))
    d=lambda p,n: mp.diff(V,p,n)
    eps=lambda p:(d(p,1)/V(p))**2/2
    pe=mp.findroot(lambda p:eps(p)-1,mp.log(2)/s2)
    ps=mp.findroot(lambda p: mp.quad(lambda w:V(w)/d(w,1),[pe,p])-N, mp.log(22)/s2)
    Vv=V(ps); e=eps(ps); h=d(ps,2)/Vv; x2=d(ps,1)*d(ps,3)/Vv**2
    return mp.e**(s2*ps),1-6*e+2*h,16*e,16*e*h-24*e**2-2*x2
print("2. scan:")
rows={}
for N in (46.08,49.21):
    rows[N]=[]
    for lr in [-16,-15,-14,-13.5,-13,-12.5,-12,-11.5,-11]:
        R=mp.mpf(10)**lr
        try: y,ns,r,a=obs(R,N)
        except Exception as ex: print(f"   N*={N} R=1e{lr}: no solution"); continue
        rows[N].append((lr,y,ns,r,a))
        print(f"   N*={N} R=1e{lr}: y*={mp.nstr(y,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha_s={mp.nstr(a,4)}",flush=True)
H=3.7e12
for N in rows:
    for target in (0.9682,0.9728):
        rr=rows[N]
        for (l1,y1,n1,r1,a1),(l2,y2,n2,r2,a2) in zip(rr,rr[1:]):
            if (n1-target)*(n2-target)<=0:
                t=float((target-n1)/(n2-n1)); lr=l1+t*(l2-l1); R=10**lr
                print(f"   N*={N}: n_s={target} at R~1e{lr:.2f}: y*~{float(y1+t*(y2-y1)):.2f} r~{float(r1+t*(r2-r1)):.3e} alpha_s~{float(a1+t*(a2-a1)):.3e}  -> m3/2 ~ {math.sqrt(3*R)*H:.2e} GeV")
