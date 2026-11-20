"""PREREG_B1_SCALE (D1744): slip ladder at 1e9/1e12/1e16 GeV (arXiv:2510.01312 Table 1). Committed copy of the inline run."""
import numpy as np
rng=np.random.default_rng(9); N=200000; e1=np.sqrt(3)*0.0145/(1+1/16)
T={'1e9':dict(u=(3.95e-6,.68e-6),d=(0.87e-5,.06e-5),s=(1.75e-4,.115e-4),c=(1.97e-3,.06e-3),b=(0.845e-2,.0095e-2),t=(0.5844,.00485)),
   '1e12':dict(u=(3.41e-6,.585e-6),d=(0.76e-5,.05e-5),s=(1.52e-4,.10e-4),c=(1.70e-3,.05e-3),b=(0.720e-2,.008e-2),t=(0.5144,.0049)),
   '1e16':dict(u=(2.89e-6,.50e-6),d=(0.65e-5,.045e-5),s=(1.31e-4,.085e-4),c=(1.44e-3,.045e-3),b=(0.607e-2,.007e-2),t=(0.4462,.00485))}
ok=True
for sc,v in T.items():
    d={k:np.abs(rng.normal(a,s,N)) for k,(a,s) in v.items()}
    ea_d,eb_d=v['s'][0]/v['b'][0],np.sqrt(v['d'][0]/v['b'][0])
    on1=all(e1/3<=x<=3*e1 for x in (ea_d,eb_d))
    gd=np.sqrt((d['s']/d['b'])*np.sqrt(d['d']/d['b'])); gu=np.sqrt((d['c']/d['t'])*np.sqrt(d['u']/d['t']))
    ms=(1+1/16)*gd/gu-1/16; m=np.median(ms); ok&= on1 and 5<=m<=14
    print(f"mu={sc} GeV: down e_a={ea_d:.4f} e_b={eb_d:.4f} on rung1={on1}; g_d={np.median(gd):.4f} g_u={np.median(gu):.5f}; m_u*={m:.2f}±{ms.std():.2f}")
print('VERDICT', 'STABLE' if ok else 'SHIFTED')
