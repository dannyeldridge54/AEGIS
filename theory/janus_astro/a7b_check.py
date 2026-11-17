import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import sommerfeld as S
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
ok1 = True
for a in (0.01, 0.03):
    for v in (1e-2, 3e-3):
        eta = a/v; ex = 2*math.pi*eta/(1 - math.exp(-2*math.pi*eta)); num = S.coulomb_single(1000.0, v, a)**2
        e = abs(num-ex)/ex; ok1 &= e <= 1e-3; P(f'B1 alpha={a} v={v}: |s|^2={num:.6f} exact={ex:.6f} rel={e:.1e}')
s = S.wino_s(1000.0, alpha_w=1e-9); e2 = max(abs(s[0]-1), abs(s[1])); ok2 = e2 <= 1e-6; P(f'B2 free limit: s={s} dev={e2:.1e}')
Ms = np.arange(1500, 3501, 10.0); s00 = np.array([abs(S.wino_s(M)[0])**2 for M in Ms])
ipk = next(i for i in range(1, len(Ms)-1) if s00[i] > s00[i-1] and s00[i] > s00[i+1])
Mpk = Ms[ipk]; ok3 = 2300 <= Mpk <= 2500; P(f'B3 first resonance of |s00|^2 at M = {Mpk:.0f} GeV (|s00|^2 = {s00[ipk]:.1f})')
P('solver', 'VALIDATED' if ok1 and ok2 and ok3 else 'NOT VALIDATED', f'(B1 {ok1}, B2 {ok2}, B3 {ok3})')
P('Application [estimate]: line rate mass dependence, sigma_line ∝ |s_+-|^2 / M^2 (tree-level annihilation)')
ref = abs(S.wino_s(1000.0)[1])**2/1000.0**2
fE = {}; fpred = {660: 0.14, 1000: 0.26, 1850: 0.67}
for M in (660, 800, 1000, 1400, 1850):
    s = S.wino_s(float(M)); R = (abs(s[1])**2/M**2)/ref
    line = f'  M={M} GeV: |s00|^2={abs(s[0])**2:.3f} |s+-|^2={abs(s[1])**2:.3f} R(M)={R:.3f}'
    # D735: f_max = sqrt(L/sigma), L = 4e-28 (M/TeV)^2, sigma = 7.1e-27 assigned at 1 TeV, now x R(M)
    L = 4e-28*(M/1000)**2; sig = 7.1e-27*R
    fe = math.sqrt(L/sig); fn = fe*math.sqrt(1.86)
    line += f'; f_max Einasto={fe:.2f}, NFW={fn:.2f}, one-loop bracket Einasto {fe*math.sqrt(3):.2f}-{fe*2:.2f}'
    if M in fpred: line += f'; SERAPIS-E f={fpred[M]}'
    P(line)
open('field_tests/results/janus_astro_a7b.txt', 'w').write('\n'.join(out) + '\n')
