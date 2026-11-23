# HEX-1 deviations (written after the first build run, before the locked tests run)
DEV-1 (physics, nuclear node): the proton-mass shift fed weave_proton with dmq/Lambda (the change of m_q/Lambda_QCD), but
weave_proton takes the change of the light-quark mass at fixed Lambda. Most of m_p scales with Lambda, so the -8.6 MeV printed in the
build run is not meaningful. The proton-mass shift is removed from N1 until a Lambda-consistent formula is wired (H5 reports it as
"not wired" instead of a number).
DEV-2 (nuclear pulls): BBN pulls use the observational error and the PRIMAT theory error in quadrature (janus_astro.bbn.sigma);
the build run used the observational error only (D/H pull -3.95 then).
DEV-3 (labelling): the Hoyle-window test takes the model's alpha_s shift as if it were the real one. It restates the forces node's
alpha_s tension in nuclear terms; it is NOT an independent constraint, and the board says so.
