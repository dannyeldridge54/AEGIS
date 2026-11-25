"""Fingerprint index: every computation is hashed, tagged, indexed and linked, and signed with the owner's key.

Each run of anything (a derivation, a check, a test, an engine cycle) becomes ONE record in a local SQLite index:
  id        SHA-256 of the record's content (inputs + code + outputs + tags), so identical work always gets the same id
  owner     the owner's name, and `sig` = HMAC-SHA256 of the id with the owner's private key file: proves the record is the owner's
  kind      what it is (derivation, check, test, cycle, result, ...)
  hashes    SHA-256 of the inputs, of every code file used, and of the outputs
  tags      key = value pairs to categorise it (sector, layer, anchor, status, model, ...)
  links     what it connects to, per level: (target, level, relation), where target is another record id or a named stream
Nothing else is stored: no chatter, no banners. The `producer` tag (which tool or model made it) is kept because it matters for checking.
Records are append-only; a correction is a new record linked to the old one with relation 'corrects'.

Use:
    fp = Index('fingerprints.sqlite', owner='Danny Eldridge', key_file='~/.aegis_owner.key')
    rid = fp.stamp('check', inputs={...}, outputs={...}, code=['tools/x.py'], tags={'sector': 'serapis_e', 'layer': 'L1'},
                   links=[('stream:modular/rho', 1, 'anchors_on')])
    fp.find(tag=('sector', 'serapis_e')); fp.links_of(rid); fp.verify(rid)
CLI:  python fingerprint.py --db fingerprints.sqlite stats | find sector=serapis_e | links <id> | verify-all"""
import hashlib, hmac, json, os, secrets, sqlite3, sys, time
from pathlib import Path

def _canon(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), default=str).encode()
def _sha(b): return hashlib.sha256(b).hexdigest()
def file_sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

SCHEMA = """
CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, created REAL NOT NULL, owner TEXT NOT NULL, sig TEXT NOT NULL,
  inputs_sha TEXT, outputs_sha TEXT, payload TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS code(record TEXT NOT NULL, path TEXT NOT NULL, sha TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tags(record TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS links(record TEXT NOT NULL, target TEXT NOT NULL, level INTEGER NOT NULL, relation TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS t_kv ON tags(key, value); CREATE INDEX IF NOT EXISTS l_t ON links(target); CREATE INDEX IF NOT EXISTS l_r ON links(record);
CREATE INDEX IF NOT EXISTS r_kind ON records(kind);
CREATE TRIGGER IF NOT EXISTS no_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT, 'records are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT, 'records are append-only'); END;
"""

class Index:
    def __init__(self, db, owner, key_file=None, key=None):
        self.db = sqlite3.connect(str(db)); self.db.executescript(SCHEMA); self.owner = owner
        if key is None:
            kf = Path(os.path.expanduser(key_file or '~/.aegis_owner.key'))
            if not kf.exists():
                kf.parent.mkdir(parents=True, exist_ok=True); kf.write_text(secrets.token_hex(32))
                try: os.chmod(kf, 0o600)
                except OSError: pass
            key = kf.read_text().strip()
        self._key = bytes.fromhex(key) if all(c in '0123456789abcdef' for c in key) and len(key) % 2 == 0 else key.encode()
    def _sign(self, rid): return hmac.new(self._key, (self.owner + '\x00' + rid).encode(), hashlib.sha256).hexdigest()
    def stamp(self, kind, inputs=None, outputs=None, code=(), tags=None, links=(), root='.'):
        """Record one computation. Returns its id. Re-stamping identical work returns the existing id."""
        code_sha = {str(p): file_sha(Path(root) / p) for p in code}
        tags = {k: str(v) for k, v in (tags or {}).items()}
        links = [(str(t), int(lv), str(rel)) for t, lv, rel in links]
        body = dict(kind=kind, inputs=inputs, outputs=outputs, code=code_sha, tags=tags, links=sorted(links))
        rid = _sha(_canon(body))
        if self.db.execute('SELECT 1 FROM records WHERE id=?', (rid,)).fetchone(): return rid
        with self.db:
            self.db.execute('INSERT INTO records VALUES (?,?,?,?,?,?,?,?)', (rid, kind, time.time(), self.owner, self._sign(rid),
                            _sha(_canon(inputs)), _sha(_canon(outputs)), _canon(body).decode()))
            self.db.executemany('INSERT INTO code VALUES (?,?,?)', [(rid, p, s) for p, s in code_sha.items()])
            self.db.executemany('INSERT INTO tags VALUES (?,?,?)', [(rid, k, v) for k, v in tags.items()])
            self.db.executemany('INSERT INTO links VALUES (?,?,?,?)', [(rid, t, lv, rel) for t, lv, rel in links])
        return rid
    def verify(self, rid):
        """True if the record's content still hashes to its id and the signature is the owner's."""
        row = self.db.execute('SELECT payload, sig, owner FROM records WHERE id=?', (rid,)).fetchone()
        if not row: return False
        payload, sig, owner = row
        return _sha(payload.encode()) == rid and owner == self.owner and hmac.compare_digest(sig, self._sign(rid))
    def get(self, rid):
        row = self.db.execute('SELECT payload, created, owner FROM records WHERE id=?', (rid,)).fetchone()
        return None if not row else dict(json.loads(row[0]), id=rid, created=row[1], owner=row[2])
    def find(self, kind=None, tag=None, limit=100):
        q, a = 'SELECT DISTINCT r.id FROM records r LEFT JOIN tags t ON t.record=r.id WHERE 1=1', []
        if kind: q += ' AND r.kind=?'; a.append(kind)
        if tag: q += ' AND t.key=? AND t.value=?'; a += list(tag)
        return [r[0] for r in self.db.execute(q + ' ORDER BY r.created LIMIT ?', a + [limit])]
    def links_of(self, rid):
        out = [dict(target=t, level=lv, relation=rel, direction='out') for t, lv, rel in self.db.execute('SELECT target, level, relation FROM links WHERE record=?', (rid,))]
        out += [dict(target=r, level=lv, relation=rel, direction='in') for r, lv, rel in self.db.execute('SELECT record, level, relation FROM links WHERE target=?', (rid,))]
        return out
    def stream(self, name, max_level=9):
        """Everything connected to a named stream, by level (breadth-first through links)."""
        seen, frontier, out = {name}, [name], {}
        for level in range(max_level + 1):
            nxt = []
            for node in frontier:
                for (r,) in self.db.execute('SELECT record FROM links WHERE target=?', (node,)):
                    if r not in seen: seen.add(r); nxt.append(r); out.setdefault(level, []).append(r)
            frontier = nxt
            if not frontier: break
        return out
    def stats(self):
        n = self.db.execute('SELECT COUNT(*) FROM records').fetchone()[0]
        kinds = dict(self.db.execute('SELECT kind, COUNT(*) FROM records GROUP BY kind').fetchall())
        keys = dict(self.db.execute('SELECT key, COUNT(DISTINCT value) FROM tags GROUP BY key').fetchall())
        return dict(records=n, kinds=kinds, tag_keys=keys, owner=self.owner)

if __name__ == '__main__':
    import argparse
    a = argparse.ArgumentParser(); a.add_argument('--db', default='fingerprints.sqlite'); a.add_argument('--owner', default=os.environ.get('AEGIS_OWNER', 'Danny Eldridge'))
    a.add_argument('cmd', choices=['stats', 'find', 'links', 'stream', 'verify-all']); a.add_argument('arg', nargs='?')
    g = a.parse_args(); fp = Index(g.db, g.owner)
    if g.cmd == 'stats': print(json.dumps(fp.stats(), indent=1))
    elif g.cmd == 'find':
        k, _, v = (g.arg or '').partition('='); print('\n'.join(fp.find(tag=(k, v)) if k else fp.find()))
    elif g.cmd == 'links': print(json.dumps(fp.links_of(g.arg), indent=1))
    elif g.cmd == 'stream': print(json.dumps(fp.stream(g.arg), indent=1))
    else:
        bad = [r for (r,) in fp.db.execute('SELECT id FROM records') if not fp.verify(r)]; print('all records verify' if not bad else f'{len(bad)} FAILED: {bad[:5]}'); sys.exit(1 if bad else 0)
