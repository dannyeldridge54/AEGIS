# PREREG D2226 — UFE pass of the D2225 result (Danny 17:27: "UFE engine on it and run like UFE"). Written before D2225 finishes, 23 Nov 2026.
Engine = the ring/hexagon engine (tools/rings/hex.py + rings.py + Bloom likelihood/BIC, the UFE v4 central map in ring form).
For the BASELINE (AS_ENGINE = 0.11446) and for EVERY stable (Db32, Db12) at tau = i from D2225 (M_s = 0.1 M_P set; if none, the baseline only):
  1. set hex.AS_ENGINE to that pair's engine alpha_s (the threshold sits at M12, so it enters the forces ring exactly where AS_ENGINE does);
  2. pulse: hex.loop() - all six rings settle, every node posts its postulates, the centre accepts only Bloom-target gains, until a NULL round;
  3. score: Bloom lnL and target with the BIC charge counted two ways - k + 0 (if the pair is later DERIVED from the Z2 x Z6p spectrum)
     and k + 2 (if the two integers are CHOSEN) - and every node's IN/EDGE/OUT via bandmap1.marks;
  4. stage map rerun with that AS_ENGINE (tag ufe_<pair>), counts reported.
Reading fixed now: a pair "balances under UFE" only if, after the pulse, A.alpha_s and A.Hoyle are IN or EDGE and no other marker gets worse
than baseline. The k + 2 target is the honest score today (the integers are not yet derived); k + 0 is the score the derivation would earn.
Referee after; DEVIATIONS before any fix; one rerun.
