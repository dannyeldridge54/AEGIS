# PREREG D1463 — where does each vacuum's correction over leading order come from?

Locked 2026-11-19 (UTC) before computing (JANUS tick 59, node janus).
Factorisation at each vacuum's centre: derived/LO = (offset-corrected first-order closed form / LO) × (derived / closed form).
τ = i at NA12 centre (n_s 0.97462, r 4.8335e-4): LO = D1405 κ = ½ (= D640 at c = 0 exactly, D1436); closed form = D640 with
c = ln1728/2π, inverted at (n_s, r) as in field_tests/scripts/d1412/tau_i_offset.py; derived = D1448 json value (−8.54295e-4).
ρ at A1 (n_s 0.974393, r 4.82095e-4): LO = −2r (D1399); closed form = D1439's first-order −2r[1 + 4w(1−t) − 6Bw/(1+t)]
(from D1439 json: plateau piece, offset piece); derived = D1442 json value (−9.97963e-4).
Report each factor in % and the "offset" share (closed form/LO − 1) vs the "slow-roll-order + remaining" share (derived/closed − 1).
Characterisation, no pass/fail. Sanity check (must hold, else "no result"): product of factors reproduces derived/LO to 1e-12.
No reruns; fixes only via PREREG_D1463_DEVIATIONS.md first.
