# PREREG D2174 — examine how we'd do on GIMPS trial factoring: wheel + small-prime sieve vs our D2005 N2 (TOOL benchmark)
Locked 2026-11-23 ~01:08 CT before running. Danny 01:05 "Examine how wed do here". Implements D2005 DEVIATIONS item 1.
New function tf_wheel(p, bits): k split into 4620 classes (4·3·5·7·11); keep classes with q=2kp+1 ≡ ±1 mod 8 and q not divisible by 3,5,7,11; within each class sieve k by small primes ≤ 2^13 before powmod.
Benchmark: 200 prime exponents p in [1e6, 1e6+20000) (first 200 primes there), TF to 2^40.
 C1 correctness: tf_wheel finds exactly the same smallest factor (or none) as the D2005 trial_factor on every p (both to 2^40). Any mismatch = FAIL.
 C2 speed: report the ratio of wall times (naive/wheel); prediction from GIMPS_STRUCTURE.md: 4–10×.
 C3 context: report our factor-candidates/s on one cloud core, and the known mfaktc order of magnitude (GPU, billions/s) as literature, labelled as such.
No prize or GIMPS claim; exponents are not GIMPS-assigned.
