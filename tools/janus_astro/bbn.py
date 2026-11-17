"""Hyperion BBN: thin wrapper on CAMB's tabulated BBN codes (PRIMAT 2021, PArthENoPE 880.2).
Yp = BBN helium NUCLEON fraction 4 n_He4/n_b (CAMB Y_p; NOT the mass fraction — DEVIATIONS_B1 D1); Yp_mass = mass fraction (table 'Yp' column); DH = D/H number ratio; inputs ω_b = Ω_b h², ΔN = N_eff − 3.044."""
from camb.bbn import BBN_table_interpolator
TABLES = {'primat': 'PRIMAT_Yp_DH_ErrorMC_2021.dat', 'parthenope': 'PArthENoPE_880.2_standard.dat'}
_cache = {}
def table(code='primat'):
    if code not in _cache: _cache[code] = BBN_table_interpolator(TABLES[code])
    return _cache[code]
def Yp(ombh2, dN=0.0, code='primat'): return float(table(code).Y_p(ombh2, dN))
def Yp_mass(ombh2, dN=0.0, code='primat'): return float(table(code).get('Yp', ombh2, dN))
def DH(ombh2, dN=0.0, code='primat'): return float(table(code).DH(ombh2, dN))
def sigma(ombh2, dN=0.0, code='primat'):
    """Theory errors (PRIMAT MC): returns (sig_Yp^BBN, sig_DH); PArthENoPE gives none -> (0, 0)."""
    if code != 'primat': return 0.0, 0.0
    t = table(code); return float(t.get('sig(Yp^BBN)', ombh2, dN)), float(t.get('sig(D/H)', ombh2, dN))
