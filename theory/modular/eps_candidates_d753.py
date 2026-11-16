"""D753 (locked PREREG_D753). AI-assisted."""
import math, mpmath as mp
L=1/(16*math.pi**2); MP=2.435e18; V=4.8e15**4; H=math.sqrt(V/3)/MP
def eta(t):
    q=mp.exp(2j*mp.pi*t); return mp.exp(2j*mp.pi*t/24)*mp.qp(q)
def E2(t):
    y=t.imag; return sum(y**2/abs(m+n*t)**4 for m in range(-60,61) for n in range(-60,61) if (m,n)!=(0,0))
ti=1j; tr=complex(0.5,math.sqrt(3)/2)
single={"L":L,"L^2":L*L,"e^-2pi y (i)":math.exp(-2*math.pi),"e^-4pi y (i)":math.exp(-4*math.pi),
 "e^-2pi y (rho)":math.exp(-2*math.pi*tr.imag),"e^-4pi y (rho)":math.exp(-4*math.pi*tr.imag),"C_BHK":1.15e-6,
 "H/M_P":H/MP,"sqrt(A_s)":math.sqrt(2.1e-9),"m_phi/M_P (i)":1.9e11/MP,"m_phi/M_P (rho)":2.2e13/MP,
 "|eta(i)|^24":float(abs(eta(ti))**24),"|eta(rho)|^24":float(abs(eta(tr))**24),"1/E(rho,2)":1/E2(tr),"1/E(i,2)":1/E2(ti)}
cands=dict(single); cands.update({f"L*{k}":L*v for k,v in single.items() if not k.startswith("L")})
N=len(cands); p=N*math.log10(4)/20
for tgt,val in (("tau=i",1.45e-4),("rho",6e-5)):
    hits=[(k,v) for k,v in cands.items() if val/2<=v<=val*2]
    print(f"{tgt} target {val:.2e}: {len(hits)} hit(s) of {N} candidates (chance of >=1 accidental hit ~{min(p,1):.2f}): "+"; ".join(f"{k}={v:.2e}" for k,v in hits))
print("all:", "; ".join(f"{k}={v:.2e}" for k,v in sorted(cands.items(),key=lambda x:x[1])))
