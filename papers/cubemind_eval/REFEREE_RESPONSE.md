# Referee response: CubeMind interim report

## 18 Nov pass

**Verdict:** The numbers are sound for the stated window. The framing overclaimed causation and generality, and the methodological limitations were missing. Fixed in the v2 .tex and PDF. No new results.

### What was checked against the repo
| Claim | Source | Result |
|---|---|---|
| 10 graded, 0 promoted; 4 tautology / 3 falsified / 2 category / 1 ill-posed / 1 open | docs/web/CHECK_INDEX.md passes 1–5 | Correct as of the paper commit (954445ea, 11:14Z). Pass 6 (11:17Z) closed the open item as falsified. |
| Final count for the night | CHECK_INDEX passes 6–8 | 16 graded, 0 promoted (tautology 4, falsified 7, category 3, ill-posed 1, input re-predicted 1). Added as a "Note added". |
| "Predicted n_s outside its own range" | CHECK_INDEX audit entry | Mis-stated. The prediction was n_s in 0.9740–0.9750; the exact value is 0.97219. Fixed. |
| T_R off ~3.6 decades; r 3.1–3.7e-4 vs exact 4.38–4.80e-4 | CHECK_INDEX audit and pass 3 | Correct. |
| 51 missing sections, 32 invisible headers | CHECK_INDEX 10:55Z | Correct as logged. |
| Cycle "every 2–6 minutes" | CHECK_INDEX ("~2–4 min", "~120 s") | Changed to about 2–4 minutes. |
| "Every verdict is checked by computation or literature" | CHECK_INDEX | Overclaim. Tautologies and category errors were judged by inspection. Reworded. |
| Prompt rules 1–4 and 5–6, supersession, ingest parser | cubemind git 532b702, 8434fbc, 23feacf, 629c940 | Confirmed. |
| Stale-cache deploy path "whenever" a name is reused | CHECK_INDEX 10:55Z | Observed directly once; earlier episodes are attributed to it. Softened. |
| Archive is public | GitHub API | Public. Confirmed. |

### Methodology issues raised and addressed in text
1. **Causal claims from n = 1–4 per phase with no control.** "Fixes changed / moved" became "after each fix … observations, not measured effects". Lesson 1 became "can bound … suggestive, not shown".
2. **"Self-learning".** The weights never change, and every fix was made by the developers. This is now stated in the abstract and the Set-up. The title is unchanged, because it is a published record.
3. **"Falsified" means falsified against the model's own exact pipeline,** not against data. Now stated.
4. **New Limitations section:** a binomial bound (0/10 allows a survival rate up to 26%, 0/16 up to 17%, one-sided 95% Clopper–Pearson); one non-blind LLM grader who also wrote the fixes and the reference notes, with no inter-rater agreement; a post-hoc taxonomy; no baseline; a non-stationary system.
5. **Snapshot cutoff stated** (passes 1–5, frozen 11:14Z), with a post-cutoff note covering passes 6–8 and the upgrades deployed later (fact sheet, runnable TOOL/SEARCH check, self-check, rejection-reason feedback). These upgrades are not evaluated.
6. Removed the self-description "honestly and without promotion".

### Citations added (each verified by web search)
FunSearch (Nature 625, 468, 2024); The AI Scientist (arXiv:2408.06292); Si–Yang–Hashimoto (arXiv:2409.04109); Zheng et al., LLM-as-a-judge (arXiv:2306.05685); Panickssery et al., self-preference (arXiv:2404.13076); Toolformer (arXiv:2302.04761); ReAct (arXiv:2210.03629); Reflexion (arXiv:2303.11366).

### Not verifiable / left as is
- "two cores" was removed from the set-up because nothing in the repo records it. The model name (qwen3-coder:30b) is taken from the CHECK_INDEX 11:58Z entry. The proposer auto-picks a model, so the model in use during passes 1–5 is not logged per proposal. A later report should log it.
- The Lock v2 citation of this paper has no DOI yet.

### Headline-claim changes
- The abstract now reports **0/16 for the night** alongside the 0/10 window.
- The abstract's causal language ("moved it from … to …") was **downgraded to observations**.
