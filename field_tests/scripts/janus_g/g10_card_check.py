"""D1647 / Janus genesis G10: machine check of docs/JANUS_GENESIS_CARD.md against its source jsons (PREREG_D1647_G10_CARD)."""
import json, re
rows, bad = [], []
for line in open('docs/JANUS_GENESIS_CARD.md'):
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(c) != 4 or not c[2].startswith('field_tests/'): continue
    q, v, f, k = c
    x = json.load(open(f))
    for part in k.split('.') if not k.startswith('beta=') else [k.split('.P')[0], 'P' + k.split('.P')[1]]:
        x = x[int(part)] if isinstance(x, list) else x[part]
    try:
        cv = float(v); mant = re.sub(r'e.*', '', v).lstrip('-').replace('.', '').lstrip('0'); sig = max(len(mant), 1)
        ok = abs(cv / float(x) - 1) <= 0.6 * 10 ** (1 - sig)
    except ValueError:
        ok = str(x) == v
    rows.append(dict(q=q, card=v, json=x, ok=ok))
    if not ok: bad.append(q)
out = dict(D='D1647', n_rows=len(rows), mismatches=bad, verdict='CONSISTENT' if not bad else 'MISMATCH', rows=rows)
json.dump(out, open('field_tests/results/D1647_G10_card_check.json', 'w'), indent=1, default=str)
print(out['n_rows'], out['verdict'], bad)
