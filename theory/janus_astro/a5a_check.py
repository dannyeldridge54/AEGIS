import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import galaxy as G
from galpy.potential import MWPotential2014, vcirc, evaluateRforces, evaluatezforces, evaluatePotentials
from galpy.orbit import Orbit
import astropy.units as u
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b)
mw = G.MW(); ok = {}
o = True
for Rk in [0.5, 1, 2, 4, 8, 16, 30]:
    R = Rk/8; a, b = mw.vcirc(R), float(vcirc(MWPotential2014, R)); e = rel(a, b); o &= e <= 1e-6
    P(f'G1 R={Rk} kpc: v_c ours={a*220:.6f} galpy={b*220:.6f} km/s rel={e:.1e}')
ok['G1'] = o; o = True
for Rk, zk in [(8, 1), (4, 0.5), (12, 3)]:
    R, z = Rk/8, zk/8; FR, Fz = mw.force(R, z)
    gR, gz = float(evaluateRforces(MWPotential2014, R, z)), float(evaluatezforces(MWPotential2014, R, z))
    e = max(rel(FR, gR), rel(Fz, gz)); o &= e <= 1e-6; P(f'G2 (R,z)=({Rk},{zk}) kpc: FR {FR:.8f}/{gR:.8f} Fz {Fz:.8f}/{gz:.8f} rel={e:.1e}')
ok['G2'] = o
v8 = mw.vcirc(1.0)*220; ok['G3'] = rel(v8, 220) <= 1e-4; P(f'G3 v_c(8 kpc) = {v8:.6f} km/s')
tG = 1.0/(8*3.0856775814913673e16/220/3.15576e16)   # 1 Gyr in natural time units (r0/v0)
t = np.linspace(0, tG, 2001); w0 = (1.0, 0.1, 1.1, 0.0, 0.05, 0.0)
s = mw.orbit(w0, t)
E = lambda X: 0.5*(X[3]**2 + X[4]**2 + X[5]**2) + mw.phi(math.hypot(X[0], X[1]), X[2])
E0, E1 = E(s.y[:, 0]), E(s.y[:, -1]); dE = abs(E1 - E0)/abs(E0)
o_ = Orbit(list(w0)); o_.integrate(t, MWPotential2014, method='dop853_c')
Rg, zg = float(o_.R(t[-1], use_physical=False)), float(o_.z(t[-1], use_physical=False))
Ro, zo = math.hypot(s.y[0, -1], s.y[1, -1]), s.y[2, -1]
dpos = max(abs(Ro - Rg), abs(zo - zg))*8
ok['G4'] = dE <= 1e-8 and dpos <= 1e-4
P(f'G4 orbit 1 Gyr: dE/E={dE:.1e}; final R ours={Ro*8:.6f} galpy={Rg*8:.6f}, z ours={zo*8:.6f} galpy={zg*8:.6f} kpc; max|d|={dpos:.1e} kpc')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A5a', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
rho = G.natural_to_rho_GeVcm3(mw.rho_halo(1.0))
vesc = math.sqrt(-2*mw.phi(1.0, 0.0))*220
P(f'Application: rho_DM(8 kpc) = {rho:.4f} GeV/cm^3 (A7a/A7b used 0.39; J scales by {(rho/0.39)**2:.3f}, f_max by {0.39/rho:.3f}); v_esc(8 kpc) = {vesc:.1f} km/s')
open('field_tests/results/janus_astro_a5a.txt', 'w').write('\n'.join(out) + '\n')
