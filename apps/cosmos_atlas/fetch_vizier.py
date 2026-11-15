"""AEGIS cosmos: VizieR via TAP (fix for asu-tsv 404). Stdlib only."""
import os, time, urllib.request, urllib.parse
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw'); os.makedirs(RAW,exist_ok=True)
LOG=open(os.path.join(HERE,'fetch_log.txt'),'a')
def log(m): s=time.strftime('%H:%M:%S ')+'[vizier] '+m; print(s,flush=True); LOG.write(s+'\n'); LOG.flush()
TAP='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync'
UA={'User-Agent':'AEGIS-cosmos-map/1.0'}
def q(adql,fmt='csv',maxrec=2000000,timeout=900):
    d=urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':fmt,'MAXREC':str(maxrec),'QUERY':adql}).encode()
    with urllib.request.urlopen(urllib.request.Request(TAP,data=d,headers=UA),timeout=timeout) as r: return r.read()
cats={'2MRS':'J/ApJS/199/26','CF4':'J/ApJ/944/94','LocalGroup':'J/AJ/144/4'}
for name,pre in cats.items():
    try:
        t=q(f"SELECT table_name, description FROM TAP_SCHEMA.tables WHERE table_name LIKE '{pre}/%'").decode()
        log(f'{name} tables:\n'+t.strip())
        names=[ln.split(',')[0].strip().strip('"') for ln in t.strip().splitlines()[1:] if ln.strip()]
        for tn in names:
            out=os.path.join(RAW,name+'__'+tn.replace('/','_')+'.csv')
            if os.path.exists(out) and os.path.getsize(out)>500: log('skip '+out); continue
            try:
                b=q(f'SELECT * FROM "{tn}"'); open(out,'wb').write(b); log(f'OK {os.path.basename(out)} {len(b)/1e6:.2f} MB')
            except Exception as e: log(f'FAIL {tn}: {e}')
    except Exception as e: log(f'FAIL {name}: {e}')
log('VIZIER DONE')
