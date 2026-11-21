"""D1946: three workstreams at once (Danny 17:22).
(a) Br(phi -> NN) from the inflaton S: M_N ∝ (Re S)^p ⇒ phi N N coupling c M_N/M_P, c = sqrt(2) p (K = -ln(S+S̄): d ln Re S / d phi = sqrt 2).
    Competing: phi -> gauge bosons through f = T + 9S: d ln Re f / d phi = sqrt2 · 9 Re S / Re f.
    Gamma_NN = m (c M_N/M_P)^2 /(16 pi) · (1 - 4M^2/m^2)^{3/2};  Gamma_gg = N_g (d ln Re f/d phi)^2 m^3 /(128 pi M_P^2).
    Three readings: p = 1, 2, 3 (each with N_g = 12, SM only, and 12 + 35, visible hidden SU(6) if it also carries S).
(b) A3/A2 ≈ 0.752 (D1940): three geometric readings — eta ratio of the two N=2 planes, |Z2|/|Z3| = 2/3, fixed-point count 3/4 (T²/Z3 vs T²/Z2).
(c) battery: A8 gravitino lifetime vs BBN; F10 moduli masses vs 30 TeV; E2 wino γ-lines (record the data status)."""
import json, math
MP = 2.435e18; m_phi = 4.93e12; MN = 1.844e11; ReS = 2 / math.sqrt(3) ** -1 if False else math.sqrt(3) / 2 ** 0  # placeholder fixed below
gs = 2 / math.sqrt(3); ReS = 1 / gs; Ref = 28.0
dlnf = math.sqrt(2) * 9 * ReS / Ref
ph = (1 - 4 * MN ** 2 / m_phi ** 2) ** 1.5
a = {}
for p in (1, 2, 3):
    c = math.sqrt(2) * p
    G_NN = m_phi * (c * MN / MP) ** 2 / (16 * math.pi) * ph
    for Ng in (12, 47):
        G_gg = Ng * dlnf ** 2 * m_phi ** 3 / (64 * math.pi * MP ** 2)  # DEVIATIONS: 64 pi (D1948)
        a['p%d_Ng%d' % (p, Ng)] = G_NN / (G_NN + G_gg)
br_need = 0.095
a_pass_natural = any(v >= br_need for k, v in a.items() if k.startswith(('p1', 'p2')))
# (b)
eta_rho, eta_i = 0.800579402820038, 0.76823
r_eta = (math.sqrt(3) / 2 * eta_rho ** 4) / (1.0 * eta_i ** 4)
b = dict(eta_ratio=r_eta, order_ratio=2 / 3, fixed_point_ratio=3 / 4)
need = 0.752; b_dev = {k: v / need - 1 for k, v in b.items()}
b_pass = [k for k, d in b_dev.items() if abs(d) <= 0.30]
# (c) A8: gravitino lifetime (all channels, MSSM: Gamma = (193/384 pi) m^3 / M_P^2)
m32 = 2.58e5; G32 = 193 / (384 * math.pi) * m32 ** 3 / MP ** 2; tau = 6.582e-25 / G32
A8 = dict(tau_s=tau, pass_=tau < 0.1, rule='hadronic BBN bounds vanish for tau < ~0.1 s (decay before n/p freeze-out/D formation)')
# F10: moduli masses (KKLT): m_T ≈ 2 x m3/2 (Kähler), complex structure / dilaton from flux ~ m3/2 · O(V^{?}) >= m3/2
x = 21.10; F10 = dict(m_T=2 * x * m32, m_flux_min=m32, bound=3e4, pass_=min(2 * x * m32, m32) > 3e4,
           note='the dark-energy thread is light by design (sequestered, D1887); its own BBN/fifth-force tests are the five must-tests')
E2 = dict(status='OPEN: H.E.S.S. wino analysis (1808.04388) is "not reliable below ~1 TeV"; 0.69 TeV non-thermal wino at 10-40 % of DM has signal ∝ f^2 = 0.01-0.16 of a pure wino; Fermi dwarf / continuum limit needed (next tick)')
out = dict(a_Br=a, a_pass_natural_p_le_2=a_pass_natural, b_ratios=b, b_dev=b_dev, b_within_30pc=b_pass, A8=A8, F10=F10, E2=E2)
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1946_three.json', 'w'), indent=1)
