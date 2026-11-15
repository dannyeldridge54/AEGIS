# SERAPIS prediction tracker

Re-scores the frozen SERAPIS predictions (`predictions.yaml`, from the locks) against the Inflation Scorecard's
data file and writes a dated status page: `docs/tracker/STATUS.md` and `docs/tracker/index.html` (static, light/dark).

```bash
pip install ./tools/scorecard
python tools/tracker/track.py            # options: --data other_constraints.yaml --out folder
```
A new data release is one new entry in `tools/scorecard/inflation_scorecard/data/constraints.yaml`; give it a
`date:` after 2026-11-15 and it counts as a real test (the page marks it "after freeze (TEST)"). Earlier data are
shown as consistency only, because the model was fitted to them. Statuses: alive / tension / KILL (a lock's kill
condition met). `pytest tools/tracker/tests` checks that a new release changes the page with no code edits.

## Licence
Dual-licensed: AGPL-3.0-or-later ([LICENSE](LICENSE)) or commercial ([COMMERCIAL.md](COMMERCIAL.md)).
