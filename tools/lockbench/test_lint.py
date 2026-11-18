# AEGIS-FP LZBIDRGZYF2MGJSV · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import sys, os, tempfile; sys.path.insert(0, '.')
from tools.lockbench.lint import lint
d = tempfile.mkdtemp()
def mk(name, body):
    p = os.path.join(d, name); open(p, 'w').write(body); return p
L8 = mk('l8.md', '```claims\n- {id: C1, quantity: chi2, op: "<=", value: 1}\n```\n```design\nn_params: 3\nn_data: 3\n```\n')
D1039 = mk('d1039.md', '```claims\n- {id: C2, quantity: rel, reduce: max, op: "<=", value: 0.05, reference_spread: 0.07}\n```\n')
JMF1 = mk('jmf1.md', '```claims\n- {id: C1, quantity: dns, op: "<=", value: 2e-4, reference_kind: approximation}\n```\n')
s_bad = mk('job_bad.py', 'for m in models:\n    run(m)\n'); s_ok = mk('job_ok.py', 'from tools.calcq.sweep import sweep\nsweep(tasks, f, part=PART, limit=1200)\n')
J7h = mk('j7h.md', f'```claims\n- {{id: C1, quantity: x, op: "<=", value: 1}}\n```\n```design\nscript: {s_bad}\n```\n')
GOOD = mk('good.md', f'```claims\n- {{id: C1, quantity: dns, op: "<=", value: 2e-4, reference_kind: exact, reference_spread: 1e-5}}\n```\n```design\nn_params: 3\nn_data: 16\nscript: {s_ok}\n```\n')
assert any('degenerate' in p for p in lint(L8)); assert any('tighter' in p for p in lint(D1039)); assert any('APPROXIMATION' in p for p in lint(JMF1))
pj = lint(J7h); assert any('wall limit' in p for p in pj) and any('resumable' in p for p in pj)
assert lint(GOOD) == [], lint(GOOD)
print('test_lint: PASS (catches L8, D1039, JMF1, J7h; clean lock passes)')
