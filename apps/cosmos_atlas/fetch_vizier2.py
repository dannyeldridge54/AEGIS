"""AEGIS cosmos: VizieR catalogs via the Harvard CfA mirror (asu-tsv). Stdlib only."""
import os, time, urllib.request, urllib.parse
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[vizier2] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
cats=[('2MRS','J/ApJS/199/26/table3'),('CF4','J/ApJ/944/94/table1'),('CF4_groups','J/ApJ/944/94/table2'),('LocalGroup','J/AJ/144/4/NearbyGal'),('VSX','B/vsx/vsx')]
for base in ['https://vizier.cfa.harvard.edu/viz-bin/asu-tsv','https://vizier.cds.unistra.fr/viz-bin/asu-tsv']:
    for name,src in cats:
        out=os.path.join(RAW,f'viz_{name}.tsv')
        if os.path.exists(out) and os.path.getsize(out)>2000: continue
        maxr='unlimited' if name!='VSX' else '2000000'
        q=urllib.parse.urlencode({'-source':src,'-out.max':maxr,'-out.all':'1'})
        if name=='VSX': q=urllib.parse.urlencode({'-source':src,'-out.max':maxr,'-out':'Name,RAJ2000,DEJ2000,Type,max,min,Period','max':'<11'})
        try:
            with urllib.request.urlopen(urllib.request.Request(base+'?'+q,headers=UA),timeout=900) as r, open(out,'wb') as f:
                while True:
                    b=r.read(1<<20)
                    if not b: break
                    f.write(b)
            log(f'{base.split("/")[2]} {name} OK {os.path.getsize(out)/1e6:.2f} MB')
        except Exception as e: log(f'{base.split("/")[2]} {name} FAIL {e}')
log('VIZIER2 DONE')
