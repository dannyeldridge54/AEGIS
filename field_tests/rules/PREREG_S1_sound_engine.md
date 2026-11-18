# PREREG S1 — sound toolkit 1: WAV engine + first physics→music render
Locked 2026-11-18 07:28Z before building/testing. Label: art/analogy (a sonification; not a physical claim), except the Balmer ratios, which are real frequency ratios scaled into the audible range by a stated factor.
Build tools/sound/engine.py: numpy oscillators (sine/saw/square/triangle), ADSR envelope, additive mix, soft-clip, 16-bit PCM WAV writer (stdlib wave), 44100 Hz; plus map_series(values, lo_hz, hi_hz) → pitch track, and note(freq, dur).
Render field_tests/results/s1_demo.wav (two layers, ~8 s):
 (a) torus glide: y(N) from docs/web/string_geom.json mapped high→low y to 440→180 Hz (inflation long tube → round torus), sine + slow vibrato;
 (b) Balmer chord: Hα:Hβ:Hγ:Hδ frequency RATIOS (456.67:616.51:690.49:730.68 THz) scaled by 1/1.0377e12 into 440.0–704.0 Hz, four detuned saws, soft envelope.
Pre-stated tests: T1 file is RIFF/WAVE, 44100 Hz, 16-bit, mono/stereo; T2 duration 8.0 s ± 0.1; T3 peak ≤ 1.0 (no hard clip) and RMS > 0.02 (not silent); T4 the four Balmer tones' measured FFT peaks match the scaled ratios to ≤ 1 %.
Adopt the engine (and register sound_render) if T1–T4 pass. Results: field_tests/results/s1_sound.txt + s1_demo.wav.
