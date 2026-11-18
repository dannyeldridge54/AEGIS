# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Wavelength, power and sound tools vs published values and exact identities."""
import math, wave
from tools.chem import wavelength as W
from tools.power import circuits as P
from tools.sound import engine as S

def test_lyman_alpha_vs_nist():                     # NIST ASD: H Ly-alpha 121.567 nm (vacuum); Bohr omits fine structure (~1e-5)
    assert abs(W.line('H', 1, 2)/121.5670 - 1) < 2e-5

def test_h_alpha_in_air_vs_nist():                  # NIST ASD: H-alpha 656.279 nm (air)
    assert abs(W.air(W.line('H', 2, 3)) - 656.279) < 0.015

def test_21cm_ch1b():                               # measured 1420.405751768 MHz (Hellwig+ 1970); lock CH1b |rel| < 1e-4
    assert abs(W.hydrogen_21cm()/1420405751.768 - 1) < 1e-4

def test_convert_bands():
    assert W.convert(lam_m=0.21)['band'] == 'radio' and W.convert(lam_m=650e-9)['colour'] == 'red'

def test_rc_corner_exact():                         # at f = 1/(2 pi R C): |H| = 1/sqrt 2, phase = -45 deg
    R, C = 1000.0, 1e-6; f = 1/(2*math.pi*R*C); r = P.rc_lowpass(f, R, C)
    assert abs(r['mag'] - 2**-0.5) < 1e-12 and abs(r['phase_deg'] + 45) < 1e-9

def test_solar_panel_sane():                        # 60-cell single-diode module: fill factor 0.70-0.85, Isc just below Iph, MPP solved
    r = P.solar_iv(); assert 0.70 < r['FF'] < 0.85 and 0.99*8.8 < r['Isc'] <= 8.8 and r['mpp_residual'] < 1e-9

def test_wav_file(tmp_path):
    p = tmp_path/'t.wav'; info = S.write_wav(p, S.note(440.0, 0.5))
    with wave.open(str(p)) as w: assert w.getframerate() == 44100 and w.getnchannels() == 2 and w.getnframes() == int(0.5*44100)
