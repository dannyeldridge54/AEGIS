"""Dimensionless potential-shape audit; no microscopic or fractal inference."""
import json
import math


def shape(x, power):
    if not math.isfinite(x) or type(power) is not int or power not in (1, 3):
        raise ValueError("Use a finite dimensionless coordinate and power 1 or 3")
    return (2 * math.sin(x / 2)**2)**power


def normalized_potential(q, amplitude, decay, power):
    if not all(math.isfinite(v) for v in (q, amplitude, decay)) or amplitude <= 0 or decay <= 0:
        raise ValueError("Coordinate must be finite; amplitude and decay must be finite and positive")
    x = q / decay
    return shape(x, power)


def effective_exponent(x, power):
    """d ln(V)/d ln(x) on the positive first rising branch."""
    shape(x, power)
    if not 0 < x < math.pi:
        raise ValueError("Exponent requires 0 < x < pi on the rising branch")
    if x < 1e-4:
        # x*cot(x/2) avoids dividing by an underflowed half-angle.
        squared = x * x
        return power * (2 - squared / 6 - squared * squared / 360)
    return power * x / math.tan(x / 2)


def calculate():
    rows = []
    # Fixed illustrative coordinates and scale factor, not fitted to a pattern.
    factor = 2.0
    for power in (1, 3):
        for x in (0.01, 0.1, 0.5, 1.0):
            exponent = 2 * power
            ratio = shape(factor * x, power) / (factor**exponent * shape(x, power))
            rows.append({
                "power": power, "x": x,
                "effective_exponent": effective_exponent(x, power),
                "small_angle_exponent": exponent,
                "scale_factor": factor,
                "scaled_shape_ratio_to_power_law": ratio,
                "relative_scaling_residual": ratio - 1,
                "monomial_control_ratio": (factor * x)**exponent / (factor**exponent * x**exponent),
            })
    return {
        "scope": "Dimensionless shape tests of assumed n=1/n=3 cosine potentials; no cross-scale observations",
        "normalization": "x=q/F, excitation V/A=(1-cos(x))**n; independent constant offset excluded",
        "rows": rows,
        "interpretation": "Local small-angle power laws are ordinary Taylor limits, not evidence of a fractal",
        "normalization_scope": "Changing A and F collapses the assumed shape by definition; not a quantum-to-cosmological derivation",
        "fractal_established": False,
        "pi_or_fibonacci_scaling_established": False,
        "quantum_to_cosmological_matching_established": False,
        "missing": ["microscopic matching and running couplings",
                    "predefined dimensionless observable across scales",
                    "independent measurements and uncertainties",
                    "non-fractal statistical nulls and held-out predictions"],
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, allow_nan=False))
