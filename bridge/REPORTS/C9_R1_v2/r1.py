import hashlib
import importlib.metadata
import importlib.util
import json
import math
import pathlib
import sys
import time
import traceback


ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT = ROOT / "r1-result-v2.json"
STARTED = ROOT / "r1-started-v2.json"
ENGINE_SHA = "32fc0710ac6ae7caa6a4436dd3801f35a0499039c936d210cacb4714a06ee178"
AUDIT_SHA = "e0fc222ac37c078de9c0b507091173b30b7e35dbf7b5f08b05fb98c34279a9de"
R0_PLAN_SHA = "1d21e7c5b39e87f8145b146d4c34c6b55c9377e866770f506ecd251247ab4bc4"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    with path.open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def write_exclusive(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def verify_admission():
    receipt = read_json(ROOT / "r1-lock-receipt-v2.json")
    require(receipt["case"] == "R1", "Receipt is not for R1")
    require(receipt["remote_verified"] is True, "Missing verified remote lock")
    commit = receipt["commit"]
    require(type(commit) is str and len(commit) == 40
            and all(c in "0123456789abcdef" for c in commit), "Invalid lock commit")
    required = {
        "r1.py", "invoke-r1.ps1", "r1-input-v2.json", "runtime-manifest-v2.json",
        "UFE_test_plan_C9_R1_v2.md", "UFE_test_plan_C9_R1_v2.md.sha256",
        "UFE_test_plan_C9_R1_v2_DEVIATIONS.md",
    }
    require(set(receipt["files"]) == required, "Incomplete or unexpected lock files")
    for name in sorted(required):
        require(digest(ROOT / name) == receipt["files"][name],
                "Locked file hash mismatch: " + name)
    plan_hash = receipt["files"]["UFE_test_plan_C9_R1_v2.md"]
    sidecar = (ROOT / "UFE_test_plan_C9_R1_v2.md.sha256").read_text(
        encoding="utf-8").strip()
    require(sidecar == plan_hash + "  UFE_test_plan_C9_R1_v2.md",
            "Plan sidecar does not bind the exact plan")
    for name, expected in {
        "ufe_pack.py": ENGINE_SHA,
        "flux-audit-source.md": AUDIT_SHA,
        "r0-plan-v1-source.md": R0_PLAN_SHA,
    }.items():
        require(digest(ROOT / name) == expected, "Source mismatch: " + name)
    require(sys.platform == "win32" and sys.version_info[:3] == (3, 12, 10),
            "Unadmitted platform or Python version")
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode,
            "Execution requires -I -B")
    runtime = read_json(ROOT / "runtime-manifest-v2.json")
    base = pathlib.Path(sys.base_prefix).resolve()
    require(digest(pathlib.Path(sys.executable)) == runtime["python_executable_sha256"],
            "Python executable mismatch")
    for item in runtime["files"]:
        relative = pathlib.PureWindowsPath(item["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                "Invalid runtime-relative path")
        require(digest(base.joinpath(*relative.parts)) == item["sha256"],
                "Runtime byte mismatch: " + item["path"])
    for name, version in runtime["versions"].items():
        require(importlib.metadata.version(name) == version,
                "Package version mismatch: " + name)
    return receipt


def main(result):
    receipt = verify_admission()
    inputs = read_json(ROOT / "r1-input-v2.json")
    require(inputs["case"] == "R1" and inputs["protocol"] == "C9-v2",
            "Wrong case or protocol")
    require(inputs["step_sizes"] == [1e-3, 3e-4, 1e-4], "Unadmitted FD steps")
    require(inputs["variants"] == ["candidate", "null_b_f_0"], "Unadmitted cases")
    require(len(inputs["coordinates"]) == 4, "Expected four real coordinates")
    reference = inputs["matching"]["m0_squared"]
    require(type(reference) is float and reference == 11.566718599357344,
            "Changed analytic reference")
    require(inputs["model"]["a"] == 0.0
            and inputs["model"]["W"] == 0.0
            and inputs["model"]["DW"] == 0.0
            and inputs["model"]["omitted_sector_or_uplift"] is False,
            "Unadmitted local model")
    write_exclusive(STARTED, {
        "case": "R1", "lock_commit": receipt["commit"],
        "input_sha256": digest(ROOT / "r1-input-v2.json"),
        "harness_sha256": digest(pathlib.Path(__file__)),
        "runtime_manifest_sha256": digest(ROOT / "runtime-manifest-v2.json"),
    })

    import numpy as np
    import scipy
    import mpmath as mp

    mp.mp.dps = 30
    require(np.__version__ == "2.5.4" and scipy.__version__ == "1.18.1"
            and mp.__version__ == "1.3.0", "Imported package version mismatch")
    spec = importlib.util.spec_from_file_location("r1_pinned_ufe_pack", ROOT / "ufe_pack.py")
    require(spec is not None and spec.loader is not None, "Cannot load pinned engine")
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    fitter, tester = engine.TOOLS["ufe_flux_mass"][2:4]
    require(callable(fitter) and callable(tester), "Missing flux fitter/tester")

    height = math.sqrt(3) / 2
    k0 = -math.log(3)
    kuu = inputs["model"]["KUUinv"]
    kss = inputs["model"]["KSSinv"]
    metric = np.diag(inputs["model"]["real_metric_diagonal"])
    require(metric.shape == (4, 4) and np.isfinite(metric).all(), "Invalid metric")
    require(np.array_equal(metric, (2 / 3) * np.eye(4)), "Changed declared real metric")
    require(kuu == 3.0 and kss == 3.0, "Changed inverse Kahler metric")
    require(abs(kuu - 4 * height**2) <= 1e-12
            and abs(kss - 4 * height**2) <= 1e-12
            and abs(k0 + math.log(4 * height**2)) <= 1e-12,
            "Inconsistent tree geometry")
    cholesky = np.linalg.cholesky(metric)
    metric_eigenvalues = np.linalg.eigvalsh(metric)
    require(np.isfinite(metric_eigenvalues).all() and min(metric_eigenvalues) > 0,
            "Metric is not positive definite")
    limits = inputs["limits"]
    result.update({
        "lock_commit": receipt["commit"],
        "input_sha256": digest(ROOT / "r1-input-v2.json"),
        "source_sha256": ENGINE_SHA,
        "harness_sha256": digest(pathlib.Path(__file__)),
        "reference_eigenvalue": reference,
        "metric": metric.tolist(),
        "metric_eigenvalues": metric_eigenvalues.tolist(),
        "cholesky": cholesky.tolist(),
        "K0": k0, "KUUinv": kuu, "KSSinv": kss,
        "matching": {
            "b_f": math.sqrt(reference / 3), "conditions_spent": 1,
            "source": "fixed R0 analytic reference, not FD-fitted",
            "UV_derivation": False,
        },
        "versions": {
            "python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__,
            "mpmath": mp.__version__, "mpmath_dps": mp.mp.dps,
        },
        "fit_budget": inputs["fit_budget"], "limits": limits, "cases": [],
    })

    def finite_difference_case(name, coupling):
        cache = {}
        domain = {"minimum_imaginary_part": height,
                  "minimum_stencil_metric_diagonal": 1 / (2 * height**2)}

        def potential(point):
            key = tuple(float(v) for v in point)
            if key not in cache:
                require(all(math.isfinite(v) for v in key), "Nonfinite coordinate")
                imag_u, imag_s = height + key[1], height + key[3]
                require(imag_u > 0 and imag_s > 0, "Stencil leaves upper half-plane")
                gdiag = [1 / (2 * imag_u**2), 1 / (2 * imag_s**2)]
                require(all(math.isfinite(v) and v > 0 for v in gdiag),
                        "Invalid tree metric on stencil")
                domain["minimum_imaginary_part"] = min(
                    domain["minimum_imaginary_part"], imag_u, imag_s)
                domain["minimum_stencil_metric_diagonal"] = min(
                    domain["minimum_stencil_metric_diagonal"], *gdiag)
                du, ds = complex(*key[:2]), complex(*key[2:])
                dwu, dws = -coupling * ds, -coupling * du
                value = math.exp(k0) * (kuu * abs(dwu)**2 + kss * abs(dws)**2)
                require(math.isfinite(value), "Nonfinite quadratic potential")
                cache[key] = value
            return cache[key]

        rows = []
        origin = np.zeros(4)
        center = potential(origin)
        for h in inputs["step_sizes"]:
            gradient = np.zeros(4)
            hessian = np.zeros((4, 4))
            for i in range(4):
                ei = np.zeros(4)
                ei[i] = h
                fp, fm = potential(ei), potential(-ei)
                gradient[i] = (fp - fm) / (2 * h)
                hessian[i, i] = (fp - 2 * center + fm) / h**2
                for j in range(i):
                    ej = np.zeros(4)
                    ej[j] = h
                    value = (potential(ei + ej) - potential(ei - ej)
                             - potential(-ei + ej) + potential(-ei - ej)) / (4 * h**2)
                    hessian[i, j] = hessian[j, i] = value
            whitened = np.linalg.solve(cholesky, hessian)
            whitened = np.linalg.solve(cholesky, whitened.T).T
            require(np.isfinite(hessian).all() and np.isfinite(gradient).all()
                    and np.isfinite(whitened).all(), "Nonfinite Hessian or gradient")
            require(np.array_equal(hessian, hessian.T)
                    and np.allclose(whitened, whitened.T, rtol=0, atol=1e-12),
                    "Nonsymmetric Hessian or whitened matrix")
            eigenvalues = np.linalg.eigvalsh(whitened)
            require(eigenvalues.shape == (4,) and np.isfinite(eigenvalues).all(),
                    "Invalid full four-real spectrum")
            rows.append({
                "h": h, "gradient": gradient.tolist(), "hessian": hessian.tolist(),
                "whitened_hessian": whitened.tolist(), "eigenvalues": eigenvalues.tolist(),
            })

        args = {"K": k0, "KUUinv": kuu, "KSSinv": kss, "b": coupling}
        engine_mass = fitter(args)
        require(type(engine_mass) in (int, float) and math.isfinite(engine_mass),
                "Nonfinite engine mass")
        engine_test = tester(args, engine_mass)
        require(type(engine_test) is bool, "Nonboolean engine tester result")
        expected = reference if name == "candidate" else 0.0
        engine_error = abs(engine_mass - expected)
        engine_limit = limits["engine_reference_scale"] * max(1.0, reference)
        all_eigenvalues = [v for row in rows for v in row["eigenvalues"]]
        margin = limits["positive_margin_scale"] * max(
            1.0, max(abs(v) for v in all_eigenvalues))
        gradient_max = max(abs(v) for row in rows for v in row["gradient"])
        gradient_limit = limits["gradient_scale"] * max(1.0, reference)
        spread = max(
            max(row["eigenvalues"][i] for row in rows)
            - min(row["eigenvalues"][i] for row in rows) for i in range(4)) / reference
        checks = {"stationarity": gradient_max <= gradient_limit,
                  "engine_reference": engine_error <= engine_limit,
                  "engine_tester": engine_test}
        details = {
            "name": name, "b_f": coupling, "rows": rows, "domain": domain,
            "unique_stencil_points": len(cache), "gradient_inf_max": gradient_max,
            "gradient_limit": gradient_limit, "mass_margin": margin,
            "inter_h_spread_relative": spread, "engine_arguments": args,
            "engine_mass": engine_mass, "engine_reference_error": engine_error,
            "engine_reference_limit": engine_limit, "engine_tester": engine_test,
        }
        if name == "candidate":
            relative_error = max(abs(v - reference) / reference for v in all_eigenvalues)
            checks.update({
                "relative_error": relative_error <= limits["candidate_relative_error"],
                "inter_h_spread": spread <= limits["candidate_inter_h_spread_relative"],
                "strict_positivity": min(all_eigenvalues) > margin,
            })
            details["relative_error_max"] = relative_error
            verdict = "NOT STABLE locally" if min(all_eigenvalues) < -margin else (
                "STABLE locally CONDITIONAL" if all(checks.values()) else "UNCLEAR")
        else:
            maximum = max(abs(v) for v in all_eigenvalues)
            null_limit = limits["null_eigenvalue_scale"] * max(1.0, reference)
            checks["massless_null"] = maximum <= null_limit
            details.update({"max_absolute_eigenvalue": maximum, "null_limit": null_limit})
            verdict = "MASSLESS locally; not strictly stable" if all(checks.values()) else "UNCLEAR"
        details.update({"checks": checks, "local_verdict": verdict,
                        "numerical_admission": all(checks.values())})
        return details

    for name in inputs["variants"]:
        coupling = math.sqrt(reference / 3) if name == "candidate" else 0.0
        result["cases"].append(finite_difference_case(name, coupling))
    result["views"] = {
        "geometry_metric": {
            "status": "positive tree metric locally; CONDITIONAL symmetry",
            "scope": "two independent complex local fields at rho, not a global modular action",
        },
        "field_space_masses": result["cases"][0]["local_verdict"],
        "data_bounds": {
            "status": "UNCLEAR",
            "reason": "No common physical action, UV realization or data/observable binding",
            "likelihood_or_observational_fit_run": False,
        },
        "loom": {
            "status": "placement metadata only",
            "placement": "mandatory U plus independent S through the declared flux-local bridge",
            "physical_fractal_or_stability_claim": False,
        },
    }
    result["overall"] = "UNCLEAR"
    result["endpoint_or_cut"] = False
    result["global_potential_retained"] = False
    result["physical_S_YFORK2_Weave_identification"] = False
    result["numerical_admission"] = all(row["numerical_admission"] for row in result["cases"])
    if not result["numerical_admission"]:
        result["error"] = {
            "type": "NumericalAdmissionFailure",
            "message": "A predeclared numerical or engine check failed; no retuning or rerun.",
            "failed_checks": {
                row["name"]: [name for name, passed in row["checks"].items() if not passed]
                for row in result["cases"] if not row["numerical_admission"]
            },
        }
        return 2
    return 0


if OUTPUT.exists() or STARTED.exists():
    raise SystemExit("Refusing to overwrite an existing R1 attempt or result")
started_at = time.monotonic()
result = {"case": "R1", "overall": "UNCLEAR", "views": {}}
try:
    exit_code = main(result)
except Exception as exc:
    traceback.print_exc()
    result["error"] = {"type": type(exc).__name__, "message": str(exc)}
    exit_code = 1
result["runtime_seconds"] = time.monotonic() - started_at
result["exit_code"] = exit_code
write_exclusive(OUTPUT, result)
print(json.dumps(result, allow_nan=False))
raise SystemExit(exit_code)
