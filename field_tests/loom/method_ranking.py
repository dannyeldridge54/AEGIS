"""Rank 25 research-method improvements by the share of today's 19 recorded errors (D1873-D1920) each would have caught.
The error->method mapping is my retro-judgement (stated), one line per error, so it can be audited and disputed."""
E = {
 'E1':  'b-prime gauge term omitted (D1881a->D1881b)',
 'E2':  'degenerate-class artefact taken as result (D1885)',
 'E3':  'no look-elsewhere on the arrow (D1894)',
 'E4':  'bounds/naturalness bars counted as evidence (D1896)',
 'E5':  'heterotic formula used in a brane model (D1881->D1900)',
 'E6':  'thread modulus already stabilised by SU(12) (D1902 vs D1812)',
 'E7':  'toy that 25,088 configs pass (D1901b)',
 'E8':  'hard-coded rows in the scoreboard (D1896)',
 'E9':  'stale/duplicate ticks',
 'E10': 'epsilon used as the step u (D1894b)',
 'E11': 'PPN convention factor sqrt2 (D1906a)',
 'E12': 'unequal extraction rules across sources (D1908a)',
 'E13': 'withdrawn value restored by a framework switch (D1904/D1907)',
 'E14': 'zero-power phase test (D1918a)',
 'E15': 'free alpha tuned and called derived (D1917a)',
 'E16': 'Z3-twisted torus has frozen U (D1917a)',
 'E17': 'heterotic Higgs counting in branes (D1907)',
 'E18': 'false summary line: every reading < 0.09 (D1909b)',
 'E19': 'tau3-localised uplift claimed as a loophole (D1906b)',
}
M = [
 ('Independent heterogeneous referee on every scoreboard change (different prompt/model framing; arXiv:2502.08788 heterogeneity)', 'E1 E2 E3 E4 E5 E10 E11 E12 E13 E14 E15 E16 E17 E18 E19'),
 ('Symbol & convention registry (one definition per symbol, units, convention; scripts import it)', 'E10 E11 E1 E19'),
 ('Framework-applicability gate (tag each formula heterotic/IIA/IIB/FT; mismatch must be justified before use)', 'E1 E5 E13 E16 E17'),
 ('Power / invariance check before any test (can the score vary? what fraction of the null passes?)', 'E7 E14 E4'),
 ('Forking-paths ledger (every analysis choice and alternative logged; trials-corrected p)', 'E3 E13 E15 E4 E12'),
 ('Multiverse / sensitivity analysis over all allowed analysis choices', 'E12 E15 E3 E4'),
 ('Constraint graph of fixed quantities and postulates (automatic conflict scan)', 'E6 E16 E19 E13'),
 ('Single source of truth for numbers (values file; docs and scripts read it; no typed numbers)', 'E8 E10 E18'),
 ('Blind analysis / hidden answer (Klein-Roodman): fix the method before seeing the verdict-relevant number', 'E15 E3 E13 E12'),
 ('Kill-first red team (spend one step trying to break the postulate before testing it)', 'E6 E16 E19 E17 E5'),
 ('Null / control runs (shuffled or random inputs through the same test)', 'E4 E7 E14 E3'),
 ('Stability check (seeds, bases, grids)', 'E2'),
 ('Analytic-limit regression tests (known limits each formula must reproduce)', 'E11 E1 E2'),
 ('Reproduce-a-published-model first (calibrate code on a known answer before the new case)', 'E1 E17 E11'),
 ('Systematic-review protocol (PRISMA-style search string, inclusion criteria, all hits)', 'E12 E18'),
 ('Meta-analysis with heterogeneity statistics and cluster reporting (Mirror-Loom)', 'E12 E18'),
 ('Mechanical quote-and-number verification of every cited value', 'E18'),
 ('Idempotent ticks keyed to the next D-number (skip if done)', 'E9'),
 ('Fit-vs-derive label enforced (count free parameters vs constraints in every claim)', 'E15 E4 E3'),
 ('Adversarial collaboration (pair agent argues the opposite hypothesis)', 'E13 E19 E6'),
 ('Expected-information-gain target selection (Bayesian experimental design, arXiv:2302.14545)', ''),
 ('Sequential / iterated design (update, re-target)', 'E14'),
 ('Delphi-style structured consensus (anonymous rounds, report spread)', 'E12'),
 ('Propagation step after every withdrawal (grep all docs/JSON/paper)', 'E18 E10'),
 ('Preregistration + sha256 locks before compute (already in use)', ''),
]
rows = []
for name, hits in M:
    h = set(hits.split()) if hits else set()
    rows.append((len(h) / len(E), name, sorted(h, key=lambda x: int(x[1:]))))
rows.sort(key=lambda r: -r[0])
for i, (p, n, h) in enumerate(rows, 1):
    print('%2d. %5.1f%%  %s  [%s]' % (i, 100 * p, n, ' '.join(h)))
cover = set().union(*[set(h) for _, _, h in rows[:8]])
print('\nTop-8 union covers %d/%d errors (%.0f%%); missing: %s' % (len(cover), len(E), 100 * len(cover) / len(E), sorted(set(E) - cover, key=lambda x: int(x[1:]))))
