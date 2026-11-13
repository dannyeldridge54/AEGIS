"""Development 96: is there ANY set of modular weights that makes every Standard-Model scale independent of x?
Fields per generation (MSSM): Q, U, D, L, E; Higgs Hu, Hd. Matter metric Z_r = (2x)^(-n_r); K = -3 ln(2x).
Conditions (one-loop Kaplunovsky-Louis + tree level):
  gauge a = 3, 2, 1:  -3 c_a + 2 sum_r T_a(r) n_r = 0, c_a = sum_r T_a(r) - T_a(G)   (1/g_a^2 independent of x)
  Yukawas: n_Q + n_U + n_Hu = 3, n_Q + n_D + n_Hd = 3, n_L + n_E + n_Hd = 3        (e^{K/2}/sqrt(Z Z Z) fixed)
  mu-term: n_Hu + n_Hd = 3                                                          (e^{K/2} mu / sqrt(Z Z) fixed)
Generation-universal weights assumed. U(1) in GUT normalisation (T = 3/5 Y^2 per Weyl state). AI-assisted."""
import numpy as np
# per-generation index sums T_a(r) (summed over all states of the multiplet), times 3 generations
T3 = {"Q": 2 * 0.5, "U": 0.5, "D": 0.5, "L": 0, "E": 0, "Hu": 0, "Hd": 0}
T2 = {"Q": 3 * 0.5, "U": 0, "D": 0, "L": 0.5, "E": 0, "Hu": 0.5, "Hd": 0.5}
Y2 = {"Q": 6 * (1 / 6) ** 2, "U": 3 * (2 / 3) ** 2, "D": 3 * (1 / 3) ** 2, "L": 2 * 0.25, "E": 1.0, "Hu": 2 * 0.25, "Hd": 2 * 0.25}
T1 = {k: 0.6 * v for k, v in Y2.items()}
gen = {"Q": 3, "U": 3, "D": 3, "L": 3, "E": 3, "Hu": 1, "Hd": 1}
F = ["Q", "U", "D", "L", "E", "Hu", "Hd"]; TG = {3: 3, 2: 2, 1: 0}
A, b = [], []
for a, T in ((3, T3), (2, T2), (1, T1)):
    c = sum(gen[f] * T[f] for f in F) - TG[a]
    A.append([2 * gen[f] * T[f] for f in F]); b.append(3 * c)
for row in (("Q", "U", "Hu"), ("Q", "D", "Hd"), ("L", "E", "Hd"), ("Hu", "Hd")):
    A.append([1 if f in row else 0 for f in F]); b.append(3)
A, b = np.array(A, float), np.array(b, float)
n, res, rank, _ = np.linalg.lstsq(A, b, rcond=None)
print("rank", rank, "of", len(F), "unknowns;", len(b), "conditions; residual", res)
for f, v in zip(F, n): print(f"  n_{f} = {v:+.4f}")
print("all conditions met:", np.allclose(A @ n, b))
r = A @ n - b
names = ["SU(3)", "SU(2)", "U(1)", "up Yukawa", "down Yukawa", "lepton Yukawa", "mu"]
print("best compromise residuals:", {k: round(v, 3) for k, v in zip(names, r)})
print("rank of [A|b]:", np.linalg.matrix_rank(np.column_stack([A, b])), "vs rank A", np.linalg.matrix_rank(A))
# drop each condition in turn: which single condition, if relaxed, allows an exact solution?
for i, k in enumerate(names):
    Ai, bi = np.delete(A, i, 0), np.delete(b, i)
    ok = np.linalg.matrix_rank(np.column_stack([Ai, bi])) == np.linalg.matrix_rank(Ai)
    print(f"  without {k}: exact solution {'exists' if ok else 'does not exist'}")
print("\nKeep everything except one condition; how far is the dropped quantity from fixed?")
kap = np.sqrt(2 / 3)
for i, k in enumerate(names):
    Ai, bi = np.delete(A, i, 0), np.delete(b, i)
    if np.linalg.matrix_rank(np.column_stack([Ai, bi])) != np.linalg.matrix_rank(Ai): continue
    ni = np.linalg.lstsq(Ai, bi, rcond=None)[0]; off = A[i] @ ni - b[i]
    if i < 3:   # gauge: d(1/g^2)/d ln(2x) = off/(16 pi^2); d ln alpha / d phi = -alpha * 16pi^2*d(1/g^2)... -> alpha*off/(16pi^2)*... per unit ln(2x); d ln(2x)/dphi = kap
        alpha = {1: 1 / 59, 2: 1 / 30}[3 - i]
        print(f"  drop {k}: d ln alpha_{3 - i} / d phi = {-alpha * off / (16 * np.pi ** 2) * kap * 4 * np.pi:.2e}  (atomic-clock / quasar bounds need ~1e-6 or less)")
    else:
        p = off / 2
        print(f"  drop {k}: that Yukawa (electron mass) goes as x^{p:+.3f}; d ln m_e / d phi = {p * kap:+.3f}; "
              f"MICROSCOPE estimate eta ~ (1.6e-5 * {p * kap:.2f}) * (2.7e-4 * {p * kap:.2f}) = {1.6e-5 * 2.7e-4 * (p * kap) ** 2:.0e} (bound 1e-15)")
