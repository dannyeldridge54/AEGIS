# D892 (W2.2): instanton-only Weinberg term vs the bound of D891. Arithmetic only.
import math
vu=170.0
for Ms in (6e15,3e16):
    mW=vu**2/Ms*1e9
    need=[m/mW for m in (4e-9,1.7e-8,7e-8)]
    for MN in (1e11,1e13):
        e=MN/Ms   # e^{-S_N} if M_N = M_s e^{-S_N} (x=1)
        print(f"M_s={Ms:.0e}: c needed {need[0]:.1e}-{need[2]:.1e} (S_W >= {-math.log(need[2]):.1f}-{-math.log(need[0]):.1f}); M_N={MN:.0e}: e^-S_N={e:.1e}, S_N={-math.log(e):.1f}")
