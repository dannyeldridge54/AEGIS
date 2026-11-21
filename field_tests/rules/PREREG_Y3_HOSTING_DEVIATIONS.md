# PREREG Y3 — DEVIATIONS
## D1 (21 Nov 09:54)
The first run crashed in the final print (numpy bool not JSON-serialisable) before any result was shown. Fix: cast HOSTS to a Python bool. Method, seed and objective unchanged; rerun once.
