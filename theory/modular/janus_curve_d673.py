"""D673 (locked PREREG_D673_JANUS_CURVE). AI-assisted."""
import re, mpmath as mp
mp.mp.dps=30
c=mp.log(1728)/(2*mp.pi)
def obs_from(u,x,cc):
    ns=1-8*u**2*((2-x)+cc*u*(5-x)); r=64*u**4*(1+x)**2*(1+2*cc*u); a=-32*u**4*(1+x)*((4+x)+cc*u*(23+2*x))
    return ns,r,a
def solve_full(N,eps):
    Nf=lambda I: mp.quad(lambda t: t**3/((t+c)**2*(4+eps*t**3)),[mp.sqrt(2),I])
    I=mp.findroot(lambda I: Nf(I)-N, mp.sqrt(8*N))
    return 1/I, eps*I**3/4, I
def solve_hyp(N,eps):
    f=lambda I: I**2/8*mp.hyp2f1(1,mp.mpf(2)/3,mp.mpf(5)/3,-eps*I**3/4)-N
    I=mp.findroot(f, mp.sqrt(8*N)); return 1/I, eps*I**3/4, I
exact=[]
for l in open('field_tests/results/janus_ext_d665.txt'):
    m=re.match(r"tau=i eps=(\S+) N\*=(\S+): y\*=(\S+) n_s=(\S+) r=(\S+) alpha=(\S+)",l)
    if m: exact.append(tuple(map(mp.mpf,m.groups())))
for l in open('field_tests/results/kairos_nstar_d637.txt'):
    m=re.match(r"Kairos N\*=(\S+): y\*=(\S+) n_s=(\S+) r=(\S+)",l)
    if m: exact.append((mp.mpf(0),mp.mpf(m.group(1)),mp.mpf(m.group(2)),mp.mpf(m.group(3)),mp.mpf(m.group(4)),None))
ok=True
for eps,N,ys,ns0,r0,a0 in exact:
    u,x,I=solve_full(N,eps); ns,r,a=obs_from(u,x,c)
    uh,xh,Ih=solve_hyp(N,eps); nsh,rh,ah=obs_from(uh,xh,0)
    dn=ns-ns0; dr=r/r0-1
    if abs(dn)>0.002 or abs(dr)>0.08: ok=False
    ae=f" alpha {mp.nstr(a,4)} vs {mp.nstr(a0,4)} ({mp.nstr(100*(a/a0-1),3)}%)" if a0 is not None else ""
    print(f"eps={mp.nstr(eps,2)} N*={mp.nstr(N,5)}: (i) I*={mp.nstr(I,4)} x={mp.nstr(x,3)} n_s={mp.nstr(ns,5)} (exact {mp.nstr(ns0,5)}, d={mp.nstr(dn,2)}) r={mp.nstr(r,4)} ({mp.nstr(100*dr,3)}%){ae} | (ii) n_s={mp.nstr(nsh,5)} r={mp.nstr(rh,4)}",flush=True)
print("VERDICT (i):","PASS" if ok else "FAIL")
print("\nJanus curve at N*=47.6 (variant i): x, eps, I*(~y*-c), n_s, r, alpha_s")
N=mp.mpf('47.6')
for x in [0,0.25,0.5,0.75,1,1.5,2,2.5]:
    # find eps giving this x at N: solve I, eps jointly via I from N with eps=4x/I^3
    g=lambda I: mp.quad(lambda t: t**3/((t+c)**2*(4+(4*x/I**3)*t**3)),[mp.sqrt(2),I])-N
    I=mp.findroot(g, mp.sqrt(8*N)); eps=4*x/I**3; ns,r,a=obs_from(1/I,x,c)
    print(f"  x={x}: eps={mp.nstr(eps,3)} I*={mp.nstr(I,4)} y*={mp.nstr(I+c,4)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha={mp.nstr(a,4)}",flush=True)
# largest n_s with y* <= 25 at N*=47.6
I25=25-c
g=lambda x: mp.quad(lambda t: t**3/((t+c)**2*(4+(4*x/I25**3)*t**3)),[mp.sqrt(2),I25])-N
xmax=mp.findroot(g,0.5); ns,r,a=obs_from(1/I25,xmax,c)
print(f"y*=25 at N*=47.6: x={mp.nstr(xmax,3)} eps={mp.nstr(4*xmax/I25**3,3)} n_s={mp.nstr(ns,5)} r={mp.nstr(r,4)} alpha={mp.nstr(a,4)}")
