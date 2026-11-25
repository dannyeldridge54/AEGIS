"""Tests for UFE stages 2-4. Run from tools/field_engine: python -m unittest -v test_ufe_stages"""
import unittest
import ufe_stages as S

class T(unittest.TestCase):
    def test_direct_sum_is_independent_and_close(self):
        from tools.serapis_calc import shapes
        self.assertLess(abs(S.direct_sum(S.RHO, 2.0, R=80) - shapes.E(S.RHO, 2.0)) / shapes.E(S.RHO, 2.0), 1e-4)
    def test_every_symbolic_step_reproduces(self):
        self.assertTrue(all(x['verdict'] == 'REPRODUCES' for x in S.stage3()))
    def test_finder_reports_known_disagreements_and_only_real_ones(self):
        found = [x['quantity'] for x in S.stage4()]; self.assertTrue(all(e in found for e in S.EXPECTED))
        self.assertEqual(S.stage4([('q', 'a', 1.0, ''), ('q', 'b', 1.0 + 1e-9, ''), ('p', 'a', 3.0, '')]), [])
        self.assertEqual(len(S.stage4([('q', 'a', 1.0, ''), ('q', 'b', 1.1, '')])), 1)
if __name__ == '__main__': unittest.main()
