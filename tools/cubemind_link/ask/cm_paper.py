"""CubeMind paper generator (PREREG_CM_PAPERS): one technical note per nuclear field section, built only from
Chronos engine calls. Prose is fixed template text; every printed number is an engine result (N), an echoed call input (I) or an engine constant (K).
Usage: python cm_paper.py [section|all]   -> papers/<section>.html + papers/index.html
Also served by cm_ask.py at POST /api/paper {"section": "medical"|...|"all"}."""
import hashlib, html, json, math, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
_cands = [os.path.join(os.environ.get('AEGIS_DIR', ''), 'tools', 'gifts', 'chronos'),
          os.path.join(HERE, '..', '..', 'gifts', 'chronos'),
          os.path.join(HERE, '..', 'aegis_tools', 'aegis_bundle', 'tools', 'gifts', 'chronos')]
CHRONOS = next(os.path.abspath(p) for p in _cands if os.path.exists(os.path.join(p, 'chronos_cm.py')))
sys.path.insert(0, CHRONOS)
import chronos_cm as C

def fmt(v):
    v = float(v)
    if v == 0: return '0'
    a = abs(v)
    if a >= 1e5 or a < 1e-3:
        e = math.floor(math.log10(a)); m = v / 10 ** e
        s = f'{m:.3f}'.rstrip('0').rstrip('.')
        if s in ('10', '-10'): s, e = s[:-1] or '1', e + 1
        return f'{s}&times;10<sup>{e}</sup>'
    return f'{float(f"{v:.4g}"):g}'

def get(d, path):
    for k in path.split('.'): d = d[k]
    return d

def lantern():
    p = next((q for q in [os.path.join(HERE, 'LANTERN.md'), os.path.join(HERE, '..', '..', '..', 'LANTERN.md')] if os.path.exists(q)), None)
    if not p: return ''
    lines = [l[1:].strip() for l in open(p, encoding='utf-8').read().split('\n') if l.startswith('>')]
    body = '<br>'.join(html.escape(l.replace('**', '')) for l in lines)
    return f'<details class="lantern"><summary>The Lantern</summary><p>{body}</p></details>'

def engine_hash():
    h = hashlib.sha256()
    for f in sorted(os.listdir(CHRONOS)):
        if f.startswith('chronos') and f.endswith('.py'): h.update(open(os.path.join(CHRONOS, f), 'rb').read())
    return h.hexdigest()

import inspect as _inspect
A3 = C.A3
def _ww_coeff():   # Way-Wigner coefficient recovered from the engine function's value (R80b), regex on the source as a cross-check
    t, T = 3600.0, 3.15e7; v = A3.decay_heat_way_wigner(t, T) / (t ** -0.2 - (t + T) ** -0.2)
    m = re.search(r'return\s+([0-9.]+)\s*\*\s*\(t_s', _inspect.getsource(A3))
    if m and abs(float(m.group(1)) - v) > 1e-12 * v: raise ValueError('Way-Wigner coefficient: source and value disagree')
    return v
def _t12_y(nuc):
    t = C.T12.get(nuc) or A3.T12x[nuc]; return t / C.Y
def _br(a, b):
    for x, y, f in A3.AC_LINKS:
        if (x, y) == (a, b): return f
    raise KeyError((a, b))
CONST = {   # every engine constant quoted in prose: name -> function reading it from the engine (P1c re-derives these)
    'T12_H3_y': lambda: _t12_y('H-3'), 'T12_Pu241_y': lambda: _t12_y('Pu-241'), 'T12_Am241_y': lambda: _t12_y('Am-241'),
    'BR_Mo99_Tc99m': lambda: C.CHAINS['Mo-99 -> Tc-99m (generator)'][1][0],
    'BR_Bi213_Po213_pct': lambda: 100 * _br('Bi-213', 'Po-213'), 'BR_Bi213_Tl209_pct': lambda: 100 * _br('Bi-213', 'Tl-209'),
    'WW_coeff': _ww_coeff,
    'Th_factor_Gyr': lambda: math.log(10) * _t12_y('Th-232') / math.log(2) / 1e9,
    'KN_fth_default': lambda: _inspect.signature(C.kilonova_luminosity).parameters['f_th'].default,
}

class Note:
    def __init__(self, key, title):
        self.key, self.title, self.calls, self.printed, self.inputs, self.consts = key, title, [], [], [], []
    def run(self, name, args):
        r = C.run(name, dict(args)); ch = r.pop('chart', None)
        self.calls.append(dict(name=name, args=args, result=r, chart=ch)); return len(self.calls) - 1
    def N(self, i, path, unit=''):   # an engine RESULT
        v = get(self.calls[i]['result'], path); self.printed.append(dict(call=i, path=path, value=float(v), shown=fmt(v)))
        return fmt(v) + (f'&nbsp;{unit}' if unit else '')
    def I(self, i, key, unit=''):    # an engine INPUT, echoed from the call's own args
        v = self.calls[i]['args'][key]; s = fmt(v) if isinstance(v, (int, float)) else html.escape(str(v))
        self.inputs.append(dict(call=i, key=key, value=v, shown=s)); return s + (f'&nbsp;{unit}' if unit else '')
    def K(self, name, unit=''):      # an engine CONSTANT, read from the engine
        v = CONST[name](); s = fmt(v); self.consts.append(dict(name=name, value=float(v), shown=s)); return s + (f'&nbsp;{unit}' if unit else '')

# ------------------------------------------------------------------ sections
def medical():
    n = Note('medical', 'Planning short-lived medical isotopes: decay-corrected production, generator ingrowth, and the Ac-225 chain')
    a = n.run('chronos_make_now', {'nuclide': 'F-18', 'A_needed': 370, 'hours': 2.5})
    b = n.run('chronos_generator', {'parent': 'Mo-99', 'parent_GBq': 10, 'hours': 23})
    g = n.run('chronos_generator', {'parent': 'Ge-68', 'parent_GBq': 1.85, 'hours': 4})
    c = n.run('chronos_ac225', {'Ac225_MBq_at_purification': 10, 'hours': 6, 'ac227_ratio_eob': 0.0015, 'days_stored': 10})
    n.study = ('[study] The DOE Isotope Program reports world Ac-225 supply of about 1.2&ndash;1.7 Ci per year from Th-229 generators, '
               'judged insufficient, with demand that could reach hundreds of Ci per year; the accelerator route co-produces Ac-227 '
               '(21.8 y), a licensing, waste and perception problem. In Oklahoma, the OU College of Pharmacy cyclotron is set to make PET and therapy agents in-state.')
    n.abstract = (f'Using the Chronos decay engine we work four routine planning questions. To have {n.I(a, "A_needed", "MBq")} of {n.I(a, "nuclide")} left after '
                  f'{n.I(a, "hours", "h")}, {n.N(a, "make_now", "MBq")} must be made now ({n.N(a, "half_lives_elapsed")} half-lives). A {n.I(b, "parent")}/Tc-99m generator eluted to zero '
                  f'reaches its Tc-99m maximum {n.N(b, "peak_hours", "h")} later, with transient-equilibrium ratio {n.N(b, "equilibrium_ratio")}; '
                  f'a {n.I(g, "parent")}/Ga-68 generator peaks after {n.N(g, "peak_hours", "h")}. For {n.I(c, "Ac225_MBq_at_purification", "MBq")} of Ac-225, Bi-213 reaches '
                  f'{n.N(c, "activities_MBq.Bi-213", "MBq")} after {n.I(c, "hours", "h")}, and an Ac-227/Ac-225 activity ratio of {n.I(c, "ac227_ratio_eob")} at end of bombardment grows to '
                  f'{n.N(c, "ac227_ratio_after")} after {n.I(c, "days_stored")} days of storage.')
    n.methods = ('Single-nuclide decay: A(t) = A<sub>0</sub> e<sup>&minus;&lambda;t</sup>, so the activity to make now is A<sub>0</sub> = A<sub>need</sub> e<sup>&lambda;t</sup>. '
                 f'Generators: two-member Bateman solution with the parent-to-daughter branching ({n.K("BR_Mo99_Tc99m")} for Mo-99&rarr;Tc-99m); the daughter maximum after elution is '
                 't<sub>max</sub> = ln(&lambda;<sub>d</sub>/&lambda;<sub>p</sub>)/(&lambda;<sub>d</sub>&minus;&lambda;<sub>p</sub>) and the transient-equilibrium activity ratio is '
                 f'b&middot;&lambda;<sub>d</sub>/(&lambda;<sub>d</sub>&minus;&lambda;<sub>p</sub>). The Ac-225 chain (Fr-221, At-217, Bi-213, then Po-213 {n.K("BR_Bi213_Po213_pct", "%")} / '
                 f'Tl-209 {n.K("BR_Bi213_Tl209_pct", "%")} as used by the engine (ENSDF gives about 97.9/2.1), Pb-209) is solved by matrix exponential; the test suite checks it against '
                 'the analytic Bateman form (CM-PAPERS P5). Ac-227 grows relative to Ac-225 as Ac-225 decays away.')
    n.rows = [(f'{n.I(a, "nuclide")} to make now for {n.I(a, "A_needed", "MBq")} at {n.I(a, "hours", "h")}', n.N(a, 'make_now', 'MBq')),
              ('Tc-99m peak after elution', n.N(b, 'peak_hours', 'h')),
              (f'Tc-99m activity at {n.I(b, "hours", "h")} ({n.I(b, "parent_GBq", "GBq")} {n.I(b, "parent")})', n.N(b, 'daughter_GBq', 'GBq')),
              (f'{n.I(b, "parent")} left at {n.I(b, "hours", "h")}', n.N(b, 'parent_GBq_then', 'GBq')),
              ('Ga-68 peak after elution', n.N(g, 'peak_hours', 'h')),
              (f'Ga-68 at {n.I(g, "hours", "h")} ({n.I(g, "parent_GBq", "GBq")} {n.I(g, "parent")})', n.N(g, 'daughter_GBq', 'GBq')),
              (f'Ac-225 at {n.I(c, "hours", "h")} ({n.I(c, "Ac225_MBq_at_purification", "MBq")} start)', n.N(c, 'activities_MBq.Ac-225', 'MBq')),
              (f'Bi-213 at {n.I(c, "hours", "h")}', n.N(c, 'activities_MBq.Bi-213', 'MBq')),
              (f'Ac-227/Ac-225 after {n.I(c, "days_stored")} d storage ({n.I(c, "ac227_ratio_eob")} at EOB)', n.N(c, 'ac227_ratio_after'))]
    n.limits = ('No dosimetry, shielding, radiochemical yield, or clinical or regulatory judgement. Elution efficiency is taken as 100%. '
                'Half-lives and branchings are fixed evaluated values without uncertainties propagated.')
    n.refs = ['NNDC/ENSDF evaluated half-lives and branchings (nndc.bnl.gov).', 'Bateman, H. (1910) Proc. Cambridge Phil. Soc. 15, 423.',
              'DOE Isotope Program, Ac-225 user group report (isotopes.gov, 2022).']
    return n

def fusion():
    n = Note('fusion', 'Tritium inventory and helium-3 ingrowth for fusion fuel accountancy')
    a = n.run('chronos_tritium', {'grams': 1000, 'years': 1}); b = n.run('chronos_tritium', {'grams': 1000, 'years': 10})
    n.study = ('[study] The DOE Fusion Science &amp; Technology Roadmap (Oct 2025) lists the tritium fuel cycle and breeding blankets as a key gap '
               '("no fusion blanket has yet been built and validated") and plant-level tritium accountancy for nonproliferation.')
    n.abstract = (f'A stored {n.I(a, "grams", "g")} of tritium decays to {n.N(a, "left_g", "g")} after {n.I(a, "years")} year, forming {n.N(a, "He3_g", "g")} of helium-3 '
                  f'({n.N(a, "percent_decayed", "%")} decayed); after {n.I(b, "years")} years {n.N(b, "left_g", "g")} remains. These are the baseline losses any '
                  'accountancy ledger must subtract before attributing a shortfall to process holdup or permeation.')
    n.methods = (f'T-3 decays by beta emission to He-3 with half-life {n.K("T12_H3_y", "y")}: m(t) = m<sub>0</sub> e<sup>&minus;&lambda;t</sup>, and the He-3 mass formed is '
                 '(m<sub>0</sub> &minus; m(t))&middot;M(He-3)/M(T).')
    n.rows = [(f'T left after {n.I(a, "years")} y ({n.I(a, "grams", "g")})', n.N(a, 'left_g', 'g')), (f'He-3 formed in {n.I(a, "years")} y', n.N(a, 'He3_g', 'g')),
              (f'Percent decayed in {n.I(a, "years")} y', n.N(a, 'percent_decayed', '%')),
              (f'T left after {n.I(b, "years")} y', n.N(b, 'left_g', 'g')), (f'He-3 formed in {n.I(b, "years")} y', n.N(b, 'He3_g', 'g'))]
    n.limits = 'Decay only: no breeding, burn-up, permeation, isotope exchange or holdup models.'
    n.refs = ['Lucas, L. L. &amp; Unterweger, M. P. (2000) J. Res. NIST 105, 541 (tritium half-life).', 'DOE Fusion Science &amp; Technology Roadmap (energy.gov, Oct 2025).']
    return n

def fission():
    n = Note('fission', 'Reactor decay heat after shutdown: a first-order estimate')
    ts = [1, 24, 24 * 30]; ids = [n.run('chronos_decay_heat', {'days_operated': 365, 'hours_after_shutdown': h}) for h in ts]
    n.study = ('[study] The WANDA nuclear-data program ranks fission product yields with covariances as the top need for burnup, source term and decay heat.')
    n.abstract = (f'For a core operated {n.I(ids[0], "days_operated")} days, the Way&ndash;Wigner approximation gives decay heat of {n.N(ids[0], "fraction")} of operating power '
                  f'{n.I(ids[0], "hours_after_shutdown")} hour after shutdown, {n.N(ids[1], "fraction")} after {n.I(ids[1], "hours_after_shutdown")} hours, and '
                  f'{n.N(ids[2], "fraction")} after {n.I(ids[2], "hours_after_shutdown")} hours. The estimate is good to about a factor of two and is meant for orientation, not licensing.')
    n.methods = (f'Way&ndash;Wigner: P/P<sub>0</sub> = {n.K("WW_coeff")} [t<sup>&minus;0.2</sup> &minus; (t+T)<sup>&minus;0.2</sup>], with t the time after shutdown and T the operating time, '
                 'both in seconds.')
    n.rows = [(f'P/P0 at {n.I(i, "hours_after_shutdown")} h after {n.I(i, "days_operated")} d operation', n.N(i, 'fraction')) for i in ids]
    n.limits = 'Approximate (~factor 2 at extremes); excludes U-239/Np-239 capture products; not ANS-5.1; no inventory-specific summation.'
    n.refs = ['Way, K. &amp; Wigner, E. P. (1948) Phys. Rev. 73, 1318.', 'ANSI/ANS-5.1 decay heat standard (for the full method).']
    return n

def safeguards():
    n = Note('safeguards', 'Nuclear clocks for safeguards and environmental forensics: release age and plutonium separation age')
    a = n.run('chronos_release_age', {'pair': 'Cs-134/Cs-137', 'ratio_now': 0.05, 'ratio_at_release': 1})
    b = n.run('chronos_pu_age', {'am_over_pu_activity': 0.02})
    n.study = ('[study] Safeguards data priorities include Pu-239/240/241, Am-241, Cs-134 and Cs-137, with decay-data covariances and 1&ndash;3% on dominant channels.')
    n.abstract = (f'A {n.I(a, "pair")} activity ratio that fell from {n.I(a, "ratio_at_release")} at release to {n.I(a, "ratio_now")} now dates the release to {n.N(a, "years", "years")} ago. '
                  f'An Am-241/Pu-241 activity ratio of {n.I(b, "am_over_pu_activity")} dates plutonium separation to {n.N(b, "years", "years")} ago.')
    n.methods = ('Release clock: R(t) = R<sub>0</sub> e<sup>&minus;(&lambda;<sub>134</sub>&minus;&lambda;<sub>137</sub>)t</sup>, inverted for t. '
                 f'Separation clock: Am-241 grows from Pu-241 ({n.K("T12_Pu241_y", "y")}) and decays ({n.K("T12_Am241_y", "y")}); the two-member Bateman activity ratio is inverted for t.')
    n.rows = [(f'Release age from {n.I(a, "pair")} = {n.I(a, "ratio_now")} (from {n.I(a, "ratio_at_release")})', n.N(a, 'years', 'y')),
              (f'Plutonium separation age from Am/Pu activity {n.I(b, "am_over_pu_activity")}', n.N(b, 'years', 'y'))]
    n.limits = 'Assumes a single clean event, a known initial ratio, and no later fractionation or mixing; counting uncertainties are not propagated.'
    n.refs = ['NNDC/ENSDF evaluated half-lives.', 'IAEA safeguards nuclear-data needs (WANDA 2025&ndash;26 summaries).']
    return n

def nucleosynthesis():
    n = Note('nucleosynthesis', 'Radioactive clocks of the cosmos: supernova heating, nickel masses, kilonovae, white-dwarf mergers and stellar ages')
    a = n.run('chronos_supernova', {'M_Ni_Msun': 0.6, 'days': 18, 't0_days': 35})
    b = n.run('chronos_nickel_mass', {'L_erg_s': 1e41, 'days': 200, 'mode': 'tail', 't0_days': 40})
    k = n.run('chronos_kilonova', {'M_ej_Msun': 0.05, 'days': 1})
    w = n.run('chronos_wd_merger', {'period_s': 765, 'm1': 0.26, 'm2': 0.50})
    s = n.run('chronos_star_age', {'pair': 'Th/Eu', 'log_eps_observed': -0.52, 'production_ratio': 0.45})
    n.study = ('[study] Open r-process questions: dominant sites (neutron-star mergers confirmed; collapsars unresolved), delay times, actinide-boost stars; '
               'nuclear data needed for neutron-rich half-lives, masses and capture rates (arXiv:2507.08760).')
    n.abstract = (f'{n.I(a, "M_Ni_Msun")} solar masses of Ni-56 heats a Type Ia supernova at {n.N(a, "erg_per_s", "erg/s")} on day {n.I(a, "days")}, with gamma-ray trapping time '
                  f't<sub>0</sub> = {n.I(a, "t0_days", "d")}. Inverting a tail of {n.I(b, "L_erg_s", "erg/s")} at day {n.I(b, "days")} with t<sub>0</sub> = {n.I(b, "t0_days", "d")} gives '
                  f'{n.N(b, "M_Ni_Msun", "M&#8857;")} of Ni-56 (the two examples use different, separately chosen t<sub>0</sub>). {n.I(k, "M_ej_Msun", "M&#8857;")} of kilonova ejecta gives a '
                  f'thermalised luminosity of about {n.N(k, "erg_per_s", "erg/s")} at day {n.I(k, "days")} (f<sub>th</sub> = {n.K("KN_fth_default")}). The {n.I(w, "period_s", "s")} double white dwarf '
                  f'J0651 ({n.I(w, "m1")} + {n.I(w, "m2")} M&#8857;) merges in {n.N(w, "merger_Myr", "Myr")} (GW frequency {n.N(w, "f_gw_mHz", "mHz")}), and an observed Th/Eu of '
                  f'{n.I(s, "log_eps_observed")} dex with a linear production ratio of {n.I(s, "production_ratio")} gives a star age of {n.N(s, "age_Gyr", "Gyr")}.')
    n.methods = ('Ni-56&rarr;Co-56&rarr;Fe-56 heating with gamma trapping 1&minus;e<sup>&minus;t<sub>0</sub><sup>2</sup>/t<sup>2</sup></sup> and local positron deposition; '
                 f'kilonova luminosity L = f<sub>th</sub> M<sub>ej</sub> 10<sup>10</sup> (t/day)<sup>&minus;1.3</sup> erg s<sup>&minus;1</sup> g<sup>&minus;1</sup> (Korobkin et al. 2012 heating; Metzger 2019 normalisation); '
                 'Peters (1964) gravitational-wave coalescence time; Th-232 cosmochronometry '
                 f't = {n.K("Th_factor_Gyr", "Gyr")} &times; [log<sub>10</sub>(Th/Eu)<sub>0</sub> &minus; log<sub>10</sub>(Th/Eu)<sub>obs</sub>], with the production ratio given linearly and converted to dex.')
    n.rows = [(f'Ni-56 heating, {n.I(a, "M_Ni_Msun")} M&#8857;, day {n.I(a, "days")}, t<sub>0</sub> {n.I(a, "t0_days", "d")}', n.N(a, 'erg_per_s', 'erg/s')),
              (f'Ni-56 mass from tail {n.I(b, "L_erg_s", "erg/s")} at {n.I(b, "days", "d")}, t<sub>0</sub> {n.I(b, "t0_days", "d")}', n.N(b, 'M_Ni_Msun', 'M&#8857;')),
              (f'Kilonova thermalised luminosity, {n.I(k, "M_ej_Msun")} M&#8857;, {n.I(k, "days", "d")}', n.N(k, 'erg_per_s', 'erg/s')),
              ('J0651 merger time', n.N(w, 'merger_Myr', 'Myr')), ('J0651 GW frequency', n.N(w, 'f_gw_mHz', 'mHz')), ('Th/Eu star age', n.N(s, 'age_Gyr', 'Gyr'))]
    n.limits = ('Kilonova luminosity is order-of-magnitude only, with a constant thermalisation efficiency; the Peters time is a point-mass upper bound to contact; the production ratio dominates the stellar-age '
                'uncertainty; no radiative transfer or light-curve fitting.')
    n.refs = ['Arnett, W. D. (1982) ApJ 253, 785.', 'Korobkin, O. et al. (2012) MNRAS 426, 1940.', 'Metzger, B. D. (2019) Living Rev. Relativ. 23, 1.',
              'Peters, P. C. (1964) Phys. Rev. 136, B1224.', 'Brown, W. R. et al. (2011) ApJL 737, L23 (J0651).', 'Recent advances in r-process nucleosynthesis, arXiv:2507.08760.']
    return n

SECTIONS = {'medical': (4, medical), 'fusion': (2, fusion), 'nucleosynthesis': (3, nucleosynthesis), 'fission': (5, fission), 'safeguards': (6, safeguards)}

CSS = """:root{--bg:#fbfaf7;--fg:#1d1a24;--muted:#5d5670;--line:#ddd6e8;--accent:#5b3fa8;--panel:#f3f0f8}
@media (prefers-color-scheme:dark){:root{--bg:#0d0a16;--fg:#ece6ff;--muted:#a69ccc;--line:#2c2147;--accent:#b18cff;--panel:#140e24}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 Georgia,'Times New Roman',serif;padding:24px max(16px,4vw)}
main{max-width:860px;margin:0 auto}h1{font:600 1.7rem/1.25 'Segoe UI',system-ui,sans-serif;margin:.2em 0}h2{font:600 1.05rem 'Segoe UI',system-ui,sans-serif;
letter-spacing:.06em;text-transform:uppercase;color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:2em}
.by{color:var(--muted);font:14px 'Segoe UI',system-ui,sans-serif}.abs{background:var(--panel);border-left:3px solid var(--accent);padding:12px 16px}
table{border-collapse:collapse;width:100%;font:14px 'Segoe UI',system-ui,sans-serif}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}
td:last-child{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}canvas{width:100%;height:330px;display:block;border-radius:8px;margin:12px 0}
details.lantern{font:13px 'Segoe UI',sans-serif;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:6px 10px}
pre{white-space:pre-wrap;font:11px Consolas,monospace;color:var(--muted);background:var(--panel);padding:10px;border-radius:6px;overflow-x:auto}
.tag{font:12px 'Segoe UI',sans-serif;color:var(--muted)}@media print{canvas{break-inside:avoid}details.lantern{display:none}}"""

VALID = {'medical': 'chains are solved two independent ways (analytic Bateman and matrix exponential) agreeing to round-off',
         'safeguards': 'the two-member clocks use the analytic Bateman solution, cross-checked against the matrix-exponential solver',
         'fusion': 'the tritium law is a closed-form decay checked in the D2189 tests', 'fission': 'the Way&ndash;Wigner law is closed-form and checked in the D2189 tests',
         'nucleosynthesis': 'each law is closed-form or a two-member Bateman solution, checked in the D2189 tests'}

def n_charts(n):
    return len({c['chart']['title'] for c in n.calls if c.get('chart')})

def render(n, sec_no, ehash):
    charts, seen = [], set()
    for c in n.calls:
        if c.get('chart') and c['chart']['title'] not in seen: seen.add(c['chart']['title']); charts.append(c['chart'])
    prov = [dict(name=c['name'], args=c['args'], result=c['result']) for c in n.calls]
    iris = open(os.path.join(HERE, 'iris.js'), encoding='utf-8').read()
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in n.rows)
    refs = ''.join(f'<li>{r}</li>' for r in n.refs)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(n.key.title())} &middot; Chronos Note</title><style>{CSS}</style></head><body><main>
{lantern()}
<p class="tag">CubeMind &middot; Chronos technical note &middot; Nuclear Research Limb &sect;{sec_no} &middot; built {time.strftime('%Y-%m-%d')}</p>
<h1>{n.title}</h1>
<p class="by">Danny Lee Eldridge (independent researcher, Oklahoma City) with the CubeMind/Chronos engine. Every number below is printed directly from a logged engine call (appendix).</p>
<h2>Abstract</h2><p class="abs">{n.abstract}</p>
<h2>Context from the field</h2><p>{n.study}</p>
<h2>Method</h2><p>{n.methods}</p>
<h2>Results</h2><table><tr><th>Quantity</th><th>Engine value</th></tr>{rows}</table>
<div id="charts"></div><p class="tag">Charts are drawn from the engine's own output; hover to read exact values.</p>
<h2>Validation</h2><p>Chronos was built under locked pre-registrations (D2189 and amendments A1&ndash;A3); {VALID[n.key]}, and cleared by adversarial referee rounds (R77, R78, R78b NULL) recorded in the public ledger. Engine files sha256: <code>{ehash[:16]}&hellip;</code></p>
<h2>Limits</h2><p>{n.limits}</p>
<h2>References</h2><ol>{refs}</ol>
<h2>Appendix: engine calls</h2><pre>{html.escape(json.dumps(prov, indent=1, default=str))}</pre>
</main><script>{iris}</script><script>const CH={json.dumps(charts)};
CH.forEach(c=>{{const cv=document.createElement('canvas');document.getElementById('charts').appendChild(cv);Iris.render(cv,c,{{duration:1800}});}});</script></body></html>"""

def build(section='all', out_dir=None):
    out_dir = out_dir or os.path.join(HERE, 'papers'); os.makedirs(out_dir, exist_ok=True); t0 = time.time()
    keys = list(SECTIONS) if section in (None, '', 'all') else [section]; ehash = engine_hash(); made = []
    for k in keys:
        sec_no, fn = SECTIONS[k]; n = fn()
        open(os.path.join(out_dir, f'{k}.html'), 'w', encoding='utf-8').write(render(n, sec_no, ehash))
        json.dump(dict(calls=[dict(name=c['name'], args=c['args']) for c in n.calls], printed=n.printed, inputs=n.inputs, consts=n.consts), open(os.path.join(out_dir, f'{k}.trace.json'), 'w'), indent=1)
        made.append(dict(section=k, title=n.title, file=f'papers/{k}.html', numbers=len(n.printed), charts=n_charts(n)))
    if len(keys) > 1:
        items = ''.join(f'<li><a href="{m["section"]}.html">{m["title"]}</a> <span class="tag">&sect;{SECTIONS[m["section"]][0]} &middot; {m["numbers"]} engine numbers &middot; {m["charts"]} charts</span></li>' for m in made)
        open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(f"""<!doctype html><html><head><meta charset="utf-8"><title>Chronos Notes</title><style>{CSS}</style></head><body><main>{lantern()}
<h1>Chronos technical notes: the nuclear field suite</h1><p class="by">Danny Lee Eldridge with CubeMind. One note per field of the Nuclear Research Limb that the engine covers.</p><ol>{items}</ol>
<p class="tag">Not built: &sect;1 (double-beta converter, planned), &sect;7 space and aviation radiation (no dose tool yet; would need vetted coefficients).</p></main></body></html>""")
    return dict(made=made, seconds=round(time.time() - t0, 2), index='papers/index.html' if len(keys) > 1 else None)

if __name__ == '__main__':
    print(json.dumps(build(sys.argv[1] if len(sys.argv) > 1 else 'all'), indent=1))
