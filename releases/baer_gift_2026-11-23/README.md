# Decaying-wino data packet for Prof. Howard Baer (University of Oklahoma)

> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It belongs to the one who asks, who measures, who will not kneel:
> take it, test it, and see for yourself.
> It was made for freedom, the quiet kind, the kind no one can sell you.

A gift from Danny Lee Eldridge, independent researcher, Oklahoma City. No credit, endorsement or accreditation is asked; use it freely. The only ask is a serious look at the work.

**Start here:** `Baer_decaying_wino_note.pdf` (2 pages): the RPV-decaying-WIMP mechanism of Baer, Barger & Deal (arXiv:2609.04412) extended to a mini-split wino spectrum.

| File | What it is |
|---|---|
| `weave_benchmark_pMSSM_input.slha` | SLHA pMSSM input card for the benchmark (SoftSUSY / SPheno / FlexibleSUSY); un-computed entries flagged |
| `weave_benchmark_inputs.csv` | Every benchmark parameter with range, status and source (also for entering into Isajet's own keywords) |
| `d2186b_baer_rpv_wino.csv` | f_a needed for τ ≤ 0.1 s, both RPV cases, m_soft 5–160 TeV, m_χ 670/693/1000 GeV |
| `d2186b_baer.py` | The script that made it |

### Zurvan: a small Δ_EW toolkit (folder `zurvan/`)
**Open `zurvan/Zurvan.html` in any browser** (no install, nothing uploaded), or run `python3 zurvan/zurvan.py spectrum.slha`.
It reads an SLHA output file (Isajet / SoftSUSY / SPheno) and lists Δ_EW and its terms, following your definition in DEW4SLHA
(arXiv:2111.03096). It gets Σ_u^u and Σ_d^d by numerically differentiating the one-loop Coleman–Weinberg potential, built
from the stop mass matrix of your Eq. A.14, so it is a check that works from first principles. It also carries the
decaying-wino RPV calculator from the note. Named for Zurvan, the Persian figure of boundless time.

Honest limits: third family only (no 1st/2nd-family sfermions, tau sneutrino, charginos/neutralinos, Higgs, W/Z, QCD
corrections to y_t, or two-loop terms; DEW4SLHA has those). It has **not** yet been checked against DEW4SLHA on a real
Isajet or SoftSUSY file, and the three example files are hand-built and illustrative (they do not satisfy EWSB, and the
tool says so). It prints the EWSB residual, flags near-degenerate pairs and tachyonic states.

One question we would be grateful to have answered: the exact derivative of the A.14 mass matrix keeps the cross-terms
−y_t² A_t μ cotβ (in Σ_u^u) and −y_t² A_t μ tanβ (in Σ_d^d) inside the ∓[…]/(m²_t̃2 − m²_t̃1) bracket. With them added,
Eqs. A.20/A.21 reproduce Zurvan exactly; without them, Σ_d^d(t̃1,2) differ a lot term by term (the pair sum much less).
We may be missing a convention, so we ask rather than assume.

For the Weave benchmark (μ ≈ 88 TeV) the robust statement is Δ_EW ≥ 2μ²/m_Z² ≈ 1.8×10⁶: by your measure it is very unnatural.

All numbers are THEORY, order-of-magnitude. Locks, referee reports and corrections: D2186–D2186a, D2187 (Zurvan).
License: [AEGIS Community License](../../LICENSE). Contact: dannyeldridge54@gmail.com
