import math
conv=1.17e-17; sv_th=2.2e-26
res={}
for m in (1e4,1e5):
    for frac in (1.0,0.01):
        sv=sv_th/frac/conv                    # GeV^-2 needed
        lam=(16*math.pi*m*m*sv)**0.25
        res[(m,frac)]=lam
        print(f"m={m:.0e} GeV, Omega<= {frac:.0%} DM: sigma v >= {sv:.2e} GeV^-2 -> lambda >= {lam:.2f}")
for sF in (65e3,140e3):
    for m in (1e4,1e5):
        G=m**5/(16*math.pi*sF**4); print(f"goldstino channel sqrtF={sF:.0e}, m={m:.0e}: tau={6.58e-25/G:.1e} s (moves charge, does not remove it)")
print("VERDICT:", "REMOVABLE PERTURBATIVELY" if res[(1e4,0.01)]<=math.sqrt(4*math.pi) else "NEEDS NON-PERTURBATIVE CHARGE BREAKING")
