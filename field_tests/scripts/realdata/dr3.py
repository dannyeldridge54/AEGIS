import numpy as np, json
src=open('field_tests/scripts/realdata/cmb.py').read().split("c0,x=fit('lcdm'")[0]; ns={}; exec(src,ns)
best={'LCDM':('lcdm',[0.3021558922461554,0.6823894242012638,0.022381669793628794],None),
 'CPL':('cpl',[0.3127613302501483,0.6734186699390241,0.022295154842803845],[-0.8203739081733297,-0.6407533645926498]),
 'thread':('thread',[0.3107233762423971,0.6713575092814403,0.0224399159629102],0.1594237608206133),
 'LsCDM':('ls',[0.30344980867279503,0.6861398714724409,0.022217099672445943],2.642881112830479)}
c=299792.458; zg=ns['zg']
pred={}
for k,(kind,(Om,h,ob),par) in best.items():
    Or=ns['og']*(1+0.2271*ns['Neff'])/h**2; E=ns['Ecalc'](kind,Om,Or,par)
    from scipy.integrate import cumulative_trapezoid
    Dc=np.concatenate([[0],cumulative_trapezoid(1/E,zg)])*c/(100*h); rd=ns['rd_fit'](ob,Om*h*h-ns['onu'])
    v=[]
    for z,q in zip(ns['bz'],ns['bq']):
        DM=np.interp(z,zg,Dc); DH=c/(100*h)/np.interp(z,zg,E)
        v.append((DM if q=='DM_over_rs' else DH if q=='DH_over_rs' else (z*DM*DM*DH)**(1/3))/rd)
    pred[k]=np.array(v)
sig=np.sqrt(np.diag(ns['bc']))
rows=[]
for i,(z,q) in enumerate(zip(ns['bz'],ns['bq'])):
    r=dict(z=float(z),q=str(q),data=float(ns['bv'][i]),sigma_DR2=float(sig[i]))
    for k in pred: r[k]=float(pred[k][i])
    r['thread_minus_CPL_in_sigma']=float((pred['thread'][i]-pred['CPL'][i])/sig[i])
    r['thread_minus_LsCDM_in_sigma']=float((pred['thread'][i]-pred['LsCDM'][i])/sig[i])
    rows.append(r)
best_bins=[(r['z'],r['q'],round(r['thread_minus_CPL_in_sigma'],2)) for r in rows if abs(r['thread_minus_CPL_in_sigma'])>1.5]
o=dict(rows=rows,discriminating_bins_vs_CPL=best_bins)
print(json.dumps(o,indent=1)); json.dump(o,open('/home/claude/aegis/field_tests/results/dr3_forecast.json','w'),indent=1)
