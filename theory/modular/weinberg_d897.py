# D897: D891-D892 Weinberg numbers redone with D895's window m_nu1 = 2e-11 - 9e-10 eV. Arithmetic only.
import math
vu=170.0; win=(2e-11,1.34e-10,9e-10)
for name,L in [("reduced M_P",2.435e18),("M_P",1.22e19),("M_s low",6e15),("M_s high",3e16)]:
    m=vu**2/L*1e9
    c=[w/m for w in win]
    print(f"{name:12s} m_W={m:.2e} eV: c needed {c[0]:.1e} / {c[1]:.1e} / {c[2]:.1e}; S_W >= {-math.log(c[2]):.1f} - {-math.log(c[0]):.1f}")
for Ms in (6e15,3e16):
    for MN in (1e11,1e12,1e13):
        print(f"M_s={Ms:.0e}, M_N={MN:.0e}: S_N={-math.log(MN/Ms):.1f}")
