"""Mirror-Loom posterior fixes (PREREG_D1950, PREREG_D1951). One pass, no reruns.
Bearings are copied from sources opened 21 Nov 2026 (see LOOM_MIRROR_NOTES.md D1952/D1953).
Combiners: Gaussian product, Student-t (nu=3) product, PRIMARY good-or-bad mixture (p_good=0.8).
"""
import math
import numpy as np

NU, PGOOD = 3.0, 0.8


def gauss(x, c, s):
    return np.exp(-0.5 * ((x - c) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def student(x, c, s, nu=NU):
    z = (x - c) / s
    k = math.gamma((nu + 1) / 2) / (math.gamma(nu / 2) * math.sqrt(nu * math.pi) * s)
    return k * (1 + z * z / nu) ** (-(nu + 1) / 2)


def quant(grid, post, qs):
    cdf = np.cumsum(post)
    cdf /= cdf[-1]
    return [float(np.interp(q, cdf, grid)) for q in qs]


QS = [0.025, 0.16, 0.5, 0.84, 0.975]


def combine(name, bearings, lo, hi, n=200001):
    """bearings: list of (label, centre, sigma). Flat prior on [lo, hi]."""
    g = np.linspace(lo, hi, n)
    dx = g[1] - g[0]
    U = 1.0 / (hi - lo)
    out = {}
    LG = [gauss(g, c, s) for _, c, s in bearings]
    LT = [student(g, c, s) for _, c, s in bearings]
    LM = [PGOOD * l + (1 - PGOOD) * U for l in LG]
    for key, Ls in (("gauss", LG), ("student", LT), ("mixture", LM)):
        logp = sum(np.log(np.maximum(l, 1e-300)) for l in Ls)
        p = np.exp(logp - logp.max())
        out[key] = quant(g, p, QS)
    # weights
    w = np.array([1 / s ** 2 for _, _, s in bearings])
    wf = w / w.sum()
    mu = float(np.sum(w * np.array([c for _, c, _ in bearings])) / w.sum())
    chi2 = float(sum(((c - mu) / s) ** 2 for _, c, s in bearings))
    dof = len(bearings) - 1
    pval = chi2_sf(chi2, dof)
    # Bayes factor: one common value vs each its own value (same flat prior)
    Z1 = float(np.sum(U * np.prod(LG, axis=0)) * dx)
    Z0 = float(np.prod([np.sum(U * l) * dx for l in LG]))
    BF = Z1 / Z0
    # mixture good-probabilities
    allm = np.prod(LM, axis=0)
    den = np.sum(allm)
    pg = []
    for i, l in enumerate(LG):
        num = np.sum(PGOOD * l * np.prod([LM[j] for j in range(len(LM)) if j != i], axis=0))
        pg.append(float(num / den))
    out.update(weights=list(map(float, wf)), mu=mu, chi2=chi2, dof=dof, p=pval, BF=BF, pgood=pg)
    return out


def chi2_sf(x, k):
    # survival function via regularised upper incomplete gamma (series/continued fraction)
    a, xx = k / 2.0, x / 2.0
    if xx < a + 1:
        s, term, n = 0.0, 1.0 / a, 0
        tot = term
        while abs(term) > 1e-15 * abs(tot) and n < 1000:
            n += 1
            term *= xx / (a + n)
            tot += term
        P = tot * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
        return 1 - P
    b, c, d = xx + 1 - a, 1e300, 1 / (xx + 1 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1 / d if d != 0 else 1e300
        c = b + an / c
        h *= d * c
        if abs(d * c - 1) < 1e-15:
            break
    return h * math.exp(-xx + a * math.log(xx) - math.lgamma(a))


def lc(a, b):
    return 0.5 * (math.log10(a) + math.log10(b)), 0.5 * abs(math.log10(b / a))


def logb(label, lo, hi, matched):
    c, hw = lc(lo, hi)
    s = max(hw, 0.20) * (1 if matched else 2)
    return (label, c, s)


def verdict(ratio, b1=1.5, b2=3.0):
    return "PASS" if ratio <= b1 else ("PARTIAL" if ratio <= b2 else "FAIL")


def rpt(title, res, tolin=lambda v: v, unit=""):
    print(f"\n== {title}")
    for k in ("gauss", "student", "mixture"):
        q = [tolin(v) for v in res[k]]
        print(f"  {k:8s} median {q[2]:.4g}{unit}  68% [{q[1]:.4g}, {q[3]:.4g}]  95% [{q[0]:.4g}, {q[4]:.4g}]")
    print(f"  weighted mean {tolin(res['mu']):.4g}{unit}; chi2 = {res['chi2']:.2f} / dof {res['dof']}  p = {res['p']:.2e};"
          f"  BF(common/separate) = {res['BF']:.3g}")


# ------------------------------------------------------------------ TEST 1 (D1950)
print("TEST 1 — |dtau| off rho (log10 space); need 0.0457 (D1894b), superseded 0.090")
near_rho = [
    ("B1 IIB flux landscape 2206.04313 (typical, no range)", math.log10(1e-5), 0.50),
    logb("B2 heterotic S+tau+ISS 2304.14437 (AdS 0.024 / dS 0.075)", 0.024, 0.075, False),
    logb("B3 CW radiative A4 2310.15604 (0.0244..0.2)", 0.0244, 0.2, False),
    logb("B4 multi-modulus SUGRA King-Wang 2310.10369 (0.012 AdS/dS)", 0.0120, 0.0125, False),
    logb("B5 nilpotent-X SUGRA Fan-Wang-Zhang 2412.07642 (6.8e-6..6.6e-5)", 6.758e-6, 6.587e-5, False),
]
for b in near_rho:
    print(f"  {b[0]:64s} centre {10**b[1]:.3g}  sigma {b[2]:.2f} dex")
R1 = combine("rho", near_rho, -7.0, 0.0)
rpt("posterior |dtau| near rho", R1, tolin=lambda v: 10 ** v)
print("  weights (inverse-variance):", ", ".join(f"{w:.2f}" for w in R1["weights"]))
print("  mixture P(good):          ", ", ".join(f"{p:.2f}" for p in R1["pgood"]))
cat = {}
for k in ("gauss", "student", "mixture"):
    m = 10 ** R1[k][2]
    for need in (0.0457, 0.090):
        r = max(need / m, m / need)
        cat[(k, need)] = verdict(r)
        print(f"  {k:8s} need {need}: ratio {r:.2f} -> {verdict(r)};"
              f" in68 {10**R1[k][1] <= need <= 10**R1[k][3]}  in95 {10**R1[k][0] <= need <= 10**R1[k][4]}")
prim = cat[("mixture", 0.0457)]
frag = len({cat[(k, 0.0457)] for k in ("gauss", "student", "mixture")}) > 1
print(f"  VERDICT (primary mixture, need 0.0457): {prim}{' FRAGILE' if frag else ''}")
# 3-point comparison (main Loom D1908a/D1894b log-centres)
three = sorted([1e-5, 0.027, 0.069])
print(f"  3-point Loom fix: median {three[1]} -> ratio {0.0457/three[1]:.2f} -> {verdict(0.0457/three[1])}")

print("\nMIRROR 1 — dark/thread modulus off i; need |delta_i| < 5.9e-3 (n=1) / 3.4e-3 (n=3)")
near_i = [
    ("I1 IIB flux landscape 2206.04313 (typical)", math.log10(1e-5), 0.50),
    logb("I2 heterotic 2304.14437 (0.010..0.028)", 0.010, 0.028, False),
]
for b in near_i:
    print(f"  {b[0]:64s} centre {10**b[1]:.3g}  sigma {b[2]:.2f} dex")
M1 = combine("i", near_i, -7.0, 0.0)
rpt("posterior |delta_i| near i (THIN: 2 bearings)", M1, tolin=lambda v: 10 ** v)
print("  weights:", ", ".join(f"{w:.2f}" for w in M1["weights"]), "  P(good):", ", ".join(f"{p:.2f}" for p in M1["pgood"]))
for k in ("gauss", "student", "mixture"):
    m = 10 ** M1[k][2]
    r = m / 5.9e-3
    v = "PASS" if r <= 1 else ("PARTIAL" if r <= 3 else "FAIL")
    print(f"  {k:8s} median {m:.3g}: /5.9e-3 = {r:.3g} -> {v};  P(delta_i<5.9e-3) from 95% band: lo {10**M1[k][0]:.2g} hi {10**M1[k][4]:.2g}")
# same-mechanism balance: the dynamical bearings only (heterotic class), forward vs mirror
print("  same-mechanism balance (2304.14437 alone): rho 0.024-0.075 vs i 0.010-0.028; mirror need < 5.9e-3 -> ratio "
      f"{0.010/5.9e-3:.1f}-{0.028/5.9e-3:.1f}")

# ------------------------------------------------------------------ TEST 2 (D1951)
print("\n\nTEST 2 — volume-direction thread vs PPN gamma")
E = 1e-5
ppn = [
    ("G1 Cassini Shapiro delay (Bertotti 2003)", 2.1 * E, 2.3 * E),
    ("G2 INPOP13c + MESSENGER (Verma 2014)", -0.3 * E, 2.5 * E),
    ("G3 EPM2011 (Pitjeva & Pitjev 2013)", 4.0 * E, 6.0 * E),
    ("G4 INPOP20a PF (Fienga 2021)", 2.64 * E, 3.44 * E),
    ("G5 DE405 (Standish 2001)", 40.0 * E, 10.0 * E),
]
RG = combine("gamma", ppn, -1e-2, 1e-2, n=400001)
rpt("posterior gamma-1", RG)
print("  weights:", ", ".join(f"{w:.2f}" for w in RG["weights"]), "  P(good):", ", ".join(f"{p:.2f}" for p in RG["pgood"]))
B95 = max(abs(RG["mixture"][0]), abs(RG["mixture"][4]))
print(f"  B95 (primary) = {B95:.3g};  Cassini-alone 2-sigma |gamma-1| < 6.7e-5 (D1906)")

a = lambda beta: math.sqrt(2) * beta
coup = [
    ("C1 Weave n=1 torus, m ~ M_s (D1906a)", 0.50, 0.10),
    ("C2 Weave n=1 torus, m_e ~ v ~ m3/2 ~ V^-1 (D1906a)", a(2 * 0.3536), 0.20 * a(2 * 0.3536)),
    ("C3 overall no-scale volume n=3, m ~ M_s", a(0.5 * math.sqrt(1.5)), 0.40 * a(0.5 * math.sqrt(1.5))),
    ("C4 overall volume n=3, m ~ m3/2", a(math.sqrt(1.5)), 0.40 * a(math.sqrt(1.5))),
    ("C5 two factors n=2, m ~ M_s", a(0.5), 0.40 * a(0.5)),
]
for c in coup:
    print(f"  {c[0]:52s} alpha {c[1]:.3f} +- {c[2]:.3f}")
RA = combine("alpha", coup, 0.0, 2.0, n=200001)
rpt("posterior DEF alpha", RA)
print("  weights:", ", ".join(f"{w:.2f}" for w in RA["weights"]), "  P(good):", ", ".join(f"{p:.2f}" for p in RA["pgood"]))
gm = lambda al: 2 * al * al / (1 + al * al)
for k in ("gauss", "student", "mixture"):
    q = RA[k]
    gmed, glo = gm(q[2]), gm(q[0])
    r = gmed / B95
    v = "PASS" if r <= 1 else ("PARTIAL" if r <= 3 else "FAIL")
    print(f"  {k:8s} |gamma-1| median {gmed:.3f} (95% lower {glo:.3f}) / B95 = {r:.3g} -> {v}")
print(f"  smallest single bearing alpha=0.50 -> |gamma-1| = {gm(0.5):.2f} -> x{gm(0.5)/B95:.0f} over B95;"
      f" Cassini needs alpha < {math.sqrt(B95/2):.2e}")

print("\nMIRROR 2 — BBN: Delta ln(G m^2) = 2|beta| Delta_phi, Delta_phi = 0.64 M_P (D1853)")
bmed = RA["mixture"][2] / math.sqrt(2)
for lab, beta in (("C1 nucleon beta=0.354", 0.3536), ("posterior median beta", bmed)):
    d = 2 * beta * 0.64
    for blab, up in (("BBN+Ob h2 upper 1.05", math.log(1.05)), ("D+He only upper 1.04", math.log(1.04))):
        r = d / up
        v = "PASS" if r <= 1 else ("PARTIAL" if r <= 3 else "FAIL")
        print(f"  {lab}: Dln(Gm2) = {d:.3f} (G_BBN/G0 eff {math.exp(d):.2f}) vs {blab} (ln {up:.3f}) -> x{r:.1f} {v}")
print("  late-ladder check: D1906 Gm2 drift 2x1.8e-11/yr vs EPM2021 Gdot/G (0.85 +- 3.75)e-14/yr -> x%.0f" % (2 * 1.8e-11 / (2 * 3.75e-14)))
