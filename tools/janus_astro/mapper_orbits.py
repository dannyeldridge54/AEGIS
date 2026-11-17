"""Hyperion -> Star Mapper orbit feed (PC version).

    python -m tools.janus_astro.mapper_orbits --cosmos-map ufe-v2/cosmos_map [--skymap apps/skymap] [--max-tiles N]

Reads the Star Mapper's DR3 tiles (cosmos_map/tiles/L5/NNNNN.csv.gz, Gaia columns as in ufe-v2/aegis/star_scanner.py),
keeps stars with a radial velocity and parallax_over_error > 5, and for each computes (Hyperion, validated D1061, D1072,
D1076, D1077): Galactic l, b (Gaia DR3 convention), Galactocentric position/velocity, M_G (no extinction — flagged), and the
orbit in MWPotential2014 over 3 Gyr: r_peri, r_apo, z_max, eccentricity. Distance: r_med_geo (Bailer-Jones) when present,
else 1/parallax (flag 'dist_parallax'). Per-tile results go to cosmos_map/hyperion/L5/NNNNN.csv.gz (resumable: done tiles
are skipped); a summary for the Sky Map goes to apps/skymap/data/hyperion_orbits.json:
  {"version", "model", "n_stars", "tiles": {tile: {n, med_ecc, med_zmax, med_rperi, med_rapo}}, "most_eccentric": [...50]}
Read-only on the sweep: never changes tiles or sweep state. AI-assisted (Claude); validated by lock PREREG_A8d."""
from __future__ import annotations
import argparse, csv, gzip, json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))
from tools.janus_astro import mapper_feed as F, fast
OUT_COLS = ['source_id', 'l', 'b', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'M_G_noext', 'rperi', 'rapo', 'zmax', 'ecc', 'flags']
def _f(v):
    try:
        x = float(v); return x if math.isfinite(x) else float('nan')
    except (TypeError, ValueError): return float('nan')
def select(rows):
    keep = []
    for r in rows:
        plx, eplx, rv = _f(r.get('parallax')), _f(r.get('parallax_error')), _f(r.get('radial_velocity'))
        if not (math.isfinite(rv) and math.isfinite(plx) and math.isfinite(eplx) and eplx > 0 and plx/eplx > 5): continue
        d = _f(r.get('r_med_geo')); flag = []
        if math.isfinite(d) and d > 0: dk = d/1000.0
        else: dk = 1.0/plx; flag.append('dist_parallax')
        keep.append((r, dk, flag))
    return keep
def process_rows(rows, mw=None):
    keep = select(rows)
    if not keep: return []
    A = lambda k: np.array([_f(r[k]) for r, _, _ in keep])
    ra, dec, pmra, pmdec, rv, G = A('ra'), A('dec'), A('pmra'), A('pmdec'), A('radial_velocity'), A('phot_g_mean_mag')
    plx = A('parallax'); d = np.array([dk for _, dk, _ in keep])
    l, b = F.icrs_to_galactic(ra, dec); p, v = F.galactocentric(ra, dec, d, pmra, pmdec, rv)
    o = fast.orbits_fast(*p, *v, mw=mw)
    MG = F.abs_mag_G(G, plx)
    out = []
    for i, (r, _, flag) in enumerate(keep):
        out.append([r['source_id'], l[i], b[i], *p[:, i], *v[:, i], MG[i], o['rperi'][i], o['rapo'][i], o['zmax'][i], o['ecc'][i],
                    ';'.join(flag + ['MG_noext'])])
    return out
def run(cosmos_map, skymap=None, max_tiles=None, level=5):
    cm = pathlib.Path(cosmos_map); tiles = sorted((cm/'tiles'/f'L{level}').glob('*.csv.gz'))
    outdir = cm/'hyperion'/f'L{level}'; outdir.mkdir(parents=True, exist_ok=True)
    done = skipped = nstars = 0; t0 = time.time()
    for tp in tiles[:max_tiles] if max_tiles else tiles:
        op = outdir/tp.name
        if op.exists(): skipped += 1; continue
        with gzip.open(tp, 'rt', newline='') as fh: rows = list(csv.DictReader(fh))
        res = process_rows(rows)
        tmp = op.with_suffix('.tmp')
        with gzip.open(tmp, 'wt', newline='') as fh:
            w = csv.writer(fh); w.writerow(OUT_COLS); w.writerows(res)
        tmp.replace(op); done += 1; nstars += len(res)
    summary = summarise(outdir)
    if skymap:
        dp = pathlib.Path(skymap)/'data'; dp.mkdir(parents=True, exist_ok=True)
        json.dump(summary, open(dp/'hyperion_orbits.json', 'w', encoding='utf-8'), indent=1)
    return dict(tiles_done=done, tiles_skipped=skipped, stars=nstars, seconds=round(time.time() - t0, 1), summary_stars=summary['n_stars'])
def summarise(outdir):
    tiles = {}; ecc_top = []; n = 0
    for op in sorted(pathlib.Path(outdir).glob('*.csv.gz')):
        with gzip.open(op, 'rt', newline='') as fh: rows = list(csv.DictReader(fh))
        if not rows: continue
        e = np.array([float(r['ecc']) for r in rows]); zm = np.array([float(r['zmax']) for r in rows])
        rp = np.array([float(r['rperi']) for r in rows]); ra = np.array([float(r['rapo']) for r in rows])
        tiles[op.name.split('.')[0]] = dict(n=len(rows), med_ecc=round(float(np.median(e)), 4), med_zmax=round(float(np.median(zm)), 4),
                                            med_rperi=round(float(np.median(rp)), 3), med_rapo=round(float(np.median(ra)), 3))
        n += len(rows)
        for r in rows: ecc_top.append((float(r['ecc']), r['source_id'], round(float(r['l']), 4), round(float(r['b']), 4), round(float(r['zmax']), 3)))
    ecc_top.sort(reverse=True)
    return dict(version='hyperion-orbits-1', model='MWPotential2014 (Bovy 2015) via Hyperion; Gaia DR3 Galactic convention; 3 Gyr orbits',
                n_stars=n, tiles=tiles,
                most_eccentric=[dict(source_id=s, ecc=round(e_, 4), l=l_, b=b_, zmax=z_) for e_, s, l_, b_, z_ in ecc_top[:50]],
                notes='Descriptive orbit parameters, no population classification; M_G without extinction; distance from r_med_geo or 1/parallax (flagged).')
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--cosmos-map', required=True); ap.add_argument('--skymap'); ap.add_argument('--max-tiles', type=int)
    a = ap.parse_args(argv); print(json.dumps(run(a.cosmos_map, a.skymap, a.max_tiles))); return 0
if __name__ == '__main__': sys.exit(main())
