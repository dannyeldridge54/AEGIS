import math
MP=2.435e18; T=8.17e12; ok=[]
for a,X in ((3846,6.12),(7852,3.0)):
    m=X*T; Y=0.145*(2/106.75)*X**1.5*math.exp(-X); tau=6.58e-25/(m**3/MP**2)
    f=Y*X*4/3; dn=7.4*f; rs=Y*m
    ok.append(dn<0.06)
    print(f"a={a}: m_KK={m:.2e} GeV, Y={Y:.2e}, tau={tau:.1e} s, energy fraction {f:.2e}, stable rho/s={rs:.1e} GeV (x{rs/4.3e-10:.0e} DM), worst dN_eff={dn:.3f}")
print("VERDICT:", "NEEDS NO KK PARITY" if all(ok) else "PROBLEM")
