import sys, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import predict_fast
f = (106.75/228.75)**0.25; ok = True; L = [f"T_R factor SM→MSSM = {f:.5f}"]
pts = [(1.25e-6, 8.94e8, 'PW2 point')] + [(C, T, 'box') for T in (6.6e8, 2.0e10) for C in (1.0e-6, 1.15e-6, 1.3e-6)]
for C, T, tag in pts:
    a = predict_fast('serapis_e', C, T); b = predict_fast('serapis_e', C, T*f, g=228.75)
    dN, dn, dr = b['Nstar'] - a['Nstar'], b['ns'] - a['ns'], b['r']/a['r'] - 1
    o = abs(dn + 6.3e-5) <= 0.5e-5 and abs(dN + 0.063) <= 0.003 and abs(dr - 0.0016) <= 0.0003; ok &= o
    L.append(f"{tag} C {C:.3g} T_R {T:.3g}→{T*f:.4g}: SM N* {a['Nstar']:.4f} n_s {a['ns']:.6f} r {a['r']:.5e} α_s {a['alpha_s']:.4e} | MSSM N* {b['Nstar']:.4f} n_s {b['ns']:.6f} r {b['r']:.5e} α_s {b['alpha_s']:.4e} | ΔN* {dN:+.4f} Δn_s {dn:+.2e} Δr/r {dr:+.2%} {'in' if o else 'OUT'}"); print(L[-1], flush=True)
L.append('A1 expectation: ' + ('PASS' if ok else 'FAIL')); print(L[-1]); open('field_tests/results/a1_mssm_gstar.txt', 'w').write('\n'.join(L) + '\n')
