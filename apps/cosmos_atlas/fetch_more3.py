"""AEGIS cosmos: ALeRCE transients by class (param 'class', ranking 1), and Gaia mirror query debug. Stdlib only."""
import os, json, time, urllib.request, urllib.parse, urllib.error
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw')
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[more3] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
out=[]
for cls in ['SNIa','SNIbc','SNII','SLSN','TDE','CV/Nova','AGN','Blazar','QSO']:
    try:
        q={'classifier':'lc_classifier','class':cls,'ranking':'1','probability':'0.4','order_by':'lastmjd','order_mode':'DESC','page_size':'300'}
        with urllib.request.urlopen(urllib.request.Request('https://api.alerce.online/ztf/v1/objects/?'+urllib.parse.urlencode(q),headers=UA),timeout=180) as r: j=json.loads(r.read())
        it=j.get('items',[]); out+=it; log(f'ALeRCE {cls}: {len(it)}; classes returned {sorted(set(x.get("class") for x in it))[:4]}')
    except Exception as e: log(f'ALeRCE {cls} FAIL {e}')
json.dump(out,open(os.path.join(RAW,'alerce_recent3.json'),'w')); log(f'ALeRCE total {len(out)}')
# Gaia mirror debug: tiny queries, print error bodies
for base,q in [('https://gaia.aip.de/tap/sync',"SELECT TOP 3 source_id, redshift_qsoc FROM gaiadr3.qso_candidates"),('https://dc.zah.uni-heidelberg.de/tap/sync',"SELECT TOP 3 * FROM TAP_SCHEMA.tables WHERE table_name LIKE 'gaia%'")]:
    try:
        d=urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q}).encode()
        with urllib.request.urlopen(urllib.request.Request(base,data=d,headers=UA),timeout=120) as r: log(f'{base} OK: '+r.read().decode()[:400].replace('\n',' | '))
    except urllib.error.HTTPError as e: log(f'{base} HTTP {e.code}: '+e.read().decode('utf-8','replace')[:400].replace('\n',' | '))
    except Exception as e: log(f'{base} FAIL {e}')
log('MORE3 DONE')
