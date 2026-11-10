import json,sys,os,numpy as np,camb
RES='/home/claude/aegis/cmb-fit/results'; out={}
for name in sys.argv[1:]:
    m=json.load(open(f"{RES}/cmp_{name}.json"))["minimum"]
    kw=dict(H0=m["H0"],ombh2=m["ombh2"],omch2=m["omch2"],mnu=0.06,num_massive_neutrinos=1,nnu=3.044,tau=m["tau"],As=m["As"],ns=m["ns"],lmax=5000,lens_potential_accuracy=2)
    if "fde_zc" in m:
        zc=m.get("zc") or (m["ombh2"]+m["omch2"])/(2.4728e-5*(1+0.22711*3.044))-1
        kw.update(dark_energy_model="EarlyQuintessence",n=3,use_zc=True,zc=zc,fde_zc=m["fde_zc"],theta_i=m["theta_i"])
    p=camb.set_params(**kw); p.set_matter_power(redshifts=[0.0],kmax=2.0); p.WantTransfer=True; r=camb.get_results(p)
    cl=r.get_lensed_scalar_cls(CMB_unit='muK',lmax=4000)  # D_l
    s8=float(r.get_sigma8_0())
    out[name]={"H0":m["H0"],"ns":m["ns"],"sigma8":s8,"sigma8_stored":m["sigma8"],"tt":cl[:,0].tolist(),"ee":cl[:,1].tolist(),"te":cl[:,3].tolist()}
    print(name,"H0 %.2f sigma8 %.4f stored %.4f"%(m["H0"],s8,m["sigma8"]),flush=True)
json.dump(out,open(f"{os.environ['OUTF']}","w"))
