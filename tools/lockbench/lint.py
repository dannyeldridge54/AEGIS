# AEGIS-FP ILSENDMMY34TWM4I · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L-2: lock linter — run before a lock is committed. Returns a list of problems (empty = clean).
Reads the ```claims block (claims.py) and an optional ```design block:
```design
n_params: 3            # free parameters fitted
n_data: 16             # data points
script: theory/x.py    # job script (checked for per-task wall limit + resume)
```
Per-claim optional keys: reference_kind (exact | data | approximation), reference_spread (relative spread of the reference itself), relative (true/false)."""
import re, os, yaml
from .claims import parse
def _block(text, name):
    m = re.search(rf'```{name}\n(.*?)```', text, re.S); return yaml.safe_load(m.group(1)) if m else {}
def lint(lock_path):
    text = open(lock_path).read(); P = []
    try: C = parse(text)
    except ValueError as e: return [f'claims: {e}']
    d = _block(text, 'design') or {}
    if 'n_params' in d and 'n_data' in d and d['n_params'] >= d['n_data']:
        P.append(f"degenerate fit: n_params {d['n_params']} >= n_data {d['n_data']} (chi2 = 0 is automatic)  [cf. L8/D1047]")
    for c in C:
        rs = c.get('reference_spread')
        if rs is not None and c.get('relative', True) and c['op'] in ('<=', '<', 'abs<=') and float(c['value']) < float(rs):
            P.append(f"{c['id']}: tolerance {c['value']} tighter than the reference's own spread {rs}  [cf. D1039]")
        if c.get('reference_kind') == 'approximation':
            P.append(f"{c['id']}: compares against an APPROXIMATION — compare to an exact reference or data instead  [cf. JMF1/D1161]")
    s = d.get('script')
    if s:
        if not os.path.exists(s): P.append(f'script {s} not found')
        else:
            src = open(s).read()
            if not re.search(r'sweep\(|timeout=|wall limit|limit=', src): P.append(f'{s}: no per-task wall limit  [cf. J7h kmiii, S4e2]')
            if not re.search(r'part\b|PART|resume|done =', src): P.append(f'{s}: not resumable (no part file)  [cf. J7g restarts]')
    return P
