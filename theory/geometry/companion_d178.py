"""D178: what does the rung-4 companion T_C of the G2 split (D177) do? AI-assisted.
Total K = -3 ln(T_A + Tbar_A) - 4 ln(T_C + Tbar_C) + (S terms). The inflation potential is V = e^K K^{SS} |W_S|^2, so it carries the factor
e^{K_C} = (2 x_C)^{-4}. In canonical units phi_C = sqrt(4/2) ln x_C, so V ~ exp(-4 phi_C / sqrt2): a runaway with slope 2 sqrt2.
If T_C is not stabilised it rolls away during inflation (epsilon_C = 4 >> 1). Stabilise it in a supersymmetric Minkowski vacuum
(Kallosh-Linde racetrack W_C = W0 (e^{-a T_C} - ... ) with W_C = dW_C = 0) with mass m_C; it then decouples if m_C >> H_inf."""
import math
k = 4; slope = k / math.sqrt(k / 2); eps = 0.5 * slope ** 2
print(f"unstabilised companion: V ~ exp(-{slope:.3f} phi_C), epsilon_C = {eps:.1f} -> runaway, inflation destroyed")
H = 1.5e13 / 2.435e18
print(f"needs m_C >> H_inf = {H:.1e} M_P ({1.5e13:.1e} GeV); then e^(K_C) is a constant absorbed into m and the Twist stays one light field")
print("a thawing companion is excluded: it would have to be light (m_C << H_inf) during inflation, where its slope 2.83 makes it run away")
# what if T_C were light today only (stabilised during inflation by a Hubble-induced mass)? then it would thaw with lambda = 1/sqrt(2)... rung 4
print("rung-4 thawing (if it were ever light late): w0 -0.93, wa -0.11 (rung_tails_d151) — excluded by the inflation argument unless its mass is Hubble-induced only")
