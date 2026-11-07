"""Validate and interpolate CLASS background data without importing CLASS."""
import numpy as np


def prepare_background(background, redshifts):
    keys = ("z", "H [1/Mpc]", "(.)p_scf", "(.)rho_scf",
            "(.)rho_g", "(.)rho_ur", "(.)rho_crit")
    arrays = {}
    for key in keys:
        if key not in background:
            raise ValueError(f"Missing CLASS background column: {key}")
        values = np.asarray(background[key], dtype=float)
        if values.ndim != 1 or values.size < 2 or not np.all(np.isfinite(values)):
            raise ValueError(f"Invalid CLASS background column: {key}")
        arrays[key] = values
    z = arrays["z"]
    if any(values.size != z.size for values in arrays.values()):
        raise ValueError("CLASS background column lengths differ")
    order = np.argsort(z)
    z = z[order]
    if np.any(np.diff(z) <= 0):
        raise ValueError("CLASS background redshifts must be unique")
    target = np.asarray(redshifts, dtype=float)
    if target.ndim != 1 or not target.size or not np.all(np.isfinite(target)) or np.any(target < 0):
        raise ValueError("Requested redshifts must be finite and nonnegative")
    if z[0] > 0 or z[-1] < max(0, target.max()):
        raise ValueError("CLASS background does not cover today and requested redshifts")
    for key in ("H [1/Mpc]", "(.)rho_scf", "(.)rho_crit"):
        if np.any(arrays[key] <= 0):
            raise ValueError(f"CLASS background column must be positive: {key}")
    for key in ("(.)rho_g", "(.)rho_ur"):
        if np.any(arrays[key] < 0):
            raise ValueError(f"CLASS background density must be nonnegative: {key}")

    def at(key, points):
        return np.interp(points, z, arrays[key][order])

    try:
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            h_today = float(at("H [1/Mpc]", 0))
            w = np.interp(target, z, (arrays["(.)p_scf"] / arrays["(.)rho_scf"])[order])
            expansion = at("H [1/Mpc]", target) / h_today
            radiation = float((at("(.)rho_g", 0) + at("(.)rho_ur", 0)) / at("(.)rho_crit", 0))
            h = h_today * 2997.92458
    except FloatingPointError as error:
        raise ValueError("CLASS background normalization overflowed or is undefined") from error
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(expansion)) or not np.isfinite(h) or not np.isfinite(radiation):
        raise ValueError("CLASS background normalized values must be finite")
    return expansion, w, h, radiation
