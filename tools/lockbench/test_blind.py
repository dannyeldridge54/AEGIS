# AEGIS-FP BCWTTBU4C3RTON6L · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import sys, os, tempfile, shutil; sys.path.insert(0, '.')
import tools.lockbench.blind as B
d = tempfile.mkdtemp(); B.SEALED = f'{d}/sealed'; B.INDEX = f'{B.SEALED}/INDEX.jsonl'
res = f'{d}/r.txt'; open(res, 'w').write('ns 0.96 secret detail\nVERDICT: VALIDATED\n'); dn = f'{d}/dn.md'
v = B.seal(res, 'L.md'); assert v['verdict'] == 'VALIDATED' and not os.path.exists(res)
open(dn, 'w').write('## D9 — something else\nNOT VALIDATED? no\n')
try: B.unseal(res, 'D10', dnotes=dn); raise SystemExit('FAIL: unsealed without D-note')
except PermissionError: pass
open(dn, 'a').write('## D10 — test\nresult sealed earlier\n')
try: B.unseal(res, 'D10', dnotes=dn); raise SystemExit('FAIL: unsealed without verdict stated')
except PermissionError: pass
open(dn, 'a').write('verdict VALIDATED\n'); B.unseal(res, 'D10', dnotes=dn); assert 'secret detail' in open(res).read()
res2 = f'{d}/r2.txt'; open(res2, 'w').write('VERDICT: PASS\n'); B.seal(res2, 'L.md')
s = [r for r in B._index() if r['results'] == res2][0]['sealed']; open(s, 'a').write('x')
open(dn, 'a').write('## D11\nPASS\n')
try: B.unseal(res2, 'D11', dnotes=dn); raise SystemExit('FAIL: tamper missed')
except RuntimeError: pass
print('test_blind: PASS (seal hides file, no D-note refused, verdict-missing refused, unseal restores, tamper detected)')
