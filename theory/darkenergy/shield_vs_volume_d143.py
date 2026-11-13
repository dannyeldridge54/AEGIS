"""D143: the shield vs a volume-type T (D123). If T ~ (volume)^{2/3}, string alpha'^3 corrections (Becker-Becker-Haack-Louis)
shift the Kahler potential by ~ xi / V = xi / x^{3/2}, with xi = -zeta(3) chi(CY) / (2 (2 pi)^3). Reaching the SM costs at least one
loop if the SM is sequestered: c_p ~ xi / (16 pi^2). The clock limit for p = 3/2 (shield_tests_d142.txt) is c_p < 2.2e-5. AI-assisted."""
import math
lim = 2.2e-5; z3 = 1.2020569
for chi in (-2, -20, -100, -200, -300):
    xi = -z3 * chi / (2 * (2 * math.pi) ** 3); cp_tree, cp_loop = xi, xi / (16 * math.pi ** 2)
    print(f"Euler number {chi:>5}: xi {xi:.4f}; leak if unsequestered {cp_tree:.1e} ({'PASS' if cp_tree < lim else 'FAIL'}), "
          f"sequestered (one loop) {cp_loop:.1e} ({'PASS' if cp_loop < lim else 'FAIL'})")
print(f"needed: |xi| < {lim:.1e} unsequestered, or |xi| < {lim*16*math.pi**2:.1e} sequestered -> |chi| < {lim*16*math.pi**2*2*(2*math.pi)**3/z3:.1f}")
