"""J7i (locked PREREG_J7i_fi_parser): rescore FI with a Fortran 3-digit-exponent-aware float parser."""
import sys, re, builtins, importlib.util; sys.path.insert(0, '.')
sp = importlib.util.spec_from_file_location('j7f', 'theory/janus/j7f_pulse.py'); F = importlib.util.module_from_spec(sp); sp.loader.exec_module(F)
_f = builtins.float
def ffloat(s):
    if isinstance(s, str): s = re.sub(r'(\d)([+-]\d{3})$', r'\1E\2', s.strip())
    return _f(s)
F.parse.__globals__['float'] = ffloat
F.P = {'fi': F.P['fi']}; F.PART = 'field_tests/results/janus_j7i.part.jsonl'
if __name__ == '__main__':
    F.run(); import json
    for l in open(F.PART): print(l.strip()[:300])
