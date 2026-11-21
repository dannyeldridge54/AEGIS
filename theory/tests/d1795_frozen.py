import math, json
MP, H0, rL, s = 2.435e27, 1.44e-33, 7.1e-121, 38.6
f = math.sqrt(3) / (2 * s); m = math.sqrt(rL) / f * MP
out = dict(f=f, m_eV=m, m_over_H0=m / H0, verdict='PASS' if m / H0 <= 3 else 'FAIL',
           f_needed_for_m_eq_H0=math.sqrt(rL) * MP / H0)
out['share_range'] = [(mm / MP) ** 2 * 0.022 ** 2 / rL for mm in (1e-33, 1e-28)]
out['svrcek_bound'] = 1 / 243 ** 2
out['c_gamma'] = {d: 4.2 / d for d in (0.5, 1, 2)}
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1795_frozen.json', 'w'), indent=1)
