@echo off
rem Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: c9b0f5262bd44e13
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
