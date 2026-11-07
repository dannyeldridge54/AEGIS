"""Run ten bounded regression review areas without fits or archive writes."""
import argparse
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


CHECKS = (
    ("Solver state, closure and failure propagation", ("test_spiral_numerics.py",)),
    ("Validation CLI exit contract", ("test_spiral_validation_cli.py",)),
    ("Independent baseline and analytic Lambda limit", ("test_effective_baseline.py",)),
    ("Covariant entropy projection and scope", ("test_coupled_stability.py",)),
    ("CLASS coverage and normalization", ("test_mirror_background.py",)),
    ("Scaling controls and extreme-angle precision", ("test_scaling_audit.py",)),
    ("Effective potential identities and claim limits", ("test_twist_potential_audit.py",)),
    ("Supergravity derivation and axion obstruction", ("test_bi_supergravity.py",)),
    ("QCD normalization and background dynamics", ("test_bi_qcd_axion.py", "test_bi_qcd_dynamics.py")),
    ("Conditional stellar weak-field limits", ("test_stellar_weak_field.py",)),
)


def summarize(report, checks=CHECKS):
    """Missing, skipped and failing evidence cannot receive a PASS."""
    cases = list(ET.parse(report).getroot().iter("testcase"))
    rows = []
    for title, files in checks:
        modules = {Path(name).stem for name in files}
        selected = [case for case in cases
                    if modules.intersection(case.get("classname", "").split("."))]
        represented = set().union(*(
            modules.intersection(case.get("classname", "").split(".")) for case in selected
        ))
        failed = sum(case.find("failure") is not None or case.find("error") is not None
                     for case in selected)
        skipped = sum(case.find("skipped") is not None for case in selected)
        status = "FAIL" if failed else (
            "BLOCKED" if represented != modules or skipped or not selected else "PASS"
        )
        rows.append((title, status, len(selected), failed, skipped))
    return rows


def run_review(timeout=120, checks=CHECKS):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Review timeout must be finite and positive")
    root = Path(__file__).resolve().parent.parent
    files = [str(Path("theory") / name) for _, names in checks for name in names]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory(prefix="aegis-numerical-review-") as temporary:
        report = Path(temporary) / "results.xml"
        command = [
            sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
            *files, "--junitxml", str(report), "--basetemp",
            str(Path(temporary) / "pytest"),
        ]
        print("Ten regression review areas; not ten presumed defects.")
        print("No fit, external data acquisition or full perturbation validation.")
        print("Command:", subprocess.list2cmdline(command), flush=True)
        try:
            result = subprocess.run(
                command, cwd=root, env=env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, errors="replace", timeout=timeout,
            )
        except subprocess.TimeoutExpired as error:
            print(f"BLOCKED: review exceeded {timeout:g} seconds.")
            if error.stdout:
                output = error.stdout
                print(output.decode(errors="replace") if isinstance(output, bytes) else output)
            return 2
        except OSError as error:
            print(f"BLOCKED: could not run review: {error}")
            return 2
        try:
            rows = summarize(report, checks)
        except (OSError, ET.ParseError) as error:
            print(f"BLOCKED: missing or invalid regression evidence: {error}")
            print(result.stdout)
            return 2
        print("\n# | Status | Tests | Failures | Skips | Review area")
        for index, (title, status, count, failures, skips) in enumerate(rows, 1):
            print(f"{index} | {status} | {count} | {failures} | {skips} | {title}")
        passed = result.returncode == 0 and all(row[1] == "PASS" for row in rows)
        if not passed:
            print(f"\nReview did not pass (pytest exit {result.returncode}).")
        print(result.stdout)
        print("Full perturbation evolution and microscopic matching remain unresolved.")
        return 0 if passed else (1 if result.returncode == 1 else 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=120,
                        help="Maximum pytest runtime in seconds (default: 120)")
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and positive")
    return run_review(args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
