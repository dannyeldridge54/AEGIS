import numpy as np, json
exec(open('field_tests/scripts/s4img/run.py').read().split("res=[]")[0])
cnt={}; pat={}
for h in G:
    g=h@S@np.linalg.inv(h); k=key(g); cnt[k]=cnt.get(k,0)+1
    if k not in pat:
        w,V=np.linalg.eig(g); w=np.round(w.real,6); vals,c=np.unique(w,return_counts=True); u=vals[c==1][0]
        v=V[:,np.where(np.isclose(w,u))[0][0]]; v=v/np.linalg.norm(v); col=np.sort(np.abs(Ue.conj().T@v)**2)[::-1]
        pat[k]='TM1' if np.allclose(col,[2/3,1/6,1/6],atol=1e-6) else 'TM2' if np.allclose(col,[1/3]*3,atol=1e-6) else 'other'
w_tm1=sum(cnt[k] for k in cnt if pat[k]=='TM1')/24
o=dict(multiplicities=sorted(cnt.values()),P_TM1_given_i=w_tm1,P_TM1_total=0.6895*w_tm1)
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/s4_image_weights.json','w'),indent=1)
