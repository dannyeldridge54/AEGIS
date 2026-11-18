"""Exact q-expansion of Klein's j: j = E4³/Δ = q⁻¹ + 744 + 196884 q + … (integer arithmetic, no rounding).
Danny 2026-11-19 "extend past that into new territory": the moonshine layer of the SERAPIS circuit uses these coefficients."""
def _sig3(n): return sum(d**3 for d in range(1, n + 1) if n % d == 0)
def coeffs(nmax=5):
    N = nmax + 2
    E4 = [1] + [240*_sig3(n) for n in range(1, N + 1)]
    def mul(a, b): return [sum(a[i]*b[k - i] for i in range(k + 1)) for k in range(N + 1)]
    E4c = mul(mul(E4, E4), E4)
    P = [1] + [0]*N                                   # ∏ (1 − qⁿ)^24 = Δ/q
    for n in range(1, N + 1):
        for _ in range(24): P = [P[k] - (P[k - n] if k >= n else 0) for k in range(N + 1)]
    inv = [0]*(N + 1); inv[0] = 1                     # 1/P as a power series
    for k in range(1, N + 1): inv[k] = -sum(P[i]*inv[k - i] for i in range(1, k + 1))
    J = mul(E4c, inv)                                  # = q·j  → J[k] is the coefficient of q^(k−1)
    return {k - 1: J[k] for k in range(0, nmax + 2)}
if __name__ == '__main__':
    print(coeffs())
