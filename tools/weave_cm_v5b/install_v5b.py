"""Install CubeMind v5b: result watcher + re-derivation tools. Run from CubeMind_janus: python install_v5b.py <kit_dir>. Backs up as .bak_v5b_22nov."""
import pathlib, shutil, sys
CM = pathlib.Path('.').resolve(); KIT = pathlib.Path(sys.argv[1]).resolve(); log = []
def backup(p):
    b = p.with_name(p.name + '.bak_v5b_22nov')
    if p.exists() and not b.exists(): shutil.copy2(p, b)
W = CM / 'aegis_tools' / 'aegis_bundle' / 'tools' / 'weave_cm'
shutil.copy2(KIT / 'weave_verify.py', W / 'weave_verify.py'); log.append('weave_verify.py installed')
wt = W / 'weave_tools.py'; s = wt.read_text(encoding='utf-8')
if 'weave_verdict' not in s:
    backup(wt)
    s += ("\n# v5b (22 Nov 2026): re-derivation checks for incoming Weave fit results\ntry:\n    import weave_verify as _WV\n"
          "    TOOLS['weave_verdict'] = _WV.weave_verdict; TOOLS['weave_wtoday'] = _WV.weave_wtoday\nexcept Exception as _e:\n    pass\n")
    wt.write_text(s, encoding='utf-8'); log.append('weave_tools: weave_verdict, weave_wtoday')
rp = CM / 'aegis_tools' / 'registry.py'; s = rp.read_text(encoding='utf-8')
if "'weave_verdict'" not in s:
    backup(rp); s = s.replace("TOOLS = {\n", "TOOLS = {\n 'weave_verdict': ('{\"chi2_W\": 7217.7, \"chi2_L\": 7215.3}', 10),\n 'weave_wtoday': ('{\"ui\": 0.157}', 120),\n", 1)
    rp.write_text(s, encoding='utf-8'); log.append('registry: 2 tools')
lp = CM / 'mindmem' / 'learn_loop.py'; s = lp.read_text(encoding='utf-8')
if 'step_lcdm_watch' not in s:
    backup(lp)
    helper = '''
def step_lcdm_watch():
    """v5b (Danny 22 Nov 20:56): pick up new Weave fit results (PC + cloud), store as EVIDENCE, queue blind re-derivations."""
    try:
        import sys as _s
        tdir = HERE / 'aegis_tools' / 'aegis_bundle' / 'tools' / 'weave_cm'
        if str(tdir) not in _s.path: _s.path.insert(0, str(tdir))
        import weave_verify as _WV
        return _WV.step(str(HERE))
    except Exception as e:
        return {'lcdm_watch_error': f'{type(e).__name__}: {e}'}
'''
    s = s.replace('\ndef step_derive():', helper + '\ndef step_derive():', 1)
    s = s.replace("    rec.update(step_weave())\n", "    rec.update(step_weave())\n    rec.update(step_lcdm_watch())\n", 1)
    lp.write_text(s, encoding='utf-8'); log.append('learn_loop: step_lcdm_watch')
print('\n'.join(log))
