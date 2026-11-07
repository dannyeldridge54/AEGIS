# Spiral Twist theory note, Zenodo version 3

This release adds a bounded QCD-anomaly scale assessment to the BI axion-dilaton theory note. It preserves the
distinction between the derived supergravity kinetic geometry, the hypothesized Spiral Twist potential, and the
separate Nieh–Yan/QCD candidate.

## Files prepared for the Zenodo record

- `spiral_twist_note_v3.pdf` — compiled manuscript.
- `spiral_twist_note_v3.tex` — manuscript source.
- `spiral_twist_v3_supplement.zip` — version 2 supplement contents plus the reproducible QCD derivation, its
  parameter-scaling tests, the updated theory README, and the v3 manuscript source.
- `METADATA_v3.json` — proposed Zenodo metadata; it is a local form reference, not a record file.
- `SHA256SUMS.txt` — hashes for the files prepared for upload.

The QCD scale calculation uses the zero-temperature susceptibility and a fixed relativistic-degree-of-freedom
approximation. Its equality fraction is an analytic, small-angle estimate relative to total density; it is not a
thermal-QCD likelihood fit. No result from the still-running combined likelihood minimization is included.

Focused validation command:

```powershell
python -m pytest theory\test_bi_supergravity.py theory\test_bi_qcd_axion.py -q
```
