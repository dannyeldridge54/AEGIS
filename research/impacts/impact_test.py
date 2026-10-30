# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: a5e25f69d45264a4
import json, numpy as np
c=json.load(open("craters.json")); t=np.array([x["age"] for x in c]); n=len(t)
Ps=np.arange(20,45.01,0.05)
def scan(ages):
    Z=np.exp(2j*np.pi*ages[None,:]/Ps[:,None]).mean(1); R=np.abs(Z); return R, np.angle(Z)
R,ph=scan(t); i=R.argmax(); Pb=Ps[i]; Rb=R[i]
# phase of the peak: ages t_k = t0 + m*P  -> t0 = phase*P/(2pi) mod P  (peak impact times, Myr ago)
t0=(ph[i]%(2*np.pi))/(2*np.pi)*Pb
print(f"n={n}; best period {Pb:.2f} Myr, R={Rb:.3f}, peaks at {t0:.1f} Myr ago (+ multiples of {Pb:.1f})")
# null: smooth version of the age distribution (kernel 15 Myr), keep only 2-260 Myr
rng=np.random.default_rng(11); best=[]
for _ in range(10000):
    s=rng.choice(t,n)+rng.normal(0,15,n); s=s[(s>=2)&(s<=260)]
    while len(s)<n:
        x=rng.choice(t)+rng.normal(0,15)
        if 2<=x<=260: s=np.append(s,x)
    best.append(scan(s)[0].max())
best=np.array(best); p=(best>=Rb).mean()
print(f"test 1 (rhythm, corrected for scanning 20-45 Myr): p = {p:.4f}")
# local p at the pre-registered window only
w=(Ps>=26)&(Ps<=36); Rw=R[w].max(); Pw=Ps[w][R[w].argmax()]
print(f"strongest inside 26-36 Myr: {Pw:.2f} Myr, R={Rw:.3f}")
# robustness: drop the 5 biggest, use D>=20 km only
for lab,mask in (("D>=20 km",np.array([x["D"]>=20 for x in c])),("D<20 km",np.array([x["D"]<20 for x in c]))):
    Rx,_=scan(t[mask]); print(f"  {lab}: n={mask.sum()}, best {Ps[Rx.argmax()]:.2f} Myr, R={Rx.max():.3f}")
json.dump({"n":n,"Pbest":float(Pb),"R":float(Rb),"t0":float(t0),"p":float(p),"ages":t.tolist(),"names":[x["name"] for x in c],"D":[x["D"] for x in c],"Rcurve":R.tolist(),"Ps":Ps.tolist()},open("impact_result.json","w"))
