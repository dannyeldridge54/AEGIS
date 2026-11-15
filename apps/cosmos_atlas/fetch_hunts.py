"""AEGIS cosmos D571 hunts: downloads only (stdlib). Gaia (AIP TAP, async), TESS TOIs, Milliquas, VSX<13."""
import os, json, time, urllib.request, urllib.parse, urllib.error, xml.etree.ElementTree as ET, csv, io
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[hunts] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
AIP='https://gaia.aip.de/tap'
def vot_to_csv(b):
    rows=[];cols=[];
    for ev,el in ET.iterparse(io.BytesIO(b),events=('end',)):
        t=el.tag.split('}')[-1]
        if t=='FIELD': cols.append(el.get('name'))
        elif t=='TR': rows.append([(td.text or '') for td in el]); el.clear()
        elif t=='INFO' and el.get('name')=='QUERY_STATUS' and el.get('value')=='ERROR': raise RuntimeError('VOT ERROR: '+(el.text or ''))
    o=io.StringIO(); w=csv.writer(o); w.writerow(cols); w.writerows(rows); return o.getvalue().encode()
def norm(b):
    s=b.lstrip()[:200]
    if s.startswith(b'<'):
        if b'BINARY' in b[:5000]: raise RuntimeError('binary votable')
        return vot_to_csv(b)
    return b
P=lambda q:{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','RESPONSEFORMAT':'csv','QUERY':q}
def sync(q,base=AIP,t=300):
    d=urllib.parse.urlencode(P(q)).encode()
    with urllib.request.urlopen(urllib.request.Request(base+'/sync',data=d,headers=UA),timeout=t) as r: return norm(r.read())
def asyncq(q,base=AIP,maxwait=3600):
    d=P(q); d['PHASE']='RUN'
    with urllib.request.urlopen(urllib.request.Request(base+'/async',data=urllib.parse.urlencode(d).encode(),headers=UA),timeout=120) as r:
        job=r.geturl(); body=r.read()
    if job.rstrip('/').endswith('async'):
        # no redirect followed; find jobId in body
        txt=body.decode('utf-8','replace'); import re; m=re.search(r'<uws:jobId>([^<]+)',txt)
        job=base+'/async/'+m.group(1)
    log('job '+job); t0=time.time(); ph=''
    try: urllib.request.urlopen(urllib.request.Request(job+'/phase',data=b'PHASE=RUN',headers=UA),timeout=60).read()
    except Exception as e: pass
    while time.time()-t0<maxwait:
        ph=urllib.request.urlopen(urllib.request.Request(job+'/phase',headers=UA),timeout=60).read().decode().strip()
        if ph in ('COMPLETED','ERROR','ABORTED'): break
        time.sleep(10)
    log(f'phase {ph} after {time.time()-t0:.0f}s')
    if ph!='COMPLETED':
        try: log('err: '+urllib.request.urlopen(urllib.request.Request(job+'/error',headers=UA),timeout=60).read().decode('utf-8','replace')[:600])
        except Exception as e: log(f'err fetch fail {e}')
        raise RuntimeError(ph)
    with urllib.request.urlopen(urllib.request.Request(job+'/results/result',headers=UA),timeout=1800) as r: return norm(r.read())
def herr(e): return f'HTTP {e.code}: '+e.read().decode('utf-8','replace')[:500].replace('\n',' | ') if isinstance(e,urllib.error.HTTPError) else repr(e)
def save(name,b):
    open(os.path.join(RAW,name),'wb').write(b); n=b.count(b'\n')-1; log(f'{name}: {len(b)/1e6:.1f} MB, {n} rows')
def gaia_job(name,variants,big=True):
    for v in variants:
        try:
            probe=v.replace('SELECT ','SELECT TOP 5 ',1); b=sync(probe,t=180); log(f'{name} probe OK: '+b.decode()[:200].replace('\n',' | '))
        except Exception as e: log(f'{name} probe FAIL {herr(e)} :: {v[:120]}'); continue
        for mode in (['async','sync'] if big else ['sync','async']):
            try: b=asyncq(v) if mode=='async' else sync(v,t=1800); save(name,b); return True
            except Exception as e: log(f'{name} {mode} FAIL {herr(e)}')
    return False
# H2 fast stars
ids=[x.strip() for x in open(os.path.join(HERE,'hunt_star_ids.txt')) if x.strip()]
cols='source_id, ra, dec, parallax, parallax_error, pmra, pmra_error, pmdec, pmdec_error, radial_velocity, radial_velocity_error, phot_g_mean_mag'
q2=f"SELECT {cols} FROM gaiadr3.gaia_source WHERE source_id IN ({','.join(ids)})"
try: save('hunt_faststars_gaia.csv',sync(q2))
except Exception as e:
    log('H2 AIP FAIL '+herr(e))
    try: save('hunt_faststars_gaia.csv',sync(q2.replace('gaiadr3.gaia_source','gaia.dr3lite'),base='https://dc.zah.uni-heidelberg.de/tap'))
    except Exception as e2: log('H2 GAVO FAIL '+herr(e2))
# H3 TOIs
try:
    u='https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urllib.parse.urlencode({'query':'select * from toi','format':'csv'})
    with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=600) as r: save('hunt_toi.csv',r.read())
except Exception as e: log('H3 FAIL '+herr(e))
# VizieR (CfA): Milliquas + VSX<13
def viz(name,params):
    try:
        u='https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?'+urllib.parse.urlencode(params)
        with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=1800) as r: save(name,r.read())
    except Exception as e: log(f'{name} FAIL '+herr(e))
viz('hunt_milliquas.tsv',{'-source':'VII/294/catalog','-out.max':'unlimited','-out':'RAJ2000,DEJ2000,Name,Type,z'})
viz('hunt_vsx13.tsv',{'-source':'B/vsx/vsx','-out.max':'unlimited','-out':'Name,RAJ2000,DEJ2000,Type,max','max':'<13'})
# H4 Gaia variables G<11
gaia_job('hunt_gaia_vari.csv',[
 "SELECT v.source_id, g.ra, g.dec, g.pmra, g.pmdec, g.phot_g_mean_mag, v.best_class_name, v.best_class_score FROM gaiadr3.vari_classifier_result AS v JOIN gaiadr3.gaia_source AS g ON g.source_id = v.source_id WHERE g.phot_g_mean_mag < 11 AND v.best_class_score >= 0.7",
 "SELECT v.source_id, g.ra, g.dec, g.pmra, g.pmdec, g.phot_g_mean_mag, v.best_class_name, v.best_class_score FROM gaiadr3.vari_classifier_result v INNER JOIN gaiadr3.gaia_source g ON g.source_id = v.source_id WHERE g.phot_g_mean_mag < 11 AND v.best_class_score >= 0.7"])
# H1 Gaia quasars
gaia_job('hunt_gaia_qso.csv',[
 "SELECT q.source_id, g.ra, g.dec, g.phot_g_mean_mag, q.redshift_qsoc, q.flags_qsoc FROM gaiadr3.qso_candidates AS q JOIN gaiadr3.gaia_source AS g ON g.source_id = q.source_id WHERE q.classlabel_dsc_joint = 'quasar'",
 "SELECT q.source_id, g.ra, g.dec, g.phot_g_mean_mag, q.redshift_qsoc, q.flags_qsoc FROM gaiadr3.qso_candidates q INNER JOIN gaiadr3.gaia_source g ON g.source_id = q.source_id WHERE q.classlabel_dsc_joint = 'quasar'"])
log('HUNTS DONE')
