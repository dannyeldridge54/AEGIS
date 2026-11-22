@echo off
REM CubeMind Ramsey engine: detects this PC's cores, RAM and GPU, runs the calibration controls, then the K=10 degree-4 search.
REM GPU is used automatically if this Python has torch (CUDA) or cupy. Results: ramsey\cm\results\cm_ramsey_<PC name>.json
cd /d "%~dp0"
python -c "import numba" 2>nul || pip install numba
python cm_ramsey.py all
pause
