"""D1662 / Janus genesis G12c (PREREG_D1662_G12C_REFEREE)."""
import json, re, subprocess, shutil
subprocess.run(['python3', 'field_tests/scripts/janus_g/g12b_referee.py'], capture_output=True, text=True)
r = json.load(open('field_tests/results/D1660_G12b_referee.json'))
txt = open('theory/pending_docs/D72_D75_weak_spots.md').read()
def sec(n):
    m = re.search(rf'(?ms)^## {n}\b.*?(?=^## D|\Z)', txt); return m.group(0) if m else ''
cover = {'D1646': sec('D1646a') and sec('D1654'), 'D1632': sec('D1661'), 'D1648': sec('D1661'), 'D1649': sec('D1661')}
covered = {k: bool(v) and ('2603.13226' in (sec('D1661') + sec('D1654'))) for k, v in cover.items()}
old = {'D1632', 'D1633', 'D1637', 'D1642', 'D1644', 'D1646', 'D1648', 'D1649', 'D1650', 'D1651', 'D1657'}
flags = [f['note'] for f in r['source_flags']]; new = sorted(set(flags) - old)
out = dict(D='D1662', order_ok=r['order_ok'], arith_ok=r['arith_ok'], card=r['card'], flags=flags, new_flags=new, covered=covered,
           mechanics_ok=r['order_ok'] and r['arith_ok'] and r['card'].endswith('CONSISTENT []'), all_covered=all(covered.values()))
json.dump(out, open('field_tests/results/D1662_G12c_referee.json', 'w'), indent=1)
subprocess.run(['git', 'checkout', '--', 'field_tests/results/D1660_G12b_referee.json'])   # keep D1660's own result unchanged
print(json.dumps(out, indent=1))
