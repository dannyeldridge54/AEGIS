import sys, json; sys.path.insert(0, '.')
import numpy as np
from tools.sound import engine as E
from tools.chem.wavelength import line
import scipy.constants as K
sg = json.load(open('docs/web/string_geom.json')); y = sg['y']
# (a) torus glide: y high->low mapped to 440->180 Hz (inflation long tube -> round torus)
f_tr = E.map_series(y, 180.0, 440.0, invert=False)  # high y -> high freq; y falls over time -> pitch falls
gl = E.glide(f_tr, 8.0, amp=0.45, vib=0.01)
# (b) Balmer chord: real THz frequencies scaled into audible by 1/1.0377e12
thz = {nm: K.c/(line('H', 2, up)*1e-9)/1e12 for nm, up in (('Ha', 3), ('Hb', 4), ('Hg', 5), ('Hd', 6))}
SCALE = 1.0377e12; aud = {nm: v*1e12/SCALE for nm, v in thz.items()}
layers = [gl]
for i, (nm, f) in enumerate(aud.items()):
    layers.append(np.concatenate([np.zeros(int(0.3*i*E.SR)), E.note(f, 8.0 - 0.3*i, 'saw', amp=0.18, vib=0.004)]))
m = E.mix(layers, 8.0); info = E.write_wav('field_tests/results/s1_demo.wav', m, stereo=True)
# tests
import wave
w = wave.open('field_tests/results/s1_demo.wav'); T1 = (w.getframerate() == 44100 and w.getsampwidth() == 2 and w.getnchannels() in (1, 2)); w.close()
T2 = abs(info['dur'] - 8.0) <= 0.1; T3 = info['peak'] <= 1.0 and info['rms'] > 0.02
# T4: FFT of a short pure render of each Balmer tone vs target
def peakhz(f):
    s = E.note(f, 1.0, 'saw', amp=0.5, env=False); sp = np.abs(np.fft.rfft(s*np.hanning(len(s)))); fr = np.fft.rfftfreq(len(s), 1/E.SR); return fr[np.argmax(sp)]
T4 = all(abs(peakhz(f)/f - 1) <= 0.01 for f in aud.values())
L = [f"render: {json.dumps(info)}",
     f"torus glide Hz: {f_tr[0]:.1f} → {f_tr[-1]:.1f} (y {y[0]:.2f}→{y[-1]:.2f})",
     f"Balmer audible Hz: " + ", ".join(f"{k} {v:.1f}" for k, v in aud.items()) + f" (ratios {', '.join(f'{v/aud['Ha']:.3f}' for v in aud.values())})",
     f"T1 WAV 44100/16-bit: {T1}", f"T2 dur 8.0±0.1: {T2} ({info['dur']:.3f})", f"T3 peak≤1 & RMS>0.02: {T3} (peak {info['peak']:.3f}, rms {info['rms']:.3f})", f"T4 FFT peaks match ratios ≤1%: {T4}",
     f"S1 VERDICT: {'ALL PASS → ADOPT engine' if (T1 and T2 and T3 and T4) else 'FAIL'}"]
open('field_tests/results/s1_sound.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
