"""D571 H2: backward orbits of the 190 vetted fast stars (PREREG_D571)."""
import csv, json, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014, evaluatePotentials, vcirc
import astropy.units as u
RO,VO,ZO=8.122,236.,0.0208
STARS=sys.argv[1]; GAIA=sys.argv[2]; OUT=sys.argv[3]
sj=json.load(open(STARS)); dpc={r[0]:r[3] for r in sj['flagged']}
g={r['source_id']:r for r in csv.DictReader(open(GAIA))}
ts=np.linspace(0,-300,3001)*u.Myr
kw=dict(ro=RO,vo=VO,zo=ZO,solarmotion='schoenrich',radec=True)
def fl(x):
    try: return float(x)
    except: return np.nan
def orbits(ra,dec,d,pmra,pmdec,rv):
    o=Orbit(np.array([ra,dec,d,pmra,pmdec,rv]).T,**kw); o.integrate(ts,MWPotential2014,method='dop853_c'); return o
def rmin(o):
    r=np.sqrt(o.R(ts)**2+o.z(ts)**2); return r.min(axis=-1)
def vesc_now(o):
    R=o.R(); z=o.z(); phi=evaluatePotentials(MWPotential2014,R/RO,z/RO)*VO**2
    v=np.sqrt(o.vx()**2+o.vy()**2+o.vz()**2); return v,np.sqrt(-2*phi)
def disk_flag(o):
    """Within 100 Myr back: z sign change at R in [3,25] kpc; ejection speed relative to local circular rotation (galpy: vT>0 along (-y,x)/R)."""
    t=ts[:1001]; z=np.atleast_2d(o.z(t)); R=np.atleast_2d(o.R(t)); x=np.atleast_2d(o.x(t)); y=np.atleast_2d(o.y(t))
    vx=np.atleast_2d(o.vx(t)); vy=np.atleast_2d(o.vy(t)); vz=np.atleast_2d(o.vz(t)); out=[]
    for i in range(z.shape[0]):
        best=None
        for k in np.where(np.sign(z[i,:-1])!=np.sign(z[i,1:]))[0]:
            Rk=R[i,k]
            if not 3<=Rk<=25: continue
            vc=vcirc(MWPotential2014,Rk/RO)*VO
            dv=np.array([vx[i,k]+vc*y[i,k]/Rk, vy[i,k]-vc*x[i,k]/Rk, vz[i,k]])
            sp=float(np.linalg.norm(dv))
            if best is None or sp<best[1]: best=(float(Rk),sp,float(-t[k].to_value(u.Myr)))
        out.append(best if best and best[1]>300 else (best and {'R':best[0],'v_ej':best[1],'note':'<300'}))
    return out
res=[]; rng=np.random.default_rng(571)
rvscan=np.arange(-800,801,10.)
ids=list(g)
for sid in ids:
    r=g[sid]; d=dpc[sid]/1000.; ra,dec,pmra,pmdec=map(fl,(r['ra'],r['dec'],r['pmra'],r['pmdec'])); rv=fl(r['radial_velocity'])
    rec={'id':sid,'ra':ra,'dec':dec,'G':fl(r['phot_g_mean_mag']),'d_kpc':d,'pmra':pmra,'pmdec':pmdec,'rv':None if np.isnan(rv) else rv}
    if not np.isnan(rv):
        o=orbits([ra],[dec],[d],[pmra],[pmdec],[rv]); rec['rmin_gc']=float(rmin(o)[0]); v,ve=vesc_now(o); rec['vgc']=float(v[0]); rec['vesc']=float(ve[0])
        rec['disk']=disk_flag(o)[0]
        n=200; dd=d*(1+0.2*rng.standard_normal(n)); dd=np.clip(dd,0.05,None)
        om=orbits(np.full(n,ra),np.full(n,dec),dd,pmra+fl(r['pmra_error'])*rng.standard_normal(n),pmdec+fl(r['pmdec_error'])*rng.standard_normal(n),rv+fl(r['radial_velocity_error'])*rng.standard_normal(n))
        rm=rmin(om); v,ve=vesc_now(om); rec['f_gc1']=float(np.mean(rm<1)); rec['f_unbound']=float(np.mean(v>ve))
    else:
        n=len(rvscan); o=orbits(np.full(n,ra),np.full(n,dec),np.full(n,d),np.full(n,pmra),np.full(n,pmdec),rvscan)
        rm=rmin(o); k=int(np.argmin(rm)); rec['rv_star']=float(rvscan[k]); rec['rmin_at_rvstar']=float(rm[k])
        ok=rvscan[rm<1]; rec['rv_gc_range']=[float(ok.min()),float(ok.max())] if len(ok) else None
        v,ve=vesc_now(o); rec['vgc_at_rvstar']=float(v[k]); rec['vesc']=float(ve[k]); rec['unbound_at_rvstar']=bool(v[k]>ve[k])
        rec['gc_candidate']=bool(rm[k]<1 and abs(rvscan[k])<=800)
    res.append(rec); print(sid, {k:v for k,v in rec.items() if k in('rmin_gc','f_gc1','rv_star','rmin_at_rvstar','gc_candidate')},flush=True)
json.dump(res,open(OUT,'w'),indent=0)
