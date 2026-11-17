"""J7h (locked PREREG_J7h_pulse_fixups): ASPIC side for the 6 fixed models, then reuse J7f/J7g machinery with separate part files."""
import sys, os, subprocess, importlib.util; sys.path.insert(0, '.')
def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
F = load('j7f', 'theory/janus/j7f_pulse.py'); G = load('j7g', 'theory/janus/j7g_pulse_reheat.py')
NEW = {'gmlfi': ['2._kp', '1._kp', '0.01_kp'], 'ncli': ['1e-4_kp', '0.18_kp', '2._kp'], 'rpqti': ['10._kp', '0.01_kp', '-0.01_kp'],
       'cnbi': ['1e-2_kp'], 'kmiii': ['1e10_kp', '1e4_kp'], 'hi': ['20000._kp']}
F.P = NEW; G.F.P = NEW
F.PART = 'field_tests/results/janus_j7h_p1.part.jsonl'; G.F.PART = F.PART; G.PART = 'field_tests/results/janus_j7h_p23.part.jsonl'
def aspic():
    I, OUT = F.I, F.OUT
    for m, pars in NEW.items():
        d = f'{OUT}/{m}'; os.makedirs(d, exist_ok=True)
        for tag, src, outname in (('p', F.fsrc(m, pars), 'out.txt'), ('r', G.src(m, pars), 'reheat_out.txt')):
            open(f'{d}/{tag}.f90', 'w').write(src)
            cc = subprocess.run(['gfortran', '-O2', '-ffree-line-length-none', f'-I{I}/include/aspic', f'{d}/{tag}.f90', f'-L{I}/lib', '-laspic', f'-Wl,-rpath,{I}/lib', '-o', f'{d}/{tag}'], capture_output=True, text=True)
            if cc.returncode: open(f'{d}/{outname}', 'w').write('COMPILE ' + cc.stderr[-300:]); print(m, tag, 'compile fail'); continue
            try: r = subprocess.run([f'{d}/{tag}'], capture_output=True, text=True, timeout=300); txt = r.stdout + r.stderr
            except subprocess.TimeoutExpired: txt = 'TIMEOUT'
            open(f'{d}/{outname}', 'w').write(txt); print(m, tag, txt.count('PT ') + txt.count('RT '), flush=True)
if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'aspic': aspic()
    elif a == 'p1': F.run(); 
    elif a == 'p23': G.run()
    elif a == 'summary':
        F.summary.__globals__['PART'] = F.PART
        import json
        for l in open(F.PART): print(l.strip()[:200])
