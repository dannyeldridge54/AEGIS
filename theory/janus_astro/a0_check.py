"""Locked battery A0 (PREREG_A0_janus_astro.md). Writes field_tests/results/janus_astro_a0.txt."""
import math, time, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import const as K, stars, compact, gw, halos, binaries
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
verdict = {}
def rel(a, b): return abs(a-b)/abs(b)
t0 = time.time()
# T1
ok = True
for n, x1ex in [(0, math.sqrt(6)), (1, math.pi), (5, math.inf)]:
    x1, w, s = stars.lane_emden(n)
    xs = np.linspace(1e-3, min(x1, 20.0) if x1 < math.inf else 20.0, 200)
    if n == 5:
        x1b, _, s = stars.lane_emden(5, xi_max=20.0)
    err = float(np.max(np.abs(s.sol(xs)[0] - stars.lane_emden_exact(n, xs))))
    dx = abs(x1 - x1ex) if x1ex < math.inf else 0.0
    ok &= err <= 1e-9 and dx <= 1e-9
    P(f'T1 n={n}: max|dtheta|={err:.2e} xi1={x1} |dxi1|={dx:.2e}')
verdict['T1'] = ok
# T2
tab = {1.5: (3.65375, 2.71406), 2: (4.35287, 2.41105), 3: (6.89685, 2.01824), 4: (14.97155, 1.79723)}
ok = True
for n, (xt, wt) in tab.items():
    a = stars.lane_emden(n); b = stars.lane_emden(n, method='RK45', rtol=1e-10, atol=1e-13)
    r1, r2 = rel(a[0], b[0]), rel(a[1], b[1]); t1, t2 = rel(a[0], xt), rel(a[1], wt)
    ok &= max(r1, r2) <= 1e-6 and max(t1, t2) <= 5e-6
    P(f'T2 n={n}: xi1={a[0]:.7f} omega={a[1]:.7f} routes {r1:.1e}/{r2:.1e} table {t1:.1e}/{t2:.1e}')
verdict['T2'] = ok
# T3
mA = stars.chandrasekhar_mass(2.0)/K.M_sun; mB = stars.chandrasekhar_mass(2.0, 2.01824)/K.M_sun
verdict['T3'] = rel(mA, mB) <= 1e-5 and rel(mA, 5.836/4) <= 5e-3
P(f'T3 M_Ch(mu_e=2) A={mA:.6f} B={mB:.6f} Msun; A/B-1={rel(mA,mB):.1e}; vs 1.459: {rel(mA,5.836/4):.1e}')
# T4
ok = True; rho = 1e18
for comp in [0.1, 0.3, 0.6, 0.8]:
    R = math.sqrt(comp*K.c**2*3/(8*math.pi*K.G*rho))
    Pc, M = compact.schwarzschild_interior_Pc(rho, R)
    Rn, Mn = compact.tov(lambda p: rho, Pc, r_max=10*R)
    ok &= max(rel(Rn, R), rel(Mn, M)) <= 1e-6
    P(f'T4 uniform 2GM/Rc2={comp}: dR/R={rel(Rn,R):.1e} dM/M={rel(Mn,M):.1e}')
Kp, rc = 1e-2, 1e3
Mpoly, Rpoly = stars.polytrope_mass_radius(1, Kp, rc)
Rn, Mn = compact.tov(lambda p: math.sqrt(p/Kp), Kp*rc**2, r_max=10*Rpoly)
ok &= max(rel(Rn, Rpoly), rel(Mn, Mpoly)) <= 1e-3
P(f'T4 Newtonian n=1 polytrope: 2GM/Rc2={2*K.G*Mpoly/(Rpoly*K.c**2):.1e} dR/R={rel(Rn,Rpoly):.1e} dM/M={rel(Mn,Mpoly):.1e}')
verdict['T4'] = ok
# T5
ok = abs(compact.kerr_isco(0) - 6) <= 1e-10 and abs(compact.kerr_isco(1, True) - 1) <= 1e-10 and abs(compact.kerr_isco(1, False) - 9) <= 1e-10
P(f'T5 limits: {compact.kerr_isco(0)} {compact.kerr_isco(1,True)} {compact.kerr_isco(1,False)}')
for a in [0, 0.3, 0.5, 0.7, 0.9, 0.99]:
    for pro in (True, False):
        d = abs(compact.kerr_isco(a, pro) - compact.kerr_isco_numeric(a, pro)); ok &= d <= 1e-5
        P(f'T5 a={a} {"pro" if pro else "retro"}: r={compact.kerr_isco(a,pro):.8f} |d|={d:.1e}')
verdict['T5'] = ok
# T6
ok = True
for mc in [1.2, 10, 30]:
    for f in [10, 30, 100]:
        A = gw.time_to_coalescence(f, mc*K.M_sun); B = gw.time_to_coalescence_numeric(f, mc*K.M_sun)
        ok &= rel(B, A) <= 1e-8; P(f'T6 Mc={mc} f={f}: tau={A:.6e} s rel={rel(B,A):.1e}')
verdict['T6'] = ok
# T7
from colossus.cosmology import cosmology; cosmology.setCosmology('planck18')
from colossus.halo import profile_nfw, profile_einasto
ok = True; rs, rhos = 20.0, 1e7          # colossus units: kpc/h, Msun h^2 / kpc^3
for x in [0.1, 1, 5, 20]:
    r = x*rs
    for name, rho, menc, p in [('NFW', halos.nfw_rho, halos.nfw_menc, (rhos, rs)),
                               ('Ein0.16', halos.einasto_rho, halos.einasto_menc, (rhos, rs, 0.16)),
                               ('Ein0.30', halos.einasto_rho, halos.einasto_menc, (rhos, rs, 0.30)),
                               ('Burkert', halos.burkert_rho, halos.burkert_menc, (rhos, rs))]:
        cf, nm = menc(r, *p), halos.menc_numeric(rho, r, *p); e = rel(nm, cf); ok &= e <= 1e-8
        line = f'T7 {name} r/rs={x}: closed vs quad {e:.1e}'
        if name == 'NFW': ref = profile_nfw.NFWProfile(rhos=rhos, rs=rs).enclosedMass(r)
        elif name.startswith('Ein'): ref = profile_einasto.EinastoProfile(rhos=rhos, rs=rs, alpha=p[2]).enclosedMass(r)
        else: ref = None
        if ref is not None:
            e2 = rel(cf, ref); ok &= e2 <= 1e-6; line += f'; vs colossus {e2:.1e}'
        P(line)
verdict['T7'] = ok
# T8
ok = True
for q in [0.1, 0.3, 1, 3, 10]:
    hi = binaries.roche_volume_radius(q, 96, 192); lo = binaries.roche_volume_radius(q, 48, 96); eg = binaries.roche_eggleton(q)
    ok &= rel(hi, eg) <= 1e-2 and rel(lo, hi) <= 1e-3
    P(f'T8 q={q}: numeric={hi:.6f} Eggleton={eg:.6f} rel={rel(hi,eg):.2e} res={rel(lo,hi):.1e}')
verdict['T8'] = ok
# T9
from astropy import constants as AC, units as u
pairs = [('G', K.G, AC.G.si.value), ('c', K.c, AC.c.si.value), ('M_sun', K.M_sun, AC.M_sun.si.value), ('R_sun', K.R_sun, AC.R_sun.si.value),
         ('L_sun', K.L_sun, AC.L_sun.si.value), ('pc', K.pc, (1*u.pc).si.value),
         ('R_s(Msun)', compact.schwarzschild_radius(K.M_sun), 2*AC.G.si.value*AC.M_sun.si.value/AC.c.si.value**2)]
ok = True
for nme, a, b in pairs: e = rel(a, b); ok &= e <= 1e-9; P(f'T9 {nme}: {a:.10e} vs astropy {b:.10e} rel={e:.1e}')
verdict['T9'] = ok
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in verdict.items()))
P('A0', 'VALIDATED' if all(verdict.values()) else 'NOT VALIDATED for: ' + ', '.join(k for k, v in verdict.items() if not v))
P(f'runtime {time.time()-t0:.1f} s')
open('field_tests/results/janus_astro_a0.txt', 'w').write('\n'.join(out) + '\n')
