"""AEGIS cosmos catalog fetcher (Danny approved downloads 14 Nov 2026 23:21 CT). Stdlib only. Writes raw/ + fetch_log.txt."""
import os, sys, time, urllib.request, urllib.error, urllib.parse, xml.etree.ElementTree as ET
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0 (independent research)'}
def get(url,out,data=None,timeout=900):
    if os.path.exists(out) and os.path.getsize(out)>1000: log(f'skip (exists) {os.path.basename(out)}'); return True
    try:
        req=urllib.request.Request(url,data=data,headers=UA)
        with urllib.request.urlopen(req,timeout=timeout) as r, open(out+'.part','wb') as f:
            while True:
                b=r.read(1<<20)
                if not b: break
                f.write(b)
        os.replace(out+'.part',out); log(f'OK {os.path.basename(out)} {os.path.getsize(out)/1e6:.1f} MB'); return True
    except Exception as e: log(f'FAIL {os.path.basename(out)}: {e}'); return False
# 1) VizieR catalogs (TSV, all rows)
viz=[('2MRS_Huchra2012','J/ApJS/199/26/table3'),('CF4_Tully2023','J/ApJ/944/94'),('LocalGroup_McConnachie2012','J/AJ/144/4'),('Gaia_CRF3_quasars_check','I/356')]
for name,src in viz[:3]:
    q=urllib.parse.urlencode({'-source':src,'-out.max':'unlimited','-out.all':'','-out.form':'|'})
    get('https://vizier.cds.unistra.fr/viz-bin/asu-tsv?'+q, os.path.join(RAW,name+'.tsv'))
# 2) Gaia DR3 extragalactic (async TAP)
def gaia(adql,out):
    if os.path.exists(out) and os.path.getsize(out)>1000: log(f'skip (exists) {os.path.basename(out)}'); return
    base='https://gea.esac.esa.int/tap-server/tap/async'
    try:
        d=urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','PHASE':'RUN','QUERY':adql}).encode()
        class NR(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*a,**k): return None
        req=urllib.request.Request(base,data=d,headers={**UA,'Content-Type':'application/x-www-form-urlencoded'})
        try:
            urllib.request.build_opener(NR()).open(req,timeout=180); raise RuntimeError('no redirect')
        except urllib.error.HTTPError as e:
            if e.code!=303: raise
            job=urllib.parse.urljoin(base+'/',e.headers['Location'])
        log(f'Gaia job {job}')
        for i in range(720):
            with urllib.request.urlopen(urllib.request.Request(job+'/phase',headers=UA),timeout=60) as r: ph=r.read().decode().strip()
            if ph in ('COMPLETED','ERROR','ABORTED'): break
            time.sleep(10)
        log(f'Gaia job phase {ph}')
        if ph=='COMPLETED': get(job+'/results/result',out,timeout=3600)
        else:
            with urllib.request.urlopen(urllib.request.Request(job+'/error',headers=UA),timeout=60) as r: log('Gaia error: '+r.read().decode()[:500])
    except Exception as e: log(f'Gaia FAIL {os.path.basename(out)}: {e}')
gaia("SELECT q.source_id, s.ra, s.dec, s.l, s.b, s.phot_g_mean_mag, q.redshift_qsoc, q.classprob_dsc_combmod_quasar FROM gaiadr3.qso_candidates AS q JOIN gaiadr3.gaia_source AS s USING (source_id) WHERE q.classlabel_dsc_joint='quasar'", os.path.join(RAW,'gaia_dr3_quasars_pure.csv'))
gaia("SELECT g.source_id, s.ra, s.dec, s.l, s.b, s.phot_g_mean_mag, g.redshift_ugc, g.classprob_dsc_combmod_galaxy FROM gaiadr3.galaxy_candidates AS g JOIN gaiadr3.gaia_source AS s USING (source_id) WHERE g.classlabel_dsc_joint='galaxy'", os.path.join(RAW,'gaia_dr3_galaxies_pure.csv'))
# 3) SDSS DR17 spectroscopic objects (chunks by class and plate range, TOP limit per query)
def sdss(sql,out):
    q=urllib.parse.urlencode({'cmd':sql,'format':'csv'})
    get('https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch?'+q,out,timeout=1800)
for cls in ('GALAXY','QSO'):
    for lo,hi in ((0,4000),(4000,8000),(8000,12000),(12000,20000)):
        sdss(f"SELECT ra, dec, z, class, subClass, plate FROM SpecObj WHERE class='{cls}' AND zWarning=0 AND plate>={lo} AND plate<{hi}", os.path.join(RAW,f'sdss_dr17_{cls.lower()}_{lo}_{hi}.csv'))
log('ALL DONE')
