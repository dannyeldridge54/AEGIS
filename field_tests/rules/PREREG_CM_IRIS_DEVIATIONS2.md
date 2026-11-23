# CM-IRIS deviations 2 (referee R80, written before fixes; no rerun of the locked I1-I4 numbers is used to change any verdict)
R80 MAJOR: (a) valueAt/headAt assume increasing x -> wrong readout for decreasing x; (b) valueAt reads raw arrays, so NaN x gives NaN
and null y (+null = 0) fakes a zero. MINOR: logy readout interpolates through dropped points and linearly in y; an all-nonpositive logy
series shifts indices; a single-point series is invisible. NOTES accepted: I1 samples only at column edges (weak test); DEV-2's stated
cause was imprecise (real cause: t = (xq - X[lo])/dX not exactly 0.37), and verdict.I4 carries no post-hoc flag.
Fixes (DEV-3): readout and tracer use the cleaned series (finite x, finite non-null y, y > 0 for logy), sorted by x; logy readout
interpolates in log10 y; empty series kept as placeholders (no index shift, readout NaN); single point drawn as a dot.
New checks added to the test as E1-E5 (edge cases above) and I1b (deviation sampled at 8 sub-pixel points per column), reported
separately; the locked I1-I4 verdict stays as recorded, with verdict.I4 now labelled "post-hoc (DEV-2)".
