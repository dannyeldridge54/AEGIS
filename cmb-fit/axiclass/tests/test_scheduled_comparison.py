import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


spec = importlib.util.spec_from_file_location(
    "scheduled_comparison", Path(__file__).resolve().parents[1] / "scheduled_comparison.py")
job = importlib.util.module_from_spec(spec)
spec.loader.exec_module(job)


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def setup(tmp_path):
    cmb = tmp_path / "cmb-fit"
    ref = cmb / "results" / "restarts" / "reference"
    snapshot = tmp_path / "snapshot"
    builds = tmp_path / "builds"
    solver = builds / "AxiCLASS_nlfix" / "python" / "build" / "lib" / "classy.so"
    packages = tmp_path / "packages"
    data = packages / "data" / "survey" / "data.txt"
    paths = {
        "runner": cmb / "axiclass" / "early_late_spa.py",
        "patch": cmb / "axiclass" / "nlfix" / "patch_nlfix.py",
        "driver": snapshot / "clean_cosmology_benchmark.py",
        "reviewer": snapshot / "review_clean_benchmark.py",
        "classy": solver,
    }
    for path in [*paths.values(), data]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
    protocol = {f"{key}_sha256": job.sha256(path) for key, path in paths.items()}
    protocol.update(classy=str(solver), models=["LCDM", "w0wa", "Late Twist"])
    put(ref / "protocol.json", protocol)
    put(ref / "post_review_protocol.json", {
        "reviewer_sha256": protocol["reviewer_sha256"],
        "review_driver_sha256": protocol["driver_sha256"],
        "review_runner_sha256": protocol["runner_sha256"]})
    for gate in ("null_gate", "spectra_gate", "parameter_routing_gate"):
        put(ref / f"{gate}.json", {"passed": True})
    put(ref / "likelihood_manifest.json",
        [{"path": str(data), "bytes": data.stat().st_size, "sha256": job.sha256(data)}])
    return SimpleNamespace(reference=str(ref), snapshot=str(snapshot),
                           output=str(ref.with_name("scheduled")), builds=str(builds),
                           packages=str(packages), job_dir=str(tmp_path / "job"), run=False)


def preflight(args):
    return job.preflight(args.reference, args.snapshot, args.output, args.builds, args.packages)


def test_frozen_inputs_pass_without_fitting(setup):
    assert preflight(setup)["files_checked"] == 6
    assert not Path(setup.output).exists()


def test_changed_input_blocks(setup):
    (Path(setup.snapshot) / "clean_cosmology_benchmark.py").write_bytes(b"changed")
    with pytest.raises(ValueError, match="drift"):
        preflight(setup)


def test_failed_gate_blocks(setup):
    put(Path(setup.reference) / "spectra_gate.json", {"passed": False})
    with pytest.raises(ValueError, match="prerequisite"):
        preflight(setup)


def test_reference_cannot_be_overwritten(setup):
    setup.output = setup.reference
    with pytest.raises(ValueError, match="separate sibling"):
        preflight(setup)


def test_wrong_build_or_packages_block(setup):
    setup.builds += "-wrong"
    with pytest.raises(ValueError, match="Build root"):
        preflight(setup)
    setup.builds = setup.builds.removesuffix("-wrong")
    setup.packages += "-wrong"
    with pytest.raises(ValueError, match="Package path"):
        preflight(setup)


def fake_lock(_path):
    from contextlib import nullcontext
    return nullcontext()


@pytest.fixture(autouse=True)
def no_real_process_checks(monkeypatch):
    monkeypatch.setattr(job, "active_comparisons", lambda: [])


@pytest.mark.parametrize("retained", ["archive", "marker"])
def test_existing_attempt_never_refits(setup, monkeypatch, retained):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    output = Path(setup.output)
    if retained == "archive":
        output.mkdir()
    else:
        put(output.parent / f".{output.name}.attempt.json", {"status": "interrupted"})
    monkeypatch.setattr(job, "run_logged", lambda *_: pytest.fail("Unexpected subprocess"))
    assert job.execute(setup)["status"] == "retained_attempt"


def test_failed_tests_never_start_or_mark_fit(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    def fail_tests(*_):
        raise job.subprocess.CalledProcessError(1, ["pytest"])
    monkeypatch.setattr(job, "run_logged", fail_tests)
    with pytest.raises(job.subprocess.CalledProcessError):
        job.execute(setup)
    output = Path(setup.output)
    assert not output.exists()
    assert not (output.parent / f".{output.name}.attempt.json").exists()


def test_fit_failure_is_preserved_and_not_retried(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    calls = []
    def fail_fit(command, *_):
        calls.append(command)
        if len(calls) == 2:
            raise job.subprocess.CalledProcessError(2, command)
    monkeypatch.setattr(job, "run_logged", fail_fit)
    with pytest.raises(job.subprocess.CalledProcessError):
        job.execute(setup)
    assert job.read_json(Path(setup.job_dir) / "failure.json")["status"] == "blocked"
    assert job.execute(setup)["status"] == "retained_attempt"
    assert len(calls) == 2


def test_review_failure_does_not_score_or_refit(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    calls = []
    def fail_review(command, *_):
        calls.append(command)
        if len(calls) == 3:
            assert "R.audit(directory)" in command[-1]
            assert "R.main" not in command[-1]
            raise job.subprocess.CalledProcessError(1, command)
    monkeypatch.setattr(job, "run_logged", fail_review)
    with pytest.raises(job.subprocess.CalledProcessError):
        job.execute(setup)
    assert len(calls) == 3


def test_active_fit_blocks_new_launch(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    monkeypatch.setattr(job, "active_comparisons", lambda: [123])
    setup.run = True
    with pytest.raises(RuntimeError, match="Existing comparison"):
        job.execute(setup)
    assert not Path(setup.job_dir).exists()


def test_pending_scorecard_is_not_completion(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    calls = []
    def pending_score(command, *_):
        calls.append(command)
        if len(calls) == 4:
            put(Path(setup.job_dir) / "scorecard.json", {"status": "pending"})
    monkeypatch.setattr(job, "run_logged", pending_score)
    with pytest.raises(ValueError, match="reviewed in-sample"):
        job.execute(setup)
    assert not (Path(setup.job_dir) / "completion.json").exists()


def test_reviewed_scorecard_completes_once(setup, monkeypatch):
    monkeypatch.setattr(job, "comparison_lock", fake_lock)
    setup.run = True
    calls = []
    def reviewed_score(command, *_):
        calls.append(command)
        if len(calls) == 4:
            put(Path(setup.job_dir) / "scorecard.json", {"status": "reviewed_in_sample"})
    monkeypatch.setattr(job, "run_logged", reviewed_score)
    assert job.execute(setup)["status"] == "reviewed_attempt"
    assert job.execute(setup)["status"] == "retained_attempt"
    assert len(calls) == 4


@pytest.mark.skipif(job.sys.platform != "linux", reason="WSL execution lock")
def test_cross_process_lock_blocks_overlap(tmp_path):
    lock = tmp_path / "lock"
    with job.comparison_lock(lock):
        with pytest.raises(RuntimeError, match="holds the lock"):
            with job.comparison_lock(lock):
                pytest.fail("Overlapping lock accepted")
