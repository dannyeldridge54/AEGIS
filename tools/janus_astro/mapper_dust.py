"""Hyperion -> Star Mapper dust feed (PREP, not yet validated: maps not reachable from the cloud workspace).
E(B-V) along each star's line of sight from dustmaps: SFD 1998 (2D, total column) or Bayestar19 (3D, distance-resolved).
A_G = R_G * E(B-V): R_G must be passed explicitly (to be sourced; no default on purpose)."""
import numpy as np
def _coords(l_deg, b_deg, d_kpc=None):
    from astropy.coordinates import SkyCoord; import astropy.units as u
    kw = dict(l=np.atleast_1d(l_deg)*u.deg, b=np.atleast_1d(b_deg)*u.deg, frame='galactic')
    if d_kpc is not None: kw['distance'] = np.atleast_1d(d_kpc)*u.kpc
    return SkyCoord(**kw)
def ebv(l_deg, b_deg, d_kpc=None, which='sfd'):
    if which == 'sfd':
        from dustmaps.sfd import SFDQuery; return SFDQuery()(_coords(l_deg, b_deg))
    if which == 'bayestar':
        from dustmaps.bayestar import BayestarQuery
        return BayestarQuery(version='bayestar2019')(_coords(l_deg, b_deg, d_kpc), mode='median')   # Bayestar units -> E(B-V) needs its own sourced factor
    raise ValueError(which)
def A_G(l_deg, b_deg, R_G, d_kpc=None, which='sfd'): return R_G*ebv(l_deg, b_deg, d_kpc, which)
def fetch(which='sfd'):
    """Run on a machine that can reach Harvard Dataverse (Danny's PC). Downloads need Danny's OK."""
    if which == 'sfd':
        import dustmaps.sfd as m; m.fetch()
    else:
        import dustmaps.bayestar as m; m.fetch(version='bayestar2019')
