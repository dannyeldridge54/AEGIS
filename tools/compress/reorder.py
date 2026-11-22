#!/usr/bin/env python3
"""STARLIT-lite reorder (D2063). usage: reorder.py fwd in out perm | inv in perm out"""
import re, sys, numpy as np
def split(d):
    starts = [m.start() for m in re.finditer(rb'  <page>', d)]; ends = [m.end() for m in re.finditer(rb'</page>\n', d)]
    head, tail = d[:starts[0]], d[ends[-1]:]; pages = [d[s:e] for s, e in zip(starts, ends)]
    assert head + b''.join(pages) + tail == d; return head, pages, tail
def fwd(inp, out, permf):
    from sklearn.feature_extraction.text import TfidfVectorizer
    d = open(inp, 'rb').read(); head, pages, tail = split(d)
    X = TfidfVectorizer(sublinear_tf=True, max_features=1 << 18, token_pattern=r'[A-Za-z]{3,}').fit_transform([p.decode('utf8', 'ignore') for p in pages])
    n = len(pages); used = np.zeros(n, bool); order = [0]; used[0] = True; Xt = X.T.tocsc()
    for _ in range(n - 1):
        s = (X[order[-1]] @ Xt).toarray().ravel(); s[used] = -1; j = int(s.argmax()); order.append(j); used[j] = True
    open(out, 'wb').write(head + b''.join(pages[i] for i in order) + tail)
    open(permf, 'wb').write(np.array(order, dtype='<u2').tobytes())
def inv(inp, permf, out):
    d = open(inp, 'rb').read(); head, pages, tail = split(d); order = np.frombuffer(open(permf, 'rb').read(), dtype='<u2')
    orig = [None] * len(pages)
    for k, i in enumerate(order): orig[i] = pages[k]
    open(out, 'wb').write(head + b''.join(orig) + tail)
if __name__ == '__main__':
    fwd(*sys.argv[2:5]) if sys.argv[1] == 'fwd' else inv(*sys.argv[2:5])
