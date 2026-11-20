import numpy as np, json, itertools
r2=np.sqrt(2); S=0.5*np.array([[0,r2,r2],[r2,-1,1],[r2,1,-1]],complex); T=np.diag([1,1j,-1j])
I=np.eye(3)
chk=dict(S2=np.allclose(S@S,I),T4=np.allclose(np.linalg.matrix_power(T,4),I),ST3=np.allclose(np.linalg.matrix_power(S@T,3),I))
G=[I]; frontier=[I]
def key(M): return tuple(np.round(M,6).flatten())
seen={key(I)}
while frontier:
    new=[]
    for M in frontier:
        for g in (S,T):
            P=M@g; k=key(P)
            if k not in seen: seen.add(k); G.append(P); new.append(P)
    frontier=new
chk['order']=len(G)
w,V=np.linalg.eig(S@T); Ue=V/np.linalg.norm(V,axis=0)
conj={}
for h in G:
    g=h@S@np.linalg.inv(h); conj[key(g)]=g
res=[]
for g in conj.values():
    w,V=np.linalg.eig(g); w=np.round(w.real,6)
    vals,cnt=np.unique(w,return_counts=True); u=vals[cnt==1][0]; v=V[:,np.where(np.isclose(w,u))[0][0]]; v=v/np.linalg.norm(v)
    col=np.sort(np.abs(Ue.conj().T@v)**2)[::-1]
    pat='TM1' if np.allclose(col,[2/3,1/6,1/6],atol=1e-6) else 'TM2' if np.allclose(col,[1/3,1/3,1/3],atol=1e-6) else 'other'
    res.append(dict(col=[float(x) for x in col],pattern=pat))
o=dict(checks={k:(bool(v) if not isinstance(v,int) else v) for k,v in chk.items()},n_conjugates=len(res),
       counts={p:sum(r['pattern']==p for r in res) for p in ('TM1','TM2','other')},detail=res)
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/s4_images.json','w'),indent=1)
