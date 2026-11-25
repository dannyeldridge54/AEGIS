"""Tests for the UFE pack (no LLM needed). Run: python -m unittest -v test_ufe_pack"""
import asyncio, json, random, tempfile, unittest
import engine as E, ufe_pack as U

class T(unittest.TestCase):
    def test_every_ufe_tool_passes_its_independent_tester_on_all_rings(self):
        r = random.Random(5)
        for name, (area, text, fit, test, tol, mk) in U.TOOLS.items():
            for ring in range(4):
                for _ in range(60):
                    a = mk(r, ring); self.assertTrue(test(a, fit(a)), (name, ring, a))
    def test_testers_catch_wrong_formulas(self):
        self.assertFalse(U._lap_test({'s': 1.5}, 1.5 * 2.5))                                   # s(s+1) instead of s(s-1)
        self.assertFalse(U._slope_test({'b': -0.1, 'rho_c': 1.0, 'Vpp': 1.0}, 3 * -0.1 * 1.0 / 1.0))   # b^2 rho_c dropped
        a = {'mu_e2': 1.0, 'mu_w2': 2.0, 'eta': 0.5, 'kappa': 0.3, 'Delta': 0.7}
        p, q = 1.0 + 1.0 + 0.6 * 0.49, 2.0 + 1.0 + 0.6 * 0.49
        self.assertFalse(U._hmin_test(a, ((p + q) + ((p - q) ** 2 + 4) ** 0.5) / 2))            # the LARGER root
        self.assertFalse(U._thread_test({'b': -0.074, 'rho_c': 1.0}, -0.074 * (-0.074 - U.BETA)))  # sign of beta flipped
        self.assertFalse(U._growth_test({'t1': 1.0, 't2': 8.0}, 8.0 ** 0.5))                    # radiation-era exponent
        d = {'y': 1.0, 's': 1.0, 'gamma': 0.2, 'E': 3.0, 'Ex': 0.1, 'Ey': 2.0}
        self.assertFalse(U._det_test(d, (1 + 2 * 0.2 * 3.0) ** 2 / 16))                         # mixing term dropped
    def test_audit_facts(self):
        self.assertEqual(U._lap({'s': 2}), 2); self.assertEqual(U._lap({'s': 1.5}), 0.75)       # the eigenvalue mismatch
        self.assertLess(U._thread({'b': -0.074, 'rho_c': 1.0}), 0)                              # b = -0.074 is a saddle
        self.assertGreater(U._thread({'b': -3.5, 'rho_c': 1.0}), 0)                             # b < -beta can be positive
    def test_sectors_are_never_merged_without_a_bridge(self):
        ok, st, why = U.combine('weave_v4', 'serapis_e'); self.assertFalse(ok); self.assertEqual(st, 'OPEN')
        ok, st, why = U.combine('yfork2', 'serapis_e'); self.assertTrue(ok); self.assertEqual(st, 'CONDITIONAL'); self.assertTrue(any('ASSUMED' in w for w in why))
        self.assertEqual(U.combine('yfork2', 'yfork2')[0], True)
    def test_gates_cannot_become_tools(self):
        self.assertTrue(all(k not in U.TOOLS for _, k, _ in U.GATES)); self.assertTrue(any(s == 'BLOCKED' for s, _, _ in U.GATES))
        U.TOOLS['bad'] = U.TOOLS['ufe_laplace']; U.META['bad'] = dict(status='OPEN')
        try:
            with self.assertRaises(ValueError): U.register(E)
        finally:
            del U.TOOLS['bad'], U.META['bad']; E.TOOLS.pop('bad', None)
    def test_engine_runs_the_pack_and_logs_status_with_every_lock(self):
        saved = dict(E.TOOLS)
        try:
            for k in list(E.TOOLS): del E.TOOLS[k]
            U.register(E); truths = {}
            def fn(prompt): return json.dumps({'steps': ['formula'], 'result': next(v for k, v in truths.items() if prompt.startswith(k))})
            eng = E.Engine(tempfile.mkdtemp(), [E.Mock('A', fn), E.Mock('B', fn)], seed=3, samples=2, serial=True); f0 = eng.frame
            def frame(tool, ring):
                fr = f0(tool, ring); truths[fr['prompt']] = float(E.TOOLS[tool][2](fr['args'])); return fr
            eng.frame = frame
            for _ in range(6): asyncio.run(eng.batch(4))
            recs = [json.loads(l) for l in eng.ledger.read_text().splitlines()]
            locks = [r for r in recs if r['kind'] == 'lock']
            self.assertTrue(all(r['meta'] and r['meta']['status'] in ('DERIVED', 'CONDITIONAL') and r['meta']['not_a'] for r in locks))
            self.assertEqual({r['tool'] for r in locks}, set(U.TOOLS)); self.assertFalse([r for r in recs if r['kind'] == 'void'])
            self.assertTrue(all(r['point_ok'] for r in recs if r['kind'] == 'result')); self.assertTrue(E.verify_ledger(eng.ledger)[1])
        finally:
            for k in list(E.TOOLS): del E.TOOLS[k]
            E.TOOLS.update(saved)
            for k in U.TOOLS: E.META.pop(k, None)
if __name__ == '__main__': unittest.main()
