"""JANUS tick 76: check the card's data-tensions rows against D1471/D1472 jsons (PREREG_D1473)."""
import json, re
a = json.load(open('field_tests/results/D1471_lya_running.json'))['pulls']; b = json.load(open('field_tests/results/D1472_spt3g.json'))['pulls']
qmap = {'α_s': 'a', 'β_s': 'b', 'n_s': 'ns'}; mism = []; n = 0
for line in open('docs/JANUS_FORMULAS.md'):
    m = re.match(r'\| (2511\.01612|2506\.20707)[^|]*\| ([^|]+) \| ([^|]+) \| ([+-][0-9.]+)σ \| ([+-][0-9.]+)σ \|', line)
    if not m: continue
    n += 1; src, comb, qty, pr, pt = m.group(1), m.group(2).strip(), m.group(3).strip(), float(m.group(4)), float(m.group(5))
    if src == '2511.01612': jr, jt = a['rho_A1'][comb][qmap[qty]], a['tau_i_NA12'][comb][qmap[qty]]
    else: jr, jt = b['rho_A1'][comb], b['tau_i_NA12'][comb]
    if round(jr, 2) != pr or round(jt, 2) != pt: mism.append(dict(row=line.strip(), json=[jr, jt]))
out = dict(D='D1473', rows_checked=n, mismatches=mism, verdict='CONSISTENT' if (n == 15 and not mism) else 'MISMATCH')
json.dump(out, open('field_tests/results/D1473_card_tensions.json', 'w'), indent=1); print(out)
