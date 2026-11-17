import math
k = math.sqrt(2.3/4.0)
band = {'LO': {'HESS': (0.189, 0.207), 'McM17': (0.266, 0.292), 'MWP14': (0.327, 0.359)},
        'NLO': {'HESS': (0.208, 0.228), 'McM17': (0.294, 0.323), 'MWP14': (0.360, 0.396)}}   # D1124
out = [f"scale factor sqrt(2.3/4) = {k:.3f}"]
for lab, d in band.items():
    for h, (a, b) in d.items():
        lo, hi = a*k, b*k; v = 'PASS' if lo >= 0.26 else ('FAIL' if hi < 0.26 else 'BAND-DEPENDENT')
        out.append(f"{lab} {h}: f_max [{lo:.3f}, {hi:.3f}] vs 0.26 -> {v}")
open('/home/claude/aegis/field_tests/results/a2g_line_igs.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
