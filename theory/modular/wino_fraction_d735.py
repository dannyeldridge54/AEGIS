"""D735 (locked PREREG_D735). AI-assisted."""
import math
sl=1.6e-27+0.5*1.1e-26
for M,f in ((660,0.14),(1000,0.26),(1850,0.67)):
    L=4e-28*(M/1000)**2; fmax=math.sqrt(L/sl)
    print(f"M2={M} GeV: f={f}, L_Einasto={L:.1e}, f_max={fmax:.2f} (x2 unc: {math.sqrt(2*L/sl):.2f} / {math.sqrt(L/2/sl):.2f}), kpc core f_max={math.sqrt(1e2*L/sl):.1f}-{math.sqrt(1e3*L/sl):.1f}: {'PASS' if f<=fmax else 'FAIL'} (Einasto)")
# where f(M) crosses f_max: f(M) from D732 linear-ish interpolation
import numpy as np
Ms=np.linspace(660,1850,200); fs=np.interp(Ms,[660,1000,1850],[0.14,0.26,0.67]); fm=np.sqrt(4e-28*(Ms/1000)**2/sl)
ok=Ms[fs<=fm]; print(f"Einasto passing M2: {ok.min():.0f}-{ok.max():.0f} GeV" if len(ok) else "none")
