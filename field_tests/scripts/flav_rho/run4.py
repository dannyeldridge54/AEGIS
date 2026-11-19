import numpy as np, json, os
s2=np.sqrt(2);s3=np.sqrt(3);s6=np.sqrt(6)
UT=np.array([[2/s6,1/s3,0],[-1/s6,1/s3,-1/s2],[-1/s6,1/s3,1/s2]])
s13t=np.sqrt(0.02195)
th=np.arcsin(s13t*np.sqrt(3/2))   # |U_e3| = sqrt(2/3) sin(th)
rows=[]
for phi in np.linspace(0,2*np.pi,720,endpoint=False):
    R=np.array([[np.cos(th),0,np.sin(th)*np.exp(-1j*phi)],[0,1,0],[-np.sin(th)*np.exp(1j*phi),0,np.cos(th)]])
    U=UT@R
    s13sq=abs(U[0,2])**2; c13sq=1-s13sq
    s23sq=abs(U[1,2])**2/c13sq; s12sq=abs(U[0,1])**2/c13sq
    J=np.imag(U[0,0]*U[1,1]*np.conj(U[0,1])*np.conj(U[1,0]))
    s12,c12=np.sqrt(s12sq),np.sqrt(1-s12sq); s23,c23=np.sqrt(s23sq),np.sqrt(1-s23sq); s13,c13=np.sqrt(s13sq),np.sqrt(c13sq)
    # |U_mu1|^2 = s12^2 c23^2 + c12^2 s23^2 s13^2 + 2 s12 c12 s23 c23 s13 cos(d)
    cd=(abs(U[1,0])**2 - s12sq*c23**2 - c12**2*s23sq*s13sq)/(2*s12*c12*s23*c23*s13)
    cd=max(-1,min(1,cd)); d=np.arccos(cd)
    if J<0: d=2*np.pi-d
    rows.append((float(phi),float(s23sq),float(s12sq),float(s13sq),float(np.degrees(d)),float(J)))
s23=[r[1] for r in rows]
out=dict(theta_deg=float(np.degrees(th)),s23_range=[min(s23),max(s23)],s12=rows[0][2],s13=rows[0][3])
for tgt in (0.561,0.470):
    sol=[r for i,r in enumerate(rows) if (rows[i-1][1]-tgt)*(r[1]-tgt)<=0]
    out[f'delta_at_s23_{tgt}']=[round(r[4],1) for r in sol]
out['consistent']=any(min(s23)<=t<=max(s23) for t in (0.561,0.470))
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/FLAV_RHO',exist_ok=True)
json.dump(dict(out,rows=rows[::20]),open('field_tests/results/FLAV_RHO/run4.json','w'),indent=1)
