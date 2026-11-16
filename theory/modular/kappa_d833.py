"""D833 (locked PREREG_D833). kappa/V0 = g_s/(8 pi v4) vs the D831 bound. AI-assisted."""
import math
a=1/(2*math.pi)**3; k10=(2*math.pi)**7; T3=a  # alpha'=1, g_s=1 check of 2kappa^2 T3^2
print("2k10^2 T3^2 =",k10*T3**2,"(2pi =",2*math.pi,")")
for ys in (13.8,14.0,14.1,14.7):
    bound=2.9e-3/ys
    print(f"y*={ys}: bound kappa/V0 <= {bound:.3e}; v4_min/g_s = {1/(8*math.pi*bound):.1f}; v4_min:",
          ", ".join(f"g_s={g}: {g/(8*math.pi*bound):.1f}" for g in (0.05,0.1,0.2,0.3)))
