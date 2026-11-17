"""A5b — PREREG_A5b_jeans.md"""
import sys, math; sys.path.insert(0, '.')
from galpy.potential import NFWPotential, HernquistPotential, MWPotential2014
from galpy.df import jeans
from tools.janus_astro import jeans as J
out = []; w1 = 0.0
pots = {'NFW': (NFWPotential(amp=1, a=1), J.M_nfw(), J.nu_nfw()), 'Hern': (HernquistPotential(amp=1, a=1), J.M_hernquist(), J.nu_hernquist())}
for name, (P, M, nuself) in pots.items():
    for tr, nu, dens in [('self', nuself, None), ('Hern0.5', J.nu_hernquist(0.5), J.nu_hernquist(0.5))]:
        for b in (0.0, 0.5):
            for r in (0.1, 0.5, 1, 3, 10):
                o = J.sigma_r(r, M, nu, b); g = float(jeans.sigmar(P, r, dens=dens, beta=b)); e = abs(o/g - 1); w1 = max(w1, e)
                out.append(f"{name} tracer={tr} beta={b} r={r}: ours {o:.8f} galpy {g:.8f} rel {e:.1e}")
T1 = w1 <= 1e-5; out.append(f"T1 worst {w1:.2e} -> {'PASS' if T1 else 'FAIL'}")
w2 = 0.0
for g_ in (3.0, 3.5):
    for b in (0.0, 0.5):
        for r in (0.3, 1, 5):
            o = J.sigma_r(r, lambda x: 1.0, lambda x: x**-g_, b); ex = math.sqrt(1/((g_ + 1 - 2*b)*r)); w2 = max(w2, abs(o/ex - 1))
T2 = w2 <= 1e-6; out.append(f"T2 point-mass power-law worst {w2:.2e} -> {'PASS' if T2 else 'FAIL'}")
h = MWPotential2014[2]; ro, vo = 8.0, 220.0
a = h.a; amp = h._amp
s = J.sigma_r(8/ro, J.M_nfw(amp, a), J.nu_hernquist(20/ro/ ro*ro/ro if False else 2.5), 0.0)*vo   # Hernquist tracer a = 20 kpc
out.append(f"R MWPotential2014 halo only (NFW a={a*ro:.1f} kpc), Hernquist tracer a=20 kpc, beta=0: sigma_r(8 kpc) = {s:.1f} km/s")
out.append("A5b VALIDATED" if T1 and T2 else "A5b NOT VALIDATED")
open('field_tests/results/janus_astro_a5b.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(l for l in out if not l.startswith(('NFW', 'Hern'))))
