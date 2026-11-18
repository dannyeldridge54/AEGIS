# AEGIS-FP 6OLLQQL4OCVFUKWN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""LOCKBENCH — the AEGIS research method as code (v0.1, 17 Nov 2026).
- lock(path): verify a PREREG lock exists, its sha256 matches, and it is committed + pushed (no result may exist before this passes).
- sweep: resumable parallel sweeps with per-task wall limits (re-exported from tools/calcq/sweep.py, tested).
- ledger.record(...): every validation stores the reference's own precision next to the claimed agreement, so no claim is sharper than its reference.
- pcjob (tools/calcq/pcjob.py) + pc_runner2.sh: package and run locked jobs on Danny's PC.
Feeds CubeMind's mirror checks (the same steps, as checks an AI must pass)."""
from tools.calcq.sweep import sweep
from .core import lock_ok
from . import ledger
__version__ = '0.1.0'
