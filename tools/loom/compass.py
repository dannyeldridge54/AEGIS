"""Loom compass (Danny 16:06): every measurement is fingerprinted with a direction (up / down / on target) and a vector
(signed pull on each knob), so results point somewhere instead of just PASS/FAIL. Pulse order: centre -> outward notches.
Run: python3 tools/loom/compass.py  -> field_tests/loom/compass_catalog.json + tools/project_docs/WEAVE_COMPASS.md"""
import json, math, sys
sys.path.insert(0, 'tools/weave_cm'); from weave_tools import weave_rg2
R = lambda f: json.load(open('field_tests/results/' + f))
v4 = {r['name']: r for r in R('weave_derivation_v4.json')}
g = lambda key: next(r for n, r in v4.items() if n.startswith(key))
cat = []
def fp(ring, notch, qty, value, target, kind, src, knobs, spread=None, note=''):
    """direction: which way the value must move to reach the target. headroom: >0 inside the bar (log10 units or sigma)."""
    if kind == 'data':
        t, s = target; pull = (value - t) / s; d = '●' if abs(pull) < 1 else ('↑' if pull < 0 else '↓'); head = 2 - abs(pull); unit = 'σ'
    elif kind in ('>', '<'):
        ok = value > target if kind == '>' else value < target
        head = (math.log10(value / target) if kind == '>' else math.log10(target / value)); unit = 'dex'
        d = ('●' if head > 0.3 else '◔') if ok else (('↑' if kind == '>' else '↓') + '!')
        pull = None
    else: d, head, unit, pull = '○', None, '', None      # prediction / input: no target yet
    cat.append(dict(id=len(cat) + 1, ring=ring, notch=notch, quantity=qty, value=value, spread=spread, target=target, kind=kind,
                    direction=d, headroom=head, unit=unit, pull=pull, knobs=knobs, source=src, note=note))
# ---- measured sensitivities (vectors): alpha_s and wino vs m3/2 (AMSB scaling), +-10 %
def amsb(m32):
    mg = 3 * 0.092 / (4 * math.pi) * m32 * (4926.4 / (3 * 0.092 / (4 * math.pi) * 257945.66)); return dict(m_wino=686.51 * m32 / 257945.66, m_gluino=mg, m_scalar=4.7e5 * m32 / 257945.66)
a_up, a_dn = weave_rg2(amsb(257945.66 * 1.1))['alpha_s_unif'], weave_rg2(amsb(257945.66 / 1.1))['alpha_s_unif']
das_dlnm = (a_up - a_dn) / (2 * math.log(1.1))
Ns = 50.3; dns_dN = (1 - 0.9706) / Ns                     # D1935: (1-n_s)/N* ~ 5.9e-4 (estimate; to be measured on the plateau), NOT 2/N*^2
dN_dlnTR = 1 / 3                                          # instant-reheating-like scaling, w=0 -> dN*/dlnT_R ~ 1/3 (estimate)
# ---- ring 0: the centre (fold + shared rung step)
fp(0, 'centre: rung step', '|u| one-spurion window (bisected to 2e-10)', 0.026631, None, 'info', 'D1932/D1932a', {}, spread=0.0015, note='window [0.02588, 0.02740], width x1.059, ONE fixed assignment, f7 22-23 %, fJ 61-66 %. Contains 0.027 BY CONSTRUCTION (search started there, D1935); upper edge is a x2-cut artefact; window non-monotone (0.0203 isolated point)')
fp(0, 'centre: rung step', '|u| single-flavon window centre (U32)', math.sqrt(0.063 * 0.148), None, 'info', 'D1928', {}, note='SECONDARY window, assignment varies')
fp(0, 'centre: rung step', 'lepton slip / down slip', g('lepton slip')['value'], (1.0, 0.05), 'data', 'v4 (D1832)', {'u': '0'}, note='same-lock fit; conflicts with Koide at rho')
# ---- ring 1: flavour
fp(1, 'quarks', 'f7 (two-size lock)', g('quark 7-observable')['value'], 0.05, '>', 'd1829_cp.json', {'u_u': '0', 'u_d': '0'}, note='PHENOMENOLOGICAL')
fp(1, 'quarks', 'fJ', g('quark CP')['value'], 0.2, '>', 'd1829_cp.json', {}, note='PHENOMENOLOGICAL')
fp(1, 'neutrinos', 'ratio natural fraction', g('neutrino ratio')['value'], 0.01, '>', 'd1821_neutrino.json', {'flux(4,4,8)': '0'}, note='thin: 0.12 dex headroom')
fp(1, 'neutrinos', 'M_N vs leptogenesis window top', g('heavy neutrino')['value'], 2.5e12, '<', 'v4 (D1822)', {'n_theta': '0', 'tan_beta': '+'})
fp(1, 'neutrinos', 'M_N vs window bottom', g('heavy neutrino')['value'], 4.5e10, '>', 'v4 (D1822)', {})
fp(1, 'leptons', 'Koide delta', 2 / 9, None, 'input', 'v4', {}, note='TRUST')
# ---- ring 2: spectrum + forces
m32 = g('gravitino')['value']
fp(2, 'spectrum', 'wino M2 [GeV]', g('wino')['value'], 660.0, '>', 'v4', {'m3/2': '+'}, note='marginal: wants m3/2 UP')
fp(2, 'spectrum', 'gluino M3 [GeV]', g('gluino')['value'], 2300.0, '>', 'v4', {'m3/2': '+'})
fp(2, 'forces', 'alpha_s(M_Z) single-stack (no threshold)', 0.1142, (0.1180, 0.0009), 'data', 'D1929 run 1; valid only under the single-stack assumption (D1942)', {'Delta3 threshold': '+'},
   note='d alpha_s / d ln m3/2 = %+.5f (measured, ±10 %%): wants m3/2 DOWN; opposes the wino arrow' % das_dlnm)
fp(2, 'forces', 'Delta3 after Higgs pair + gauge', g('Delta_3 after')['value'], -0.05, '>', 'v4 (D1881b)', {'b_prime': '-', 'brane threshold': '+'}, note='needs +0.044 more')
fp(2, 'forces', 'alpha_s with S at i (self-consistent spectrum)', 0.1112, (0.1180, 0.0009), 'data', 'D1929', {'S vacuum': 'rho'}, note='S at i pushes the wrong way')
fp(2, 'forces', 'S-T seam: supergravity-form threshold (non-universal part)', 1e-9, 0.044, '>', 'D1938 (Conlon-Palti 0901.4350)', {'non-universal threshold': '+', 'split stacks (f3 != f2)': '+'}, note='universal on one stack: cancels in Delta3; plotted as 1e-9')
fp(2, 'forces', 'proton lifetime [yr]', g('proton')['value'], 2.4e34, '>', 'v4', {'M12': '+'})
# ---- ring 3: inflation / cosmology
fp(3, 'inflation', 'n_s', g('n_s')['value'], (0.9728, 0.0027), 'data', 'v4', {}, note='inside its band (0.8σ): no pull counted (D1935); N* = 50.3 not yet cross-checked against T_R')
fp(3, 'inflation', 'n_s with S at i', 0.9704, (0.9728, 0.0027), 'data', 'D1926', {'S vacuum': 'rho'})
fp(3, 'inflation', 'r', g('r')['value'], 0.036, '<', 'v4', {})
fp(3, 'cosmology', 'T_R vs M_N (thermal leptogenesis)', g('T_R')['value'], None, 'info', 'v4 (D1897)', {}, note='a bound the model sidesteps (non-thermal leptogenesis): NOT a pull (D1935)')
fp(3, 'cosmology', 'non-thermal leptogenesis: Br(phi->NN) needed', 0.095, 1.0, '<', 'D1941 (m_phi 4.9e12 > 2 M_N)', {'Br(phi->NN)': '+'}, note='viable inside the gravitino box at max DI CP; a branching requirement, not derived')
fp(3, 'cosmology', 'non-thermal wino Omega from gravitinos (Omega ∝ T_R)', 0.017 * g('T_R')['value'] / 3.2e8, 0.12, '<', 'D732 (Y3/2 ∝ T_R)', {'T_R': '-'}, note='D732: Omega 0.017 at T_R 3.2e8 (M2 0.66 TeV), 0.11 at 3.0e9 ⇒ T_R capped at ~3e9')
fp(3, 'cosmology', 'Delta N_eff', 1e-6, 0.17, '<', 'v4', {}, note='0 exactly; plotted as 1e-6')
fp(3, 'cosmology', 'dark-matter mass [GeV]', g('dark-matter')['value'], None, 'prediction', 'v4', {})
# ---- ring 4: reverse thread
fp(4, 'reverse', 'alpha drift zeta', g('thread alpha')['value'], 1.66e-6, '<', 'v4 (D1887)', {'b_bf': '-'})
fp(4, 'reverse', 'thread slope lambda (DESI needs ~0.95)', float('nan'), None, 'open', 'D1906', {}, note='OPEN: non-Kähler only')
# ---- the compass: aggregate the arrows per knob
from collections import defaultdict
pull = defaultdict(list)
for c in cat:
    for k, s in c['knobs'].items():
        if s in '+-' and c['direction'] not in ('○',): pull[k].append((c['notch'] + ': ' + c['quantity'], s, c['direction']))
compass = {k: dict(up=[p for p in v if p[1] == '+'], down=[p for p in v if p[1] == '-'], tension=len({p[1] for p in v}) > 1) for k, v in pull.items()}
json.dump(dict(catalog=cat, compass=compass, sensitivities=dict(dalpha_s_dlnm32=das_dlnm, dns_dNstar=dns_dN)), open('field_tests/loom/compass_catalog.json', 'w'), indent=1, default=str)
L = ['# The Weave compass (Danny 16:06): every measurement fingerprinted with a direction and a vector', '',
     'Legend: ● on target (inside the bar by > 0.3 dex or < 1σ); ◔ passes but thin; ↑! / ↓! fails now and must move up / down; ↑ / ↓ (data) outside 1σ; ○ prediction, input or info (no pull). Corrected after referee D1935. Headroom is in σ (data) or dex (bounds); smaller means tighter.', '',
     '| # | ring | notch | quantity | value | dir | headroom | knobs it pulls | source | note |', '|---|---|---|---|---|---|---|---|---|---|']
for c in cat:
    hv = '' if c['headroom'] is None else '%.2f %s' % (c['headroom'], c['unit'])
    L.append('| %d | %d | %s | %s | %.4g | %s | %s | %s | %s | %s |' % (c['id'], c['ring'], c['notch'], c['quantity'], c['value'], c['direction'], hv,
             ', '.join('%s %s' % (k, v) for k, v in c['knobs'].items()) or '—', c['source'], c['note']))
L += ['', '## Where it points (per knob)', '']
for k, v in compass.items():
    L.append('- **%s**%s: wants ↑ from %s; wants ↓ from %s.' % (k, ' — TENSION' if v['tension'] else '', '; '.join(p[0] for p in v['up']) or 'none', '; '.join(p[0] for p in v['down']) or 'none'))
# interactions: can one knob satisfy the arrows that pull on it?
need_as = 0.1180 - 0.1142; dln = need_as / das_dlnm; wino_new = 686.5 * math.exp(dln)
dN = 0.0022 / dns_dN; TR_ns = 3.7e8 * math.exp(dN / dN_dlnTR)
L += ['', '## Interactions (where two arrows meet one knob)', '',
      '- **m3/2 cannot fix α_s.** Closing α_s needs Δ ln m3/2 = %.2f (m3/2 ×%.2f). That puts the wino at %.0f GeV, far below the 660 GeV bar, which already has only 4 %% room. So α_s must come from a threshold (Δ₃), not from the spectrum.' % (dln, math.exp(dln), wino_new),
      '- **T_R is boxed, not pulled (corrected D1935).** Gravitino→wino production caps T_R at ~3e9 GeV (Ω ∝ T_R; 0.11 at 3e9, D732). Thermal leptogenesis (T_R ≳ M_N) is a bound the model sidesteps, and n_s already sits inside its band. So T_R cannot rise 3 dex, and leptogenesis must be non-thermal. The earlier "two arrows agree, T_R ~ 1e11–1e12" is withdrawn.',
      '- **u (corrected D1935):** the one-spurion window [0.02588, 0.02740] is narrow (×1.059) and has one fixed charge pattern, natural throughout. That it contains 0.027 is by construction (the search started there), so it is not a convergence. u_d = 0.02587 still fails by 0.05 %. The window is non-monotone in u (isolated point 0.0203; U32 0.063–0.148).']
L += ['', 'Knob convention: "+" means this measurement wants the knob raised, "−" lowered.']
L += ['', 'Measured: dα_s/d ln m₃/₂ = %+.5f; dn_s/dN* = %.2e.' % (das_dlnm, dns_dN)]
open('tools/project_docs/WEAVE_COMPASS.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
