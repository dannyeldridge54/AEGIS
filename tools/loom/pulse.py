"""The pulsing Loom (Danny 17:12): mark every tension point, triangulate them ALL AT ONCE, test, re-read the compass, repeat.
Coupled state: knobs ln m3/2 (K_T) and ln T_R (S-T seam; derived value 3.7e8 is the start, it is treated as a knob here = postulate).
Tension points and their margins (log headroom; > 0 passes):
 P1 wino:          ln(M2 / 660 GeV), M2 = 686.5 (m3/2 / 2.58e5)
 P2 gravitino box: ln(0.12 / Omega_w), Omega_w = 0.017 (T_R/3.2e8)(M2/660)^p, three readings of p (D732 table): 1.44, 1.50, 1.54
 P3 leptogenesis (non-thermal, inflaton -> N N): need Br(phi -> NN) = Y_need / Y_per_Br <= 1;  margin ln(1/Br_needed)
    Y_per_Br = (28/79)(3/2)(T_R/m_phi) eps_DI, eps_DI = (3/16 pi) M_N m3nu / v_u^2; three readings of m_phi (below)
 P4 alpha_s seam (split stacks, D1940): margin ln(3 / max(r, 1/r)), r = A3/A2 = exp(2 pi dT/6), dT = 1/0.1180 - 1/alpha_s(m3/2)
    alpha_s(m3/2) = 0.11422 * (m3/2/2.58e5)^(-0.0254) (measured Jacobian, D1937)
Pulse: coordinate 3-point triangulation on (ln m3/2, ln T_R) maximising the MIN margin; a pulse is NULL when the state moves < 1e-4
and the min margin changes < 1e-4. Stop after 7 null pulses in a row (deterministic search: reported honestly as such)."""
import json, math, statistics
MP = 2.435e18; Vinf = 4.9e15 ** 4
# three readings of the inflaton mass at rho
m_a = math.sqrt(0.5625 * Vinf / 2.25) / MP          # D1926: m^2 = 0.5625 V0, plateau V_inf = 2.25 V0 (E ~ y^{3/2} ⇒ (3/2)^2)
H = math.sqrt(Vinf / 3) / MP                          # Hubble on the plateau
m_b = math.sqrt(0.5625 * 3 / 2.25) * H                # the same written through H (consistency reading)
Vr = 1.5 * math.pi ** 2 * 2.1e-9 * 5.4e-4 * MP ** 4   # V from r = 5.4e-4, A_s = 2.1e-9
m_c = math.sqrt(0.5625 * Vr / 2.25) / MP
m_phi = statistics.median([m_a, m_b, m_c])
MN, m3nu, vu = 1.844e11, 0.0502e-9, 174.0 * 2 / math.sqrt(5)
eps = 3 / (16 * math.pi) * MN * m3nu / vu ** 2
def margins(lm, lt):
    m32, TR = math.exp(lm), math.exp(lt); M2 = 686.5 * m32 / 2.58e5
    P1 = math.log(M2 / 660)
    P2 = statistics.median([math.log(0.12 / (0.017 * TR / 3.2e8 * (M2 / 660) ** p)) for p in (1.44, 1.50, 1.54)])
    YperBr = (28 / 79) * 1.5 * (TR / m_phi) * eps; P3 = math.log(YperBr / 0.87e-10)
    a_s = 0.11422 * (m32 / 2.58e5) ** (-0.0254); dT = 1 / 0.1180 - 1 / a_s; r = math.exp(2 * math.pi * dT / 6)
    P4 = math.log(3 / max(r, 1 / r))
    return dict(wino=P1, gravitino_box=P2, leptogenesis=P3, alpha_s_seam=P4)
state = [math.log(2.58e5), math.log(3.7e8)]; h = [0.2, 0.5]; log = []; nulls = 0; prev = None
for pulse in range(1, 400):
    for i in (0, 1):
        cands = []
        for d in (-h[i], 0.0, h[i]):
            s = list(state); s[i] += d; cands.append((min(margins(*s).values()), d))
        best = max(cands)
        if best[1] == 0.0: h[i] *= 0.5
        state[i] += best[1]
    mg = margins(*state); mn = min(mg.values())
    null = prev is not None and abs(mn - prev[0]) < 1e-4 and max(abs(a - b) for a, b in zip(state, prev[1])) < 1e-4
    nulls = nulls + 1 if null else 0
    log.append(dict(pulse=pulse, m32=math.exp(state[0]), T_R=math.exp(state[1]), margins=mg, min=mn, null=null,
                    pointing={k: ('●' if v > 0.3 else '◔' if v > 0 else '!') for k, v in mg.items()}))
    prev = (mn, list(state))
    if nulls >= 7: break
fin = log[-1]
out = dict(m_phi_readings=[m_a, m_b, m_c], m_phi=m_phi, two_MN=2 * MN, decay_open=m_phi > 2 * MN, eps_DI=eps,
           start=dict(m32=2.58e5, T_R=3.7e8, margins=margins(math.log(2.58e5), math.log(3.7e8))),
           final=fin, pulses=len(log), all_pass=all(v > 0 for v in fin['margins'].values()), log=log)
print(json.dumps({k: v for k, v in out.items() if k != 'log'}, indent=1, default=float))
json.dump(out, open('field_tests/results/d1941_pulse.json', 'w'), indent=1, default=float)
