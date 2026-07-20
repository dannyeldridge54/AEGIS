from __future__ import annotations

import numpy as np

from aegis.physics import (
    torsion_hubble,
    torsion_hubble_evolving,
    comoving_distance,
    comoving_distance_evolving,
    growth_factor,
    luminosity_distance,
    distance_modulus,
)
from aegis.constants import (
    H0_PLANCK,
    OMEGA_M0,
    OMEGA_R0,
    SIGMA8_0,
    RS_PLANCK,
    C_LIGHT,
)
from aegis.tasks.data import (
    CC_DATA,
    DESI_BAO,
    RSD_DATA,
    PANTHEON_BINNED,
    SNE_SUMMARY,
)


def _param(name, min_value, max_value, description):
    return {"name": name, "min": min_value, "max": max_value, "description": description}


HZ_OBSERVATIONS = [
    {"z": 0.0, "H": 67.4, "sigma": 0.5},
    {"z": 0.07, "H": 69.0, "sigma": 19.6},
    {"z": 0.09, "H": 69.0, "sigma": 12.0},
    {"z": 0.12, "H": 68.6, "sigma": 26.2},
    {"z": 0.17, "H": 83.0, "sigma": 8.0},
    {"z": 0.20, "H": 72.9, "sigma": 29.6},
    {"z": 0.27, "H": 77.0, "sigma": 14.0},
    {"z": 0.28, "H": 88.8, "sigma": 36.6},
    {"z": 0.35, "H": 82.7, "sigma": 8.4},
    {"z": 0.40, "H": 95.0, "sigma": 17.0},
    {"z": 0.44, "H": 82.6, "sigma": 7.8},
    {"z": 0.48, "H": 97.0, "sigma": 62.0},
    {"z": 0.57, "H": 96.8, "sigma": 3.4},
    {"z": 0.59, "H": 104.0, "sigma": 13.0},
    {"z": 0.60, "H": 87.9, "sigma": 6.1},
    {"z": 0.68, "H": 92.0, "sigma": 8.0},
    {"z": 0.73, "H": 97.3, "sigma": 7.0},
    {"z": 0.78, "H": 105.0, "sigma": 12.0},
    {"z": 0.88, "H": 90.0, "sigma": 40.0},
    {"z": 1.04, "H": 154.0, "sigma": 20.0},
    {"z": 1.30, "H": 168.0, "sigma": 17.0},
    {"z": 1.43, "H": 177.0, "sigma": 18.0},
    {"z": 1.53, "H": 140.0, "sigma": 14.0},
    {"z": 1.75, "H": 202.0, "sigma": 40.0},
    {"z": 2.34, "H": 222.0, "sigma": 7.0},
    {"z": 2.36, "H": 226.0, "sigma": 8.0},
]


def _pantheon_value(*names):
    if PANTHEON_BINNED is None:
        return None
    for name in names:
        if name in PANTHEON_BINNED:
            return PANTHEON_BINNED[name]
    return None


def _desi_contribution(d, dm, dh, rs):
    chi2 = 0.0
    dv_rs = d.get("DV_rs")
    if dv_rs is not None:
        dv = (d["z"] * dm * dm * dh) ** (1.0 / 3.0)
        chi2 += ((dv / rs - dv_rs) / d["sigma"]) ** 2
    dm_rs = d.get("DM_rs")
    if dm_rs is not None:
        chi2 += ((dm / rs - dm_rs) / d["sigma"]) ** 2
    dh_rs = d.get("DH_rs")
    if dh_rs is not None:
        chi2 += ((dh / rs - dh_rs) / d["DH_sig"]) ** 2
    return chi2


def _compute_torsion_scalar(components):
    return float(np.sum(np.square(components)))


def _compute_trace_vector(components, dim=4):
    trace = np.zeros(dim, dtype=float)
    for a in range(dim):
        for b in range(dim):
            idx = min(a * dim + b, len(components) - 1)
            trace[a] += components[idx] if idx >= 0 else 0.0
    return trace


def _compute_axial_torsion(components):
    if len(components) < 4:
        return 0.0
    return components[0] * components[3] - components[1] * components[2]


def _ft_gravity_power_law(t_scalar, alpha, n):
    return alpha * np.power(abs(t_scalar), n) * np.sign(t_scalar)


def _ft_gravity_born_infeld(t_scalar, lam):
    arg = 1.0 + 2.0 * t_scalar / lam
    if arg <= 0:
        return -lam
    return lam * (np.sqrt(arg) - 1.0)


def _ft_gravity_logarithmic(t_scalar, alpha, beta, t0):
    if abs(t_scalar) < 1e-30:
        return 0.0
    return alpha * t_scalar + beta * t_scalar * np.log(abs(t_scalar / t0))


def _ft_gravity_exponential(t_scalar, alpha, beta, t0):
    if abs(t_scalar) < 1e-30:
        return 0.0
    return alpha * t_scalar * (1.0 - np.exp(beta * t0 / t_scalar))


def _cc_hubble_fit(p):
    chi2 = 0.0
    for z, h_obs, sigma in CC_DATA:
        h_pred = torsion_hubble(z, p["H0"], p["omega_m"], OMEGA_R0, p["beta"])
        chi2 += ((h_obs - h_pred) / sigma) ** 2
    return chi2


def _desi_bao_fit(p):
    chi2 = 0.0
    for d in DESI_BAO:
        dm = comoving_distance(d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta"])
        dh = C_LIGHT / torsion_hubble(d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta"])
        chi2 += _desi_contribution(d, dm, dh, p["rs"])
    return chi2


def _sne_pantheon_fit(p):
    if PANTHEON_BINNED is None:
        return 1e6
    z = _pantheon_value("z", "binZ")
    mu_obs = _pantheon_value("mu", "binMu")
    cov_inv = _pantheon_value("cov_inv", "covBinInv")
    n_bins = int(_pantheon_value("n_bins", "nBins") or len(z))
    if z is None or mu_obs is None or cov_inv is None:
        return 1e6
    delta = np.zeros(n_bins, dtype=float)
    for i in range(n_bins):
        mu_pred = distance_modulus(
            z[i],
            p["H0"],
            p["omega_m"],
            OMEGA_R0,
            p["beta0"],
            p["beta1"],
            50,
        )
        mb_pred = mu_pred + p["M_B"]
        delta[i] = mu_obs[i] - mb_pred
    return float(delta @ cov_inv @ delta)


def _h0_tension(p):
    z_star = 1089
    dc_star = comoving_distance_evolving(
        z_star,
        p["H0"],
        p["omega_m"],
        p["omega_r"],
        p["beta0"],
        p["beta1"],
        1000,
    )
    theta_star_pred = RS_PLANCK / dc_star
    theta_star_obs = 0.010411
    cmb_frac = (theta_star_pred / theta_star_obs - 1.0) / 0.003
    cmb_chi2 = cmb_frac * cmb_frac
    shoes_chi2 = ((p["H0"] - 73.04) / 1.04) ** 2

    cc_chi2 = 0.0
    for z, h_obs, sigma in CC_DATA[:10]:
        h_pred = torsion_hubble_evolving(
            z, p["H0"], p["omega_m"], p["omega_r"], p["beta0"], p["beta1"]
        )
        cc_chi2 += ((h_obs - h_pred) / sigma) ** 2

    bao_chi2 = 0.0
    for b in (
        {"z": 0.38, "DV_obs": 1477, "sigma": 16},
        {"z": 0.51, "DV_obs": 1877, "sigma": 19},
        {"z": 0.61, "DV_obs": 2140, "sigma": 22},
    ):
        dc = comoving_distance_evolving(
            b["z"], p["H0"], p["omega_m"], p["omega_r"], p["beta0"], p["beta1"], 200
        )
        hz = torsion_hubble_evolving(
            b["z"], p["H0"], p["omega_m"], p["omega_r"], p["beta0"], p["beta1"]
        )
        dv = (dc * dc * b["z"] * C_LIGHT / hz) ** (1.0 / 3.0)
        bao_chi2 += ((dv - b["DV_obs"]) / b["sigma"]) ** 2

    total = cmb_chi2 + shoes_chi2 + 0.5 * cc_chi2 + 0.3 * bao_chi2
    return float(total) if np.isfinite(total) else 1e6


def _rsd_growth(p):
    chi2 = 0.0
    for z, fsigma8_obs, sigma in RSD_DATA:
        d_growth = growth_factor(z, p["omega_m"], p["beta"])
        om_z = (
            p["omega_m"] * (1.0 + p["beta"]) * (1.0 + z) ** 3
            / (p["omega_m"] * (1.0 + p["beta"]) * (1.0 + z) ** 3 + (1.0 - p["omega_m"]))
        )
        f_growth = om_z ** p["gamma"]
        fsigma8_pred = f_growth * p["sigma8"] * d_growth
        chi2 += ((fsigma8_obs - fsigma8_pred) / sigma) ** 2
    return chi2


def _energy_conditions(p):
    violations = 0.0
    z_sample = [0, 0.1, 0.3, 0.5, 1, 2, 5, 10, 50, 100, 500, 1089]
    for z in z_sample:
        zp1 = 1.0 + z
        rho_m = p["omega_m"] * (1.0 + p["beta"]) * zp1**3
        rho_r = OMEGA_R0 * zp1**4
        rho_l = 1.0 - p["omega_m"] - OMEGA_R0
        rho_total = rho_m + rho_r + rho_l
        p_total = rho_r / 3.0 - rho_l
        if rho_total < 0:
            violations += 1
        if rho_total + p_total < 0:
            violations += 1
        if rho_total < abs(p_total):
            violations += 0.5
        rho_torsion = p["beta"] * p["omega_m"] * zp1**3
        if rho_torsion < -0.1 * rho_total:
            violations += 2
    for z in z_sample:
        h_val = torsion_hubble(z, H0_PLANCK, p["omega_m"], OMEGA_R0, p["beta"])
        if np.isnan(h_val) or h_val <= 0:
            violations += 5
    return violations


def _s8_tension(p):
    s8 = p["sigma8"] * np.sqrt(p["omega_m"] / 0.3)
    planck_chi2 = ((s8 - 0.834) / 0.016) ** 2
    kids_chi2 = ((s8 - 0.759) / 0.024) ** 2
    des_chi2 = ((s8 - 0.776) / 0.017) ** 2

    growth_chi2 = 0.0
    for z, fsigma8_obs, sigma in RSD_DATA[:4]:
        d_growth = growth_factor(z, p["omega_m"], p["beta"])
        om_z = (
            p["omega_m"] * (1.0 + p["beta"]) * (1.0 + z) ** 3
            / (p["omega_m"] * (1.0 + p["beta"]) * (1.0 + z) ** 3 + (1.0 - p["omega_m"]))
        )
        f_growth = om_z ** 0.55
        fsigma8_pred = f_growth * p["sigma8"] * d_growth
        growth_chi2 += ((fsigma8_obs - fsigma8_pred) / sigma) ** 2

    return planck_chi2 + kids_chi2 + des_chi2 + 0.3 * growth_chi2


def _dark_energy_eos(p):
    def hz(z):
        zp1 = 1.0 + z
        de = (
            (1.0 - p["omega_m"] - OMEGA_R0)
            * zp1 ** (3.0 * (1.0 + p["w0"] + p["wa"]))
            * np.exp(-3.0 * p["wa"] * z / zp1)
        )
        e2 = OMEGA_R0 * zp1**4 + p["omega_m"] * (1.0 + p["beta"]) * zp1**3 + de
        return p["H0"] * np.sqrt(max(e2, 1e-10))

    chi2 = 0.0
    for z, h_obs, sigma in CC_DATA:
        chi2 += ((h_obs - hz(z)) / sigma) ** 2

    for d in DESI_BAO:
        if d.get("DV_rs") is None:
            continue
        integral = 0.0
        steps = 100
        dz = d["z"] / steps
        for i in range(steps):
            z1 = i * dz
            z2 = (i + 1) * dz
            integral += 0.5 * (C_LIGHT / hz(z1) + C_LIGHT / hz(z2)) * dz
        dh = C_LIGHT / hz(d["z"])
        dv = (d["z"] * integral * integral * dh) ** (1.0 / 3.0)
        chi2 += ((dv / p["rs"] - d["DV_rs"]) / d["sigma"]) ** 2

    chi2 += 0.1 * ((p["w0"] + 1.0) / 0.3) ** 2
    return chi2


def _combined_multisurvey(p):
    chi2 = 0.0
    for z, h_obs, sigma in CC_DATA:
        h_pred = torsion_hubble_evolving(
            z, p["H0"], p["omega_m"], OMEGA_R0, p["beta0"], p["beta1"]
        )
        chi2 += ((h_obs - h_pred) / sigma) ** 2

    for d in DESI_BAO:
        dm = comoving_distance_evolving(
            d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta0"], p["beta1"], 200
        )
        dh = C_LIGHT / torsion_hubble_evolving(
            d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta0"], p["beta1"]
        )
        chi2 += _desi_contribution(d, dm, dh, p["rs"])

    for z, mu_obs, sigma in SNE_SUMMARY:
        mu_pred = distance_modulus(
            z, p["H0"], p["omega_m"], OMEGA_R0, p["beta0"], p["beta1"], 200
        )
        chi2 += ((mu_obs - mu_pred) / sigma) ** 2

    for z, fsigma8_obs, sigma in RSD_DATA:
        beta_eff = p["beta0"] + p["beta1"] * z / (1.0 + z)
        d_growth = growth_factor(z, p["omega_m"], beta_eff)
        om_z = (
            p["omega_m"] * (1.0 + beta_eff) * (1.0 + z) ** 3
            / (p["omega_m"] * (1.0 + beta_eff) * (1.0 + z) ** 3 + (1.0 - p["omega_m"]))
        )
        f_growth = om_z ** 0.55
        fsigma8_pred = f_growth * p["sigma8"] * d_growth
        chi2 += ((fsigma8_obs - fsigma8_pred) / sigma) ** 2
    return chi2


def _model_selection_bic(p):
    torsion_chi2 = _cc_hubble_fit(p)
    for d in DESI_BAO:
        dm = comoving_distance(d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta"])
        dh = C_LIGHT / torsion_hubble(d["z"], p["H0"], p["omega_m"], OMEGA_R0, p["beta"])
        torsion_chi2 += _desi_contribution(d, dm, dh, p["rs"])

    lcdm_chi2 = 0.0
    for z, h_obs, sigma in CC_DATA:
        h_pred = torsion_hubble(z, H0_PLANCK, OMEGA_M0, OMEGA_R0, 0.0)
        lcdm_chi2 += ((h_obs - h_pred) / sigma) ** 2
    for d in DESI_BAO:
        dm = comoving_distance(d["z"], H0_PLANCK, OMEGA_M0, OMEGA_R0, 0.0)
        dh = C_LIGHT / torsion_hubble(d["z"], H0_PLANCK, OMEGA_M0, OMEGA_R0, 0.0)
        lcdm_chi2 += _desi_contribution(d, dm, dh, RS_PLANCK)

    n_points = CC_DATA.shape[0] + len(DESI_BAO)
    bic_torsion = torsion_chi2 + 4 * np.log(n_points)
    bic_lcdm = lcdm_chi2 + 3 * np.log(n_points)
    delta_bic = bic_torsion - bic_lcdm
    return torsion_chi2 + max(0.0, delta_bic) * 5.0


def _ufe_emergence(p):
    mu2 = 10 ** p["log_mu2"]
    lam = 10 ** p["log_lambda"]
    if mu2 <= 0 or lam <= 0:
        return 1e6

    t_vev = np.sqrt(mu2 / (2.0 * lam))
    m_t2 = 4.0 * mu2
    m_t = np.sqrt(m_t2)
    _delta_t = 1.0 / np.sqrt(m_t + 1e-30)
    kappa_g = p["kappa_g"]
    z_decohere = p["z_decohere"]
    alpha_dec = p["alpha_dec"]

    def decoherence(z):
        return 1.0 / (1.0 + (z / z_decohere) ** alpha_dec)

    beta_classical = kappa_g * t_vev * t_vev * p["beta_scale"]
    beta_quantum = p["beta_quantum"]

    def beta_emergence(z):
        d_val = decoherence(z)
        beta_base = d_val * beta_classical + (1.0 - d_val) * beta_quantum
        transition_peak = np.exp(-0.5 * ((z - z_decohere) / (z_decohere * 0.3)) ** 2)
        transition_energy = p["transition_amp"] * transition_peak
        return beta_base + transition_energy

    def h_emergence(z):
        beta = beta_emergence(z)
        omega_l = 1.0 - p["omega_m"] - OMEGA_R0
        zp1 = 1.0 + z
        e2 = OMEGA_R0 * zp1**4 + p["omega_m"] * (1.0 + beta) * zp1**3 + omega_l
        return p["H0"] * np.sqrt(max(e2, 1e-10))

    def d_c(z, steps=200):
        if z <= 0:
            return 0.0
        ln_zp1 = np.log(1.0 + z)
        dln_zp1 = ln_zp1 / steps
        integral = 0.0
        for i in range(steps):
            z1 = np.exp(i * dln_zp1) - 1.0
            z2 = np.exp((i + 1) * dln_zp1) - 1.0
            dz = z2 - z1
            integral += 0.5 * (1.0 / h_emergence(z1) + 1.0 / h_emergence(z2)) * dz
        return C_LIGHT * integral

    chi2 = 0.0
    for z, h_obs, sigma in CC_DATA:
        chi2 += ((h_obs - h_emergence(z)) / sigma) ** 2

    for d in DESI_BAO:
        dm = d_c(d["z"])
        dh = C_LIGHT / h_emergence(d["z"])
        chi2 += _desi_contribution(d, dm, dh, p["rs"])

    sigma8 = p["sigma8"]
    for z, fsigma8_obs, sigma in RSD_DATA:
        beta = beta_emergence(z)
        d_growth = growth_factor(z, p["omega_m"], beta)
        om_z = (
            p["omega_m"] * (1.0 + beta) * (1.0 + z) ** 3
            / (p["omega_m"] * (1.0 + beta) * (1.0 + z) ** 3 + (1.0 - p["omega_m"]))
        )
        gamma_eff = 0.55 + beta * 0.1
        f_growth = om_z ** max(0.2, gamma_eff)
        fsigma8_pred = f_growth * sigma8 * d_growth
        chi2 += ((fsigma8_obs - fsigma8_pred) / sigma) ** 2

    for z, mu_obs, sigma in SNE_SUMMARY[[3, 5, 7, 9, 11, 13]]:
        d_l = (1.0 + z) * d_c(z)
        mu_pred = 5.0 * np.log10(max(d_l, 1e-10)) + 25.0
        chi2 += ((mu_obs - mu_pred) / sigma) ** 2

    effective_mass2 = m_t2 + 3.0 * lam * t_vev * t_vev
    wave_penalty = 100.0 if effective_mass2 < 0 else 0.0
    bbn_penalty = 50.0 * (0.1 - m_t) ** 2 if m_t < 0.1 else 0.0
    nec_violation = 0.0
    for z in np.arange(0.0, 5.01, 0.25):
        if 1.0 + beta_emergence(float(z)) < 0:
            nec_violation += 20.0
    beta_rec = beta_emergence(1089.0)
    rs_predicted = RS_PLANCK * np.sqrt(1.0 / (1.0 + beta_rec * 0.5))
    rs_penalty = ((p["rs"] - rs_predicted) / 5.0) ** 2
    dec_penalty = 50.0 * (0.1 - z_decohere) ** 2 if z_decohere < 0.1 else 0.0
    tension_bonus = -3.0 if 69.5 < p["H0"] < 74.5 else 0.0
    return (
        chi2
        + wave_penalty
        + bbn_penalty
        + nec_violation
        + rs_penalty
        + dec_penalty
        + tension_bonus
    )


def _einstein_cartan(p):
    torsion_components = [p["T01"], p["T02"], p["T03"], p["T12"], p["T13"], p["T23"]]
    t2 = _compute_torsion_scalar(torsion_components)
    trace = _compute_trace_vector(torsion_components)
    axial = _compute_axial_torsion(torsion_components)
    source_strength = 8.0 * np.pi * 6.674e-11 * p["spinDensity"]
    residual = sum((t - source_strength) ** 2 for t in torsion_components)
    action_term = p["couplingLambda"] * t2
    trace_residual = float(np.sum(trace * trace))
    return residual + 0.1 * action_term + 0.01 * trace_residual + 0.001 * axial * axial


def _ft_gravity(p):
    chi2 = 0.0
    for obs in HZ_OBSERVATIONS:
        hz_lcdm = H0_PLANCK * np.sqrt(OMEGA_M0 * (1.0 + obs["z"]) ** 3 + (1.0 - OMEGA_M0))
        t_scalar = -6.0 * hz_lcdm * hz_lcdm
        model_type = int(round(p["modelType"]))
        if model_type == 0:
            f_t = _ft_gravity_power_law(t_scalar, p["alpha"], p["n"])
        elif model_type == 1:
            f_t = _ft_gravity_born_infeld(t_scalar, abs(p["lambda"]) or 1.0)
        elif model_type == 2:
            f_t = _ft_gravity_logarithmic(t_scalar, p["alpha"], p["beta"], -6.0 * H0_PLANCK * H0_PLANCK)
        elif model_type == 3:
            f_t = _ft_gravity_exponential(t_scalar, p["alpha"], p["beta"], -6.0 * H0_PLANCK * H0_PLANCK)
        else:
            f_t = _ft_gravity_power_law(t_scalar, p["alpha"], p["n"])
        correction = f_t / (6.0 * H0_PLANCK * H0_PLANCK)
        hz_ft = hz_lcdm * np.sqrt(max(0.01, 1.0 + correction))
        chi2 += ((hz_ft - obs["H"]) / obs["sigma"]) ** 2
    regularization = 0.01 * (p["alpha"] ** 2 + p["beta"] ** 2 + p["n"] ** 2)
    result = chi2 + regularization
    return float(result) if np.isfinite(result) else 1e6


def _ufe_torsion(p):
    mu2 = 10 ** p.get("log_mu2", 10)
    lam = 10 ** p.get("log_lambda", 0)
    gamma = p["gamma"]
    epsilon = p["epsilon"]
    kappa_f = p["kappa_f"]
    kappa_g = p["kappa_g"]
    t0 = 10 ** p.get("log_T0", -6)
    n_density = 10 ** p.get("log_nDensity", 5)

    t2 = t0 * t0
    t4 = t2 * t2
    v_mexican = -mu2 * t2 + lam * t4
    t_vev = np.sqrt(mu2 / (2.0 * lam)) if mu2 > 0 and lam > 0 else 0.0
    m_t2 = 4.0 * mu2
    kinetic = 0.5 * gamma * t2 * 0.01
    h0_natural = 2.2e-18
    r_cosmo = 12.0 * h0_natural * h0_natural
    mixing = epsilon * r_cosmo * t2
    spin_polarization = 0.01
    axial_source = kappa_f * n_density * spin_polarization * t0
    graviton_source = kappa_g * r_cosmo * t2
    v_vev = -(mu2 * mu2) / (4.0 * lam) if mu2 > 0 and lam > 0 else 0.0
    _t_screen = t2 / (t2 + t_vev * t_vev) if t_vev > 0 else 1.0
    _action = v_mexican + kinetic + mixing + axial_source + graviton_source
    field_eqn = (
        -2.0 * mu2 * t0
        + 4.0 * lam * t0 * t2
        + 2.0 * epsilon * r_cosmo * t0
        + kappa_f * n_density * spin_polarization
    )
    field_scale = max(abs(2.0 * mu2 * t0), abs(4.0 * lam * t0 * t2), 1e-30)
    field_residual = (field_eqn / field_scale) ** 2

    penalty = 0.0
    if mu2 <= 0:
        penalty += 50.0 * mu2 * mu2
    if lam <= 0:
        penalty += 50.0 * lam * lam
    if mu2 > 0 and gamma > 0:
        v2 = gamma / (2.0 * mu2)
        if v2 > 1:
            penalty += 20.0 * (v2 - 1.0)
    if abs(kappa_f) > 4.0 * np.pi:
        penalty += 10.0 * (abs(kappa_f) - 4.0 * np.pi) ** 2

    v_ratio = abs((v_mexican - v_vev) / v_vev) if v_vev != 0 else abs(v_mexican)
    cosmo_penalty = min(v_ratio, 100.0)
    abs_t0 = abs(t0)
    log_t0 = p.get("log_T0", -6)
    log_barrier = 50.0 * (-10.0 - log_t0) ** 2 if log_t0 < -10 else 0.0
    vev_residual = np.log10(abs_t0 / t_vev) ** 2 if t_vev > 0 and abs_t0 > 0 else 100.0
    min_vev_scale = 1e-15
    vev_scale_penalty = (
        50.0 * np.log10(min_vev_scale / t_vev) ** 2
        if t_vev > 0 and t_vev < min_vev_scale
        else 0.0
    )
    m_t = np.sqrt(max(0.0, m_t2))
    bbn_penalty = (1.0 - m_t) ** 2 if m_t < 1.0 else 0.0
    return (
        field_residual
        + 10.0 * vev_residual
        + log_barrier
        + vev_scale_penalty
        + penalty
        + 0.5 * cosmo_penalty
        + 0.3 * bbn_penalty
    )


def _torsion_wave(p):
    m_t2 = 4.0 * max(0.0, p["mu2"])
    t_vev = np.sqrt(p["mu2"] / (2.0 * p["lambda_q"])) if p["mu2"] > 0 and p["lambda_q"] > 0 else 0.0
    effective_mass2 = m_t2 + 3.0 * p["lambda_q"] * t_vev * t_vev
    total_residual = 0.0
    n_points = 80
    for i in range(n_points):
        t = (i / n_points) * 4.0 * np.pi
        arg = p["frequency"] * t - p["wavenumber"] * t * 0.3 + p["phase"]
        d_t = p["amplitude"] * np.sin(arg)
        d2t_dt2 = -p["amplitude"] * p["frequency"] * p["frequency"] * np.sin(arg)
        d2t_dx2 = -p["amplitude"] * p["wavenumber"] * p["wavenumber"] * np.sin(arg)
        box_t = -d2t_dt2 + d2t_dx2
        nonlinear = 3.0 * p["lambda_q"] * t_vev * d_t * d_t
        residual = box_t + effective_mass2 * d_t + nonlinear - p["J_spin"]
        total_residual += residual * residual
    total_residual /= n_points

    dispersion = p["frequency"] ** 2 - p["wavenumber"] ** 2 - effective_mass2
    dispersion_residual = dispersion * dispersion / (effective_mass2 * effective_mass2 + 1e-30)
    v_group = abs(p["wavenumber"]) / p["frequency"] if p["frequency"] > 0 else 0.0
    causality_penalty = 50.0 * (v_group - 1.0) ** 2 if v_group > 1 else 0.0
    stability = 0.0
    if p["mu2"] <= 0:
        stability += 20.0
    if p["lambda_q"] <= 0:
        stability += 20.0
    amp_penalty = (p["amplitude"] / 1e6) ** 2 if abs(p["amplitude"]) > 1e6 else 0.0
    return total_residual + 0.5 * dispersion_residual + causality_penalty + stability + 0.001 * amp_penalty


def _ufe_cross_domain(p):
    h0 = p["H0_rescaled"] * 70.0
    ec_source = 8.0 * np.pi * p["spinDensity"]
    ec_residual = (p["T_scalar"] - ec_source) ** 2 + (p["ec_coupling"] * p["T_scalar"] * p["T_scalar"]) ** 2

    h0_nat = h0 * 1.967e-37
    t_cosmo = -6.0 * h0_nat * h0_nat
    f_t = p["fT_alpha"] * np.power(abs(t_cosmo), p["fT_n"]) * np.sign(t_cosmo)
    hz_predicted = h0 * np.sqrt(max(0.01, OMEGA_M0 + (1.0 - OMEGA_M0) + f_t / (6.0 * h0_nat * h0_nat + 1e-80)))
    cosmo_residual = ((hz_predicted - 67.4) / 3.37) ** 2

    mt2 = 4.0 * p["mu2"]
    t_vev = np.sqrt(p["mu2"] / (2.0 * p["lambda_quartic"])) if p["mu2"] > 0 and p["lambda_quartic"] > 0 else 0.0
    omega2 = mt2 + 3.0 * p["lambda_quartic"] * t_vev * t_vev
    wave_residual = (
        (p["wave_freq"] * p["wave_freq"] - omega2) ** 2 / (omega2 * omega2 + 1e-30)
        if omega2 > 0
        else 10.0
    )
    j_expected = 8.0 * np.pi * p["spinDensity"] * t_vev
    source_residual = (p["wave_source"] - j_expected) ** 2 / (j_expected * j_expected + 1e-30)
    ec_ft_consistency = (
        ((p["T_scalar"] * p["T_scalar"] - abs(t_cosmo)) / (abs(t_cosmo) + 1e-30)) ** 2
        if p["T_scalar"] != 0
        else 0.0
    )
    vev_penalty = max(0.0, np.log10(t_vev) + 10.0) ** 2 if t_vev > 0 else 50.0
    stability_penalty = 0.0
    if p["mu2"] <= 0:
        stability_penalty += 20.0
    if p["lambda_quartic"] <= 0:
        stability_penalty += 20.0
    abs_t = abs(p["T_scalar"])
    cross_log_barrier = 50.0 * max(0.0, -np.log10(abs_t) - 5.0) ** 2 if abs_t > 1e-20 else 1e5
    cross_vev_residual = 5.0 * ((abs_t - t_vev) / (t_vev + 1e-30)) ** 2 if t_vev > 1e-20 else 50.0
    return (
        ec_residual
        + 0.5 * cosmo_residual
        + 0.3 * wave_residual
        + 0.2 * source_residual
        + 0.1 * ec_ft_consistency
        + vev_penalty
        + stability_penalty
        + cross_log_barrier
        + cross_vev_residual
    )


CC_HUBBLE_FIT = {
    "id": "cc-hubble-fit",
    "name": "Cosmic Chronometer H(z) — Torsion Fit",
    "evaluate": _cc_hubble_fit,
    "parameters": [
        _param("H0", 55, 85, "Hubble constant km/s/Mpc"),
        _param("omega_m", 0.15, 0.50, "Matter density Ωm₀"),
        _param("beta", -0.8, 0.8, "Torsion coupling β"),
    ],
}

DESI_BAO_FIT = {
    "id": "desi-bao-fit",
    "name": "DESI DR1 BAO — Torsion Distances",
    "evaluate": _desi_bao_fit,
    "parameters": [
        _param("H0", 55, 85, "Hubble constant"),
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("beta", -0.8, 0.8, "Torsion coupling"),
        _param("rs", 125, 165, "Sound horizon r_s (Mpc)"),
    ],
}

SNE_PANTHEON_FIT = {
    "id": "sne-pantheon-fit",
    "name": "Pantheon+ 1701 SNe — Full Covariance (STAT+SYS)",
    "evaluate": _sne_pantheon_fit,
    "parameters": [
        _param("H0", 55, 100, "Hubble constant"),
        _param("omega_m", 0.10, 0.50, "Matter density"),
        _param("beta0", -0.3, 0.3, "Torsion coupling at z=0"),
        _param("beta1", -1.0, 1.0, "Torsion evolution: β(z) = β₀ + β₁·z/(1+z)"),
        _param("M_B", -19.6, -18.8, "SNe absolute magnitude"),
    ],
}

H0_TENSION = {
    "id": "h0-tension",
    "name": "H₀ Tension — Evolving Torsion Resolution",
    "evaluate": _h0_tension,
    "parameters": [
        _param("H0", 64, 76, "Hubble constant (tension range)"),
        _param("omega_m", 0.25, 0.40, "Matter density"),
        _param("omega_r", 5e-5, 2e-4, "Radiation density"),
        _param("beta0", -0.15, 0.15, "Torsion coupling at z=0 (late universe)"),
        _param("beta1", -0.5, 0.5, "Torsion evolution: β(z) = β₀ + β₁·z/(1+z)"),
    ],
}

RSD_GROWTH = {
    "id": "rsd-growth",
    "name": "RSD fσ₈ — Structure Growth under Torsion",
    "evaluate": _rsd_growth,
    "parameters": [
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("beta", -0.8, 0.8, "Torsion coupling"),
        _param("sigma8", 0.60, 1.00, "σ₈ amplitude"),
        _param("gamma", 0.35, 0.75, "Growth index (GR ≈ 0.55)"),
    ],
}

ENERGY_CONDITIONS = {
    "id": "energy-conditions",
    "name": "Energy Conditions — Torsion Viability",
    "evaluate": _energy_conditions,
    "parameters": [
        _param("omega_m", 0.20, 0.45, "Matter density"),
        _param("beta", -0.5, 0.5, "Torsion coupling"),
    ],
}

S8_TENSION = {
    "id": "s8-tension",
    "name": "S₈ Tension — Weak Lensing vs CMB",
    "evaluate": _s8_tension,
    "parameters": [
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("sigma8", 0.60, 1.00, "σ₈ amplitude"),
        _param("beta", -0.8, 0.8, "Torsion coupling"),
    ],
}

DARK_ENERGY_EOS = {
    "id": "dark-energy-eos",
    "name": "Dark Energy EoS — Torsion vs w₀wₐCDM",
    "evaluate": _dark_energy_eos,
    "parameters": [
        _param("H0", 55, 85, "Hubble constant"),
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("beta", -0.8, 0.8, "Torsion coupling"),
        _param("w0", -2.0, -0.3, "DE equation of state today"),
        _param("wa", -2.0, 2.0, "DE evolution parameter"),
        _param("rs", 125, 165, "Sound horizon"),
    ],
}

COMBINED_MULTISURVEY = {
    "id": "combined-multisurvey",
    "name": "Combined Multi-Survey — Evolving Torsion Fit",
    "evaluate": _combined_multisurvey,
    "parameters": [
        _param("H0", 55, 85, "Hubble constant"),
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("beta0", -0.3, 0.3, "Torsion at z=0"),
        _param("beta1", -1.0, 1.0, "Torsion evolution slope"),
        _param("rs", 125, 165, "Sound horizon"),
        _param("sigma8", 0.60, 1.00, "σ₈ amplitude"),
    ],
}

MODEL_SELECTION_BIC = {
    "id": "model-selection-bic",
    "name": "Model Selection — ΔBIC vs ΛCDM",
    "evaluate": _model_selection_bic,
    "parameters": [
        _param("H0", 55, 85, "Hubble constant"),
        _param("omega_m", 0.15, 0.50, "Matter density"),
        _param("beta", -0.8, 0.8, "Torsion coupling"),
        _param("rs", 125, 165, "Sound horizon"),
    ],
}

UFE_EMERGENCE = {
    "id": "ufe-emergence",
    "name": "UFE Emergence — Quantum to Cosmos",
    "evaluate": _ufe_emergence,
    "parameters": [
        _param("log_mu2", -2, 5, "log₁₀(μ²) Mexican hat mass"),
        _param("log_lambda", -3, 3, "log₁₀(λ) quartic coupling"),
        _param("kappa_g", -5, 5, "κ_g graviton-torsion coupling"),
        _param("z_decohere", 0.3, 5.0, "Redshift of quantum→classical transition"),
        _param("alpha_dec", 0.5, 5.0, "Sharpness of decoherence transition"),
        _param("beta_quantum", -0.05, 0.05, "Residual β in quantum regime (~0)"),
        _param("transition_amp", -0.3, 0.3, "Phase transition energy amplitude"),
        _param("beta_scale", -0.01, 0.01, "β₀ = κ_g·T²_vev·scale (condensate→cosmo)"),
        _param("kappa_f", -2, 2, "κ_f fermion coupling (drives β₁)"),
        _param("H0", 64, 76, "Hubble constant km/s/Mpc"),
        _param("omega_m", 0.25, 0.35, "Matter density (tighter: emergent)"),
        _param("rs", 140, 155, "Sound horizon (Mpc)"),
        _param("sigma8", 0.75, 0.90, "σ₈ amplitude"),
    ],
}

EINSTEIN_CARTAN = {
    "id": "einstein-cartan",
    "name": "Einstein-Cartan Torsion",
    "evaluate": _einstein_cartan,
    "parameters": [
        _param("T01", -1, 1, "Torsion T^0_{01}"),
        _param("T02", -1, 1, "Torsion T^0_{02}"),
        _param("T03", -1, 1, "Torsion T^0_{03}"),
        _param("T12", -1, 1, "Torsion T^1_{12}"),
        _param("T13", -1, 1, "Torsion T^1_{13}"),
        _param("T23", -1, 1, "Torsion T^2_{23}"),
        _param("spinDensity", 0, 1e20, "Spin density magnitude"),
        _param("couplingLambda", -10, 10, "Torsion-curvature coupling"),
    ],
}

TORSION_WAVE = {
    "id": "torsion-wave",
    "name": "Torsion Wave Dispersion",
    "evaluate": _torsion_wave,
    "parameters": [
        _param("mu2", 0.01, 1e15, "μ² from Mexican hat"),
        _param("lambda_q", 0.001, 5, "λ quartic coupling"),
        _param("amplitude", -1e3, 1e3, "Wave amplitude δT"),
        _param("frequency", 0.1, 1000, "Angular frequency ω"),
        _param("wavenumber", 0.01, 500, "Spatial wavenumber k"),
        _param("phase", 0, 6.283, "Phase offset"),
        _param("J_spin", -100, 100, "Spin current source"),
    ],
}

FT_GRAVITY = {
    "id": "ft-gravity",
    "name": "f(T) Teleparallel Gravity",
    "evaluate": _ft_gravity,
    "parameters": [
        _param("alpha", -5, 5, "f(T) primary coupling"),
        _param("beta", -5, 5, "f(T) secondary coupling"),
        _param("n", 0.5, 3, "Power law exponent"),
        _param("lambda", 0.01, 1000, "Born-Infeld scale"),
        _param("modelType", 0, 3, "0=power, 1=BI, 2=log, 3=exp"),
    ],
}

UFE_CROSS_DOMAIN = {
    "id": "ufe-cross-domain",
    "name": "UFE Cross-Domain Unified v3",
    "evaluate": _ufe_cross_domain,
    "parameters": [
        _param("T_scalar", 1e-10, 100, "Torsion scalar magnitude (forced non-zero)"),
        _param("mu2", 1e-3, 1e15, "μ² mass parameter (positive for SSB)"),
        _param("lambda_quartic", 1e-3, 50, "Quartic self-coupling (positive)"),
        _param("spinDensity", 1, 1e20, "Spin source (non-zero)"),
        _param("ec_coupling", -50, 50, "EC torsion-curvature coupling"),
        _param("fT_alpha", -20, 20, "f(T) amplitude"),
        _param("fT_n", 0.1, 4, "f(T) power law index"),
        _param("wave_freq", 0.01, 5000, "Torsion wave frequency"),
        _param("wave_source", -1000, 1000, "Wave spin current source"),
        _param("H0_rescaled", 0.85, 1.15, "H₀ in units of 70 km/s/Mpc"),
    ],
}

UFE_TORSION = {
    "id": "ufe-torsion",
    "name": "UFE Torsion Field (Mexican Hat v4)",
    "evaluate": _ufe_torsion,
    "parameters": [
        _param("log_mu2", -5, 25, "log₁₀(μ²) mass parameter"),
        _param("log_lambda", -4, 2, "log₁₀(λ) quartic coupling"),
        _param("gamma", 0.001, 100, "γ kinetic/gradient term"),
        _param("epsilon", -20, 20, "ε curvature-torsion mixing"),
        _param("kappa_f", -12, 12, "κ_f fermion axial coupling"),
        _param("kappa_g", -20, 20, "κ_g graviton-torsion coupling"),
        _param("log_T0", -12, 0, "log₁₀(T₀) background torsion"),
        _param("log_nDensity", 0, 10, "log₁₀(n) fermion density"),
    ],
}


ALL_TASKS = [
    CC_HUBBLE_FIT,
    DESI_BAO_FIT,
    SNE_PANTHEON_FIT,
    H0_TENSION,
    RSD_GROWTH,
    ENERGY_CONDITIONS,
    S8_TENSION,
    DARK_ENERGY_EOS,
    COMBINED_MULTISURVEY,
    MODEL_SELECTION_BIC,
    UFE_EMERGENCE,
    EINSTEIN_CARTAN,
    TORSION_WAVE,
    FT_GRAVITY,
    UFE_CROSS_DOMAIN,
    UFE_TORSION,
]

_TASKS_BY_ID = {task["id"]: task for task in ALL_TASKS}


def get_task(task_id):
    return _TASKS_BY_ID.get(task_id)


__all__ = [
    "ALL_TASKS",
    "CC_HUBBLE_FIT",
    "DESI_BAO_FIT",
    "SNE_PANTHEON_FIT",
    "H0_TENSION",
    "RSD_GROWTH",
    "ENERGY_CONDITIONS",
    "S8_TENSION",
    "DARK_ENERGY_EOS",
    "COMBINED_MULTISURVEY",
    "MODEL_SELECTION_BIC",
    "UFE_EMERGENCE",
    "EINSTEIN_CARTAN",
    "TORSION_WAVE",
    "FT_GRAVITY",
    "UFE_CROSS_DOMAIN",
    "UFE_TORSION",
    "get_task",
    "H0_PLANCK",
    "OMEGA_M0",
    "OMEGA_R0",
    "SIGMA8_0",
    "RS_PLANCK",
    "C_LIGHT",
]
