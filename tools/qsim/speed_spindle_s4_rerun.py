"""DEV-1 rerun harness for S4 (committed per DEV-4). Note: since DEV-3 the sparse path is dense below dim 5000."""
import json, time, numpy as np, sys
sys.path.insert(0, 'tools/qsim')
from loom_qsim import bh_spectrum
from spindle_fast import bh_spectrum_sparse
for case in [(5,5,0.2,1.0),(5,5,1.0,0.0),(5,5,0.0,1.0),(6,6,0.2,1.0)]:
    print(case, bh_spectrum(*case, 3)[0], bh_spectrum_sparse(*case, 3)[0])
