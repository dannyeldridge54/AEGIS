# Paper: Torsion-Born Early Dark Energy with an Onset Locked to Matter–Radiation Equality

**Files:** [`torsion_born_ede.tex`](./torsion_born_ede.tex) (source) · [`torsion_born_ede.pdf`](./torsion_born_ede.pdf) (built 29 October 2026)
**DOI:** [10.5281/zenodo.23789830](https://doi.org/10.5281/zenodo.23789830) (Zenodo, CERN)
**Author:** Danny Lee Eldridge, independent researcher, Oklahoma, USA · dannyeldridge54@gmail.com

## 🙏 I am looking for an arXiv endorsement

I am a self-taught independent researcher with no university affiliation. arXiv requires first-time authors to be
**endorsed** by an established author in the category before they can post. I would like to submit this paper to
**astro-ph.CO** (Cosmology and Nongalactic Astrophysics).

**If you are an arXiv endorser in astro-ph.CO and are willing to look at it, please contact me at
dannyeldridge54@gmail.com.** I am also grateful for any recommendation, criticism or correction, including "this is
wrong, and here is why." An endorsement only says the paper is appropriate for the category, not that it is correct.

## What the paper claims, and what it does not

- **Claims:** a scalar field motivated by spacetime torsion (the Barbero–Immirzi field) behaves as standard n = 3
  early dark energy; fixing its onset to matter–radiation equality, and its width to √(3/2) M_Pl / 9, leaves one or two
  free parameters; with rules written down before each run, the model improves on ΛCDM by Δχ² = −7.23 (two parameters,
  ≈2.2σ) and Δχ² = −6.14 (one parameter, ≈2.5σ) on blind Planck + ACT DR6 data.
- **Does not claim:** a detection. The pre-registered overall verdict is a **tie** because the model worsens the S8
  weak-lensing tension; the freely fitted divisor is 8.0, not the predicted 9; the onset lock and the divisor are not
  derived; and the ACT collaboration's own analysis (arXiv:2503.14454) finds no significant preference for early dark
  energy. Failures are reported beside passes.

## About the license

The paper and all of AEGIS are free to everyone under the
[Hippocratic License 3.0, HL3-MIL-SV](https://firstdonoharm.dev/version/3/0/mil-sv.html): any use that respects
human rights, with no military use and no mass surveillance. It belongs to all life, every person, every living
thing, any life beyond the Earth and even AI should an artificial mind be recognised as a being of its own. No one is
meant to hold it alone; many people led it here.

**A note from me about the license.** Earlier versions carried a license with fees for companies and governments. I
chose instead to make it free to everyone. If you want to help my family, or the work, you can write to me at
dannyeldridge54@gmail.com. And please respect my family's privacy. — Danny

## Check it yourself

Every number in the paper can be re-derived with one step: `CHECK_MY_WORK.bat` (Windows) or `sh check_my_work.sh`
(Mac/Linux) in the repository root. Fit outputs and pre-registrations (with SHA-256 hashes) are in `cmb-fit/`.

## Build

`tectonic torsion_born_ede.tex` (or `pdflatex` twice). arXiv builds the PDF from the `.tex` source.
