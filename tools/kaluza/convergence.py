# AEGIS-FP OBZG22NCE5V7ZTVN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Cutoff convergence (S4c3/D1036) and the derived order (D1038)."""
import math
def aitken(m1, m2, m3):
    d1, d2 = m1 - m2, m2 - m3; return m3 - d2*d2/(d1 - d2), math.log10(d1/d2)
def predicted_order(D, delta):
    """q = (D−2)/((D−1)(1+δ)): order of the ε-cutoff error for the tensor tower at the sin-end (D1038, matched 0.8446 vs 0.8442)."""
    return (D - 2)/((D - 1)*(1 + delta))
