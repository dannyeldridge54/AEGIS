# AEGIS-FP JTY5S3LUTCXSBXMB · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Data for the Janus 'Strings' view: the inflaton torus modulus y(N) = Im τ along the SERAPIS-E history at the A1 point (C 1.25e-6, N* 50.18),
and the brane / tadpole configuration (D696, D861, NA11). Output: docs/web/string_geom.json."""
import sys, json, math, pathlib; R = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(R))
from tools.serapis_calc.pipeline import build
from tools.janus_calc.core import Model
C = 1.25e-6; m, V, dV, p0 = build('serapis_e', C); M = Model(V, dV, p0, Nmax=4000)
Ns = [M.Nend*k/240 for k in range(241)]; ys = [math.exp(math.sqrt(2)*float(M.sol.sol(n)[0])) for n in Ns]
out = dict(C=C, Nstar=50.18, Nend=M.Nend, N=Ns, y=ys, y_star=math.exp(math.sqrt(2)*float(M.sol.sol(M.Nend - 50.18)[0])),
           branes=[dict(at=[0.5, 0], n=5, label='O3 + 5 stuck D3'), dict(at=[0, 0.5], n=5, label='O3 + 5 stuck D3'), dict(at=[0.5, 0.5], n=5, label='O3 + 5 stuck D3'), dict(at=[0, 0], n=1, label='O3 + 1 D3 (origin)')],
           tadpole='3N + N0 + N_flux = 16 → (5, 1, 0); N_eff = N − N0 = 4', ImS_Imrho=15*4/(64*math.pi**6*C), gs=0.232, ImS=0.485, ImT1=4.31,
           formula='C = 15 N_eff / (64 π⁶ Im S · Im ρ)  (BHK one-loop; D689, D696, NA11)')
json.dump(out, open(R / 'docs/web/string_geom.json', 'w'), indent=0); print('y* =', round(out['y_star'], 3), 'Nend', round(M.Nend, 2), 'ImS·Imρ', round(out['ImS_Imrho'], 1))
