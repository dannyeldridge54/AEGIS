"""D571 follow-up: SIMBAD (Harvard mirror) lookups of Gaia DR3 ids; optional cone list. Stdlib."""
import os, time, urllib.request, urllib.parse, urllib.error, csv, io
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw')
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[hunts2] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}; TAP='https://simbad.harvard.edu/simbad/sim-tap/sync'
def q(adql):
    d=urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':adql}).encode()
    with urllib.request.urlopen(urllib.request.Request(TAP,data=d,headers=UA),timeout=300) as r: return r.read().decode('utf-8','replace')
ids=[x.strip() for x in open(os.path.join(HERE,'hunt_simbad_ids.txt')) if x.strip()]
out=['gaia_id,main_id,otype,nbref']
for i in range(0,len(ids),300):
    chunk=ids[i:i+300]; lst=','.join("'Gaia DR3 %s'"%x for x in chunk)
    try:
        t=q(f"SELECT i.id, b.main_id, b.otype, b.nbref FROM ident AS i JOIN basic AS b ON b.oid=i.oidref WHERE i.id IN ({lst})")
        rows=list(csv.reader(io.StringIO(t)))[1:]
        for r in rows: out.append(','.join([r[0].replace('Gaia DR3 ','')]+['"%s"'%r[1].replace('"','')]+r[2:]))
        log(f'ident chunk {i}: {len(rows)} hits')
    except urllib.error.HTTPError as e: log(f'chunk {i} HTTP {e.code} '+e.read().decode()[:300])
    except Exception as e: log(f'chunk {i} FAIL {e}')
open(os.path.join(RAW,'hunt_simbad_ids_result.csv'),'w').write('\n'.join(out)); log(f'saved {len(out)-1}')
cf=os.path.join(HERE,'hunt_cones.txt')
if os.path.exists(cf):
    out=['tag,main_id,otype,sep_arcsec,nbref']
    for line in open(cf):
        if not line.strip(): continue
        tag,ra,dec=line.split(',')[:3]
        try:
            t=q(f"SELECT main_id, otype, DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',{ra},{dec}))*3600 AS sep, nbref FROM basic WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{dec},0.00139))=1")
            for r in list(csv.reader(io.StringIO(t)))[1:]: out.append(','.join([tag,'"%s"'%r[0]]+r[1:]))
        except Exception as e: log(f'cone {tag} FAIL {e}')
    open(os.path.join(RAW,'hunt_simbad_cones.csv'),'w').write('\n'.join(out)); log(f'cones saved {len(out)-1}')
log('HUNTS2 DONE')
