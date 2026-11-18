# AEGIS-FP XWW47DALN6E3ZP4U · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CH1 wavelength map (tool label: standard atomic physics; constants scipy.constants = CODATA). Lock PREREG_CH1_wavelength_map."""
import math
from scipy import constants as K
Rinf = K.Rydberg; c = K.c; h = K.h; me = K.m_e; mp = K.m_p; alpha = K.alpha; eV = K.e; gp = K.physical_constants['proton g factor'][0]
MASS = {'H': mp, 'He+': 4.001506179127*K.atomic_mass, 'Li2+': 7.014357697*K.atomic_mass}   # nuclear masses (He-4, Li-7 nuclei)
ZOF = {'H': 1, 'He+': 2, 'Li2+': 3}
SERIES = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund', 6: 'Humphreys'}
def line(ion='H', n_low=1, n_up=2):
    """Vacuum wavelength (nm) of a hydrogen-like transition (Bohr, reduced mass)."""
    Z = ZOF[ion]; R = Rinf/(1 + me/MASS[ion]); inv = R*Z*Z*(1/n_low**2 - 1/n_up**2); return 1e9/inv
def air(lam_vac_nm):
    """Vacuum→air wavelength (Morton 2000 / Edlén form), valid λ > 200 nm."""
    s2 = (1e3/lam_vac_nm)**2; n = 1 + 8.34254e-5 + 2.406147e-2/(130 - s2) + 1.5998e-4/(38.9 - s2); return lam_vac_nm/n
def series(ion='H', n_low=2, n_max=12):
    return [dict(ion=ion, series=SERIES.get(n_low, f'n={n_low}'), n_up=k, lam_nm=line(ion, n_low, k)) for k in range(n_low + 1, n_max + 1)] + [dict(ion=ion, series=SERIES.get(n_low), n_up='∞', lam_nm=line(ion, n_low, 10**9))]
def hydrogen_21cm():
    """Hyperfine frequency (Hz), Fermi formula with reduced-mass factor; no QED/recoil corrections."""
    return (8/3)*gp*(me/mp)*alpha**2*c*Rinf*(1 + me/mp)**-3   # CH1 DEV D1: 8/3 (lock had 4/3)
BANDS = [(1e-3, 'radio'), (1e-6, 'microwave/sub-mm'), (7.8e-7, 'infrared'), (3.8e-7, 'visible'), (1e-8, 'ultraviolet'), (1e-11, 'X-ray'), (0, 'gamma')]
def convert(lam_m=None, nu_hz=None, E_eV=None):
    if lam_m is None: lam_m = c/nu_hz if nu_hz else h*c/(E_eV*eV)
    nu = c/lam_m; E = h*nu/eV; band = next(b for lim, b in BANDS if lam_m >= lim)
    col = None
    if 3.8e-7 <= lam_m <= 7.8e-7:
        nm = lam_m*1e9; col = next(n for lim, n in ((450, 'violet'), (485, 'blue'), (500, 'cyan'), (565, 'green'), (590, 'yellow'), (625, 'orange'), (781, 'red')) if nm < lim)
    return dict(lam_m=lam_m, nu_hz=nu, E_eV=E, band=band, colour=col)
def ribbon():
    """Key marks on one log-λ axis (tool + physics marks; for the Janus wavelength view)."""
    T0 = 2.7255; lam_cmb = K.physical_constants['Wien wavelength displacement law constant'][0]/T0
    m = [dict(label='H Lyα', lam_m=line()*1e-9, kind='tool'), dict(label='H Hα', lam_m=line('H', 2, 3)*1e-9, kind='tool'),
         dict(label='He II 30.4 nm', lam_m=line('He+', 1, 2)*1e-9, kind='tool'), dict(label='H 21 cm', lam_m=c/hydrogen_21cm(), kind='tool'),
         dict(label='CMB peak today (Wien, T 2.7255 K)', lam_m=lam_cmb, kind='physics-literature'),
         dict(label='Lyα emitted at recombination z*≈1090 → observed today', lam_m=line()*1e-9*(1 + 1090.39), kind='physics (our U4 z*)')]
    return sorted(m, key=lambda x: x['lam_m'])
