"""CM-CARDS DEV-4/5 patch for CubeMind's mindmem/learn_loop.py (run on the PC from the CubeMind_janus folder: python patch_cm_speed.py).
Idempotent; backs up to learn_loop.py.bak_dev45. DEV-6 needs no patch: derivations.jsonl already records formula_ok (= calc_ok)."""
import pathlib, shutil, sys
p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'mindmem/learn_loop.py'); s = p.read_text(encoding='utf-8')
if 'CM-CARDS DEV-4' in s: print('already patched'); sys.exit(0)
if 'CM-CARDS (23 Nov 2026)' not in s: sys.exit('cards patch missing: apply the CM-CARDS learn_loop patch first')
A = "_body = dict({'model': model, 'prompt': prompt, 'stream': False, 'options': {'temperature': 0.2, 'num_predict': 900}}, **_nothink(model))"
B = "        if not ok:\n            try:\n                _sc = ("
assert s.count(A) == 1 and s.count(B) == 1, 'anchors not found exactly once'
s = s.replace(A, A.replace("'num_predict': 900", "'num_predict': (600 if _facts else 900)") + "   # CM-CARDS DEV-5: shorter replies on card tasks")
s = s.replace(B, "        if not ok and formula_ok:   # CM-CARDS DEV-4: formula right, hand arithmetic wrong -> no self-check model call\n"
                 "            err_class = 'arithmetic'; rule = 'Your formula was right; evaluate the expression exactly instead of doing long arithmetic by hand.'\n"
                 "            try: S.add(f'RULE [{tool}] (arithmetic): ' + rule, 'cubemind_selfcheck', kind='derivation_rule', tier='HYPOTHESIS', topic='weave', importance=3)\n"
                 "            except Exception: pass\n"
                 "        if not ok and not formula_ok:\n            try:\n                _sc = (")
shutil.copy(p, str(p) + '.bak_dev45'); p.write_text(s, encoding='utf-8'); compile(s, str(p), 'exec'); print('patched', p)
