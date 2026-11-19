# PREREG: SERAPIS circuit, layer 9 "CM" (complex multiplication), written before the first run
Danny 2026-11-19 19:20 CT: "Move to new layer". Exact mathematical identities, not physics predictions. Pure mpmath (60 digits), no tool calls.
Laws and tolerances (fixed now):
1. down CM→A2: |j(ρ)| < 1e-40 (SERAPIS-E vacuum ρ = zero of j).
2. up Moonshine→CM: j(i) = 1728 to 1e-40 relative AND Moonshine's series j_at_i within 1e-3.
3. elliptic points: |S·i − i|, |ST·ρ − ρ| < 1e-40; S² = −I, (ST)³ = ±I.
4. Heegner (literature: Baker–Heegner–Stark list 3,4,7,8,11,19,43,67,163): j = k³ with k = 0,12,−15,20,−32,−96,−960,−5280,−640320, rel. tol 1e-30.
5. up Moonshine→CM: e^{π√163} = 640320³ + 744 − δ, 0 < δ < 1e-12, with c₀ = 744 from the Moonshine wire.
6. control: D = 15 (class number 2): fractional part of Re j > 1e-3.
7. Chudnovsky first term (literature constant 13591409): |640320^{3/2}/(12·13591409) − π| < 1e-13.
Code: apps/aegis_studio/circuit.py (CM layout, wires, laws).
