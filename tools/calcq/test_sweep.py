import os, sys, time, json, tempfile; sys.path.insert(0, '.')
from tools.calcq.sweep import sweep
def f(t):
    if t == 3: time.sleep(5)
    if t == 4: raise ValueError('boom')
    return {'sq': t*t}
if __name__ == '__main__':
    part = os.path.join(tempfile.mkdtemp(), 'p.jsonl')
    R = sweep([1, 2, 3, 4], f, part, limit=2, ncpu=2, log=lambda s: None); S = {r['key']: r for r in R}
    assert S[1]['result'] == {'sq': 1} and S[2]['status'] == 'ok' and S[3]['status'] == 'timeout' and S[4]['status'] == 'error'
    R2 = sweep([1, 2, 3, 4, 5], f, part, limit=2, ncpu=2, log=lambda s: None)   # resume: only task 5 runs
    assert len(R2) == 5 and {r['key'] for r in R2} == {1, 2, 3, 4, 5}
    print('test_sweep: PASS')
