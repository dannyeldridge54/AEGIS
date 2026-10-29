# S8 check (weak lensing): values fixed before computing (2026-10-29 09:01 CT)

S8 = σ8 √(Ωm/0.3). Two published cosmic-shear values. Both were verified by web search on 2026-10-29, before any
penalty was computed.
- A: DES Y3 + KiDS-1000 joint cosmic shear (DES & KiDS collaborations 2023, arXiv:2305.17173): S8 = 0.790 +0.018/−0.014
- B: KiDS-Legacy cosmic shear (2025; kids.strw.leidenuniv.nl): S8 = 0.815 +0.016/−0.021 (agrees with Planck at 0.73σ)

## Rule
- Penalty Δχ²_S8 = ((S8_Twist − S8_obs)/σ)² − ((S8_ΛCDM − S8_obs)/σ)². Use σ from the side the model falls on.
- Report A and B separately, never averaged.
- If the penalty is above 1 for either value, refit lcdmP, edelockP and edeP with an S8 likelihood (suffix `_s8`)
  for that value.
- A penalty against A but not B means the S8 verdict depends on which survey is right; say exactly that.
