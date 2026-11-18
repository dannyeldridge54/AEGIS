import sys, time; sys.path.insert(0, '.')
import numpy as np, math
from tools.serapis_calc.meter import TABLE
C0 = 1.25e-6
u = np.array([math.log(r[1]/C0) for r in TABLE]); NS = np.array([r[0] for r in TABLE]); R = np.array([r[4] for r in TABLE]); AL = np.array([r[5] for r in TABLE])
dns = dr = dal = 0.0
for i in range(len(TABLE)):
    m = np.ones(len(TABLE), bool); m[i] = False
    pn = np.polyfit(u[m], NS[m], 2); pr = np.polyfit(u[m], np.log(R[m]), 2); pa = np.polyfit(u[m], AL[m], 2)
    dns = max(dns, abs(np.polyval(pn, u[i]) - NS[i])); dr = max(dr, abs(math.exp(np.polyval(pr, u[i]))/R[i] - 1)); dal = max(dal, abs(np.polyval(pa, u[i]) - AL[i]))
from tools.serapis_calc.emulator import emulate
t = time.time(); [emulate(1.1e-6) for _ in range(1000)]; dt = (time.time() - t)/1000*1000
T1 = dns <= 2e-4; T2 = dr <= 0.02; T3 = dal <= 5e-5; T4 = dt <= 1.0
L = [f"leave-one-out over 5 PW6 points: max|Δn_s| {dns:.2e} (T1 {T1}); max|Δr/r| {dr:.3%} (T2 {T2}); max|Δα_s| {dal:.2e} (T3 {T3})",
     f"emulate() {dt:.4f} ms/call (T4 {T4})",
     f"sample: emulate(1.15e-6) = {emulate(1.15e-6)}",
     f"PT1 VERDICT: {'ALL PASS → ADOPT (register serapis_emulator)' if (T1 and T2 and T3 and T4) else 'FAIL / not adopted'}"]
open('field_tests/results/pt1_emulator.txt', 'w').write('\n'.join(str(x) for x in L) + '\n'); print('\n'.join(str(x) for x in L))
