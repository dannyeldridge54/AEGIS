#!/usr/bin/env python3
"""CubeMind archiver: compresses data it has processed with the Loom compressor (best build D2014: indirect node + faders),
verifies an exact round-trip, and records the saving. Large files fall back to xz (lzma) for speed (Loom ~4-5 MB/min).
Originals are KEPT unless CM_DELETE_ORIGINALS=1 is set by Danny (and only after the round-trip is verified).
Usage: python cm_compress.py <file> [<file> ...]      |      python cm_compress.py --restore <file.lmz|file.xz>"""
import os, sys, subprocess, hashlib, lzma, json, time, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, 'loomz.exe' if os.name == 'nt' else 'loomz_linux')
ENV = dict(os.environ, EV='1', LR1='3', CLASSMAP=os.path.join(HERE, 'DIR_ONE.map'), MASK=str(0x12ffff),
           GAINS='1,1,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,1,0.5,0.5,0.5')
LOOM_MAX = int(os.environ.get('CM_LOOM_MAX_MB', '50')) * 1000000
LOG = os.path.join(HERE, 'archive_log.jsonl')
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def loom(mode, a, b): return subprocess.run([EXE, mode, a, b], env=ENV, capture_output=True, text=True).returncode == 0
def compress(p):
    n = os.path.getsize(p); s0 = sha(p); t = time.time()
    if n <= LOOM_MAX and os.path.exists(EXE):
        out = p + '.lmz'; ok = loom('c', p, out)
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, 'r'); ok = ok and loom('d', out, r) and sha(r) == s0
        how = 'loom'
    else:
        out = p + '.xz'
        with open(p, 'rb') as f, lzma.open(out, 'wb', preset=9 | lzma.PRESET_EXTREME) as g:
            for b in iter(lambda: f.read(1 << 20), b''): g.write(b)
        h = hashlib.sha256()
        with lzma.open(out, 'rb') as g:
            for b in iter(lambda: g.read(1 << 20), b''): h.update(b)
        ok = h.hexdigest() == s0; how = 'xz'
    rec = dict(file=p, method=how, bytes_in=n, bytes_out=os.path.getsize(out) if os.path.exists(out) else None, roundtrip=ok, sha256=s0, secs=round(time.time() - t, 1))
    if ok and os.environ.get('CM_DELETE_ORIGINALS') == '1': os.remove(p); rec['original_deleted'] = True
    if not ok and os.path.exists(out): os.remove(out)
    with open(LOG, 'a') as f: f.write(json.dumps(rec) + '\n')
    return rec
def restore(p):
    if p.endswith('.lmz'): return loom('d', p, p[:-4])
    with lzma.open(p, 'rb') as g, open(p[:-3], 'wb') as f:
        for b in iter(lambda: g.read(1 << 20), b''): f.write(b)
    return True
if __name__ == '__main__':
    if sys.argv[1] == '--restore': print(all(restore(p) for p in sys.argv[2:]))
    else:
        for p in sys.argv[1:]: print(json.dumps(compress(p)))
