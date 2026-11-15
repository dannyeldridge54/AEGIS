"""AEGIS cosmos: cross-match flagged fast stars with SIMBAD and Gaia DR3 (RV, RUWE, epoch photometry). Stdlib only."""
import os, json, time, csv, io, urllib.request, urllib.parse, urllib.error
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[xmatch] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
ids=[r[0] for r in json.load(open(os.path.join(HERE,'layers','stars.json')))['flagged']]
log(f'{len(ids)} flagged ids')
def post(url,params,timeout=600):
    d=urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=d,headers=UA),timeout=timeout) as r: return r.read().decode('utf-8','replace')
# SIMBAD TAP in chunks
out=os.path.join(RAW,'simbad_xmatch.csv'); rows=[]
for k in range(0,len(ids),300):
    chunk=ids[k:k+300]; lst=",".join("'Gaia DR3 %s'"%i for i in chunk)
    q=f"SELECT i.id, b.main_id, b.otype, b.rvz_radvel, b.sp_type FROM ident AS i JOIN basic AS b ON i.oidref=b.oid WHERE i.id IN ({lst})"
    for attempt in range(3):
        try:
            t=post('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q}); rows.append(t); break
        except Exception as e: log(f'SIMBAD chunk {k} attempt {attempt}: {e}'); time.sleep(5)
if rows:
    hdr=rows[0].splitlines()[0]; body=[ln for t in rows for ln in t.splitlines()[1:] if ln.strip()]
    open(out,'w').write(hdr+'\n'+'\n'.join(body)+'\n'); log(f'SIMBAD OK {len(body)} matches')
# Gaia DR3: RV, RUWE, epoch photometry, variability flag (sync, chunks)
out2=os.path.join(RAW,'gaia_flagged_extra.csv'); g=[]
for k in range(0,len(ids),400):
    q=f"SELECT source_id, ruwe, radial_velocity, radial_velocity_error, has_epoch_photometry, phot_variable_flag, parallax, parallax_error FROM gaiadr3.gaia_source WHERE source_id IN ({','.join(ids[k:k+400])})"
    for attempt in range(3):
        try: g.append(post('https://gea.esac.esa.int/tap-server/tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q},timeout=300)); break
        except Exception as e: log(f'Gaia chunk {k} attempt {attempt}: {e}'); time.sleep(5)
if g:
    hdr=g[0].splitlines()[0]; body=[ln for t in g for ln in t.splitlines()[1:] if ln.strip()]
    open(out2,'w').write(hdr+'\n'+'\n'.join(body)+'\n'); log(f'Gaia extra OK {len(body)} rows')
log('XMATCH DONE')
