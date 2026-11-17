"""Locked battery A0s (PREREG_A0s_janus_astro_standards.md)."""
import math, sys, numpy as np
sys.path.insert(0, '.')
from scipy.optimize import brentq
from tools.janus_astro import const as K, stars, compact, gw, halos, binaries
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b); V = {}
# S1
import lalsimulation as ls
ok = True
for m1, m2 in [(1.4, 1.4), (10, 10), (36, 29), (5, 50)]:
    for f in [10, 20, 40]:
        ours = gw.time_to_coalescence(f, gw.chirp_mass(m1*K.M_sun, m2*K.M_sun))
        lal = ls.SimInspiralTaylorF2ReducedSpinChirpTime(f, m1*K.M_sun, m2*K.M_sun, 0.0, 0)
        e = rel(ours, lal); ok &= e <= 1e-6; P(f'S1 m=({m1},{m2}) f={f}: ours={ours:.8e} LAL={lal:.8e} rel={e:.1e}')
V['S1'] = ok
# S2
mc = gw.chirp_mass(35.6, 30.6); V['S2'] = rel(mc, 28.6) <= 5e-3; P(f'S2 GW150914 Mc={mc:.4f} vs 28.6 rel={rel(mc,28.6):.1e}')
# S3
import astropy.units as u
from galpy.potential import NFWPotential, BurkertPotential
rs, rhos = 20.0, 5e6; ok = True
nfw = NFWPotential(amp=4*math.pi*rhos*rs**3*u.Msun, a=rs*u.kpc); bk = BurkertPotential(amp=rhos*u.Msun/u.kpc**3, a=rs*u.kpc)
for r in [1, 8, 20, 100]:
    rr = r*K.kpc
    v1 = halos.v_circ(halos.nfw_menc(rr, rhos*K.M_sun/K.kpc**3, rs*K.kpc), rr)/1e3
    v2 = halos.v_circ(halos.burkert_menc(rr, rhos*K.M_sun/K.kpc**3, rs*K.kpc), rr)/1e3
    g1 = nfw.vcirc(r*u.kpc, quantity=True).to(u.km/u.s).value; g2 = bk.vcirc(r*u.kpc, quantity=True).to(u.km/u.s).value
    ok &= rel(v1, g1) <= 1e-4 and rel(v2, g2) <= 1e-4
    P(f'S3 r={r} kpc: NFW {v1:.6f} vs galpy {g1:.6f} ({rel(v1,g1):.1e}); Burkert {v2:.6f} vs galpy {g2:.6f} ({rel(v2,g2):.1e})')
V['S3'] = ok
# S4
from colossus.cosmology import cosmology; from colossus.halo import mass_so
cosmo = cosmology.setCosmology('planck18'); ok = True
rho_c = cosmo.rho_c(0.0)   # Msun h^2 / kpc^3
for M in [1e10, 1e12, 1e15]:
    R = halos.nfw_from_Mdelta(M, 5.0, rho_c, 200.0)[2]; Rc = mass_so.M_to_R(M, 0.0, '200c')
    ok &= rel(R, Rc) <= 1e-6; P(f'S4 M={M:.0e}: R200c ours={R:.8f} colossus={Rc:.8f} kpc/h rel={rel(R,Rc):.1e}')
V['S4'] = ok
# S5
L = stars.eddington_luminosity(K.M_sun, X=1.0); V['S5'] = rel(L, 1.26e31) <= 1e-2; P(f'S5 L_Edd(1 Msun, X=1) = {L:.4e} W vs 1.26e31 rel={rel(L,1.26e31):.1e}')
# S6
AU = 1.495978707e11
T = binaries.kepler_period(1.00000261*AU, K.M_sun*(1 + 1/328900.56))/86400
V['S6'] = rel(T, 365.256363) <= 5e-5; P(f'S6 sidereal year {T:.6f} d vs 365.256363 rel={rel(T,365.256363):.1e}')
# S7  free neutron gas (Oppenheimer-Volkoff 1939)
from scipy.constants import m_n, hbar, c
lam = hbar/(m_n*c); E0 = m_n*c*c/(lam**3*8*math.pi**2)
Pn = lambda x: E0*(x*(2*x*x/3 - 1)*math.sqrt(1+x*x) + math.asinh(x))
en = lambda x: E0*(x*(2*x*x + 1)*math.sqrt(1+x*x) - math.asinh(x))
def rho_of_P(p):
    if p <= 0: return 0.0
    x = brentq(lambda t: Pn(t) - p, 1e-6, 1e3, xtol=1e-15, rtol=1e-14); return en(x)/c**2
best = (0, 0, 0)
for xc in np.geomspace(0.5, 20, 80):
    R, M = compact.tov(rho_of_P, Pn(xc), r_max=1e6, rtol=1e-9)
    if M > best[1]: best = (xc, M, R)
xs = np.linspace(best[0]*0.85, best[0]*1.15, 61)
for xc in xs:
    R, M = compact.tov(rho_of_P, Pn(xc), r_max=1e6, rtol=1e-9)
    if M > best[1]: best = (xc, M, R)
Mmax = best[1]/K.M_sun; V['S7'] = rel(Mmax, 0.71) <= 2e-2
P(f'S7 OV free neutron gas: M_max={Mmax:.4f} Msun at R={best[2]/1e3:.3f} km (x_c={best[0]:.3f}) vs 0.71 rel={rel(Mmax,0.71):.1e}')
# S8 (reported only)
P(f'S8 (reported) M_Ch(mu_e=2) = {stars.chandrasekhar_mass(2.0)/K.M_sun:.4f} Msun; textbook values 1.44-1.46')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in V.items()))
P('A0s', 'VALIDATED AGAINST STANDARDS' if all(V.values()) else 'NOT VALIDATED for: ' + ', '.join(k for k, v in V.items() if not v))
open('field_tests/results/janus_astro_a0s.txt', 'w').write('\n'.join(out) + '\n')
