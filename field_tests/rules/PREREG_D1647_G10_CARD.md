# PREREG_D1647_G10_CARD — genesis budget card, machine-checked (Janus genesis G10; locked 2026-11-19 ~22:48Z)
Card: docs/JANUS_GENESIS_CARD.md. Every number is typed on the card with its source json and key path; the card is written BEFORE the check script reads anything.
Check (field_tests/scripts/janus_g/g10_card_check.py): parses the card's table rows (value | file | key), re-reads each json key, and compares. A row is OK if |card/json − 1| ≤ 0.6 × 10^(1 − sig) (sig = significant digits typed on the card, i.e. a correct rounding passes), or exact for booleans/strings.
Pass rule: CONSISTENT if every row is OK; any MISMATCH is listed and must be fixed as a card correction note (D1647a), never by editing the json.
Output: field_tests/results/D1647_G10_card_check.json
