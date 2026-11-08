"""CosmoSIS module for the KiDS-Legacy test (field_tests/rules/PREREG_KIDS_LEGACY_SHEAR.md): load a stored model's linear
P(k, z), distances and growth (files from axiclass_pk.py / axhm_pk.py) and make the nonlinear power with KiDS-Legacy's
baseline model, HMcode-2020 with baryon feedback (Mead et al. 2021), via pyhmx (Tröster & Mead), at the sampled
halo_model_parameters/logT_AGN. Options:
    pk_file   = path to pk_<run>.npz
    nonlinear = camb_boost (default) | hmcode2020_feedback | stored  (stored: the file's p_k_nl as is, e.g. axionHMcode
                for S8-L)
    camb_boost: P_nl = P_lin(model) x [P_nl / P_lin] from CAMB HMcode-2020 + feedback at the model's omega_b, omega_cdm,
                h, n_s, sigma8 (A_s rescaled to match) and CPL (w0, wa); exact CAMB for LCDM (deviation D1: pyhmx
                differed from CAMB's HMcode-2020 feedback by 5-12% at k = 3-10 h/Mpc, so CAMB is used)
    omega_b, omega_cdm, n_s, w0, wa = the model's values (w0 = -1, wa = 0 for LCDM)"""
import numpy as np
from cosmosis.datablock import names, option_section

FEEDBACK_MODE = 103          # HMcode2020_feedback in the HMx library (library/src/hmx.f90)


def setup(options):
    d = dict(np.load(options.get_string(option_section, "pk_file")))
    d["_nl"] = options.get_string(option_section, "nonlinear", default="camb_boost")
    d["_w0"] = options.get_double(option_section, "w0", default=-1.0)
    d["_wa"] = options.get_double(option_section, "wa", default=0.0)
    d["_omb"] = options.get_double(option_section, "omega_b")
    d["_omc"] = options.get_double(option_section, "omega_cdm", default=0.0)
    d["_ns"] = options.get_double(option_section, "n_s")
    d["_cache"] = {}
    d["_cachefile"] = options.get_string(option_section, "cache_file", default="")
    if d["_nl"] == "hmcode2020_feedback":
        import pyhmx
        d["_hmx"] = pyhmx.HMx()
        d["_const"] = pyhmx.constants
    return d


def nonlinear(d, logT):
    key = round(float(logT), 6)
    if key not in d["_cache"]:
        if len(d["_cache"]) > 64:
            d["_cache"].clear()
        h = float(d["h0"]); om = float(d["omega_m"])
        pk = d["_hmx"]._run_hmx(om, d["_omb"], 1 - om, h, d["_ns"], float(d["sigma_8"][0]), 0.06, d["_w0"], d["_wa"],
                                halo_model_mode=FEEDBACK_MODE, Theat=10 ** key, eta0=0.603, As=3.13,
                                fields=np.array([d["_const"].field_matter]), k=d["k_h"], z=d["z_pk"],
                                pk_lin=d["p_k_lin"], verbose=False)
        d["_cache"][key] = np.ascontiguousarray(pk[0, 0])               # (nz, nk)
    return d["_cache"][key]


LOGT_GRID = np.round(np.arange(7.3, 8.3001, 0.05), 3)    # KiDS-Legacy prior range of logT_AGN


def camb_boost(d, logT):
    """ln P_nl interpolated linearly in logT_AGN between CAMB runs on LOGT_GRID (step 0.05), built once per model."""
    if "_grid" not in d:
        cf = d.get("_cachefile")
        if cf and __import__("os").path.exists(cf):
            d["_grid"] = np.load(cf)["lnp"]
        else:
            d["_grid"] = np.array([np.log(_camb_boost_at(d, t)) for t in LOGT_GRID])
            if cf:
                np.savez(cf, lnp=d["_grid"], logT=LOGT_GRID)
    t = float(np.clip(logT, LOGT_GRID[0], LOGT_GRID[-1]))
    i = min(int((t - LOGT_GRID[0]) / 0.05), len(LOGT_GRID) - 2)
    w = (t - LOGT_GRID[i]) / (LOGT_GRID[i + 1] - LOGT_GRID[i])
    return np.exp((1 - w) * d["_grid"][i] + w * d["_grid"][i + 1])


def _camb_boost_at(d, logT):
    key = round(float(logT), 6)
    if key not in d["_cache"]:
        if len(d["_cache"]) > 64:
            d["_cache"].clear()
        import camb
        h = float(d["h0"])
        kw = dict(H0=100 * h, ombh2=d["_omb"], omch2=d["_omc"], mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                  ns=d["_ns"], halofit_version="mead2020_feedback", HMCode_logT_AGN=key)
        if d["_w0"] != -1.0 or d["_wa"] != 0.0:
            kw.update(dark_energy_model="ppf", w=d["_w0"], wa=d["_wa"])
        zs = list(d["z_pk"])
        As = 2.1e-9
        for _ in range(2):                           # match the model's sigma8 (linear, z = 0)
            p = camb.set_params(As=As, **kw)
            p.set_matter_power(redshifts=zs, kmax=60.0, nonlinear=False)
            s8 = camb.get_results(p).get_sigma8_0()
            As *= (float(d["sigma_8"][0]) / s8) ** 2
        p = camb.set_params(As=As, **kw)
        p.set_matter_power(redshifts=zs, kmax=60.0, nonlinear=True)
        r = camb.get_results(p)
        kmax = 50.0
        ipl = r.get_matter_power_interpolator(nonlinear=False, hubble_units=True, k_hunit=True, extrap_kmax=600)
        ipn = r.get_matter_power_interpolator(nonlinear=True, hubble_units=True, k_hunit=True, extrap_kmax=600)
        kk = np.minimum(d["k_h"], kmax)
        boost = ipn.P(d["z_pk"], kk) / ipl.P(d["z_pk"], kk)          # beyond k = 50 h/Mpc the boost is held fixed
        d["_cache"][key] = d["p_k_lin"] * boost
    return d["_cache"][key]


def execute(block, d):
    zb = d["z_bg"]
    block[names.cosmological_parameters, "h0"] = float(d["h0"])
    block[names.cosmological_parameters, "omega_m"] = float(d["omega_m"])
    block[names.cosmological_parameters, "sigma_8"] = float(d["sigma_8"][0])
    dm = d["d_m"]
    block[names.distances, "z"] = zb
    block[names.distances, "a"] = 1 / (1 + zb)
    block[names.distances, "d_c"] = dm
    block[names.distances, "d_m"] = dm
    block[names.distances, "d_a"] = dm / (1 + zb)
    block[names.distances, "d_l"] = dm * (1 + zb)
    block[names.distances, "h"] = d["h"]
    block[names.distances, "nz"] = len(zb)
    block.put_grid(names.matter_power_lin, "z", d["z_pk"], "k_h", d["k_h"], "p_k", d["p_k_lin"])
    if d["_nl"] == "stored":
        pnl = d["p_k_nl"]
    elif d["_nl"] == "camb_boost":
        pnl = camb_boost(d, block[names.halo_model_parameters, "logT_AGN"])
    else:
        pnl = nonlinear(d, block[names.halo_model_parameters, "logT_AGN"])
    block.put_grid(names.matter_power_nl, "z", d["z_pk"], "k_h", d["k_h"], "p_k", pnl)
    zg = d["z_growth"]
    block[names.growth_parameters, "z"] = zg
    block[names.growth_parameters, "a"] = 1 / (1 + zg)
    block[names.growth_parameters, "d_z"] = d["d_z"]
    block[names.growth_parameters, "f_z"] = d["f_z"]
    block[names.growth_parameters, "sigma_8"] = d["sigma_8"]
    return 0
