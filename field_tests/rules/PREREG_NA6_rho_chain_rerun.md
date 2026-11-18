# PREREG NA6 — ρ chain rerun with the n = 1 canonical factor and m_φ = 3.17e13 (from NA3/NA5, D1235/D1237)
Locked before running. Scripts: copies of theory/modular/tr_2p1_d725.py and lepto_rho_ci_d775.py, changed ONLY in:
 - tr_2p1: can = y·√2 (was y·√(2/3)); m = 3.1746e13 (was 2.2e13).
 - lepto_rho_ci: mphi = 3.1746e13; cases' T_R taken from part 1's output; Y_B multiplied by κ = 0.9391 (D986) — stated assumption for rows with M/T_R ≥ 500; rows below 500 marked "κ unverified".
## 1. T_R direct rerun
PASS if each open row's T_R agrees with NA3's rescaled value (field_tests/results/na3_reheat_rho.txt) within 1 % (NA3 rescaled from 3-digit printed couplings), except near-threshold rows (x = M/m_φ > 0.45), which are reported only.
## 2. D775 pass fractions with corrected inputs
Same CI grid, same m1 ∈ {1e-4, 1e-3} eV, same D775 locked rule: lepto_rho PASS if every M_H = 1e12 case has a pass fraction ≥ 10 % (pair or single).
Note also the D775 case list: rows whose channel closes or opens under the new m_φ are reported (kinematics changed).
## Rules
Post-hoc; frozen predictions unchanged. No reruns to chase; deviations first. κ recheck at M/T_R < 500 is a separate lock (NA7). Results: field_tests/results/na6_rho_chain.txt.
