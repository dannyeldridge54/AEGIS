import pathlib, numpy as np, warnings, json, sys; warnings.filterwarnings('ignore')
from cfspopcon.input_file_handling import read_case
from cfspopcon.algorithm_class import CompositeAlgorithm
import xarray as xr
from cfspopcon.unit_handling import ureg
case = pathlib.Path(sys.argv[1])
inp, algs, pts, _ = read_case(case)
alg = CompositeAlgorithm.from_list(algs) if isinstance(algs, list) else algs
try: ds = alg.update_dataset(xr.Dataset(inp))
except Exception as e:
    import traceback; traceback.print_exc(limit=8); raise SystemExit
from cfspopcon import file_io; file_io.write_dataset_to_netcdf(ds, filepath=pathlib.Path("ours_full.nc"))
Pf = ds['P_fusion'].pint.to('MW'); Pa = ds['P_auxiliary_launched'].pint.to('MW'); Q = ds['Q']
m = (Pa <= 25 * ureg.MW) & (Pa >= 0 * ureg.MW) & (ds['greenwald_fraction'] <= 0.9) & (ds['ratio_of_P_SOL_to_P_LH'] >= 1.0) & (Pf <= 140 * ureg.MW)
Qm = Q.where(m); i = np.unravel_index(int(np.nanargmax(Qm.values)), Qm.shape); pt = ds.isel({d: i[k] for k, d in enumerate(Qm.dims)})
out = {}
for k in ('average_electron_density', 'average_electron_temp', 'P_fusion', 'P_auxiliary_launched', 'P_auxiliary_absorbed', 'Q', 'energy_confinement_time', 'plasma_stored_energy',
          'P_radiation', 'greenwald_fraction', 'plasma_volume', 'z_effective', 'dilution', 'P_in', 'P_alpha', 'P_ohmic', 'ratio_of_P_SOL_to_P_LH', 'peak_electron_temp', 'electron_density_peaking'):
    if k in pt: out[k] = [float(np.squeeze(pt[k].pint.magnitude)), str(pt[k].pint.units)]
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out))
