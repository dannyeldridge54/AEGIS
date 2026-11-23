"""CubeMind v5c (22 Nov 2026, Danny 22:17-22:18): "run the engine alongside itself: postulate, then use the engine, and it will check itself".
Patches mindmem/learn_loop.py step_derive (backup .bak_v5c_22nov):
 1. POSTULATE: the model also writes its formula as one arithmetic expression ("expr") in the task's input names.
 2. ENGINE ALONGSIDE: the expression is evaluated exactly (safe math evaluator) -> formula_ok, graded separately from its own arithmetic.
 3. SELF-CHECK: when its number is wrong, it is shown the engine's value and its own steps, must name the first wrong step and its class
    (formula / units / arithmetic / reading), and write one rule. The rule is stored per tool (kind derivation_rule) and the 4 newest
    rules FOR THAT TOOL go into its next prompt for that tool. Never deletes; the tool's number stays the grade."""
import pathlib, sys, shutil
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
if 'derivation_rule' in s: print('already patched'); sys.exit(0)
shutil.copy(p, str(p) + '.bak_v5c_22nov')
old_lessons = "        lessons = [r['text'] for r in S.recs if r.get('kind') == 'derivation_failed'][-4:]\n"
new_lessons = ("        lessons = [r['text'] for r in S.recs if r.get('kind') == 'derivation_rule' and ('[' + tool + ']') in r.get('text', '')][-4:] \\\n"
               "                  or [r['text'] for r in S.recs if r.get('kind') == 'derivation_failed'][-4:]\n")
assert old_lessons in s; s = s.replace(old_lessons, new_lessons)
old_reply = """                  '\\nReply JSON only: {"steps": [<strings>], "result": <number>}')"""
new_reply = """                  '\\nAlso write your formula as ONE arithmetic expression "expr" using the input names exactly as given (python syntax; math functions sqrt, log, exp, pi, sin, cos allowed; ** for powers). The engine will evaluate it exactly alongside you.'
                  '\\nReply JSON only: {"steps": [<strings>], "expr": "<expression>", "result": <number>}')"""
assert old_reply in s; s = s.replace(old_reply, new_reply)
old_ok = "        true = float(res[key]); ok = abs(mine - true) <= tol * max(abs(true), 1e-30)\n"
new_ok = old_ok + """        expr_val = _safe_eval(j.get('expr'), args); formula_ok = (expr_val is not None) and abs(expr_val - true) <= tol * max(abs(true), 1e-30)
        rule = err_class = None
        if not ok:
            try:
                _sc = ("You are CubeMind checking your own derivation against the engine. Task: " + task.replace('{x}', _j.dumps(args)) +
                       "\\nYour steps: " + _j.dumps(j.get('steps'))[:1500] + f"\\nYour result: {mine}. Your expression evaluated exactly: {expr_val}. The engine's value: {true}." +
                       "\\nFind the FIRST wrong step. Classify it as one of: formula, units, arithmetic, reading (misread the task or the definition)." +
                       " Then write ONE short general rule that would have prevented it (no numbers from this task)." +
                       '\\nReply JSON only: {"first_wrong_step": <int>, "class": "<formula|units|arithmetic|reading>", "rule": "<one sentence>"}')
                _b2 = dict({'model': model, 'prompt': _sc, 'stream': False, 'options': {'temperature': 0.1, 'num_predict': 300}}, **_nothink(model))
                _j2 = _extract_json(LM._post('/api/generate', _b2).get('response', '')) or {}
                err_class = str(_j2.get('class', ''))[:12]; rule = str(_j2.get('rule', ''))[:240]
                if formula_ok and err_class == 'formula': err_class = 'arithmetic'   # engine shows its formula was right
                if rule:
                    S.add(f"RULE [{tool}] ({err_class}): {rule}", 'cubemind_selfcheck', kind='derivation_rule', tier='HYPOTHESIS', topic='weave', importance=3)
            except Exception: pass
"""
assert old_ok in s; s = s.replace(old_ok, new_ok)
old_log = "'tool_value': true, 'ok': ok, 'model': model, 'steps': j.get('steps')}"
new_log = "'tool_value': true, 'ok': ok, 'model': model, 'steps': j.get('steps'), 'expr': j.get('expr'), 'expr_value': expr_val, 'formula_ok': formula_ok, 'err_class': err_class, 'rule': rule, 't': time.time()}"
assert old_log in s; s = s.replace(old_log, new_log)
old_ret = "        return {'derive': tool, 'derive_ok': ok, 'derive_score': f'{nok}/{nok + nbad}', 'model': model}"
new_ret = "        return {'derive': tool, 'derive_ok': ok, 'formula_ok': formula_ok, 'err_class': err_class, 'derive_score': f'{nok}/{nok + nbad}', 'model': model}"
assert old_ret in s; s = s.replace(old_ret, new_ret)
helper = '''
def _safe_eval(expr, args):
    """v5c: evaluate CubeMind's own formula exactly (the engine alongside it). Only math names and the task's inputs; no builtins."""
    import math as _m, ast as _ast
    if not isinstance(expr, str) or len(expr) > 400: return None
    env = {k: getattr(_m, k) for k in ('sqrt', 'log', 'log10', 'exp', 'pi', 'e', 'sin', 'cos', 'tan', 'atan', 'atan2', 'cbrt') if hasattr(_m, k)}
    env['abs'] = abs; env['zeta2'] = _m.pi ** 2 / 6; env['zeta3'] = 1.2020569031595942
    for k, v in (args or {}).items():
        if isinstance(v, (int, float)): env[k] = float(v)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, (int, float)): env[f'{k}{i}'] = float(x)
            env[k] = [float(x) for x in v if isinstance(x, (int, float))]
    try:
        t = _ast.parse(expr.replace('^', '**'), mode='eval')
        for n in _ast.walk(t):
            if isinstance(n, (_ast.Attribute, _ast.Lambda, _ast.comprehension)) or (isinstance(n, _ast.Name) and n.id.startswith('_')): return None
        v = eval(compile(t, '<cm>', 'eval'), {'__builtins__': {}}, env)
        return float(v) if isinstance(v, (int, float)) and _m.isfinite(v) else None
    except Exception: return None

'''
s = s.replace('def step_derive():', helper + 'def step_derive():', 1)
p.write_text(s, encoding='utf-8'); print('patched')
