"""AEGIS cosmos: probe hosts, then fetch exoplanets, recent transients, and retry SIMBAD via GET/mirror. Stdlib only."""
import os, json, time, urllib.request, urllib.parse
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[more] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
def get(url,timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=timeout) as r: return r.status, r.read()
for u in ['https://simbad.cds.unistra.fr/simbad/','https://simbad.harvard.edu/simbad/','https://gea.esac.esa.int/archive/','https://exoplanetarchive.ipac.caltech.edu/','https://api.alerce.online/ztf/v1/objects/?page_size=1','https://www.wis-tns.org/','https://vizier.cds.unistra.fr/','https://irsa.ipac.caltech.edu/']:
    try: st,b=get(u,30); log(f'probe {u} -> {st} {len(b)} B')
    except Exception as e: log(f'probe {u} -> FAIL {e}')
# 1) Exoplanets (NASA Exoplanet Archive TAP, default parameter set)
try:
    q="select pl_name,hostname,ra,dec,sy_dist,disc_year,discoverymethod,pl_rade,pl_orbper,pl_eqt,sy_vmag from ps where default_flag=1"
    st,b=get('https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urllib.parse.urlencode({'query':q,'format':'csv'}),300)
    open(os.path.join(RAW,'exoplanets_ps_default.csv'),'wb').write(b); log(f'exoplanets OK {len(b)/1e6:.2f} MB')
except Exception as e: log(f'exoplanets FAIL {e}')
# 2) Recent transients from ALeRCE (ZTF): SN-like classified objects, last ~30 days
try:
    now=time.time(); mjd=now/86400+40587-30
    params={'classifier':'lc_classifier','class':'SNIa','probability':'0.5','firstmjd':str(round(mjd,1)),'page_size':'500','order_by':'lastmjd','order_mode':'DESC'}
    out=[]
    for cls in ['SNIa','SNIbc','SNII','SLSN','TDE','AGN','QSO','CV/Nova']:
        params['class']=cls
        try:
            st,b=get('https://api.alerce.online/ztf/v1/objects/?'+urllib.parse.urlencode(params),120); j=json.loads(b); items=j.get('items',[])
            for it in items: it['_class']=cls
            out+=items; log(f'ALeRCE {cls}: {len(items)}')
        except Exception as e: log(f'ALeRCE {cls} FAIL {e}')
    json.dump(out,open(os.path.join(RAW,'alerce_recent.json'),'w')); log(f'ALeRCE total {len(out)}')
except Exception as e: log(f'ALeRCE FAIL {e}')
# 3) SIMBAD via GET on mirror(s) for flagged stars
try:
    ids=[r[0] for r in json.load(open(os.path.join(HERE,'layers','stars.json')))['flagged']]
    for base in ['https://simbad.cds.unistra.fr/simbad/sim-tap/sync','https://simbad.harvard.edu/simbad/sim-tap/sync']:
        rows=[]; ok=True
        for k in range(0,len(ids),150):
            lst=",".join("'Gaia DR3 %s'"%i for i in ids[k:k+150])
            q=f"SELECT i.id, b.main_id, b.otype FROM ident AS i JOIN basic AS b ON i.oidref=b.oid WHERE i.id IN ({lst})"
            try:
                st,b=get(base+'?'+urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q}),120); rows.append(b.decode('utf-8','replace'))
            except Exception as e: log(f'SIMBAD {base} chunk {k} FAIL {e}'); ok=False; break
        if ok and rows:
            hdr=rows[0].splitlines()[0]; body=[ln for t in rows for ln in t.splitlines()[1:] if ln.strip()]
            open(os.path.join(RAW,'simbad_xmatch.csv'),'w').write(hdr+'\n'+'\n'.join(body)+'\n'); log(f'SIMBAD OK via {base}: {len(body)} matches'); break
except Exception as e: log(f'SIMBAD FAIL {e}')
log('MORE DONE')
