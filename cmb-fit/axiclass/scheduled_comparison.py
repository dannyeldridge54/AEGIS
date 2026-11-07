"""Run one preserved, test-gated comparison on the existing WSL environment."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def read_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def preflight(reference, snapshot, output, builds, packages):
    reference, snapshot, output = map(lambda p: Path(p).resolve(),
                                     (reference, snapshot, output))
    cmb = reference.parents[2]
    if output.parent != reference.parent or output == reference:
        raise ValueError("Output must be a separate sibling of the reference archive")
    protocol = read_json(reference / "protocol.json")
    review = read_json(reference / "post_review_protocol.json")
    files = {
        cmb / "axiclass" / "early_late_spa.py": protocol["runner_sha256"],
        cmb / "axiclass" / "nlfix" / "patch_nlfix.py": protocol["patch_sha256"],
        snapshot / "clean_cosmology_benchmark.py": protocol["driver_sha256"],
        snapshot / "review_clean_benchmark.py": review["reviewer_sha256"],
        Path(protocol["classy"]): protocol["classy_sha256"],
    }
    if review["review_driver_sha256"] != protocol["driver_sha256"]:
        raise ValueError("Reviewer and driver provenance differ")
    if review["review_runner_sha256"] != protocol["runner_sha256"]:
        raise ValueError("Reviewer and adapter provenance differ")
    if Path(protocol["classy"]).resolve().parents[3] != (
            Path(builds).resolve() / "AxiCLASS_nlfix"):
        raise ValueError("Build root differs from the frozen solver")
    for gate in ("null_gate", "spectra_gate", "parameter_routing_gate"):
        if read_json(reference / f"{gate}.json").get("passed") is not True:
            raise ValueError(f"Failed reference prerequisite: {gate}")
    manifest = read_json(reference / "likelihood_manifest.json")
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("Missing likelihood provenance")
    data_root = Path(packages).resolve() / "data"
    if not any(data_root in Path(row["path"]).resolve().parents for row in manifest):
        raise ValueError("Package path differs from the recorded data")
    for row in manifest:
        path = Path(row["path"])
        if path.stat().st_size != row["bytes"]:
            raise ValueError(f"Input size drift: {path}")
        files[path] = row["sha256"]
    for path, expected in files.items():
        if sha256(path) != expected:
            raise ValueError(f"Fingerprint drift: {path}")
    return {"status": "preflight_passed", "reference": str(reference),
            "output": str(output), "files_checked": len(files),
            "models": protocol["models"],
            "scope": "Input provenance only; not a fit or scientific result"}


@contextmanager
def comparison_lock(path):
    if sys.platform != "linux":
        raise RuntimeError("Comparison execution requires WSL/Linux advisory locking")
    import fcntl
    with Path(path).open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another scheduled comparison holds the lock") from None
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def run_logged(command, environment, cwd, log):
    with Path(log).open("x", encoding="utf-8") as stream:
        subprocess.run(command, cwd=cwd, env=environment, stdout=stream,
                       stderr=subprocess.STDOUT, check=True)


def active_comparisons(proc=Path("/proc")):
    names = {"clean_cosmology_benchmark.py", "review_clean_benchmark.py",
             "scheduled_comparison.py"}
    active = []
    for process in proc.iterdir():
        if not process.name.isdigit() or int(process.name) == os.getpid():
            continue
        try:
            command = (process / "cmdline").read_bytes().split(b"\0")
        except FileNotFoundError:
            continue
        if any(Path(os.fsdecode(argument)).name in names for argument in command if argument):
            active.append(int(process.name))
    return active


def execute(args):
    reference, snapshot, output, job = (
        Path(p).resolve() for p in (args.reference, args.snapshot, args.output, args.job_dir))
    cmb = reference.parents[2]
    repo = cmb.parent
    output.parent.mkdir(parents=True, exist_ok=True)
    with comparison_lock(output.parent / ".scheduled_comparison.lock"):
        evidence = preflight(reference, snapshot, output, args.builds, args.packages)
        if not args.run:
            return evidence
        marker = output.parent / f".{output.name}.attempt.json"
        if marker.exists() or output.exists():
            return {"status": "retained_attempt", "output": str(output),
                    "scope": "No retry, overwrite or new fit; inspect review/failure evidence"}
        active = active_comparisons()
        if active:
            raise RuntimeError(f"Existing comparison processes block a new fit: {active}")
        job.mkdir(parents=True, exist_ok=False)
        env = dict(os.environ, TWIST_RESULTS=str(output),
                   TWIST_BUILDS=str(Path(args.builds).resolve()),
                   COBAYA_PACKAGES_PATH=str(Path(args.packages).resolve()),
                   OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                   MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1",
                   PYTHONPATH=os.pathsep.join((str(repo / "ufe-v2"), str(cmb / "axiclass"))))
        tests = [str(cmb / "axiclass" / "tests")]
        tests.extend(str(repo / "ufe-v2" / "tests" / name) for name in (
            "test_anomaly_report.py", "test_scanner_readiness.py",
            "test_matched_control.py", "test_v2.py"))
        write_new(job / "preflight.json", evidence)
        run_logged([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                    *tests, "--basetemp", str(job / "pytest")],
                   env, repo, job / "tests.log")
        # Persist the attempt before launching: a killed process must not refit next day.
        preflight(reference, snapshot, output, args.builds, args.packages)
        write_new(marker, {"output": str(output), "job_dir": str(job),
                           "policy": "One attempt only; interruption/failure requires a new decision"})
        try:
            run_logged([sys.executable, str(snapshot / "clean_cosmology_benchmark.py")],
                       env, repo, job / "fit.log")
            # A separate process uses the frozen reviewer's audit, never its auto-refit path.
            review_code = (
                "import os; from pathlib import Path; import review_clean_benchmark as R; "
                "directory=Path(os.environ['TWIST_RESULTS']); "
                "report=R.audit(directory); "
                "report['reviewer_sha256']=R.hashlib.sha256(Path(R.__file__).read_bytes()).hexdigest(); "
                "R.B.write(directory/'post_run_review.json',report); "
                "raise SystemExit(0 if report['passed'] else 1)"
            )
            review_env = dict(env, PYTHONPATH=os.pathsep.join((str(snapshot), env["PYTHONPATH"])))
            run_logged([sys.executable, "-c", review_code],
                       review_env, repo, job / "review.log")
            preflight(reference, snapshot, output, args.builds, args.packages)
            run_logged([sys.executable, str(cmb / "axiclass" / "comparison_scorecard.py"),
                        "--archive", str(output), "--output", str(job / "scorecard.json")],
                       env, repo, job / "scorecard.log")
            if read_json(job / "scorecard.json").get("status") != "reviewed_in_sample":
                raise ValueError("Scorecard did not establish a reviewed in-sample comparison")
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            failure = {"status": "blocked", "error": str(exc), "output": str(output)}
            write_new(job / "failure.json", failure)
            if output.is_dir() and not (output / "failure.json").exists():
                write_new(output / "failure.json", failure)
            raise
        result = {"status": "reviewed_attempt", "output": str(output),
                  "scorecard": str(job / "scorecard.json"),
                  "scope": "Matched in-sample comparison only; not microscopic theory validation"}
        write_new(job / "completion.json", result)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("reference", "snapshot", "output", "builds", "packages", "job-dir"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--run", action="store_true",
                        help="Run tests and at most one new fit; default checks provenance only")
    args = parser.parse_args()
    try:
        print(json.dumps(execute(args), indent=2, allow_nan=False))
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Scheduled comparison blocked: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
