<!-- AEGIS-FP YBWOQVUJ7L5W6VNU · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# AION — lock before you look

*(Working name. Aion is the Greek god of unbounded time; the kit exists to prove what came first.)*

AION is a small, dependency-free pre-registration kit for computational research kept in git.
The rule is simple: **write down what you will compute and how you will judge it, hash it, commit it — then run.**
Afterwards anyone can check that every result in the repository was preceded by its lock.

It grew out of the AEGIS / SERAPIS project, where several hundred locked tests were run this way.

## Install
```bash
pip install ./tools/aion        # from this repository (PyPI release pending)
```

## Use
```bash
aion new D714 "Lyman-alpha rescore"     # creates field_tests/rules/PREREG_D714_LYMAN_ALPHA_RESCORE.md from the template
# ... fill in question, inputs, method and the PASS/FAIL rule ...
aion lock field_tests/rules/PREREG_D714_LYMAN_ALPHA_RESCORE.md --push   # writes .sha256, commits (and pushes)
# now run your script; name its output with the same id, e.g. results/lya_d714.txt
aion deviate D714                        # if something breaks: write the fix here BEFORE rerunning
aion check --repo .                      # audit: every result file must have an earlier lock
```

`aion check` reports each result file as:

| Status | Meaning |
|---|---|
| OK | a lock with the same id was committed no later than the result |
| LATE | the lock was committed **after** the result |
| NO_LOCK | the result has an id but no lock |
| NO_ID | the file name carries no id, so it cannot be matched |
| HASH_MISMATCH | the lock file was edited after its hash was written |
| UNCOMMITTED | the result is not in git yet |

Paths and the id pattern are configurable with an `aion.json` at the repository root:
```json
{"rules_glob": "field_tests/rules/PREREG_*.md", "results_glob": "field_tests/results/*", "id_regex": "[dD](\\d{2,5})"}
```

## Addenda
If a locked rule must gain an addendum (a dated, append-only extra prediction), hash the new text into
`<rule>.addendum.sha256` and commit it before any result that uses it; AION accepts either hash. The original
`.sha256` stays untouched, so the original lock remains provable from git history.

AION grew from the earlier AEGIS Method kit in `method/` (templates and `lock_rule.py`), adding the ordering audit.

## What it does not do
It proves ordering, not honesty of content: a lock written vaguely enough can still be gamed. The templates
push towards an explicit PASS/FAIL rule for that reason. Commit times come from git and can be forged by
someone with write access; for stronger proof, timestamp the lock commits externally (e.g. OpenTimestamps or a
Zenodo deposit).

## Licence
Dual-licensed: **AGPL-3.0-or-later** (free for everyone; see [LICENSE](LICENSE)) or a **commercial licence** for organisations that do not want the AGPL's obligations — tiers and contact in [COMMERCIAL.md](COMMERCIAL.md). © 2026 Danny Lee Eldridge.
