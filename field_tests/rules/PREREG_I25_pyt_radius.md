# PREREG I25 — PyTransport NC at sphere radius R = 1.5 and 2 (item 25)
Locked 2026-11-17 19:00 CT. PyTransJNC_DQuad (compiled for JMF9) with p[2] = R (G = diag(R², R² sin²φ1)), same potential parameters and start (0.4, 26),
PyTransport slow-roll velocity, n_s exactly as jmf9_curved.ns_pyt (tol 1e-8 and 1e-10), N* = 55.
Read-out: if PyTransport gives a physical n_s (0.8–1.1) where mfms_nc gave −0.83 (R=1.5) / 3.49 (R=2) → SHARED BUG in mfms_nc (Janus-MF-NC), JMF9 scope restricted to R=1
and a fix needs its own lock; if PyTransport is also unphysical or fails → REAL/COMMON regime (not our bug).
