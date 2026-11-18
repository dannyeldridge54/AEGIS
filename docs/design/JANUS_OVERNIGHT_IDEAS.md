# Janus and its associates: new toolkits and views (overnight plan, 18 Nov 2026)

Danny (22:41 CT): keep the Djl loops going on theory research, Janus and its associates. Overnight, work out new toolkits and visualizations for Janus and the others, using the same colours and look.

## Shared look (do not change)

**Background**
- Deep violet-black: #05010f, #04020b, #0b0620.
- Cards: rgba(6,2,20,0.7) with a 3 px border in the accent colour.

**Colour ramp**
- `PR(f)`: HSL hue 0.57 → 0.93 (blue → magenta), saturation 0.95, lightness 0.6.
- Low values are cyan-blue: #4cc3ff, #4f7dff, #6fb8ff.
- High values are magenta-pink: #ff4fd8, #d43cff, #ff6ec7, #ff3d8b.

**Neutral and accent colours**
- #a07bff and #7a5cff (violet).
- Text #f3eeff; secondary text #a296d8.

**Type and rendering**
- Segoe UI, bold 38 px titles on canvas sprites.
- three.js 0.128 with bloom.
- Wireframes at 0.25–0.35 opacity.

**Meaning of the colours**
- Colour encodes a value: cyan means low or early, magenta means high or late.
- Data from the theory glows; postulates pulse; killed nodes are grey and stay on the web.

## Toolkits (each one: profile → lock → build → equivalence test → adopt → register in aegis_tools → wire to the app and CubeMind)

1. **U6 — speed up the Janus-MF-NC / kaluza solvers** (already queued). This makes the two-field and Kaluza scans interactive.
2. **Inverse meter tool (`string_meter`)** in the registry. It takes n_s (± σ), T_R and the vacuum, and returns Im S·Im ρ, C, g_s and torus areas, with an exact inversion (PW6 method).
3. **Posterior-by-grid tool.** It turns the COLLECT grid (serapis_grid.csv) into a likelihood surface over (C, T_R) for any (n_s, r) measurement, so the app can answer "what does a measurement imply?" instantly.
4. **Reheating-chain explorer.** Given m_φ, couplings and g*, it returns T_R → N* → (n_s, r, α_s) and the leptogenesis pass fraction in one call, with each link's measured response from W1/W2 attached.
5. **Recheck queue runner.** It reruns every D-note quoting an exact-MS α_s through U1b, under one lock (ACCURACY_QUEUE item).
6. **CubeMind QA check (QA1).** Twenty physics questions with known D-note answers; measures hit@5 with the default weights and with similarity only (lock first).
7. **Hyperion late-universe pad.** A DESI/BAO residual plotter for ΛCDM vs w0wa at SERAPIS's Σm_ν; built on U4, fit in about 19 s.

## Visualizations (same look; each is a new tab or a lens in the app)

1. **Measurement lens on the Strings view.** A slider for n_s (and r) reshapes the torus live: tube length = y*, colour = Im S·Im ρ from the inverse meter, and the D3 stacks dim or brighten with C.
2. **Audit time-lapse** (offered). Replays D1233 → D1268 on the web: each node flashes when its status changes (corrected = magenta flash, killed = fade to grey, postulate = slow pulse), with a running ticker card.
3. **CubeMind memory stars** (offered). Each MindMem record is a star, placed by its embedding (PCA to 3-D), sized by importance and coloured by tier: EVIDENCE magenta, HYPOTHESIS cyan, quarantined grey. A query lights up the top-5 as constellation lines.
4. **Response ribbons.** The measured derivatives (∂n_s/∂ln C, ∂n_s/∂log T_R, …) drawn as ribbons flowing between input nodes and the (n_s, r) plane, with width proportional to strength in σ (data from W1/W2/PW5).
5. **Reheating river.** The inflaton decays into heavy-ν channels shown as a branching river; width = branching ratio, hue = temperature.
6. **Spectrum waterfall.** P(k) from exact MS, before and after the ripple fix: a 3-D waterfall over ln k with the bd = 200 ripple visible as interference fringes (the methods paper, made visible).
7. **Sky forecast dial.** Ellipses for Simons Observatory, SPHEREx and LiteBIRD around the point prediction on the (n_s, r) plane, with the attractor tracks and the CMB-SPA / DESI bands.
8. **Sound (optional).** Map the Strings torus y(N) to a falling tone and the D3 glow to chords; off by default.

## Overnight order

Each Djl tick does one item.
1. QA1 (lock) on CubeMind.
2. Measurement lens.
3. Memory stars.
4. Audit time-lapse.
5. Inverse meter tool plus registry entry.
6. Response ribbons.
7. U6.
8. Spectrum waterfall.
9. Sky dial.
10. Reheating river.

Research ticks (PW7 and onward) are interleaved.

Every view reads its data from data.js (make_data.py), which goes to the PC by device_commit_files to Desktop\AEGIS_PCJOBS\aegis_studio. Danny restarts Janus.bat to load the changes.
