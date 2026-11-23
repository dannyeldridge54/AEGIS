"""D2187 locked tests T1 (stop closed forms vs Zurvan numerical CW) and T3 (Weave benchmark Delta_EW)."""
import math, json
from zurvan import sectors, sigmas, delta_ew
PI2 = math.pi**2
def point(mQ3, mtR, At, mu, tanb, yt, mHu2, mHd2):
    v = 174.1; b = math.atan(tanb)
    p = dict(mQ3=mQ3, mtR=mtR, At=At, mu=mu, tanb=tanb, yt=yt, yb=0.0, ytau=0.0, Ab=0, Atau=0,
             mbR=mQ3, mL3=mQ3, meR3=mQ3, g=0.65, gp=0.36, vu=v*math.sin(b), vd=v*math.cos(b), mHu2=mHu2, mHd2=mHd2)
    s = sectors(dict(p, Q=1.0), p['vu'], p['vd'])
    p['Q'] = math.sqrt(math.sqrt(s['stop1'][0][0]*s['stop2'][0][0]))
    p['mZ'] = math.sqrt((p['g']**2+p['gp']**2)/2*v*v)
    return p
P = {'P1_natural': point(1500,1300,-2500,250,10,0.85,-300.0**2,1.0e6),
     'P2_heavy_mixing': point(3000,2000,-5000,300,20,0.85,-350.0**2,4.0e6),
     'P3_weave_minisplit': point(159000,159000,0,87600,1.9,0.60,0.058*159000**2,1.0*159000**2)}
def closed(p):
    g,gp=p['g'],p['gp']; sw2=gp*gp/(g*g+gp*gp); gZ2=(g*g+gp*gp)/8; Q2=p['Q']**2
    s = sectors(p,p['vu'],p['vd']); m1=s['stop1'][0][0]; m2=s['stop2'][0][0]
    F=lambda m: m*(math.log(m/Q2)-1); yt=p['yt']; at=p['At']*yt
    c2b=(1-p['tanb']**2)/(1+p['tanb']**2); mZ2=p['mZ']**2
    Dt=2*(0.5-4/3*sw2)*((p['mQ3']**2-p['mtR']**2)/2+mZ2*c2b*(0.25-2/3*sw2))
    out={}
    for name,m,sg in (('stop1',m1,-1),('stop2',m2,+1)):   # upper sign (minus) for t1
        su=3/(16*PI2)*F(m)*(yt*yt-gZ2+sg*(at*at-2*gZ2*Dt)/(m2-m1))
        sd=3/(16*PI2)*F(m)*(gZ2+sg*(yt*yt*p['mu']**2+2*gZ2*Dt)/(m2-m1))
        out[name]=(su,sd)
    return out
R={}
for k,p in P.items():
    n4=sigmas(p,1e-4); n3=sigmas(p,1e-3); c=closed(p); r={}
    for st in ('stop1','stop2'):
        for i,lab in ((0,'Su'),(1,'Sd')):
            num=n4[st][i]; step=abs(n3[st][i]-num)/max(abs(num),1e-30); cl=c[st][i]
            r[f'{lab}({st})']=dict(zurvan=num,paper_closed_form=cl,rel_diff=abs(num-cl)/max(abs(cl),1e-30),step_stability=step)
    tot_u_num=n4['stop1'][0]+n4['stop2'][0]; tot_u_cl=c['stop1'][0]+c['stop2'][0]
    r['Su(stop1+stop2)']=dict(zurvan=tot_u_num,paper_closed_form=tot_u_cl,rel_diff=abs(tot_u_num-tot_u_cl)/abs(tot_u_cl))
    de=delta_ew(p)
    r['Delta_EW']=de['Delta_EW']; r['largest']=de['largest']; r['top3']=[(a,b,c_) for a,b,c_ in de['contributions'][:3]]
    r['Q']=p['Q']; R[k]=r
json.dump(R,open('d2187_tests.json','w'),indent=1,default=float)
for k,r in R.items():
    print('==',k,'Q=%.0f'%r['Q'],'Delta_EW=%.4g'%r['Delta_EW'],r['largest'])
    for kk,vv in r.items():
        if isinstance(vv,dict): print('  %-18s zurvan %+.4e  paper %+.4e  diff %.2e  %s'%(kk,vv['zurvan'],vv['paper_closed_form'],vv['rel_diff'],('step %.1e'%vv['step_stability']) if 'step_stability' in vv else ''))
