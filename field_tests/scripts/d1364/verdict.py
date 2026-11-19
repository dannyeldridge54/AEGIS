"""D1364: apply the LOCKED rule of PREREG_D1364_p3_mix.md to the merged results (reading only, no computation).
Usage: python3 field_tests/scripts/d1364/verdict.py [path/to/D1364_p3_mix.json]  -> prints the verdict block for the D-note."""
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else 'field_tests/results/D1364_p3_mix.json'
d = json.load(open(p)); rows = {r['w']: r for r in d['rows']}
r1 = rows[1.0]
g0 = abs(r1['ns'] - 0.97446) <= 2e-4 and abs(r1['r']/4.81e-4 - 1) <= 0.02
inb = lambda r: 0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4
print(f"k = {d['k']:.6f}")
print('| w | n_s | r | α_s | N* | in band | s |')
print('|---|---|---|---|---|---|---|')
for w in (1.0, 0.75, 0.5, 0.25, 0.0):
    r = rows[w]; print(f"| {w} | {r['ns']:.5f} | {r['r']:.4g} | {r['alpha_s']:.4g} | {r['Nstar']:.2f} | {'yes' if inb(r) else 'no'} | {r['seconds']} |")
print(f"G0 (w = 1 reproduces serapis_point n_s 0.97446 ± 2e-4, r 4.81e-4 ± 2%): {'PASS' if g0 else 'FAIL'} "
      f"(n_s {r1['ns']:.5f}, r {r1['r']:.4g})")
if not g0:
    print('VERDICT: G0 failed — per the lock nothing else is read.'); sys.exit()
passing = [w for w in (1.0, 0.75, 0.5, 0.25, 0.0) if inb(rows[w])]
print('passing w:', passing)
small = [w for w in passing if w <= 0.25]
if small:
    print('VERDICT (locked rule): small w passes the band → P3 → "derived (candidate)".')
elif passing:
    print('VERDICT (locked rule): only w near 1 passes → "the SERAPIS plateau needs the s = 2 term to dominate, which the controlled string '
          'expansion does not give — P3 stays a postulate; blocker = order of the expansion" (unless the s = 1 piece cancels: see D1365–D1375).')
else:
    print('VERDICT (locked rule): no w passes the band (only possible if G0 passed but w = 1 sits outside the band) — record as is.')
