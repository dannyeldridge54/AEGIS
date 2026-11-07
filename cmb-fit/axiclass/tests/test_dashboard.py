"""Include dashboard regressions in the scheduled Python test gate."""
import shutil
import subprocess
import sys
from pathlib import Path


def test_kairos_dashboard():
    script = Path(__file__).resolve().parents[3] / "ufe-v2" / "tests" / "test_candidate_filters.cjs"
    node = shutil.which("node") or shutil.which("node.exe")
    assert node, "Dashboard gate requires the existing Node runtime; no automatic installation"
    argument = str(script)
    if sys.platform == "linux" and node.lower().endswith(".exe"):
        argument = subprocess.run(
            ["wslpath", "-w", str(script)], check=True, capture_output=True, text=True
        ).stdout.strip()
    result = subprocess.run(
        [node, "--test", argument], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stdout + result.stderr
