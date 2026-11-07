"""Fresh same-build likelihood benchmark; preserves previous runs and fails closed."""
import copy
import hashlib
import inspect
import json
import math
import os
from pathlib import Path
import sys
import time
import numpy as np

AXI = Path("/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
sys.path.insert(0, str(AXI))
import early_late_spa as E

NAMES = (
    "ax_spa_lcdm_halofit_planckfull_nlfix",
    "ax_spa_w0wa_halofit_planckfull_nlfix",
    "ax_spa_latetwist_planckfull_nlfix",
)
SEED = 20261104
NUMERICS = {"tol_background_integration": 1e-10, "tol_perturbations_integration": 1e-8,
            "l_linstep": 10, "l_logstep": 1.02}
DENSE_NUMERICS = dict(NUMERICS, accurate_lensing=1, delta_l_max=1000, num_mu_minus_lmax=1000,
                      k_step_sub=.015, k_step_super=.0001, k_step_super_reduction=.1,
                      q_linstep=.2, perturbations_sampling_stepsize=.025)


def write(path, value):
    def native(value):
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
        raise TypeError(f"Unsupported JSON value: {type(value).__name__}")
    content = json.dumps(value, indent=2, allow_nan=False, default=native)
    with open(path, "x", encoding="utf-8") as f:
        f.write(content)


def config(name):
    # Fresh documented reference distributions, not imported CAMB or old fitted points.
    original = E._start_from_camb
    E._start_from_camb = lambda *_args: None
    try:
        info = E.make(name)
    finally:
        E._start_from_camb = original
    info["sampler"]["minimize"].update(best_of=4, seed=SEED, ignore_prior=True, max_evals=10000)
    info["theory"]["classytwist"]["extra_args"].update(NUMERICS)
    # ignore_prior drops external priors, so retain this hard physical domain in the likelihood.
    if "w0wa_bound" in info["prior"]:
        info["likelihood"]["benchmark_w0wa_domain"] = {"external": info["prior"].pop("w0wa_bound")}
    info["force"] = False
    return info


def evaluate(info, point):
    from cobaya.model import get_model
    info = copy.deepcopy(info)
    for key in ("sampler", "output", "resume", "force"):
        info.pop(key, None)
    with get_model(info) as model:
        sampled = list(model.parameterization.sampled_params())
        post = model.logposterior({k: point[k] for k in sampled}, cached=False)
        if not math.isfinite(post.logpost):
            raise RuntimeError("Non-finite uncached best-point evaluation")
        return float(-2 * sum(post.loglikes))


def spectrum_snapshot(info, point):
    from cobaya.model import get_model
    info = copy.deepcopy(info)
    for key in ("sampler", "output", "resume", "force"):
        info.pop(key, None)
    with get_model(info) as model:
        post = model.logposterior({k: point[k] for k in model.parameterization.sampled_params()}, cached=False)
        if not math.isfinite(post.logpost):
            raise RuntimeError("Nonfinite spectrum gate")
        solver = model.theory["classytwist"].classy
        k = np.geomspace(.001, 1., 200)
        cls = model.provider.get_Cl(ell_factor=False)
        return {"chi2": float(-2*sum(post.loglikes)),
                "pk": np.array([solver.pk(x, 0.) for x in k]),
                "pk_lin": np.array([solver.pk_lin(x, 0.) for x in k]),
                "tt": np.array(cls["tt"])[30:2501], "ee": np.array(cls["ee"])[30:2501]}


def spectrum_errors(first, second):
    return {key: float(np.max(np.abs(second[key]/first[key]-1)))
            for key in ("pk", "pk_lin", "tt", "ee")}


def likelihood_manifest(info):
    from cobaya.model import get_model
    cfg = copy.deepcopy(info)
    for key in ("sampler", "output", "resume", "force"):
        cfg.pop(key, None)
    data = Path(E.PACKAGES) / "data"
    roots = {data / "planck_2018_pliklite_native",
             data / "planck_supp_data_and_covmats" / "lensing" / "2018",
             data / "sn_data" / "PantheonPlus", data / "bao_data" / "desi_bao_dr2"}
    with get_model(cfg) as model:
        for likelihood in model.likelihood.values():
            roots.add(Path(inspect.getfile(type(likelihood))).parent)
    manifest = []
    for root in sorted(roots):
        if not root.is_dir():
            raise FileNotFoundError(f"Missing likelihood provenance directory: {root}")
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024*1024), b""):
                    digest.update(chunk)
            manifest.append({"path": str(path), "bytes": path.stat().st_size, "sha256": digest.hexdigest()})
    return manifest


def main():
    out = Path(E.OUT)
    if out.exists():
        raise FileExistsError(f"Refusing to reuse benchmark directory: {out}")
    out.mkdir(parents=True)
    (out / "chains").mkdir()
    E._maybe_coupled(NAMES[0])
    import classy
    write(out / "protocol.json", {
        "models": NAMES, "branch": "Existing effective one-field Late Twist, not full two-field theory",
        "seed": SEED, "best_of": 4, "max_evals_per_restart": 10000,
        "objective": "Likelihood minimum within existing priors; ignore_prior=True",
        "data": "Planck 2018 low-l, high-l lite and lensing + DESI DR2 + Pantheon+",
        "classy": classy.__file__,
        "classy_sha256": hashlib.sha256(Path(classy.__file__).read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256((AXI / "early_late_spa.py").read_bytes()).hexdigest(),
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "patch_sha256": hashlib.sha256((AXI / "nlfix" / "patch_nlfix.py").read_bytes()).hexdigest(),
        "numerics": NUMERICS, "dense_verification_numerics": DENSE_NUMERICS,
        "spectrum_gate": "Frozen/control relative spectra < 1e-4, k=0.001..1/Mpc at z=0 and ell=30..2500. Differential null chi2 stable within 0.02 under dense refinement.",
        "restart_gate": "At least two successful restarts and successful-minimum chi2 spread <0.1.",
        "null_gate": "Absolute frozen-field chi2 difference < 0.15 at original F=100,m=0.015. Accuracy and spectra convergence must also pass; a passing finite-field variant alone is insufficient.",
        "reproduction_gate": "Absolute uncached likelihood chi2 difference < 0.02",
        "limitations": "No claim of theory validation before spectra, restart spread, and held-out checks. BIC omitted without a justified effective data count.",
    })
    from cobaya.run import run
    E._guard_minimizer()
    results = []
    for index, name in enumerate(NAMES):
        info = config(name)
        if index == 2:
            # Undo AxiCLASS baseline centering for shared parameters to keep independent starts.
            control = config(NAMES[0])
            for key in control["params"]:
                if "ref" in control["params"][key] and key in info["params"]:
                    info["params"][key]["ref"] = copy.deepcopy(control["params"][key]["ref"])
        if index == 0:
            write(out / "likelihood_manifest.json", likelihood_manifest(info))
            null_point = {
                k: p["ref"]["loc"] for k, p in info["params"].items()
                if isinstance(p, dict) and isinstance(p.get("ref"), dict)
            }
            null_point["A_planck"] = 1.0
            reference_name = "ax_spa_lcdm_halofit_planckfull"
            write(out / f"cmp_{reference_name}.json", {"minimum": null_point, "purpose": "Unfitted null-test seed only"})
            frozen = config("ax_spa_latetwist_gF2m-1.824_planckfull_nlfix")
            frozen["theory"]["classytwist"]["extra_args"].update(f_axion=100.0, m_axion=0.015)
            first = spectrum_snapshot(info, null_point)
            second = spectrum_snapshot(frozen, null_point)
            chi_control, chi_frozen = first["chi2"], second["chi2"]
            delta = chi_frozen - chi_control
            write(out / "null_gate.json", {"control_chi2": chi_control, "frozen_chi2": chi_frozen,
                                         "difference": delta, "passed": abs(delta) < 0.15,
                                         "F": 100.0, "m": 0.015,
                                         "qualification": "Do not select alternative limits or accuracy settings solely to pass."})
            if abs(delta) >= 0.15:
                raise RuntimeError(f"Null gate failed: delta chi2={delta}; benchmark halted")
            dense_control, dense_frozen = copy.deepcopy(info), copy.deepcopy(frozen)
            for cfg in (dense_control, dense_frozen):
                cfg["theory"]["classytwist"]["extra_args"].update(DENSE_NUMERICS)
            dense_first = spectrum_snapshot(dense_control, null_point)
            dense_second = spectrum_snapshot(dense_frozen, null_point)
            dense_delta = dense_second["chi2"]-dense_first["chi2"]
            errors = spectrum_errors(first, second)
            dense_errors = spectrum_errors(dense_first, dense_second)
            spectra_ok = all(value < 1e-4 for value in [*errors.values(), *dense_errors.values()])
            differential_ok = abs(dense_delta-delta) < .02 and abs(dense_delta) < .15
            write(out / "spectra_gate.json", {"errors": errors, "dense_errors": dense_errors,
                  "dense_delta_chi2": dense_delta, "differential_null_stable": differential_ok,
                  "absolute_baseline_accuracy_shift": dense_first["chi2"]-chi_control,
                  "passed": spectra_ok and differential_ok,
                  "qualification": "This gate validates the null, not accuracy at fitted non-null points."})
            if not (spectra_ok and differential_ok):
                raise RuntimeError("Spectrum or differential-null convergence gate failed")
        started = time.time()
        archived_info = copy.deepcopy(info)
        archived_info["theory"]["classytwist"]["external"] = "early_late_spa._theory_class()"
        write(out / f"config_{name}.json", archived_info)
        _, sampler = run(info)
        E.save(name, time.time() - started, ignore_prior=True)
        result = json.loads((out / f"cmp_{name}.json").read_text())
        chi = evaluate(info, result["minimum"])
        if abs(chi - result["minimum"]["chi2"]) >= 0.02:
            raise RuntimeError(f"Uncached minimum did not reproduce for {name}")
        results.append({"run": name, "chi2": chi, "sampled_parameters": len(sampler.model.parameterization.sampled_params()),
                        "restart_minima": sampler.full_set_of_mins})
        minima = sampler.full_set_of_mins or {}
        successful = [2*float(value) for value, success in minima.values() if success]
        results[-1]["successful_restarts"] = len(successful)
        results[-1]["restart_spread_chi2"] = max(successful)-min(successful) if successful else None
        results[-1]["convergence_resolved"] = len(successful) >= 2 and max(successful)-min(successful) < .1
        write(out / f"validation_{name}.json", results[-1])
        print(f"Validated {name}: chi2={chi}", flush=True)
    baseline = results[0]
    for result in results:
        result["delta_chi2"] = result["chi2"] - baseline["chi2"]
        result["delta_aic"] = result["delta_chi2"] + 2 * (result["sampled_parameters"] - baseline["sampled_parameters"])
    write(out / "comparison.json", {"results": results, "status": "Preliminary fits; best-point accuracy and held-out validation pending"})
    for result in results:
        cfg = config(result["run"])
        cfg["theory"]["classytwist"]["extra_args"].update(DENSE_NUMERICS)
        saved = json.loads((out / f"cmp_{result['run']}.json").read_text())
        result["dense_chi2_at_saved_minimum"] = evaluate(cfg, saved["minimum"])
        result["dense_accuracy_shift"] = result["dense_chi2_at_saved_minimum"]-result["chi2"]
        result["best_point_accuracy_resolved"] = abs(result["dense_accuracy_shift"]) < .02
        write(out / f"accuracy_{result['run']}.json", result)
    write(out / "accuracy_comparison.json", {
        "results": results,
        "status": "Held-out validation pending; any unresolved restart/accuracy gate requires further optimization, not a preference claim.",
        "optimization_resolved": all(r["convergence_resolved"] and r["best_point_accuracy_resolved"] for r in results)})


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        out = Path(E.OUT)
        if out.exists() and not (out / "failure.json").exists():
            write(out / "failure.json", {"error": repr(exc)})
        raise
