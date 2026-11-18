import sys, json; sys.path.insert(0, '.')
from tools.power.circuits import solar_iv, rc_lowpass, rl_lowpass
s = solar_iv(); R, C, L = 1000.0, 1e-6, 1.0
fc = 1/(2*3.141592653589793*R*C); rc = rc_lowpass(fc, R, C); lfc = R/(2*3.141592653589793*L); rl = rl_lowpass(lfc, R, L)
T1 = 36 <= s['Voc'] <= 40 and abs(s['Isc'] - 8.8) < 0.1 and 230 <= s['Pmax'] <= 270 and 0.70 <= s['FF'] <= 0.80
T2 = abs(s['mpp_residual']) <= 1e-6
T3 = abs(rc['mag'] - 1/2**0.5) <= 1e-9 and abs(rc['phase_deg'] + 45) <= 1e-6
T4 = abs(rl['mag'] - 1/2**0.5) <= 1e-9 and abs(rl['phase_deg'] + 45) <= 1e-6
L_ = [f"solar: Voc {s['Voc']:.2f} V, Isc {s['Isc']:.3f} A, Pmax {s['Pmax']:.1f} W @ Vmp {s['Vmp']:.2f} Imp {s['Imp']:.2f}, FF {s['FF']:.3f}, MPP residual {s['mpp_residual']:.2e} A",
      f"RC fc {rc['fc']:.2f} Hz: |H| {rc['mag']:.9f} phase {rc['phase_deg']:.6f}°",
      f"RL fc {rl['fc']:.4f} Hz: |H| {rl['mag']:.9f} phase {rl['phase_deg']:.6f}°",
      f"T1 solar band: {T1}", f"T2 MPP residual≤1e-6: {T2}", f"T3 RC corner: {T3}", f"T4 RL corner: {T4}",
      f"P1 VERDICT: {'ALL PASS → ADOPT' if (T1 and T2 and T3 and T4) else 'FAIL'}"]
open('field_tests/results/p1_power.txt', 'w').write('\n'.join(L_) + '\n'); print('\n'.join(L_))
