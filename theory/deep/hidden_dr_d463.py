gh=10.0
def dn(eps):
    xi0=(eps*106.75/gh)**0.25; xib=xi0*(10.75/106.75)**(-1/3)
    return xi0,xib,(4/7)*gh*xib**4
for eps in (1e-5,1e-3):
    xi0,xib,d=dn(eps)
    for kk in (0.005,0.021):
        print(f"eps_h={eps:.0e}: xi0={xi0:.3f}, xi_BBN={xib:.3f}, dN_eff(hidden)={d:.4f}; total with 0.047+{kk} = {d+0.047+kk:.3f}")
# largest eps with total < 0.14 (worst KK 0.021)
lo,hi=1e-8,1e-2
for _ in range(100):
    m=(lo*hi)**0.5; lo,hi=(m,hi) if dn(m)[2]+0.068<0.14 else (lo,m)
print(f"largest eps_h (worst KK): {lo:.2e}; VERDICT: {'SAFE' if dn(1e-5)[2]+0.068<0.14 else 'EXCLUDED'}")
