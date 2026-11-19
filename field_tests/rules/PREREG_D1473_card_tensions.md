# PREREG D1473 — "data tensions" section on docs/JANUS_FORMULAS.md, machine-checked

Locked 2026-11-19 (UTC) before writing/checking (JANUS tick 76, node janus).
Add rows for D1471 (2511.01612 Table IV) and D1472 (2506.20707 Tables I/VI) to the card, numbers rounded to 2 decimals in σ.
Check script field_tests/scripts/d1473/card_check2.py parses the new card rows and compares each quoted pull with the
D1471/D1472 result jsons at 2-decimal precision. Rule: CONSISTENT if no mismatch.
No reruns; fixes only via PREREG_D1473_DEVIATIONS.md first.
