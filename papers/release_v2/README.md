# UFE v2 release: arXiv and Zenodo

Paper: *Torsion-Born Early Dark Energy with an Onset Locked to Matter–Radiation Equality* (version 2, 19 pages).
Rebuild everything with `tectonic torsion_born_ede.tex` then `python make_release.py` in `AEGIS/papers`.

| Folder / file | Use |
|---|---|
| `torsion_born_ede_v2_arxiv.tar.gz` | **Upload this to arXiv.** The .tex plus `anc/` (34 ancillary files). Test-compiled from a clean folder. |
| `ARXIV_FORM.txt` | Copy into the arXiv form: title, abstract (1,752 of 1,920 characters), comments, category. |
| `zenodo/` | **Upload these to Zenodo** as a *new version* of 10.5281/zenodo.23789830. |
| `zenodo/.zenodo.json` | Metadata: title, description, keywords, links to the N = 9 and silver records. |
| `zenodo/SHA256SUMS.txt` | Fingerprints of the Zenodo files. |

## Three things only you can decide or do

1. **Wait for the SPT-3G free-width fit, or say "pending".** The fit (`spt_edelock`) was still running when this was
   built, so Table 8 and §14 say "still running". It is the direct SPT-3G counterpart of the P-ACT test. When it
   lands, fill the `\SPTfree…` macros at the top of the .tex, rebuild, and rerun `make_release.py`. The hourly loop
   does this automatically. Recommended: submit after it lands.
2. **Choose the license.**
   - The .tex header says *AEGIS People's License* (free for people; no AI use; no military or surveillance use).
   - arXiv only offers its own options. CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, or the arXiv non-exclusive
     distribution license are the usual choices; the last grants arXiv only the right to distribute.
   - Zenodo needs a license id in `.zenodo.json` (currently a placeholder). The Locked Twist record used CC BY-SA 4.0.
   - Note: the license's "no AI use" clause sits awkwardly beside the acknowledgement that AI assistants helped.
     Consider rewording it, for example to "no use for training AI models".
3. **arXiv endorsement and sign-in.**
   - First-time authors in astro-ph.CO need an endorsement. The paper README (`papers/README.md`) already asks for one.
   - You submit and sign in yourself; Claude cannot sign in for you.

## What changed from version 1 (29 October)

- **§14, SPT-3G D1:** N = 9 fails (Δχ² +0.52); the zero-parameter angle variant fails (+0.43); free width pending.
- **§13, checks of the computation:**
  - AxiCLASS and CAMB agree to 0.23 and 0.42.
  - The Floquet analysis with expansion finds growth of at most ×20, against the ~10⁵ fragmentation would need.
- **§12, profile in the divisor N:** minimum at N = 8 on P-ACT and N = 9 on Planck; N = 9 disfavoured by 1.11.
- **The rest:**
  - The abstract is rewritten to fit arXiv's 1,920-character limit.
  - The verdict and conclusions are updated, the date is fixed, and the citations to SPT-3G D1 and candl are added.
