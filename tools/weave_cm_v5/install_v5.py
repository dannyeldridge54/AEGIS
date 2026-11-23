"""Install CubeMind v5 (the Weave in LCDM parts as central thinking). Run from the CubeMind_janus folder:
    python install_v5.py <kit_dir>
Idempotent. Every patched file is first copied to <file>.bak_v5_22nov (nothing is deleted)."""
import pathlib, shutil, sys
CM = pathlib.Path('.').resolve(); KIT = pathlib.Path(sys.argv[1]).resolve(); log = []
def backup(p):
    b = p.with_name(p.name + '.bak_v5_22nov')
    if p.exists() and not b.exists(): shutil.copy2(p, b)
# 1. facts, brief, prize board, vault tools
for f in ('WEAVE_FACTS.txt', 'CUBEMIND_V5_BRIEF.md', 'PRIZE_BOARD.md'):
    backup(CM / f); shutil.copy2(KIT / f, CM / f)
for f in ('weave_vault.py', 'weave_dials_rng.py'): shutil.copy2(KIT / f, CM / 'ufe_tools' / f)
log.append('facts v5, brief, prize board, vault tools')
# 2. calibrated engine into the bundle + registration
W = CM / 'aegis_tools' / 'aegis_bundle' / 'tools' / 'weave_cm'
for f in ('weave_engine.py', 'early_calib.json'): shutil.copy2(KIT / f, W / f)
wt = W / 'weave_tools.py'; s = wt.read_text(encoding='utf-8')
if 'weave_engine' not in s:
    backup(wt)
    s += ("\n# v5 (22 Nov 2026): the calibrated Weave late-universe engine (AEGIS D2134; gate 8e-5 vs CAMB)\n"
          "try:\n    import weave_engine as _WE\n    TOOLS['weave_engine'] = _WE.run\nexcept Exception as _e:\n"
          "    TOOLS['weave_engine'] = lambda a, _m=str(_e): {'error': 'weave_engine unavailable: ' + _m}\n")
    wt.write_text(s, encoding='utf-8'); log.append('weave_tools: weave_engine registered')
rp = CM / 'aegis_tools' / 'registry.py'; s = rp.read_text(encoding='utf-8')
if "'weave_engine'" not in s:
    backup(rp); s = s.replace("TOOLS = {\n", "TOOLS = {\n 'weave_engine': ('{\"mode\": \"background\", \"ui\": 0.13}', 180),\n", 1)
    rp.write_text(s, encoding='utf-8'); log.append('registry: weave_engine')
# 3. missions: the full prize list + big questions
mp = CM / 'janus' / 'mission.py'; s = mp.read_text(encoding='utf-8')
if 'Beal conjecture' not in s:
    backup(mp)
    s = s.replace("'the strong CP problem', 'the matter-antimatter asymmetry']",
                  "'the strong CP problem', 'the matter-antimatter asymmetry',\n"
                  "            'Beal conjecture', 'Collatz conjecture', 'small open Erdos problems', 'a sieve that beats the GIMPS 420/4620 wheel (vortex track)',\n"
                  "            'Hutter Prize compression gains', 'the S8 tension', 'the neutrino-mass preference from DESI', 'dynamical dark energy and the phantom crossing',\n"
                  "            'the cosmological constant from first principles', 'cosmic birefringence', 'alpha_s at M_Z (the Weave fails it)']", 1)
    mp.write_text(s, encoding='utf-8'); log.append('mission: prize list')
# 4. lens + exam facts
lp = CM / 'janus' / 'ufe_lens.py'; s = lp.read_text(encoding='utf-8')
if 'v5 CENTRAL' not in s:
    backup(lp)
    s = s.replace('LENS = ("UFE LENS (the Weave, v4). ', 'LENS = ("UFE LENS (the Weave, v4; v5 CENTRAL: for any physics or astrophysics question use the Weave in LCDM parts '
                  'and check numbers with the calibrated tool weave_engine; dark energy = reverse thread V = V_L(1 - 7.30 e^(-2.83 phi)), w >= -1; '
                  'H0 tension NOT solved; thread-DM coupling NOT adopted). ', 1)
    lp.write_text(s, encoding='utf-8'); log.append('lens: v5 central line')
ap = CM / 'janus' / 'astro.py'; s = ap.read_text(encoding='utf-8')
if 'reverse thread' not in s:
    backup(ap)
    add = ("    ('In the Weave reverse thread V = V_L(1 - A e^(-beta phi)), what is A = 16 zeta(2)/(3 zeta(3))?', 'NUM:7.30:0.01'),\n"
           "    ('In the Weave reverse thread, beta = 2 sqrt 2. Give its value.', 'NUM:2.828:0.01'),\n"
           "    ('Can the Weave dark-energy thread have w below -1? Answer YES or NO.', 'NO'),\n"
           "    ('Does the Weave solve the Hubble tension? Answer YES or NO.', 'NO'),\n"
           "    ('Was the thread-dark-matter coupling b adopted (D2134)? Answer YES or NO.', 'NO'),\n"
           "    ('Weave sum of neutrino masses in eV (input, normal ordering)?', 'NUM:0.0587:0.01'),\n")
    s = s.replace("UFE_FACTS = [\n", "UFE_FACTS = [\n" + add, 1); ap.write_text(s, encoding='utf-8'); log.append('astro: 6 v5 exam facts')
# 5. data: AEGIS LCDM-parts results + Mersenne kit
for sub in ('lcdm', 'mersenne'):
    d = CM / ('weave_data' if sub == 'lcdm' else '.') / sub; d.mkdir(parents=True, exist_ok=True)
    for f in (KIT / sub).iterdir(): shutil.copy2(f, d / f.name)
log.append('weave_data/lcdm + mersenne/ copied')
print('\n'.join(log))
