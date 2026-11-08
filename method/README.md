# The AEGIS Method (portable kit)

A way to do research that cannot quietly fool itself, usable in any field: physics, medicine, psychology, AI
evaluation, citizen science. Developed by Danny Lee Eldridge in the AEGIS / Twist cosmology project (2026).

## The rules
1. **Write the rule before the data.** Question, model, data, method, a code gate, and the exact thresholds that turn
   numbers into words (`RULE_TEMPLATE.md`).
2. **Lock it.** SHA-256 fingerprint + UTC time (`python lock_rule.py lock RULE.md`), then publish the fingerprint
   (git push, Zenodo, Software Heritage) before looking.
3. **Gate the code.** Before any result, the code must reproduce a known answer within a stated tolerance.
4. **Never edit a locked rule.** Changes go in a deviation log, written before rerunning (`DEVIATION_TEMPLATE.md`).
5. **Report failures at full size.** A failed test gets the same space as a pass and stays on record.
6. **Count your attempts.** Report local and global significance (look-elsewhere correction) side by side.
7. **Keep a ledger.** Every rule, its fingerprint re-verified, every verdict (`python lock_rule.py verify FOLDER`).
8. **State what is derived, chosen and fitted.** Every number in a model is labelled.
9. **Lock predictions before new data arrive,** and score them mechanically when the data are public.
10. **Make it reproducible:** one command from public data to the headline number.

## In practice (AEGIS, as of 8 Nov 2026)
50 locked files re-verified (47 exact, 3 Windows line endings only, 0 content changes); 72 verdicts on record,
16 of them failures. See `field_tests/ledger/LEDGER.md`.

## Licence
Same as the repository.
