import sympy as sp
import math
import json
import pytest

from theory import coupled_stability


def test_projection_basis_is_orthonormal():
    result = coupled_stability.derive()
    assert result["normal_norm_residual"] == 0
    assert result["orthogonality_residual"] == 0
    assert result["covariant_hessian"] == result["covariant_hessian"].T


def test_flat_metric_recovers_ordinary_hessian():
    result = coupled_stability.derive()
    chi, theta = sp.symbols("chi theta", real=True)
    lam = sp.symbols("lambda", real=True)
    expected = sp.hessian(result["potential"], (chi, theta))
    assert (result["covariant_hessian"].subs(lam, 0) - expected).applyfunc(sp.simplify) == sp.zeros(2)


def test_connection_changes_transverse_mass_even_at_cosine_minimum():
    result = coupled_stability.derive()
    chi, theta, lam, direction = sp.symbols("chi theta lambda direction", real=True)
    V0, kap, mass = sp.symbols("V0 kappa m", real=True)
    expected = mass**2 * sp.exp(-lam * chi) - lam * kap * V0 * sp.exp(-kap * chi) / 2
    actual = result["projected_hessian"].subs({theta: 0, direction: 0})
    assert sp.simplify(actual - expected) == 0


def test_geometric_mass_sign_and_turning_term():
    result = coupled_stability.derive()
    lam, speed, turn = sp.symbols("lambda sigma_dot turn_rate", real=True)
    assert result["geometric_mass_contribution"] == -lam**2 * speed**2 / 4
    assert sp.simplify(result["entropy_mass_squared"] - result["projected_hessian"]
                       - result["geometric_mass_contribution"]) == 3 * turn**2


def test_no_stability_verdict_without_trajectory_or_modes():
    result = coupled_stability.calculate()
    assert result["full_stability_established"] is False
    import json
    json.dumps(result, allow_nan=False)
    assert "undefined at rest" in result["trajectory_requirements"]
    assert "not the fitted n=3" in result["scope"]


def test_actual_bounded_trajectory_has_finite_consistent_mass_terms():
    from theory import spiral_w
    V0, sol, potential = spiral_w.closed(1, 1, 0.15)
    for N in (-math.log(3), -math.log(2), 0):
        result = coupled_stability.trajectory_diagnostic(
            sol, potential, V0, 1, 1, spiral_w.FDEC, spiral_w.LAM, N
        )
        assert result["entropy_mass_squared_over_H2"] == pytest.approx(
            result["projected_hessian_over_H2"] + result["turning_contribution_over_H2"]
            + result["geometric_contribution_over_H2"]
        )
        assert result["turning_contribution_over_H2"] >= 0
        assert result["geometric_contribution_over_H2"] <= 0
        assert result["full_stability_established"] is False


def test_static_lambda_solution_has_no_entropy_direction():
    from theory import spiral_w
    sol, potential = spiral_w.solve(1, 0, 0, 0)
    with pytest.raises(ValueError, match="undefined"):
        coupled_stability.trajectory_diagnostic(
            sol, potential, 1, 0, 0, spiral_w.FDEC, spiral_w.LAM, 0
        )


def test_diagnostic_cannot_mix_actions_or_potentials():
    from theory import spiral_w
    sol, potential = spiral_w.solve(1, 1, 1, 0.15)
    with pytest.raises(ValueError, match="parameters"):
        coupled_stability.trajectory_diagnostic(sol, potential, 2, 1, 1, spiral_w.FDEC, spiral_w.LAM, 0)
    with pytest.raises(ValueError, match="potential"):
        coupled_stability.trajectory_diagnostic(sol, lambda c, t: 1, 1, 1, 1, spiral_w.FDEC, spiral_w.LAM, 0)


def test_sampled_interval_preserves_scope_and_reports_coverage():
    from theory import spiral_w
    V0, sol, potential = spiral_w.closed(1, 1, 0.15)
    result = coupled_stability.sample_trajectory(
        sol, potential, V0, 1, 1, spiral_w.FDEC, spiral_w.LAM, [i / 20 for i in range(41)]
    )
    assert result["sample_count"] == 41
    assert result["maximum_redshift_gap"] == pytest.approx(0.05)
    assert result["minimum_sample"]["entropy_mass_squared_over_H2"] == min(
        row["entropy_mass_squared_over_H2"] for row in result["rows"]
    )
    assert result["full_stability_established"] is False
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("redshifts", [[], [0], [1, 0], [0, 0], [0, float("nan")], [-1, 0]])
def test_sampling_rejects_invalid_coverage(redshifts):
    with pytest.raises(ValueError):
        coupled_stability.sample_trajectory(None, None, 1, 1, 1, 1, 1, redshifts)


@pytest.mark.parametrize("lam", [0.0, -2 * math.sqrt(2 / 3), 0.5])
def test_numerical_projection_matches_independent_symbolic_derivation(lam):
    from theory import spiral_w
    V0, sol, potential = spiral_w.closed(1, 1, 0.15, lam=lam)
    expression = coupled_stability.derive()["projected_hessian"]
    for N in (-math.log(3), -math.log(2), 0):
        chi, cp, theta, tp = sol.sol(N)
        direction = math.atan2(math.exp(lam * chi / 2) * tp, cp)
        values = {"chi": chi, "theta": theta, "lambda": lam,
                  "direction": direction, "V0": V0, "kappa": 1,
                  "m": 1, "F": spiral_w.FDEC}
        expected = float(expression.subs({
            symbol: values[str(symbol)] for symbol in expression.free_symbols
        }))
        h2 = spiral_w.H2_of(sol, potential, N, lam)[0]
        report = coupled_stability.trajectory_diagnostic(
            sol, potential, V0, 1, 1, spiral_w.FDEC, lam, N
        )
        assert report["projected_hessian_over_H2"] == pytest.approx(
            expected / h2, rel=1e-10, abs=1e-12
        )
