import sys, math, time; sys.path.insert(0, '.')
from tools.serapis_calc.pipeline import predict_fast
from tools.serapis_calc.nstar import Nstar
C, T0 = 1.25e-6, 8.94e8; t0 = time.time(); B = predict_fast('serapis_e', C, T0)
L = [f"baseline (PW2 point): N* {B['Nstar']:.4f} n_s {B['ns']:.6f} r {B['r']:.5e} α_s {B['alpha_s']:.5e}"]; print(L[-1], flush=True)
waves = {'w_m': 1.1**1.5, 'w_g': (106.75/228.75)**0.25, 'w_n': 3**0.5}; exp = {'w_m': 0.048, 'w_g': 0.064, 'w_n': 0.183}; ok = True
for k, f in waves.items():
    P = [predict_fast('serapis_e', C, T0*f**s) for s in (1, -1)]; d = [(p['Nstar'] - B['Nstar'], p['ns'] - B['ns'], p['r']/B['r'] - 1, p['alpha_s'] - B['alpha_s']) for p in P]
    e_ns = 1.0e-3*exp[k]; o = all(abs(abs(x[1]) - e_ns) <= 0.3*e_ns for x in d); ok &= o
    asym = abs(d[0][1] + d[1][1])/max(abs(d[0][1]), abs(d[1][1]))
    L.append(f"{k} (T_R ×{f:.4f}^±1): +: ΔN* {d[0][0]:+.4f} Δn_s {d[0][1]:+.2e} Δr/r {d[0][2]:+.2e} Δα {d[0][3]:+.1e} | −: ΔN* {d[1][0]:+.4f} Δn_s {d[1][1]:+.2e} Δr/r {d[1][2]:+.2e} | strength {max(abs(d[0][1]), abs(d[1][1]))/0.003:.3f} σ_SPA | asym {asym:.2f} | expect |Δn_s| {e_ns:.1e} → {'in' if o else 'OUT'}"); print(L[-1], flush=True)
    if k == 'w_g': gN = Nstar(P[0]['r'], 2.2675, T0*f, g=228.75); L.append(f"   g-term check: Nstar(g=228.75, T_R_MSSM) = {gN:.4f} vs Nstar(g=106.75, same T_R) = {Nstar(P[0]['r'], 2.2675, T0*f):.4f} (cancellation at fixed T_R)"); print(L[-1], flush=True)
L.append(f"(1) expectation: {'PASS' if ok else 'FAIL'}  ({time.time()-t0:.0f} s)"); print(L[-1])
open('field_tests/results/w2_reheat_chain.txt', 'w').write('\n'.join(L) + '\n')
