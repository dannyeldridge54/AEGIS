# DEVIATIONS B4 (written before any rerun) — 2026-11-17
D1: Setting PRyM_init.Omegabh2 after import had no effect. Both runs gave identical output, so quantities derived from Omegabh2 at module import are cached. Every B4 number is therefore at PRyMordial's default Ωbh2 = 0.02230, not 0.02242.
Planned fix (for a B4b rerun, not done this tick): set Omegabh2 and recompute the derived quantities per PRyMordial's documented API, or edit a COPY of PRyM_init.py in scratch before import. The results file records the run as-is.
