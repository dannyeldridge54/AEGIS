"""CosmoSIS module for S8-WL Part 2 (field_tests/rules/PREREG_S8_WL.md): the CosmoSIS-standard-library CAMB module,
with the dark energy of a stored AEGIS best fit put in. Options (in the [camb] section of the pipeline ini):
    aegis_model = lcdm | edelock | ub      aegis_point = path to the stored cmp_<run>.json
lcdm: CAMB's plain cosmological constant. edelock: CAMB EarlyQuintessence n = 3 with the stored f_EDE, theta_i and the
locked z_c. ub: the two-field UB module (needs the CAMB build from cmb-fit/ub2_camb/). Everything else (P(k,z),
distances, halofit Takahashi, saving) is the standard library's camb_interface, unchanged."""
import json
import math
import os
import sys

from cosmosis.datablock import option_section

CSL = os.environ["CSL_DIR"]
sys.path.insert(0, os.path.join(CSL, "boltzmann", "camb"))
import camb  # noqa: E402
import camb_interface as CI  # noqa: E402

_orig_de = CI.extract_dark_energy_params


def _bao_no_reinit(self, redshifts, params=None):
    """Same outputs as CAMBdata.get_BAO (rs/DV, H, DA, F_AP), from the already computed background. CAMB's own get_BAO
    re-runs the background on a copy of the params, which re-initialises EarlyQuintessence and crashes in Fortran."""
    import numpy as np
    z = np.atleast_1d(np.asarray(redshifts, dtype=float))
    c = 299792.458
    rd = self.get_derived_params()["rdrag"]
    H = np.array([self.hubble_parameter(zz) for zz in z])
    DA = np.array([self.angular_diameter_distance(zz) for zz in z])
    DV = ((1 + z) ** 2 * DA ** 2 * c * z / H) ** (1 / 3)
    return np.array([rd / DV, H, DA, (1 + z) * DA * H / c]).T


camb.results.CAMBdata.get_BAO = _bao_no_reinit
STATE = {}


def _de(block, config, more_config):
    model, m = STATE["model"], STATE["point"]
    if model in ("lcdm", "edelock"):
        return _orig_de(block, config, more_config)          # edelock: replaced just before get_results (execute)
    if model == "edelock_unused":
        zc = m.get("zc") or (m["ombh2"] + m["omch2"]) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1
        de = camb.dark_energy.EarlyQuintessence()
        de.set_params(n=3, use_zc=True, zc=zc, fde_zc=m["fde_zc"], theta_i=m["theta_i"])
        return de
    if model == "ub":
        sys.path.insert(0, os.path.join(STATE["aegis"], "cmb-fit"))
        import ub2_fit as U
        p = camb.set_params(H0=m["H0"], ombh2=m["ombh2"], omch2=m["omch2"], mnu=0.06, num_massive_neutrinos=1,
                            nnu=3.044, As=2.1e-9, ns=0.965)
        rho, rhop, other0 = U.other_densities(p)
        par = {k: m[k] for k in ("ub_lnL", "ub_thi", "ub_phii", "ub_kappa")}
        rf, lnA, tab = U.field_history(par, "B", rho, rhop, other0)
        return U.ub_darkenergy(tab, m["H0"])
    raise ValueError(f"unknown aegis_model {model}")


def setup(options):
    STATE["model"] = options.get_string(option_section, "aegis_model")
    STATE["point"] = json.load(open(options.get_string(option_section, "aegis_point")))["minimum"]
    STATE["aegis"] = os.environ.get("AEGIS_DIR", os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    CI.extract_dark_energy_params = _de
    return CI.setup(options)


def execute(block, config):
    """Cosmology is held fixed in Part 2, so CAMB runs once and its results are reused for every nuisance step
    (the block is filled by the standard library's own save functions each time)."""
    cfg, more = config
    if "r" not in STATE:
        p = CI.extract_camb_params(block, cfg, more)
        if STATE["model"] == "edelock":
            # CAMB's EarlyQuintessence is initialised twice when attached to the standard-library params object
            # (Fortran "already allocated"); build a fresh params object with the same cosmology and P(k) settings.
            m = STATE["point"]
            zc = m.get("zc") or (m["ombh2"] + m["omch2"]) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1
            p2 = camb.set_params(H0=p.H0, ombh2=p.ombh2, omch2=p.omch2, mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                                 tau=m["tau"], As=p.InitPower.As, ns=p.InitPower.ns, dark_energy_model="EarlyQuintessence",
                                 n=3, use_zc=True, zc=zc, fde_zc=m["fde_zc"], theta_i=m["theta_i"])
            nz = p.Transfer.PK_num_redshifts
            p2.set_matter_power(redshifts=list(p.Transfer.PK_redshifts[:nz]), kmax=p.Transfer.kmax, nonlinear=True)
            p2.NonLinearModel.set_params(halofit_version="takahashi")
            p2.WantCls = False
            p = p2
        STATE["r"] = camb.get_results(p)
        STATE["want_transfer"] = p.WantTransfer
    r = STATE["r"]
    with CI.be_quiet_camb():
        CI.save_derived_parameters(r, block)
        CI.save_distances(r, block, more)
        if STATE["want_transfer"]:
            CI.save_matter_power(r, block, more)
    return 0
