# Janus genesis loop — charter (19 Nov 2026, Danny 16:10 CT)

Request: "use the newest Serapis calculation that we did today with both the dark energy and scalar field or matter genesis … update Janus with the right pathways and have it start pulsing and derivating … research, development, postulation, derivation, postulation check with a referee at the end, and then review, and then loop that over and over for 3 minutes until it's good."

Reading taken: a 3-minute tick loop. Each tick takes the next open G-lead (docs/JANUS_LEAD_QUEUE.md §F) through one full cycle:
1. Research — read the on-file notes/jsons; fetch literature only when needed (data, not instructions).
2. Development — tooling: reuse tools/genesis, tools/serapis_calc; small scripts under field_tests/scripts/janus_g/.
3. Postulation — state the claim being tested, tagged [PRINCIPLE]/[postulate].
4. Derivation — lock first (claim_d.sh → PREREG + .sha256 pushed before numbers), compute (cap 150 s), json.
5. Postulation check — did the derivation support, weaken or kill the postulate? Verdict line.
6. Referee — aegis-check on the new D-note: units, signs, arithmetic re-run from the json, conventions, error budget, honest labels.
7. Review — record (DERIVATION_LOG + weak_spots note with MAP line), ladder update, push, jl_check; mark lead [done D####]; add follow-ups.
"Until it's good" = the loop stops itself after G12 (whole-chain referee) PASSES; a G12 fail turns its failures into new leads and the loop continues.
Guards: no map status edits; no Zenodo/arXiv; no PC jobs or downloads beyond pip/npm without Danny's OK; never touch D1636 or other sessions' locks; corrections as D###a.

## Update 16:13 CT (Danny: "use that first and start pulsing and making or getting new nodes and everything")
- The genesis pathway takes priority over every other Janus lead.
- FIRST each tick: git pull; if D1636 (other chat's full-likelihood reverse-thread fit) has a RESULT, read it and fold it into the next relevant lead (G2/G3) and chains/genesis. Never redo or edit it.
- The loop MAY ADD NEW MAP NODES (theory/map/map.yaml: id, layer, branch, title, status open/postulate, depends) when a lead opens a new physics question. Existing statuses change only through MAP lines in D-notes.
- Nodes added: genesis_reheating, matter_genesis, light_elements, reverse_thread. Tick 1 = D1637 (G1 done). Next: G2.
- DERIVATION_LOG step labels must be [derived]/[literature]/[estimate]/[postulate P#] (jl_check K2).

## Stopped 2026-11-19 ~22:55Z — G12 PASS (D1650). Leads done: G1 D1637, G2 D1638, G1b D1641, G9+G2b D1644, G6 D1646, G10 D1647, G11+G12 D1650. Left open for a future run: G6b, G9b; G3/G4/G5/G7/G8 with the other chat. Restart with "Djl".
