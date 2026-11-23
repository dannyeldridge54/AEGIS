"""PROM-5: OPEN-ADAS ADF11 reader, coronal ionisation balance, line cooling rate L_line(T_e, n_e) for Ar, Be, He, W.
ADF11 layout: header iz0, idmax, itmax, iz1min, iz1max; log10 densities (cm^-3); log10 temperatures (eV); then one block per Z1 of
itmax x idmax log10 coefficients, density index fastest (checked: a column then varies smoothly with T) [cm^3/s for SCD/ACD, W cm^3 for PLT/PRB]."""
import os, re
import numpy as np
from scipy.interpolate import RectBivariateSpline
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adas')
FILES = dict(ar='89', be='89', he='89', w='50')   # PROM-5 DEV-3: year-50 W set

def read_adf11(path):
    txt = open(path).read().split('\n'); h = txt[0].split(); iz0, idm, itm = int(h[0]), int(h[1]), int(h[2])
    nums, i = [], 2
    while len(nums) < idm + itm:
        nums += [float(x) for x in txt[i].split()]; i += 1
    logn, logT = np.array(nums[:idm]), np.array(nums[idm:idm + itm]); blocks = {}
    while i < len(txt):
        line = txt[i]
        m = re.search(r'Z1=\s*(\d+)', line)
        if m:
            z1 = int(m.group(1)); vals = []; i += 1
            while len(vals) < idm * itm and i < len(txt):
                if re.search(r'Z1=', txt[i]) or txt[i].strip().startswith('C'): break
                vals += [float(x) for x in txt[i].replace('D', 'E').split()]; i += 1
            blocks[z1] = np.array(vals[:idm * itm]).reshape(itm, idm).T   # stored density-fastest per temperature -> [density, temperature]
            continue
        i += 1
    return dict(iz0=iz0, logn=logn, logT=logT, blocks=blocks)

_CACHE = {}
def _load(el, kind):
    k = (el, kind)
    if k not in _CACHE: _CACHE[k] = read_adf11(os.path.join(HERE, f'{kind}{FILES[el]}_{el}.dat'))
    return _CACHE[k]

def _coef(d, z1, ne_cm3, Te_eV):
    b = d['blocks'][z1]; sp = RectBivariateSpline(d['logn'], d['logT'], b, kx=1, ky=1)
    x = np.clip(np.log10(ne_cm3), d['logn'][0], d['logn'][-1]); y = np.clip(np.log10(Te_eV), d['logT'][0], d['logT'][-1])
    return 10 ** float(sp(x, y)[0, 0])

def fractions(el, ne_m3, Te_keV):
    """Coronal balance: n_{z+1}/n_z = S_z / alpha_{z+1}; returns f_z for z = 0..Z."""
    scd, acd = _load(el, 'scd'), _load(el, 'acd'); Z = scd['iz0']; ne = ne_m3 * 1e-6; Te = Te_keV * 1e3
    logr = np.zeros(Z + 1)
    for z in range(Z):
        S = _coef(scd, z + 1, ne, Te); A = _coef(acd, z + 1, ne, Te); logr[z + 1] = logr[z] + np.log(S) - np.log(A)
    logr -= logr.max(); f = np.exp(logr); return f / f.sum()

def L_line(el, ne_m3, Te_keV):
    """Line cooling rate sum_z f_z PLT_z, in W m^3 (PLT block Z1 = z+1 is the emission of the ion with charge z)."""
    f = fractions(el, ne_m3, Te_keV); plt = _load(el, 'plt'); ne = ne_m3 * 1e-6; Te = Te_keV * 1e3
    return sum(f[z] * _coef(plt, z + 1, ne, Te) for z in range(plt['iz0'])) * 1e-6

_TAB = {}
def L_table(el, ne_m3=1e20, n=240, Tmin=0.01, Tmax=40.0):
    """Tabulated L_line(T) at fixed n_e on a log grid (n_e dependence is weak at these densities); log-log interpolation."""
    k = (el, ne_m3)
    if k not in _TAB:
        Ts = np.geomspace(Tmin, Tmax, n); _TAB[k] = (np.log(Ts), np.log([L_line(el, ne_m3, T) for T in Ts]))
    return _TAB[k]
def L_interp(el, T_keV, ne_m3=1e20):
    lt, ll = L_table(el, ne_m3); return np.exp(np.interp(np.log(np.clip(T_keV, 0.0105, 39.9)), lt, ll))


def L_imp(el, ne_m3, Te_keV, C_B=5.35e-37):
    """PROM-5 DEV-1: impurity radiation per impurity ion per electron beyond the Z_eff bremsstrahlung already in S3 (W m^3):
    sum_z f_z PLT_z + sum_z f_{z+1} PRB_z - C_B <z^2> sqrt(T_e)."""
    f = fractions(el, ne_m3, Te_keV); plt, prb = _load(el, 'plt'), _load(el, 'prb'); ne = ne_m3 * 1e-6; Te = Te_keV * 1e3; Z = plt['iz0']
    Lp = sum(f[z] * _coef(plt, z + 1, ne, Te) for z in range(Z)) * 1e-6
    Lr = sum(f[z + 1] * _coef(prb, z + 1, ne, Te) for z in range(Z)) * 1e-6
    z2 = float(sum(f[z] * z * z for z in range(Z + 1)))
    return Lp + Lr - C_B * z2 * Te_keV ** 0.5

_TAB2 = {}
def Limp_interp(el, T_keV, ne_m3=1e20, n=240):
    k = (el, ne_m3)
    if k not in _TAB2:
        Ts = np.geomspace(0.01, 40.0, n); _TAB2[k] = (np.log(Ts), np.array([L_imp(el, ne_m3, T) for T in Ts]))
    lt, L = _TAB2[k]; return np.interp(np.log(np.clip(T_keV, 0.0105, 39.9)), lt, L)
