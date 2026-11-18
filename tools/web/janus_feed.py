"""Janus auto-feeder (AF). Every tool run / D-note / collector pass / ingest appends an event here; Janus animates a
pulse along the named edge and grows the web when new nodes/edges arrive. Honest: this just records activity — no claims.
Writes docs/web/janus_feed.jsonl (tail-able); the Janus app polls a deployed copy. Keep it small (ring-trimmed)."""
import json, time, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
FEED = R / 'docs/web/janus_feed.jsonl'
def _append(rec, keep=500):
    FEED.parent.mkdir(parents=True, exist_ok=True)
    lines = FEED.read_text(encoding='utf-8').splitlines() if FEED.exists() else []
    lines.append(json.dumps(rec)); lines = lines[-keep:]
    FEED.write_text('\n'.join(lines) + '\n', encoding='utf-8')
def pulse(s, t, strength=1.0, reason=''):
    """A pulse travelling edge s->t (node ids)."""
    _append(dict(k='pulse', s=s, t=t, w=round(float(strength), 3), why=reason[:120], ts=time.time())); return True
def add_node(id, lane='theory', status='note', title=''):
    _append(dict(k='node', id=id, lane=lane, status=status, title=title[:120], ts=time.time())); return True
def add_edge(s, t, sign=1, reason=''):
    _append(dict(k='edge', s=s, t=t, sign=int(sign), why=reason[:120], ts=time.time())); return True
if __name__ == '__main__':
    pulse('serapis_e', 'serapis_point', 1.0, 'demo'); print('feed at', FEED)
