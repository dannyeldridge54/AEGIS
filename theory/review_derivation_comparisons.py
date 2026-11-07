"""Review numerical, independent-derivation and comparison contracts offline."""
import argparse
import math
from pathlib import Path
import sys

if __package__:
    from .review_numerical import run_review
else:
    from review_numerical import run_review


ROOT = Path(__file__).resolve().parent.parent
CHECKS = (
    ("Numerical solver and closure contracts",
     ("test_spiral_numerics.py", "test_spiral_validation_cli.py")),
    ("Independent methods versus analytic Lambda background",
     ("test_effective_baseline.py", "test_effective_modes.py", "test_coupled_perturbations.py",
      "test_primordial_conventions.py", "test_neutrino_contract.py",
      "test_neutrino_hierarchy.py", "test_matter_hierarchy.py")),
    ("Scaling derivative versus finite differences and controls",
     ("test_scaling_audit.py",)),
    ("Exact potential identities and microscopic obstruction",
     ("test_twist_potential_audit.py", "test_bi_supergravity.py")),
    ("Numerical versus symbolic covariant projection",
     ("test_coupled_stability.py",)),
    ("QCD evolution versus density replacement and CAMB expression",
     ("test_bi_qcd_axion.py", "test_bi_qcd_dynamics.py")),
    ("CLASS and observable interpolation contracts",
     ("test_mirror_background.py",
      str(ROOT / "cmb-fit" / "axiclass" / "tests" / "test_observable_outputs.py"))),
    ("Reproducible minima and saved objective consistency",
     tuple(str(ROOT / "cmb-fit" / "axiclass" / "tests" / name) for name in
           ("test_minimizer_guard.py", "test_save_objective.py"))),
    ("Paired scores, likelihood parity and evidence drift",
     (str(ROOT / "cmb-fit" / "axiclass" / "tests" / "test_comparison_scorecard.py"),)),
    ("Independent likelihood covariance and overlap controls",
     tuple(str(ROOT / "cmb-fit" / "axiclass" / "tests" / name) for name in
           ("test_chronometers.py", "test_observational_coverage.py"))),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=120,
                        help="Maximum pytest runtime in seconds (default: 120)")
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and positive")
    print("Comparison checks use temporary synthetic evidence, not live fit scores.")
    print("This does not establish real CLASS/CAMB agreement or a microscopic model.")
    return run_review(args.timeout, CHECKS)


if __name__ == "__main__":
    sys.exit(main())
