<!-- AEGIS-FP WI5W36IH2D6B6LVO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# DEVIATIONS — PREREG_J6_two_field_deltaN

D1 (17 Nov 04:2xZ, before any test output): first run crashed at the T1 comparison line with
AttributeError (core.spectra is a method, Model.spectra). No number was printed or seen. Fix: call m.spectra(N).
No change to method, tests or tolerances.
