# Deviations for PREREG_D437_FI_TOY
D1 (19:08 CT, reporting bug fix before scoring): (i) the "minimum x after the first reflection" included the segment before the first
reflection (it reported the start value 27.178); now only times after the first reflection are used. (ii) The bounce loop stopped at a
cap of 60 reflections (the field was chattering against the wall); now it stops when the reflected speed is below 10⁻⁹ (x resting on the
wall) or after 5000 bounces. Physics, parameters and reading unchanged. First-run output kept in results/toy_fi_d437.txt for the record.
