import warnings, json, numpy as np, xarray as xr; warnings.filterwarnings('ignore')
def sel(path):
    D = xr.open_dataset(path)
    t = lambda k: D[k].transpose('dim_average_electron_temp','dim_average_electron_density', missing_dims='ignore')
    Q, Pf, Pa, fg, lh = (t(k) for k in ('Q','P_fusion','P_auxiliary_launched','greenwald_fraction','ratio_of_P_SOL_to_P_LH'))
    fg = fg.broadcast_like(Q)
    m = (Pa <= 25) & (Pa >= 0) & (fg <= 0.9) & (lh >= 1.0) & (Pf <= 140)
    Qm = Q.where(m); i = np.unravel_index(int(np.nanargmax(Qm.values)), Qm.shape)
    pt = {k: float(t(k).broadcast_like(Q).values[i]) for k in ('Q','P_fusion','P_auxiliary_launched','P_radiation','z_effective','dilution','energy_confinement_time','plasma_stored_energy')}
    pt['T_keV'] = float(Q.dim_average_electron_temp[i[0]]); pt['n_1e19'] = float(Q.dim_average_electron_density[i[1]])
    return D, pt
Dr, pr = sel('cfsp/tests/regression_results/SPARC_PRD_result.nc'); Do, po = sel('ours_full.nc')
print('THEIRS', json.dumps(pr)); print('OURS-ATOMIC', json.dumps(po))
# whole-grid atomic-data comparison where both finite
for k in ('P_radiation','z_effective','dilution','P_fusion','Q'):
    a = Dr[k].transpose(*Do[k].dims).values; b = Do[k].values; ok = np.isfinite(a) & np.isfinite(b) & (np.abs(a) > 1e-9)
    r = b[ok] / a[ok]; print(k, 'median ratio ours/theirs', round(float(np.median(r)),4), 'p5-p95', np.round(np.percentile(r,[5,95]),4))
json.dump(dict(theirs=pr, ours_atomic=po), open('cyc3_points.json','w'), indent=1)
