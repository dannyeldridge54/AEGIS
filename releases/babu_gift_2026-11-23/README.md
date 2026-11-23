# Aion: a Zee–Babu prediction engine for Prof. K. S. Babu (Oklahoma State University)

> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It belongs to the one who asks, who measures, who will not kneel:
> take it, test it, and see for yourself.
> It was made for freedom, the quiet kind, the kind no one can sell you.

A gift from Danny Lee Eldridge, an independent researcher in Oklahoma City. No credit, endorsement or accreditation is asked; use it freely. The only ask is a serious look at the work.

**Start here:** open `Aion.html` in any browser (no install). Move the oscillation dials and the minimal-model predictions update live.
`python3 aion.py` gives the same numbers plus 3σ ranges: the envelope of the 1D 3σ ranges, δ over 0–360°, both θ23 octants (conservative; ignores correlations).

What it uses: the null vector of M_ν (det M_ν = 0, lightest neutrino massless at two loops) fixes the f-ratios
(formulas of Herrero-García, Nebot, Rius & Santamaria, arXiv:1402.4491; checked to 1e-16 in the convention M_ν = U diag(m) Uᵀ).
Inputs: NuFIT 6.0 (IC19 without SK-atm). The model: Zee, NPB 264 (1986) 99; Babu, PLB 203 (1988) 132; Babu & Macesanu, hep-ph/0212058; Nebot et al., arXiv:0711.0483.

| Ordering | h⁺→eν best (3σ) | h⁺→μν | h⁺→τν | m_ββ (meV) | Σm_ν (eV) | max \|f_μτ\| at m_h = 1 TeV (MEG II, 3σ) |
|---|---|---|---|---|---|---|
| Normal (m1 = 0) | 16% (14%–18%) | 46% (36%–47%) | 38% (36%–47%) | 1.5–3.7 | 0.0590 | 0.031–0.049 |
| Inverted (m3 = 0) | 49% (49%–49%) | 23% (21%–29%) | 29% (22%–30%) | 18.3–48.5 | 0.0994 | 0.011–0.012 |

Notes, stated plainly:
- The μ→eγ ceiling is the h⁺ contribution only; the k⁺⁺ loop has the opposite chirality and adds incoherently, so it is conservative. It scales as m_h.
- Σm_ν for inverted ordering is in tension with the DESI DR2 + CMB ΛCDM bound (< 0.0642 eV, 95%). That is model-dependent and applies to any inverted-ordering model with m₃ = 0, not specifically to Zee–Babu.
- Aion predicts flavour ratios only, not the overall scale or the loop function I(m_k/m_h). It does not cover your SU(5) completion with Shaikh Saad (arXiv:2412.14562), where coloured scalars contribute comparably, or the k⁺⁺ sector (g couplings free).
- Checked by an independent referee in two rounds; locks and corrections: D2188 (field_tests/rules/PREREG_D2188_*).

| File | What it is |
|---|---|
| `Aion.html` | The live tool (one file, works offline) |
| `aion.py` / `aion_core.js` | Same engine in Python and JavaScript (agree to 4e-16) |
| `d2188_results.json` | All numbers above, with 3σ scan ranges |
| `test_d2188.py`, `d2188_tests.json` | The locked checks (null vector, m_ββ sanity) |

License: [AEGIS Community License](../../LICENSE). Contact: dannyeldridge54@gmail.com
