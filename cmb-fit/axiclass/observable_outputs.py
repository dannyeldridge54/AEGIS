"""Read-only common observable predictions, with scalar diagnostics kept separate."""
import copy
import math

import numpy as np


REDSHIFTS = np.array([0., .295, .38, .51, .61, .706, .934, 1.321, 1.484, 2.33, 2.5])
WAVENUMBERS = np.geomspace(.001, 1., 100)
C_KM_S = 299792.458


def finite_values(values, label):
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"Nonfinite observable: {label}")
    return values.tolist()


def interpolate_background(background, column, redshifts):
    z = np.asarray(background["z"], dtype=float)
    values = np.asarray(background[column], dtype=float)
    requested = np.asarray(redshifts, dtype=float)
    if z.ndim != 1 or z.size < 2 or values.shape != z.shape or requested.ndim != 1:
        raise ValueError(f"Invalid background column dimensions: {column}")
    if not np.isfinite(z).all() or not np.isfinite(values).all() or not np.isfinite(requested).all():
        raise ValueError(f"Nonfinite background column: {column}")
    order = np.argsort(z)
    z, values = z[order], values[order]
    if np.any(np.diff(z) <= 0):
        raise ValueError("Background redshifts must be distinct")
    if requested.size and (requested.min() < z[0] or requested.max() > z[-1]):
        raise ValueError("Requested redshifts extend beyond computed background")
    return finite_values(np.interp(requested, z, values), column)


def evaluate_observables(info, point):
    """Evaluate a supplied point; never minimize, write files, or modify input config."""
    from cobaya.model import get_model

    cfg = copy.deepcopy(info)
    for key in ("sampler", "output", "resume", "force"):
        cfg.pop(key, None)
    with get_model(cfg) as model:
        model.add_requirements({"Pk_grid": {"z": REDSHIFTS.tolist(), "k_max": 1., "nonlinear": True}})
        sampled = {key: point[key] for key in model.parameterization.sampled_params()}
        post = model.logposterior(sampled, cached=False)
        if not math.isfinite(post.logpost) or not np.isfinite(post.loglikes).all():
            raise RuntimeError("Observable export requires a finite likelihood and allowed parameter point")
        loglikes = np.asarray(post.loglikes, dtype=float)
        if loglikes.ndim != 1 or loglikes.size != len(model.likelihood):
            raise ValueError("Likelihood results do not match the configured likelihoods")
        with np.errstate(over="raise", invalid="raise"):
            try:
                contributions = -2 * loglikes
            except FloatingPointError as error:
                raise ValueError("Likelihood contribution calculation overflowed") from error
        if not np.isfinite(contributions).all():
            raise ValueError("Likelihood contributions must be finite")
        solver = model.theory["classytwist"].classy
        derived = solver.get_current_derived_parameters(["H0", "sigma8", "Omega_m", "age"])
        for key in ("H0", "sigma8", "Omega_m", "age"):
            if key not in derived or not math.isfinite(derived[key]):
                raise ValueError(f"Missing or nonfinite derived parameter: {key}")
        # Use actual background density, not the scalar-contaminated CLASS summary.
        background = solver.get_background()
        densities = [column for column in background
                     if column in ("(.)rho_b", "(.)rho_cdm") or column.startswith("(.)rho_ncdm[")]
        if not {"(.)rho_b", "(.)rho_cdm"}.issubset(densities):
            raise ValueError("Missing physical matter-density background")
        matter_components = [interpolate_background(background, column, [0.])[0]
                             for column in densities]
        if any(value < 0 for value in matter_components):
            raise ValueError("Physical matter-density components must be nonnegative")
        rho_m = sum(matter_components)
        if not math.isfinite(rho_m):
            raise ValueError("Total matter density must be finite")
        rho_crit = interpolate_background(background, "(.)rho_crit", [0.])[0]
        if rho_crit <= 0:
            raise ValueError("Nonpositive present critical density")
        omega_m = rho_m/rho_crit
        if not math.isfinite(omega_m):
            raise ValueError("Normalized matter density must be finite")
        s8 = float(derived["sigma8"]) * math.sqrt(omega_m) / math.sqrt(.3)
        if not math.isfinite(s8):
            raise ValueError("S8 must be finite")
        rd = float(solver.rs_drag())
        if not math.isfinite(rd) or rd <= 0:
            raise ValueError("Invalid drag sound horizon")
        hubble = np.array([solver.Hubble(z)*C_KM_S for z in REDSHIFTS])
        if not np.isfinite(hubble).all() or np.any(hubble <= 0):
            raise ValueError("Invalid expansion-rate predictions")
        dm = np.array([solver.angular_distance(z)*(1+z) for z in REDSHIFTS])
        dl = np.array([solver.luminosity_distance(z) for z in REDSHIFTS])
        cls = model.provider.get_Cl(ell_factor=False)
        if "ell" not in cls:
            raise ValueError("Missing required CMB multipoles")
        ell = np.asarray(cls["ell"])
        if (ell.ndim != 1 or ell.size < 2501
                or not np.array_equal(ell[:2501], np.arange(2501))):
            raise ValueError("CMB multipoles must cover integer ell=0 through 2500 in order")
        result = {
            "status": "Predictions at supplied point, not measurements or posterior intervals",
            "parameters": {key: float(value) for key, value in sampled.items()},
            "chi2_by_likelihood": {key: float(value) for key, value in zip(model.likelihood, contributions)},
            "H0_km_s_Mpc": float(derived["H0"]), "sigma8": float(derived["sigma8"]),
            "Omega_m_matter_background": omega_m, "Omega_m_class_reported": float(derived["Omega_m"]),
            "S8": s8,
            "age_Gyr": float(derived["age"]), "r_drag_Mpc": rd,
            "redshift": REDSHIFTS.tolist(),
            "H_km_s_Mpc": finite_values(hubble, "H"),
            "D_M_Mpc": finite_values(dm, "D_M"),
            "D_L_Mpc": finite_values(dl, "D_L"),
            "D_M_over_r_drag": finite_values(dm/rd, "D_M/r_drag"),
            "D_H_over_r_drag": finite_values(C_KM_S/hubble/rd, "D_H/r_drag"),
            "fsigma8": finite_values([solver.effective_f_sigma8(z) for z in REDSHIFTS], "fsigma8"),
            "k_per_Mpc": WAVENUMBERS.tolist(),
            "P_linear_Mpc3": finite_values([[solver.pk_lin(k, z) for k in WAVENUMBERS]
                                          for z in REDSHIFTS], "linear matter power"),
            "P_nonlinear_Mpc3": finite_values([[solver.pk(k, z) for k in WAVENUMBERS]
                                             for z in REDSHIFTS], "nonlinear matter power"),
            "cmb": {"ell": [int(ell) for ell in cls["ell"][2:2501]],
                    "convention": "Unweighted lensed C_ell; TT/TE/EE/BB in microkelvin squared, pp dimensionless"},
            "limitations": ["No galaxy-shear likelihood or nuisance marginalization is performed.",
                            "Fixed-point exports contain no measurement or posterior uncertainty.",
                            "Effective growth approximation must be revalidated for coupled or scale-dependent branches."]
        }
        for key in ("tt", "te", "ee", "bb", "pp"):
            if key not in cls:
                raise ValueError(f"Missing required CMB spectrum: {key}")
            spectrum = np.asarray(cls[key], dtype=float)
            if spectrum.ndim != 1 or spectrum.size < 2501:
                raise ValueError(f"Invalid required CMB spectrum dimensions: {key}")
            result["cmb"][key] = finite_values(spectrum[2:2501], key)
        scalar = {}
        for column in ("(.)Omega_scf", "(.)w_scf", "phi_scf", "phi'_scf", "V_scf"):
            if column in background:
                scalar[column] = interpolate_background(background, column, REDSHIFTS)
        result["scalar_field_diagnostics"] = {
            "available": bool(scalar), "values": scalar,
            "scope": "Branch-specific solver diagnostics, not shared observations or a local Galactic field solution"}
        return result
