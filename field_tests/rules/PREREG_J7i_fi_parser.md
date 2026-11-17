# PREREG J7i — FI rescored with a parser that reads Fortran 3-digit exponents (J7f D1035 listed fi on a parse error)
Locked 2026-11-17 before any J7i number. Only change: tokens of the form d.ddd+ddd / d.ddd-ddd (Fortran ES output drops the 'E'
for |exponent| ≥ 100) are read as d.dddE+ddd. Same ASPIC output file (theory/janus/aspic/pulse/fi/out.txt, unchanged), same
J7f method, exact reference and claims; reported as its own lines and added to pulse-1 totals with the source stated.
Pre-check already done (not a result): kmii's listed parse error is in ASPIC's own PT line (x* = 4.5e15, n_s = 1, x_end = 4.7e-310),
i.e. an ASPIC failure at those parameters, not my parser — recorded as a correction to D1035, kmii stays unscored.
