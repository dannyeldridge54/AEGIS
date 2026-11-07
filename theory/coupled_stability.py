"""Symbolic entropy-mode diagnostics for the assumed two-field action.

Reduced Planck units. No fit, trajectory integration, or archive writes.
"""
import json
import math

import sympy as sp


def trajectory_diagnostic(sol, potential, V0, kap, mass, decay, lam, N):
    """Evaluate scalar-sector mass terms on an existing spiral_w solution."""
    from theory.spiral_w import H2_of

    if not all(math.isfinite(v) for v in (V0, kap, mass, decay, lam, N)) or decay <= 0:
        raise ValueError("Diagnostic parameters must be finite with positive decay constant")
    if getattr(sol, "action_parameters", None) != (V0, kap, mass, decay, lam):
        raise ValueError("Diagnostic action parameters do not match the solved trajectory")
    if getattr(sol, "action_potential", None) is not potential:
        raise ValueError("Diagnostic potential does not belong to the solved trajectory")
    h2 = H2_of(sol, potential, N, lam)[0]
    chi, chi_prime, theta, theta_prime = sol.sol(N)
    metric = math.exp(lam * chi)
    vchi = math.sqrt(h2) * chi_prime
    vtheta = math.sqrt(h2) * theta_prime
    speed2 = vchi**2 + metric * vtheta**2
    if not math.isfinite(speed2) or speed2 <= 0:
        raise ValueError("Entropy direction is undefined at zero/nonfinite field speed")
    speed = math.sqrt(speed2)
    normal_chi = -math.sqrt(metric) * vtheta / speed
    normal_theta = vchi / (math.sqrt(metric) * speed)
    exponential = V0 * math.exp(-kap * chi)
    gradient_chi = -kap * exponential
    gradient_theta = mass**2 * decay * math.sin(theta / decay)
    hessian_chi_chi = kap**2 * exponential
    hessian_chi_theta = -lam * gradient_theta / 2
    hessian_theta_theta = mass**2 * math.cos(theta / decay) + lam * metric * gradient_chi / 2
    projected = (
        normal_chi**2 * hessian_chi_chi
        + 2 * normal_chi * normal_theta * hessian_chi_theta
        + normal_theta**2 * hessian_theta_theta
    )
    normal_gradient = normal_chi * gradient_chi + normal_theta * gradient_theta
    turning = 3 * (normal_gradient / speed)**2
    geometric = -lam**2 * speed2 / 4
    terms = (projected, turning, geometric)
    if not all(math.isfinite(v) for v in terms):
        raise ValueError("Entropy mass diagnostic is non-finite")
    total = sum(terms)
    normalized = [float(value / h2) for value in (*terms, total)]
    if not all(math.isfinite(value) for value in normalized):
        raise ValueError("Normalized entropy mass diagnostic is non-finite")
    return {
        "N": float(N),
        "projected_hessian_over_H2": normalized[0],
        "turning_contribution_over_H2": normalized[1],
        "geometric_contribution_over_H2": normalized[2],
        "entropy_mass_squared_over_H2": normalized[3],
        "negative_mass_risk": bool(total < 0),
        "full_stability_established": False,
        "scope": "Instantaneous scalar-sector diagnostic for supplied n=1 trajectory; no mode evolution",
    }


def sample_trajectory(sol, potential, V0, kap, mass, decay, lam, redshifts):
    """Report sampled mass risks, never continuous stability or mode growth."""
    redshifts = list(redshifts)
    if len(redshifts) < 2 or not all(math.isfinite(z) and z >= 0 for z in redshifts):
        raise ValueError("Provide at least two finite nonnegative redshifts")
    if any(right <= left for left, right in zip(redshifts, redshifts[1:])):
        raise ValueError("Sample redshifts must be strictly increasing")
    rows = [
        {"z": float(z), **trajectory_diagnostic(
            sol, potential, V0, kap, mass, decay, lam, -math.log1p(z)
        )} for z in redshifts
    ]
    minimum = min(rows, key=lambda row: row["entropy_mass_squared_over_H2"])
    return {
        "rows": rows,
        "sample_count": len(rows),
        "negative_mass_samples": sum(row["negative_mass_risk"] for row in rows),
        "minimum_sample": minimum,
        "maximum_redshift_gap": max(b - a for a, b in zip(redshifts, redshifts[1:])),
        "scope": "Sampled instantaneous n=1 scalar-sector risks; unsampled intervals and mode growth untested",
        "full_stability_established": False,
    }


def derive():
    chi, theta, lam, direction = sp.symbols("chi theta lambda direction", real=True)
    V0, kap, mass = sp.symbols("V0 kappa m", real=True)
    decay = sp.symbols("F", positive=True)
    speed, turn = sp.symbols("sigma_dot turn_rate", real=True)
    metric = sp.diag(1, sp.exp(lam * chi))
    inverse = metric.inv()
    coordinates = (chi, theta)
    connection = {
        (i, j, k): sp.simplify(sum(
            inverse[i, l] * (
                sp.diff(metric[l, k], coordinates[j])
                + sp.diff(metric[l, j], coordinates[k])
                - sp.diff(metric[j, k], coordinates[l])
            ) / 2 for l in range(2)
        ))
        for i in range(2) for j in range(2) for k in range(2)
    }
    potential = V0 * sp.exp(-kap * chi) + mass**2 * decay**2 * (1 - sp.cos(theta / decay))
    hessian = sp.Matrix(2, 2, lambda i, j: sp.simplify(
        sp.diff(potential, coordinates[i], coordinates[j])
        - sum(connection[k, i, j] * sp.diff(potential, coordinates[k]) for k in range(2))
    ))
    tangent = sp.Matrix([sp.cos(direction), sp.exp(-lam * chi / 2) * sp.sin(direction)])
    normal = sp.Matrix([-sp.sin(direction), sp.exp(-lam * chi / 2) * sp.cos(direction)])
    projected = sp.simplify((normal.T * hessian * normal)[0])
    ricci = -lam**2 / 2
    geometric = speed**2 * ricci / 2
    entropy_mass = projected + 3 * turn**2 + geometric
    return {
        "metric": metric,
        "potential": potential,
        "covariant_hessian": hessian,
        "tangent": tangent,
        "normal": normal,
        "normal_norm_residual": sp.trigsimp((normal.T * metric * normal)[0] - 1),
        "orthogonality_residual": sp.trigsimp((normal.T * metric * tangent)[0]),
        "projected_hessian": projected,
        "geometric_mass_contribution": geometric,
        "entropy_mass_squared": entropy_mass,
    }


def calculate():
    result = derive()
    return {
        "scope": "Assumed n=1 two-field exponential-plus-cosine action; not the fitted n=3 one-field model",
        "covariant_hessian": [[str(value) for value in result["covariant_hessian"].row(i)] for i in range(2)],
        "normal_norm_residual": str(result["normal_norm_residual"]),
        "orthogonality_residual": str(result["orthogonality_residual"]),
        "projected_hessian": str(result["projected_hessian"]),
        "geometric_mass_contribution": str(result["geometric_mass_contribution"]),
        "entropy_mass_squared": str(result["entropy_mass_squared"]),
        "formula_scope": "Standard scalar-sector entropy mass: V_ss + 3*turn_rate**2 + sigma_dot**2*R_fs/2",
        "trajectory_requirements": "Nonzero field speed, actual tangent direction and turn rate; direction is undefined at rest",
        "interpretation": "Negative entropy mass is a growth-risk diagnostic, not a ghost or automatic cosmological exclusion",
        "missing": ["trajectory evaluation", "matter/radiation perturbations and gravitational constraints",
                    "isocurvature initial spectrum", "time-dependent mode growth and resonance"],
        "full_stability_established": False,
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
