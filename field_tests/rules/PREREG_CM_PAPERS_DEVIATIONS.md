# CM-PAPERS deviations (referee R80, written before fixes)
R80 MAJOR: P1 traces only N() outputs; input values and constants are literals in the prose, unchecked, so a changed argument or
engine constant would leave stale text while P1 passes. The supernova sentence omits t0 = 35 d. P4's chart-title claim was not tested.
MINOR: Th/Eu factor 46.7 Gyr vs engine 46.51 Gyr; mixed dex/linear stellar-age inputs; kilonova value is thermalised luminosity
(f_th = 0.5), normalisation from Metzger (2019) not Korobkin; "checked against analytic Bateman" for Ac-225 not backed by code;
Bi-213 97.8/2.2 vs ENSDF ~97.9/2.1.
Fixes (DEV-1): every input in the prose printed through I() from the call's own args, and every engine constant (half-lives, branching,
Way-Wigner coefficient, Th chronometer factor) read from the engine; P1 extended to check inputs (P1b) and constants (P1c); P4b
tests each chart has a title and y-label; supernova sentence states t0; kilonova labelled "thermalised luminosity (f_th = 0.5)"
with Metzger 2019 cited; star-age inputs labelled (dex observed; linear production ratio); Ac-225 analytic Bateman check added to the
test (P5) instead of claimed. Bi-213 branching: engine stays at 0.978/0.022 (changing it is a D2189 engine change); the note says
"97.8%/2.2% as used by the engine (ENSDF ~97.9/2.1)". One rerun.
