Spindle (spin-1 simulator; part of the Potter's Wheel engine family). Theory tools for spin-1 Bose gases. Python 3.10+, numpy, scipy.
  loom_qsim.py      exact single-mode (SMA, M=0), mean-field spin-1 lattice, exact Bose-Hubbard chain, compass
  d2185_lib.py      exact spin-1 single-mode Fock-space model with drive: H = (c2/N)[N0(N-N0)+(N+-N-)^2/2] - (p/2) Sy
  validate_d2183.py checks: free bosons, Mott gap, exact vs mean field, conservation, Hermiticity
  d2184.py          period vs q for c2 = 23.7 Hz (file A); d2185.py: beta curve (file B), revival scan
  d2185_tuner.py    compass-guided knob search (file D); liu_packet_data.py: rebuilds data/ files
Run from the folder above engine/ with:  python engine/<script>.py   (paths assume the AEGIS repo layout; adjust OUT/paths as needed)
