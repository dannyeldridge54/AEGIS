"""Gate G1 (DRAFT_S8L_NONLINEAR.md): axionHMcode with no ULA vs CAMB HMcode-2020, same linear power, z = 0, 0.5, 1.
Code check only; no survey data. Pass: |ratio - 1| <= 2% for 0.01 <= k <= 10 h/Mpc.
    AXHM=<axionHMcode dir> python gate_g1.py  -> gate_g1.json"""
import json, os, sys
import numpy as np
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid   # numpy 2 rename; axionHMcode calls np.trapz (execution only)
sys.path.insert(0, os.environ.get("AXHM", "/home/claude/builds/ext/axionHMcode"))
import camb
from camb import model
from halo_model import HMcode_params, PS_nonlin_cold
from cosmology.overdensities import func_D_z_unnorm_int  # noqa: F401 (import check)
from axionCAMB_and_lin_PS import load_cosmology
sys.path.insert(0, HERE if "HERE" in dir() else os.path.dirname(os.path.abspath(__file__)))
from dewiggle import dewiggle_ratio
DW = os.environ.get("DEWIGGLE", "1") == "1"   # HMcode-2020 BAO damping of the two-halo term (patched copy)

HERE = os.path.dirname(os.path.abspath(__file__))
P = dict(h=0.6817, omega_b_0=0.02237, omega_d_0=0.1190, ns=0.966, As=2.1e-9)   # near the stored LCDM P+ point
FLAGS = dict(alpha=True, eta_given=True, one_halo_damping=True, two_halo_damping=True, concentration_param=True,
             full_2h=False)
out = {"flags": FLAGS, "dewiggle": DW, "axhm": os.environ.get("AXHM", ""), "rows": {}}
ok = True
for z in (0.0, 0.5, 1.0):
    f = os.path.join(HERE, "_g1_in.txt")
    open(f, "w").write("\n".join([f"omega_b_0 = {P['omega_b_0']}", f"omega_d_0 = {P['omega_d_0']}", "ax_fraction = 0.0",
                                  "m_ax = 1e-25", f"h = {P['h']}", f"z = {z}", "M_min = 7", "M_max = 18",
                                  f"ns = {P['ns']}", f"As = {P['As']}", "k_piv = 0.05", "transfer_kmax = 100",
                                  "version = 'dome'"]) + "\n")
    cos = load_cosmology.load_cosmology_input(f, LCDM=True)
    pars = camb.set_params(H0=100 * P["h"], ombh2=P["omega_b_0"], omch2=P["omega_d_0"], ns=P["ns"], As=P["As"], mnu=0.0,
                           omk=0, halofit_version="mead2020", tau=0.06)
    pars.set_matter_power(redshifts=[z], kmax=200.0)
    pars.NonLinear = model.NonLinear_none
    r = camb.get_results(pars)
    kh, _, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=100, npoints=600)
    pars.NonLinear = model.NonLinear_both
    r.calc_power_spectra(pars)
    kn, _, pn = r.get_matter_power_spectrum(minkh=1e-4, maxkh=100, npoints=600)
    M = np.logspace(cos["M_min"], cos["M_max"], 100)
    hp = HMcode_params.HMCode_param_dic(cos, kh, pk[0])
    if DW:
        hp["dw"] = dewiggle_ratio(kh, pk[0], P["h"], P["omega_b_0"] + P["omega_d_0"], P["omega_b_0"], P["ns"])
    nl = PS_nonlin_cold.func_non_lin_PS_matter(M, kh, pk[0], cos, hp, cos["Omega_m_0"], **FLAGS)[0]
    sel = (kh >= 0.01) & (kh <= 10)
    ratio = nl[sel] / pn[0][sel]
    dev = float(np.max(np.abs(ratio - 1)))
    ok &= dev <= 0.02
    out["rows"][f"{z:g}"] = {"max_dev": dev, "k_at_max": float(kh[sel][np.argmax(np.abs(ratio - 1))])}
    print(z, dev, flush=True)
os.remove(os.path.join(HERE, "_g1_in.txt"))
out["G1"] = "PASS" if ok else "FAIL"
json.dump(out, open(os.path.join(HERE, "gate_g1%s.json" % ("_dw" if DW else "")), "w"), indent=1)
print(out["G1"])
