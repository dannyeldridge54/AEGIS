# PREREG J7g — pulse-2 and pulse-3: every J7f-scored ASPIC model through ASPIC's two reheating routes, one batch each
Locked 2026-11-17 before any J7g number (Danny 00:42: run the same research steps on each pulse model).
Models: every model with status 'scored' in J7f (field_tests/results/janus_j7f.part.jsonl), same parameter set as J7f.
pulse-2 (as J7c2): ASPIC foo_x_rrad(params, x_end, ln R_rad, P*, bfold) at ln R_rad = 0, −10; reference: exact Martin–Ringeval
matching (Eq. 15, M⁴ from exact-MS amplitude, iterated); Janus: same matching, second-order amplitude.
pulse-3 (as J8): ASPIC foo_x_star(params, x_end, w = 0, ln ρ_reh, P*, bfold) at ln ρ_reh = −100, −150; reference/Janus: Eq. 13
→ ln R_rad iterated with M⁴, then Eq. 15.
Potential: the same spline of ASPIC's own V̂(x), φ = s·x, as J7f (re-using its grid files). Claims C1–C3 and the C5/C6 pivot report
exactly as PREREG_J7c2, per pulse. Models with no ASPIC reheating function (e.g. DI) or where ASPIC stops are listed.
