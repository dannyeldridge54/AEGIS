import json, math
Hinf=5.8e12; m=0.866*Hinf; Trh=9e8; YB=8.7e-11; C=28/79; v=174.0; matm=0.05e-9
eps=YB/((3/4)*(Trh/m)*C)
Mmin=eps*16*math.pi*v*v/(3*matm)
q1=dict(m_phi=m,eps_needed=eps,M_min=Mmin,M_max=m/2,T_rh=Trh,viable=(max(Mmin,Trh)<m/2))
xi=0.45; share=xi**4; mdm=5.364*0.938272/share
q2=dict(share_at_xi045=share,m_DM_GeV=mdm,conflict=mdm>50)
q3=dict(mirror_baryon_mass=0.938272,needed_share=5.364)
o=dict(Q1=q1,Q2=q2,Q3=q3); print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/rc34.json','w'),indent=1)
