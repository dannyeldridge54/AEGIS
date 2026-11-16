"""D791 (locked PREREG_D791). AI-assisted."""
import math
beta=0.038; PR=2.1e-9; rbc=0.0493/0.265; dx=7.4e-6
PSmax=beta/(1-beta)*PR
dxmin=rbc*dx/math.sqrt(PSmax)
eta=2*dxmin
YB=(28/79)*0.75*(3.2e8/2.2e13)*2*eta
print(f"P_S max={PSmax:.2e}; |dx|_min={dxmin:.3f}; eta={eta:.3f}; Y_B={YB:.2e}; over-production (dilution needed) = {YB/8.75e-11:.1e}")
print("VERDICT:","WALL" if YB/8.75e-11>10 else "VIABLE")
