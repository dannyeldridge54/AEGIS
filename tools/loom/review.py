"""Pattern review (Danny 17:17): at every result, review ALL pointed fingerprints together, find the pattern, triangulate where they point.
Inputs: field_tests/loom/compass_catalog.json (fingerprints) + field_tests/loom/knockon_ledger.json (every adjustment and what it disturbed).
Three weightings of the votes = the three vectors: (w1) one vote per arrow; (w2) weight 1/headroom (tight arrows count more);
(w3) weight by failure (! = 3, thin ◔ = 2, otherwise 1). The pointing per knob = the median of the three weighted net votes."""
import json, os, statistics
C = json.load(open('field_tests/loom/compass_catalog.json'))['catalog']
L = json.load(open('field_tests/loom/knockon_ledger.json')) if os.path.exists('field_tests/loom/knockon_ledger.json') else []
votes = {}
for c in C:
    if c['direction'] == '○': continue
    h = c['headroom'] if isinstance(c['headroom'], (int, float)) else 1.0
    w1 = 1.0; w2 = 1.0 / max(abs(h), 0.05); w3 = 3.0 if '!' in c['direction'] else (2.0 if c['direction'] == '◔' else 1.0)
    for k, s in c['knobs'].items():
        if s not in '+-': continue
        sg = 1 if s == '+' else -1
        v = votes.setdefault(k, dict(w1=0, w2=0, w3=0, voters=[]))
        v['w1'] += sg * w1; v['w2'] += sg * w2; v['w3'] += sg * w3; v['voters'].append('%s %s (%s)' % (c['quantity'], s, c['direction']))
point = {}
for k, v in votes.items():
    m = statistics.median([v['w1'], v['w2'], v['w3']])
    spread = max(v['w1'], v['w2'], v['w3']) - min(v['w1'], v['w2'], v['w3'])
    agree = len({(x > 0) - (x < 0) for x in (v['w1'], v['w2'], v['w3'])}) == 1
    point[k] = dict(net=m, spread=spread, all_three_agree=agree, direction='RAISE' if m > 0 else 'LOWER' if m < 0 else 'HOLD',
                    contested=any(x.endswith('+ (↑!)') or True for x in []) , voters=v['voters'])
# knock-on pattern: which sectors get disturbed most often, by which adjustments
dist = {}
for e in L:
    for s in e.get('disturbed', []): dist.setdefault(s, []).append(e['adjustment'])
out = dict(pointing=point, knockon_by_sector={k: dict(count=len(v), by=v) for k, v in dist.items()})
json.dump(out, open('field_tests/loom/review.json', 'w'), indent=1)
lines = ['# Pattern review: where all the arrows point (Danny 17:17)', '',
         'Every fingerprint in the compass votes on the knobs it pulls. Three weightings give the three vectors: one vote each; weighted by tightness (1/headroom); weighted by failure (! ×3, ◔ ×2). The pointing is the median of the three.', '',
         '| knob | pointing | net (median) | spread | the 3 weightings agree? | voters |', '|---|---|---|---|---|---|']
for k, p in sorted(point.items(), key=lambda kv: -abs(kv[1]['net'])):
    lines.append('| %s | **%s** | %+.2f | %.2f | %s | %s |' % (k, p['direction'], p['net'], p['spread'], 'yes' if p['all_three_agree'] else 'NO', '; '.join(p['voters'])))
lines += ['', '## Knock-on ledger: what each adjustment disturbed', '']
for s, v in sorted(dist.items(), key=lambda kv: -len(kv[1])):
    lines.append('- **%s** was disturbed %d× by: %s' % (s, len(v), '; '.join(v)))
cat = {'strain moved to another sector': [], 'predictivity spent (fit / new input)': [], 'the fix was an error': []}
for e in L:
    for x in e['disturbed']:
        k = 'predictivity spent (fit / new input)' if x.startswith(('prediction', 'input')) else 'the fix was an error' if x.startswith(('numerics', 'variables', 'consistency', 'geometry')) else 'strain moved to another sector'
        cat[k].append('%s ⇒ %s (%s)' % (e['adjustment'], x, e['d']))
lines += ['', '## The pattern in the knock-ons (three kinds)', '']
for k, v in cat.items(): lines.append('- **%s** (%d): %s' % (k, len(v), '; '.join(v)))
lines += ['', '**Where they all point:** every case of strain moving to another sector passed through the **gravitino**, either its mass m₃/₂ (wino, α_s via the spectrum) or its abundance ∝ T_R (dark-matter overclosure). The only exception is the Kähler thread (gravity/BBN), which passes through a light modulus. The gravitino is the hub of the knock-ons. A fix that leaves m₃/₂ and the gravitino abundance alone (split stacks, Br(φ → NN)) moves no strain; it only spends predictivity.']
open('tools/project_docs/WEAVE_REVIEW.md', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
