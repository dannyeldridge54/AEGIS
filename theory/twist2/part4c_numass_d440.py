# D440: leptogenesis window vs DESI DR2 sum-mass bound (standard formulas; no new model)
import math
dm21,dm31=7.42e-5,2.51e-3   # eV^2 (NuFIT-like)
S=lambda m1: m1+math.sqrt(m1**2+dm21)+math.sqrt(m1**2+dm31)
lo,hi=0,0.05
for _ in range(80):
    mid=(lo+hi)/2; lo,hi=(mid,hi) if S(mid)<0.0642 else (lo,mid)
print(f"NO min sum {S(0):.4f} eV; sum<0.0642 -> m1 < {lo:.4f} eV; IO min sum {2*math.sqrt(dm31)+0:.4f} (excluded at 95%)")
v=174.0; matm=math.sqrt(dm31)*1e-9  # GeV
YB=8.7e-11
for mt in (math.sqrt(dm21),0.02,math.sqrt(dm31)):
    kappa=0.02*(0.01/mt)**1.1           # Buchmuller-Di Bari-Plumacher fit, strong washout
    eps_need=YB/(1.3e-3*kappa)         # Y_B ~ 1.3e-3 eps kappa  (sphaleron 28/79, g*=106.75)
    M1=eps_need*16*math.pi*v**2/(3*matm)  # Davidson-Ibarra eps_max = 3 M1 m_atm/(16 pi v^2)
    print(f"m~1={mt:.4f} eV: kappa={kappa:.2e} eps_need={eps_need:.2e} M1_min={M1:.2e} GeV  T_RH>M1 needs <= capture T 1.5e11? {M1<1.5e11}")
