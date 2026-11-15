import subprocess, time
from pathlib import Path
from aion import core

def git(repo, *a):
    subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)

def make_repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com"); git(tmp_path, "config", "user.name", "t")
    (tmp_path / "field_tests/rules").mkdir(parents=True); (tmp_path / "field_tests/results").mkdir(parents=True)
    return tmp_path

def commit_file(repo, rel, text, ts):
    p = repo / rel; p.write_text(text); git(repo, "add", rel)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", rel], check=True, capture_output=True,
                   env={"GIT_AUTHOR_DATE": f"@{ts} +0000", "GIT_COMMITTER_DATE": f"@{ts} +0000", "PATH": "/usr/bin:/bin", "HOME": str(repo)})

def test_lock_writes_hash_and_verifies(tmp_path):
    repo = make_repo(tmp_path)
    p = core.new_prereg(repo / "field_tests/rules", "D1", "toy test")
    side = core.lock(p)
    assert side.exists() and core.verify_hash(p)
    p.write_text(p.read_text() + "edit after lock\n")
    assert not core.verify_hash(p)

def test_check_ok_late_nolock(tmp_path):
    repo = make_repo(tmp_path)
    commit_file(repo, "field_tests/rules/PREREG_D15_A.md", "rule", 1000)
    commit_file(repo, "field_tests/results/a_d15.txt", "result", 2000)
    commit_file(repo, "field_tests/results/b_d16.txt", "result", 2100)
    commit_file(repo, "field_tests/rules/PREREG_D16_B.md", "rule", 2200)
    commit_file(repo, "field_tests/results/c_d17.txt", "result", 2300)
    commit_file(repo, "field_tests/results/notes.txt", "no id", 2400)
    st = {f.result.split('/')[-1]: f.status for f in core.check(repo)}
    assert st == {"a_d15.txt": "OK", "b_d16.txt": "LATE", "c_d17.txt": "NO_LOCK", "notes.txt": "NO_ID"}

def test_template_fields():
    t = core.template("PREREG", id="D9", title="X", script="s.py", output="o.txt", date="2026-01-01")
    assert "PREREG D9: X" in t and "2026-01-01" in t and "{" not in t.split("## Question")[0]

def test_addendum_hash_accepted(tmp_path):
    repo = make_repo(tmp_path)
    p = core.new_prereg(repo / "field_tests/rules", "D20", "addendum case")
    core.lock(p)
    p.write_text(p.read_text() + "\n## Addendum (dated): extra prediction R7\n")
    assert not core.verify_hash(p)
    (repo / "field_tests/rules" / (p.name + ".addendum.sha256")).write_text(core.sha256_file(p) + "  " + p.name + "\n")
    assert core.verify_hash(p)
