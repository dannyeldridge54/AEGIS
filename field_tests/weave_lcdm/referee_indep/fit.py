import sys, json, math, time, numpy as np, camb
sys.path.insert(0,'/tmp/claude-0/referee/indep')
from thread import wtable
from scipy.optimize import minimize
C=299792.458; D='/tmp/claude-0/cobaya_pkgs/data/'
mu_cmb=np.array([1.7502,301.471,0.02236,0.9649]); sg=np.array([0.0046,0.0895,0.00015,0.0043])
rho=np.array([[1,.46,-.66,-.74],[.46,1,-.33,-.35],[-.66,-.33,1,.46],[-.74,-.35,.46,1]]); ICMB=np.linalg.inv(rho*np.outer(sg,sg))
bm=[l.split() for l in open(D+'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt') if not l.startswith('#')]
bz=np.array([float(r[0]) for r in bm]); bv=np.array([float(r[1]) for r in bm]); bq=[r[2] for r in bm]
IB=np.linalg.inv(np.loadtxt(D+'bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'))
import csv
rows=list(csv.DictReader(open(D+'sn_data/DES-Dovekie/DES-Dovekie_HD.csv')))
zhd=np.array([float(r['zHD']) for r in rows]); zhel=np.array([float(r['zHEL']) for r in rows]); mu=np.array([float(r['MU']) for r in rows])
d=np.load(D+'sn_data/DES-Dovekie/covtot_inv_000.npz'); n=int(d[d.files[0]][0]); IS=np.zeros((n,n)); IS[np.triu_indices(n)]=d[d.files[1]]; il=np.tril_indices(n,-1); IS[il]=IS.T[il]
assert n==len(mu)
Es=IS.sum(); one=IS.sum(axis=1)
zg=np.unique(np.concatenate([np.geomspace(zhd.min()*0.99,zhd.max()*1.01,300)]))
def hs(wb,wm):
    g1=0.0783*wb**-0.238/(1+39.5*wb**0.763); g2=0.560/(1+21.1*wb**1.81); return 1048*(1+0.00124*wb**-0.738)*(1+g1*wm**g2)
TAB={}
def model(p,kind,ui=None):
    wb,wc,H0=p[:3]; h=H0/100
    if not(0.018<wb<0.027 and 0.09<wc<0.15 and 58<H0<78): return None
    if kind=='L': ns=p[3]; mnu=0.06; nm=1; hier='degenerate'
    else: ns=0.9706; mnu=0.0587; nm=3; hier='normal'
    P=camb.CAMBparams()
    try: P.set_cosmology(H0=H0,ombh2=wb,omch2=wc,mnu=mnu,num_massive_neutrinos=nm,neutrino_hierarchy=hier,nnu=3.044,TCMB=2.7255,omk=0)
    except Exception: return None
    wm=wb+wc+mnu/93.14
    if kind=='W':
        Om=wm/h**2; key=(ui,round(Om,3))
        if key not in TAB:
            try: a,w,_=wtable(ui,round(Om,3),2.4728e-5*(1+0.2271*3.044)/h**2); TAB[key]=(np.concatenate([[1e-8],a]),np.concatenate([[-1.0],w]))
            except Exception: TAB[key]=None
        if TAB[key] is None: return None
        P.DarkEnergy=camb.dark_energy.DarkEnergyPPF(); P.DarkEnergy.set_w_a_table(*TAB[key])
    try: r=camb.get_background(P)
    except Exception: return None
    rd=r.get_derived_params()['rdrag']; zs=hs(wb,wm); DMs=r.comoving_radial_distance(zs); rs=r.sound_horizon(zs)
    x=np.array([math.sqrt(wm)*100*DMs/C, math.pi*DMs/rs, wb, ns])-mu_cmb; c_cmb=float(x@ICMB@x)
    th=[]
    for z,q in zip(bz,bq):
        DM=r.comoving_radial_distance(z); DH=C/r.hubble_parameter(z)
        th.append({'DM_over_rs':DM/rd,'DH_over_rs':DH/rd,'DV_over_rs':(z*DM**2*DH)**(1/3)/rd}[q])
    y=np.array(th)-bv; c_bao=float(y@IB@y)
    DMg=r.comoving_radial_distance(zg); DM=np.interp(zhd,zg,DMg); dl=(1+zhel)*DM
    t=mu-5*np.log10(dl)-25; Av=t@IS@t; Bv=one@t; c_sn=float(Av-Bv**2/Es)
    return c_cmb+c_bao+c_sn,(c_cmb,c_bao,c_sn,rd,H0)
def chi(p,kind,ui=None):
    m=model(p,kind,ui); return 1e9 if m is None else m[0]
if __name__=='__main__':
    kind=sys.argv[1]; nodes=[float(v) for v in sys.argv[2:]] or [None]; out={}
    for ui in nodes:
        t=time.time(); best=None
        starts=[[0.02236,0.119,67.5,0.965],[0.0225,0.118,66.0,0.97]] if kind=='L' else [[0.02236,0.119,67.5],[0.0225,0.118,66.0]]
        for s in starts:
            r=minimize(chi,s,args=(kind,ui),method='Nelder-Mead',options={'maxiter':400,'xatol':1e-5,'fatol':1e-3})
            if best is None or r.fun<best.fun: best=r
        m=model(best.x,kind,ui); out[str(ui)]=dict(chi2=best.fun,x=list(best.x),parts=m[1],sec=time.time()-t)
        print(kind,ui,round(best.fun,3),[round(v,3) for v in m[1]],round(time.time()-t,1),flush=True)
    json.dump(out,open(f'/tmp/claude-0/referee/indep/res_{kind}_{"_".join(sys.argv[2:]) or "x"}.json','w'),indent=1)
