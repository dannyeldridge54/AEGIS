"""D1498: separation of DILMIX strip vs SERAPIS-E and form A with SO sigma(n_s)=0.002, LiteBIRD dr=1e-3 (PREREG_D1498)."""
import json, math
g = json.load(open('field_tests/results/D1494_strip_edges.json'))['grid']
strip = [(p['alpha'], p['C'], p['ns'], p['r']) for p in g if p.get('in_band')]
ex = json.load(open('field_tests/results/D1491_dilmix_ms.json')); strip.append((0.375, 1.5e-6, ex['ns'], ex['r']))
REF = {"SERAPIS_rho_A1": (0.974393, 4.82095e-4), "SERAPIS_tau_i": (0.97462, 4.8335e-4), "formA_closest": (0.969, 6.56e-4)}
sn, sr = 0.002, 1e-3
out = {"D": "D1498", "n_strip": len(strip), "vs": {}}
for k, (n0, r0) in REF.items():
    d = [(math.hypot((ns - n0) / sn, (r - r0) / sr), a, C, ns, r) for a, C, ns, r in strip]
    d.sort(); out['vs'][k] = dict(min=d[0][0], min_at=d[0][1:3], max=d[-1][0], max_at=d[-1][1:3],
                                  centre=math.hypot((ex['ns'] - n0) / sn, (ex['r'] - r0) / sr))
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/D1498_testability.json', 'w'), indent=1)
