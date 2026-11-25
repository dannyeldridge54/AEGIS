"""Reproduce the conditional loop-metric identities; not a stability solver."""

import sympy as sp


def check_zero(name, expression):
    result = sp.simplify(expression)
    if result != 0:
        raise AssertionError(f"{name}: {result}")
    print(f"{name}: verified")


def main():
    x, c = sp.symbols("x c", real=True)
    y, s = sp.symbols("y s", positive=True)
    m, n = sp.symbols("m n", real=True)
    gamma = sp.symbols("gamma", nonnegative=True)
    e = sp.Function("E")(x, y)
    k = -sp.log(2 * y) - sp.log(2 * s) + gamma * e / s
    kuu = (sp.diff(k, x, 2) + sp.diff(k, y, 2)) / 4
    kss = (sp.diff(k, c, 2) + sp.diff(k, s, 2)) / 4
    kus = (
        sp.diff(k, x, c)
        + sp.diff(k, y, s)
        + sp.I * (sp.diff(k, x, s) - sp.diff(k, y, c))
    ) / 4
    f = 1 + 2 * gamma * e / s
    check_zero(
        "K_UbarU",
        kuu.subs(sp.diff(e, y, 2), 2 * e / y**2 - sp.diff(e, x, 2))
        - f / (4 * y**2),
    )
    check_zero("K_SbarS", kss - f / (4 * s**2))
    check_zero(
        "K_UbarS",
        kus + gamma * (sp.diff(e, y) + sp.I * sp.diff(e, x)) / (4 * s**2),
    )

    term = y**2 / ((m + n * x) ** 2 + n**2 * y**2) ** 2
    check_zero(
        "single-term gradient norm",
        sp.diff(term, x) ** 2 + sp.diff(term, y) ** 2 - 4 * term**2 / y**2,
    )
    check_zero(
        "determinant lower-bound numerator",
        f**2 - (2 * gamma * e / s) ** 2 - (1 + 4 * gamma * e / s),
    )

    delta = ((c - 1) ** 2 + s**2 - 1) / s
    mixed = (sp.diff(delta, c, 2) + sp.diff(delta, s, 2)) / 4
    check_zero("S duality counterexample", mixed.subs({c: 1, s: 2}) - sp.Rational(3, 16))

    u, v, p, a, b, eta, z, w = sp.symbols("u v p a b eta z w", real=True)
    quadratic = (
        a * u**2 / 2
        + b * v**2 / 2
        + eta * (u - v) ** 2 / 2
        + z * (u**2 + v**2) / 2
        + w * p**2 / 2
    )
    hessian = sp.hessian(quadratic, (u, v, p))
    expected = sp.Matrix([[a + eta + z, -eta, 0],
                          [-eta, b + eta + z, 0],
                          [0, 0, w]])
    if hessian != expected:
        raise AssertionError(f"anchor Hessian: {hessian}")
    print("anchor Hessian: verified")
    print("Conditional identities only; see theory/COMMON_ACTION_CHECK.md.")


if __name__ == "__main__":
    main()
