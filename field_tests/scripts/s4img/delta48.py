import numpy as np, json
M=4; j=np.arange(M)
T=np.diag(np.exp(1j*np.pi*j**2/M)); S=np.exp(1j*np.pi/4)/np.sqrt(M)*np.exp(2j*np.pi*np.outer(j,j)/M)
P=np.zeros((M,3),complex); P[0,0]=1; P[1,1]=P[3,1]=1/np.sqrt(2); P[2,2]=1
S3=P.conj().T@S@P; T3=P.conj().T@T@P
chk=dict(unitary=bool(np.allclose(S3@S3.conj().T,np.eye(3)) and np.allclose(T3@T3.conj().T,np.eye(3))))
def norm(Mx):
    f=Mx.flatten(); k=np.argmax(np.abs(f)>1e-9); return Mx*np.exp(-1j*np.angle(f[k]))
def key(Mx): return tuple(np.round(norm(Mx),6).flatten())
G=[np.eye(3,dtype=complex)]; seen={key(G[0])}; fr=[G[0]]
while fr and len(G)<5000:
    new=[]
    for A in fr:
        for g in (S3,T3):
            B=A@g; k=key(B)
            if k not in seen: seen.add(k); G.append(B); new.append(B)
    fr=new
chk['proj_order']=len(G); chk['finite']=len(G)<5000
w,V=np.linalg.eig(S3@T3); Ue=V/np.linalg.norm(V,axis=0)
conj={}
for h in G:
    g=h@S3@np.linalg.inv(h); conj[key(g)]=g
res=[]
for g in conj.values():
    w,V=np.linalg.eig(g); wn=np.round(w/ w[0] if False else w,6)
    # non-degenerate eigenvalue
    vals=[np.round(x,5) for x in w]; idx=[i for i in range(3) if sum(np.isclose(w[i],w[k],atol=1e-6) for k in range(3))==1]
    if not idx: res.append('degenerate'); continue
    for i in idx[:1]:
        v=V[:,i]/np.linalg.norm(V[:,i]); col=np.sort(np.abs(Ue.conj().T@v)**2)[::-1]
        pat='TM1' if np.allclose(col,[2/3,1/6,1/6],atol=1e-6) else 'TM2' if np.allclose(col,[1/3]*3,atol=1e-6) else 'other:'+','.join(f'{c:.4f}' for c in col)
        res.append(pat)
from collections import Counter
o=dict(checks=chk,n_conj=len(conj),patterns=dict(Counter(res)))
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/d7_delta48.json','w'),indent=1)
