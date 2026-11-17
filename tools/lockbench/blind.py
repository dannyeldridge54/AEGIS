"""L-3: blind mode. A finished job seals its full results; only the claims verdict is visible until a D-note records that verdict.
seal(results, lock) -> verdict dict (runs claims.evaluate on the parsed numbers, moves the file to field_tests/sealed/, records sha256)
unseal(results, dnote_id, dnotes=...) -> restores the file only if the D-note exists and states the sealed verdict; verifies the hash."""
import hashlib, json, os, shutil, re
SEALED = 'field_tests/sealed'; INDEX = f'{SEALED}/INDEX.jsonl'
DNOTES = 'theory/pending_docs/D72_D75_weak_spots.md'
def _h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def seal(results, lock, values=None):
    """values: {name: number} for claims.evaluate; if None, the verdict is read from a final 'VERDICT: <text>' line of the results file."""
    os.makedirs(SEALED, exist_ok=True); h = _h(results)
    if values is not None:
        from tools.lockbench.claims import evaluate
        v = evaluate(lock, values); verdict = 'PASS' if v['verdict'] else 'FAIL'; per = {k: c['ok'] for k, c in v['claims'].items()}
    else:
        last = [l for l in open(results).read().splitlines() if l.startswith('VERDICT:')]
        verdict = last[-1][8:].strip() if last else 'UNKNOWN'; per = {}
    dst = f'{SEALED}/{h[:16]}_{os.path.basename(results)}'; shutil.move(results, dst)
    rec = dict(results=results, sealed=dst, sha256=h, lock=lock, verdict=verdict, claims=per, unsealed=None)
    open(INDEX, 'a').write(json.dumps(rec) + '\n'); return dict(verdict=verdict, claims=per)
def _index(): return [json.loads(l) for l in open(INDEX)] if os.path.exists(INDEX) else []
def unseal(results, dnote_id, dnotes=DNOTES):
    R = [r for r in _index() if r['results'] == results and not r['unsealed']]
    if not R: raise KeyError('nothing sealed for ' + results)
    r = R[-1]; txt = open(dnotes).read()
    m = re.search(rf'^## {re.escape(dnote_id)}\b.*?(?=^## D|\Z)', txt, re.S | re.M)
    if not m: raise PermissionError(f'{dnote_id} not found in {dnotes}: write the D-note first')
    if r['verdict'].split()[0].lower() not in m.group(0).lower(): raise PermissionError(f"{dnote_id} does not state the sealed verdict '{r['verdict']}'")
    if _h(r['sealed']) != r['sha256']: raise RuntimeError('sealed file changed — integrity failure')
    shutil.copy(r['sealed'], results); r['unsealed'] = dnote_id
    L = _index(); L = [dict(x, unsealed=dnote_id) if (x['sealed'] == r['sealed']) else x for x in L]
    open(INDEX, 'w').write(''.join(json.dumps(x) + '\n' for x in L)); return results
