# AEGIS-FP RJPCULNHJ4K2SRNU · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Level 7: distances to data (values as used in the D-notes; update here only with a sourced D-note)."""
DATA = {'CMB-SPA': (0.9684, 0.0030), 'CMB-SPA+DESI': (0.9728, 0.0027)}
R_LIMIT = 0.036
def sigma(ns):
    return {k: (ns-m)/s for k, (m, s) in DATA.items()}
