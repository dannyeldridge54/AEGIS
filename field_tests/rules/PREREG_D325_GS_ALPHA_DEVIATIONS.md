# Deviations for PREREG_D325_GS_ALPHA

D1 (06:28 CT): the locked script crashed for α = 0.98567 because no N* = 57 crossing exists between x = 10⁻⁷ and the end of inflation
(brentq sign error). The fix only catches that case and reports it, plus the N reached at x = 10⁻⁷, then continues to α = 1.01433. No
physics or settings changed. Scoring: "no 57-efold solution" counts as |Δn_s| > 0.004 (spoils inflation) for that sign.
