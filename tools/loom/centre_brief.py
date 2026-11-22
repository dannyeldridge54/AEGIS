"""Centre brief for the centre referee N0 (Danny 18:15). Collects the previous round's data into one compact input:
still point + directions (D1978), resonance lock map (D1972), method tests (D1976), review pointing, last knock-ons, board states.
N0 reads ONLY this brief + the charter, makes no claims and edits nothing (the null), and returns the ordered direction list from the
inside outwards (the lead)."""
import json, os
R = lambda p: json.load(open(p)) if os.path.exists(p) else None
sp = R('field_tests/results/d1978_still_point.json'); rs = R('field_tests/results/d1972_resonance.json')
mt = R('field_tests/results/d1976_method_3axis.json'); rv = R('field_tests/loom/review.json'); L = R('field_tests/loom/knockon_ledger.json') or []
lines = ['# Centre brief (input for the centre referee N0)', '']
if sp:
    lines += ['## Still point (three tandem axes)', 'T_R %.3g, m3/2 %.3g, u %.4g, chi2 %.1f' % (sp['still_point']['T_R'], sp['still_point']['m32'], sp['still_point']['u'], sp['still_point']['chi2'])]
    lines += ['- %s: eigenvalue %.0f, 1σ step %.3f, %s' % (list(d['composition'].items())[max(range(3), key=lambda i: abs(list(d['composition'].values())[i]))][0], d['eigenvalue'], d['one_sigma_step'], d['kind']) for d in sp['directions']]
if rs:
    last = rs['sweeps'][-1]
    lines += ['', '## Resonance lock map (centre outwards)'] + ['- L%d %s: %s %s' % (r['layer'], r['name'], r['status'][:24], r['margins']) for r in last['rows']] + ['- fits spent: %s' % last['fits_spent']]
if mt:
    lines += ['', '## Method tests (3 axes)', '- coverage %.3f (bar 0.90), false-balance %.3f (bar 0.20), dof %d, chi2/dof %.1f' % (mt['T1_coverage']['centre'], mt['T2_false_balance']['centre'], mt['T3']['dof'], mt['T3']['chi2'] / mt['T3']['dof'])]
    lines += ['- real-data pulls: %s' % {k: round(v, 2) for k, v in mt['T3']['pulls'].items()}]
if rv:
    lines += ['', '## Where the compass arrows point (review)'] + ['- %s: %s (net %+.2f)' % (k, v['direction'], v['net']) for k, v in sorted(rv['pointing'].items(), key=lambda kv: -abs(kv[1]['net']))[:8]]
lines += ['', '## Last knock-ons'] + ['- %s: %s ⇒ %s' % (e['d'], e['adjustment'], '; '.join(e['disturbed'])) for e in L[-5:]]
open('field_tests/loom/centre_brief.md', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
