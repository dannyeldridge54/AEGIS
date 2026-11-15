# AION audit of the AEGIS repository (2026-11-15)

Command: `aion check --repo .` (AION 0.1.0, tools/aion). Rule: a result file is OK when a PREREG file with the same D-number was committed no later than it.

```
summary: NO_ID 133, NO_LOCK 66, OK 184
```

- **OK**: preceded by its lock. **NO_LOCK**: a D-numbered result with no PREREG of that number (mostly early exploratory notes, D72–D521 era, written before locking became mandatory). **NO_ID**: file name carries no D-number, so it cannot be matched (mostly the pre-SERAPIS Twist v1–v7 score files). **LATE**: none.
- No HASH_MISMATCH: no locked rule was edited after hashing.

## Results with a D-number but no lock
```
34  field_tests/results/audit_D13_D34_reruns.txt
47  field_tests/results/audit_D35_D47.txt
170  field_tests/results/bao_ratios_d170.txt
116  field_tests/results/cc_field_dependent_d116.txt
118  field_tests/results/chi_saturating_d118.txt
128  field_tests/results/chi_su2_d128.txt
287  field_tests/results/chi_weight32_d287.txt
178  field_tests/results/companion_d178.txt
268  field_tests/results/coupling_alt_d268.txt
268  field_tests/results/coupling_alt_d268_coarse.txt
118  field_tests/results/crossing_angle_d118.txt
175  field_tests/results/fano_rung3_d175.txt
177  field_tests/results/g2_split_d177.txt
179  field_tests/results/g2_split_search_d179.txt
112  field_tests/results/gaps_d112.txt
181  field_tests/results/gkly_compatible_d181.txt
180  field_tests/results/gkly_exact_split_d180.txt
186  field_tests/results/gs_dilaton_d186.txt
169  field_tests/results/h0_shift_d169.txt
185  field_tests/results/heat_window_d185.txt
153  field_tests/results/heterotic_cliff_d153.txt
164  field_tests/results/heterotic_coupling_d164.txt
152  field_tests/results/heterotic_z3_d152.txt
183  field_tests/results/hw_walls_d183.txt
159  field_tests/results/kahler_cliff_d159.txt
127  field_tests/results/kahler_sqrt_d127.txt
182  field_tests/results/kappa_counts_d182.txt
168  field_tests/results/late_predictions_d168.txt
511  field_tests/results/lens_d511_neff.txt
156  field_tests/results/loop_shift_d156.txt
127  field_tests/results/matter_pc/matter_d127_form.txt
160  field_tests/results/matter_pc/matter_twistk_d160.txt
171  field_tests/results/neutrino_mimic_d171.txt
173  field_tests/results/neutrino_scale_d173.txt
108  field_tests/results/ns_routes_d108.txt
461  field_tests/results/part10d_gauge_d461.txt
464  field_tests/results/part2e_fibre_d464.txt
440  field_tests/results/part4c_numass_d440.txt
454  field_tests/results/part4d_window_d454.txt
443  field_tests/results/part7c_beta_d443.txt
457  field_tests/results/part7d_axion_f_d457.txt
295  field_tests/results/polonyi_shift_d295.txt
165  field_tests/results/quintic_n_d165.txt
126  field_tests/results/racetrack_d126.txt
259  field_tests/results/referee_fixes_d259.txt
187  field_tests/results/rung4_vs_rung3_d187.txt
151  field_tests/results/rung_tails_d151.txt
127  field_tests/results/s_mass_d127.txt
184  field_tests/results/scale_preserving_d184.txt
140  field_tests/results/scaling_shield_d140.txt
141  field_tests/results/scaling_shield_d141.txt
142  field_tests/results/shield_tests_d142.txt
143  field_tests/results/shield_vs_volume_d143.txt
172  field_tests/results/strongcp_isw_d172.txt
148  field_tests/results/su8_weak_d148.txt
269  field_tests/results/t32_gravitino_d269.txt
125  field_tests/results/tail_at_08_d125.txt
105  field_tests/results/tail_stability_d105.txt
69  field_tests/results/theory_items_D67_D69.txt
123  field_tests/results/tower_volume_d123.txt
163  field_tests/results/twistl_naturalness_d163.txt
521  field_tests/results/variants_d521.txt
167  field_tests/results/warp_shapes_d167.txt
72  field_tests/results/weak_spots_D72.txt
373  field_tests/results/weight3_stabiliser_d373.txt
298  field_tests/results/yend_precise_d298.txt
NO_ID  133,
```
