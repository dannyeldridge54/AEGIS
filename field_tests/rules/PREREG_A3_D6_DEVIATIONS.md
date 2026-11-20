# DEVIATIONS — PREREG_A3_D6
D1: crash before any output: np.trapz was removed in this numpy. Replaced with np.trapezoid (same rule). Nothing else changed.
D2: output-only crash (numpy bool not JSON-serialisable), no result seen. Fix: default=lambda v: bool(v) if isinstance(v,(bool,)) or type(v).__name__=="bool_" else float(v).
