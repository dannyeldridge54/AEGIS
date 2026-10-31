@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: c9b0f5262bd44e13
cd /d "%~dp0"
(
echo === python ===
where python
python --version
python -c "import numpy, scipy; print('numpy', numpy.__version__, 'scipy', scipy.__version__)"
echo === node ===
where node
node --version
) > env_check.txt 2>&1
