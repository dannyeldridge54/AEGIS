"""J7k (locked PREREG_J7k_listed_long): RPQTI, HI, KMIII with long limits on the PC."""
import sys, os, json, subprocess, runpy; sys.path.insert(0, '.')
P1 = 'field_tests/results/janus_j7k_p1.part.jsonl'; P23 = 'field_tests/results/janus_j7k_p23.part.jsonl'; MODELS = ('rpqti', 'hi', 'kmiii')
SETUP = ("import runpy,sys,os; sys.argv=['x']; g=runpy.run_path('theory/janus/j7h_fixups.py'); F,G=g['F'],g['G']; "
         "F.I=os.path.expanduser('~/aspic_inst'); F.PART='" + P1 + "'; G.F.PART=F.PART; G.PART='" + P23 + "'; ")
if sys.argv[1] == 'aspic':
    for m in MODELS:   # same driver code as J7h aspic(), timeout 3600 s
        code = SETUP + ("import subprocess as S; I,OUT=F.I,F.OUT; pars=g['NEW']['%s']; d=f'{OUT}/%s'; os.makedirs(d,exist_ok=True)\n"
            "for tag,src,on in (('p',F.fsrc('%s',pars),'out.txt'),('r',G.src('%s',pars),'reheat_out.txt')):\n"
            "  open(f'{d}/{tag}.f90','w').write(src); cc=S.run(['gfortran','-O2','-ffree-line-length-none',f'-I{I}/include/aspic',f'{d}/{tag}.f90',f'-L{I}/lib','-laspic',f'-Wl,-rpath,{I}/lib','-o',f'{d}/{tag}'],capture_output=True,text=True)\n"
            "  if cc.returncode: open(f'{d}/{on}','w').write('COMPILE '+cc.stderr[-300:]); print('%s',tag,'compile fail'); continue\n"
            "  try: r=S.run([f'{d}/{tag}'],capture_output=True,text=True,timeout=3600); txt=r.stdout+r.stderr\n"
            "  except S.TimeoutExpired: txt='TIMEOUT'\n"
            "  open(f'{d}/{on}','w').write(txt); print('%s',tag,txt.count('PT ')+txt.count('RT '),flush=True)\n") % ((m,)*6)
        subprocess.run([sys.executable, '-c', code])
elif sys.argv[1] == 'run':
    done = {json.loads(l)['m'] for l in open(P1) if l.strip()} if os.path.exists(P1) else set()
    for m in MODELS:
        if m in done: continue
        code = SETUP + f"F.P={{'{m}': g['NEW']['{m}']}}; G.F.P=F.P; F.run(); G.run()"
        try: subprocess.run([sys.executable, '-c', code], timeout=7200)
        except subprocess.TimeoutExpired:
            open(P1, 'a').write(json.dumps(dict(m=m, status='listed', why='per-model wall limit 2 h (J7k)')) + '\n'); print(m, 'listed (2 h)', flush=True)
    print('J7K DONE', flush=True)
