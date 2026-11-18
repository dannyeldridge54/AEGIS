<!-- AEGIS-FP KTFLMTAH7V4QAFZL · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Referee response: Lock Before You Compute v2 addendum

## 18 Nov pass

**Verdict:** The six rules are reasonable and mostly well grounded. One number was wrong (R3). One worked example (R4) was presented as stronger than it is. The audit's coverage and independence were overstated, and there was no prior art. Fixed in the v2 .tex and PDF. No new results.

### What was checked against the repo
| Claim | Source | Result |
|---|---|---|
| ~15 results | CHECK_INDEX 10:55Z ("tonight's 15 notes") | 9 results (D1272–D1280) + 6 correction notes. Now stated that way. |
| 10 machine proposals | CHECK_INDEX passes 1–5 | Correct at the time of writing; 16 by the end of the morning. Both now given in R6. |
| R1 circularity, one claim withdrawn | D1275b; audit_2026-11-18.txt §4 | Confirmed. |
| R2 "four results corrected (D1265a/b, D1273a, D1274a, D1275a/b)" | DERIVATION_LOG | 4 originals, 6 correction notes. Reworded. |
| R3 slope "13% low" | audit §1, D1265a, D1265b | **Wrong.** The fresh symmetric slope is 0.01334, so 0.01171 is **12.2% low**. 13.4% is relative to D1265a's wide fit (0.01352), which D1265b superseded. Fixed to 12%, and the text notes that the first correction was itself 1.3% high. |
| R4 E6/E7 predicted first, then passed | D1278 (commit cf9ab850, 04:24 CST) → D1282 (962a655c, 04:53 CST) | The order is confirmed. But (a) the prediction was in a D-note, not a SHA-256 lock; (b) D1282 compared E6/E7 only with their own duals, and its own steps 1–2 show the swap at α = 1 is forced by Poisson duality for any lattice that is not self-dual. The test therefore had almost no chance to fail. The rule is extended: state whether a known identity already implies the prediction. The later locked test, PREREG_D1286, is mentioned. |
| R5 round(x,6) incident, "cost an hour" | searched both repos and the session docs | **Not found in the archive.** It is kept, labelled as from the working session, and the "cost an hour" figure is dropped. |
| R6 "each phase fixed … failures mostly memory/deploy, not model" | CHECK_INDEX passes 5–6 | Overclaim. Rules 5–6 stopped the d-dimension error, but category mixing continued in pass 6. Reworded. |
| "Audit confirmed every computed result of the night" | CHECK_INDEX audit (10:40Z), audit file | The audit covered D1265a and D1272–D1279. D1280 (10:42Z) and D1282 came later and have only internal checks. The audit was also a self-audit by the same AI. Both are now stated. |
| "Corrections concerned interpretation and data inputs, not arithmetic" | D1265a/b, D1273a | Mostly right. The point at which a coefficient was evaluated is added as a third category. |

### Citations added (each verified by web search)
Nosek et al., PNAS 115, 2600 (2018); Chambers, Cortex 49, 609 (2013); Klein & Roodman, Annu. Rev. Nucl. Part. Sci. 55, 141 (2005); Kerr, PSPR 2, 196 (1998). A short paragraph places the rules relative to pre-registration, registered reports, blind analysis and HARKing. It also notes that the locks are self-imposed and nothing is reviewed in advance.

### Headline-claim changes
- Abstract rule (3): **13% → 12%**.
- Abstract rule (4): the E6/E7 example is now described as **near-guaranteed by a known identity**, and the rule gains "say how risky it is".
- Abstract rule (6): "failures are mostly failures of memory and deployment, not of the model" was **withdrawn**. It now reads: early failures traced to prompt, memory and deploy; category errors persisted.
- Abstract rule (5): the "phantom bug" anecdote is now flagged in the body as not archived.
