"""SERAPIS circuit (Danny 2026-11-18: "think of every node as a part of a circuit — a SERAPIS circuit, perfected as we learn and grow").

Wires carry quantities (n_s, C, N*, r, α_s, T_R, wino mass, lattice values). Components are web nodes: each reads its input
wires, runs its tool, drives its output wires, and checks the circuit laws that touch it (round trips, independent routes,
the twin-ladder bridge). A failed law is an OPEN circuit at that component — work for the loop, never hidden.

Correction 2026-11-18 22:41 UTC: bridge B1 was misapplied as a law on the first run; it is a Starobinsky-class relation,
now reported as a ratio (see the band_e component).
Tolerances are fixed in code before a run and only change through a dated note (never loosened to make a run pass).
"Learning" = every run is appended to circuit_runs.jsonl (→ CubeMind), each wire's drift against the previous run is
reported, and open circuits are listed for the loop to derive or fix.
Usage: run(call) where call(tool_name, args_dict) -> dict (Janus run_tool or CubeMind aegis_tools.call)."""
import json, math, os, time

DATA = dict(ns_spa_desi=(0.9728, 0.0027), ns_spa=(0.9684, 0.0030), r_max=0.036, atlas_dt_GeV=660.0)   # data the circuit is scored on
NS_MODEL = 0.9744   # the frozen SERAPIS point (D1251), the circuit's operating point

def run(call, ns_model=NS_MODEL, log_path=None):
    W = {}          # the wires
    comps = []      # one entry per component firing
    t0 = time.time()
    def comp(node, tool, fn):
        c = dict(node=node, tool=tool, laws=[], ok=True); t = time.time()
        try: fn(c)
        except Exception as e: c['laws'].append(dict(law='component ran', ok=False, text=f'{type(e).__name__}: {e}'))
        c['ok'] = all(l['ok'] for l in c['laws']); c['seconds'] = round(time.time() - t, 2); comps.append(c)
    def law(c, name, ok, text): c['laws'].append(dict(law=name, ok=bool(ok), text=text))
    def drive(**kw): W.update({k: float(v) for k, v in kw.items() if v is not None})

    # ---- stage 1: CMB → string scale (left ladder) ----
    def f(c):
        m = call('string_meter', {'ns': ns_model, 'ns_sigma': 0.0016})
        drive(ns_in=ns_model, C=m['C'], Nstar_meter=m['Nstar'], r_meter=m['r'], alpha_meter=m['alpha_s'], T_R=m['T_R'])
        law(c, 'C in the audited range 1.0–1.3e-6', 1.0e-6 <= W['C'] <= 1.3e-6, f"C = {W['C']:.4g}")
    comp('string_meter', 'string_meter', f)
    def f(c):
        e = call('serapis_emulator', {'C': W['C']}); drive(ns=e['ns'], r=e['r'], alpha_s=e['alpha_s'])
        d = abs(W['ns'] - W['ns_in']); law(c, 'round trip n_s → C → n_s', d < 1e-4, f"|Δn_s| = {d:.1e} (tol 1e-4)")
        d = abs(W['r'] - W['r_meter'])/W['r_meter']; law(c, 'r: meter = emulator', d < 0.01, f"rel {d:.1e} (tol 1%)")
    comp('serapis_e', 'serapis_emulator', f)
    def f(c):
        p = call('serapis_point', {'C': W['C'], 'T_R': W['T_R']}); drive(ns_pt=p['ns'], r_pt=p['r'], alpha_pt=p['alpha_s'], Nstar=p['Nstar'], V_ratio=p['V_ratio'])
        d = abs(W['ns_pt'] - W['ns']); law(c, 'exact point = emulator (n_s)', d < 3e-4, f"|Δ| = {d:.1e} (tol 3e-4)")
        d = abs(W['r_pt'] - W['r'])/W['r']; law(c, 'exact point = emulator (r)', d < 0.02, f"rel {d:.1e} (tol 2%)")
    comp('serapis_point', 'serapis_point', f)
    def f(c):
        j = call('janus_relation', {'ns': W['ns_pt'], 'r': W['r_pt'], 'p': 2.8284, 'kappa': 1}); drive(alpha_janus=j['alpha_s'])
        d = abs(W['alpha_janus'] - W['alpha_pt'])/abs(W['alpha_pt']); law(c, 'Janus relation α_s(n_s, r) = computed α_s', d < 0.06, f"rel {d:.1%} (D1234 tol 6%)")
    comp('L_bridge', 'janus_relation', f)
    def f(c):
        n = call('nstar_match', {'r': W['r_pt'], 'V_ratio': W['V_ratio'], 'T_R': W['T_R']}); drive(Nstar_match=n['Nstar'])
        d = abs(W['Nstar_match'] - W['Nstar']); law(c, 'N* from r = N* of the point', d < 0.2, f"|ΔN*| = {d:.2g} (tol 0.2)")
    comp('L_nstar', 'nstar_match', f)
    def f(c):
        m = call('serapis_ms', {'C': W['C'], 'Nstar': W['Nstar']}); drive(ns_ms=m['ns'])
        d = abs(W['ns_ms'] - W['ns_pt']); law(c, 'exact Mukhanov–Sasaki = slow roll', d < 1e-3, f"|Δn_s| = {d:.1e} (tol 1e-3)")
    comp('X_ms', 'serapis_ms', f)
    def f(c):
        m = call('string_meter', {'ns': W['ns_pt'], 'ns_sigma': 0.0016}); drive(C_back=m['C'])
        d = abs(W['C_back'] - W['C'])/W['C']; law(c, 'inverse meter returns the same C', d < 0.02, f"rel {d:.1e} (tol 2%)")
    comp('inverse_meter', 'string_meter', f)
    # ---- circuit laws on the shared quantities (twin-ladder bridges, filters) ----
    def f(c):
        # B1 (twin-ladder bridge r ≈ 3(1−n_s)², D403 era) belongs to the Starobinsky-class plateau; first circuit run (22:41 UTC)
        # misapplied it as a law here. SERAPIS-E is a different plateau with r far BELOW that line by design, so B1 is
        # REPORTED (ratio), not a law. Correction recorded in the circuit docstring and the D-note, not a silent tolerance change.
        b1 = W['r_pt'] - 3*(1 - W['ns_pt'])**2; drive(B1=b1, r_over_starobinsky=W['r_pt']/(3*(1 - W['ns_pt'])**2))
        law(c, 'report: r / Starobinsky-line 3(1−n_s)² (B1, not a law for SERAPIS-E)', True, f"ratio {W['r_over_starobinsky']:.3f} (SERAPIS-E sits below the R² line)")
        ns0, s0 = DATA['ns_spa_desi']; pull = (W['ns_pt'] - ns0)/s0; drive(pull_spa_desi=pull)
        law(c, 'filter F3: n_s within 2σ of CMB-SPA+DESI', abs(pull) < 2, f"pull {pull:+.2f}σ")
        law(c, 'filter F3: r below the bound', W['r_pt'] < DATA['r_max'], f"r = {W['r_pt']:.3g} < {DATA['r_max']}")
        law(c, 'frozen band n_s 0.969–0.975', 0.969 <= W['ns_pt'] <= 0.975, f"n_s = {W['ns_pt']:.5f}")
    comp('band_e', 'laws', f)
    def f(c):
        e = call('serapis_emulator', {'C': 1.6e-6}); drive(ns_cap=e['ns'])
        law(c, 'family cap n_s < 0.985 at the top of C', W['ns_cap'] < 0.985, f"n_s(C = 1.6e-6) = {W['ns_cap']:.4f}")
    comp('caps', 'serapis_emulator', f)
    # ---- stage 2: collider side (wino) ----
    def f(c):
        l = call('lhc_lifetime', {'m': 1000}); drive(dm_MeV=l['dm_MeV'], ctau_cm=l['ctau_cm'])
        law(c, 'two-loop Δm in 150–175 MeV', 150 < W['dm_MeV'] < 175, f"Δm = {W['dm_MeV']:.2f} MeV, cτ = {W['ctau_cm']:.3g} cm")
    comp('Q_life', 'lhc_lifetime', f)
    def f(c):
        d = call('lhc_dt_limit', {'lumi': 136, 'sqrts': '13', 'search': 'ATLAS_136', 'boost': 'fixed', 'band': False}); drive(m_floor=d['m_limit_GeV'])
        law(c, 'recast = ATLAS published limit', abs(W['m_floor'] - DATA['atlas_dt_GeV']) < 15, f"{W['m_floor']:.1f} vs {DATA['atlas_dt_GeV']:.0f} GeV (tol 15)")
    comp('Q_dt', 'lhc_dt_limit', f)
    def f(c):
        p = call('lhc_panel', {}); fu = call('lhc_future', {}); drive(hl_reach=p['hl_lhc_reach_GeV'], hl_future=fu['HL-LHC']['low_bkg_TeV']*1000)
        law(c, 'window floor = recast limit', abs(p['run2_limit_GeV'] - W['m_floor']) < 1, f"{p['run2_limit_GeV']:.1f} = {W['m_floor']:.1f} GeV")
        law(c, 'panel HL-LHC reach = future-collider tool', abs(W['hl_reach'] - W['hl_future']) < 5, f"{W['hl_reach']:.1f} vs {W['hl_future']:.1f} GeV")
    comp('wino_window', 'lhc_panel', f)
    # ---- stage 3: geometry (lattices) ----
    def f(c):
        e = call('lattice_lab', {'cmd': 'epstein', 'args': ['A2', '2']}); drive(E_rho2=e['epstein'])
        law(c, 'A2 Epstein E(ρ,2) (the SERAPIS-E vacuum scale)', abs(W['E_rho2'] - 5.7833593) < 2e-6, f"{W['E_rho2']:.7f}")
    comp('X_epstein', 'lattice_lab', f)
    def f(c):
        h = call('lattice_lab', {'cmd': 'hexagons', 'args': ['E8']}); m = call('lattice_lab', {'cmd': 'modular', 'args': ['E8']}); fl = call('lattice_lab', {'cmd': 'flip', 'args': ['E8']})
        drive(E8_hex=h['hexagonal_planes'])
        law(c, 'E8 holds 1120 SERAPIS hexagons', W['E8_hex'] == 1120, f"{int(W['E8_hex'])}")
        law(c, 'modularity ⇔ no flip (θ_E8 = E4)', m.get('match') is True and fl.get('flips') is False, f"match {m.get('match')}, flips {fl.get('flips')}")
    comp('X_mod', 'lattice_lab', f)
    def f(c):   # lattice-disk configs (D1352, P6 side model): closed form, separation from SERAPIS r
        out = []
        for g, d in (('A2', 2), ('D4', 4), ('E6', 6), ('E8', 8), ('BW16', 16), ('Leech', 24)):
            a = d/6; ye = math.asinh(math.sqrt(4/(3*a))); y = math.acosh(math.cosh(ye) + 4*W['Nstar']/(3*a)); r = 64/(3*a*math.sinh(y)**2)
            W[f'r_cfg_{g}'] = r; out.append(f'{g} {r/W["r_pt"]:.1f}×')
        law(c, 'every lattice config is ≥3× SERAPIS r (separable by r data)', min(W[f'r_cfg_{g}'] for g in ('A2', 'D4', 'E6', 'E8', 'BW16', 'Leech')) > 3*W['r_pt'], 'r_cfg / r_SERAPIS: ' + ', '.join(out))
    comp('G_A2', 'closed form', f)

    opens = [dict(node=c['node'], law=l['law'], text=l['text']) for c in comps for l in c['laws'] if not l['ok']]
    nl = sum(len(c['laws']) for c in comps)
    res = dict(t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), components=len(comps), laws=nl, closed=nl - len(opens), open=opens,
               health=round((nl - len(opens))/max(nl, 1), 4), wires={k: (round(v, 10) if abs(v) < 1e6 else v) for k, v in W.items()},
               comps=comps, seconds=round(time.time() - t0, 2))
    if log_path:
        prev = None
        try:
            with open(log_path, encoding='utf-8') as fh:
                for l in fh: prev = json.loads(l) if l.strip() else prev
        except (OSError, ValueError): pass
        if prev:
            res['drift'] = {k: v - prev['wires'][k] for k, v in res['wires'].items() if k in prev.get('wires', {}) and v != prev['wires'][k]}
        try:
            with open(log_path, 'a', encoding='utf-8') as fh: fh.write(json.dumps({k: v for k, v in res.items() if k != 'comps'}) + '\n')
        except OSError: pass
    return res
