"""PREREG_PLANCK_CLASS (D1713) — the reverse thread (exact curve), uncoupled and coupled to CDM, in patched CLASS v3.3.0,
on full Planck 2018 + DESI DR2 BAO + SN (same likelihoods as D1636/D1712). LCDM is refit with the SAME CLASS build
so every Delta chi2 is like-with-like.
Usage: python coupled_class.py {build_check|lcdm|thread|coupled}[_desy5|_union3]
"""
import json, math, os, sys, time, copy
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
CLASS_PATH=os.environ.get('AEGIS_CLASS',os.path.join(HERE,'class_v330'))
CF=os.path.join(HERE,'..','d1636','cmb-fit'); sys.path.insert(0,CF)
Z2=math.pi**2/6; Z3=1.2020569031595942
A=16*Z2/(3*Z3); BETA=2*math.sqrt(2); CC=2*Z2/Z3
def scf_string(amp,bc,VL=3.0):
    phii=math.log(A/amp)/BETA
    return f'{BETA:.16g}, {CC:.16g}, {bc:.16g}, {VL:.16g}, {phii:.16g}, 0.0'
COMMON=dict(N_ur=2.0328,N_ncdm=1,m_ncdm=0.06,non_linear='halofit')
SCF=dict(Omega_Lambda=0,Omega_fld=0,Omega_scf=-0.7,attractor_ic_scf='no',scf_tuning_index=3)
def theory():
    from cobaya.theories.classy import classy
    class AegisClassy(classy):
        def set(self,pv):
            p=dict(pv); amp=p.pop('rt_ui',None); bc=p.pop('rt_bc',None)
            if amp is not None:
                p['scf_parameters']=scf_string(amp,bc or 0.0)
            return super().set(p)
        def get_can_support_params(self):
            return super().get_can_support_params()+['rt_ui','rt_bc']
    return AegisClassy
def make(name):
    import cmbfit as C
    core,sn=name,None
    nested=name.endswith('_nested')
    if nested: name_core=name[:-7]
    else: name_core=name
    core=name_core
    for suf in ('_desy5','_union3'):
        if core.endswith(suf): core,sn=core[:-len(suf)],suf
    likes=dict(C.LIKES_BASE); likes[{None:'sn.pantheonplus','_desy5':'sn.desy5','_union3':'sn.union3'}[sn]]=None
    ex=dict(COMMON)
    if core in ('thread','coupled'): ex.update(SCF)
    pr={
      'logA':{'prior':{'min':1.61,'max':3.91},'ref':{'dist':'norm','loc':3.05,'scale':0.001},'proposal':0.001,'drop':True},
      'A_s':{'value':'lambda logA: 1e-10*np.exp(logA)'},
      'n_s':{'prior':{'min':0.8,'max':1.2},'ref':{'dist':'norm','loc':0.965,'scale':0.004},'proposal':0.002},
      'H0':{'prior':{'min':50,'max':90},'ref':{'dist':'norm','loc':67.5,'scale':0.5},'proposal':0.3},
      'omega_b':{'prior':{'min':0.005,'max':0.1},'ref':{'dist':'norm','loc':0.0224,'scale':0.0001},'proposal':0.0001},
      'omega_cdm':{'prior':{'min':0.001,'max':0.99},'ref':{'dist':'norm','loc':0.12,'scale':0.001},'proposal':0.0005},
      'tau_reio':{'prior':{'min':0.01,'max':0.8},'ref':{'dist':'norm','loc':0.055,'scale':0.006},'proposal':0.003},
      'Omega_m':{'latex':r'\Omega_m'},'sigma8':{'latex':r'\sigma_8'}}
    if core in ('thread','coupled'):
        pr['rt_ui']={'prior':{'min':1e-6,'max':3.0},'ref':{'dist':'uniform','min':0.1,'max':0.25},'proposal':0.02}
    if core=='coupled':
        pr['rt_bc']={'prior':{'min':-0.3,'max':0.1},'ref':{'dist':'uniform','min':-0.12,'max':-0.02},'proposal':0.01}
    if nested:   # PREREG_PLANCK_CLASS DEVIATIONS D1: start at the CLASS LCDM best point (nested start)
        L=json.load(open(os.path.join(HERE,'results','cls_lcdm'+(sn or '')+'.json')))['minimum']
        for k in ('logA','n_s','H0','omega_b','omega_cdm','tau_reio'):
            if k in L: pr[k]['ref']={'dist':'norm','loc':L[k],'scale':abs(L[k])*1e-4+1e-6}
        if 'rt_ui' in pr: pr['rt_ui']['ref']={'dist':'uniform','min':1e-3,'max':0.05}
        if 'rt_bc' in pr: pr['rt_bc']['ref']={'dist':'uniform','min':-0.01,'max':0.0}
    th={'external':theory(),'path':CLASS_PATH,'extra_args':ex,'stop_at_error':False,'ignore_obsolete':True}  # patched v3.3.0
    info={'theory':{'aegisclassy':th},'likelihood':likes,'params':pr,'packages_path':C.PACKAGES,
          'sampler':{'minimize':{'method':'bobyqa','best_of':4}},
          'output':os.path.join(HERE,'results','chains','cls_'+name),'force':True}
    return info
def build_check():
    """Patched build must give the validated numbers (D1713 cloud validation)."""
    sys.path.insert(0,[os.path.join(CLASS_PATH,'build',d) for d in os.listdir(os.path.join(CLASS_PATH,'build')) if d.startswith('lib.')][0])
    from classy import Class
    out={}
    for tag,amp,bc in (('u',0.2,0.0),('c',1.8324583119096416,-0.0740259963681026)):
        M=Class(); M.set(dict(h=0.6738491397304909,omega_b=0.022281521225743756,omega_cdm=0.11971849246055141,N_ur=3.044,N_ncdm=0,
                              T_cmb=2.7255,scf_parameters=scf_string(amp,bc),**SCF)); M.compute()
        bg=M.get_background(); z=bg['z'][::-1]; H=bg['H [1/Mpc]'][::-1]
        out[tag]=[float(np.interp(zz,z,H)/H[0]) for zz in (0.5,1.0,2.0)]; M.struct_cleanup()
    ref={'u':[1.336374,1.801428,3.033054],'c':[1.310305,1.758225,2.958513]}
    out['max_rel_err']=max(abs(out[t][i]/ref[t][i]-1) for t in 'uc' for i in range(3)); out['pass']=out['max_rel_err']<1e-4
    os.makedirs(os.path.join(HERE,'results'),exist_ok=True)
    json.dump(out,open(os.path.join(HERE,'results','build_check.json'),'w'),indent=1); print(json.dumps(out),flush=True)
def run(name):
    from cobaya import run as crun
    t=time.time(); upd,s=crun(make(name))
    row={k:float(v) for k,v in s.products()['minimum'].data.iloc[0].items() if isinstance(v,(int,float,np.integer,np.floating))}
    json.dump({'run':name,'seconds':time.time()-t,'minimum':row},open(os.path.join(HERE,'results',f'cls_{name}.json'),'w'),indent=2)
    print('done',name,row.get('chi2'),row.get('rt_ui'),row.get('rt_bc'),flush=True)
if __name__=='__main__':
    try: os.nice(10)
    except Exception: pass
    os.makedirs(os.path.join(HERE,'results','chains'),exist_ok=True)
    if sys.argv[1]=='build_check': build_check()
    else:
        b=os.path.join(HERE,'results','build_check.json')
        if not os.path.exists(b) or not json.load(open(b))['pass']: raise SystemExit('build check not passed')
        run(sys.argv[1])
