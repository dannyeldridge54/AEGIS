# PREREG_D1662_G12C_REFEREE — re-run of the round-2 source audit after D1661 (Janus genesis G12c; locked 2026-11-19 ~23:40Z before the audit runs)
Re-run field_tests/scripts/janus_g/g12b_referee.py unchanged (lock order, arithmetic, card, source audit), output copied to field_tests/results/D1662_G12c_referee.json.
Additional check (script g12c_referee.py): every note D1660 classed VERDICT-DEPENDENT must have a later sourced scope note: D1646 → D1646a + D1654; D1632, D1648, D1649 → D1661 (which must contain "2603.13226"). Any NEW flagged note not in D1660's list is read by hand.
Pass rule: PASS if mechanics pass, every verdict-dependent flag is covered by a sourced scope note, and no new verdict-dependent flag appears; remaining flags are nits (listed). PASS ⇒ the round-2 loop stops.
