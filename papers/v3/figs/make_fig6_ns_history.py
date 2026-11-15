"""Fig. 6: n_s by data release vs the frozen SERAPIS band (D710). AI-assisted."""
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d=[("WMAP9",2012.9,0.972,0.013),("Planck13",2013.2,0.9603,0.0073),("Planck15",2015.1,0.9655,0.0062),("Planck18",2018.5,0.9649,0.0042),("P-ACT-LB",2024.9,0.974,0.003),("SPA",2025.9,0.9682,0.0032),("SPA+DESI",2026.3,0.9728,0.0029)]
fig,ax=plt.subplots(figsize=(5.2,3.2),dpi=200)
ax.axhspan(0.970,0.975,color='#c9a227',alpha=0.30,lw=0,label='SERAPIS band (frozen)')
for n,x,c,s in d:
    ax.errorbar(x,c,yerr=s,fmt='o',ms=4,color='#1f3b5c',capsize=2,lw=1)
    below=n in ('SPA','Planck13')
    ax.annotate(n,(x,c-s if below else c+s),xytext=((-14 if n=='P-ACT-LB' else 10 if n=='SPA+DESI' else 0),(-9 if below else 4)),textcoords='offset points',ha='center',fontsize=6.5)
ax.set_xlabel('release year'); ax.set_ylabel(r'$n_s$'); ax.set_ylim(0.945,0.99); ax.set_xlim(2011.5,2027)
ax.legend(fontsize=7,loc='lower right',frameon=False); fig.tight_layout()
fig.savefig('fig6_ns_history.pdf'); fig.savefig('fig6_ns_history.png')
