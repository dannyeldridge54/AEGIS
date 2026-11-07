import subprocess
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import pytest

from theory import review_numerical as review


def evidence(path, *, missing=None, skip=None, failure=None):
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite")
    for _, files in review.CHECKS:
        for name in files:
            if name == missing:
                continue
            case = ET.SubElement(suite, "testcase",
                                 classname=f"theory.{name[:-3]}", name="regression")
            if name == skip:
                ET.SubElement(case, "skipped")
            if name == failure:
                ET.SubElement(case, "failure")
    ET.ElementTree(root).write(path)


@pytest.mark.parametrize("kind,status", [
    (None, "PASS"), ("missing", "BLOCKED"), ("skip", "BLOCKED"), ("failure", "FAIL"),
])
def test_each_area_requires_complete_passing_evidence(tmp_path, kind, status):
    report = tmp_path / "report.xml"
    options = {} if kind is None else {kind: "test_bi_qcd_dynamics.py"}
    evidence(report, **options)
    rows = review.summarize(report)
    assert len(rows) == 10
    assert rows[8][1] == status
    assert all(row[1] == "PASS" for index, row in enumerate(rows) if index != 8)


@pytest.mark.parametrize("exit_code,expected", [(0, 0), (1, 1), (2, 2), (5, 2)])
def test_pytest_exit_cannot_be_hidden_by_passing_cases(monkeypatch, exit_code, expected):
    def run(command, **kwargs):
        evidence(command[command.index("--junitxml") + 1])
        assert kwargs["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
        assert kwargs["stdin"] == subprocess.DEVNULL
        return SimpleNamespace(returncode=exit_code, stdout="pytest diagnostics")
    monkeypatch.setattr(review.subprocess, "run", run)
    assert review.run_review() == expected


def test_timeout_is_blocked_not_pass(monkeypatch):
    def run(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output=b"partial evidence")
    monkeypatch.setattr(review.subprocess, "run", run)
    assert review.run_review() == 2


def test_missing_xml_is_blocked(monkeypatch):
    monkeypatch.setattr(review.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout="no evidence"))
    assert review.run_review() == 2


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_invalid_timeout_rejected(timeout):
    with pytest.raises(ValueError, match="timeout"):
        review.run_review(timeout)


def test_derivation_comparison_review_has_complete_distinct_evidence(tmp_path):
    from theory.review_derivation_comparisons import CHECKS
    assert len(CHECKS) == 10
    root = ET.Element("testsuites")
    for _, files in CHECKS:
        for name in files:
            path = Path(name)
            resolved = path if path.is_absolute() else Path(review.__file__).parent / path
            assert resolved.is_file()
            ET.SubElement(root, "testcase", classname=path.stem, name="regression")
    report = tmp_path / "comparison.xml"
    ET.ElementTree(root).write(report)
    assert all(row[1] == "PASS" for row in review.summarize(report, CHECKS))
    root.remove(root[-1])
    ET.ElementTree(root).write(report)
    assert review.summarize(report, CHECKS)[-1][1] == "BLOCKED"


@pytest.mark.parametrize("classname,status", [
    ("test_save_objective.SaveTests", "PASS"),
    ("package.test_save_objective.SaveTests", "PASS"),
    ("test_save_objective_extra.SaveTests", "BLOCKED"),
])
def test_unittest_class_names_require_exact_module_component(tmp_path, classname, status):
    report = tmp_path / "unittest.xml"
    root = ET.Element("testsuites")
    ET.SubElement(root, "testcase", classname=classname, name="test_saved_objective")
    ET.ElementTree(root).write(report)
    checks = (("Saved objective", ("test_save_objective.py",)),)
    assert review.summarize(report, checks)[0][1] == status
