@echo off
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
