# Pre-registration: <short name>

**Status:** DRAFT (becomes locked only with `python lock_rule.py lock` and a published .sha256).
**Written:** <date>, by <who> (<tools/AI assistance used>). **Data seen when written:** <none / list exactly what>.

## Question
One sentence, answerable yes/no or by a number.

## Hypothesis and model (fixed)
What is being tested, every free parameter and its prior range, and everything held fixed.

## Data (fixed)
Exact datasets, versions, cuts. What is excluded and why.

## Method (fixed)
Code, version/commit, settings, number of restarts or chains, convergence criteria.

## Gate (code check before any data result)
A check that the code reproduces a known answer within a stated tolerance. If it fails: no result, no verdict.

## Decision rule (fixed)
Thresholds that turn numbers into words (e.g. PASS / TIE / FAIL), including what counts as NO VERDICT.
Also reported (not verdicts): <list>.

## Blindness
Is the outcome unknown when this is locked? If not, say exactly what was already known.

## Failures and deviations
Any later change is logged first in a deviation file (see DEVIATION_TEMPLATE.md); the original is run and reported too.
