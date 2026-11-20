"""PREREG_PLANCK_COUPLED (D1712) — coupled exact-curve reverse thread on full Planck + DESI DR2 + SN, via the D1636 stack."""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
HERE=os.path.dirname(os.path.abspath(__file__)); CF=os.path.join(HERE,'..','d1636','cmb-fit')
sys.path.insert(0,CF)
import cmbfit as C
import rt_planck_fit as R
A=R.A_PL; BETA=R.BETA; OMNU=R.OMNU; CC=2*1.6449340668482264/1.2020569031595942
def g_ex(p):
    u=math.exp(-BETA*p); return ((2/3)*(1.5-2*CC*u/(1+CC*u)))**2
def dg_ex(p):
    u=math.exp(-BETA*p); f=(2/3)*(1.5-2*CC*u/(1+CC*u)); df=(2/3)*(-2*CC/(1+CC*u)**2)*(-BETA*u); return 2*f*df
def g_lo(p): return 1-A*math.exp(-BETA*p)
def dg_lo(p): return A*BETA*math.exp(-BETA*p)
def wtable(ui,bc,Ob,Oc,Or,shape='exact'):
    g,dg=(g_ex,dg_ex) if shape=='exact' else (g_lo,dg_lo)
    phii=math.log(A/ui)/BETA
    def run(VL):
        def f(N,s):
            p,q=s; a=math.exp(N); rb=3*Ob*a**-3; rc=3*Oc*a**-3*math.exp(bc*(p-phii)); rr=3*Or*a**-4
            V=VL*g(p); H2=(rb+rc+rr+V)/(3-q*q/2); eps=(rb+rc+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-(VL*dg(p)+bc*rc)/H2]
        return solve_ivp(f,(math.log(1e-3),0),[phii,0],rtol=1e-8,atol=1e-11,dense_output=True)
    def H2end(VL):
        s=run(VL); p,q=s.y[:,-1]; return (3*Ob+3*Oc*math.exp(bc*(p-phii))+3*Or+VL*g(p))/(3-q*q/2)-1
    lo,hi=None,None; grid=[0.05*2**k for k in range(16)]; vals=[]
    for v in grid:
        try: vals.append(H2end(v))
        except Exception: vals.append(np.nan)
    from scipy.optimize import brentq
    VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if np.isfinite(fa) and np.isfinite(fb) and fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-12); break
    if VL is None: return None
    s=run(VL); Ns=np.linspace(math.log(1e-3),0,500); P,Q=s.sol(Ns); a=np.exp(Ns)
    rb=3*Ob*a**-3; rcx=3*Oc*a**-3*np.exp(bc*(P-phii)); rr=3*Or*a**-4; V=VL*np.array([g(x) for x in P])
    H2=(rb+rcx+rr+V)/(3-Q*Q/2); rphi=H2*Q*Q/2+V
    rde=rphi+3*Oc*a**-3*(np.exp(bc*(P-phii))-1)
    if np.any(rde<=0): return None
    w=-1-np.gradient(np.log(rde),Ns)/3
    return np.concatenate([[1e-8,9.99e-4],a]),np.concatenate([[w[0],w[0]],w])
def theory(shape):
    from cobaya.theories.camb import CAMB
    from camb.dark_energy import DarkEnergyPPF
    class CTCamb(CAMB):
        def set(self,pv,state):
            p=dict(pv); ui=p.pop('rt_ui',None); bc=p.pop('rt_bc',0.0)
            cp=super().set(p,state)
            if cp is None or ui is None: return cp
            h=cp.H0/100; Ob=cp.ombh2/h**2; Oc=(cp.omch2+OMNU)/h**2; Or=2.4728e-5*(1+0.2271*3.044)/h**2
            tab=wtable(ui,bc,Ob,Oc,Or,shape)
            if tab is None: return None
            de=DarkEnergyPPF(); de.set_w_a_table(tab[0],tab[1]); cp.DarkEnergy=de; return cp
        def get_helper_theories(self):
            helpers=super().get_helper_theories(); tr=self._camb_transfers; base=tr.get_can_support_params
            tr.get_can_support_params=lambda: set(base())|{'rt_ui','rt_bc'}; return helpers
    return CTCamb
def make(name):
    # name: cx_{coupled|uncoupled}[_desy5|_union3] ; gate uses leading order
    sn=None; core=name
    for suf in ('_desy5','_union3'):
        if core.endswith(suf): core,sn=core[:-len(suf)],suf
    info,ref=R.make('rtP'+(sn or ''))
    info['output']=os.path.join(HERE,'results','chains','cmp_'+name+'_r2'); info['force']=True
    shape='lo' if core=='gate' else 'exact'
    ex=info['theory']['rtcamb']['extra_args']; info['theory']={'ctcamb':{'external':theory(shape),'extra_args':ex,'stop_at_error':False}}
    pr=info['params']; pr['rt_ui']={'prior':{'min':1e-6,'max':0.9},'ref':{'dist':'uniform','min':0.1,'max':0.25},'proposal':0.02}
    if core=='cx_coupled': pr['rt_bc']={'prior':{'min':-0.3,'max':0.1},'ref':{'dist':'uniform','min':-0.12,'max':-0.02},'proposal':0.01}
    else: pr['rt_bc']=0.0
    return info,ref,sn
def gate():
    import copy
    from cobaya.model import get_model
    info,ref,sn=make('gate_desy5'); stored=json.load(open(os.path.join(CF,'results','cmp_rtP_desy5.json')))['minimum']
    i=copy.deepcopy(info); i.pop('sampler',None); i.pop('output',None); m=get_model(i); sp=m.parameterization.sampled_params()
    pt={k:stored[k] for k in sp if k in stored}; pt['rt_ui']=stored['rt_ui']
    c=-2*sum(m.loglikes(pt,as_dict=True)[0].values())
    out=dict(stored=stored['chi2'],recomputed=float(c),diff=float(c-stored['chi2']),pass_=bool(abs(c-stored['chi2'])<=1.0))
    json.dump(out,open(os.path.join(HERE,'results','gate.json'),'w'),indent=1); print(json.dumps(out),flush=True)
    return out['pass_']
def run(name):
    from cobaya import run as crun
    t=time.time(); info,ref,sn=make(name); upd,s=crun(info)
    row={k:float(v) for k,v in s.products()['minimum'].data.iloc[0].items() if isinstance(v,(int,float,np.integer,np.floating))}
    json.dump({'run':name,'seconds':time.time()-t,'minimum':row},open(os.path.join(HERE,'results',f'cmp_{name}.json'),'w'),indent=2)
    print('done',name,row.get('chi2'),row.get('rt_ui'),row.get('rt_bc'),flush=True)
if __name__=='__main__':
    C.lower_priority(); os.makedirs(os.path.join(HERE,'results','chains'),exist_ok=True)
    if sys.argv[1]=='gate': gate()
    else:
        g=json.load(open(os.path.join(HERE,'results','gate.json'))) if os.path.exists(os.path.join(HERE,'results','gate.json')) else None
        if not g or not g['pass_']: raise SystemExit('gate not passed')
        run(sys.argv[1])
