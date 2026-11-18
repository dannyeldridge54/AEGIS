# AEGIS-FP MIYRO6WR4DN7EOK5 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Figure 5: the exact allowed strip (D678/D679) against current n_s bands. AI-assisted."""
import re, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R='field_tests/results/janus_strip_d678.txt'; R2='field_tests/results/rho_strip_d680.txt'; O='papers/v3/figs/'
pts={}
for l in open(R):
    m=re.match(r"N\*=(\S+) eps=(\S+): y\*=\S+ n_s=(\S+) r=(\S+)",l)
    if m: pts.setdefault(float(m.group(1)),[]).append((float(m.group(3)),float(m.group(4)),float(m.group(2))))
rp={}
for l in open(R2):
    m=re.match(r"N\*=(\S+) eps=(\S+): y\*=\S+ n_s=(\S+) r=(\S+)",l)
    if m: rp.setdefault(float(m.group(1)),[]).append((float(m.group(3)),float(m.group(4))))
fig,ax=plt.subplots(figsize=(6,3.8))
for mu,s,lab,c in ((0.9682,0.0032,'CMB (SPA+BK)','tab:blue'),(0.9728,0.0029,'CMB+DESI','tab:orange')):
    for k,a in ((1,0.18),(2,0.08)): ax.axvspan(mu-k*s,mu+k*s,color=c,alpha=a,lw=0)
    ax.plot([],[],c=c,lw=6,alpha=0.3,label=f'{lab}: 1σ, 2σ')
A=np.array(pts[46.08]); B=np.array(pts[49.21])
poly=np.vstack([A[:,:2],B[::-1,:2]])
ax.fill(poly[:,0],poly[:,1]*1e4,color='tab:red',alpha=0.35,lw=0,label='SERAPIS (τ = i), any ε, N* = 46–49')
ax.plot(A[:,0],A[:,1]*1e4,'o-',c='tab:red',ms=3,lw=1); ax.plot(B[:,0],B[:,1]*1e4,'s-',c='darkred',ms=3,lw=1)
ax.plot([A[-1,0],B[-1,0]],[A[-1,1]*1e4,B[-1,1]*1e4],'k--',lw=1,label='string bound Im τ = 25')
ax.plot([A[0,0],B[0,0]],[A[0,1]*1e4,B[0,1]*1e4],'k:',lw=1,label='no tilt (ε = 0)')
for N,st in ((46.09,'--'),(49.49,'--')):
    P=np.array(rp[N]); ax.plot(P[:,0],P[:,1]*1e4,st,c='tab:green',lw=1.2)
ax.plot([],[],'--',c='tab:green',label='SERAPIS-ρ edges')
ax.set_xlabel('n_s'); ax.set_ylabel('r × 10⁴'); ax.set_xlim(0.955,0.988); ax.set_ylim(2.5,9)
ax.legend(fontsize=7,loc='upper left'); ax.set_title('The allowed SERAPIS strip, both vacua (exact spectra)')
fig.tight_layout(); fig.savefig(O+'fig5_strip.pdf'); fig.savefig(O+'fig5_strip.png',dpi=150)
print('done')
