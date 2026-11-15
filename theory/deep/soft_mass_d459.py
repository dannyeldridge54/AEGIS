import math, sys
sys.path.insert(0,'theory/deep'); from cloud_capture_d446 import run
r=1.43e-4; T0,N0=1.714e12,6.0
for ms in (1e-9,1e0,1e2,1e3,1e4):
    refl,xmin,ret,xf,rem=run(ms,r)
    Tr=f"{T0*math.exp(-(ret-N0)):.2e}" if ret else "none"
    print(f"m_s={ms:.0e} GeV: reflections {len(refl)}, xmin {xmin if xmin is None else round(xmin,4)}, return T={Tr}, x at N-Ne=20 {xf:.4f}",flush=True)
