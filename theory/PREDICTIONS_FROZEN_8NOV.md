# Frozen forward predictions, all current models (8 Nov 2026)

Computed with `theory/forward_predictions_cloud.py` from the stored best fits; no new data compared. Files: `theory/fpc_<run>.json`
(SHA-256 below). For validation step V1 (DESI DR3 BAO) and V2/V4 (Euclid, Rubin, growth). Scoring rules for these
comparisons still need locking (V1 rule) before the data are read.

Caveat (S8-LNL deviation D2): for S8-L, σ8, S8 and fσ8 come from CLASS's matter power, which in this build leaves the
ultralight field out (cold matter + neutrinos only). BAO, H0, r_d and w(z) are unaffected.

## DESI-like BAO, D_V/r_d at the DR2 effective redshifts

| Model | SN set | r_d [Mpc] | H0 | z=0.295 | z=0.51 | z=0.706 | z=0.934 | z=1.321 | z=1.484 | z=2.33 |
|---|---|---|---|---|---|---|---|---|---|---|
| ΛCDM | Pantheon+ | 147.54 | 68.17 | 7.964 | 12.712 | 16.332 | 19.820 | 24.356 | 25.866 | 31.282 |
| ΛCDM | DES-Dovekie | 147.59 | 68.27 | 7.953 | 12.697 | 16.316 | 19.804 | 24.342 | 25.853 | 31.273 |
| ΛCDM | Union3 | 147.56 | 68.10 | 7.969 | 12.719 | 16.340 | 19.827 | 24.362 | 25.872 | 31.286 |
| Spiral | Pantheon+ | 147.32 | 67.78 | 7.939 | 12.641 | 16.235 | 19.711 | 24.255 | 25.773 | 31.230 |
| Spiral | DES-Dovekie | 147.28 | 67.79 | 7.934 | 12.631 | 16.222 | 19.698 | 24.245 | 25.764 | 31.228 |
| Spiral | Union3 | 147.20 | 67.11 | 7.958 | 12.640 | 16.218 | 19.684 | 24.225 | 25.744 | 31.214 |
| S8-J | Pantheon+ | 147.43 | 67.87 | 7.934 | 12.639 | 16.235 | 19.712 | 24.256 | 25.774 | 31.228 |
| S8-J | DES-Dovekie | 147.38 | 67.78 | 7.930 | 12.627 | 16.218 | 19.693 | 24.238 | 25.757 | 31.221 |
| S8-J | Union3 | 147.42 | 67.25 | 7.948 | 12.633 | 16.214 | 19.682 | 24.222 | 25.741 | 31.207 |
| S8-L | Pantheon+ | 147.18 | 67.90 | 7.931 | 12.628 | 16.221 | 19.698 | 24.245 | 25.765 | 31.229 |
| S8-L | DES-Dovekie | 147.25 | 67.59 | 7.933 | 12.617 | 16.201 | 19.672 | 24.219 | 25.739 | 31.212 |
| S8-L | Union3 | 147.32 | 66.59 | 7.967 | 12.632 | 16.197 | 19.654 | 24.191 | 25.711 | 31.191 |

## Dark energy, clustering

| Model | SN set | w0 (CPL fit, z<2.5) | wa | min w | S8 | fσ8(z=0.5) | fσ8(z=1.0) |
|---|---|---|---|---|---|---|---|
| ΛCDM | Pantheon+ | — | — | — | 0.8175 | 0.4709 | 0.4316 |
| ΛCDM | DES-Dovekie | — | — | — | 0.8162 | 0.4708 | 0.4319 |
| ΛCDM | Union3 | — | — | — | 0.8168 | 0.4702 | 0.4307 |
| Spiral | Pantheon+ | -0.917 | -0.132 | -1.000 | 0.8326 | 0.4688 | 0.4328 |
| Spiral | DES-Dovekie | -0.910 | -0.144 | -1.000 | 0.8338 | 0.4685 | 0.4330 |
| Spiral | Union3 | -0.863 | -0.218 | -1.000 | 0.8395 | 0.4648 | 0.4299 |
| S8-J | Pantheon+ | -0.927 | -0.116 | -1.000 | 0.8221 | 0.4649 | 0.4291 |
| S8-J | DES-Dovekie | -0.911 | -0.141 | -1.000 | 0.8260 | 0.4651 | 0.4299 |
| S8-J | Union3 | -0.879 | -0.192 | -1.000 | 0.8269 | 0.4611 | 0.4263 |
| S8-L | Pantheon+ | -0.912 | -0.140 | -1.000 | 0.8170 | 0.4443 | 0.4108 |
| S8-L | DES-Dovekie | -0.886 | -0.182 | -1.000 | 0.8168 | 0.4404 | 0.4077 |
| S8-L | Union3 | -0.824 | -0.278 | -1.000 | 0.8190 | 0.4335 | 0.4015 |

## What would separate the models
- BAO: Spiral family vs ΛCDM differs by at most 0.60–0.68% in D_V/r_d (Pantheon+ fits), about the size of one DESI DR2 bin error, so DR3 alone separates them only in combination (all bins + w0–wa).
- Dark energy: Spiral family predicts w0 ≈ −0.82 to −0.93 with wa < 0 (thawing); ΛCDM w = −1.

## File fingerprints (SHA-256)

- `fpc_ax_spa_lcdm_halofit.json` 594d75b274549949a6c4a8cdcaca54ef231fa65684bb05aad7e5d1c09e4af345
- `fpc_ax_spa_lcdm_halofit_dovekie.json` 16bec680f572ce5088d1b7dba9a9b6282840c6d2072afeedef4d6db076e6b127
- `fpc_ax_spa_lcdm_halofit_union3.json` 0dbfb587c4d7a587141df9e2e110d95f858e05f7daa8cfffb82c98d79824da86
- `fpc_ax_spa_spiraltwist_dovekie_nlfix.json` 3e95e8879d5b762e50379c12473e599973e498a5fc2f76ede6bb8603b4c7cc65
- `fpc_ax_spa_spiraltwist_dovekie_nlfix_s8y6.json` 972cd9805621bcff38d1fbd41337b3be21dd580ba6903324c1245bf307585bf1
- `fpc_ax_spa_spiraltwist_nlfix.json` a8b57fbbe5cd59be4c2922a0d3f1d95ea09f095d6bbb0876f67a033734df3061
- `fpc_ax_spa_spiraltwist_nlfix_s8y6.json` 90bb3370bdcc28ffcef704f6d8152603bdfc665ff3e10656be1fe41e95118914
- `fpc_ax_spa_spiraltwist_union3_nlfix.json` a1206c1ea47f4d380cf665f24987d1fe5e0dd6d9a2a20b068ed1d4f40ad44317
- `fpc_ax_spa_spiraltwist_union3_nlfix_s8y6.json` 900b2d033c8fc6d8c6015ae7fcef7598282ca153209f94acea7d80af2888e7f4
- `fpc_spiralL.json` 9b04d937a4e02c6ced21d6ed9c48ef91a6f6ed34fa7056ae9e4fcd6939e02e97
- `fpc_spiralL_dovekie.json` cb37182f610bda3e5d9fc2f95f5b47ddddfb266da24a5fc21dcaf9078d722d34
- `fpc_spiralL_union3.json` 827bb655c23e0de28cd647421fbf29fa2cf2683e7c9dfc2549abf388e5498f88

## Added 8 Nov 16:55 CT: Locked Twist (early field, CAMB EarlyQuintessence n = 3; `forward_predictions_camb.py`, σ8 gate passed)
- Pantheon+: H0 70.53, r_d 143.16, S8 0.8252, D_V/r_d at z = 0.295/0.51/0.706/0.934/1.321/1.484/2.33: 7.940 / 12.682 / 16.301 / 19.791 / 24.333 / 25.846 / 31.275; fσ8(0.5) 0.4789. SHA-256 `fpc_edelockP.json` 99814d538db593af9f953ea1e6363e2d9eda540e0c9aad798d01b3064b8ba58b
- DES-Dovekie: H0 70.53, r_d 143.14, S8 0.8269, D_V/r_d at z = 0.295/0.51/0.706/0.934/1.321/1.484/2.33: 7.941 / 12.683 / 16.302 / 19.792 / 24.334 / 25.846 / 31.275; fσ8(0.5) 0.4799. SHA-256 `fpc_edelockP_dovekie.json` 7e048e980a97ef9756ce2088ac1c67f9d0a0f58b0593e4c5f843acf4e7b66819
- Union3: H0 70.55, r_d 143.22, S8 0.8255, D_V/r_d at z = 0.295/0.51/0.706/0.934/1.321/1.484/2.33: 7.936 / 12.677 / 16.295 / 19.785 / 24.327 / 25.840 / 31.270; fσ8(0.5) 0.4793. SHA-256 `fpc_edelockP_union3.json` 982e5c80e9876fbdb762d7097b4f97c3729446e292375a520f92e0bc1421fa3c
Note: these Locked Twist numbers were frozen after PREREG_V1_DESI_DR3.md was locked (20:58 UTC); V1 scores only the four models it names. The Locked Twist is scored with the same statistic and reported beside them, marked as frozen at 22:55 UTC, still before DR3.
