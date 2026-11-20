from tools import nested_guard as G
NEST = [('lcdm', 'thread'), ('thread', 'coupled')]
def test_d1725_pantheon_is_flagged():       # real D1713 numbers (Pantheon+): coupled 2432.28 vs thread 2430.14
    chi2 = {'lcdm': 2432.76, 'thread': 2430.14, 'coupled': 2432.28}
    v = G.check(chi2, NEST); assert len(v) == 1 and v[0]['outer'] == 'coupled' and abs(v[0]['excess'] - 2.14) < 1e-9
    assert G.best_lower_bound(chi2, NEST)['coupled'] == 2430.14
def test_d1724_transitive():                # original coupled run sat +0.90 above ΛCDM
    chi2 = {'lcdm': 2432.76, 'thread': 2430.14, 'coupled': 2433.66}
    assert G.best_lower_bound(chi2, NEST)['coupled'] == 2430.14 and 'VIOLATION' in G.report(chi2, NEST)
def test_clean_and_tolerance():
    assert G.report({'lcdm': 10.0, 'thread': 9.0, 'coupled': 9.3}, NEST, tol=0.5) == 'NESTED OK'
