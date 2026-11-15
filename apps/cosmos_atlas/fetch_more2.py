"""AEGIS cosmos: recent transients (ALeRCE, fixed params) and Gaia DR3 extragalactic via mirrors (AIP Potsdam, GAVO Heidelberg). Stdlib only."""
import os, json, time, urllib.request, urllib.parse, urllib.error
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[more2] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
def get(url,timeout=180):
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=timeout) as r: return r.read()
# 1) ALeRCE recent classified transients
out=[]
for cls in ['SNIa','SNIbc','SNII','SLSN','TDE','CV/Nova','AGN','Blazar']:
    try:
        q={'classifier':'lc_classifier','class_name':cls,'probability':'0.4','order_by':'lastmjd','order_mode':'DESC','page_size':'300','count':'false'}
        j=json.loads(get('https://api.alerce.online/ztf/v1/objects/?'+urllib.parse.urlencode(q)))
        it=j.get('items',[]); [x.__setitem__('_class',cls) for x in it]; out+=it; log(f'ALeRCE {cls}: {len(it)}')
    except Exception as e: log(f'ALeRCE {cls} FAIL {e}')
json.dump(out,open(os.path.join(RAW,'alerce_recent2.json'),'w')); log(f'ALeRCE total {len(out)}')
# 2) Gaia DR3 extragalactic via mirrors (TAP sync with MAXREC)
qs={'gaia_quasars':"SELECT q.source_id, s.ra, s.dec, s.phot_g_mean_mag AS g, q.redshift_qsoc AS z FROM gaiadr3.qso_candidates AS q JOIN gaiadr3.gaia_source AS s ON q.source_id=s.source_id WHERE q.classlabel_dsc_joint='quasar'",
    'gaia_galaxies':"SELECT g.source_id, s.ra, s.dec, s.phot_g_mean_mag AS g, g.redshift_ugc AS z FROM gaiadr3.galaxy_candidates AS g JOIN gaiadr3.gaia_source AS s ON g.source_id=s.source_id WHERE g.classlabel_dsc_joint='galaxy'"}
for name,q in qs.items():
    outp=os.path.join(RAW,name+'.csv')
    if os.path.exists(outp) and os.path.getsize(outp)>10000: continue
    for base in ['https://gaia.aip.de/tap/sync','https://dc.zah.uni-heidelberg.de/tap/sync','https://gea.esac.esa.int/tap-server/tap/sync']:
        try:
            d=urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','MAXREC':'3000000','QUERY':q}).encode()
            with urllib.request.urlopen(urllib.request.Request(base,data=d,headers=UA),timeout=1800) as r, open(outp,'wb') as f:
                while True:
                    b=r.read(1<<20)
                    if not b: break
                    f.write(b)
            sz=os.path.getsize(outp); log(f'{name} via {base.split("/")[2]}: {sz/1e6:.1f} MB')
            if sz>10000: break
        except Exception as e: log(f'{name} via {base.split("/")[2]} FAIL {e}')
log('MORE2 DONE')
