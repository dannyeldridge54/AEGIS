"""Tests for the neural web. Run: python -m unittest -v test_neural_web"""
import tempfile, unittest
from pathlib import Path
import fingerprint as F, neural_web as N

class T(unittest.TestCase):
    def setUp(self):
        self.ix = F.Index(Path(tempfile.mkdtemp()) / 'w.sqlite', 'Danny Eldridge', key='ab' * 32); self.web = N.Web(self.ix, cap=6)
    def rec(self, i, side, layer, good=True, area='ufe', links=()):
        t = dict(side=side, layer=layer, area=area, status='DERIVED' if good else '', tested=str(good), locked=str(good), fits='0' if good else '6')
        return self.ix.stamp('check', inputs={'i': i}, outputs={'v': i}, tags=t, links=links)
    def test_scales_mean_something(self):
        g = N.scales_from(self.ix.get(self.rec(1, 'left', 'torus', True))); b = N.scales_from(self.ix.get(self.rec(2, 'left', 'torus', False)))
        self.assertGreater(sum(g.values()), 3); self.assertLess(sum(b.values()), 0)
    def test_web_grows_by_splitting_and_separates_left_from_right(self):
        ids = [self.rec(i, 'left' if i % 2 else 'right', 'cosmology') for i in range(20)]
        for r in ids: self.web.place(r)
        leaves = [s for s in self.web.sheet() if s['leaf']]; self.assertGreater(len(leaves), 1)
        for s in leaves:
            if s['records']: self.assertTrue(abs(s['side']) > 0.99, s)                     # no leaf mixes the two ladders
    def test_one_record_lives_in_several_perspectives(self):
        r = self.rec(1, 'centre', 'torus'); out = self.web.place(r, views={'early': {'side': 'left'}, 'late': {'side': 'right'}})
        self.assertEqual(set(out), {'early', 'late'})
    def test_links_strengthen_synapses_and_mining_reaches_out(self):
        a = self.rec(1, 'left', 'cosmology'); self.web.place(a)
        for i in range(8): self.web.place(self.rec(10 + i, 'right', 'late universe'))
        b = self.rec(2, 'right', 'late universe', links=[(a, 1, 'tension_with')]); self.web.place(b)
        self.assertTrue(self.web.synapses())
        leaf = self.web.leaf_for(N.shape(self.ix.get(b))); props = self.web.mine(leaf, radius=3.0)
        self.assertTrue(all(p['src'] != p['dst'] for p in props)); self.assertTrue(props)
    def test_grading_teaches_which_qualities_predict_being_right(self):
        good = [self.rec(i, 'left', 'torus', True) for i in range(15)]; bad = [self.rec(100 + i, 'left', 'torus', False) for i in range(15)]
        for _ in range(5):
            for r in good: self.web.grade(r, True)
            for r in bad: self.web.grade(r, False)
        self.assertGreater(self.web.trust(good[0]), 0.8); self.assertLess(self.web.trust(bad[0]), 0.2); self.assertGreater(self.web.w['diligence_sloth'], 0)
    def test_state_survives_reopen(self):
        for i in range(10): self.web.place(self.rec(i, 'left', 'torus'))
        n = len(self.web.sheet()); self.assertEqual(len(N.Web(self.ix, cap=6).sheet()), n)
if __name__ == '__main__': unittest.main()
