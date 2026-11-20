"""PREREG_NEGSPACE_DERIVE (D1716): effective dark energy of the coupled thread with CDM fixed at the CMB."""
import numpy as np, json
def run(f):
    d=np.loadtxt(f); z=d[:,0]; o=np.argsort(z); z=z[o]; d=d[o]
    a=1/(1+z); rc=d[:,10]; rs=d[:,13]; zs=1090.0
    rcs=np.interp(zs,z,rc); acs=1/(1+zs)
    de=rs+(rc-rcs*(acs/a)**3)
    m=z<=10; zz=z[m]; dd=de[m]/np.interp(0,z,de)
    sc=np.where(np.diff(np.sign(dd))!=0)[0]
    zdag=[float(np.interp(0,[dd[i],dd[i+1]] if dd[i]<dd[i+1] else [dd[i+1],dd[i]],[zz[i],zz[i+1]] if dd[i]<dd[i+1] else [zz[i+1],zz[i]])) for i in sc]
    w=lambda x: float(np.interp(x,zz,dd))
    return dict(n_switch=len(sc),z_dagger=zdag,r3=w(3.0),profile={str(x):round(w(x),3) for x in (0,0.5,1,1.5,2,2.5,3,4,6,10)},
                cdm_mass_loss_z0=float(rc[0]/(rcs*(acs)**3)))
out={'coupled':run('out_c_00_background.dat'),'control_uncoupled':run('out_u2_00_background.dat')}
c=out['coupled']; u=out['control_uncoupled']
out['DERIVED']=bool(c['n_switch']==1 and 1.5<=c['z_dagger'][0]<=3.2 and u['n_switch']==0)
out['SHAPE_MATCH']=bool(-3<=c['r3']<=-0.3)
print(json.dumps(out,indent=1)); json.dump(out,open('../../results/negspace_D1716.json','w'),indent=1)
