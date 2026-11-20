import numpy as np
rng=np.random.default_rng(5); N=2_000_000; c=np.sqrt(3)*0.0145; eps=lambda m: c/(m+1/16)
L=lambda n: np.exp(rng.uniform(np.log(1/3),np.log(3),n))
k=lambda: np.sqrt(L(N)*np.sqrt(L(N)))
lr0=np.log(0.1312); post={}
for m in range(1,33):
    lr=np.log(k()*eps(m))-np.log(k()*eps(1))
    post[m]=np.mean(np.exp(-0.5*((lr-lr0)/0.05)**2))
Z=sum(post.values()); post={m:v/Z for m,v in post.items()}
order=sorted(post,key=post.get,reverse=True); cum=0; s68=[]; s95=[]
for m in order:
    if cum<0.68: s68.append(m)
    if cum<0.95: s95.append(m)
    cum+=post[m]
print("P(m_u):", " ".join(f"{m}:{post[m]:.3f}" for m in range(1,21)))
print(f"most probable rung {order[0]} (P={post[order[0]]:.3f}); 68% set {sorted(s68)}; 95% set {sorted(s95)}")
print("VERDICT:", "SHARP" if post[8]>=0.5 else ("BROAD" if len(s68)>=4 else "INTERMEDIATE"))
