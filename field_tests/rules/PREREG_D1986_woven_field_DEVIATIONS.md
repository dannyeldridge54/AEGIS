# D1986 DEVIATIONS: design details fixed BEFORE calibration and before the scored run
1. **Whitening.** z = (m − baseline)/sd inherits the running estimate's AR(1) memory (φ = 1 − 0.05 = 0.95). CUSUM on autocorrelated z would give random-walk false alarms.
   - The detector runs on whitened residuals w = (z − φ z_prev)/√(1 − φ²). A persistent step of s sd in z appears as about 0.16·s per pulse in w, which CUSUM accumulates.
   - **The shadows** (O3) run on iid N(0, 1) w plus probes of 2 sd in z (0.32 per pulse in w). They are fully independent of the scored stream.
2. **DONE (strict reading).** A FIT-kind goalpost, including one that passes, **blocks** DONE, in keeping with the endpoint rule that no fit poses as a prediction. The same goes for TRUST and NULL-kind goalposts: they do not block DONE, but they never count as predictions.
