# CM-CARDS DEVIATIONS (written before any fix)
C3 FAILS as locked (2 of 5 spot checks):
- DEV-1 U-238: the card gives 4.4629e9 y (NUBASE2020 as parsed). My goalpost 4.468e9 y is the older ENSDF/Jaffey (1971) value; NUBASE2020
  lists 4.463(3) Gy. Goalpost error (mine, same class as the 14.07 MeV shortcut), not a card error. No change to the card.
- DEV-2 Au: mendeleev stores "[Xe] 4f14 5d10 6s" (a single electron written without the "1"). Fix: normalise a bare trailing subshell
  to "...1" in the card's electron_configuration (format only), keeping the raw string as electron_configuration_raw.
- DEV-3 (found in the summary text, not a goalpost): summary() read ionization energies with int keys; after a JSON round trip the keys are
  strings -> "IE1..3 [None, None, None]". Fix: accept both.

## Run on the PC (18:27-18:32 UTC, first 8 fusion derives after the restart; written before any fix)
- A1 PASS as locked: 5/8 (fusion_ign, burn_1, burn_2, tbr_0, tbr_1 pass; ign2, burn_0, burn_3 fail). Caveat: these task texts already
  stated their formulas, so the gain is not cleanly attributable to the cards; the clean comparison (sigmav, 0/8 closed-book) has not recurred.
- S1 FAILS as locked: median spacing ~39 s (41, 40, 35, 56, 35, 39, 29), same as baseline. Cutting the prompt did not help: the time is
  output generation (num_predict 900) plus the self-check call on every failure.
- Finding: 3/8 failures (burn_0, burn_3, and earlier Q_DHe3) had formula_ok = True: the expression was right (the engine evaluated it
  exactly) but the hand arithmetic in "result" was wrong.
Fixes (one rerun on the next 8 graded fusion/element derives):
- DEV-4 skip the self-check LLM call when formula_ok is True: class = arithmetic, rule = fixed text "your formula was right; evaluate
  the expression, do not do long arithmetic by hand" (saves one model call per such failure).
- DEV-5 num_predict 900 -> 600 for card tasks (short numbered steps); a truncated reply counts as a fail.
- DEV-6 a 'calc_ok' field (= formula_ok: method right, number by calculator) is recorded beside 'ok'. Grading by 'ok' is unchanged.
