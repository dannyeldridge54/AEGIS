"""D571 H3: amateur-reachable TESS planet candidates and their transits 2026-11-15..12-15 UTC (PREREG_D571)."""
import sys, json, numpy as np, pandas as pd
from astropy.time import Time
t=pd.read_csv(sys.argv[1],comment='#',low_memory=False)
n0=len(t)
s=t[t.tfopwg_disp.isin(['PC','APC'])&(t.st_tmag<=12.0)&(t.pl_trandep>=3000)&t.pl_orbper.notna()&t.pl_tranmid.notna()].copy()
j0=Time('2026-11-15T00:00:00',scale='utc').jd; j1=Time('2026-12-15T00:00:00',scale='utc').jd
sT0=s[['pl_tranmiderr1','pl_tranmiderr2']].abs().max(axis=1).fillna(0); sP=s[['pl_orbpererr1','pl_orbpererr2']].abs().max(axis=1).fillna(0)
rows=[]
for (i,r),e0,eP in zip(s.iterrows(),sT0,sP):
    P=r.pl_orbper; T0=r.pl_tranmid
    k0=int(np.ceil((j0-T0)/P)); k1=int(np.floor((j1-T0)/P))
    for k in range(k0,k1+1):
        tm=T0+k*P; sig_h=np.sqrt(e0**2+(k*eP)**2)*24
        rows.append(dict(toi=r.toidisplay,tic=int(r.tid),ra=round(r.ra,5),dec=round(r.dec,5),tmag=round(r.st_tmag,2),depth_ppt=round(r.pl_trandep/1000,2),
            dur_h=round(r.pl_trandurh,2) if pd.notna(r.pl_trandurh) else None,P=round(P,5),rp=round(r.pl_rade,1) if pd.notna(r.pl_rade) else None,disp=r.tfopwg_disp,
            mid_jd=round(tm,5),mid_utc=Time(tm,format='jd').utc.iso[:16],sig_h=round(sig_h,2),stale=bool(sig_h>1.0),score=round(r.pl_trandep/1000/(1+sig_h),3)))
o=pd.DataFrame(rows)
summ=dict(n_toi=n0,n_selected=len(s),n_transits=len(o),n_nonstale=int((~o.stale).sum()),n_targets_nonstale=int(o[~o.stale].toi.nunique()),n_stale_targets=int(o[o.stale].toi.nunique()))
good=o[~o.stale].sort_values('score',ascending=False)
json.dump(dict(summary=summ,transits=good.to_dict('records'),stale_targets=sorted(o[o.stale].toi.unique().tolist())),open(sys.argv[2],'w'))
print(summ); print(good.drop_duplicates('toi').head(15).to_string())
