import importlib.util
import json
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "comparison_scorecard", Path(__file__).resolve().parents[1] / "comparison_scorecard.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


def row(name, chi, count):
    return {"name": name, "chi2": chi, "sampled_parameters": count,
            "minimum": {"chi2__survey": chi, "chi2": chi, "H0": 67.}}


def test_paired_aic_includes_extra_parameters_and_flexible_control():
    pairs = score.pair_scores([row("LCDM", 100., 7), row("w0wa", 95., 9), row("AEGIS", 96., 9)])
    assert len(pairs) == 3
    assert pairs[1]["delta_chi2"] == -4.
    assert pairs[1]["delta_aic"] == 0.
    assert pairs[2]["delta_chi2"] == 1.
    assert pairs[2]["delta_aic"] == 1.


def test_mismatched_likelihood_or_total_rejected():
    first, second = row("LCDM", 100., 7), row("AEGIS", 95., 9)
    second["minimum"]["chi2__survey"] = 90.
    with pytest.raises(ValueError, match="sum"):
        score.pair_scores([first, second])
    del second["minimum"]["chi2__survey"]
    with pytest.raises(ValueError, match="identical"):
        score.pair_scores([first, second])

def test_zero_hard_domain_is_not_an_extra_observational_dataset():
    first, second = row("LCDM", 100., 7), row("w0wa", 95., 9)
    second["minimum"]["chi2__benchmark_w0wa_domain"] = 0.
    assert score.pair_scores([first, second])[0]["delta_chi2"] == -5.
    second["minimum"]["chi2__benchmark_w0wa_domain"] = 1.
    with pytest.raises(ValueError, match="domain"):
        score.pair_scores([first, second])


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True, "10"])
def test_invalid_scores_rejected(value):
    with pytest.raises(ValueError):
        score.finite(value)


@pytest.mark.parametrize("quantity", ["total", "delta", "shared", "component"])
def test_finite_score_inputs_cannot_export_overflow(quantity):
    first, second = row("LCDM", 100., 7), row("AEGIS", 100., 9)
    if quantity == "total":
        first["minimum"]["chi2__survey"] = 1e308
        first["minimum"]["chi2__extra"] = 1e308
        second["minimum"]["chi2__extra"] = 0.
    elif quantity == "delta":
        first, second = row("LCDM", -1e308, 7), row("AEGIS", 1e308, 9)
    elif quantity == "shared":
        first["minimum"]["H0"], second["minimum"]["H0"] = -1e308, 1e308
    else:
        first["chi2"] = second["chi2"] = 0.
        first["minimum"].update(chi2__survey=-1e308, chi2__extra=1e308)
        second["minimum"].update(chi2__survey=1e308, chi2__extra=-1e308)
    with pytest.raises(ValueError, match="Invalid numeric score input"):
        score.pair_scores([first, second])


def test_fingerprint_captures_bytes(tmp_path):
    path = tmp_path / "input.dat"
    path.write_bytes(b"data")
    initial = score.fingerprint(path, "test")
    assert initial["bytes"] == 4
    path.write_bytes(b"changed")
    assert score.fingerprint(path, "test")["sha256"] != initial["sha256"]


def test_pending_archive_never_gets_scores_and_drift_blocks(tmp_path):
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    archive.mkdir(parents=True)
    axi = tmp_path / "cmb-fit" / "axiclass"
    (axi / "nlfix").mkdir(parents=True)
    solver = tmp_path / "solver.so"
    solver.write_bytes(b"solver")
    runner = axi / "early_late_spa.py"
    runner.write_bytes(b"runner")
    patch = axi / "nlfix" / "patch_nlfix.py"
    patch.write_bytes(b"patch")
    protocol = {"models": ["LCDM", "w0wa", "AEGIS"], "classy": str(solver)}
    for key, path in (("classy_sha256", solver), ("runner_sha256", runner), ("patch_sha256", patch)):
        protocol[key] = score.fingerprint(path, "test")["sha256"]
    (archive / "protocol.json").write_text(json.dumps(protocol))
    data = tmp_path / "survey.dat"
    data.write_bytes(b"survey")
    (archive / "likelihood_manifest.json").write_text(json.dumps([score.fingerprint(data, "test")]))
    report = score.build_scorecard(archive)
    assert report["status"] == "pending"
    assert report["pairs"] == []
    assert report["scoring_available"] == []
    (archive / "likelihood_manifest.json").write_text("[]")
    with pytest.raises(ValueError, match="nonempty"):
        score.build_scorecard(archive)
    (archive / "likelihood_manifest.json").write_text(json.dumps([score.fingerprint(data, "test")]))
    assert "post_run_review" in report["pending"]
    solver.write_bytes(b"drift")
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert report["scoring_available"] == []
    assert "Solver fingerprint drift" in report["errors"]
    assert report["pairs"] == []


def test_reviewed_archive_scores_all_pairs(tmp_path):
    # Reuse the pending-archive fixture construction, then add reviewed results.
    test_pending_archive_never_gets_scores_and_drift_blocks(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    protocol = score.read_json(archive / "protocol.json")
    protocol["classy_sha256"] = score.fingerprint(Path(protocol["classy"]), "test")["sha256"]
    (archive / "protocol.json").write_text(json.dumps(protocol))
    for gate in ("null_gate", "spectra_gate", "parameter_routing_gate"):
        (archive / f"{gate}.json").write_text('{"passed": true}')
    reviews = []
    for name, chi, count in (("LCDM", 100., 7), ("w0wa", 95., 9), ("AEGIS", 96., 9)):
        result = row(name, chi, count)
        validation = {"chi2": chi, "sampled_parameters": count,
                      "convergence_resolved": True, "restart_spread_chi2": .01,
                      "restart_minima": {str(i): [chi / 2 + (i % 2) * .005, True]
                                         for i in range(4)}}
        accuracy = {"best_point_accuracy_resolved": True, "dense_accuracy_shift": .001,
                    "chi2": chi, "dense_chi2_at_saved_minimum": chi + .001}
        reviews.append({"name": name, "chi2": chi, "accuracy_shift": .001, "dense_chi2": chi + .001,
                        "accuracy_passed": True,
                        "restarts": {"passed": True, "successful_restarts": 4, "spread_chi2": .01}})
        config = {"sampler": {"minimize": {"ignore_prior": True}},
                  "likelihood": {"survey": None}}
        for prefix, value in (("cmp", result), ("validation", validation),
                              ("accuracy", accuracy), ("config", config)):
            (archive / f"{prefix}_{name}.json").write_text(json.dumps(value))
    (archive / "post_run_review.json").write_text(json.dumps({"passed": True, "models": reviews}))
    report = score.build_scorecard(archive)
    assert report["status"] == "reviewed_in_sample"
    assert len(report["pairs"]) == 3
    assert len(report["catalog_sha256"]) == 64
    assert "paired AIC" in report["scoring_available"]


def test_changed_evidence_during_capture_blocks_scores(tmp_path, monkeypatch):
    test_reviewed_archive_scores_all_pairs(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    original = score.read_json

    def change_after_read(path):
        value = original(path)
        if path.name == "post_run_review.json":
            path.write_text('{"passed": false}')
        return value

    monkeypatch.setattr(score, "read_json", change_after_read)
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert report["pairs"] == []
    assert any("Evidence changed" in error for error in report["errors"])


@pytest.mark.parametrize("mutation", ["missing_model", "bad_spread", "bad_accuracy", "wrong_best"])
def test_pass_flags_do_not_override_invalid_evidence(tmp_path, mutation):
    test_reviewed_archive_scores_all_pairs(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    if mutation == "missing_model":
        path = archive / "post_run_review.json"
        value = score.read_json(path)
        value["models"].pop()
    elif mutation == "bad_accuracy":
        path = archive / "accuracy_AEGIS.json"
        value = score.read_json(path)
        value["dense_accuracy_shift"] = .1
    else:
        path = archive / "validation_AEGIS.json"
        value = score.read_json(path)
        if mutation == "bad_spread":
            value["restart_minima"]["0"][0] += 1.
        else:
            for record in value["restart_minima"].values():
                record[0] -= 1.
    path.write_text(json.dumps(value))
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert report["pairs"] == []


def test_likelihood_options_must_match(tmp_path):
    test_reviewed_archive_scores_all_pairs(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    path = archive / "config_AEGIS.json"
    config = score.read_json(path)
    config["likelihood"]["survey"] = {"scale_cut": 100}
    path.write_text(json.dumps(config))
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert any("likelihood settings differ" in error for error in report["errors"])


def test_shared_wrong_likelihood_names_cannot_pass_review(tmp_path):
    test_reviewed_archive_scores_all_pairs(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    for name in ("LCDM", "w0wa", "AEGIS"):
        path = archive / f"config_{name}.json"
        config = score.read_json(path)
        config["likelihood"] = {"different_survey": None}
        path.write_text(json.dumps(config))
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert report["pairs"] == []
    assert report["scoring_available"] == []
    assert sum("do not match configuration" in error for error in report["errors"]) == 3


def test_new_failure_file_during_capture_blocks_scores(tmp_path, monkeypatch):
    test_reviewed_archive_scores_all_pairs(tmp_path)
    archive = tmp_path / "cmb-fit" / "results" / "restarts" / "test"
    original = score.fingerprint
    captures = 0

    def create_failure(path, role):
        nonlocal captures
        item = original(path, role)
        if path.name == "config_AEGIS.json":
            captures += 1
            if captures == 2:
                (archive / "failure.json").write_text('{"error": "concurrent failure"}')
        return item

    monkeypatch.setattr(score, "fingerprint", create_failure)
    report = score.build_scorecard(archive)
    assert report["status"] == "blocked"
    assert report["pairs"] == []
    assert "Benchmark evidence file set changed during scorecard capture" in report["errors"]
