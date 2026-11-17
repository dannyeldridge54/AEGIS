import csv, gzip, json, math, pathlib, shutil, sys, tempfile, hashlib, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import mapper_orbits as MO, mapper_feed as F, fast
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
sys.path.insert(0, 'ufe-v2'); from aegis import star_scanner as SS
cols = list(dict.fromkeys(SS.COLUMNS + list(SS.ASTROMETRY_FIELDS)))
tmp = pathlib.Path(tempfile.mkdtemp()); cm = tmp/'cosmos_map'; td = cm/'tiles'/'L5'; td.mkdir(parents=True); sk = tmp/'skymap'
r = np.random.default_rng(5); allrows = []
for t in (101, 202):
    rows = []
    for i in range(60):
        plx = r.uniform(0.2, 5); row = {c: '' for c in cols}
        fr = lambda x: repr(float(x))          # A8d D1: plain decimal strings
        row.update(source_id=str(t*1000 + i), ra=fr(r.uniform(0, 360)), dec=fr(math.degrees(math.asin(r.uniform(-1, 1)))), parallax=fr(plx),
                   parallax_error=fr(plx/r.choice([3.0, 8.0, 20.0])), pmra=fr(r.normal(0, 10)), pmdec=fr(r.normal(0, 10)),
                   radial_velocity=fr(r.normal(0, 40)) if r.uniform() > 0.3 else '', phot_g_mean_mag=fr(r.uniform(8, 16)),
                   bp_rp=fr(r.uniform(0, 2)), ruwe=fr(r.uniform(0.8, 1.4)), r_med_geo=fr(1000/plx*r.uniform(0.95, 1.05)) if r.uniform() > 0.2 else '')
        rows.append(row)
    with gzip.open(td/f'{t:05d}.csv.gz', 'wt', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    allrows += rows
res1 = MO.run(cm, sk); P('run 1:', res1)
outs = {}
for op in sorted((cm/'hyperion'/'L5').glob('*.csv.gz')):
    with gzip.open(op, 'rt', newline='') as fh: outs.update({rr['source_id']: rr for rr in csv.DictReader(fh)})
expect = [rw for rw in allrows if rw['radial_velocity'] and float(rw['parallax'])/float(rw['parallax_error']) > 5]
m1 = set(outs) == {rw['source_id'] for rw in expect}
for rw in expect:
    fl = outs[rw['source_id']]['flags'].split(';'); m1 &= ('MG_noext' in fl) and (('dist_parallax' in fl) == (rw['r_med_geo'] == ''))
ok['M1'] = m1; P(f'M1 selection: {len(outs)} processed of {len(allrows)} (expected {len(expect)}): {"PASS" if m1 else "FAIL"}')
g = lambda k: np.array([float(rw[k]) for rw in expect])
d = np.array([float(rw['r_med_geo'])/1000 if rw['r_med_geo'] else 1/float(rw['parallax']) for rw in expect])
l, b = F.icrs_to_galactic(g('ra'), g('dec')); p, v = F.galactocentric(g('ra'), g('dec'), d, g('pmra'), g('pmdec'), g('radial_velocity'))
o = fast.orbits_fast(*p, *v); MG = F.abs_mag_G(g('phot_g_mean_mag'), g('parallax'))
worst = 0.0
for i, rw in enumerate(expect):
    got = outs[rw['source_id']]
    ref = dict(l=l[i], b=b[i], x=p[0, i], y=p[1, i], z=p[2, i], vx=v[0, i], vy=v[1, i], vz=v[2, i], M_G_noext=MG[i],
               rperi=o['rperi'][i], rapo=o['rapo'][i], zmax=o['zmax'][i], ecc=o['ecc'][i])
    for k, x in ref.items():
        y = float(got[k]); e = abs(y - x)/abs(x) if x != 0 else abs(y); worst = max(worst, e)
ok['M2'] = worst <= 1e-12; P(f'M2 values vs direct calls: worst {worst:.1e}')
h1 = {p_.name: hashlib.sha256(p_.read_bytes()).hexdigest() for p_ in (cm/'hyperion'/'L5').glob('*.csv.gz')}
res2 = MO.run(cm, sk); h2 = {p_.name: hashlib.sha256(p_.read_bytes()).hexdigest() for p_ in (cm/'hyperion'/'L5').glob('*.csv.gz')}
ok['M3'] = res2['tiles_done'] == 0 and res2['tiles_skipped'] == 2 and h1 == h2; P('M3 resume:', res2, 'identical' if h1 == h2 else 'CHANGED')
S = json.load(open(sk/'data'/'hyperion_orbits.json'))
m4 = all(k in S for k in ('version', 'model', 'n_stars', 'tiles', 'most_eccentric')) and S['n_stars'] == len(expect)
m4 &= all(set(t_) == {'n', 'med_ecc', 'med_zmax', 'med_rperi', 'med_rapo'} for t_ in S['tiles'].values())
es = [x['ecc'] for x in S['most_eccentric']]; m4 &= es == sorted(es, reverse=True) and len(es) <= 50
ok['M4'] = m4; P(f'M4 summary: n_stars {S["n_stars"]}, tiles {list(S["tiles"])}, top ecc {es[:3]}: {"PASS" if m4 else "FAIL"}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x else "FAIL"}' for k, x in ok.items()), '-> A8d', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
shutil.rmtree(tmp)
open('field_tests/results/janus_astro_a8d.txt', 'w').write('\n'.join(out) + '\n')
