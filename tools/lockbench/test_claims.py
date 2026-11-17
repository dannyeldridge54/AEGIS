import sys, os, tempfile; sys.path.insert(0, '.')
from tools.lockbench.claims import evaluate
lock = '''# test lock\n```claims\n- id: C1\n  quantity: dns\n  reduce: all\n  op: "<="\n  value: 2.0e-4\n- id: C2\n  quantity: drr\n  reduce: max\n  op: "<="\n  value: 2.0e-3\n```\n'''
p = os.path.join(tempfile.mkdtemp(), 'L.md'); open(p, 'w').write(lock)
# JMF2's own numbers (D1162) must pass; JMF1's δN errors (D1161) must fail C1
a = evaluate(p, dict(dns=[6.3e-6, 3.3e-8, 4.7e-6], drr=[1.2e-4, 2.2e-5, 1.4e-5])); assert a['verdict'] is True
b = evaluate(p, dict(dns=[1.3e-4, 7.6e-4, 1.7e-3], drr=[1e-4])); assert b['verdict'] is False and b['claims'][0]['passed'] is False and b['claims'][1]['passed'] is True
c = evaluate(p, dict(dns=[1e-6])); assert c['verdict'] is False and c['claims'][1]['why'] == 'quantity not emitted'
import numpy as np; d = evaluate(p, dict(dns=[np.float64(1e-6)], drr=np.float64(1e-4))); assert d['verdict'] is True and isinstance(d['verdict'], bool)  # numpy-bool trap (J7b)
print('test_claims: PASS')
