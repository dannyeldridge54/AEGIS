# Pre-registration: does early energy survive when late dark energy is allowed? (ROUTE.md A3)

**Written:** 2026-10-31 21:36 CT (time from the clock), before any of the runs below was run.
**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Set-up

Engine: AxiCLASS (classy v3.3.0) for all four models, because CAMB cannot run its early-quintessence field and a w0-wa
fluid together.
- **Early:** the Locked Twist scalar field (n = 3), with its energy peak locked at equality.
- **Late:** a w0-wa fluid (CLP form, PPF; priors w0 in [-3, 1], wa in [-3, 2], w0 + wa < 0).

Data: Planck low-l TT/EE + Planck PR3 (ACT cut) + ACT DR6 CMB-only + ACT x Planck lensing + SPT-3G D1 lite + DESI DR2 +
Pantheon+, with the same calibration priors as the CAMB combined runs.

Fitting: bobyqa, best of 2 restarts, the same for all four models. Each restart starts near the CAMB best point of the
same model on the same data; the early+late model starts from spa_edelock plus w0, wa from spa_w0wa. Code:
`cmb-fit/axiclass/early_late_spa.py`.

| Run | Early | Late | Extra settings vs LCDM |
|---|---|---|---|
| `ax_spa_lcdm` | no | no | 0 |
| `ax_spa_w0wa` | no | yes | 2 |
| `ax_spa_edelock` | yes | no | 2 |
| `ax_spa_edelock_w0wa` | yes | yes | 4 |

## Rule (all chi2 from AxiCLASS, so engine offsets cancel)

**Main question:** with late dark energy already in, does early energy still earn its two settings?
- D = chi2(ax_spa_edelock_w0wa) - chi2(ax_spa_w0wa); dAIC_early = D + 4.
- **Early SURVIVES:** D < -4 and dAIC_early < 0.
- **Early NOT NEEDED:** D >= -1 (adding early energy gains almost nothing once late is allowed).
- **Mild:** in between.

**Cross-checks reported beside it:**
- AxiCLASS chi2(ax_spa_edelock) - chi2(ax_spa_lcdm) against CAMB's -5.63;
- AxiCLASS chi2(ax_spa_w0wa) - chi2(ax_spa_lcdm) against CAMB's -10.89.

They agree if within 1.0. If not, say so: the engines differ for these models on these data.

**Also reported:** f_EDE, theta_i, w0, wa, H0 for the early+late model, and whether w0, wa move towards -1, 0 when early
energy is added (Wang & Piao 2025 found early energy weakens the late signal).
