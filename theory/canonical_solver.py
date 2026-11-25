"""Bounded reverse-exponential scalar/fluid component; not a unified solver."""

from copy import deepcopy
import math

from theory.coupled_perturbations import equations, integrate
from theory.effective_baseline import CanonicalPotential, CanonicalScalar


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite JSON number")
    return float(value)


def _object(value, keys, name):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f"{name} must contain exactly: {', '.join(keys)}")
    return value


def run(request: dict) -> dict:
    """Run a bounded, explicit initial-value calculation without fitting."""
    request = _object(request, ("model", "background", "perturbations"), "request")
    model = _object(request["model"], ("type", "amplitude", "coefficient", "slope"), "model")
    if model["type"] != "reverse_exponential":
        raise ValueError("Only the reverse_exponential potential is supported")
    amplitude = _number(model["amplitude"], "amplitude")
    coefficient = _number(model["coefficient"], "coefficient")
    slope = _number(model["slope"], "slope")
    if min(amplitude, coefficient, slope) <= 0:
        raise ValueError("Potential parameters must be positive")

    def exponential(field):
        return amplitude * coefficient * math.exp(-slope * field)

    potential = CanonicalPotential(
        lambda field: amplitude - exponential(field),
        lambda field: slope * exponential(field),
        lambda field: -slope**2 * exponential(field),
    )
    background_keys = ("matter_today", "radiation_today", "initial_N", "final_N",
                       "initial_field", "initial_field_prime")
    background = _object(request["background"], background_keys, "background")
    values = {key: _number(background[key], key) for key in background_keys}
    if not -10 <= values["initial_N"] < values["final_N"] <= 0:
        raise ValueError("Bounded component requires -10 <= initial_N < final_N <= 0")
    config = CanonicalScalar(potential, **values)

    perturbations = _object(request["perturbations"],
                            ("initial_state", "k_over_Href", "sample_N"), "perturbations")
    k = _number(perturbations["k_over_Href"], "k_over_Href")
    if not 0 < k <= 200:
        raise ValueError("Bounded component requires 0 < k_over_Href <= 200")
    initial = perturbations["initial_state"]
    if not isinstance(initial, list) or len(initial) != 7:
        raise ValueError("initial_state must contain seven numbers")
    initial = [_number(value, "initial_state") for value in initial]
    samples = perturbations["sample_N"]
    if not isinstance(samples, list) or not 1 <= len(samples) <= 128:
        raise ValueError("sample_N must contain between 1 and 128 epochs")
    samples = [_number(value, "sample_N") for value in samples]
    if (any(not config.initial_N <= N <= config.final_N for N in samples)
            or any(right <= left for left, right in zip(samples, samples[1:]))):
        raise ValueError("sample_N must be strictly increasing and within the interval")

    solution = integrate(config, initial, k, rtol=1e-12, atol=1e-18)
    rows = []
    for N in samples:
        field, prime = solution.background.sol(N)
        h2, _ = config.background(N, field, prime)
        state = solution.sol(N)
        _, constraint = equations(config, solution.background, N, state, k)
        rows.append({"N": N, "field": float(field), "field_prime": float(prime),
                     "H_over_Href": math.sqrt(h2), "state": state.tolist(),
                     "density_constraint": constraint})
    return {
        "status": "ok",
        "source": r"theory\canonical_solver.py",
        "contract_version": 1,
        "assumptions": ["single canonical scalar", "uncoupled dust and perfect radiation",
                        "Newtonian gauge; zero anisotropic stress", "reduced Planck units"],
        "inputs": deepcopy(request),
        "results": rows,
        "limitations": ["no five-field or observer coupling", "no Boltzmann hierarchy or fitting",
                        "momentum constraint is imposed, not independently tested",
                        "sampled constraint residuals do not establish full stability"],
    }


if __name__ == "__main__":
    import json
    import sys

    json.dump(run(json.load(sys.stdin)), sys.stdout, allow_nan=False)
    print()
