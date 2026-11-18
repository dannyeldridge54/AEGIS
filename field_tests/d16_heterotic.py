"""D1288 (locked PREREG_D1288): E8+E8 vs D16+ (both even unimodular, d=16). Shell counts + Gaussian energy."""
import numpy as np, math, sys, time
sys.path.insert(0,'field_tests')
import importlib.util; spec=importlib.util.spec_from_file_location('ef','field_tests/e6e7_flip.py')
src=open('field_tests/e6e7_flip.py').read().split('al=np.array')[0]; ns={}; exec(src,ns); cartan, norms = ns['cartan'], ns['norms']
E8=cartan(8); EE=np.zeros((16,16)); EE[:8,:8]=E8; EE[8:,8:]=E8
B=np.zeros((16,16))
for i in range(15): B[i,i]=1; B[i,i+1]=-1
B[15,14]=1; B[15,15]=1
B[0,:]=0.5          # D16 basis with e1-e2 replaced by the glue vector s=(1/2)^16: det 1, even (checked below) -> D16+
DP=B@B.T
D16b=np.zeros((16,16))
for i in range(15): D16b[i,i]=1; D16b[i,i+1]=-1
D16b[15,14]=1; D16b[15,15]=1; D16=D16b@D16b.T
out=[]
for name,G in (('E8+E8',EE),('D16+',DP),('D16',D16),('Z16',np.eye(16))):
    det=np.linalg.det(G); Gn=G/det**(1/16); t=time.time(); q=norms(Gn,6.0001); 
    vals,cnt=np.unique(np.round(q,6),return_counts=True)
    shells=dict(zip(vals.tolist(),cnt.tolist()))
    al=np.array([1.0,1.25,1.5,2.0,3.0]); th=np.exp(-np.pi*np.outer(al,q)).sum(1)-1
    print(f"{name:6s} det {det:.4f} even? {np.allclose(np.diag(G)%2,0)} N={len(q)} ({time.time()-t:.0f}s) shells {dict(list(shells.items())[:6])}")
    print(f"        theta-1 at alpha 1,1.25,1.5,2,3: " + ' '.join(f'{x:.10f}' for x in th)); out.append((name,th))
print("truncation (norm-8 shell bound, 1-ish e5 vectors * e^{-8 pi alpha}): at alpha=1 ~", f"{2e7*math.exp(-8*math.pi):.1e}")
print("E8+E8 minus D16+ :", ' '.join(f'{a-b:.2e}' for a,b in zip(out[0][1],out[1][1])))
