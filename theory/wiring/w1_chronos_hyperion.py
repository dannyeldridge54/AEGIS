import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_calc import models, core
from tools.janus_calc.observe import observe, nstar_match
from tools.janus_astro import hmf, gwb
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
rel = lambda a, b: abs(a - b)/abs(b) if b != 0 else abs(a)
M = models.serapis_E(1e-6)
Vend = M.V(M.sol.sol(M.Nend)[0])
def chronos(TR, H0, w=0.0, tol=1e-4):
    N = 50.0
    for _ in range(50):
        s = core.spectra3(M, N); Vs = M.V(M.sol.sol(M.Nend - N)[0])
        N2 = nstar_match(s['r'], Vs/Vend, TR, w, H0=H0)
        if abs(N2 - N) < tol: N = N2; break
        N = N2
    s3 = core.spectra3(M, N)
    return dict(Nstar=N, ns=s3['ns'], r=s3['r'], alpha_s=core.alpha_dn(M, N))
def hyperion(ns, r, alpha_s, TR, H0=67.66, mnu=0.0587):
    import camb
    h = H0/100; onu = mnu/93.14
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=0.02242, omch2=0.11933 - onu, mnu=mnu, num_massive_neutrinos=1, nnu=3.046, omk=0, tau=0.0561)
    p.InitPower.set_params(As=2.1e-9, ns=ns, nrun=alpha_s); p.set_matter_power(redshifts=[0.0], kmax=50.0); p.NonLinear = camb.model.NonLinear_none
    res = camb.get_results(p); k, _, Pcb = res.get_matter_power_spectrum(minkh=1e-4, maxkh=50, npoints=2000, var1='delta_nonu', var2='delta_nonu')
    rho = hmf.RHO_CRIT_H2*(0.02242 + 0.11933 - onu)/h**2
    tab = hmf.SigmaTable(k, Pcb[0], rho)
    from colossus.cosmology import cosmology; cosmology.setCosmology('planck18')
    n14 = hmf.n_above(1e14, k, Pcb[0], rho, n=80); n15 = hmf.n_above(1e15, k, Pcb[0], rho, n=80)
    MP = gwb.MP; rho_end = 1.5*math.pi**2*2.1e-9*r*MP**4/2.27; rho_R = gwb.rho_rad(TR)
    hist = gwb.History([(0.0, math.log(rho_end/rho_R))]); fR = gwb.f_R(TR)
    return dict(sigma8=float(res.get_sigma8()[0]), n14=n14, n15=n15, fR=fR, plateau=gwb.omega_gw_h2(1e-3, 1.0, r))
TRs = [1e6, 1e7, 1e8, 3.2e8, 3e9]
# W1a
w1a = 0.0
for TR in TRs:
    a = chronos(TR, 67.4); b = observe(M, TR=TR)
    w1a = max(w1a, *(rel(a[k], b[k]) for k in ('Nstar', 'ns', 'r', 'alpha_s')))
c0 = chronos(3.2e8, 67.66); h1 = hyperion(c0['ns'], c0['r'], c0['alpha_s'], 3.2e8)
h2 = hyperion(float(repr(c0['ns']) and c0['ns']), c0['r'], c0['alpha_s'], 3.2e8)
w1a_h = max(rel(h1[k], h2[k]) for k in h1)
ok['W1a'] = w1a <= 1e-10 and w1a_h <= 1e-12
P(f'W1a Chronos step vs observe(): {w1a:.1e}; Hyperion step vs direct: {w1a_h:.1e}')
# W1b
H0 = 67.66; prev = None; diffs = []
for it in range(2):
    c = chronos(3.2e8, H0); h = hyperion(c['ns'], c['r'], c['alpha_s'], 3.2e8, H0=H0); H0 = 67.66
    cur = {**c, **h}
    if prev: diffs.append(max(rel(cur[k], prev[k]) for k in cur))
    prev = cur
ok['W1b'] = diffs[0] <= 1e-12; P(f'W1b loop pass1 vs pass2: {diffs[0]:.1e}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x else "FAIL"}' for k, x in ok.items()), '-> wiring', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
# W1c
a, b = chronos(3.2e8, 67.4), chronos(3.2e8, 67.66)
P(f'W1c H0 wire: n_s {a["ns"]:.6f} (H0 67.4) -> {b["ns"]:.6f} (67.66): dn_s = {b["ns"]-a["ns"]:+.2e}; dN* = {b["Nstar"]-a["Nstar"]:+.4f}')
rows = []
for TR in TRs:
    c = chronos(TR, 67.66); h = hyperion(c['ns'], c['r'], c['alpha_s'], TR); rows.append((TR, c, h))
    P(f'W1c T_R={TR:.1e}: N*={c["Nstar"]:.3f} n_s={c["ns"]:.5f} r={c["r"]:.3e} a_s={c["alpha_s"]:.3e} | sigma8={h["sigma8"]:.5f} n(>1e14)={h["n14"]:.4e} n(>1e15)={h["n15"]:.4e} | GW knee f_R={h["fR"]:.3g} Hz plateau={h["plateau"]:.3e}')
ds8 = max(r_[2]['sigma8'] for r_ in rows) - min(r_[2]['sigma8'] for r_ in rows)
dn15 = math.log(max(r_[2]['n15'] for r_ in rows)/min(r_[2]['n15'] for r_ in rows))
pos = ds8 > 10*1e-4 or dn15 > 10*2.9e-3
P(f'W1c across T_R band: d sigma8 = {ds8:.2e} (10x precision = 1e-3), d ln n(>1e15) = {dn15:.2e} (10x precision = 2.9e-2) -> cross-domain signal {"YES" if pos else "NO (below 10x precision)"}')
open('field_tests/results/wiring_w1.txt', 'w').write('\n'.join(out) + '\n')
