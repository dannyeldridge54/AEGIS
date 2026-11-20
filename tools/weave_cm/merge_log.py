"""Merged DERIVATION_LOG for CubeMind (house format '## D####: …'): the ladder log plus every D-note of the main log
not already in it. Headers are normalised so CubeMind's ingest parser reads them; bodies are copied unchanged."""
import re, sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
L = (R / 'theory/derivations/DERIVATION_LOG.md').read_text(encoding='utf-8')
W = (R / 'theory/pending_docs/D72_D75_weak_spots.md').read_text(encoding='utf-8')
have = set(re.findall(r'^## (D\d+[a-z]?)\b', L, re.M))
blocks = re.split(r'\n(?=(?:#{2,4} \**|\*\*)D\d+[a-z]?\b)', W)
out = [L.rstrip(), '\n\n# Main-log D-notes (merged for CubeMind, house format)\n']
n = 0
for b in blocks:
    m = re.match(r'(?:#{2,4} \**|\*\*)(D\d+[a-z]?)\b\**\s*[:—–-]?\s*(.*)', b)
    if not m or m.group(1) in have: continue
    first, _, rest = b.partition('\n'); title = re.sub(r'\*\*', '', m.group(2)).strip(' —:') or first
    out.append(f'## {m.group(1)}: {title}\n{rest}\n'); have.add(m.group(1)); n += 1
pathlib.Path(sys.argv[1]).write_text('\n'.join(out), encoding='utf-8')
print(n, 'notes merged;', len(have), 'total')
