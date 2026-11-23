"""N3: read ENDF/B-VIII.0 (OpenMC HDF5) cross sections."""
import os, h5py, numpy as np
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ndata', 'h5')
def xs(nuc, mt, T='294K'):
    h = h5py.File(os.path.join(HERE, f'{nuc}.h5'))[nuc]; E = h['energy'][T][()]
    r = h['reactions'].get(f'reaction_{mt:03d}')
    if r is None: raise KeyError(f'{nuc} has no MT {mt}')
    d = r[T]['xs']; i0 = d.attrs.get('threshold_idx', 0); y = np.zeros_like(E); y[i0:i0 + len(d)] = d[()]
    return E, y
def at(nuc, mt, E_eV, T='294K'):
    E, y = xs(nuc, mt, T); return float(np.interp(E_eV, E, y))
def mts(nuc):
    h = h5py.File(os.path.join(HERE, f'{nuc}.h5'))[nuc]; return sorted(int(k.split('_')[1]) for k in h['reactions'])
