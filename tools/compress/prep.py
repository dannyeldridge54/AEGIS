#!/usr/bin/env python3
"""Reversible enwik preprocessing (Loom rings outside the coder). fwd/inv. Requires bytes 0x01-0x04 absent in input (checked)."""
import sys, re
M = {b'&quot;': b'\x01', b'&gt;': b'\x02', b'&lt;': b'\x03', b'&amp;': b'\x04'}; INV = {v: k for k, v in M.items()}
def fwd(d):
    assert not any(b in d for b in INV), 'reserved byte present'
    return re.sub(rb'&quot;|&gt;|&lt;|&amp;', lambda m: M[m.group(0)], d)
def inv(d): return re.sub(rb'[\x01-\x04]', lambda m: INV[m.group(0)], d)
if __name__ == '__main__':
    mode, a, b = sys.argv[1:4]; d = open(a, 'rb').read(); open(b, 'wb').write(fwd(d) if mode == 'fwd' else inv(d))
