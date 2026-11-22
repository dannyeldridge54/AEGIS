#!/usr/bin/env python3
"""Reversible symbol transform for enwik (Hutter-style): capital flag + word dictionary. fwd/inv.
- Capital flag: 'The' -> \\x05 'the'; 'NASA' -> \\x06 'nasa' (only pure-letter words; mixed case left as is).
- Dictionary: the most valuable words (frequency x bytes saved) get 2-byte codes: lead byte in 0x0E-0x1F (18 leads) + one byte.
  Words are sorted alphabetically before coding, so related words (run, runs, running) get neighbouring codes.
- Reserved bytes 0x05, 0x06, 0x0E-0x1F must be absent from the input (checked). The dictionary is written as a header
  (its size counts in every comparison)."""
import sys, re, collections, struct
LEADS = list(range(0x0E, 0x20)); NCODE = len(LEADS) * 256
WORD = re.compile(rb'[A-Za-z]+')
def build_dict(d, n=NCODE, minlen=4):
    c = collections.Counter(w.lower() for w in WORD.findall(d) if len(w) >= minlen)
    best = sorted(c.items(), key=lambda kv: -kv[1] * (len(kv[0]) - 2))[:n]
    return sorted(w for w, k in best if k * (len(w) - 2) > len(w) + 1)
def fwd(d):
    bad = [b for b in [5, 6] + LEADS if bytes([b]) in d]; assert not bad, 'reserved bytes present: %r' % bad
    import os; words = build_dict(d, int(os.environ.get("DICTN", NCODE))) if os.environ.get("DICTN", "1") != "0" else []; code = {w: bytes([LEADS[i >> 8], i & 255]) for i, w in enumerate(words)}
    def rep(m):
        w = m.group(0); lw = w.lower()
        if w == lw: flag = b''
        elif w[:1].isupper() and w[1:] == lw[1:]: flag = b'\x05'
        elif w == w.upper() and len(w) > 1: flag = b'\x06'
        else: return w
        return flag + code.get(lw, lw)
    body = WORD.sub(rep, d)
    head = b'\n'.join(words); return struct.pack('<I', len(head)) + head + body
def inv(d):
    n = struct.unpack('<I', d[:4])[0]; words = d[4:4 + n].split(b'\n') if n else []; body = d[4 + n:]
    out = bytearray(); i = 0; L = len(body); flag = 0
    while i < L:
        b = body[i]
        if b in (5, 6): flag = b; i += 1; continue
        if 0x0E <= b <= 0x1F:
            w = words[((b - 0x0E) << 8) | body[i + 1]]; i += 2
        else:
            m = WORD.match(body, i) if (65 <= b <= 90 or 97 <= b <= 122) else None
            if m: w = m.group(0); i = m.end()
            else:
                out.append(b); i += 1; flag = 0; continue
        if flag == 5: w = w[:1].upper() + w[1:]
        elif flag == 6: w = w.upper()
        out += w; flag = 0
    return bytes(out)
if __name__ == '__main__':
    mode, a, b = sys.argv[1:4]; d = open(a, 'rb').read(); open(b, 'wb').write(fwd(d) if mode == 'fwd' else inv(d))
