"""Build CubeMind's aegis_link/ folder from this repo (Danny 2026-11-18: "link everything to cubemind to learn").
Usage (repo root): python tools/cubemind_link/build_link.py <out_dir>
Copies the ladder's state (DERIVATION_LOG, map, sync ledger, postulates) and lists every lock with its sha256.
CubeMind's learn loop ingests the folder with honest tiers (mindmem/ingest.py aegis_link). Read-only on the repo."""
import pathlib, shutil, sys
R = pathlib.Path(__file__).resolve().parents[2]
FILES = {'DERIVATION_LOG.md': 'theory/derivations/DERIVATION_LOG.md', 'map.yaml': 'theory/map/map.yaml',
         'sync.yaml': 'theory/map/sync.yaml', 'POSTULATES.md': 'theory/derivations/POSTULATES.md'}
def build(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    for dst, src in FILES.items(): shutil.copyfile(R / src, out / dst)
    locks = []
    for s in sorted((R / 'field_tests/rules').glob('PREREG_*.sha256')):
        h = s.read_text(encoding='utf-8', errors='replace').split()
        if h: locks.append(f"{s.name[:-7]} {h[0]}")
    (out / 'locks.txt').write_text('\n'.join(locks) + '\n', encoding='utf-8')
    import re   # every D-note heading (record checks in Janus look cited D-numbers up here)
    ids = re.findall(r'^(?:#{2,4} \**|\*\*)(D\d+[a-z]?)\b', (R / 'theory/pending_docs/D72_D75_weak_spots.md').read_text(encoding='utf-8'), re.M)
    (out / 'dnotes_index.txt').write_text(' '.join(sorted(set(ids))) + '\n', encoding='utf-8')
    return {k: (out / k).stat().st_size for k in list(FILES) + ['locks.txt', 'dnotes_index.txt']}
if __name__ == '__main__':
    print(build(sys.argv[1] if len(sys.argv) > 1 else 'aegis_link'))
