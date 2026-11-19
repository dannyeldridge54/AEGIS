"""Attach proper motions to the sky map's named stars and constellation-line vertices (for the Time machine).

Source: Yale Bright Star Catalogue, 5th rev. ed. (Hoffleit & Warren 1991, VizieR V/50), JSON from
github.com/brettonw/YaleBrightStarCatalog (bsc5-all.json). pmRA there is mu_alpha*cos(dec), arcsec/yr, J2000/FK5.
Match: nearest BSC star within 0.25 deg (and within 1.0 mag for named stars). Unmatched points get no motion (stay put).
Usage: python tools/build_proper_motions.py <bsc5-all.json>   ->  data/proper_motions.json
"""
import json, math, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parents[1]

def hms(r):  # "06h 45m 08.9s"
    h, m, s = r.replace('h', '').replace('m', '').replace('s', '').split(); return 15 * (int(h) + int(m) / 60 + float(s) / 3600)
def dms(d):  # "-16° 42′ 58″"
    sgn = -1 if d.strip().startswith('-') else 1
    a, b, c = d.replace('+', '').replace('-', '').replace('°', ' ').replace('′', ' ').replace('″', ' ').split()
    return sgn * (int(a) + int(b) / 60 + float(c) / 3600)
def sep(ra1, de1, ra2, de2):
    r = math.radians; c = math.sin(r(de1)) * math.sin(r(de2)) + math.cos(r(de1)) * math.cos(r(de2)) * math.cos(r(ra1 - ra2))
    return math.degrees(math.acos(max(-1, min(1, c))))

def main(path):
    bsc = []
    for s in json.load(open(path, encoding='utf-8')):
        try: bsc.append((hms(s['RA']), dms(s['Dec']), float(s['Vmag']), float(s['pmRA']) * 1000, float(s['pmDE']) * 1000, s.get('HR')))
        except Exception: pass
    cells = {}
    for b in bsc: cells.setdefault((int(b[1] + 90), int(b[0] / 5)), []).append(b)
    def near(ra, de, mag=None):
        best = None
        for dd in (-1, 0, 1):
            for dr in range(-73, 74):
                for b in cells.get((int(de + 90) + dd, (int(ra / 5) + dr) % 72), ()):
                    if abs(dr) > 1 and abs(de) < 80: continue
                    d = sep(ra, de, b[0], b[1])
                    if d < 0.25 and (mag is None or abs(b[2] - mag) < 1.0) and (best is None or d < best[0]): best = (d, b)
        return best[1] if best else None
    stars = json.load(open(HERE / 'data/stars.json', encoding='utf-8'))['stars']
    cons = json.load(open(HERE / 'data/constellations.json', encoding='utf-8'))['constellations']
    out = {'source': 'Yale Bright Star Catalogue 5th ed. (Hoffleit & Warren 1991; VizieR V/50) via github.com/brettonw/YaleBrightStarCatalog',
           'units': 'mas/yr; pmra includes cos(dec); epoch J2000', 'stars': {}, 'lines': {}}
    ns = nv = ms = mv = 0
    for s in stars:
        ns += 1; b = near(s['ra'], s['dec'], s.get('mag'))
        if b: out['stars'][s['name']] = [round(b[3], 1), round(b[4], 1)]; ms += 1
    for c in cons:
        segs = []
        for seg in c['lines']:
            row = []
            for ra, de in seg:
                nv += 1; b = near(ra, de)
                row.append([round(b[3], 1), round(b[4], 1)] if b else None); mv += b is not None
            segs.append(row)
        out['lines'][c['id']] = segs
    out['matched'] = {'stars': [ms, ns], 'line_vertices': [mv, nv]}
    (HERE / 'data/proper_motions.json').write_text(json.dumps(out, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    print(json.dumps(out['matched']), 'Sirius', out['stars'].get('Sirius'), 'Arcturus', out['stars'].get('Arcturus'))

if __name__ == '__main__':
    main(sys.argv[1])
