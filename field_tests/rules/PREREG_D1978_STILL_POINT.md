# PREREG D1978 — the still point, its inward and outward directions, and the 360° view (Danny 18:12; locked 21 Nov 2026 before running; repo at 089357b4)
Script: tools/loom/still_point.py. It uses the D1976 three-axis model and data.
- **The still point:** the best fit.
- **Directions:** the Fisher-matrix eigenvectors at the still point. INWARD (restoring) if the eigenvalue is > 1, meaning a unit-log step costs more than 1 in χ². OUTWARD (free) otherwise.
- **The 360° view:** Δχ² at radius 0.1 (in ln) at 36 angles in each plane S–T, T–U and S–U.
- This is a deterministic geometric analysis, not new evidence. It reports which combinations of the axes the data pin down and which are free.
