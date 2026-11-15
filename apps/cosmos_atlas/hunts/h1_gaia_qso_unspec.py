"""D571 H1: Gaia DR3 DSC-joint quasars with no SDSS DR17 / Milliquas-spectroscopic match within 2 arcsec (PREREG_D571)."""
import sys, json, glob, io, numpy as np, pandas as pd
from astropy.coordinates import SkyCoord; import astropy.units as u
gq=pd.read_csv(sys.argv[1]).drop_duplicates('source_id')
sd=pd.concat([pd.read_csv(f,comment='#') for f in glob.glob(sys.argv[2])]); sd=sd[pd.to_numeric(sd.ra,errors='coerce').notna()]
txt=[l for l in open(sys.argv[3]) if not l.startswith('#') and l.strip()]
mq=pd.read_csv(io.StringIO(''.join([txt[0]]+txt[3:])),sep='\t'); mq.columns=[c.strip() for c in mq.columns]
mq=mq[pd.to_numeric(mq.RAJ2000,errors='coerce').notna()]; mq['Type']=mq.Type.astype(str).str.strip()
mqs=mq[mq.Type.str.contains('[QABKN]',regex=True)]
cg=SkyCoord(gq.ra.values*u.deg,gq.dec.values*u.deg)
def m(ra,dec):
    c=SkyCoord(np.asarray(ra,float)*u.deg,np.asarray(dec,float)*u.deg); i,s,_=cg.match_to_catalog_sky(c); return s.arcsec<2.0
gq['sdss']=m(sd.ra,sd.dec); gq['mq_spec']=m(mqs.RAJ2000,mqs.DEJ2000); gq['mq_any']=m(mq.RAJ2000,mq.DEJ2000)
un=gq[~gq.sdss&~gq.mq_spec].sort_values('phot_g_mean_mag')
S=dict(N_total=len(gq),N_sdss=int(gq.sdss.sum()),N_mq_spec=int(gq.mq_spec.sum()),N_unmatched=len(un),N_unmatched_G19=int((un.phot_g_mean_mag<19).sum()),N_unmatched_G18=int((un.phot_g_mean_mag<18).sum()),
       N_unmatched_in_mq_as_candidate=int(un.mq_any.sum()),N_sdss_rows=len(sd),N_mq=len(mq),N_mq_spec=len(mqs))
print(S); print(un.head(10).to_string())
un.head(20000).round(6).astype({'source_id':str}).to_csv(sys.argv[4],index=False); json.dump(S,open(sys.argv[4].replace('.csv','_summary.json'),'w'))
