# DEVIATIONS A2d (written before any rerun) — 2026-11-17
D1: The first run crashed with NameError. gw.py imports G and c directly (`from .const import G, c, pc`), not as K. Fix: use G and c in taylorf2_tidal_dphase. No other change; no result was produced.
