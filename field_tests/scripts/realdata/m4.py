import numpy as np, json
src=open('field_tests/scripts/realdata/cmb.py').read().split("c0,x=fit('lcdm'")[0]
out={}
for lab,idx in (('A_theta',[0]),('B_omegas',[1,2])):
    ns={}; exec(src,ns)
    C=ns['Cc'][np.ix_(idx,idx)]; Ci=np.linalg.inv(C); mu=ns['mu_c'][idx]
    oldchi=ns['chi2_all']
    def chi2_sub(kind,Om,h,ob,par,ns=ns,Ci=Ci,mu=mu,idx=idx):
        # recompute: full minus full-CMB term plus sub-CMB term
        Or=ns['og']*(1+0.2271*ns['Neff'])/h**2
        E=ns['Ecalc'](kind,Om,Or,par)
        if E is None or not np.all(np.isfinite(E)): return 1e9
        rde25=E[-1]**2-Om*(3.5)**3-Or*(3.5)**4
        Eh=ns['make_Ehigh'](Om,Or,rde25,kind,par)
        th,obc=ns['thetastar'](h,ob,Om,Or,E,Eh); th*=ns['cal']
        v=np.array([th,ob,obc]); d=v[idx]-mu; ccmb=float(d@Ci@d)
        full=oldchi(kind,Om,h,ob,par)
        dd=v-ns['mu_c']; cfull=float(dd@ns['Cci']@dd)
        return full-cfull+ccmb
    ns['chi2_all']=chi2_sub
    fit=ns['fit']; B3=ns['B3']
    c0,x0=fit('lcdm',[[0.31,0.68,0.0223]],B3)
    c2,x2=fit('thread',[[0.31,0.67,0.0224,0.16],[0.31,0.68,0.0224,0.3]],B3+[(0.005,0.9)])
    c3,x3=fit('ls',[[0.304,0.687,0.0222,2.6],[0.304,0.687,0.0222,5]],B3+[(0.3,10)])
    out[lab]=dict(LCDM=c0,thread_d=c2-c0,ls_d=c3-c0,x_thread=x2,x_ls=x3)
    print(json.dumps(out),flush=True)
for m in ('thread_d','ls_d'):
    a,b=out['A_theta'][m],out['B_omegas'][m]
    out[m.split('_')[0]+'_driver']='theta*' if a<b-1 else ('densities' if b<a-1 else 'mixed')
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/m4_cmbsplit.json','w'),indent=1)
