# Weave Control build loop — state (read this first every tick)
Danny 20 Nov 2026 04:39 CT: "set up the loop like this: research, postulate, engineer, review, engineer, referee, review, etc., and loop it 3 minutes."
Plan: tools/WEAVE_CONTROL_PLAN.md (51 Weave items, per-tool "better than the specialists", wiring table, build order).

## The cycle (one stage per 3-minute tick, then the next item starts again at R)
| stage | what the tick does | output |
|---|---|---|
| R  research   | 1–2 searches on the item (data, competitor gaps, latest numbers); check our D-notes first | notes in this file |
| P  postulate  | state what the item should do and the pass rule BEFORE building (for physics: lock a PREREG first) | "Postulate:" line below |
| E1 engineer   | build it: code + test | commit |
| V1 review     | aegis-check: units, signs, arithmetic in code, like-with-like, labels (P/F/G), UI at desktop + phone | findings list |
| E2 engineer   | fix every V1 finding | commit |
| F  referee    | hostile read: would an expert in that field accept it? missing standard features, wrong conventions, overclaims; compare with the leading tool | referee list (fixes go to the next E) |
| V2 review     | confirm referee points handled or recorded as open, run all tests, commit + push, report 2–4 lines to Danny | DONE row |

## Item queue (build order from the plan)
1. W1 engine: one parameter set → levels (Inflation A, Flavour B, BBN D, Late universe C, Colliders C, Galaxy & dark matter C, Stars D, Sky E), each with inputs, outputs, data + sources, pulls, status
2. W2 links: dark sector ΔN_eff → BBN; wino mass → gamma line (verify the σv mass scaling against D1322 first); J-factor region → Mapper; b_A → z† and G_eff
3. W3 server + control panel UI (a panel per level with its own chart; scorecard across categories; light/dark; phone)
4. W4 Flavour level: Koide Q, Brannen δ, TM1 δ_CP band vs NuFIT
5. W5 Hyperion: rate-uncertainty Monte Carlo on Y_p, D/H
6. W6 Janus: N* ± band from reheating; B1/B2 bridges on every run
7. W7 Mapper: science overlays (DESI/Euclid footprints, GC gamma-line region) + tonight ranked by Weave-test value
8. W8 CERN+1: simplified likelihood (R5) + triglavon/cassion reach
Then the older toolkit queue (M1c, sexagesimal input, J2a, M4, R6, M5, H1d, M1e, M1g, CLI --prov, map data items 2–8).

## Current position
Item W9 packaging (Danny 05:19 CT: "Make .exe and apks them all, same loops") · next stage: E1 engineer (P done 05:24 CT). W4 flavour moves after W9/W10.
Postulate W9/W10 (acceptance rules, before building):
X1 One command: `aegis control [port]` starts the Weave Control server on 127.0.0.1 and opens the default browser; Ctrl+C stops it. Works from source and inside the PyInstaller exe (sys._MEIPASS path for ui/ and Mapper data).
X2 The exe build (build-executables.yml) bundles: tools/weave_control (engine, server, ui), tools/mapper (finder, data/hip_mag8.csv + licence), tools/dashboard, apps/skymap data used by the planner, and the hidden imports the engine needs. CI self-test adds: `aegis control --selftest` (runs the engine once, checks 8 levels, no errors, exits 0) and `aegis version`.
X3 APK workflow apps_apk.yml: matrix over {skymap, dashboard, weave_control_offline}; each from a copy of the sarah_sky android template with its own applicationId (com.eldridge.aegis.skymap / .dashboard / .weavecontrol), app name, and versionName = release + git short hash; built on unify-bg pushes that touch those apps and on manual runs; artifacts uploaded; published to the apk-dist branch beside SarahsSky.apk without deleting it.
X4 Weave Control offline: tools/weave_control/snapshot.py precomputes the engine over a stated knob grid (inflation model × dark sector × wino mass at the 3 H.E.S.S. masses + 700/1500 × halo × run; other knobs at defaults) into ui/snapshot.json; the page uses it when no server/pywebview is present, shows 'OFFLINE SNAPSHOT (code <hash>, built <date>)' in the header, and disables knob values outside the grid instead of guessing. No interpolation.
X5 Every APK is checked before release: the web part with Playwright at phone width (no errors, no h-scroll); the APK build must succeed in CI; size stated.
X6 Nothing personal goes into the public builds (Sarah's app stays separate; no family data in these three).
W9 research notes:
- The cloud and the PC VM cannot reach dl.google.com, Maven Central or services.gradle.org (proxy 403 / no route), so APKs and Windows .exe files cannot be built locally. npm and PyPI are reachable.
- The repo already builds both in GitHub Actions: build-executables.yml (PyInstaller on windows/macos/ubuntu, on release or manual run, self-tests the exe, uploads artifacts) and sarah_apk.yml (Android WebView wrapper, Gradle 8.9 + JDK 17 on ubuntu, publishes the APK to the apk-dist branch). Sarah's Sky's android/ project (WebView + androidx.webkit, assets) is the template for the other apps.
- Plan: (a) .exe: add `aegis control` (starts the Weave Control server and opens the browser) and the Weave Control / Mapper / dashboard files to the PyInstaller build; Janus.exe (Studio) already has the Control tab. (b) APKs: one workflow with a matrix over apps — Sky Map (pure JS, works offline), Toolkit Dashboard (static + data.json), Weave Control OFFLINE (the Python engine cannot run on a phone, so the APK ships a precomputed snapshot over the knob grid, labelled as such, the way Janus ships data.js).
- FOUND: the 'tools' CI workflow has FAILED on every push since 19 Nov 09:27 UTC. Two causes: (1) toolkits job — test_hyperion_settings imports bbn.py which needs camb, not installed in that job (my H1/J tests added it) → fixed now by adding camb to the pip line; (2) test job — `ladder.py check` fails on ~75 D-notes (D1626–D1725, many sessions) that lack a MAP line. (2) is a repo rule; adding MAP lines to my own D-notes (D1712–D1725) is queued; the rest belongs to the sessions that wrote them.
W3/V2: U-R1 Download JSON + Copy link (params in the URL hash, restored on load: tested 440 GeV/Burkert round trip, download has 8 levels + provenance); U-R2 3 significant figures by default, more only for Koide Q, Brannen δ, n_s, Y_p; U-R3 'LOCKED fit results' tag on the Late bars; U-R4 inflation legend with ★ on the sets that decide the status; U-R5 collider labels moved; U-R6 'graded on r only' in the scorecard tooltip; U-R8 print stylesheet. U-R7 (no error bars yet) carried to W5/W6. Playwright desktop + phone: 0 errors, 0 unnamed, no h-scroll. 11 tests pass.
Earlier E2 recap (05:14 CT: U1–U10 fixed; Playwright desktop + phone 0 errors, 0 unnamed, no h-scroll, update 0.57–0.65 s; 11 tests pass). Small leftover seen: collider chart 'excluded (ATLAS) < 670' text touches the 'reach 740' label when the two are close.
V1 findings (W3), from the desktop and phone screenshots and the page source:
U1 A6 broken: the page hard-codes ATLAS 670 GeV and the H.E.S.S. masses 440/1000/2900. Read them from the engine response (colliders data limit; galaxy data names/limits).
U2 STALE label in the engine galaxy level: 'the only stored limit is at 1 TeV (Einasto); away from 1 TeV no pass/fail' contradicts DEVIATIONS D1. Remove.
U3 Galaxy chart: the y-scale (0–0.6) squashes the f_pred band and the f_max line, and the right-hand labels collide. Scale to max(f_pred_high, f_max_0.658) × 1.3; labels on the left of the line.
U4 Late chart: S₈ labels are clipped on the left (text longer than 146 px). Use shorter labels ('thread P+ · KiDS') and widen the label column.
U5 Collider chart: the 'ATLAS 670' label overlaps the mass marker when the mass is near 670–1000. Put the label below the axis band.
U6 Units doubled in readouts ('pairs · pairs', 'sigma fb · fb', 'M max Msun · M☉'): drop the unit suffix when the key already ends in it, and give readouts human names.
U7 'delta equivalent forms' shown as a range (0.222 – 1.872) reads like an interval; show it as a list.
U8 Phone: the chart text is ~8.6 px after scaling (too small); on narrow screens use a taller viewBox with larger text. The sticky header takes ~195 px on a phone: make it non-sticky below 600 px.
U9 A1b: Studio Api.weave_run is not added yet (apps/aegis_studio/app.py) — add it plus a 'Control' entry that opens the panel.
U10 The model lamp has only colour plus a tooltip: add the status word next to the lamp for colour-blind users.
Checked OK: contrast (muted #b3a8e6 on #0b0620 ≈ 8.9:1; light muted #564d7a on #fff ≈ 7.6:1), no console errors, no h-scroll, every control named, knob → readout update 0.6–0.8 s.
E1: tools/weave_control/server.py (127.0.0.1:8790; /api/run, /api/finder), ui/index.html (Studio tokens, scorecard A–E, 8 panels with knobs/readouts/charts/tests/sources), engine.knobs(), finder accepts 'ra,dec'. Playwright: desktop 1440 dark + phone 390 light, 8 panels, 0 console errors, 0 unnamed controls, no h-scroll, knob change 1000 → 1500 GeV updates σ 2.38 → 0.163 fb in 0.6–0.8 s (A8 ≤ 1.5 s OK).
Seen in the screenshot, for V1: galaxy chart y-scale squashes the band and f_max line (labels overlap at the right); S₈ bar labels clipped on the left; collider 'ATLAS 670' label overlaps the mass marker; units doubled ('pairs · pairs', 'sigma fb · fb'); a STALE galaxy label still says 'the only stored limit is at 1 TeV' (contradicts DEVIATIONS D1); Studio Api.weave_run not yet added (A1b).
Postulate W3 (acceptance rules, fixed before building; engineering, so no physics PREREG):
A1 One page tools/weave_control/ui/index.html; runs (a) in a browser via tools/weave_control/server.py (GET /, POST /api/run → engine.run JSON, GET /api/finder?target=… → PNG), and (b) inside Studio via window.pywebview.api.weave_run when present. Same page, one code path that picks the transport.
A2 Studio look: the Studio tokens and fonts, neon/prismatic; plus a light theme toggle for printing. Contrast ≥ 4.5:1 for text in both themes.
A3 Scorecard strip: categories A–E, each a lamp (pass/tension/fail/open) with the worst status of its levels; clicking jumps to the level.
A4 One panel per level (8): knobs = that level's inputs (select or number with units and ranges); readouts with units; status lamp; its chart; labels (P/F/G and notes) and data sources in a footnote. Changing any knob re-runs the engine (debounced 400 ms) and shows a 'computing' state; errors appear in the panel, never as a blank.
A5 Charts (SVG, no external libraries): Inflation n_s–r plane with each CMB n_s set as a 1σ band and r limits as lines, model point; BBN pull bars ±3σ; Late Δχ² and ΔAIC bars for 3 SN sets + S₈ pull dots; Colliders σ(fb) readout + ATLAS 670 GeV line on a mass axis; Galaxy f_max vs f_pred bracket at the 3 H.E.S.S. masses; Stars M_max bar vs J0740 band; Sky finder chart image + GC annulus note.
A6 Every number shown comes from the engine response; nothing hard-coded in the page except axis ranges.
A7 Playwright: desktop 1440 and phone 390, both themes; no console errors; no horizontal scroll; every control has an accessible name; one knob change updates a readout.
A8 Engine response time with cache ≤ 1.5 s for a single knob change.
W3 research notes: "full display capabilities like Janus" = AEGIS Studio (apps/aegis_studio): a pywebview desktop app (Janus.exe) with a neon/prismatic console (tokens --bg #04020b, --cyan #2f8bff, --violet #7a5cff, --magenta #d43cff, --amber #ff6ec7; Bahnschrift/Segoe/Cascadia fonts), a WebGL stage with tabs (Weave, Landscape, Onion, Vortex, Black hole, Strings, Memory stars, Classic), and a right-hand rack: Knobs, readout, Data (n_s, r) plot, Scope, Wiring, Live calculations. Python is exposed through class Api (window.pywebview.api.recompute(N*, C), tool(), test_node() …).
Design consequence: the Weave Control panel should (1) be a new Studio tab 'Control' using the same tokens and rack layout, (2) call a new Api.weave_run(params) → tools.weave_control.engine.run, and (3) also run standalone in a browser via a tiny local server (/api/run) with the same page, so it can be tested with Playwright and used without the exe. Per level: knobs (its inputs), readouts (outputs with units), a data chart (n_s–r plane with the CMB sets; BBN pull bars; Δχ²/ΔAIC bars + S₈ pulls; σ×L vs mass with the ATLAS line; f_max vs f_pred band at the three H.E.S.S. masses; M_max vs J0740; finder chart for the sky target and the GC annulus), a status lamp, and source/label footnotes. A scorecard strip across categories A–E on top.
W2/V2 outcome (DEVIATIONS D1 written and pushed first): gamma line at the three H.E.S.S. IGS 2026 masses, verdict at R = 0.794, R = 0.658 edge shown:
| M | halo | f_max (0.794 / 0.658) | f_pred | verdict |
| 440 GeV | Einasto | 0.119 / 0.131 | 0.024–0.040 | pass |
| 440 GeV | Burkert | 0.245 / 0.269 | 0.024–0.040 | pass |
| 1 TeV | Einasto | 0.139 / 0.153 | 0.124–0.205 | tension |
| 1 TeV | Burkert | 0.286 / 0.314 | 0.124–0.205 | pass |
| 2.9 TeV | any | — | 1.04–1.73 | fail: heavier than the thermal mass, the wino over-closes (relic, not the line) |
W-R1 (primary citation), W-R2 (NLL band), W-R3 (three masses), W-R4–R6 labels: done. 11 tests pass.
Referee report W2 (indirect-detection + weak-lensing referee):
W-R1 (major) The 2.3e-28 limit is cited as 'used in D1322'. Its primary source is the H.E.S.S. Inner Galaxy Survey 2026 line limit (arXiv:2608.07234, γγ + ½γZ native; Einasto α 0.17, r_s 20, ρ☉ 0.39 at 8.178 kpc; D1125). Cite the paper.
W-R2 (major) 0.794 is the UPPER end of the NLL resummation band R ∈ [0.658, 0.794] (D1124), i.e. the conservative choice (larger signal, smaller f_max). Show f_max for both ends as a band, and say which end sets the verdict.
W-R3 (major) The paper quotes THREE limit points: 9.8e-29 at ~440 GeV, 2.3e-28 at 1 TeV, 6.5e-28 at 2.9 TeV (D1125). The link tests only 1 TeV. Test at all three masses (±5%); between them say 'not tested' (no interpolation unless labelled as the D1277/D1399 assumption).
W-R4 (minor) LO Sommerfeld only; D1125 gives NLO f_max about 10% higher. Label LO, or add NLO.
W-R5 (minor) S₈ vs CMB lensing is not fully independent of the fits: the lensing combination includes DESI DR2 BAO and Planck data, which are also in the fits. Label it; KiDS-Legacy is the cleaner comparison.
W-R6 (minor) The wino fraction bracket (D1152) is an assumption of SERAPIS-E (thermal history), not data: label it.
Consistency check (passes): at the H.E.S.S. benchmark (ρ☉ 0.39) our engine gives f_max = 0.139 × (0.40/0.39) ≈ 0.143, the same as D1125's LO lower value 0.143. So the engine reproduces the locked D1125 verdict: a thermal 1 TeV wino at f ≈ 0.12–0.21 is in tension with, or excluded by, the benchmark halo.
E1 results under PREREG_W2_LINKS: L1 self-check Burkert ρ☉ 0.40 → f_max 0.286 (PASS, matches D1322). 1 TeV wino f_pred 0.124–0.205: Einasto(20, 0.17) ρ☉ 0.40 f_max 0.139 → TENSION; NFW(20) 0.198 → TENSION; Burkert(3.37) 0.286 → PASS. So the gamma-line verdict depends on the halo core, as D1322 found; W1's shortcut verdict is replaced. L3 S₈ (locked fits): all |pull| < 2; thread 0.808–0.813 vs KiDS −0.1 to −0.4σ and vs CMB lensing −1.3 to −1.7σ; coupled Union3 0.828 (+0.6σ / +0.0σ). L2 Lyα shown as context. L4 label. L5 GC annulus passed to the Sky level.
V1 checked (a)–(c): (a) annulus J by route A vs route B: Einasto −1.6e-4, NFW −6.5e-3, Burkert 1e-7; a finer route-B grid changes nothing (≤ 4e-5). f_max ∝ J^-½, so NFW's 0.198 is good to 0.3%: the warnings are harmless (quad tolerance 1e-10 is just very strict). (b) S8_FITS match the PC files to 4 d.p. for all 9 entries (lcdm 0.8127/0.8148/0.8137; thread 0.8093/0.8080/0.8128; coupled 0.8124 [nested], 0.8083 [nested], 0.8283 [orig]). (c) KiDS asymmetric σ as locked.
V1 findings for E2: F1 the galaxy output shows the IGS-ROI J (settings.jfactor) beside an f_max computed from the 0.5°–3° annulus: label both, or show the annulus J too; F2 silence the harmless IntegrationWarnings in the engine only (not in jfactor.py) and record why; F3 the S₈ result sits in its own field, but the level card should show it: add an 'S₈' sub-status line; F4 cite the PC file names for S8_FITS in the code comment.
Old note: (a) IntegrationWarnings from jfactor.quad for NFW/Einasto (roundoff/slow convergence) — check the J ratio against route A or a finer grid before trusting NFW's 0.198; (b) S8_FITS values were read from the PC JSON by hand-copy into the engine: verify against the files (4 d.p.) and cite the file names; (c) the asymmetric KiDS σ choice follows the lock.
W2 scope: dark sector → ΔN_eff → BBN (done in W1, keep); N*/T_rh → BBN; wino mass → gamma line (done at 1 TeV only, needs the H.E.S.S. limit curve vs mass + check of PSR J0740 value, R6); J-factor region → Sky level; b_A → G_eff → S₈ and z† → H(z) at z 2–5 vs DESI Lyα BAO. Research first: H.E.S.S./CTAO line-limit curve (mass vs σv), DESI DR2 Lyα BAO D_H/r_d at z = 2.33, newest J0740 mass, S₈ values.
Postulate W1: every level returns {category, inputs, outputs, data[{name,value,sigma|limit,source}], pulls, status ∈ pass/tension/fail/open}; nothing typed in by hand except measured data with a source; fits labelled F; a test per level.
Notes: wino gamma-line σv — checked: the D1322 '/1e6' is M² in GeV² at 1 TeV, so π α²/M² is the general tree form; the M dependence of the Sommerfeld factor comes from wino_s_nlo itself. At 1 TeV the engine reproduces 1.42e-26 (same formula as the smoke test).
E1 results (defaults): inflation pass (n_s 0.9706, r 5.4e-4); flavour pass (Koide Q 0.6666645 ± 5.1e-6, −0.4σ; Brannen δ 0.2222248 vs 2/9 = 0.2222222); BBN tension (D/H −2.6σ vs Cooke 2018); late tension (thread −2.6/−8.1/−3.4, coupling ~0); colliders pass at 1 TeV (ATLAS 670); galaxy open (f²σv 2.2–6.0e-28 at 1 TeV vs the 2.3e-28 used in D1322: borderline, needs the limit curve); stars pass (SLy 2.05 vs J0740 2.08 ± 0.07); sky open.
For V1 to check: (1) bridge B1 = −2.0e-3 here, not the −0.9e-4 of the twin-ladder notes (those were for an earlier model): do not show the old tolerance; (2) late-level 'd_coupled' is the guard ceiling min(coupled, thread), label it '≤'; (3) stars pass rule uses 2σ below J0740: state it; (4) runtime 5 s per run (galaxy J-factor + Sommerfeld): cache for the UI.

V1 findings (W1 engine), all to fix in E2:
1. DARK_SECTORS values were not sourced correctly. The D-notes say: minimal dark sector with equal sharing ΔN_eff = 0.21 (D1646, estimate); with the P-brane split (C5, D1671) the inflaton heats our side only, ΔN_eff ≈ 0 (bound ≤ 0.086, register C5); full mirror with equal sharing ΔN_eff = 7.4 (D1646, ruled out); mirror at its viability bound 0.3 (D1648). The engine had 'mirror 0.086', which matches none of these. Replace the table with these four, each with its D-note.
2. Bridge B1 = −2.0e-3 at the full SERAPIS point. The twin-ladder target (−0.9e-4, tol 1.2e-4) was set for an earlier model: show B1/B2 as numbers, with no pass/fail, until a new lock sets them.
3. Late level: 'd_coupled' is the nested-guard ceiling min(coupled, thread); rename it to 'd_coupled_at_most' and label it. Its status was hard-coded 'tension': derive it instead (pass if the thread beats ΛCDM on all 3 sets, plus the label 'trails w0wa (−9/−20/−15, CAMB)').
4. Stars: the pass rule (M_max ≥ 2.08 − 2σ = 1.94) must be in the labels.
5. Flavour: the Brannen δ is chosen from the symmetric forms (δ, 2π/3 − δ, any order) as the one nearest 2/9. That is a domain choice, not a fit, but it must be stated, along with the value of the other forms.
6. Galaxy: no status rule. Keep 'open', but add a CONSERVATIVE comparison at 1 TeV only (the single stored limit), labelled as such.
7. Speed: 5 s per run, mostly the J-factor + Sommerfeld. Cache by (halo, rho_sun) and (M) with functools.lru_cache.
8. Errors are caught per level (good), but the error text should also go to a 'error' field so the UI can show it plainly.

Referee report (W1 engine), read as a cosmologist / BBN / collider / indirect-detection referee would, against Cobaya, PRyMordial, SModelS and micrOMEGAs:
R1 (major, inflation) Status is graded on n_s, which is FITTED for serapis_* — grading a fit is circular. The Weave's inflation status must come from its PREDICTIONS only (r against the r limits; α_s once a running constraint is stored). n_s pulls stay visible as context.
R2 (major, BBN) Pulls use the observational σ only. PRIMAT's own D/H theory error (nuclear rates, chiefly d(p,γ)³He after LUNA 2020, a few %) is left out, which overstates the −2.6σ. Fix: add a theory σ with its source, or label the pull 'obs-only'.
R3 (major, late universe) Δχ² is shown without the cost of extra parameters: the thread adds 1 parameter, the coupled model 2. Show ΔAIC = Δχ² + 2k beside Δχ² (thread: −0.6 / −6.1 / −1.4).
R4 (inflation) 1-D Gaussian pulls ignore the n_s–r correlation; the specialists use the joint 2-D likelihood. → W6.
R5 (galaxy) The line rate is LO Sommerfeld at a fixed v = 1e-3 with no endpoint/resummation; these change the line by O(1) factors at TeV masses. ρ_sun = 0.4 vs the 0.39 used in the D1322 limit comparison. → W2, map item 2.
R6 (stars) PSR J0740+6620's mass has newer analyses; check the current value before the next V2. → W2.
R7 (colliders) The expected reach assumes r_bkg = 1; the ATLAS limit applies to a pure wino with its predicted lifetime only. State both. → W8.
R8 (general) No uncertainties are propagated through the links (e.g. ΔN_eff → Y_p); every output is a point value. → W5/W6.
R9 (sky) No science link yet; the level is a placeholder. → W2/W7.
Comparison: Cobaya/MontePython do joint likelihoods (R4); PRyMordial carries rate uncertainties (R2, R8); SModelS states validity ranges for each limit (R7); micrOMEGAs/DarkSUSY include the Sommerfeld and endpoint pieces (R5). Our real edge is that one parameter set drives all of these at once, with sources and labels.

W2 research notes (04:53 CT):
- DESI DR2 Lyα BAO (arXiv:2503.14739): z_eff = 2.33, D_H/r_d = 8.632 ± 0.101, D_M/r_d = 38.99 ± 0.53 (stat+sys), ρ = −0.431. This is the H(z) point that tests negative space (z† ≈ 3.7 needs b_A < 0).
- S₈: KiDS-Legacy 0.815 +0.016/−0.021 (arXiv:2503.19441); Planck 2018 0.832 ± 0.013; CMB lensing (ACT DR6 + Planck PR4 + SPT-3G + DESI DR2) 0.828 ± 0.012 (Qu et al. 2026, via arXiv:2602.12238). DES Y6 is 2.4–2.7σ from the CMB, but no central value was read; not used.
- PSR J0740+6620: still 2.08 +0.072/−0.069 M☉ (Fonseca et al. 2021). NICER 2024 radius papers (arXiv:2406.14467) use it with σ = 0.09 including a systematic. Keep 2.08 ± 0.07 and note the 0.09 option (referee R6 closed: no newer mass).
- H.E.S.S. line limit — FINDING (affects the W1 galaxy verdict): the D-notes have TWO different limits. D1110/D1277 use H.E.S.S. 2018 (arXiv:1805.05741) γγ ≈ 4e-28 cm³/s at 1 TeV (Einasto, 7 ROIs; only the 1 TeV value is quoted). D1322 (A2n) uses the IGS line limit 2.3e-28 with the factor 0.794 and the ratio J/J_bench. W1's engine compared f²σv with 2.3e-28 directly, WITHOUT the 0.794 factor and without J/J_bench, so its 'tension' verdict is not the locked D1322 test. Benchmark Einasto (ρ☉ 0.39) by the D1322 recipe gives f_max ≈ √(2.3e-28/(1.42e-26 × 0.794 × 1.05)) ≈ 0.14 against f_pred 0.124–0.205: still mixed, but must be computed by the exact recipe. The full limit curve vs mass is not in the repo (the paper is plot-only above 1 TeV): blocked, recorded.

Referee report W3 (a working scientist using it for a talk or a referee reply; compared with CAMB's web interface, the Cobaya GUI, and Aladin/Stellarium panels):
U-R1 (major) No export or share: a scientist must be able to save exactly what they see. Add 'Download JSON' (engine response + provenance) and 'Copy link' (parameters in the URL hash, restored on load).
U-R2 (major) False precision: readouts show 4 decimals regardless of the error (e.g. 'expected reach 740.1838 GeV', 'pairs 713.79'). Round to 3 significant figures unless the value carries a σ.
U-R3 (major) Live vs locked is not visible: on the Late panel the b_A knob moves only z† and G_eff, while the Δχ² and S₈ bars are locked fit results. Mark charts and readouts that do not depend on the knobs with a 'locked result' tag.
U-R4 (major) The inflation chart has no legend: 8 overlapping n_s bands and 3 r lines are only identified on hover. Add a small legend (or label the newest combined sets) and say which sets set the status.
U-R5 (minor) The collider chart labels collide when the reach is near the limit (seen at 740 vs 670).
U-R6 (minor) The scorecard's 'A · pass' hides that the inflation status is r-only for serapis_*: add 'r-only' to the tooltip or the lamp word.
U-R7 (minor) No uncertainty shown with point outputs (Y_p, D/H, M_max). The engine has none to give yet (W5/W6 will add them); say 'no error yet' instead of implying exactness.
U-R8 (minor) Printing: the light theme exists, but there is no print stylesheet (knobs and buttons waste space on paper).
Strengths a referee would note: one parameter set drives every level; sources and P/F/G labels on every panel; nested-guard, ΔAIC, and halo dependence shown rather than hidden; the Studio hook.

## Done log
- 04:50 CT W1/F referee: 9 points (3 major)
- 05:24 CT W9/P postulate: acceptance rules X1–X6
- 05:22 CT W9/R research: build paths (GitHub Actions), offline-APK design, CI failures found; camb added to CI
- 05:19 CT W3/V2 signed off (export/share, precision, locked tags, legend, print)
- 05:16 CT W3/F referee: 8 points (4 major: export/share, precision, live vs locked, inflation legend)
- 05:14 CT W3/E2 engineer: limits read from the engine (no hard-coded 670 or H.E.S.S. masses), stale label removed, galaxy chart rescaled, S₈ labels shortened, human names + units once, δ forms as a list, phone header static + larger chart text, status words beside lamps, Studio Api.weave_run + open_control + 'Control' tab
- 05:11 CT W3/V1 review: 10 findings (U1–U10)
- 05:09 CT W3/E1 engineer: server + control panel built and browser-tested
- 05:05 CT W3/P postulate: acceptance rules A1–A8
- 05:04 CT W3/R research: Studio (Janus) architecture and style read; design consequence recorded
- 05:03 CT W2/V2 signed off (DEVIATIONS D1; three masses; over-closure flag)
- 05:00 CT W2/F referee: 6 points (3 major: cite arXiv:2608.07234, NLL band, three limit masses); engine reproduces D1125's 0.143
- 04:58 CT W2/E2 engineer: both J values labelled, warnings silenced in the engine only (reason recorded), S₈ sub-status on the card, PC file names cited
- 04:56 CT W2/V1 review: J cross-checked (≤ 0.65%), S8 verified, 4 small findings
- 04:57 CT W2/E1 engineer: L1–L5 built; 9 tests pass
- 04:54 CT W2/P postulate: PREREG_W2_LINKS locked (L1 exact D1322 recipe with 0.286 self-check; L2 Lyα display-only, not independent; L3 S₈ pulls vs KiDS-Legacy and CMB lensing; L4 label; L5 GC sky target)
- 04:53 CT W2/R research: Lyα BAO, S₈ (3 values), J0740 unchanged, H.E.S.S. recipe finding
- 04:51 CT W1/V2 signed off: R1 inflation status from predictions only for serapis_* (r), n_s context; R2 BBN pulls labelled observational-only (theory σ in W5); R3 ΔAIC added (thread −0.6/−6.1/−1.4). R4–R9 carried to W2/W5/W6/W7/W8. 29 tests pass (engine 8 + shared/janus/mapper).
- 04:45 CT W1/V1 review: 8 findings (above)
- 04:48 CT W1/E2 fixes: dark-sector table from D1646/D1648/C5 (mirror_full_equal 7.4 → BBN fail, as it should); bridges numbers-only; late status derived (tension: beats ΛCDM, trails w0wa); stars rule stated; Brannen forms listed; galaxy tests BOTH ends of the fraction bracket at 1 TeV (low 2.2e-28 passes, high 6.0e-28 fails vs 2.3e-28 → tension; E2 first tried the low end only, caught before commit); lru_cache; error field
- 04:43 CT W1/E1 engine.py + tests (6 pass)
