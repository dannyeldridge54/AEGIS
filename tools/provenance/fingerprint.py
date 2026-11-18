# AEGIS-FP ACU2DLIXR7SKVG36 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""AEGIS provenance kit: prove authorship and detect copying.

Layers (all legal; none alters a scientific result beyond 1e-10 relative):
  1. manifest   SHA-256 of every tracked file + a Merkle root, committed and timestamped (git, Zenodo DOIs). Public.
  2. stamp      a keyed header tag in every .py/.md/.tex file: only the holder of the secret key can generate or verify it.
  3. canary     trap digits in our own fitted constants, far below their stated precision (a "trap street").
                Their locations live only in the PRIVATE registry, so a copier cannot know which digits to scrub.
  4. winnow     MOSS-style code fingerprints (normalised tokens, k-gram hashes, winnowing). Survives renamed
                variables, removed comments and reformatting. The fingerprint database is kept private.
  5. scan       check any suspect folder: header tags, canary digits, and the share of our code fingerprints it contains.

Usage (repo root):
  python -m tools.provenance.fingerprint keygen  [--key PATH]
  python -m tools.provenance.fingerprint stamp   [--key PATH] [--dry]
  python -m tools.provenance.fingerprint manifest
  python -m tools.provenance.fingerprint winnow  --db PRIVATE_DB.json
  python -m tools.provenance.fingerprint scan SUSPECT_DIR --db PRIVATE_DB.json [--key PATH] [--registry PRIVATE_REGISTRY.json]
  python -m tools.provenance.fingerprint spread [--dry]        keyed trap digits in every solver tolerance
  python -m tools.provenance.fingerprint winnow-all            token + AST + text (papers) fingerprints
  python -m tools.provenance.fingerprint scan2 SUSPECT_DIR     full scan: stamps, canaries, token, AST and text matches
  python -m tools.provenance.fingerprint licensee NAME OUTDIR  traceable copy for one licensee (traitor tracing)
  python -m tools.provenance.fingerprint trace SUSPECT_DIR     which licensee's copy leaked
"""
import os, sys, hmac, hashlib, base64, json, subprocess, io, tokenize, re, time

DEFAULT_KEY = os.path.expanduser('~/.aegis/fp_key')
STAMP_RE = re.compile(r'AEGIS-FP ([A-Z2-7]{16})')
EXTS = {'.py': '# ', '.md': None, '.tex': '% '}

def _files(root='.'):
    out = subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True, text=True).stdout.split('\n')
    return [f for f in out if f]

def keygen(path=DEFAULT_KEY):
    if os.path.exists(path): print('key exists:', path); return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fh: fh.write(os.urandom(32))
    os.chmod(path, 0o600); print('new key written to', path, '(keep a private copy; never publish it)')

def _key(path=DEFAULT_KEY): return open(path, 'rb').read()

def tag(key, relpath):
    d = hmac.new(key, ('AEGIS|Danny Lee Eldridge|' + relpath).encode(), hashlib.sha256).digest()
    return base64.b32encode(d)[:16].decode()

def _header(ext, t):
    body = f'AEGIS-FP {t} · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)'
    return f'<!-- {body} -->\n' if ext == '.md' else EXTS[ext] + body + '\n'

def stamp(keypath=DEFAULT_KEY, dry=False, roots=('tools', 'papers', 'licensing', 'theory/derivations')):
    key = _key(keypath); n = 0
    for f in _files():
        ext = os.path.splitext(f)[1]
        if ext not in EXTS or not f.startswith(roots) or '/data/' in f: continue
        s = open(f, encoding='utf-8', errors='replace').read()
        if STAMP_RE.search(s[:600]): continue
        h = _header(ext, tag(key, f))
        if ext == '.py' and s.startswith('#!'):  # keep shebang first
            first, rest = s.split('\n', 1) if '\n' in s else (s, ''); s2 = first + '\n' + h + rest
        else: s2 = h + s
        n += 1
        if not dry: open(f, 'w', encoding='utf-8').write(s2)
    print(('would stamp' if dry else 'stamped'), n, 'files')

def manifest(out='provenance/MANIFEST.txt'):
    rows = []
    for f in sorted(_files()):
        try: rows.append((hashlib.sha256(open(f, 'rb').read()).hexdigest(), f))
        except (IsADirectoryError, FileNotFoundError): pass
    level = [bytes.fromhex(h) for h, _ in rows]
    while len(level) > 1:
        level = [hashlib.sha256(level[i] + (level[i + 1] if i + 1 < len(level) else level[i])).digest() for i in range(0, len(level), 2)]
    root = level[0].hex() if level else ''
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as fh:
        fh.write(f'# AEGIS provenance manifest · Danny Lee Eldridge · {time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}\n')
        fh.write(f'# files {len(rows)} · Merkle root {root}\n')
        for h, f in rows: fh.write(f'{h}  {f}\n')
    print('manifest:', out, len(rows), 'files, root', root)

# ---- winnowing (Schleimer, Wilkerson & Aiken 2003, the method behind MOSS) ----
def _norm_tokens(src):
    toks = []
    try:
        for t in tokenize.generate_tokens(io.StringIO(src).readline):
            if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING): continue
            if t.type == tokenize.NAME: toks.append(t.string if t.string in KEYWORDS else 'N')
            elif t.type == tokenize.STRING: toks.append('S')
            else: toks.append(t.string)
    except (tokenize.TokenError, IndentationError, SyntaxError): pass
    return toks
import keyword; KEYWORDS = set(keyword.kwlist) | {'math', 'np', 'numpy', 'scipy', 'exp', 'log', 'sqrt', 'pi'}

def winnow_src(src, k=25, w=8):
    t = _norm_tokens(src)
    hs = [int.from_bytes(hashlib.blake2b(' '.join(t[i:i + k]).encode(), digest_size=8).digest(), 'big') for i in range(max(0, len(t) - k + 1))]
    fp = set()
    for i in range(max(0, len(hs) - w + 1)): fp.add(min(hs[i:i + w]))
    return fp

def winnow(db='~/.aegis/winnow_db.json', roots=('tools/',)):
    db = os.path.expanduser(db); store = {}
    for f in _files():
        if f.endswith('.py') and f.startswith(roots):
            for h in winnow_src(open(f, encoding='utf-8', errors='replace').read()): store.setdefault(str(h), f)
    os.makedirs(os.path.dirname(db), exist_ok=True); json.dump(store, open(db, 'w'))
    print('winnow db:', db, len(store), 'fingerprints')

def scan(suspect, db='~/.aegis/winnow_db.json', keypath=DEFAULT_KEY, registry='~/.aegis/canary_registry.json'):
    db = json.load(open(os.path.expanduser(db))); key = _key(keypath) if os.path.exists(keypath) else None
    reg = json.load(open(os.path.expanduser(registry))) if os.path.exists(os.path.expanduser(registry)) else []
    report = {'files': 0, 'stamped': [], 'valid_stamps': 0, 'canaries': [], 'code_matches': {}}
    for dp, _, fs in os.walk(suspect):
        for fn in fs:
            p = os.path.join(dp, fn)
            try: s = open(p, encoding='utf-8', errors='replace').read()
            except Exception: continue
            report['files'] += 1
            for t in STAMP_RE.findall(s):
                report['stamped'].append(p)
                if key and any(hmac.compare_digest(t, tag(key, f)) for f in _files()): report['valid_stamps'] += 1
            for c in reg:
                if c['digits'] in s: report['canaries'].append({'file': p, 'canary': c['name']})
            if fn.endswith('.py'):
                fp = winnow_src(s); hit = [db[str(h)] for h in fp if str(h) in db]
                if fp and hit:
                    share = len(hit) / len(fp)
                    report['code_matches'][p] = {'share_of_file': round(share, 3), 'matched_fingerprints': len(hit), 'our_files': sorted(set(hit))[:5],
                                                 'verdict': 'LIKELY COPIED' if share >= 0.5 and len(hit) >= 15 else 'weak (common boilerplate)'}
    print(json.dumps(report, indent=1)); return report

# ---- stronger layers (added 18 Nov 2026) ----
TOL_RE = re.compile(r'\b(rtol|atol|xtol|ftol|fatol|xatol|tol)\s*=\s*1e-(\d+)\b')
EXCLUDE = ('tools/janus_astro/', 'tools/provenance/')

def spread(keypath=DEFAULT_KEY, registry='~/.aegis/canary_registry.json', roots=('tools/',), dry=False):
    """Turn solver/root-finder tolerances (rtol=1e-N etc.) into keyed trap values 1.0000ddddddde-N.
    A relative change of <1e-5 in a tolerance changes no result; each file gets its own keyed digits."""
    key = _key(keypath); reg_p = os.path.expanduser(registry)
    reg = json.load(open(reg_p)) if os.path.exists(reg_p) else []; n = 0
    for f in _files():
        if not f.endswith('.py') or not f.startswith(roots) or f.startswith(EXCLUDE): continue
        s = open(f, encoding='utf-8').read(); i = [0]
        def rep(m):
            i[0] += 1
            d = int.from_bytes(hmac.new(key, f'{f}|{i[0]}'.encode(), hashlib.sha256).digest()[:4], 'big') % 10**7
            val = f'1.0000{d:07d}e-{m.group(2)}'
            reg.append({'name': f'tol {m.group(1)} #{i[0]}', 'file': f, 'digits': val, 'effect': 'none (tolerance)'})
            return f'{m.group(1)}={val}'
        s2 = TOL_RE.sub(rep, s)
        if s2 != s:
            n += i[0]
            if not dry: open(f, 'w', encoding='utf-8').write(s2)
    if not dry: json.dump(reg, open(reg_p, 'w'), indent=1)
    print(('would place' if dry else 'placed'), n, 'tolerance canaries; registry now', len(reg))

def _norm_ast(src):
    """AST-level normal form: identifiers, constants and docstrings removed; survives renaming, reformatting,
    comment/docstring removal, changed literals and reordered keyword arguments."""
    import ast
    try: tree = ast.parse(src)
    except SyntaxError: return []
    out = []
    for node in ast.walk(tree):
        t = type(node).__name__
        if isinstance(node, ast.BinOp): t += ':' + type(node.op).__name__
        elif isinstance(node, ast.Compare): t += ':' + ','.join(type(o).__name__ for o in node.ops)
        elif isinstance(node, ast.Attribute): t += ':' + node.attr          # library calls (np.exp, brentq...) kept
        elif isinstance(node, ast.Name) and node.id in KEYWORDS: t += ':' + node.id
        out.append(t)
    return out

def winnow_ast(src, k=30, w=8):
    t = _norm_ast(src)
    hs = [int.from_bytes(hashlib.blake2b(' '.join(t[i:i + k]).encode(), digest_size=8).digest(), 'big') for i in range(max(0, len(t) - k + 1))]
    return {min(hs[i:i + w]) for i in range(max(0, len(hs) - w + 1))}

def _norm_text(s):
    s = re.sub(r'\\[a-zA-Z]+|[{}$\\%&_^~#]', ' ', s.lower())
    return re.findall(r'[a-z0-9]+', s)

def winnow_text(s, k=12, w=6):
    t = _norm_text(s)
    hs = [int.from_bytes(hashlib.blake2b(' '.join(t[i:i + k]).encode(), digest_size=8).digest(), 'big') for i in range(max(0, len(t) - k + 1))]
    return {min(hs[i:i + w]) for i in range(max(0, len(hs) - w + 1))}

def winnow_all(db='~/.aegis/winnow_db.json', roots=('tools/', 'papers/', 'theory/derivations/', 'licensing/')):
    """Three fingerprint sets: token (code), AST (code structure), text (papers and docs, word 12-grams)."""
    store = {'tok': {}, 'ast': {}, 'txt': {}}
    for f in _files():
        if not f.startswith(roots): continue
        try: s = open(f, encoding='utf-8', errors='replace').read()
        except Exception: continue
        if f.endswith('.py'):
            for h in winnow_src(s): store['tok'].setdefault(str(h), f)
            for h in winnow_ast(s): store['ast'].setdefault(str(h), f)
        elif f.endswith(('.tex', '.md')):
            for h in winnow_text(s): store['txt'].setdefault(str(h), f)
    db = os.path.expanduser(db); json.dump(store, open(db, 'w'))
    print('db', db, {k: len(v) for k, v in store.items()})

def scan2(suspect, db='~/.aegis/winnow_db.json', keypath=DEFAULT_KEY, registry='~/.aegis/canary_registry.json'):
    D = json.load(open(os.path.expanduser(db)))
    if 'tok' not in D: D = {'tok': D, 'ast': {}, 'txt': {}}
    key = _key(keypath) if os.path.exists(keypath) else None
    reg = json.load(open(os.path.expanduser(registry))) if os.path.exists(os.path.expanduser(registry)) else []
    ours = _files() if key else []
    rep = {'files': 0, 'valid_stamps': [], 'canaries': [], 'code': {}, 'text': {}}
    for dp, _, fs in os.walk(suspect):
        for fn in fs:
            p = os.path.join(dp, fn)
            try: s = open(p, encoding='utf-8', errors='replace').read()
            except Exception: continue
            rep['files'] += 1
            for t in STAMP_RE.findall(s):
                if key and any(hmac.compare_digest(t, tag(key, f)) or hmac.compare_digest(t, tag(key, f + '#pdf')) for f in ours): rep['valid_stamps'].append(p)
            for c in reg:
                if c['digits'] in s: rep['canaries'].append({'file': p, 'canary': c['name'], 'from': c['file']})
            if fn.endswith('.py'):
                a, b = winnow_src(s), winnow_ast(s)
                ha = [D['tok'][str(h)] for h in a if str(h) in D['tok']]; hb = [D['ast'][str(h)] for h in b if str(h) in D['ast']]
                sa = len(ha)/len(a) if a else 0; sb = len(hb)/len(b) if b else 0
                if ha or hb:
                    strong = (sa >= .5 and len(ha) >= 15) or (sb >= .5 and len(hb) >= 15)
                    rep['code'][p] = {'token_share': round(sa, 3), 'ast_share': round(sb, 3), 'our_files': sorted(set(ha + hb))[:5],
                                      'verdict': 'LIKELY COPIED' if strong else 'weak'}
            elif fn.endswith(('.tex', '.md', '.txt', '.html')):
                c = winnow_text(s); hc = [D['txt'][str(h)] for h in c if str(h) in D['txt']]
                if hc: rep['text'][p] = {'share': round(len(hc)/len(c), 3), 'matches': len(hc), 'our_files': sorted(set(hc))[:5],
                                         'verdict': 'LIKELY COPIED' if len(hc) >= 10 else 'weak'}
    strong = sum(v['verdict'] == 'LIKELY COPIED' for v in list(rep['code'].values()) + list(rep['text'].values()))
    rep['summary'] = {'valid_stamps': len(rep['valid_stamps']), 'canaries_found': len(rep['canaries']), 'likely_copied_files': strong}
    print(json.dumps(rep, indent=1)); return rep

def licensee_build(name, outdir, keypath=DEFAULT_KEY, registry='~/.aegis/licensee_registry.json', roots=('tools/lhc/', 'tools/lattice/', 'tools/janus_calc/')):
    """Traitor tracing: a copy for one licensee whose tolerance canaries carry digits unique to that licensee.
    If the copy leaks, the digits name the licensee it came from."""
    import shutil
    key = _key(keypath); reg_p = os.path.expanduser(registry)
    reg = json.load(open(reg_p)) if os.path.exists(reg_p) else {}
    marks = []
    for f in _files():
        if not f.startswith(roots): continue
        dst = os.path.join(outdir, f); os.makedirs(os.path.dirname(dst), exist_ok=True)
        if f.endswith('.py'):
            s = open(f, encoding='utf-8').read(); i = [0]
            def rep(m):
                i[0] += 1
                d = int.from_bytes(hmac.new(key, f'LIC|{name}|{f}|{i[0]}'.encode(), hashlib.sha256).digest()[:4], 'big') % 10**7
                v = f'1.0000{d:07d}e-{m.group(2).split("e-")[-1]}'; marks.append(v); return f'{m.group(1)}={v}'
            s = re.sub(r'\b(rtol|atol|xtol|ftol|fatol|xatol|tol)\s*=\s*(1(?:\.0000\d{7})?e-\d+)\b', rep, s)
            s = STAMP_RE.sub(lambda m: 'AEGIS-FP ' + base64.b32encode(hmac.new(key, f'LIC|{name}|{f}'.encode(), hashlib.sha256).digest())[:16].decode(), s)
            open(dst, 'w', encoding='utf-8').write(s)
        else: shutil.copy2(f, dst)
    reg[name] = {'date': time.strftime('%Y-%m-%d'), 'marks': marks}; json.dump(reg, open(reg_p, 'w'), indent=1)
    print(f'licensee build for {name!r}: {outdir} ({len(marks)} unique marks)')

def trace(suspect, registry='~/.aegis/licensee_registry.json'):
    reg = json.load(open(os.path.expanduser(registry))); hits = {}
    for dp, _, fs in os.walk(suspect):
        for fn in fs:
            try: s = open(os.path.join(dp, fn), encoding='utf-8', errors='replace').read()
            except Exception: continue
            for n, r in reg.items():
                k = sum(m in s for m in r['marks'])
                if k: hits[n] = hits.get(n, 0) + k
    print(json.dumps({'licensee_marks_found': hits}, indent=1)); return hits

if __name__ == '__main__':
    a = sys.argv[1:]
    opt = lambda n, d=None: a[a.index(n) + 1] if n in a else d
    if not a: print(__doc__)
    elif a[0] == 'keygen': keygen(opt('--key', DEFAULT_KEY))
    elif a[0] == 'stamp': stamp(opt('--key', DEFAULT_KEY), '--dry' in a)
    elif a[0] == 'manifest': manifest()
    elif a[0] == 'winnow': winnow(opt('--db', '~/.aegis/winnow_db.json'))
    elif a[0] == 'spread': spread(opt('--key', DEFAULT_KEY), dry='--dry' in a)
    elif a[0] == 'winnow-all': winnow_all()
    elif a[0] == 'scan2': scan2(a[1])
    elif a[0] == 'licensee': licensee_build(a[1], a[2])
    elif a[0] == 'trace': trace(a[1])
    elif a[0] == 'scan': scan(a[1], opt('--db', '~/.aegis/winnow_db.json'), opt('--key', DEFAULT_KEY), opt('--registry', '~/.aegis/canary_registry.json'))
    else: print(__doc__)
