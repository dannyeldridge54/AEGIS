"""S1 sound engine (lock PREREG_S1). numpy synthesis → 16-bit PCM WAV. Label: art/analogy (sonification).
Real frequency ratios (e.g. Balmer) are scaled into the audible range by a stated factor; nothing here is a physical claim."""
import json, wave, math, pathlib
import numpy as np
SR = 44100
def _osc(freq, t, kind='sine'):
    ph = 2*np.pi*freq*t
    if kind == 'sine': return np.sin(ph)
    if kind == 'saw': return 2*(freq*t - np.floor(0.5 + freq*t))
    if kind == 'square': return np.sign(np.sin(ph))
    if kind == 'triangle': return 2*np.abs(2*(freq*t - np.floor(0.5 + freq*t))) - 1
    raise ValueError(kind)
def adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    A, D, R = int(a*SR), int(d*SR), int(r*SR); S = max(0, n - A - D - R); env = np.ones(n)
    if A: env[:A] = np.linspace(0, 1, A)
    if D: env[A:A+D] = np.linspace(1, s, D)
    env[A+D:A+D+S] = s
    if R: env[A+D+S:] = np.linspace(s, 0, n - A - D - S)
    return env
def note(freq, dur, kind='sine', amp=0.5, vib=0.0, env=True):
    t = np.arange(int(dur*SR))/SR; f = freq*(1 + vib*np.sin(2*np.pi*5*t)) if vib else freq
    y = amp*_osc(f, t, kind)
    return y*adsr(len(y)) if env else y
def glide(freqs, dur, kind='sine', amp=0.5, vib=0.0):
    n = int(dur*SR); t = np.arange(n)/SR; f = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(freqs)), freqs)
    ph = 2*np.pi*np.cumsum(f*(1 + vib*np.sin(2*np.pi*5*t)))/SR
    return amp*np.sin(ph)*adsr(n, a=0.05, d=0.1, s=0.9, r=0.3)
def map_series(values, lo_hz=180.0, hi_hz=440.0, invert=False):
    v = np.asarray(values, float); lo, hi = v.min(), v.max(); u = (v - lo)/((hi - lo) or 1)
    if invert: u = 1 - u
    return lo_hz*(hi_hz/lo_hz)**u   # log (musical) mapping
def mix(layers, dur):
    n = int(dur*SR); out = np.zeros(n)
    for y in layers: out[:len(y)] += y[:n]
    return out
def softclip(y): return np.tanh(y)
def write_wav(path, y, stereo=True):
    y = softclip(y); y = y/(np.max(np.abs(y)) or 1)*0.95; pcm = (y*32767).astype('<i2')
    data = np.column_stack([pcm, pcm]).ravel() if stereo else pcm
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2 if stereo else 1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
    return dict(path=str(path), sr=SR, dur=len(y)/SR, peak=float(np.max(np.abs(y))), rms=float(np.sqrt(np.mean(y*y))), channels=2 if stereo else 1)
