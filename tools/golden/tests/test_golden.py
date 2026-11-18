# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
from tools.golden.golden import compare
def test_drift_is_caught():
    old = {'a': 1.0, 'b': {'c': [2.0, 3.0]}}
    assert compare(old, old) == []
    assert compare(old, {'a': 1.0, 'b': {'c': [2.0, 3.0001]}}) == ['.b.c[1]: 3.0 -> 3.0001']
    assert compare(old, {'a': 1.0}) == ['.b.c[0] missing', '.b.c[1] missing']
