import subprocess, sys, pathlib, yaml
from importlib import resources
HERE = pathlib.Path(__file__).resolve().parents[1]

def run(tmp, data):
    out = tmp / "out"
    subprocess.run([sys.executable, str(HERE / "track.py"), "--data", str(data), "--out", str(out)], check=True, capture_output=True)
    return (out / "STATUS.md").read_text(encoding="utf-8")

def test_new_release_changes_page_without_code_edits(tmp_path):
    base = yaml.safe_load(resources.files("inflation_scorecard").joinpath("data/constraints.yaml").read_text(encoding="utf-8"))
    f0 = tmp_path / "c0.yaml"; f0.write_text(yaml.safe_dump(base, allow_unicode=True), encoding="utf-8")
    s0 = run(tmp_path, f0)
    assert "after freeze (TEST)" not in s0
    base["ns_releases"].append({"name": "Hypothetical SO 2030", "year": 2030.5, "value": 0.950, "sigma": 0.002, "arxiv": "none", "date": "2030-06-01"})
    f1 = tmp_path / "c1.yaml"; f1.write_text(yaml.safe_dump(base, allow_unicode=True), encoding="utf-8")
    s1 = run(tmp_path, f1)
    assert "Hypothetical SO 2030" in s1 and "after freeze (TEST)" in s1
    assert "| Spectral index n_s | 0.969 – 0.975 | measured n_s more than 3σ outside the band | **KILL** |" in s1
