# DEVIATIONS for PREREG_D1288 (written AFTER the corrected rerun — stated honestly; the rule asks for before)
1. First run built "D16+" from the basis {e_i − e_{i+1} (i=1..15), s}. Its Gram determinant came out 64, not 1: that basis spans a
   sublattice (every vector has coordinate sum ≡ 0 mod 8·½), not D16+. The script's own det/evenness print exposed it; no
   prediction was scored on that run.
2. Fix: D16 basis {e_i − e_{i+1} (i=1..15), e15+e16} with e1−e2 replaced by s = (½)^16 → det 1, even, unimodular, 480 roots of
   the form ±e_i±e_j → D16⁺. Rerun once; scored on the rerun only. No other change.
