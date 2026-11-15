"""AION core: lock, deviate, check. Standard library only."""
from __future__ import annotations
import datetime as _dt, fnmatch, hashlib, json, os, re, subprocess
from dataclasses import dataclass, field
from pathlib import Path
from importlib import resources

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def template(kind: str, **fields: str) -> str:
    text = resources.files("aion").joinpath(f"templates/{kind}.md").read_text(encoding="utf-8")
    fields.setdefault("date", _dt.date.today().isoformat())
    for k, v in fields.items():
        text = text.replace("{" + k + "}", v)
    return text

def new_prereg(rules_dir: Path, ident: str, title: str, script: str = "", output: str = "") -> Path:
    rules_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_").upper()[:40] or "RULE"
    path = rules_dir / f"PREREG_{ident}_{slug}.md"
    if path.exists():
        raise FileExistsError(path)
    path.write_text(template("PREREG", id=ident, title=title, script=script or "(path)", output=output or "(path)"), encoding="utf-8")
    return path

def new_deviation(rules_dir: Path, ident: str) -> Path:
    path = rules_dir / f"PREREG_{ident}_DEVIATIONS.md"
    if not path.exists():
        path.write_text(template("DEVIATIONS", id=ident), encoding="utf-8")
    return path

def lock(path: Path, commit: bool = True, push: bool = False, message: str | None = None) -> Path:
    """Write <file>.sha256 next to the rule and (optionally) commit both."""
    path = Path(path)
    digest = sha256_file(path)
    side = path.with_name(path.name + ".sha256")
    side.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    if commit:
        repo = Path(_git(path.parent, "rev-parse", "--show-toplevel").strip())
        _git(repo, "add", str(path), str(side))
        _git(repo, "commit", "-q", "-m", message or f"AION lock: {path.name} sha256 {digest[:12]}")
        if push:
            _git(repo, "push", "-q")
    return side

def verify_hash(path: Path) -> bool:
    side = Path(str(path) + ".sha256")
    if not side.exists():
        return False
    return side.read_text().split()[0] == sha256_file(path)

@dataclass
class Config:
    rules_glob: str = "field_tests/rules/PREREG_*.md"
    results_glob: str = "field_tests/results/*"
    id_regex: str = r"[dD](\d{2,5})"

    @classmethod
    def load(cls, repo: Path) -> "Config":
        f = repo / "aion.json"
        return cls(**json.loads(f.read_text())) if f.exists() else cls()

@dataclass
class Finding:
    result: str
    ident: str | None
    status: str          # OK, LATE, NO_LOCK, NO_ID, UNCOMMITTED, HASH_MISMATCH
    detail: str = ""

def _first_commit_time(repo: Path, rel: str) -> int | None:
    out = _git(repo, "log", "--diff-filter=A", "--format=%ct", "--", rel).split()
    return int(out[-1]) if out else None

def check(repo: Path, cfg: Config | None = None) -> list[Finding]:
    """For every result file with an id, require a lock (PREREG) for that id
    whose first commit is not later than the result's first commit."""
    repo = Path(repo)
    cfg = cfg or Config.load(repo)
    rx = re.compile(cfg.id_regex)
    tracked = _git(repo, "ls-files").splitlines()
    rules = [p for p in tracked if fnmatch.fnmatch(p, cfg.rules_glob) and not p.endswith("_DEVIATIONS.md")]
    results = [p for p in tracked if fnmatch.fnmatch(p, cfg.results_glob)]
    by_id: dict[str, list[str]] = {}
    for r in rules:
        for m in rx.finditer(Path(r).name):
            by_id.setdefault(str(int(m.group(1))), []).append(r)
    out: list[Finding] = []
    for res in sorted(results):
        ids = [str(int(m.group(1))) for m in rx.finditer(Path(res).name)]
        if not ids:
            out.append(Finding(res, None, "NO_ID")); continue
        ident = ids[-1]
        locks = by_id.get(ident, [])
        if not locks:
            out.append(Finding(res, ident, "NO_LOCK")); continue
        t_res = _first_commit_time(repo, res)
        if t_res is None:
            out.append(Finding(res, ident, "UNCOMMITTED")); continue
        t_lock = min(t for t in (_first_commit_time(repo, l) for l in locks) if t is not None)
        bad_hash = [l for l in locks if Path(repo / (l + ".sha256")).exists() and not verify_hash(repo / l)]
        if bad_hash:
            out.append(Finding(res, ident, "HASH_MISMATCH", ", ".join(bad_hash)))
        elif t_lock <= t_res:
            out.append(Finding(res, ident, "OK", f"lock {t_res - t_lock}s before result"))
        else:
            out.append(Finding(res, ident, "LATE", f"lock committed {t_lock - t_res}s AFTER result"))
    return out

def summary(findings: list[Finding]) -> dict[str, int]:
    s: dict[str, int] = {}
    for f in findings:
        s[f.status] = s.get(f.status, 0) + 1
    return s
