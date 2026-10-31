#!/bin/bash
# Quick check that AxiCLASS (classy) works in the 'aegis' micromamba environment. Logged to smoke_test.log.
set -euo pipefail
HERE=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
exec > >(tee "$HERE/smoke_test.log") 2>&1
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$("$HOME/bin/micromamba" shell hook -s bash)"
micromamba activate aegis
python - <<'EOF'
import numpy, cobaya
from classy import Class
c = Class()
c.set({"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.12,
       "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544})
c.compute()
cl = c.lensed_cl(2500)
print("AxiCLASS OK: H0 = %.2f  sigma8 = %.4f  100*theta_s = %.5f  D_l(TT, l=220) = %.0f muK^2" % (
    c.h() * 100, c.sigma8(), 100 * c.theta_s_100() / 100 if hasattr(c, "theta_s_100") else float("nan"),
    220 * 221 / (2 * numpy.pi) * cl["tt"][220] * (2.7255e6) ** 2))
print("numpy", numpy.__version__, "cobaya", cobaya.__version__)
c.struct_cleanup()
EOF
