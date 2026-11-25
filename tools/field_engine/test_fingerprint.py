"""Tests for the fingerprint index. Run: python -m unittest -v test_fingerprint"""
import asyncio, json, os, sqlite3, tempfile, unittest
from pathlib import Path
import fingerprint as F

class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp()); (self.d / 'code.py').write_text('x = 1\n')
        self.fp = F.Index(self.d / 'fp.sqlite', 'Danny Eldridge', key='ab' * 32)
    def test_stamp_is_deterministic_tagged_linked_and_signed(self):
        a = self.fp.stamp('check', inputs={'s': 2}, outputs={'E': 5.783}, code=['code.py'], tags={'sector': 'serapis_e', 'layer': 'L1'},
                          links=[('stream:modular/rho', 1, 'anchors_on')], root=self.d)
        self.assertEqual(a, self.fp.stamp('check', inputs={'s': 2}, outputs={'E': 5.783}, code=['code.py'], tags={'layer': 'L1', 'sector': 'serapis_e'},
                                          links=[('stream:modular/rho', 1, 'anchors_on')], root=self.d))
        self.assertTrue(self.fp.verify(a)); self.assertEqual(self.fp.find(tag=('sector', 'serapis_e')), [a])
        self.assertEqual(self.fp.links_of(a)[0]['target'], 'stream:modular/rho'); self.assertEqual(self.fp.get(a)['owner'], 'Danny Eldridge')
    def test_code_change_gives_a_new_fingerprint(self):
        a = self.fp.stamp('check', code=['code.py'], root=self.d); (self.d / 'code.py').write_text('x = 2\n')
        self.assertNotEqual(a, self.fp.stamp('check', code=['code.py'], root=self.d))
    def test_append_only_and_tamper_and_wrong_owner_are_caught(self):
        a = self.fp.stamp('check', outputs={'v': 1})
        with self.assertRaises(sqlite3.IntegrityError): self.fp.db.execute('DELETE FROM records')
        with self.assertRaises(sqlite3.IntegrityError): self.fp.db.execute("UPDATE records SET payload='x'")
        other = F.Index(self.d / 'fp.sqlite', 'Danny Eldridge', key='cd' * 32); self.assertFalse(other.verify(a))
    def test_stream_walks_levels(self):
        a = self.fp.stamp('derivation', links=[('stream:ufe', 1, 'part_of')]); b = self.fp.stamp('check', links=[(a, 2, 'checks')])
        c = self.fp.stamp('test', links=[(b, 3, 'tests')]); self.assertEqual(self.fp.stream('stream:ufe'), {0: [a], 1: [b], 2: [c]})
    def test_engine_writes_signed_records_when_enabled(self):
        import engine as E, ufe_pack as U
        os.environ['ENGINE_INDEX'] = str(self.d / 'eng.sqlite'); os.environ['AEGIS_OWNER'] = 'Danny Eldridge'
        saved = dict(E.TOOLS)
        try:
            U.register(E); truths = {}
            def fn(p): return json.dumps({'steps': ['f'], 'result': next(v for k, v in truths.items() if p.startswith(k))})
            eng = E.Engine(self.d / 'home', [E.Mock('A', fn), E.Mock('B', fn)], seed=2, samples=1); f0 = eng.frame
            def frame(t, r):
                fr = f0(t, r); truths[fr['prompt']] = float(E.TOOLS[t][2](fr['args'])); return fr
            eng.frame = frame; asyncio.run(eng.batch(4))
            ids = eng.index.find(kind='engine_result'); self.assertEqual(len(ids), 4); self.assertTrue(all(eng.index.verify(i) for i in ids))
            self.assertTrue(eng.index.find(tag=('status', 'CONDITIONAL')) or eng.index.find(tag=('status', 'DERIVED')))
        finally:
            del os.environ['ENGINE_INDEX']; E.TOOLS.clear(); E.TOOLS.update(saved)
            for k in U.TOOLS: E.META.pop(k, None)
if __name__ == '__main__': unittest.main()
