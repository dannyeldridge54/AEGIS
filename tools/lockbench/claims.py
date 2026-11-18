# AEGIS-FP LIIPGMJE4EPFDUDU · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L-1: machine-readable claims. A lock may carry a fenced block

```claims
- id: C1
  quantity: dns            # key in the results dict the job emits (number or list of numbers)
  reduce: max              # one of: value, all, any, max, min, median, mean
  op: "<="                 # <=, <, >=, >, ==, abs<= (|x| <= v)
  value: 2.0e-4
  label: "|n_s - n_s(MMC)| at every R"
```
evaluate(lock_path, results) -> dict(claims=[...], verdict=bool). Scripts emit numbers only; LOCKBENCH decides (no hand-coded verdict strings)."""
import re, statistics, yaml
OPS = {'<=': lambda x, v: x <= v, '<': lambda x, v: x < v, '>=': lambda x, v: x >= v, '>': lambda x, v: x > v, '==': lambda x, v: x == v, 'abs<=': lambda x, v: abs(x) <= v}
def parse(text):
    m = re.search(r'```claims\n(.*?)```', text, re.S)
    if not m: raise ValueError('lock has no ```claims block')
    C = yaml.safe_load(m.group(1))
    for c in C:
        for k in ('id', 'quantity', 'op', 'value'):
            if k not in c: raise ValueError(f'claim missing {k}: {c}')
        if c['op'] not in OPS: raise ValueError(f"bad op {c['op']}")
        c.setdefault('reduce', 'value')
    return C
def _reduce(x, how):
    if how == 'value': return [float(x)] if not isinstance(x, (list, tuple)) else [float(v) for v in x]
    xs = [float(v) for v in x] if isinstance(x, (list, tuple)) else [float(x)]
    return {'all': xs, 'any': xs, 'max': [max(xs)], 'min': [min(xs)], 'median': [statistics.median(xs)], 'mean': [statistics.fmean(xs)]}[how]
def evaluate(lock_path, results):
    out = []; ok = True
    for c in parse(open(lock_path).read()):
        if c['quantity'] not in results: r = dict(c, passed=False, why='quantity not emitted'); ok = False; out.append(r); continue
        xs = _reduce(results[c['quantity']], c['reduce']); f = OPS[c['op']]
        p = any(f(x, float(c['value'])) for x in xs) if c['reduce'] == 'any' else all(f(x, float(c['value'])) for x in xs)
        ok &= p; out.append(dict(c, passed=bool(p), observed=xs if len(xs) > 1 else xs[0]))
    return dict(claims=out, verdict=bool(ok))
