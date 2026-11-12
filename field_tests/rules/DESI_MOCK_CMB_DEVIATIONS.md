# DESI-MOCK-CMB deviations (PREREG_DESI_MOCK_CMB.md is locked and unchanged)

## D1 (11 Nov 2026, after the result): score step tolerates a missing comparison file
On the PC run the score step crashed after the reading had been computed: it loads `desi_mock_result.json` (the compressed
DESI-MOCK result) only to print a side-by-side comparison, and that file was not on the PC. The file was copied over and
the score step rerun from the saved fits (no refit, no change to inputs, reading unchanged: REPRODUCES DESI'S SIGNAL).
Afterwards `desi_mock_cmb.py` was changed so a missing comparison file is recorded as "not available" instead of
crashing. The change touches only that comparison; the fits, Δχ², σ and the reading rule are untouched.
