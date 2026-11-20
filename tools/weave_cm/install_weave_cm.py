"""Install the Weave derivation track into CubeMind (run from the CubeMind_janus folder: python3 install_weave_cm.py <kit_dir>).
Idempotent. Backs up every file it patches as <file>.bak_weave_20nov (copy; nothing is deleted)."""
import pathlib, re, shutil, sys
CM = pathlib.Path('.').resolve(); KIT = pathlib.Path(sys.argv[1]).resolve()
def backup(p):
    b = p.with_name(p.name + '.bak_weave_20nov')
    if not b.exists(): shutil.copy2(p, b)
log = []
# 1. tools into the bundle
dst = CM / 'aegis_tools' / 'aegis_bundle' / 'tools' / 'weave_cm'; dst.mkdir(parents=True, exist_ok=True)
for f in ('weave_tools.py', 'weave_sweep.py'): shutil.copy2(KIT / f, dst / f)
log.append('tools -> ' + str(dst))
# 2. brief + facts + merged log
for f in ('WEAVE_BRIEF.md', 'WEAVE_FACTS.txt', 'PAPERS_2026-11-20.md', 'WEAVE_RUNG_NAMES.md', 'WEAVE_QUARK_LADDER.md'):
    if (KIT / f).exists(): shutil.copy2(KIT / f, CM / f)
d = CM / 'DERIVATION_LOG.md'; backup(d); shutil.copy2(KIT / 'DERIVATION_LOG_merged.md', d)
la = CM / 'aegis_link' / 'DERIVATION_LOG.md'
if la.exists(): backup(la); shutil.copy2(KIT / 'DERIVATION_LOG_merged.md', la)
log.append('merged DERIVATION_LOG installed')
# 3. registry: weave tools
rp = CM / 'aegis_tools' / 'registry.py'; s = rp.read_text(encoding='utf-8')
if "'weave_rung'" not in s:
    backup(rp)
    entries = {'weave_rung': ('{"m": 9}', 5), 'weave_rung_of': ('{"masses": [0.0028, 0.0557, 2.794]}', 5), 'weave_koide': ('{"masses": [1.29e-3, 0.629, 169]}', 5),
               'weave_koide_slip': ('{"eps": 1e-4}', 30), 'weave_tauq': ('{"mass_GeV": 3e10, "phi0": 1}', 5),
               'weave_ckm': ('{"model": "w864", "rung_d": 1, "rung_u": 9, "down": {"r1": 1.8, "r2": 0.7, "g_abs": 0.8, "g_arg": 2.9, "f_abs": 2.2, "f_arg": 3.1}, "up": {"r1": 2.6, "r2": 0.33, "g_abs": 0.4, "g_arg": -3.1, "f_abs": 1.7, "f_arg": -3.1}}', 60),
               'weave_proton': ('{"dmhat_over_mhat": 0.01, "dms_over_ms": 0.0}', 5), 'weave_atomic': ('{"m_e_MeV": 0.511, "alpha": 0.0072973525, "m_p_MeV": 938.272}', 5)}
    add = ''.join(f" {k!r}: ({v[0]!r}, {v[1]}),\n" for k, v in entries.items())
    s = s.replace("TOOLS = {\n", "TOOLS = {\n" + add, 1)
    branch = ("elif name.startswith('weave_'):   # Weave derivation track (20 Nov 2026)\n"
              "    sys.path.insert(0, os.path.join(os.environ['AEGIS_DIR'], 'tools', 'weave_cm')); import weave_tools as _W; out = _W.TOOLS[name](a)\n")
    s = s.replace("\nprint(json.dumps(out, default=str))", "\n" + branch + "print(json.dumps(out, default=str))", 1)
    rp.write_text(s, encoding='utf-8'); log.append('registry patched (8 weave tools)')
# 4. learn loop: Weave facts + data-builder step
lp = CM / 'mindmem' / 'learn_loop.py'; s = lp.read_text(encoding='utf-8')
if 'step_weave' not in s:
    backup(lp)
    s, n = re.subn(r'        facts = \("\\nMODEL FACTS.*?\\n"\)\n',
                   "        facts = _weave_facts()\n", s, count=1, flags=re.S)
    if n != 1: raise SystemExit('facts block not found; nothing written')
    helper = '''
def _weave_facts():
    """Model facts for the proposer: WEAVE_FACTS.txt (20 Nov 2026) if present, else the old SERAPIS-E line."""
    p = HERE / 'WEAVE_FACTS.txt'
    try: return '\\n' + p.read_text(encoding='utf-8').strip()[:3000] + '\\n'
    except Exception: return "\\nMODEL FACTS: SERAPIS-E has ONE torus modulus tau; vacuum only at rho.\\n"
def step_weave():
    """Weave data builder (Danny 20 Nov: 'give it most of what's left in storage to build up the data and sift'): a time-boxed
    batch of systematic scans into weave_data/ (disk guard: keeps >= WEAVE_MIN_FREE_GB free), then the current best points go
    into MindMem as tool results (EVIDENCE of what the tool returns; the physics stays HYPOTHESIS until locked and refereed)."""
    try:
        import sys as _s
        tdir = HERE / 'aegis_tools' / 'aegis_bundle' / 'tools' / 'weave_cm'
        if str(tdir) not in _s.path: _s.path.insert(0, str(tdir))
        import weave_sweep as WS
        res = WS.run(str(HERE / 'weave_data'), seconds=int(os.environ.get('WEAVE_SWEEP_S', '240')))
        if isinstance(res.get('weave_sweep'), int) and res.get('best_at'):
            from mindmem.store import Store
            S = Store(str(HERE / 'cubemind_memory.jsonl'))
            txt = f"WEAVE SCAN best so far: {res['best_at']} score {res['best_score']} (O(1) box, locked Q8/Q12 tolerances; rows in weave_data/ckm_scan.jsonl)"
            if not any(r['text'] == txt for r in S.recs[-50:]):
                S.add(txt, 'weave_sweep', kind='tool_result', tier='EVIDENCE', topic='weave', importance=3)
        return res
    except Exception as e:
        return {'weave_error': f'{type(e).__name__}: {e}'}
'''
    s = s.replace('\ndef step_ingest():', helper + 'def step_ingest():', 1)
    s = s.replace("    rec.update(step_resultbus())\n", "    rec.update(step_resultbus())\n    rec.update(step_weave())\n", 1)
    lp.write_text(s, encoding='utf-8'); log.append('learn_loop patched (Weave facts + step_weave)')
print('\n'.join(log))
