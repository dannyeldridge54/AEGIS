# PREREG_D1636_PLANCK — DEVIATIONS (written before any rerun)
D1 (2026-11-19 16:11 CT, before gate rerun): the gate run computed its χ² but crashed writing JSON (numpy bool not serialisable);
no number was printed or seen. Fix: cast to Python float/bool before json.dump (output only). Nothing else changes.
Also (process, not science): the first queue file used a two-level workdir, which the PC runner cannot log; it never ran (moved to done/ as .badworkdir).
