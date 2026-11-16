# D903 (W3.1): Weinberg suppression needed at tau=i for AD (window D900). Arithmetic only.
import math
vu=174.0; MP=2.435e18
for m in (1.6e-10,2.7e-9):
    M=vu**2/(m*1e-9)
    cs=[(n,L/M) for n,L in (("M_P",MP),("M_s 6e15",6e15),("M_s 3e16",3e16))]
    print(f"m_nu1={m:.1e} eV: M=v^2/m={M:.1e} GeV; "+"; ".join(f"c({n})={c:.1e}, S>={-math.log(c):.1f}" for n,c in cs))
print(f"Planck-size singlet Weinberg (|E4(i)|=1.456, c=1): m ~ {1.456*vu**2/MP*1e9:.1e} eV")
