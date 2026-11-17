"""KALUZA — Kaluza–Klein masses and stability for 1D warped (Dudas–Mourad-type) compactifications.
v0.1 (17 Nov 2026), assembled from pieces validated in AEGIS: S4b background (D1015), S4c2/S4c3 tensor tower (D1036), convergence order (D1038),
scalar stability condition (D1140), scalar operator (S4e/D1141 — solver NOT yet validated against BTR's 2-sig-fig numbers; flagged).
Modules: background (general-D vacua, Basile–Thomée–Raucci 2209.10553 conventions), solvers (Prüfer shooting + finite differences),
spectra (tensor tower, scalar operator), convergence (Aitken + derived order), stability (BTR Eq. 5.10)."""
__version__ = '0.1.0'
