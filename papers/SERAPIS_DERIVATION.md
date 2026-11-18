# SERAPIS — derivation status (audited 17–18 Nov 2026)

Status as of D1252. Every number below was re-derived or recomputed during the node audit NA1–NA16 (D1233–D1252) and the web postulates PW1–PW2 (D1245, D1251). Labels: **[computed]** (code run tonight, locked), **[literature]** (fetched source), **[assumed]** (stated input, not derived), **[postulate]** (built from post-hoc choices; scored only on future data).

## 1. The chain in one line

String compactification on T⁶/(Z₂×Z₂) with stuck D3 branes → one-loop BHK Kähler correction ∝ E(U,2) → SERAPIS-E potential V/V₀ = P_E(1 + CÊ), P_E = Ê/(Ê+1), Ê = E(τ,2) − E(ρ,2) → vacuum at ρ (heavy inflaton) → reheating through the Γ₂ 2⊕1 heavy-neutrino sector → N* → (n_s, r, α_s) → leptogenesis, dark radiation, gravitino → wino, neutrino masses → tests.

## 2. Inputs and their status

| Input | Value | Status | Audit |
|---|---|---|---|
| Plateau origin (P_E placed in the uplift sector) | — | [assumed] | open (D1229 NULL for a 2026 string home) |
| Epstein zeta E(τ,2), minimum at ρ | E(ρ,2) = 5.7833592, E(i,2) = 6.0268120 | [computed] | NA11: direct lattice sum; isotropic minimum E_xx = E_yy = 7.7111 |
| Plateau approach | E(½+iy,2) → 2ζ(4)y² | [computed] | NA11: 1.000065 at y = 30 |
| Kähler weight of the inflaton | K = −ln(2 Im τ), n = 1 | [computed] | NA3/NA5: d²V/dφ² at ρ = 11.567 V₀ |
| BHK tilt | C = 15 N_eff/(64π⁶ Im S Im ρ) | [literature] + [computed] | NA11: reproduces C = 1.0–1.3e-6 for every tadpole row |
| Stuck-D3 tadpole | 3N + N₀ + N_flux = 16, (N, N₀) = (5, 1) | [literature] + [computed] | NA11 PASS |
| String benchmark | g_s = 0.232, Im S = 0.485, Im S·Im ρ₁ = 781 → C = 1.249e-6 | [computed] | NA12 PASS |
| Neutrino masses (NO, m₁ ≈ 0) | Σm_ν = 0.05878 eV (NuFIT 6.0) | [computed] | NA2 PASS (frozen 0.0587) |

## 3. Derived quantities (audited)

| Quantity | Before audit | Audited | Note |
|---|---|---|---|
| Inflaton mass at ρ | 2.2e13 GeV | **3.17e13 GeV** | D1235: old H* low ×1.44 |
| Inflaton coupling normalisation (ρ chain) | n = 3 (y√(2/3)) | **n = 1 (y√2)** | D1235/D1237: same field had two Kähler weights in D721/D722 |
| T_R at ρ | 3e8–3e9 GeV | **6.6e8–2.0e10 GeV** | D1239 (direct rerun, ≤ 0.15 % vs rescaling) |
| N* (SERAPIS-E, ρ) | 49.7–50.5 | **50.1–51.3** | D1234 (exact ε_H = 1 end, D979) + D1235 |
| Inflaton mass at τ = i | 1.9e11 GeV | **2.28–2.65e11 GeV** | D1241 (D730's computed value) |
| T_R at τ = i | 1–3e6 GeV | **1.3–5.0e6 GeV** | D1241 |
| N* at τ = i | 50.31 | **50.40–50.45** | D1247 |
| τ = i tilt window | ε 1.40–1.45e-4 | **ε ≈ 1.39–1.44e-4** | D1247 (exact MS) |
| Janus relation error (κ = 1, p = 2√2) | "13–16 %" (wrong model) | **3.3–4.0 %** (≤ 6 % frozen) | D1234, D1234a |

## 4. Predictions

**Frozen (D693, scored on future data):** n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4, N* 48.4–49.9, C 1.0–1.3e-6. Caps n_s ≤ 0.985, r ≤ 8.3e-4 (still valid, D1240).

**Audited box (PW1, D1245) [postulate]:** C 1.0–1.3e-6 × N* 50.1–51.3 → n_s 0.9717–0.9760, r (4.38–4.90)e-4, α_s −(9.1–10.1)e-4. Only 4 of 9 corners inside the frozen band.

**Point prediction (PW2, D1251) [postulate]:** leptogenesis (c = 1, M_H = 1e12 GeV) → T_R = 8.94e8 GeV → N* = 50.24; string benchmark C = 1.25e-6 →
**n_s = 0.97445, r = 4.81e-4, α_s = −9.97e-4** (inside the frozen band; CMB-SPA +2.0σ, CMB-SPA+DESI +0.6σ).

**τ = i variant:** ε ≈ 1.40e-4: n_s 0.97462, r 4.83e-4, α_s −8.54e-4 (D1247).

## 5. Side predictions (audited)

| Sector | Result | Audit |
|---|---|---|
| Leptogenesis at ρ | works for c ≳ 1 (41–64 % at M_H 1e12), fails c = 0.3 (2.2 %) | D1239 (+D1236a) |
| Leptogenesis at τ = i (radiative resonant) | PASS, 38–86 % / 42–86 % of the grid | D1243 |
| Dark radiation at ρ | none: light N's thermalise, margin ×55–376 | D1240 |
| Gravitino → wino | Ω_nth ≤ 4.4e-4 (≪ 0.01) | D1242 |
| Wino window | 0.67–1.85 TeV thermal, 5–41 % of DM | BLOCKED: g*(T) EOS table needed |
| Matter parity / covariant completion | PASS (mod-4 rule general; m₃/₂ bounds ρ = i to ≤ 3.3 %) | D1250 |

## 6. Tests

- **n_s (SO + SPHEREx, σ ≈ 0.0016, ~2030):** audited SERAPIS-E sits ≥ 3.1σ from the N* = 60 attractor and 2.5σ from the maximal-kination attractor; τ = i 5.0σ / 4.3σ (D1248).
- **r:** 4.4–4.9e-4 — visible only if LiteBIRD reaches its optimistic σ(r) ≈ 5e-5 (8.8–9.7σ); invisible at its δr = 1e-3 requirement.
- **α_s:** not a 2030 discriminant (σ ≈ 0.002).
- **Winos:** HL-LHC disappearing tracks reach 0.9–1.1 TeV only (1812.07831); 1.1–1.85 TeV needs the H.E.S.S./CTA line or a 27 TeV collider (D1249).
- **Σm_ν:** any robust bound below 0.0588 eV excludes normal ordering and SERAPIS's input together.
- **Late universe:** ΛCDM; DESI w0–wa pulls −2.8σ / +2.6σ (1-D) — the main open data tension (shared with ΛCDM) (D1252).

## 7. Toolkit cross-checks (TK1 complete, D1254–D1256; U1b D1255)

| Toolkit | Agreement with exact Mukhanov–Sasaki over the audited box (9 points) |
|---|---|
| Janus core, third-order flow | Δn_s ≤ 1.1e-6, Δr/r ≈ 0.011 %, Δα_s ≤ 3.3e-6 |
| Janus core, second order | Δn_s ≈ −1.6e-5 |
| Janus relation (κ = 1, p = 2√2) | α_s 3.4–3.5 % below exact (frozen bar ≤ 6 %) |
| Exact MS, compiled (U1b) | 0.9–3.8 s per 9-k spectrum (old path ≈ 570 s); α_s stable to 2e-5 |
| CAMB 2.0.5 | primordial-tensor D_ℓ^BB(80) = 2.7–3.0e-5 μK² for r = 4.4–4.9e-4 |
| Data pulls | CMB-SPA +1.5 to +2.5σ; CMB-SPA+DESI 0.0 to +1.2σ; r < 0.036 |

The old exact-MS α_s carried a start-condition ripple (bd = 200) at the 1e-4 level; fixed in U1b, recheck of older α_s quotes queued.
Wiring: every toolkit above sits in one shared registry (aegis_tools) used by the Janus app and by CubeMind; every app result and every collector point is stored in CubeMind's memory.

## 8. What is still open

1. Plateau origin (assumed) — the deepest open item.
2. Wino window — needs the Saikawa–Shirai g*(T) table (blocked by the network proxy; manual save needed).
3. τ = i: ε is fitted, not derived.
4. Frozen band vs audited box: post-hoc tension recorded (PW1); the frozen band is still what gets scored.
