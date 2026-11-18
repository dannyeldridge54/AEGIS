<!-- AEGIS-FP TLR42BXG2JJGD4YW · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# DEVIATIONS — PREREG_J7c_aspic_reheating

D1 (17 Nov ~04:47Z, after the J7c run): the lock's own [derived] step is wrong. From Martin–Ringeval Eq. 15,
−¼ ln(H*²/ε1*) + ¼ ln[3H_end²/(ε1* H*²)] = ¼ ln(3H_end²/H*⁴), so ΔN* = ln R_rad − N_0 + ln H* − ¼ ln(3H_end²)
(coefficient 1 on ln H*, not ½). With the correct coefficient the potential normalisation does NOT cancel: H* must
be physical, i.e. M⁴ fixed by the measured amplitude P* (Eq. 17: H*²/ε1* = 8π²P* at leading order). The J7c
reference and the Janus side both used the wrong equation; the run is VOID as a test (its ΔN* "errors" of ~5.5
e-folds for ASPIC are this slip, not ASPIC's). Results file kept and labelled VOID. Replacement: new lock
PREREG_J7c2 written before any rerun.
