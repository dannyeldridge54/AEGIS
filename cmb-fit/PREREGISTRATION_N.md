# Pre-registration: is the field's width a whole-number fraction of the torsion value?

Written 26 October 2026, 19:10 CT, before any fit below was run. Danny Lee Eldridge, with Claude.

## The idea (a lead, not a derivation)

If the Barbero–Immirzi parameter acts as a gravitational θ-angle (Mercuri 2009, arXiv:0902.2764; arXiv:1005.1291; arXiv:1411.4793), its potential may come from torsional instantons. Instanton potentials are often periodic as cos(N·θ) with N a whole number, so the width becomes F = F_torsion / N, with F_torsion = √(3/2) M_Pl = 1.2247 M_Pl from our field definition.

## What we already know (disclosed)

The free Twist best fit has F = 0.13657 M_Pl (AxiCLASS derived `f_axion`, Planck 2018 + DESI DR2 + Pantheon+), so F_torsion / F = **8.97**. We noticed this before writing this file. So "N = 9" is **not** a blind prediction, and the scan below cannot by itself confirm it.

## The scan

Model: the Locked Twist (switch-on at matter–radiation equality, PREREGISTRATION_ZEQ.md) with F fixed to 1.2247/N (1% external constraint, its own χ² term removed before comparing).
N = 7, 8, 9, 10, 11 (whole numbers) and 8.5, 9.5 (half-number controls). Same data and settings as the free fit.

## What counts

1. **Can the data tell whole numbers apart?** From χ²(N), fit a parabola and find the Δχ² = 1 range in N. If that range is wider than ±0.5, the data **cannot** tell N = 9 from N = 8 or 10, and we say: "untestable with these data". No claim is made.
2. **If they can:** the result supports the whole-number idea only if the best N lies within ±0.15 of a whole number **and** both half-number controls fit worse than that whole number by Δχ² ≥ 1.
3. **Counting settings:** choosing N counts as one setting unless a physics argument fixes N beforehand. So "Locked Twist + F = 1.2247/N" has two settings (θ_i and N), the same as the Locked Twist. It cannot beat the Locked Twist on the fair score; it can only explain one of its numbers.
4. **The real test** is a physics derivation that gives N (for example an instanton charge) before looking, then the same scan on new data (Planck PR4 + ACT DR6 + SPT-3G).

## What we will say either way

- Untestable: "The data don't pin the width tightly enough to test the whole-number idea yet."
- Fails: "The width is not a whole-number fraction of the torsion value; the 8.97 was a coincidence."
- Passes: "Consistent with a whole-number fraction. Not evidence until N is derived from physics."
