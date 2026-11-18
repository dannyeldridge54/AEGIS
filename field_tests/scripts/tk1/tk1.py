"""TK1 (locked PREREG_TK1). SERAPIS-E through Janus core (3rd/2nd order), exact MS, Janus relation, data pulls, CAMB BB."""
import sys, math, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import build, predict
from tools.serapis_calc.ms import Background, spectra as ms_spectra
from tools.serapis_calc import relation, data
from tools.janus_calc.core import Model, spectra3
S2 = 2*math.sqrt(2); ok = True
def row(C, N, tag):
    global ok
    m, V, dV, p0 = build('serapis_e', C); M = Model(V, dV, p0, Nmax=4000); bg = Background(V, dV, p0, Nmax=4000)
    t = time.time(); a = spectra3(M, N); ta = time.time()-t
    c = M.spectra(N); t = time.time(); b = ms_spectra(bg, N); tb = time.time()-t
    rel = relation.alpha_s(b['ns'], b['r'], S2, 1.0); sg = data.sigma(b['ns'])
    dn, dr, da = abs(a['ns']-b['ns']), abs(a['r']/b['r']-1), abs(a['alpha_s']-b['alpha_s']); dre = abs(rel/b['alpha_s']-1)
    o = dn <= 3e-4 and dr <= 0.02 and da <= 5e-5 and dre <= 0.06; ok &= o
    print(f"{tag} C {C:.2e} N* {N:.3f} | MS n_s {b['ns']:.5f} r {b['r']:.4e} α_s {b['alpha_s']:.3e} ({tb:.1f}s) | Janus3 Δn_s {a['ns']-b['ns']:+.1e} Δr/r {a['r']/b['r']-1:+.2%} Δα {a['alpha_s']-b['alpha_s']:+.1e} ({ta*1e3:.0f} ms) "
          f"| Janus2 Δn_s {c['ns']-b['ns']:+.1e} | rel α_s {rel:.3e} ({dre:.1%}) | pulls SPA {sg['CMB-SPA']:+.2f}σ SPA+DESI {sg['CMB-SPA+DESI']:+.2f}σ, r<0.036 {'ok' if b['r']<0.036 else 'X'} | {'PASS' if o else 'FAIL'}", flush=True)
    return b
print('(i) grid at N* = 50.7', flush=True)
R = [row(C, 50.7, 'grid') for C in (1.0e-6, 1.15e-6, 1.3e-6)]
print('(ii) end-to-end derived (self-consistent N*, audited ρ reheating)', flush=True)
for TR in (6.6e8, 2.0e10):
    for C in (1.0e-6, 1.15e-6, 1.3e-6):
        p = predict('serapis_e', C, TR, tol=0.002); R.append(row(C, p['Nstar'], f'e2e T_R {TR:.1e}'))
print('(f) CAMB primordial-tensor BB at ℓ = 80', flush=True)
try:
    import camb
    for r in sorted({round(x['r'], 6) for x in R})[::2]:
        pars = camb.set_params(H0=67.4, ombh2=0.0224, omch2=0.12, As=2.1e-9, ns=0.972, r=r, nt=-r/8, WantTensors=True, lmax=300)
        res = camb.get_results(pars); bb = res.get_cmb_power_spectra(pars, CMB_unit='muK', raw_cl=False)['tensor'][80, 2]
        print(f"  r {r:.3e}: D_ℓ^BB(80) tensor = {bb:.3e} μK²", flush=True)
except Exception as e: print('  CAMB error', e)
print('TK1 VERDICT (agreement bars, all points): ' + ('PASS' if ok else 'FAIL'))
