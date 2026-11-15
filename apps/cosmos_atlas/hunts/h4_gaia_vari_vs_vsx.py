"""D571 H4: bright Gaia DR3 classified variables (G<11, score>=0.7) not in VSX (max<13) within 10 arcsec (PREREG_D571)."""
import sys, json, numpy as np, pandas as pd, io
from astropy.coordinates import SkyCoord; import astropy.units as u
g=pd.read_csv(sys.argv[1]).drop_duplicates('source_id')
txt=[l for l in open(sys.argv[2]) if not l.startswith('#') and l.strip()]
v=pd.read_csv(io.StringIO(''.join([txt[0]]+txt[3:])),sep='\t'); v.columns=[c.strip() for c in v.columns]
v=v[pd.to_numeric(v.RAJ2000,errors='coerce').notna()]
pmra=g.pmra.fillna(0); pmdec=g.pmdec.fillna(0); dt=-16.0
ra2000=g.ra+pmra*dt/3.6e6/np.cos(np.radians(g.dec)); de2000=g.dec+pmdec*dt/3.6e6
cg=SkyCoord(ra2000.values*u.deg,de2000.values*u.deg); cv=SkyCoord(v.RAJ2000.astype(float).values*u.deg,v.DEJ2000.astype(float).values*u.deg)
idx,sep,_=cg.match_to_catalog_sky(cv); g['sep_vsx']=sep.arcsec; g['vsx_name']=v.Name.str.strip().values[idx]; g['vsx_type']=v.Type.str.strip().values[idx]
g['matched']=g.sep_vsx<10
per=g.groupby('best_class_name').agg(N=('source_id','size'),matched=('matched','sum')); per['unmatched']=per.N-per.matched
un=g[~g.matched].sort_values('best_class_score',ascending=False)
out=dict(summary=dict(N_total=len(g),N_matched=int(g.matched.sum()),N_unmatched=len(un),N_vsx=len(v)),per_class=per.reset_index().to_dict('records'),
 unmatched=un[['source_id','ra','dec','phot_g_mean_mag','best_class_name','best_class_score','sep_vsx']].round(5).astype({'source_id':str}).to_dict('records'))
json.dump(out,open(sys.argv[3],'w')); print(out['summary']); print(per.sort_values('N',ascending=False).to_string())
print(un.head(12)[['source_id','ra','dec','phot_g_mean_mag','best_class_name','best_class_score','sep_vsx','vsx_name']].to_string())
