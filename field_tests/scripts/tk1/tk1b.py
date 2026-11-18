"""TK1 per DEV D1. Usage: tk1b.py grid|e2e. Janus core 3rd/2nd order, exact MS (3 k), Janus relation, data pulls; CAMB BB in the e2e job."""
import sys, math, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import build
from tools.serapis_calc.ms import Background, spectra as ms_spectra
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc import relation, data
from tools.janus_calc.core import Model, spectra3
S2 = 2*math.sqrt(2); ok = True; rs = []
def selfc(M, V, TR):
    Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend-N)[0])/Ve, TR)
        if abs(N2-N) < 1e-3: return N2
        N = N2
    return N2
def row(C, N=None, TR=None):
    global ok
    m, V, dV, p0 = build('serapis_e', C); M = Model(V, dV, p0, Nmax=4000); bg = Background(V, dV, p0, Nmax=4000)
    if TR is not None: N = selfc(M, V, TR)
    a = spectra3(M, N); c = M.spectra(N); t = time.time(); b = ms_spectra(bg, N, dlnk=(-0.05, 0.0, 0.05)); tb = time.time()-t
    rel = relation.alpha_s(b['ns'], b['r'], S2, 1.0); sg = data.sigma(b['ns'])
    dn, dr, da = abs(a['ns']-b['ns']), abs(a['r']/b['r']-1), abs(a['alpha_s']-b['alpha_s']); dre = abs(rel/b['alpha_s']-1)
    o = dn <= 3e-4 and dr <= 0.02 and da <= 5e-5 and dre <= 0.06; ok &= o; rs.append(b['r'])
    tag = f"T_R {TR:.1e}" if TR else "grid"
    print(f"{tag} C {C:.2e} N* {N:.3f} | MS n_s {b['ns']:.5f} r {b['r']:.4e} α_s {b['alpha_s']:.3e} ({tb:.0f}s) | Janus3 Δn_s {a['ns']-b['ns']:+.1e} Δr/r {a['r']/b['r']-1:+.2%} Δα {a['alpha_s']-b['alpha_s']:+.1e} "
          f"| Janus2 Δn_s {c['ns']-b['ns']:+.1e} | rel α_s {rel:.3e} ({dre:.1%}) | pulls SPA {sg['CMB-SPA']:+.2f}σ SPA+DESI {sg['CMB-SPA+DESI']:+.2f}σ, r<0.036 {'ok' if b['r']<0.036 else 'X'} | {'PASS' if o else 'FAIL'}", flush=True)
job = sys.argv[1]
if job == 'grid':
    for C in (1.0e-6, 1.15e-6, 1.3e-6): row(C, N=50.7)
else:
    for TR in (6.6e8, 2.0e10):
        for C in (1.0e-6, 1.15e-6, 1.3e-6): row(C, TR=TR)
    try:
        import camb
        for r in (min(rs), max(rs)):
            pars = camb.set_params(H0=67.4, ombh2=0.0224, omch2=0.12, As=2.1e-9, ns=0.972, r=r, nt=-r/8, WantTensors=True, lmax=300)
            bb = camb.get_results(pars).get_cmb_power_spectra(pars, CMB_unit='muK')['tensor'][80, 2]
            print(f"CAMB r {r:.3e}: tensor D_ℓ^BB(80) = {bb:.3e} μK²", flush=True)
    except Exception as e: print('CAMB error', e, flush=True)
print(f'TK1 {job} VERDICT (agreement bars): ' + ('PASS' if ok else 'FAIL'), flush=True)
