"""Cycle 3: radas-format atomic data (cfspopcon) built from our local OPEN-ADAS ADF11 mirror. Coronal; equilibrium_* = coronal copies."""
import os, sys, numpy as np, xarray as xr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import adas as A
def build(el, name, out, Ts=np.geomspace(1.0, 4.0e4, 60), nes=np.geomspace(1e17, 1e21, 9), ne_tau=(0.5e17, 1e17, 1e18, 1e19, 1e20)):
    Lz = np.zeros((len(Ts), len(nes))); Zm = np.zeros_like(Lz)
    plt, prb = A._load(el, 'plt'), A._load(el, 'prb'); Z = plt['iz0']
    for j, ne in enumerate(nes):
        for i, T in enumerate(Ts):
            f = A.fractions(el, ne, T / 1e3); nc, Te = ne * 1e-6, T
            Lp = sum(f[z] * A._coef(plt, z + 1, nc, Te) for z in range(Z)) * 1e-6
            Lr = sum(f[z + 1] * A._coef(prb, z + 1, nc, Te) for z in range(Z)) * 1e-6
            Lz[i, j] = max(Lp + Lr, 1e-45); Zm[i, j] = max(float(sum(z * f[z] for z in range(Z + 1))), 1e-6)
    nt = len(ne_tau)
    ds = xr.Dataset(dict(coronal_Lz=(('dim_electron_temp', 'dim_electron_density'), Lz, dict(units='W*m**3')),
                         coronal_mean_charge_state=(('dim_electron_temp', 'dim_electron_density'), Zm, dict(units='dimensionless')),
                         equilibrium_Lz=(('dim_ne_tau', 'dim_electron_temp', 'dim_electron_density'), np.repeat(Lz[None], nt, 0), dict(units='W*m**3')),
                         equilibrium_mean_charge_state=(('dim_ne_tau', 'dim_electron_temp', 'dim_electron_density'), np.repeat(Zm[None], nt, 0), dict(units='dimensionless')),
                         ne_tau=(('dim_ne_tau',), np.array(ne_tau), dict(units='m**-3*s')),
                         reference_electron_density=((), 1.0, dict(units='m**-3')), reference_electron_temp=((), 1.0, dict(units='eV'))),
                    coords=dict(dim_electron_temp=('dim_electron_temp', Ts), dim_electron_density=('dim_electron_density', nes),
                                dim_ne_tau=('dim_ne_tau', np.array(ne_tau))),
                    attrs=dict(atomic_number=dict(he=2, o=8, w=74, xe=54, ar=18, ne=10, n=7, c=6)[el], radas_version='aegis-adas-mirror-coronal-1', source='OPEN-ADAS ADF11 via ProjectTorreyPines/ADAS.jl mirror; coronal'))
    ds.to_netcdf(os.path.join(out, f'{name}.nc'))
if __name__ == '__main__':
    out = sys.argv[1]
    for el, nm in (('he', 'helium'), ('o', 'oxygen'), ('w', 'tungsten'), ('xe', 'xenon'), ('ar', 'argon')): build(el, nm, out); print('built', nm)
