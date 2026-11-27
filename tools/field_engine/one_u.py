"""D2266: one-|u| lepton consistency near tau = i (see PREREG_D2266)."""
import json, numpy as np
r, s13 = 7.49e-5/2.513e-3, 0.02195
x_oct = 0.0685/2.0685
xs = np.linspace(0.005, 0.6, 119001)
ok = (r/xs**3 >= 1/3) & (r/xs**3 <= 3) & (s13/xs**2 >= 1/3) & (s13/xs**2 <= 3)
X = xs[ok]; out = dict(r=r, s13=s13, x_oct=x_oct, X_nu=[float(X.min()), float(X.max())] if X.size else None,
    c_r_at_oct=r/x_oct**3, c13_at_oct=s13/x_oct**2, verdict='PASS' if X.size and X.min() <= x_oct <= X.max() else 'FAIL')
json.dump(out, open('field_tests/results/d2266_one_u.json', 'w'), indent=1); print(out)
