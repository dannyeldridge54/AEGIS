"""The Weave as a magnetic field (Danny 17:10): every fix attempt today is a move of one knob; record what it pulled elsewhere.
Rows are HISTORICAL moves taken from the D-notes (each with its D-number). Effects: +1 helped, -1 hurt, 0 neutral, per sector.
Then: the field matrix (which sectors each knob couples), the 'north' (the knob direction that hurts nobody), and the open problems."""
import json
sectors = ['inflation', 'forces(alpha_s)', 'spectrum(wino)', 'flavour', 'leptogenesis/DM', 'gravity/DE', 'control(g_s)']
moves = [  # (D-note, knob, direction, description, {sector: effect})
 ('D1919/D1929', 'K_S: S vacuum rho -> i', '+', 'g_s 2/sqrt3 -> 1 [D1929 reading; contradicts the engine, D1939a]', {'control(g_s)': +1, 'inflation': 0, 'forces(alpha_s)': -1, 'spectrum(wino)': +1}),
 ('D1931/D1937', 'K_T: m3/2 down', '-', 'to raise alpha_s', {'forces(alpha_s)': +1, 'spectrum(wino)': -1}),
 ('D1931a/D732', 'S-T: T_R up', '+', 'for thermal leptogenesis / n_s', {'leptogenesis/DM': -1, 'inflation': 0}),
 ('D1922/D1923', 'K_U: quark slip on tau', '0', 'modular home', {'flavour': -1}),
 ('D1932', 'K_U: one spurion u~0.0266', '0', 'single FN flavon', {'flavour': +1}),
 ('D1906', 'S-T: Kähler thread for DE', '+', 'lambda 0.94 from warped uplift', {'gravity/DE': -1}),
 ('D1881b/D1907', 'S-T: Higgs-pair threshold / U29 tilt', '+', 'close Delta3', {'forces(alpha_s)': -1}),
 ('D1938', 'S-T: supergravity seam term', '0', 'parent-equation threshold', {'forces(alpha_s)': 0}),
 ('D1885a', 'K_U: flux-6 electron offset', '0', 'Koide delta', {'flavour': -1}),
 ('D1894b', 'K_U: one shared step u*', '0', 'the arrow', {'flavour': -1}),
 ('D1926', 'K_S: plateau ends at i', '+', 'inflation check', {'inflation': +1}),
]
knobs = sorted({m[1].split(':')[0] for m in moves})
F = {k: {s: [] for s in sectors} for k in knobs}
for d, kn, sgn, desc, eff in moves:
    for s, e in eff.items(): F[kn.split(':')[0]][s].append(e)
field = {k: {s: (sum(v) if v else None) for s, v in row.items()} for k, row in F.items()}
open_problems = [
 ('alpha_s / Delta3', 'S-T', 'FAIL -4.1 sigma; needs non-universal +0.044 (D1937, D1938)'),
 ('wino margin', 'T', '2 % above the 660 GeV limit; pinned against alpha_s through m3/2'),
 ('non-thermal leptogenesis', 'S-T', 'T_R boxed <~3e9 by gravitino->wino; no mechanism derived'),
 ('g_s > 1 control', 'S', 'rho gives 1.155; i gives 1 but breaks alpha_s'),
 ('quark spurion home', 'U / T-U', 'one spurion fits (PHEN); no geometric source'),
 ('dark-energy thread', 'S-T', 'non-Kähler only; lambda ~0.95 source missing'),
 ('Koide delta, c_e', 'U', 'TRUST'),
 ('neutrino fluxes (4,4,8)', 'U', 'chosen; ratio margin thin'),
 ('v / m_SUSY', 'T', 'tuned 2.7e-7'),
 ('V_inf height, Lambda', 'S', 'inputs'),
 ('N* vs T_R, n_s tilt', 'S', 'tilt chosen; N* not cross-checked'),
 ('battery NEED items', 'mixed', 'BBN late decays, moduli problem, cosmic strings, birefringence, eta_B'),
]
# the poles: which seam collects the hurt
hurt = {}
for d, kn, sgn, desc, eff in moves:
    for s, e in eff.items():
        if e < 0: hurt.setdefault(kn.split(':')[0], []).append((d, s))
out = dict(moves=[dict(d=m[0], knob=m[1], description=m[3], effects=m[4]) for m in moves], field=field, hurt_by_knob=hurt, open_problems=open_problems)
json.dump(out, open('field_tests/loom/field_map.json', 'w'), indent=1)
L = ['# The Weave as a field: how the knobs pull on each other (Danny 17:10)', '',
     'Every fix attempt today was one knob turned. The table records what each attempt did to every sector: **+** helped, **−** hurt, **0** no effect, blank not touched. **These effects are hand judgments read from the D-notes named in each row, not measurements (referee D1942).**', '',
     '| attempt (D-note) | knob turned | ' + ' | '.join(sectors) + ' |', '|---|---|' + '---|' * len(sectors)]
sym = {1: '+', -1: '−', 0: '0'}
for d, kn, sgn, desc, eff in moves:
    L.append('| %s (%s) | %s | ' % (desc, d, kn) + ' | '.join(sym.get(eff.get(s), '') for s in sectors) + ' |')
L += ['', '## The field lines (summed per knob family)', '']
for k, row in field.items():
    L.append('- **%s**: ' % k + ', '.join('%s %+d' % (s, v) for s, v in row.items() if v is not None))
L += ['', '## Where the hurt collects', '']
for k, v in hurt.items(): L.append('- **%s**: %d hurts (%s)' % (k, len(v), '; '.join('%s→%s' % x for x in v)))
L += ['', '## Open problems (the net to cast)', '', '| problem | field | state |', '|---|---|---|'] + ['| %s | %s | %s |' % p for p in open_problems]
open('tools/project_docs/WEAVE_FIELD_MAP.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
