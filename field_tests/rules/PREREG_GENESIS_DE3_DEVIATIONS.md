# DEVIATIONS — PREREG_GENESIS_DE3
D1: the run finished its computation but crashed on JSON output (numpy int64), so no result was seen. Fix: json.dumps(..., default=float). Nothing else changed.
