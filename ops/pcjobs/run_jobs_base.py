"""AEGIS PC jobs J1–J3 (locked: PREREG_D500_TWISTM_CASE1 + DEVIATIONS, PREREG_PCJOBS_J2_J3). Parallel; results in results/."""
import os, sys, math, io, contextlib, time, multiprocessing as mp
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0,os.path.join(HERE,'theory','deep'))
os.makedirs('results',exist_ok=True)
def load_twistm():
    src=open('theory/deep/twistm_case1_d500.py').read().replace("for ms in (1e-9,1e4): run(ms)","")
    g={'__name__':'twistm'}; exec(compile(src,'twistm_case1_d500.py','exec'),g); return g
def job_twistm(args):
    tag,ms,a=args; g=load_twistm(); MP=g['MP']
    Vol=(2*a)**1.5; g['Ms']=0.5**0.25*math.sqrt(math.pi/Vol)*MP
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): g['run'](ms)
    return f"[{tag}] a={a} "+buf.getvalue().strip()
def job_fi(args):
    tag,ms,r=args; import capture_ext_d460 as C
    refl,xmin,ret,xf,rem=C.run(ms,r,32.0)
    Tr=C.T0G*math.exp(-(ret-C.N0)) if ret else None; ok=ret is not None and abs(29.6-xf)<1e-2
    return f"[{tag}] r={r:.0e} m_s={ms:.0e}: hits {len(refl)}, return T={Tr if Tr is None else f'{Tr:.2e}'}, offset {29.6-xf:.1e}, remnant rho/s={rem:.2e} -> {'CAPTURES' if ok else 'FAILS'}"
if __name__=='__main__':
    ncpu=max(1,(os.cpu_count() or 4)-2); print(f"cores used: {ncpu}",flush=True)
    J1=[('J1',ms,7599) for ms in (1e-9,1e4)]
    J2=[('J2',ms,a) for a in (3846,7599,15000) for ms in (1e-9,1e-6,1e-3,1.0,1e2,1e4)]
    J3=[('J3',ms,r) for r in (1e-5,3e-5,1e-4,3e-4,1e-3,1e-2,0.1) for ms in (1e-9,1e-6,1e-3,1.0,1e2,1e4,1e5)]
    t0=time.time()
    with mp.Pool(ncpu) as P:
        for name,fn,jobs in (('J1_D500',job_twistm,J1),('J2_D502',job_twistm,[j for j in J2 if not (j[2]==7599 and j[1] in (1e-9,1e4))]),('J3_D503',job_fi,J3)):
            with open(f'results/{name}.txt','w') as fo:
                for line in P.imap_unordered(fn,jobs):
                    print(line,flush=True); fo.write(line+'\n'); fo.flush()
            print(f"== {name} done at {time.time()-t0:.0f} s",flush=True)
    print("ALL JOBS DONE",flush=True)
