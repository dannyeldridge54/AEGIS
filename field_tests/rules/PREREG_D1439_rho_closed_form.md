# PREREG D1439 — ρ analogue of D640 in closed form: first order in B/(A y²)

Locked 2026-11-19 (UTC) before the numerical check (JANUS tick 35, node janus).
Model: D1415's B-only model V/V0 = (1 − w)(1 + C(1/w − 1)), w = 1/(A y² + B) = 1/(Ê + 1), B = −4.7833, φ = ln y/√2,
so dw/dφ = −2√2 w(1 − Bw) exactly. D/y Epstein term dropped (relative size ~D/(A y³) ≈ 6e-4, stated).
Derivation [derived] (field_tests/scripts/d1439/derive_symbolic.py, sympy, first-order slow roll, C = t w², expanded at fixed t
to relative order w and Bw):
  1 − n_s = 16w(1 − t) + 8w²(5t² + 2t + 5) + 16Bw²(t − 3)
  r = 64w²(1 + t)²[1 + 2w(1 − t) − 2Bw]
  α_s = −128w²(1 + t)²[1 − 6w(t − 1) − 2Bw(t + 4)/(1 + t)]
  ⇒ closed form: α_s = −2r·[1 + 4w(1 − t) − 6Bw/(1 + t)], t = (ρ − 1)/(ρ + 1), w = (1 − n_s)/(16(1 − t)), ρ = 2√2 √(r/2)/(1 − n_s).
  Leading order reproduces D1399 (α_s = −2r) and the κ = 1 Janus x = t.
Disclosure: a rough hand evaluation at A1 (≈ +2 % vs exact) was seen while deriving, before this lock.
Tests at A1 (n_s 0.974393, r 4.82095e-4, exact α_s −9.9814e-4):
 (a) closed form vs D1415's numerical B-only first-order control (field_tests/results/D1415_rho_offset_relation.json, B_only.alpha):
     VALID if |α_cf/α_B-only − 1| < 0.3 % (closed form captures the model).
 (b) vs exact A1: PASS if |α_cf/α_A1 − 1| < 1 %, else FAIL (expected FAIL: first-order SR limit, D1415).
 Also report the pure-plateau piece 4w(1 − t) and offset piece −6Bw/(1 + t) separately.
No reruns to chase results; fixes only via PREREG_D1439_DEVIATIONS.md written first.
