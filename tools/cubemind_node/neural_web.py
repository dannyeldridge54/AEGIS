"""Neural web: the index grows like neurons as data passes through it (25 Nov 2026, Danny's design).

Every record in the fingerprint index gets a SHAPE: a point on ten axes.
  side       -1 = left ladder (early universe: inflation, n_s, r), +1 = right ladder (late universe: dark energy, clocks), 0 = centre (mathematics)
  layer      0..1 = how far out from the centre, along the Loom's nine layers (torus, pyramid, turnover, cube, fold, dilaton, forces, cosmology, late universe)
  7 scales   virtue (+1) against vice (-1), each defined by something checkable in the record, so the scale means something:
               humility/pride        the claim is labelled honestly (status given)  vs  strong words with no test behind them
               charity/greed         the claim stays inside its stated model        vs  no model or scope given
               chastity/lust         locked before it ran                           vs  rerun or changed after seeing the result
               gratitude/envy        cites its sources                              vs  no source
               temperance/gluttony   few free parameters                            vs  many fitted knobs
               patience/wrath        numbers converged, nothing forced              vs  clamped or forced
               diligence/sloth       checked by an independent method               vs  untested
  confidence 0..1, the learned trust (below)
A record can be read from several PERSPECTIVES (views). Each view is placed separately, so one record can live in several neurons at once.

NEURONS. The web starts as one centre neuron (where the language model sits). Each record goes down the tree to the nearest neuron. When a
neuron holds more than `cap` placements, it SPLITS in two along its widest spread, so the web grows where the data is dense. Each neuron
carries an ENGINE label (the tag most common among its members, e.g. 'ufe' or 'reactor') and its own accuracy from grades.
SYNAPSES. When two records are linked in the index, the link between their neurons is strengthened; all synapses fade slowly when unused.
MINING. Every neuron can mine: it proposes links from its records to nearby records in OTHER neurons that are not linked yet ("reaching out
for strings"). Proposals are suggestions, never written as links until a check accepts them.
GRADING. When a record is graded right or wrong, the weights on the seven scales are readjusted (online logistic update), so the web learns
which qualities predict being right; every record's confidence and every neuron's accuracy update with it.
All state is stored in the same SQLite file as the fingerprint index (tables web_*). Grades are append-only."""
import json, math, sqlite3
import fingerprint as FP

SCALES = ['humility_pride', 'charity_greed', 'chastity_lust', 'gratitude_envy', 'temperance_gluttony', 'patience_wrath', 'diligence_sloth']
LAYERS = ['torus', 'pyramid', 'turnover', 'cube', 'fold', 'dilaton', 'forces', 'cosmology', 'late universe']
SIDE = {'left': -1.0, 'early': -1.0, 'centre': 0.0, 'center': 0.0, 'math': 0.0, 'right': 1.0, 'late': 1.0}
OVERCLAIM = ('proves', 'proven', 'confirms', 'confirmed', 'definitely', 'breakthrough', 'solved')

def scales_from(rec):
    """The seven scales, each from checkable fields of a fingerprint record (tags as strings). Missing information scores 0, not a penalty."""
    t = rec.get('tags', {}); txt = json.dumps(rec.get('outputs'), default=str).lower(); links = rec.get('links', [])
    s = dict.fromkeys(SCALES, 0.0)
    if t.get('status'): s['humility_pride'] = 1.0
    if any(w in txt for w in OVERCLAIM) and t.get('tested') != 'True': s['humility_pride'] = -1.0
    if t.get('model') or t.get('scope'): s['charity_greed'] = 1.0
    elif t.get('status') in ('CONDITIONAL', 'ASSUMED'): s['charity_greed'] = -1.0
    if t.get('locked') == 'True' or (rec.get('inputs') or {}).get('lock'): s['chastity_lust'] = 1.0
    if t.get('rerun') == 'True' or t.get('post_hoc') == 'True': s['chastity_lust'] = -1.0
    if any(str(l[2]) in ('cites', 'source') for l in links) or t.get('source'): s['gratitude_envy'] = 1.0
    if 'fits' in t:
        try: s['temperance_gluttony'] = max(-1.0, 1.0 - float(t['fits']) / 3.0)
        except ValueError: pass
    if t.get('converged') == 'True': s['patience_wrath'] = 1.0
    if t.get('forced') == 'True' or t.get('clamped') == 'True': s['patience_wrath'] = -1.0
    if t.get('tested') == 'True' or t.get('point_ok') == 'True': s['diligence_sloth'] = 1.0
    elif t.get('tested') == 'False': s['diligence_sloth'] = -1.0
    return s

def shape(rec, view=None):
    """The record's point on the ten axes, for one perspective (view overrides side/layer)."""
    t = dict(rec.get('tags', {})); t.update(view or {})
    side = SIDE.get(str(t.get('side', 'centre')).lower(), 0.0)
    lay = t.get('layer', 0)
    try: layer = (LAYERS.index(lay) + 1) / len(LAYERS) if lay in LAYERS else min(1.0, float(str(lay).lstrip('L')) / len(LAYERS))
    except ValueError: layer = 0.0
    sc = scales_from(rec)
    return [side, layer] + [sc[k] for k in SCALES]

def _d2(a, b): return sum((x - y) ** 2 for x, y in zip(a, b))
def _mean(vs): return [sum(c) / len(vs) for c in zip(*vs)]

class Web:
    def __init__(self, index, cap=12, fade=0.995):
        self.ix, self.cap, self.fade, db = index, cap, fade, index.db
        db.executescript("""
        CREATE TABLE IF NOT EXISTS web_nodes(id INTEGER PRIMARY KEY, parent INTEGER, centroid TEXT, engine TEXT, children TEXT);
        CREATE TABLE IF NOT EXISTS web_place(record TEXT, view TEXT, node INTEGER, vec TEXT, PRIMARY KEY(record, view));
        CREATE TABLE IF NOT EXISTS web_syn(a INTEGER, b INTEGER, w REAL, PRIMARY KEY(a, b));
        CREATE TABLE IF NOT EXISTS web_grades(record TEXT, correct INTEGER, t REAL);
        CREATE TABLE IF NOT EXISTS web_weights(k TEXT PRIMARY KEY, v REAL);
        CREATE TRIGGER IF NOT EXISTS grades_append_only BEFORE DELETE ON web_grades BEGIN SELECT RAISE(ABORT, 'grades are append-only'); END;""")
        if not db.execute('SELECT 1 FROM web_nodes').fetchone():
            with db: db.execute("INSERT INTO web_nodes VALUES (0, NULL, ?, 'centre (language model)', '[]')", (json.dumps([0.0] * (2 + len(SCALES))),))
        self.w = {k: 0.0 for k in ['bias'] + SCALES}; self.w.update(dict(db.execute('SELECT k, v FROM web_weights').fetchall()))
    # ---------------------------------------------------------------- structure
    def _node(self, nid):
        r = self.ix.db.execute('SELECT parent, centroid, engine, children FROM web_nodes WHERE id=?', (nid,)).fetchone()
        return dict(id=nid, parent=r[0], centroid=json.loads(r[1]), engine=r[2], children=json.loads(r[3]))
    def leaf_for(self, vec):
        n = self._node(0)
        while n['children']: n = min((self._node(c) for c in n['children']), key=lambda c: _d2(c['centroid'], vec))
        return n['id']
    def members(self, nid): return [(r, v, json.loads(x)) for r, v, x in self.ix.db.execute('SELECT record, view, vec FROM web_place WHERE node=?', (nid,))]
    def _engine_label(self, nid):
        recs = [self.ix.get(r) for r, _, _ in self.members(nid)]; c = {}
        for rec in recs:
            for k in ('area', 'sector', 'kind'):
                v = (rec or {}).get('tags', {}).get(k)
                if v: c[v] = c.get(v, 0) + 1; break
        return max(c, key=c.get) if c else 'unlabelled'
    def _split(self, nid):
        mem = self.members(nid); vecs = [m[2] for m in mem]
        if len({tuple(v) for v in vecs}) < 2: return                                     # identical shapes cannot split
        a = max(vecs, key=lambda v: _d2(v, vecs[0])); b = max(vecs, key=lambda v: _d2(v, a))   # farthest pair, deterministic
        for _ in range(10):
            A = [v for v in vecs if _d2(v, a) <= _d2(v, b)]; B = [v for v in vecs if _d2(v, a) > _d2(v, b)]
            if not A or not B: return
            a, b = _mean(A), _mean(B)
        db = self.ix.db
        with db:
            ids = []
            for c in (a, b):
                cur = db.execute('INSERT INTO web_nodes(parent, centroid, engine, children) VALUES (?,?,?,?)', (nid, json.dumps(c), 'unlabelled', '[]')); ids.append(cur.lastrowid)
            db.execute('UPDATE web_nodes SET children=? WHERE id=?', (json.dumps(ids), nid))
            for r, v, vec in mem: db.execute('UPDATE web_place SET node=? WHERE record=? AND view=?', (ids[0] if _d2(vec, a) <= _d2(vec, b) else ids[1], r, v))
        for c in ids: db.execute('UPDATE web_nodes SET engine=? WHERE id=?', (self._engine_label(c), c))
    # ---------------------------------------------------------------- data passing through
    def place(self, rid, views=None):
        """Place a record (all its perspectives). views: {name: {'side': .., 'layer': ..}}; default one view from its own tags."""
        rec = self.ix.get(rid); views = views or {'own': {}}; out = {}
        for name, v in views.items():
            vec = shape(rec, v); nid = self.leaf_for(vec)
            with self.ix.db: self.ix.db.execute('INSERT OR REPLACE INTO web_place VALUES (?,?,?,?)', (rid, name, nid, json.dumps(vec)))
            out[name] = nid
            mem = self.members(nid)
            with self.ix.db: self.ix.db.execute('UPDATE web_nodes SET centroid=?, engine=? WHERE id=?', (json.dumps(_mean([m[2] for m in mem])), self._engine_label(nid), nid))
            if len(mem) > self.cap: self._split(nid)
        for l in self.ix.links_of(rid):                                                  # strengthen synapses along existing links
            other = [n for (n,) in self.ix.db.execute('SELECT node FROM web_place WHERE record=?', (l['target'],))]
            for a in {self._node_of(rid, n) for n in out}:
                for b in other: self._strengthen(a, b)
        return out
    def _node_of(self, rid, view): return self.ix.db.execute('SELECT node FROM web_place WHERE record=? AND view=?', (rid, view)).fetchone()[0]
    def _strengthen(self, a, b):
        if a == b: return
        a, b = min(a, b), max(a, b); db = self.ix.db
        with db:
            db.execute('UPDATE web_syn SET w = w * ?', (self.fade,))
            db.execute('INSERT INTO web_syn VALUES (?,?,1.0) ON CONFLICT(a,b) DO UPDATE SET w = w + 1.0', (a, b))
    def synapses(self): return self.ix.db.execute('SELECT a, b, w FROM web_syn ORDER BY w DESC').fetchall()
    # ---------------------------------------------------------------- mining
    def mine(self, nid, radius=0.5, limit=10, members=24, sample=4000):
        """Proposed links from this neuron's records to nearby records in other neurons, not already linked. Suggestions only.
        Bounded work: the newest `members` records of this neuron against a random `sample` of other placements (the full pairwise
        search grew with the square of the web and froze the node once the scan had placed ~100k records)."""
        mine_ = [(r, v, json.loads(x)) for r, v, x in self.ix.db.execute(
            'SELECT record, view, vec FROM web_place WHERE node=? ORDER BY rowid DESC LIMIT ?', (nid, members))]
        others = [(r, v, json.loads(x), n) for r, v, n, x in self.ix.db.execute(
            'SELECT record, view, node, vec FROM web_place WHERE node != ? ORDER BY random() LIMIT ?', (nid, sample))]
        props, r2 = [], radius * radius
        for r, _, vec in mine_:
            linked = {l['target'] for l in self.ix.links_of(r)}
            for o, _, ovec, n in others:
                d2 = _d2(vec, ovec)
                if d2 <= r2 and o != r and o not in linked: props.append(dict(src=r, dst=o, neuron=n, distance=round(math.sqrt(d2), 4)))
        return sorted(props, key=lambda p: p['distance'])[:limit]
    # ---------------------------------------------------------------- grading
    def trust(self, rid):
        sc = scales_from(self.ix.get(rid)); z = self.w['bias'] + sum(self.w[k] * sc[k] for k in SCALES)
        return 1 / (1 + math.exp(-z))
    def grade(self, rid, correct, lr=0.3):
        sc = scales_from(self.ix.get(rid)); p = self.trust(rid); g = (1.0 if correct else 0.0) - p
        self.w['bias'] += lr * g
        for k in SCALES: self.w[k] += lr * g * sc[k]
        with self.ix.db:
            self.ix.db.execute('INSERT INTO web_grades VALUES (?,?,julianday())', (rid, int(bool(correct))))
            self.ix.db.executemany('INSERT OR REPLACE INTO web_weights VALUES (?,?)', list(self.w.items()))
    def neuron_accuracy(self, nid):
        rows = self.ix.db.execute('SELECT g.correct FROM web_grades g JOIN web_place p ON p.record=g.record WHERE p.node=?', (nid,)).fetchall()
        return None if not rows else sum(r[0] for r in rows) / len(rows)
    # ---------------------------------------------------------------- the central sheet
    def sheet(self):
        """One row per neuron: where it sits, its engine, size, accuracy, strongest synapse."""
        rows = []
        for (nid,) in self.ix.db.execute('SELECT id FROM web_nodes ORDER BY id'):
            n = self._node(nid); c = n['centroid']; syn = [s for s in self.synapses() if nid in s[:2]]
            rows.append(dict(neuron=nid, parent=n['parent'], leaf=not n['children'], engine=n['engine'], side=round(c[0], 2), layer=round(c[1], 2),
                             balance=round(sum(c[2:]), 2), records=len(self.members(nid)), accuracy=self.neuron_accuracy(nid),
                             strongest_link=(max(syn, key=lambda s: s[2])[:2] if syn else None)))
        return rows
