"""Fingerprint a benchmark and score reviewed, matched likelihood minima only."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import itertools
import json
import math
from pathlib import Path
import platform


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint(path, role):
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"File changed during fingerprinting: {path}")
    return {"path": str(path), "role": role, "bytes": after.st_size,
            "sha256": digest.hexdigest()}


def finite(value):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError(f"Invalid numeric score input: {value!r}")
    return value


def software_versions():
    versions = {"python": platform.python_version()}
    for name in ("cobaya", "numpy", "scipy", "Py-BOBYQA"):
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "Not installed as distribution metadata in this interpreter"
    return versions


def validation_errors(name, result, validation, accuracy, reviewed):
    """Check numerical evidence rather than trusting summary pass flags alone."""
    errors = []
    chi = finite(validation["chi2"])
    if abs(chi - finite(result["minimum"]["chi2"])) >= .02:
        errors.append(f"Saved/reproduced chi-square mismatch: {name}")
    minima = validation.get("restart_minima")
    good = []
    if not isinstance(minima, dict) or len(minima) != 4:
        errors.append(f"Expected four restart records: {name}")
    else:
        for value in minima.values():
            if (not isinstance(value, (list, tuple)) or len(value) != 2
                    or type(value[1]) is not bool):
                errors.append(f"Malformed restart record: {name}")
                continue
            objective = finite(value[0])
            if value[1]:
                good.append(2 * objective)
    spread = max(good) - min(good) if good else None
    if len(good) < 2 or spread >= .1:
        errors.append(f"Restart evidence does not meet gate: {name}")
    if good and abs(min(good) - chi) >= .02:
        errors.append(f"Restart best point differs from saved minimum: {name}")
    reported_spread = finite(validation["restart_spread_chi2"])
    if spread is not None and abs(reported_spread - spread) > 1e-8:
        errors.append(f"Restart spread summary mismatch: {name}")
    shift = finite(accuracy["dense_accuracy_shift"])
    if abs(shift) >= .02 or abs(finite(accuracy["chi2"]) - chi) >= .02:
        errors.append(f"Dense accuracy evidence does not meet gate: {name}")
    if abs(finite(accuracy["dense_chi2_at_saved_minimum"]) - chi - shift) > 1e-8:
        errors.append(f"Dense shift summary mismatch: {name}")
    if reviewed is not None:
        if (abs(finite(reviewed["chi2"]) - chi) >= .02
                or abs(finite(reviewed["accuracy_shift"])) >= .02
                or abs(finite(reviewed["dense_chi2"]) - finite(reviewed["chi2"])
                       - finite(reviewed["accuracy_shift"])) > 1e-8
                or reviewed.get("accuracy_passed") is not True
                or reviewed["restarts"].get("passed") is not True
                or reviewed["restarts"].get("successful_restarts") != len(good)
                or (spread is not None and
                    abs(finite(reviewed["restarts"]["spread_chi2"]) - spread) > 1e-8)):
            errors.append(f"Independent model review mismatch: {name}")
    return errors


def pair_scores(rows):
    """Differences are candidate minus control; negatives favor the candidate."""
    pairs = []
    for control, candidate in itertools.combinations(rows, 2):
        first, second = control["minimum"], candidate["minimum"]
        domain = "chi2__benchmark_w0wa_domain"
        for point in (first, second):
            if domain in point and finite(point[domain]) != 0:
                raise ValueError("Nonzero hard-domain contribution at a claimed finite minimum")
        terms = {key for key in first if key.startswith("chi2__") and key != domain}
        if not terms or terms != {key for key in second if key.startswith("chi2__") and key != domain}:
            raise ValueError("Matched score requires identical per-likelihood contributions")
        for row in (control, candidate):
            total = finite(sum(finite(row["minimum"][key]) for key in terms))
            if abs(total - finite(row["chi2"])) >= .02:
                raise ValueError("Per-likelihood sum does not reproduce reviewed chi-square")
            if type(row["sampled_parameters"]) is not int or row["sampled_parameters"] <= 0:
                raise ValueError("Missing explicit fitted parameter count")
        delta = finite(finite(candidate["chi2"]) - finite(control["chi2"]))
        shared = {}
        for key in sorted(first.keys() & second.keys()):
            if key.startswith(("chi2", "minuslog", "weight")):
                continue
            if isinstance(first[key], (int, float)) and isinstance(second[key], (int, float)):
                shared[key] = finite(finite(second[key]) - finite(first[key]))
        pairs.append({
            "control": control["name"], "candidate": candidate["name"],
            "delta_chi2": delta,
            "delta_aic": finite(delta + 2 * (candidate["sampled_parameters"] - control["sampled_parameters"])),
            "delta_chi2_by_likelihood": {key: finite(finite(second[key]) - finite(first[key]))
                                         for key in sorted(terms)},
            "shared_bestpoint_differences": shared,
            "interpretation": "In-sample likelihood/AIC only; differences have no posterior error bars."
        })
    return pairs


def build_scorecard(archive):
    archive = Path(archive).resolve()
    evidence_paths = set(archive.glob("*.json"))
    catalog = [fingerprint(Path(__file__).resolve(), "scorecard_source")]
    catalog.extend(fingerprint(path, "benchmark_evidence") for path in sorted(evidence_paths))
    protocol = read_json(archive / "protocol.json")
    names = protocol["models"]
    if not isinstance(names, list) or len(names) != 3 or len(set(names)) != 3:
        raise ValueError("Expected three distinct declared comparison models")
    if any(not isinstance(name, str) or Path(name).name != name or "/" in name or "\\" in name
           for name in names):
        raise ValueError("Invalid model name")
    errors = []
    manifest = read_json(archive / "likelihood_manifest.json")
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("A nonempty declared likelihood manifest is required")
    for entry in manifest:
        item = fingerprint(Path(entry["path"]), "likelihood_source_or_data")
        catalog.append(item)
        if item["sha256"] != entry["sha256"] or item["bytes"] != entry["bytes"]:
            errors.append(f"Likelihood fingerprint drift: {item['path']}")
    solver = fingerprint(Path(protocol["classy"]), "solver_binary")
    catalog.append(solver)
    if solver["sha256"] != protocol["classy_sha256"]:
        errors.append("Solver fingerprint drift")
    axi = archive.parents[2] / "axiclass"
    for key, path in (("runner_sha256", axi / "early_late_spa.py"),
                      ("patch_sha256", axi / "nlfix" / "patch_nlfix.py")):
        item = fingerprint(path, "solver_adapter_or_patch")
        catalog.append(item)
        if item["sha256"] != protocol[key]:
            errors.append(f"Source fingerprint drift: {path}")
    pending = []
    reviews = {}
    for gate in ("null_gate", "spectra_gate", "parameter_routing_gate", "post_run_review"):
        path = archive / f"{gate}.json"
        if not path.exists():
            pending.append(gate)
        else:
            evidence = read_json(path)
            if evidence.get("passed") is not True:
                errors.append(f"Failed gate: {gate}")
            if gate == "post_run_review":
                models = evidence.get("models", [])
                if (not isinstance(models, list) or len(models) != len(names)
                        or any(not isinstance(row, dict) or row.get("name") not in names for row in models)
                        or len({row["name"] for row in models}) != len(names)):
                    errors.append("Independent review does not cover exactly the declared models")
                else:
                    reviews = {row["name"]: row for row in models}
    for marker in ("failure.json", "post_run_review_failure.json",
                   "interruption_parameter_routing.json"):
        if (archive / marker).exists():
            errors.append(f"Failure/interruption marker: {marker}")
    rows = []
    likelihood_settings = None
    for name in names:
        paths = [archive / f"{prefix}_{name}.json"
                 for prefix in ("cmp", "validation", "accuracy", "config")]
        if not all(path.exists() for path in paths):
            pending.append(name)
            continue
        result, validation, accuracy, config = map(read_json, paths)
        settings = {key: value for key, value in config["likelihood"].items()
                    if key != "benchmark_w0wa_domain"}
        if not settings:
            errors.append(f"No observational likelihood settings: {name}")
        contribution_names = {
            key[len("chi2__"):] for key in result["minimum"]
            if key.startswith("chi2__") and key != "chi2__benchmark_w0wa_domain"
        }
        if contribution_names != set(settings):
            errors.append(f"Saved likelihood contributions do not match configuration: {name}")
        if likelihood_settings is None:
            likelihood_settings = settings
        elif settings != likelihood_settings:
            errors.append(f"Observational likelihood settings differ: {name}")
        if validation.get("convergence_resolved") is not True:
            errors.append(f"Restart convergence unresolved: {name}")
        if accuracy.get("best_point_accuracy_resolved") is not True:
            errors.append(f"Dense accuracy unresolved: {name}")
        if config["sampler"]["minimize"].get("ignore_prior") is not True:
            errors.append(f"Objective is not likelihood-only: {name}")
        chi = finite(validation["chi2"])
        errors.extend(validation_errors(name, result, validation, accuracy, reviews.get(name)))
        rows.append({"name": name, "chi2": chi,
                     "sampled_parameters": validation["sampled_parameters"],
                     "restart_spread_chi2": validation["restart_spread_chi2"],
                     "dense_accuracy_shift": accuracy["dense_accuracy_shift"],
                     "minimum": result["minimum"]})
    for item in catalog:
        current = fingerprint(Path(item["path"]), item["role"])
        if (current["sha256"], current["bytes"]) != (item["sha256"], item["bytes"]):
            errors.append(f"Evidence changed during scorecard capture: {item['path']}")
    if set(archive.glob("*.json")) != evidence_paths:
        errors.append("Benchmark evidence file set changed during scorecard capture")
    status = "blocked" if errors else "pending" if pending else "reviewed_in_sample"
    pairs = pair_scores(rows) if status == "reviewed_in_sample" else []
    identity = [{"path": item["path"], "role": item["role"], "bytes": item["bytes"],
                 "sha256": item["sha256"]} for item in catalog]
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "archive": str(archive), "status": status, "errors": errors, "pending": pending,
        "protocol": protocol, "catalog": catalog,
        "software_versions": software_versions(),
        "catalog_sha256": hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest(),
        "models": rows, "pairs": pairs,
        "scoring_available": ["paired chi-square", "paired AIC", "per-likelihood differences",
                              "shared bestpoint differences", "restart spread", "dense accuracy shift"]
                             if status == "reviewed_in_sample" else [],
        "scoring_pending": [] if status == "reviewed_in_sample" else
            ["Paired scores require complete, unchanged evidence and passed independent review."],
        "scoring_unavailable": {
            "BIC": "No justified effective data count supplied.",
            "Bayes_factor": "No normalized-prior nested evidence calculation.",
            "posterior_intervals": "No converged matched chains/profile intervals.",
            "detection_significance": "No calibrated test distribution or look-elsewhere correction.",
            "held_out_score": "No predeclared independent test evaluated.",
            "full_shear_or_local_gravity": "No validated likelihood in this suite."
        },
        "limitations": ["No claim of superiority or microscopic torsion detection.",
                        "Catalog covers declared likelihood inputs, solver and JSON evidence, not every environment file.",
                        "Frozen-driver provenance relies on the independent reviewer; this utility does not locate its source.",
                        "No refitting, observational downloads or active-archive writes performed."]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    archive, output = args.archive.resolve(), args.output.resolve()
    if output == archive or archive in output.parents:
        raise ValueError("Scorecard output must be outside the active archive")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite scorecard: {output}")
    report = build_scorecard(archive)
    content = json.dumps(report, indent=2, allow_nan=False)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(content)
    print(f"{report['status']}: {output}")
    if report["errors"]:
        raise RuntimeError("; ".join(report["errors"]))


if __name__ == "__main__":
    main()
