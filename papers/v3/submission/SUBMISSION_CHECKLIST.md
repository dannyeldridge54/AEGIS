# SERAPIS v3 — submission checklist (PRD + arXiv)
Status 2026-11-15 (updated after weak-point rounds 1–2): package rebuilt and tested. Every remaining step needs Danny; Claude does not submit, publish or send anything.

## Ready (done by the readiness ladder)
- [x] Manuscript: serapis_v3.tex / .pdf (REVTeX 4.2, PRD style, 8 pp, clean compile, no overfull boxes).
- [x] Two independent referee passes (papers/v3/referee/); all raised issues fixed or disclosed (D636–D639).
- [x] References: 38 cited, each checked against its arXiv record or journal listing (refs_checked.md); NuFit-6.0 checked via search listing. Two 1980s journal refs (Turner 1983; Affleck–Dine 1985) checked from knowledge only.
- [x] Figures 1–4 (vector PDF), reproducible via figs/make_figs.py.
- [x] Reproducibility appendix mapping every computation to its pre-registration and script.
- [x] Forward predictions frozen and hashed (D605, D615, D633); differences between locks and paper disclosed in the text.
- [x] AI-assistance statement (APS policy: AI not an author; role disclosed; author responsible).
- [x] arXiv tarball (submission/serapis_v3_arxiv.tar.gz) compiled standalone; metadata in ARXIV_METADATA.txt.
- [x] PRD cover letter draft (COVER_LETTER_PRD.md); arXiv endorsement request draft (drafts/endorsement_request.md).

## Danny's steps, in order
1. Read the whole PDF yourself. arXiv's policy since 2026 penalises unchecked AI-generated content: you must be able to stand behind every sentence.
2. Say "Publish" → Claude stages the Zenodo package (R9); you press Publish on Zenodo yourself; then the DOI goes into the paper (two places: Acknowledgements + arXiv comments) and the tarball is rebuilt.
3. arXiv: create an account if needed; get an endorsement for astro-ph.CO (send the drafted request yourself to someone whose work you genuinely cite); upload the tarball; paste the metadata; check the arXiv-built PDF.
4. PRD: submit via the APS portal (journals.aps.org/prd → Submit) with the PDF, the source tarball and the cover letter; pick PhySH subject terms (e.g. Inflation; Supergravity; Cosmic microwave background); add the arXiv ID.
5. Optional: choose suggested referees with no conflict of interest.

## Known weak points a referee may still press (disclosed in the paper)
- ε is fitted, not derived; its string origin is open.
- Frozen bands assume inefficient preheating; estimates (D641) support this.
- Superpartner window (covariant completion) rests on estimates: anomaly-mediated gauginos, initial conditions within ~12 e-folds of horizon exit.
- Affleck–Dine is a numerical estimate (thermal effects shown negligible); M ≫ M_P needs a protecting symmetry; the Weinberg operator at τ = i needs a flavour multiplet.
- In the covariant completion the modular-centre matter parity is lost; standard matter parity is assumed (D656–D657).
- The frozen D605 superpartner prediction (constant-W0 chain) differs from the covariant completion's; disclosed in the paper.
- r ≈ 5×10⁻⁴ can be excluded soon but confirmed only by a future σ(r) ~ 10⁻⁴ experiment.
